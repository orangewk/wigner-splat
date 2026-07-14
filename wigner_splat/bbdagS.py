"""Multimode SQUEEZED-product rho=BB^dagger reconstructor (issue #28 step 2).

The representation upgrade motivated by experiment 10: coherent-product kets
approximate a squeezed cat only slowly in K (F 0.79-0.82 at K=2-8, vs the
generic Fock control's 0.96). Here each ket factor is a displaced SQUEEZED
vacuum, so the squeezed-cat family is inside the ansatz:

    |psi> = sum_c z_c prod_m D(alpha_c^m) S(xi_c^m) |0>

    p_theta(x) = |psi_theta(x)|^2 / Z,   Z = <psi|psi>

with the LO rotation alpha -> alpha e^{-i theta}, xi -> xi e^{-2 i theta}
(bbdag.sq_coherent_wavefunction convention, tested there). At xi = 0 this
reduces exactly to bbdagM.CoherentKetState.

Everything stays closed form because the per-mode wavefunction is a complex
Gaussian  f(x) = pref * exp(-(q/2)(x - x0)^2 + i p0 x - i br bi):

  * pair overlaps <g_c|g_d> = integral conj(f_c) f_d are complex Gaussian
    integrals: with A = (conj(q_c) + q_d)/2, B = conj(q_c) x0c + q_d x0d
    + i (p0d - p0c), the overlap is P sqrt(pi/A) exp(B^2/(4A) + C);
  * d log f / d(parameter) is a POLYNOMIAL in x of degree <= 2, so the
    gradient of every overlap is the same integral with x-moments
    R1 = B/(2A), R2 = R1^2 + 1/(2A) -- no quadrature anywhere;
  * the xi = 0 phase singularity of (r, phi) is removed by writing
    nu = xi sinh|xi| / |xi| and mu = cosh|xi| (smooth functions of xi).

The NLL and its analytic gradient follow the bbdagM pattern (issue #25);
the gradient is pinned against central differences in tests/test_bbdagS.py.
"""

import numpy as np

sqrt2 = np.sqrt(2.0)


def _sinhc(s):
    """sinh(s)/s, smooth at 0."""
    small = np.abs(s) < 1e-6
    safe = np.where(small, 1.0, s)
    return np.where(small, 1.0 + s ** 2 / 6.0, np.sinh(safe) / safe)


def _sinhc_prime_over_s(s):
    """h'(s)/s with h = sinh(s)/s: (s cosh s - sinh s)/s^3, smooth (1/3 at 0)."""
    small = np.abs(s) < 1e-4
    safe = np.where(small, 1.0, s)
    val = (safe * np.cosh(safe) - np.sinh(safe)) / safe ** 3
    return np.where(small, 1.0 / 3.0 + s ** 2 / 30.0, val)


def _gauss_params(beta, zeta):
    """Complex-Gaussian parameters of f(x) = <x|D(beta)S(zeta)|0>.

    Returns (mu, nu, q, x0, p0, pref) with
    f(x) = pref exp(-(q/2)(x - x0)^2 + i p0 x - i Re(beta) Im(beta)),
    mu = cosh|zeta|, nu = zeta sinh|zeta|/|zeta| (smooth at 0),
    q = (mu + nu)/(mu - nu), x0 = sqrt2 Re beta, p0 = sqrt2 Im beta,
    pref = pi^{-1/4} (mu - nu)^{-1/2}. Identical to
    bbdag.sq_coherent_wavefunction, in the singularity-free parameterization.
    """
    beta = np.asarray(beta, complex)
    zeta = np.asarray(zeta, complex)
    s = np.abs(zeta)
    mu = np.cosh(s)
    nu = zeta * _sinhc(s)
    q = (mu + nu) / (mu - nu)
    x0 = sqrt2 * np.real(beta)
    p0 = sqrt2 * np.imag(beta)
    pref = np.pi ** -0.25 * (mu - nu) ** -0.5
    return mu, nu, q, x0, p0, pref


def sq_wavefunction(x, beta, zeta):
    """f(x) = <x|D(beta)S(zeta)|0>, broadcasting; equals bbdag's closed form."""
    _, _, q, x0, p0, pref = _gauss_params(beta, zeta)
    br, bi = np.real(beta), np.imag(beta)
    return pref * np.exp(-(q / 2) * (x - x0) ** 2 + 1j * p0 * x - 1j * br * bi)


def _pair_ABCP(params_c, params_d):
    """Exponent parameters of conj(f_c) f_d = P exp(-A x^2 + B x + C).

    params_* = (mu, nu, q, x0, p0, pref) arrays; broadcasting c against d.
    """
    _, _, qc, x0c, p0c, prefc = params_c
    _, _, qd, x0d, p0d, prefd = params_d
    A = (np.conj(qc) + qd) / 2.0
    B = np.conj(qc) * x0c + qd * x0d + 1j * (p0d - p0c)
    # the residual constant from completing each ket's phase terms:
    # -i br bi = -i x0 p0 / 2 per ket (conj flips the first ket's sign)
    C = (
        -np.conj(qc) / 2.0 * x0c ** 2
        - qd / 2.0 * x0d ** 2
        + 1j * (x0c * p0c - x0d * p0d) / 2.0
    )
    P = np.conj(prefc) * prefd
    return A, B, C, P


def _pair_moments(params_c, params_d):
    """Overlap O = <g_c|g_d> and moment ratios R1 = <x>, R2 = <x^2>.

    conj(f_c) f_d = P exp(-A x^2 + B x + C) integrates to
    O = P sqrt(pi/A) exp(B^2/(4A) + C); the x-moment ratios follow from the
    same complex Gaussian: R1 = B/(2A), R2 = R1^2 + 1/(2A).
    """
    A, B, C, P = _pair_ABCP(params_c, params_d)
    O = P * np.sqrt(np.pi / A) * np.exp(B ** 2 / (4.0 * A) + C)
    R1 = B / (2.0 * A)
    R2 = R1 ** 2 + 1.0 / (2.0 * A)
    return O, R1, R2


def _dlogf_poly_coeffs(beta, zeta):
    """Polynomial coefficients (in x) of d log f / d(real parameter).

    Returns a dict param -> (a, b, c) with d log f/d param = a + b x + c x^2,
    for param in br, bi (Re/Im beta) and zr, zi (Re/Im zeta). Derivation:

      log f = const - (1/2) log(mu - nu) - (q/2)(x - x0)^2 + i p0 x - i br bi

      d/d br = sqrt2 q (x - x0) - i bi          (linear in x)
      d/d bi = i (sqrt2 x - br)                 (linear in x)
      d/d mu = -1/(2(mu-nu)) + nu (x-x0)^2/(mu-nu)^2
      d/d nu = +1/(2(mu-nu)) - mu (x-x0)^2/(mu-nu)^2
      d mu/d zr = h(s) zr,   d mu/d zi = h(s) zi          (mu = cosh s)
      d nu/d zr = h(s) + zeta zr k(s),  d nu/d zi = i h(s) + zeta zi k(s)
      with h = sinh(s)/s, k = h'(s)/s (both smooth at s = 0).
    """
    beta = np.asarray(beta, complex)
    zeta = np.asarray(zeta, complex)
    mu, nu, q, x0, _, _ = _gauss_params(beta, zeta)
    br, bi = np.real(beta), np.imag(beta)
    s = np.abs(zeta)
    h = _sinhc(s)
    k = _sinhc_prime_over_s(s)
    zr, zi = np.real(zeta), np.imag(zeta)

    d = mu - nu
    # d log f/d mu and /d nu as (a, b, c) via (x - x0)^2 = x0^2 - 2 x0 x + x^2
    dmu = (-0.5 / d + nu * x0 ** 2 / d ** 2, -2.0 * nu * x0 / d ** 2, nu / d ** 2)
    dnu = (0.5 / d - mu * x0 ** 2 / d ** 2, 2.0 * mu * x0 / d ** 2, -mu / d ** 2)

    dmu_zr, dmu_zi = h * zr, h * zi
    dnu_zr, dnu_zi = h + zeta * zr * k, 1j * h + zeta * zi * k

    def chain(w_mu, w_nu):
        return tuple(w_mu * m + w_nu * n for m, n in zip(dmu, dnu))

    return {
        "br": (-sqrt2 * q * x0 - 1j * bi, sqrt2 * q, np.zeros_like(q)),
        "bi": (-1j * br, 1j * sqrt2 * np.ones_like(q), np.zeros_like(q)),
        "zr": chain(dmu_zr, dnu_zr),
        "zi": chain(dmu_zi, dnu_zi),
    }


class SqueezedKetState:
    """|psi> = sum_c z_c prod_m D(alpha[c,m]) S(xi[c,m]) |0>, M modes.

    z: (K,) complex. alpha, xi: (K, M) complex. xi = 0 rows reproduce
    bbdagM.CoherentKetState exactly. rho = |psi><psi|/Z is rank-1 PSD.
    """

    def __init__(self, z, alpha, xi):
        self.z = np.asarray(z, complex)
        self.alpha = np.asarray(alpha, complex)
        self.xi = np.asarray(xi, complex)

    @property
    def K(self):
        return len(self.z)

    @property
    def M(self):
        return self.alpha.shape[1]

    @classmethod
    def random_init(cls, K, M, scale=1.5, rng=None):
        rng = np.random.default_rng(rng)
        a = rng.uniform(-scale, scale, (K, M)) + 1j * rng.uniform(-scale, scale, (K, M))
        return cls(
            z=np.ones(K, complex) / np.sqrt(K),
            alpha=a,
            xi=np.zeros((K, M), complex),  # start unsqueezed
        )

    def _mode_gram(self):
        """Per-mode pair overlaps: list of (O, R1, R2), each (K, K)."""
        out = []
        for m in range(self.M):
            p = _gauss_params(self.alpha[:, m], self.xi[:, m])
            pc = tuple(np.asarray(v)[:, None] for v in p)
            pd = tuple(np.asarray(v)[None, :] for v in p)
            out.append(_pair_moments(pc, pd))
        return out

    def gram(self):
        """G[c, d] = <g_c|g_d> = prod_m O_m[c, d]."""
        G = np.ones((self.K, self.K), complex)
        for O, _, _ in self._mode_gram():
            G = G * O
        return G

    def norm_sq(self):
        return float(np.real(np.conj(self.z) @ self.gram() @ self.z))

    def psi_at(self, X, theta):
        """psi_theta(X) for samples X (S, M) at LO phases theta (M,)."""
        theta = np.asarray(theta, float)
        rot_a = self.alpha * np.exp(-1j * theta)[None, :]
        rot_x = self.xi * np.exp(-2j * theta)[None, :]
        prod = np.ones((X.shape[0], self.K), complex)
        for m in range(self.M):
            prod *= sq_wavefunction(
                X[:, m][:, None], rot_a[None, :, m], rot_x[None, :, m]
            )
        return prod @ self.z

    def overlap_with_sq_kets(self, kets_z, kets_alpha, kets_xi):
        """<psi|phi> for phi = sum_j kets_z[j] prod_m D(a) S(x) |0>, closed form."""
        kz = np.asarray(kets_z, complex)
        ka = np.asarray(kets_alpha, complex)
        kx = np.asarray(kets_xi, complex)
        G = np.ones((self.K, len(kz)), complex)
        for m in range(self.M):
            pc = tuple(
                np.asarray(v)[:, None]
                for v in _gauss_params(self.alpha[:, m], self.xi[:, m])
            )
            pd = tuple(
                np.asarray(v)[None, :]
                for v in _gauss_params(ka[:, m], kx[:, m])
            )
            O, _, _ = _pair_moments(pc, pd)
            G = G * O
        return np.conj(self.z) @ G @ kz


def _pack(state):
    return np.concatenate([
        np.real(state.z), np.imag(state.z),
        np.real(state.alpha).ravel(), np.imag(state.alpha).ravel(),
        np.real(state.xi).ravel(), np.imag(state.xi).ravel(),
    ])


def _unpack(v, K, M):
    n = K * M
    z = v[0:K] + 1j * v[K:2 * K]
    ar = v[2 * K:2 * K + n].reshape(K, M)
    ai = v[2 * K + n:2 * K + 2 * n].reshape(K, M)
    xr = v[2 * K + 2 * n:2 * K + 3 * n].reshape(K, M)
    xi_ = v[2 * K + 3 * n:2 * K + 4 * n].reshape(K, M)
    return SqueezedKetState(z=z, alpha=ar + 1j * ai, xi=xr + 1j * xi_)


def nll(state, data):
    """Mean per-sample negative log likelihood over all angle groups."""
    Z = state.norm_sq()
    tot, n = 0.0, 0
    for theta, X in data:
        p = np.abs(state.psi_at(np.asarray(X, float), theta)) ** 2 / Z
        tot += -np.sum(np.log(np.maximum(p, 1e-300)))
        n += len(X)
    return tot / n


def _nll_grad_fd(v, K, M, data, eps=1e-6):
    g = np.zeros_like(v)
    for i in range(len(v)):
        vp = v.copy(); vp[i] += eps
        vm = v.copy(); vm[i] -= eps
        g[i] = (nll(_unpack(vp, K, M), data) - nll(_unpack(vm, K, M), data)) / (2 * eps)
    return g


def _z_block(state):
    """Z = <psi|psi> and its closed-form gradient (rotation invariant).

    Returns (Z, dZ_zr, dZ_zi, dZ) with dZ a dict over ("ar", "ai", "xr",
    "xi") of (K, M) arrays: dZ/d(ket e param) = 2 Re sum_d W[e,d]
    (conj(a_e) + conj(b_e) R1_m[e,d] + conj(c_e) R2_m[e,d]) with
    W = conj(z) z^T * G -- the overlap-moment identity of the module
    docstring. Shared by the pure and lossy NLL gradients.
    """
    z, alpha, xi = state.z, state.alpha, state.xi
    K, M = state.K, state.M
    mode_gram = state._mode_gram()
    G = np.ones((K, K), complex)
    for O, _, _ in mode_gram:
        G = G * O
    Gz = G @ z
    Z = float(np.real(np.conj(z) @ Gz))
    dZ_zr = 2.0 * np.real(Gz)
    dZ_zi = 2.0 * np.imag(Gz)
    W = np.conj(z)[:, None] * z[None, :] * G
    dZ = {p: np.zeros((K, M)) for p in ("ar", "ai", "xr", "xi")}
    for m in range(M):
        _, R1, R2 = mode_gram[m]
        coeffs = _dlogf_poly_coeffs(alpha[:, m], xi[:, m])
        for p_out, p_in in (("ar", "br"), ("ai", "bi"), ("xr", "zr"), ("xi", "zi")):
            a, b, c = coeffs[p_in]
            term = (
                np.conj(a)[:, None] + np.conj(b)[:, None] * R1
                + np.conj(c)[:, None] * R2
            )
            dZ[p_out][:, m] = 2.0 * np.real(np.sum(W * term, axis=1))
    return Z, dZ_zr, dZ_zi, dZ


def nll_and_grad(state, data):
    """Mean NLL and closed-form gradient w.r.t. the packed real parameters.

    Sample term: bbdagM pattern with the squeezed d log f (evaluated at the
    sample x), pulled back through the LO rotations (angle theta for alpha,
    2 theta for xi). Z term: dZ/d(ket e param) = 2 Re sum_d W[e,d]
    (conj(a_e) + conj(b_e) R1_m[e,d] + conj(c_e) R2_m[e,d]) with
    W = conj(z) z^T * G -- the overlap-moment identity described in the
    module docstring, at theta = 0 (Z is rotation invariant).
    """
    z, alpha, xi = state.z, state.alpha, state.xi
    K, M = state.K, state.M

    Z, dZ_zr, dZ_zi, dZ = _z_block(state)

    # --- sample term ---
    g_zr = np.zeros(K)
    g_zi = np.zeros(K)
    g = {p: np.zeros((K, M)) for p in ("ar", "ai", "xr", "xi")}
    logpsi_sum, n = 0.0, 0
    for theta, X in data:
        theta = np.asarray(theta, float)
        X = np.asarray(X, float)
        rot_a = alpha * np.exp(-1j * theta)[None, :]
        rot_x = xi * np.exp(-2j * theta)[None, :]
        prod = np.ones((X.shape[0], K), complex)
        for m in range(M):
            prod *= sq_wavefunction(
                X[:, m][:, None], rot_a[None, :, m], rot_x[None, :, m]
            )
        psi = prod @ z
        absq = np.abs(psi) ** 2
        logpsi_sum += np.sum(np.log(np.maximum(absq, 1e-300)))
        n += X.shape[0]
        r = np.conj(psi) / np.maximum(absq, 1e-300)
        T = r[:, None] * prod
        g_zr += -2.0 * np.sum(np.real(T), axis=0)
        g_zi += 2.0 * np.sum(np.imag(T), axis=0)
        A_ = T * z[None, :]                                    # (S, K)
        for m in range(M):
            coeffs = _dlogf_poly_coeffs(rot_a[:, m], rot_x[:, m])
            xm = X[:, m][:, None]
            dlog = {}
            for p, (a, b, c) in coeffs.items():
                dlog[p] = a[None, :] + b[None, :] * xm + c[None, :] * xm ** 2
            ca, sa = np.cos(theta[m]), np.sin(theta[m])
            c2, s2 = np.cos(2 * theta[m]), np.sin(2 * theta[m])
            rots = {
                "ar": ca * dlog["br"] - sa * dlog["bi"],
                "ai": sa * dlog["br"] + ca * dlog["bi"],
                "xr": c2 * dlog["zr"] - s2 * dlog["zi"],
                "xi": s2 * dlog["zr"] + c2 * dlog["zi"],
            }
            for p, dv in rots.items():
                g[p][:, m] += -2.0 * np.sum(np.real(A_ * dv), axis=0)

    value = np.log(Z) - logpsi_sum / n
    grad = np.concatenate([
        g_zr / n + dZ_zr / Z,
        g_zi / n + dZ_zi / Z,
        (g["ar"] / n + dZ["ar"] / Z).ravel(),
        (g["ai"] / n + dZ["ai"] / Z).ravel(),
        (g["xr"] / n + dZ["xr"] / Z).ravel(),
        (g["xi"] / n + dZ["xi"] / Z).ravel(),
    ])
    return value, grad


def fit_bbdagS(data, K=4, M=3, iters=200, lr=0.05, seed=0, callback=None):
    """Adam on the analytic squeezed-ket NLL gradient. Physical by construction."""
    state = SqueezedKetState.random_init(K, M, rng=seed)
    v = _pack(state)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        val, grd = nll_and_grad(_unpack(v, K, M), data)
        m1 = 0.9 * m1 + 0.1 * grd
        m2 = 0.999 * m2 + 0.001 * grd ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 25 == 0:
            callback(t, nll(_unpack(v, K, M), data))
    return _unpack(v, K, M)


# ---------------------------------------------------------------------------
# Detection-efficiency (loss) forward model -- issue #42.
#
# Homodyne detection with efficiency eta measures X_meas = sqrt(eta) X +
# sqrt(1 - eta) X_vac (X_vac ~ N(0, 1/2) in this repo's vacuum-variance-1/2
# convention), optionally plus electronic noise of variance extra_noise_var.
# The measured pdf is therefore the pure-model pdf convolved with a Gaussian:
#
#   p_eta(x) = int p(y) N(x - sqrt(eta) y; sigma2) dy,
#   sigma2 = (1 - eta)/2 + extra_noise_var,
#
# which is EXACTLY the homodyne marginal of the state after a transmissivity-
# eta loss channel. Everything stays closed form: per pair (c, d) of kets,
# conj(f_c) f_d = P exp(-A y^2 + B y + C), and the convolution just tilts the
# Gaussian --
#
#   A' = A + eta/(2 sigma2),   B'(x) = B + (sqrt(eta)/sigma2) x,
#   O_cd(x) = P / sqrt(2 pi sigma2) * sqrt(pi/A')
#             * exp(B'^2/(4A') + C - x^2/(2 sigma2)),
#
# so p_eta(x) = sum_cd conj(z_c) z_d prod_m O_cd^m(x_m) / Z with Z unchanged
# (loss is trace preserving; integrating O_cd over x recovers the pure
# overlap). Gradients reuse the d log f polynomial trick with the TILTED
# moment ratios R1' = B'/(2A'), R2' = R1'^2 + 1/(2A') -- the same identity
# that powers the pure Z gradient, now applied per sample per pair.
# The model rho = loss_eta(|psi><psi|/Z) is PSD by construction (a CPTP map
# of a PSD state); the fitted |psi> is the loss-corrected pure estimate.
# ---------------------------------------------------------------------------


def _lossy_mode_pair_density(params, x, eta, sigma2):
    """Per-mode pair densities O(x) and tilted moments R1, R2, all (S, K, K).

    params = (mu, nu, q, x0, p0, pref) arrays of shape (K,) for one mode
    (already LO rotated); x is the (S,) measured quadratures of that mode.
    """
    pc = tuple(np.asarray(v)[:, None] for v in params)
    pd = tuple(np.asarray(v)[None, :] for v in params)
    A, B, C, P = _pair_ABCP(pc, pd)
    Ap = A + eta / (2.0 * sigma2)
    x = np.asarray(x, float)[:, None, None]
    Bp = B[None, :, :] + (np.sqrt(eta) / sigma2) * x
    expo = Bp ** 2 / (4.0 * Ap[None, :, :]) + C[None, :, :] - x ** 2 / (2.0 * sigma2)
    O = (
        P[None, :, :] / np.sqrt(2.0 * np.pi * sigma2)
        * np.sqrt(np.pi / Ap)[None, :, :] * np.exp(expo)
    )
    R1 = Bp / (2.0 * Ap[None, :, :])
    R2 = R1 ** 2 + 1.0 / (2.0 * Ap[None, :, :])
    return O, R1, R2


def _rot_coeff_triples(alpha_rot_m, xi_rot_m, theta_m):
    """d log f coefficient triples in LAB-frame params (ar, ai, xr, xi).

    Combines _dlogf_poly_coeffs (evaluated at the rotated ket params) with
    the LO rotation chain (theta for alpha, 2 theta for xi) at the triple
    level -- the rotation is linear, so it commutes with evaluating at x.
    """
    coeffs = _dlogf_poly_coeffs(alpha_rot_m, xi_rot_m)
    ca, sa = np.cos(theta_m), np.sin(theta_m)
    c2, s2 = np.cos(2.0 * theta_m), np.sin(2.0 * theta_m)

    def comb(u, v, cu, cv):
        return tuple(cu * a + cv * b for a, b in zip(coeffs[u], coeffs[v]))

    return {
        "ar": comb("br", "bi", ca, -sa),
        "ai": comb("br", "bi", sa, ca),
        "xr": comb("zr", "zi", c2, -s2),
        "xi": comb("zr", "zi", s2, c2),
    }


def lossy_pdf(state, X, theta, eta, extra_noise_var=0.0):
    """Measured pdf p_eta(X) (S,) under detection efficiency eta + noise."""
    sigma2 = (1.0 - eta) / 2.0 + extra_noise_var
    Z = state.norm_sq()
    X = np.asarray(X, float)
    theta = np.asarray(theta, float)
    if sigma2 <= 1e-14:
        return np.abs(state.psi_at(X, theta)) ** 2 / Z
    rot_a = state.alpha * np.exp(-1j * theta)[None, :]
    rot_x = state.xi * np.exp(-2j * theta)[None, :]
    Q = np.ones((X.shape[0], state.K, state.K), complex)
    for m in range(state.M):
        O, _, _ = _lossy_mode_pair_density(
            _gauss_params(rot_a[:, m], rot_x[:, m]), X[:, m], eta, sigma2
        )
        Q *= O
    num = np.real(np.einsum("c,scd,d->s", np.conj(state.z), Q, state.z))
    return np.maximum(num, 0.0) / Z


def nll_lossy(state, data, eta, extra_noise_var=0.0):
    """Mean per-sample NLL of the measured (lossy) pdf."""
    tot, n = 0.0, 0
    for theta, X in data:
        p = lossy_pdf(state, X, theta, eta, extra_noise_var)
        tot += -np.sum(np.log(np.maximum(p, 1e-300)))
        n += len(np.asarray(X))
    return tot / n


def nll_and_grad_lossy(state, data, eta, extra_noise_var=0.0, chunk=8192):
    """Mean lossy NLL and closed-form gradient w.r.t. the packed state params.

    Same packing as nll_and_grad; eta is NOT part of the gradient (fit it in
    fit_bbdagS_lossy via a cheap scalar finite difference). Structure: the Z
    term is shared with the pure case (_z_block); the sample term is the
    pure pattern lifted from per-ket to per-PAIR, with the tilted moment
    ratios R1', R2' replacing the pointwise polynomial evaluation. Samples
    are processed in chunks to bound the (S, K, K) intermediates.
    """
    sigma2 = (1.0 - eta) / 2.0 + extra_noise_var
    if sigma2 <= 1e-14:
        return nll_and_grad(state, data)
    z, alpha, xi = state.z, state.alpha, state.xi
    K, M = state.K, state.M
    Z, dZ_zr, dZ_zi, dZ = _z_block(state)
    zz = np.conj(z)[:, None] * z[None, :]

    g_zr = np.zeros(K)
    g_zi = np.zeros(K)
    g = {p: np.zeros((K, M)) for p in ("ar", "ai", "xr", "xi")}
    lognum_sum, n = 0.0, 0
    for theta, X in data:
        theta = np.asarray(theta, float)
        X = np.asarray(X, float)
        rot_a = alpha * np.exp(-1j * theta)[None, :]
        rot_x = xi * np.exp(-2j * theta)[None, :]
        mode_params = [
            _gauss_params(rot_a[:, m], rot_x[:, m]) for m in range(M)
        ]
        mode_triples = [
            _rot_coeff_triples(rot_a[:, m], rot_x[:, m], theta[m])
            for m in range(M)
        ]
        n += X.shape[0]
        for s0 in range(0, X.shape[0], chunk):
            Xc = X[s0:s0 + chunk]
            per_mode = [
                _lossy_mode_pair_density(mode_params[m], Xc[:, m], eta, sigma2)
                for m in range(M)
            ]
            Q = np.ones((Xc.shape[0], K, K), complex)
            for O, _, _ in per_mode:
                Q *= O
            num = np.maximum(
                np.real(np.einsum("c,scd,d->s", np.conj(z), Q, z)), 1e-300
            )
            lognum_sum += np.sum(np.log(num))
            inv = 1.0 / num
            Qz = np.einsum("scd,d->sc", Q, z)
            g_zr += -2.0 * np.sum(np.real(Qz) * inv[:, None], axis=0)
            g_zi += -2.0 * np.sum(np.imag(Qz) * inv[:, None], axis=0)
            Wn = zz[None, :, :] * Q * inv[:, None, None]
            for m in range(M):
                _, R1, R2 = per_mode[m]
                for p, (a, b, c) in mode_triples[m].items():
                    E = (
                        np.conj(a)[None, :, None]
                        + np.conj(b)[None, :, None] * R1
                        + np.conj(c)[None, :, None] * R2
                    )
                    g[p][:, m] += -2.0 * np.sum(np.real(Wn * E), axis=(0, 2))

    value = np.log(Z) - lognum_sum / n
    grad = np.concatenate([
        g_zr / n + dZ_zr / Z,
        g_zi / n + dZ_zi / Z,
        (g["ar"] / n + dZ["ar"] / Z).ravel(),
        (g["ai"] / n + dZ["ai"] / Z).ravel(),
        (g["xr"] / n + dZ["xr"] / Z).ravel(),
        (g["xi"] / n + dZ["xi"] / Z).ravel(),
    ])
    return value, grad


def fit_bbdagS_lossy(data, K=4, M=1, eta0=0.8, fit_eta=True,
                     extra_noise_var=0.0, iters=300, lr=0.05, seed=0,
                     callback=None):
    """Adam on the lossy NLL; returns (state, eta). Physical by construction.

    eta is optimized (when fit_eta) through a logit reparameterization
    t -> 1/(1 + e^{-t}) so it stays in (0, 1), with a central finite
    difference in t (a single scalar -- two extra forward passes per
    iteration; the state gradient stays fully analytic).
    """
    state = SqueezedKetState.random_init(K, M, rng=seed)
    v = _pack(state)
    t = float(np.log(eta0 / (1.0 - eta0)))
    m1, m2 = np.zeros(len(v) + 1), np.zeros(len(v) + 1)
    h = 1e-4
    for it in range(1, iters + 1):
        st = _unpack(v, K, M)
        eta = 1.0 / (1.0 + np.exp(-t))
        val, grd = nll_and_grad_lossy(st, data, eta, extra_noise_var)
        if fit_eta:
            ep = 1.0 / (1.0 + np.exp(-(t + h)))
            em = 1.0 / (1.0 + np.exp(-(t - h)))
            g_t = (nll_lossy(st, data, ep, extra_noise_var)
                   - nll_lossy(st, data, em, extra_noise_var)) / (2.0 * h)
        else:
            g_t = 0.0
        grd = np.concatenate([grd, [g_t]])
        m1 = 0.9 * m1 + 0.1 * grd
        m2 = 0.999 * m2 + 0.001 * grd ** 2
        step = lr * (m1 / (1 - 0.9 ** it)) / (np.sqrt(m2 / (1 - 0.999 ** it)) + 1e-8)
        v -= step[:-1]
        t -= step[-1]
        if callback and it % 25 == 0:
            eta_now = 1.0 / (1.0 + np.exp(-t))
            callback(it, nll_lossy(_unpack(v, K, M), data, eta_now,
                                   extra_noise_var), eta_now)
    return _unpack(v, K, M), 1.0 / (1.0 + np.exp(-t))


def fidelity_vs_squeezed_cat3(state, alpha, parity=+1, r=0.0):
    """Exact |<psi|target>|^2/(Z Z_t) vs the squeezed cat, all closed form.

    target = prod_m D(a)S(r)|0> + parity prod_m D(-a)S(r)|0> (M = state.M).
    At r = 0 this is the coherent cat3 (bbdagM.fidelity_vs_cat3 agreement is
    pinned in tests).
    """
    M = state.M
    a = float(alpha)
    kets_alpha = np.array([[a] * M, [-a] * M], complex)
    kets_xi = np.full((2, M), complex(r))
    kets_z = np.array([1.0, parity], complex)
    ov = state.overlap_with_sq_kets(kets_z, kets_alpha, kets_xi)
    # <target|target> via the same pair-overlap closed form
    target = SqueezedKetState(kets_z, kets_alpha, kets_xi)
    return float(np.abs(ov) ** 2 / (state.norm_sq() * target.norm_sq()))
