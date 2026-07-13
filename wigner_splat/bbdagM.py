"""Multimode rho=BB^dagger reconstructor (coherent-product kets), issue #8.

The multimode lift of bbdag.py, specialized to COHERENT product kets (no
squeeze) -- the minimal ansatz that can represent the entangled three-mode cat,
which is exactly a rank-2 superposition of two product coherent states
|a,a,a> + parity|-a,-a,-a> (see states3.ThreeModeCat.homodyne_pdf). Squeeze is a
strict generalization added later if this is not enough.

Ansatz (M modes):

    |psi> = sum_c z_c  prod_m |alpha_c^m>,      |alpha_c^m> coherent

    p_theta(x) = |psi_theta(x)|^2 / Z,    Z = <psi|psi>

with psi_theta(x) = sum_c z_c prod_m <x_m | alpha_c^m e^{-i theta_m}> and every
quantity closed-form: the coherent overlap <alpha|beta> =
exp(-|alpha|^2/2 - |beta|^2/2 + conj(alpha) beta) gives Z and the state fidelity
against any coherent-superposition target WITHOUT a phase-space grid. Physicality
is automatic (rho = |psi><psi|/Z is rank-1 PSD).

Loss is the per-sample NLL (no binning): the marginal is |.|^2/Z >= 0 and
normalized by construction, so unlike forward3f there is no nonnegativity or
sum penalty to add.
"""

import numpy as np

from .states import coherent_wavefunction


def coherent_overlap(a, b):
    """<a|b> = exp(-|a|^2/2 - |b|^2/2 + conj(a) b), elementwise on complex arrays."""
    return np.exp(-0.5 * np.abs(a) ** 2 - 0.5 * np.abs(b) ** 2 + np.conj(a) * b)


class CoherentKetState:
    """|psi> = sum_c z_c prod_m |alpha[c, m]>, M-mode coherent-product superposition.

    z: (K,) complex amplitudes. alpha: (K, M) complex per-mode displacements.
    """

    def __init__(self, z, alpha):
        self.z = np.asarray(z, complex)
        self.alpha = np.asarray(alpha, complex)  # (K, M)

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
        return cls(z=np.ones(K, complex) / np.sqrt(K), alpha=a)

    def norm_sq(self):
        """Z = <psi|psi> = sum_{c,d} conj(z_c) z_d prod_m <alpha_c^m|alpha_d^m>."""
        # G[c, d] = prod_m <alpha[c,m]|alpha[d,m]>
        ov = coherent_overlap(self.alpha[:, None, :], self.alpha[None, :, :])  # (K,K,M)
        G = np.prod(ov, axis=2)  # (K, K)
        return np.real(np.conj(self.z) @ G @ self.z)

    def psi_at(self, X, theta):
        """psi_theta(X) for samples X (S, M) at LO phases theta (M,).

        Returns (S,) complex amplitude sum_c z_c prod_m <x_m|alpha_c^m e^{-i theta_m}>.
        """
        rot = self.alpha * np.exp(-1j * np.asarray(theta))[None, :]  # (K, M)
        # f[s, c, m] = <X[s,m] | rot[c,m]>
        S = X.shape[0]
        prod = np.ones((S, self.K), complex)
        for m in range(self.M):
            # coherent_wavefunction broadcasts (S,1) x (1,K) -> (S,K)
            fm = coherent_wavefunction(X[:, m][:, None], rot[None, :, m])
            prod *= fm
        return prod @ self.z  # (S,)

    def overlap_with(self, kets_z, kets_alpha):
        """<psi | phi> for phi = sum_j kets_z[j] prod_m |kets_alpha[j, m]>.

        Closed form via coherent overlaps; used for exact state fidelity.
        """
        ka = np.asarray(kets_alpha, complex)  # (J, M)
        kz = np.asarray(kets_z, complex)      # (J,)
        ov = coherent_overlap(self.alpha[:, None, :], ka[None, :, :])  # (K, J, M)
        G = np.prod(ov, axis=2)  # (K, J)
        return np.conj(self.z) @ G @ kz


def _pack(state):
    return np.concatenate([
        np.real(state.z), np.imag(state.z),
        np.real(state.alpha).ravel(), np.imag(state.alpha).ravel(),
    ])


def _unpack(v, K, M):
    z = v[0:K] + 1j * v[K:2 * K]
    ar = v[2 * K:2 * K + K * M].reshape(K, M)
    ai = v[2 * K + K * M:2 * K + 2 * K * M].reshape(K, M)
    return CoherentKetState(z=z, alpha=ar + 1j * ai)


def nll(state, data):
    """Mean per-sample negative log likelihood over all angle triples."""
    Z = state.norm_sq()
    tot = 0.0
    n = 0
    for theta, X in data:
        p = np.abs(state.psi_at(X, theta)) ** 2 / Z
        tot += -np.sum(np.log(np.maximum(p, 1e-300)))
        n += len(X)
    return tot / n


def _nll_grad_fd(v, K, M, data, eps=1e-5):
    g = np.zeros_like(v)
    for i in range(len(v)):
        vp = v.copy(); vp[i] += eps
        vm = v.copy(); vm[i] -= eps
        g[i] = (nll(_unpack(vp, K, M), data) - nll(_unpack(vm, K, M), data)) / (2 * eps)
    return g


def nll_and_grad(state, data):
    """Mean NLL and its closed-form gradient w.r.t. the packed real parameters.

    NLL = log Z - (1/N) sum_s log |psi_s|^2 with everything analytic (issue #25):

      * Z = z^dag G z with G[c,d] = prod_m <alpha_c^m|alpha_d^m>, so
        dZ/d(Re z, Im z) = 2(Re, Im)(G z) and, from
        d log<a|b>/d(Re a, Im a) = (b - Re a, -Im a - i b) plus the Hermitian
        mirror term (its conjugate), dZ/dalpha is a weighted overlap sum.
      * psi_s = sum_c z_c P_sc, P_sc = prod_m f(x_sm; beta_cm),
        beta = alpha e^{-i theta}. With
        d log f/d(Re beta) = sqrt2 (x - sqrt2 Re beta) - i Im beta and
        d log f/d(Im beta) = i (sqrt2 x - Re beta), the LO rotation gives
        d/d(Re alpha) = cos(theta) d/d(Re beta) - sin(theta) d/d(Im beta) and
        d/d(Im alpha) = sin(theta) d/d(Re beta) + cos(theta) d/d(Im beta).

    Returns (nll_value, grad) with grad ordered like _pack: Re z, Im z,
    Re alpha (K*M), Im alpha (K*M). Samples clamped at p = 1e-300 in nll() are
    astronomically far from any fit trajectory and are not special-cased.
    """
    z, alpha = state.z, state.alpha
    K, M = state.K, state.M

    # --- normalization Z and its closed-form gradient ---
    ov = coherent_overlap(alpha[:, None, :], alpha[None, :, :])  # (K,K,M)
    G = np.prod(ov, axis=2)                                      # (K,K) Hermitian
    Gz = G @ z
    Z = float(np.real(np.conj(z) @ Gz))
    dZ_zr = 2.0 * np.real(Gz)
    dZ_zi = 2.0 * np.imag(Gz)
    W = np.conj(z)[:, None] * z[None, :] * G                     # (K,K)
    S1 = W @ alpha                                               # (K,M)
    S0 = np.sum(W, axis=1)[:, None]                              # (K,1)
    dZ_ar = 2.0 * np.real(S1 - S0 * np.real(alpha))
    dZ_ai = 2.0 * np.real(-S0 * np.imag(alpha) - 1j * S1)

    # --- sample term: -(1/N) sum log |psi|^2 ---
    g_zr = np.zeros(K)
    g_zi = np.zeros(K)
    g_ar = np.zeros((K, M))
    g_ai = np.zeros((K, M))
    logpsi_sum = 0.0
    n = 0
    sqrt2 = np.sqrt(2.0)
    for theta, X in data:
        theta = np.asarray(theta, float)
        X = np.asarray(X, float)
        rot = alpha * np.exp(-1j * theta)[None, :]               # (K,M) beta
        prod = np.ones((X.shape[0], K), complex)
        for m in range(M):
            prod *= coherent_wavefunction(X[:, m][:, None], rot[None, :, m])
        psi = prod @ z                                           # (S,)
        absq = np.abs(psi) ** 2
        logpsi_sum += np.sum(np.log(np.maximum(absq, 1e-300)))
        n += X.shape[0]
        # d(-log|psi|^2)/dt = -2 Re(conj(psi) dpsi/dt) / |psi|^2
        r = np.conj(psi) / np.maximum(absq, 1e-300)              # (S,)
        T = r[:, None] * prod                                    # (S,K): r * dpsi/dz_c
        g_zr += -2.0 * np.sum(np.real(T), axis=0)
        g_zi += 2.0 * np.sum(np.imag(T), axis=0)                 # Re(i T) = -Im(T)
        A = T * z[None, :]                                       # (S,K): r * z_c * P_sc
        for m in range(M):
            br = np.real(rot[:, m])[None, :]
            bi = np.imag(rot[:, m])[None, :]
            xm = X[:, m][:, None]
            gr = sqrt2 * (xm - sqrt2 * br) - 1j * bi             # d log f / d Re beta
            gi = 1j * (sqrt2 * xm - br)                          # d log f / d Im beta
            c, s = np.cos(theta[m]), np.sin(theta[m])
            g_ar[:, m] += -2.0 * np.sum(np.real(A * (c * gr - s * gi)), axis=0)
            g_ai[:, m] += -2.0 * np.sum(np.real(A * (s * gr + c * gi)), axis=0)

    value = np.log(Z) - logpsi_sum / n
    grad = np.concatenate([
        g_zr / n + dZ_zr / Z,
        g_zi / n + dZ_zi / Z,
        (g_ar / n + dZ_ar / Z).ravel(),
        (g_ai / n + dZ_ai / Z).ravel(),
    ])
    return value, grad


def fit_bbdagM(data, K=8, M=3, iters=200, lr=0.05, seed=0, callback=None,
               grad_eps=1e-5, gradient="analytic"):
    """Adam on the NLL gradient. Returns a physical CoherentKetState.

    gradient="analytic" (default) uses the closed-form nll_and_grad;
    gradient="fd" keeps the original central-difference path (grad_eps),
    retained as the independent reference the analytic path is tested against.
    """
    if gradient not in ("analytic", "fd"):
        raise ValueError(f"gradient must be 'analytic' or 'fd', got {gradient!r}")
    state = CoherentKetState.random_init(K, M, rng=seed)
    v = _pack(state)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        if gradient == "analytic":
            val, g = nll_and_grad(_unpack(v, K, M), data)
        else:
            g = _nll_grad_fd(v, K, M, data, eps=grad_eps)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 25 == 0:
            callback(t, nll(_unpack(v, K, M), data))
    return _unpack(v, K, M)


class MixedCoherentKetState:
    """rho = sum_r |psi_r><psi_r| / Z, each column a coherent-product ket (issue #28).

    The rank-R lift of CoherentKetState: B has R columns, so rho = B B^dagger
    is automatically PSD with rank <= R -- the mixed-state extension needed for
    decohered targets (a rank-1 ket cannot represent a lossy cat).

    z: (R, K) complex amplitudes. alpha: (R, K, M) complex displacements.
    Z = sum_r <psi_r|psi_r>; p_theta(x) = sum_r |psi_r,theta(x)|^2 / Z.
    """

    def __init__(self, z, alpha):
        self.z = np.asarray(z, complex)          # (R, K)
        self.alpha = np.asarray(alpha, complex)  # (R, K, M)

    @property
    def R(self):
        return self.z.shape[0]

    @property
    def K(self):
        return self.z.shape[1]

    @property
    def M(self):
        return self.alpha.shape[2]

    @classmethod
    def random_init(cls, R, K, M, scale=1.5, rng=None):
        rng = np.random.default_rng(rng)
        a = rng.uniform(-scale, scale, (R, K, M)) \
            + 1j * rng.uniform(-scale, scale, (R, K, M))
        return cls(z=np.ones((R, K), complex) / np.sqrt(R * K), alpha=a)

    def columns(self):
        """The R pure columns as CoherentKetState objects."""
        return [CoherentKetState(self.z[r], self.alpha[r]) for r in range(self.R)]

    def norm_sq(self):
        return sum(col.norm_sq() for col in self.columns())


def _pack_mixed(state):
    return np.concatenate([
        np.real(state.z).ravel(), np.imag(state.z).ravel(),
        np.real(state.alpha).ravel(), np.imag(state.alpha).ravel(),
    ])


def _unpack_mixed(v, R, K, M):
    n = R * K
    z = (v[0:n] + 1j * v[n:2 * n]).reshape(R, K)
    ar = v[2 * n:2 * n + n * M].reshape(R, K, M)
    ai = v[2 * n + n * M:2 * n + 2 * n * M].reshape(R, K, M)
    return MixedCoherentKetState(z=z, alpha=ar + 1j * ai)


def nll_mixed(state, data):
    """Mean per-sample NLL of the rank-R model p = sum_r |psi_r|^2 / Z."""
    Z = state.norm_sq()
    cols = state.columns()
    tot = 0.0
    n = 0
    for theta, X in data:
        dens = np.zeros(X.shape[0])
        for col in cols:
            dens += np.abs(col.psi_at(X, theta)) ** 2
        tot += -np.sum(np.log(np.maximum(dens / Z, 1e-300)))
        n += len(X)
    return tot / n


def nll_and_grad_mixed(state, data):
    """Mean NLL and closed-form gradient for the rank-R model.

    Identical calculus to nll_and_grad per column; the only change is the
    sample weight: with p~_s = sum_r |psi_rs|^2, each column's contribution is
    weighted by r_rs = conj(psi_rs) / p~_s (its share of the total density),
    and Z = sum_r z_r^dag G_r z_r differentiates column by column.
    """
    R, K, M = state.R, state.K, state.M
    g_zr = np.zeros((R, K))
    g_zi = np.zeros((R, K))
    g_ar = np.zeros((R, K, M))
    g_ai = np.zeros((R, K, M))
    dZ_zr = np.zeros((R, K))
    dZ_zi = np.zeros((R, K))
    dZ_ar = np.zeros((R, K, M))
    dZ_ai = np.zeros((R, K, M))
    sqrt2 = np.sqrt(2.0)

    # --- Z and dZ, column by column (same closed form as nll_and_grad) ---
    Z = 0.0
    for r in range(R):
        z, alpha = state.z[r], state.alpha[r]
        ov = coherent_overlap(alpha[:, None, :], alpha[None, :, :])
        G = np.prod(ov, axis=2)
        Gz = G @ z
        Z += float(np.real(np.conj(z) @ Gz))
        dZ_zr[r] = 2.0 * np.real(Gz)
        dZ_zi[r] = 2.0 * np.imag(Gz)
        W = np.conj(z)[:, None] * z[None, :] * G
        S1 = W @ alpha
        S0 = np.sum(W, axis=1)[:, None]
        dZ_ar[r] = 2.0 * np.real(S1 - S0 * np.real(alpha))
        dZ_ai[r] = 2.0 * np.real(-S0 * np.imag(alpha) - 1j * S1)

    # --- sample term ---
    logdens_sum = 0.0
    n = 0
    for theta, X in data:
        theta = np.asarray(theta, float)
        X = np.asarray(X, float)
        S = X.shape[0]
        rots, prods, psis = [], [], []
        dens = np.zeros(S)
        for r in range(R):
            rot = state.alpha[r] * np.exp(-1j * theta)[None, :]  # (K, M)
            prod = np.ones((S, K), complex)
            for m in range(M):
                prod *= coherent_wavefunction(X[:, m][:, None], rot[None, :, m])
            psi = prod @ state.z[r]
            rots.append(rot); prods.append(prod); psis.append(psi)
            dens += np.abs(psi) ** 2
        logdens_sum += np.sum(np.log(np.maximum(dens, 1e-300)))
        n += S
        inv = 1.0 / np.maximum(dens, 1e-300)
        for r in range(R):
            w = np.conj(psis[r]) * inv                           # (S,)
            T = w[:, None] * prods[r]                            # (S, K)
            g_zr[r] += -2.0 * np.sum(np.real(T), axis=0)
            g_zi[r] += 2.0 * np.sum(np.imag(T), axis=0)
            A = T * state.z[r][None, :]
            for m in range(M):
                br = np.real(rots[r][:, m])[None, :]
                bi = np.imag(rots[r][:, m])[None, :]
                xm = X[:, m][:, None]
                gr = sqrt2 * (xm - sqrt2 * br) - 1j * bi
                gi = 1j * (sqrt2 * xm - br)
                c, s = np.cos(theta[m]), np.sin(theta[m])
                g_ar[r, :, m] += -2.0 * np.sum(np.real(A * (c * gr - s * gi)), axis=0)
                g_ai[r, :, m] += -2.0 * np.sum(np.real(A * (s * gr + c * gi)), axis=0)

    value = np.log(Z) - logdens_sum / n
    grad = np.concatenate([
        (g_zr / n + dZ_zr / Z).ravel(),
        (g_zi / n + dZ_zi / Z).ravel(),
        (g_ar / n + dZ_ar / Z).ravel(),
        (g_ai / n + dZ_ai / Z).ravel(),
    ])
    return value, grad


def fit_bbdagM_mixed(data, R=2, K=4, M=3, iters=200, lr=0.05, seed=0,
                     callback=None):
    """Adam on the analytic rank-R NLL gradient. Returns MixedCoherentKetState."""
    state = MixedCoherentKetState.random_init(R, K, M, rng=seed)
    v = _pack_mixed(state)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        val, g = nll_and_grad_mixed(_unpack_mixed(v, R, K, M), data)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 25 == 0:
            callback(t, nll_mixed(_unpack_mixed(v, R, K, M), data))
    return _unpack_mixed(v, R, K, M)


def fidelity_vs_cat3(state, alpha, parity=+1):
    """Exact state fidelity F = |<psi|cat3>|^2 for cat3 = |a,a,a>+parity|-a,-a,-a>.

    cat3 is a 2-ket coherent superposition, so this is closed form (no grid).
    """
    M = state.M
    a = float(alpha)
    kets_alpha = np.array([[a] * M, [-a] * M], complex)  # (2, M)
    kets_z = np.array([1.0, parity], complex)
    ov = state.overlap_with(kets_z, kets_alpha)
    Z = state.norm_sq()
    # <cat3|cat3> = sum_{i,j} z_i* z_j prod_m <ket_i^m|ket_j^m>
    g = coherent_overlap(kets_alpha[:, None, :], kets_alpha[None, :, :])
    Gt = np.prod(g, axis=2)
    Ncat = np.real(np.conj(kets_z) @ Gt @ kets_z)
    return np.abs(ov) ** 2 / (Z * Ncat)
