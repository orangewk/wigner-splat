"""Pure-state Fock-basis maximum likelihood, three modes (issue #27).

The FAIR baseline for the BB-dagger comparison: same rank-1 (pure-state)
constraint, same per-sample NLL objective, same Adam optimizer, same analytic
gradient discipline -- the ONLY difference from bbdagM is the representation:

    bbdagM:    |psi> = sum_c z_c prod_m |alpha_c^m>     (structured, ~8K reals)
    purefock3: |psi> = sum_{mnq} psi[m,n,q] |m,n,q>     (generic, 2 n_max^3 reals)

If this generic-representation fit matches BB-dagger's fidelity at comparable
compute, BB-dagger's advantage over full-rank MLE was the parameter-count
constraint, not the coherent ansatz (issue #27's falsification condition).

The model is p_theta(x) = |<x_theta|psi>|^2 / <psi|psi> with
<x_theta|m,n,q> = psi_m(x1) psi_n(x2) psi_q(x3) e^{-i(m th1 + n th2 + q th3)}
(fock.quadrature_vectors convention). Truncation at n_max caps the exact-state
fidelity at fock.cat3_truncation_fidelity (0.99321 at n_max=8, alpha=1.5) --
quoted alongside results, exactly like the mle3 ceiling.
"""

import numpy as np

from .fock import cat3_truncation_fidelity, cat3_fock, quadrature_vectors


def _mode_vectors(X, theta, n_max):
    """Per-mode <n|x_theta> for samples X (S, 3): three (S, n_max) arrays."""
    return [quadrature_vectors(X[:, m], theta[m], n_max) for m in range(3)]


def _amplitudes(psi, v1, v2, v3):
    """amp_s = sum_{mnq} psi[m,n,q] v1[s,m] v2[s,n] v3[s,q], (S,) complex."""
    # sequential contraction keeps cost at O(S n_max^2 (n_max + 1))
    t = np.einsum("sm,mnq->snq", v1, psi)
    t = np.einsum("sn,snq->sq", v2, t)
    return np.einsum("sq,sq->s", v3, t)


def nll_psi(psi, data, n_max=None):
    """Mean per-sample negative log likelihood over all angle triples."""
    n_max = psi.shape[0] if n_max is None else n_max
    Z = float(np.sum(np.abs(psi) ** 2))
    tot = 0.0
    n = 0
    for theta, X in data:
        v1, v2, v3 = _mode_vectors(np.asarray(X, float), np.asarray(theta, float), n_max)
        p = np.abs(_amplitudes(psi, v1, v2, v3)) ** 2 / Z
        tot += -np.sum(np.log(np.maximum(p, 1e-300)))
        n += len(X)
    return tot / n


def nll_and_grad_psi(psi, data):
    """Mean NLL and closed-form gradient w.r.t. [Re psi, Im psi] (flattened).

    Same calculus as bbdagM.nll_and_grad: NLL = log Z - (1/N) sum log|amp|^2
    with Z = ||psi||^2 and amp linear in psi, so
    d(-log|amp|^2)/d(psi component) = -2 Re(r_s V_s), r_s = conj(amp)/|amp|^2,
    V_s the product quadrature vector, and dZ/d(Re, Im psi) = 2 (Re, Im) psi.
    """
    n_max = psi.shape[0]
    Z = float(np.sum(np.abs(psi) ** 2))
    grad_c = np.zeros_like(psi)  # accumulates sum_s r_s V_s (complex)
    logpsi_sum = 0.0
    n = 0
    for theta, X in data:
        v1, v2, v3 = _mode_vectors(np.asarray(X, float), np.asarray(theta, float), n_max)
        amp = _amplitudes(psi, v1, v2, v3)
        absq = np.abs(amp) ** 2
        logpsi_sum += np.sum(np.log(np.maximum(absq, 1e-300)))
        n += len(X)
        r = np.conj(amp) / np.maximum(absq, 1e-300)
        # sum_s r_s v1[s,m] v2[s,n] v3[s,q], contracted sequentially
        t = np.einsum("s,sm->sm", r, v1)
        t2 = np.einsum("sm,sn->smn", t, v2)
        grad_c += np.einsum("smn,sq->mnq", t2, v3)
    value = np.log(Z) - logpsi_sum / n
    g_re = -2.0 * np.real(grad_c) / n + 2.0 * np.real(psi) / Z
    g_im = 2.0 * np.imag(grad_c) / n + 2.0 * np.imag(psi) / Z  # Re(i w) = -Im w
    return value, np.concatenate([g_re.ravel(), g_im.ravel()])


def _nll_grad_fd(v, n_max, data, eps=1e-6):
    """Central-difference reference gradient (tests only)."""
    g = np.zeros_like(v)
    for i in range(len(v)):
        vp = v.copy(); vp[i] += eps
        vm = v.copy(); vm[i] -= eps
        g[i] = (nll_psi(_unpack(vp, n_max), data)
                - nll_psi(_unpack(vm, n_max), data)) / (2 * eps)
    return g


def _pack(psi):
    return np.concatenate([np.real(psi).ravel(), np.imag(psi).ravel()])


def _unpack(v, n_max):
    n3 = n_max ** 3
    return (v[:n3] + 1j * v[n3:]).reshape(n_max, n_max, n_max)


def fit_purefock3(data, n_max=8, iters=400, lr=0.05, seed=0, callback=None):
    """Adam on the analytic NLL gradient over a generic pure Fock ket.

    Init: complex Gaussian noise (seeded), normalized -- no target knowledge.
    Returns the (unnormalized) fitted psi (n_max, n_max, n_max); normalize by
    ||psi|| for state-vector use. Physical by construction (rank-1 PSD).
    """
    rng = np.random.default_rng(seed)
    psi = rng.normal(size=(n_max,) * 3) + 1j * rng.normal(size=(n_max,) * 3)
    psi /= np.linalg.norm(psi)
    v = _pack(psi)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        val, g = nll_and_grad_psi(_unpack(v, n_max), data)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 25 == 0:
            callback(t, nll_psi(_unpack(v, n_max), data))
    return _unpack(v, n_max)


# ---------------------------------------------------------------------------
# Detection-efficiency (loss) forward model -- issue #42 deployment.
#
# The measured pdf of loss_eta(rho), rho = |psi><psi|/Z, is the pure pdf
# convolved per mode with N(0, sigma2), sigma2 = (1 - eta)/2 +
# extra_noise_var. In the Fock basis this is a per-mode POVM matrix
#
#   Phi[n, n'](x) = integral psi_n(y) psi_n'(y) N(x - sqrt(eta) y; sigma2) dy
#
# (the inefficient-homodyne POVM element <n|Pi_eta(x)|n'>), so
# p(x|theta) = psi^dag (E1 (x) E2 (x) E3) psi / Z with E_m the phase-rotated
# Phi of mode m -- a Kronecker product of n_max x n_max matrices, applied by
# three sequential mode contractions. The integrand is a polynomial of
# degree 2 n_max - 2 times a Gaussian (the psi_n Gaussians and the loss
# kernel merge into one), so an n_max-point Gauss-Hermite rule is EXACT up
# to floating point: closed form in the same sense as the rest of the repo.
# The eta channel keeps rho PSD (CPTP); the loss channel commutes with the
# LO phase rotation, so the pure model's e^{-i n theta} phases carry over
# unchanged. Z is unchanged (trace preserving). extra_noise_var > 0 is
# supported directly by the same integral (it only widens sigma2) --
# unlike a truncated Kraus route, which the tests use as an independent
# cross-check at extra_noise_var = 0.
# ---------------------------------------------------------------------------


def _hermite_poly_part(y, n_max):
    """h_n(y) = psi_n(y) e^{y^2/2} (the polynomial part), (n_max,) + y.shape."""
    h = np.empty((n_max,) + y.shape)
    h[0] = np.pi ** -0.25
    if n_max > 1:
        h[1] = np.sqrt(2.0) * y * h[0]
    for n in range(2, n_max):
        h[n] = np.sqrt(2.0 / n) * y * h[n - 1] - np.sqrt((n - 1) / n) * h[n - 2]
    return h


def _lossy_mode_matrices(x, theta, n_max, eta, sigma2):
    """Phase-rotated POVM matrices E (S, n_max, n_max), Hermitian PSD.

    E[s] = diag(e^{i n theta}) Phi(x_s) diag(e^{-i n theta}) with Phi the
    real symmetric convolved pair-basis matrix above, evaluated by the exact
    Gauss-Hermite rule (nodes fixed, centers shifted per sample: the merged
    Gaussian e^{-y^2} e^{-(x - sqrt(eta) y)^2 / (2 sigma2)} =
    e^{c} e^{-a (y - b)^2} has sample-independent width a).
    """
    x = np.asarray(x, float)
    a = 1.0 + eta / (2.0 * sigma2)
    b = (np.sqrt(eta) / sigma2) * x / (2.0 * a)                # (S,)
    c = a * b ** 2 - x ** 2 / (2.0 * sigma2)                   # (S,)
    t, w = np.polynomial.hermite.hermgauss(n_max + 4)
    y = b[:, None] + t[None, :] / np.sqrt(a)                   # (S, G)
    h = _hermite_poly_part(y, n_max)                           # (n, S, G)
    pref = np.exp(c) / np.sqrt(2.0 * np.pi * sigma2 * a)       # (S,)
    Phi = np.einsum("g,nsg,msg->snm", w, h, h)
    Phi *= pref[:, None, None]
    ph = np.exp(-1j * theta * np.arange(n_max))
    return np.conj(ph)[None, :, None] * Phi * ph[None, None, :]


def _lossy_apply(E1, E2, E3, psi):
    """(E1 (x) E2 (x) E3) psi per sample: (S, n_max, n_max, n_max)."""
    t = np.einsum("sab,bnq->sanq", E1, psi)
    t = np.einsum("scn,sanq->sacq", E2, t)
    return np.einsum("sdq,sacq->sacd", E3, t)


def lossy_pdf_psi(psi, X, theta, eta, extra_noise_var=0.0, chunk=4096):
    """Measured pdf p_eta(X) (S,) of loss_eta(|psi><psi|/Z)."""
    from .bbdagS import _check_loss_params
    _check_loss_params(eta, extra_noise_var)
    sigma2 = (1.0 - eta) / 2.0 + extra_noise_var
    n_max = psi.shape[0]
    X = np.asarray(X, float)
    theta = np.asarray(theta, float)
    Z = float(np.sum(np.abs(psi) ** 2))
    if sigma2 <= 1e-14:
        v1, v2, v3 = _mode_vectors(X, theta, n_max)
        return np.abs(_amplitudes(psi, v1, v2, v3)) ** 2 / Z
    out = np.empty(X.shape[0])
    for s0 in range(0, X.shape[0], chunk):
        Xc = X[s0:s0 + chunk]
        E1, E2, E3 = (
            _lossy_mode_matrices(Xc[:, m], theta[m], n_max, eta, sigma2)
            for m in range(3)
        )
        Mpsi = _lossy_apply(E1, E2, E3, psi)
        out[s0:s0 + Xc.shape[0]] = np.maximum(
            np.real(np.einsum("acd,sacd->s", np.conj(psi), Mpsi)), 0.0
        ) / Z
    return out


def lossy_nll_psi(psi, data, eta, extra_noise_var=0.0, chunk=4096):
    """Mean per-sample NLL of the measured (lossy) pdf."""
    val, _ = _lossy_nll_core(psi, data, eta, extra_noise_var, chunk,
                             want_grad=False)
    return val


def lossy_nll_and_grad_psi(psi, data, eta, extra_noise_var=0.0, chunk=4096):
    """Lossy NLL and closed-form gradient w.r.t. [Re psi, Im psi]."""
    return _lossy_nll_core(psi, data, eta, extra_noise_var, chunk,
                           want_grad=True)


def _lossy_nll_core(psi, data, eta, extra_noise_var, chunk, want_grad):
    from .bbdagS import _check_loss_params
    _check_loss_params(eta, extra_noise_var)
    sigma2 = (1.0 - eta) / 2.0 + extra_noise_var
    if sigma2 <= 1e-14:
        if want_grad:
            return nll_and_grad_psi(psi, data)
        return nll_psi(psi, data), None
    n_max = psi.shape[0]
    Z = float(np.sum(np.abs(psi) ** 2))
    grad_c = np.zeros_like(psi) if want_grad else None
    lognum_sum = 0.0
    n = 0
    for theta, X in data:
        X = np.asarray(X, float)
        theta = np.asarray(theta, float)
        n += X.shape[0]
        for s0 in range(0, X.shape[0], chunk):
            Xc = X[s0:s0 + chunk]
            E1, E2, E3 = (
                _lossy_mode_matrices(Xc[:, m], theta[m], n_max, eta, sigma2)
                for m in range(3)
            )
            Mpsi = _lossy_apply(E1, E2, E3, psi)              # (s, n, n, n)
            num = np.maximum(
                np.real(np.einsum("acd,sacd->s", np.conj(psi), Mpsi)), 1e-300
            )
            lognum_sum += np.sum(np.log(num))
            if want_grad:
                grad_c += np.einsum("s,sacd->acd", 1.0 / num, Mpsi)
    value = np.log(Z) - lognum_sum / n
    if not want_grad:
        return value, None
    g_re = -2.0 * np.real(grad_c) / n + 2.0 * np.real(psi) / Z
    g_im = -2.0 * np.imag(grad_c) / n + 2.0 * np.imag(psi) / Z
    return value, np.concatenate([g_re.ravel(), g_im.ravel()])


def fit_purefock3_lossy(data, n_max=8, eta=0.8, extra_noise_var=0.0,
                        iters=400, lr=0.05, seed=0, callback=None,
                        chunk=4096):
    """Adam on the lossy NLL at KNOWN eta / extra_noise_var (issue #42 scope).

    Same init and schedule as fit_purefock3; the fitted psi estimates the
    PRE-loss pure state. eta is not fitted here (the joint-eta path lives in
    the bbdag family, where the scalar finite difference is cheap).
    """
    rng = np.random.default_rng(seed)
    psi = rng.normal(size=(n_max,) * 3) + 1j * rng.normal(size=(n_max,) * 3)
    psi /= np.linalg.norm(psi)
    v = _pack(psi)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        val, g = lossy_nll_and_grad_psi(_unpack(v, n_max), data, eta,
                                        extra_noise_var, chunk=chunk)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 25 == 0:
            callback(t, lossy_nll_psi(_unpack(v, n_max), data, eta,
                                      extra_noise_var, chunk=chunk))
    return _unpack(v, n_max)


def fidelity_vs_cat3(psi, alpha, parity=+1):
    """(truncated, exact) state fidelities of a Fock ket against the cat3.

    truncated: |<cat3_trunc|psi>|^2 / ||psi||^2 with the normalized truncated
    cat (comparable to fock.fidelity_pure / the mle3 convention).
    exact: against the exact untruncated cat = truncated x the truncation
    ceiling (fock.cat3_truncation_fidelity) -- comparable to the BB-dagger
    exact state fidelity.
    """
    n_max = psi.shape[0]
    target = cat3_fock(alpha, parity, n_max)
    flat = psi.ravel()
    f_trunc = float(
        np.abs(np.conj(target) @ flat) ** 2 / np.sum(np.abs(flat) ** 2)
    )
    return f_trunc, f_trunc * cat3_truncation_fidelity(alpha, parity, n_max)
