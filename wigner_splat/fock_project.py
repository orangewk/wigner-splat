"""Closed-form Fock-basis density matrix from a signed Gaussian splat mixture.

Issue #8 (positivity): a signed splat mixture's Hermitian operator rho_mix has
well-defined Fock matrix elements (the Weyl transform is a bijection between
phase-space functions and operators), but materializing them via a phase-space
grid (as experiments/08_positivity/diagnose_1mode.py does, for validation only)
is O(n_max^2 * grid^2) and not something a fit-loop penalty can afford. This
module builds rho DIRECTLY in closed form, one Gaussian component at a time,
via a Bargmann/Hermite generating-function route -- no grid integration.

Derivation (matches wigner_splat.fock / .forward*'s conventions -- vacuum
Wigner (1/pi) exp(-x^2-p^2), i.e. N(z; 0, 0.5 I); quadrature vectors
<n|x_theta> from fock.hermite_psi):

1. W -> rho(q,q') kernel. For a single mode, the standard (hbar=1) Wigner
   transform is W(X,P) = (1/pi) int dy exp(2iPy) <X-y|rho|X+y>; inverting the
   Fourier transform in y and substituting q=X-y, q'=X+y gives

       rho(q,q') = int d^M p exp(-i p.(q-q')) W((q+q')/2, p)

   for M modes, z=(x_1,p_1,...,x_M,p_M) (interleaved, matching forward.py /
   forward2f.py / forward3f.py's mu/Sigma layout). This sign (exp(-i p.(q-q')),
   NOT +i) was verified by hand against the vacuum: it is the unique choice
   that reproduces W_vac(x,p) = (1/pi) exp(-x^2-p^2) from rho=|0><0|.

   For a Gaussian W(z) = N(z; mu, Sigma), splitting z into position block x
   (mean mu_x, covariance Sigma_xx) and the p-conditional Gaussian
   N(p; mu_{p|x}(x), Sigma_{p|x}) (mu_{p|x}(x) = mu_p + Sigma_px Sigma_xx^-1
   (x-mu_x), Sigma_{p|x} = Sigma_pp - Sigma_px Sigma_xx^-1 Sigma_xp), the p
   integral is the Gaussian's characteristic function, giving rho(q,q') in
   closed form directly (no integral left):

       rho(q,q') = N(u; mu_x, Sigma_xx)
                   * exp[-i mu_{p|x}(u).v - 0.5 v^T Sigma_{p|x} v]

   with u=(q+q')/2, v=q-q'.

2. Hermite generating function. G(q,s) = pi^{-1/4} exp(-q^2/2 + sqrt2 q s -
   s^2/2) = sum_n psi_n(q) s^n / sqrt(n!) (single mode; M modes: product over
   the M position coordinates). Then

       R(s,t) = int int d^M q d^M q' G(q,s) G(q',t) rho(q,q')

   is again a Gaussian integral (now over (q,q') given rho's closed form
   above), yielding R(s,t) = C * exp(a^T xi + 0.5 xi^T B xi), xi=(s,t) in
   C^{2M} -- see _component_R_params for the matrix algebra.

3. Coefficient extraction. rho_{m,n} = sqrt(m! n!) * [s^m t^n] R(s,t). The
   Taylor coefficients of exp(a^T xi + 0.5 xi^T B xi) satisfy a linear
   recurrence obtained by differentiating F = exp(...):
   dF/dxi_i = (a_i + (B xi)_i) F, giving (for F = sum_alpha T[alpha] xi^alpha)

       (beta_i + 1) T[beta + e_i] = a_i T[beta] + sum_j B[i,j] T[beta - e_j]

   computed by _series_coeffs in order of increasing total degree.

Validation: experiments/08_positivity/diagnose_1mode.py (grid-based, kept as
the ground truth) and tests/test_fock_project.py.
"""

import numpy as np


def _sigma_1mode(mixture):
    """Per-splat covariance (K,2,2) for forward.SplatMixture, which stores
    (s, phi) rather than exposing a .Sigma() method (unlike forward2f /
    forward3f). Mirrors the inline computation in SplatMixture.wigner."""
    K = len(mixture.w)
    Sigma = np.empty((K, 2, 2))
    for k in range(K):
        c, s_ = np.cos(mixture.phi[k]), np.sin(mixture.phi[k])
        R = np.array([[c, -s_], [s_, c]])
        Sigma[k] = R @ np.diag(np.exp(2 * mixture.s[k])) @ R.T
    return Sigma


def _mixture_arrays(mixture):
    """(w, mu, Sigma) as plain arrays for any SplatMixture* -- forward.py's
    SplatMixture has no .Sigma() (uses s/phi instead); forward2f/forward3f's
    SplatMixture2F/SplatMixture3F both do."""
    if hasattr(mixture, "Sigma"):
        return mixture.w, mixture.mu, mixture.Sigma()
    return mixture.w, mixture.mu, _sigma_1mode(mixture)


def _component_R_params(mu, Sigma, M):
    """(C, a, B) such that R(s,t) = C * exp(a^T xi + 0.5 xi^T B xi),
    xi=(s,t) in C^{2M}, for ONE phase-space Gaussian component
    W(z) = N(z; mu, Sigma), z=(x_1,p_1,...,x_M,p_M) interleaved.

    mu (2M,) may be COMPLEX (used to build the exact off-diagonal
    |alpha><-alpha|-type components of a cat state's Wigner function in
    tests -- same "complex mean" trick as forward2f/forward3f's
    _gaussian_overlap). Sigma (2M,2M) is real.
    """
    pos = np.arange(0, 2 * M, 2)
    mom = np.arange(1, 2 * M, 2)
    mu = np.asarray(mu, dtype=complex)
    Sigma = np.asarray(Sigma, dtype=float)

    mu_x, mu_p = mu[pos], mu[mom]
    Sxx = Sigma[np.ix_(pos, pos)]
    Sxp = Sigma[np.ix_(pos, mom)]
    Spx = Sxp.T
    Spp = Sigma[np.ix_(mom, mom)]

    Sxx_inv = np.linalg.inv(Sxx)
    Sp_given_x = Spp - Spx @ Sxx_inv @ Sxp

    c_u = Sxx_inv @ mu_x
    c_v = -1j * (mu_p - Spx @ Sxx_inv @ mu_x)
    c_const = np.concatenate([c_u, c_v])

    I_M = np.eye(M)
    Quu = Sxx_inv + 2 * I_M
    Quv = 1j * (Sxx_inv @ Sxp)
    Qvu = 1j * (Spx @ Sxx_inv)
    Qvv = Sp_given_x + 0.5 * I_M
    Qm = np.block([[Quu, Quv], [Qvu, Qvv]])

    r2 = np.sqrt(2.0)
    Cst = np.zeros((2 * M, 2 * M), dtype=complex)
    Cst[0:M, 0:M] = r2 * I_M          # u <- s
    Cst[0:M, M:2 * M] = r2 * I_M      # u <- t
    Cst[M:2 * M, 0:M] = (r2 / 2) * I_M     # v <- s
    Cst[M:2 * M, M:2 * M] = -(r2 / 2) * I_M  # v <- t

    Qm_inv = np.linalg.inv(Qm)
    const0 = -0.5 * (mu_x @ Sxx_inv @ mu_x)

    a = Cst.T @ (Qm_inv @ c_const)
    B = Cst.T @ Qm_inv @ Cst - np.eye(2 * M)

    P0 = (np.pi ** (-M / 2)) * ((2 * np.pi) ** (-M / 2)) / np.sqrt(np.linalg.det(Sxx))
    detQ = np.linalg.det(Qm)
    C = (
        P0
        * (2 * np.pi) ** M
        / np.sqrt(detQ)
        * np.exp(const0 + 0.5 * (c_const @ (Qm_inv @ c_const)))
    )
    return C, a, B


def _series_coeffs(a, B, n_max, dim):
    """Taylor coefficients T[alpha] (alpha in {0,...,n_max-1}^dim) of
    F(xi) = exp(a.xi + 0.5 xi^T B xi), via the recurrence derived in the
    module docstring. T[0,...,0] = 1; higher-degree entries are filled in
    order of increasing total degree, each from one lower-degree neighbor."""
    shape = (n_max,) * dim
    T = np.zeros(shape, dtype=complex)
    zero = (0,) * dim
    T[zero] = 1.0
    idxs = sorted(np.ndindex(*shape), key=sum)
    for gamma in idxs:
        deg = sum(gamma)
        if deg == 0:
            continue
        i = next(k for k in range(dim) if gamma[k] > 0)
        beta = list(gamma)
        beta[i] -= 1
        val = a[i] * T[tuple(beta)]
        for j in range(dim):
            if beta[j] > 0:
                bj = list(beta)
                bj[j] -= 1
                val = val + B[i, j] * T[tuple(bj)]
        T[gamma] = val / gamma[i]
    return T


def _rho_component(mu, Sigma, n_max, M):
    """Fock matrix elements (n_max**M, n_max**M) of ONE Gaussian phase-space
    component, materialized via the Bargmann/Hermite route (module docstring
    steps 2-3). mu may be complex (see _component_R_params)."""
    C, a, B = _component_R_params(mu, Sigma, M)
    T = _series_coeffs(a, B, n_max, 2 * M)  # axes: m_1..m_M, n_1..n_M

    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    fact_sqrt = np.exp(0.5 * log_fact)  # sqrt(k!) for k = 0..n_max-1

    rho_tensor = C * T
    for ax in range(2 * M):
        shape_ax = [1] * (2 * M)
        shape_ax[ax] = n_max
        rho_tensor = rho_tensor * fact_sqrt.reshape(shape_ax)

    dim_out = n_max ** M
    return rho_tensor.reshape(dim_out, dim_out)


def rho_from_components(components, n_max, M):
    """Sum_k weight_k * rho_component(mu_k, Sigma_k) for arbitrary (weight,
    mu, Sigma) triples -- the building block rho_from_splat wraps, and the
    same one tests use to build a cat state's EXACT Wigner-as-splats
    decomposition (2 real blobs + a complex-mean fringe pair) as an
    independent closed-form cross-check.
    """
    dim_out = n_max ** M
    rho = np.zeros((dim_out, dim_out), dtype=complex)
    for weight, mu, Sigma in components:
        rho = rho + weight * _rho_component(mu, Sigma, n_max, M)
    return rho


def rho_from_splat(mixture, n_max):
    """Fock-basis density operator (n_max**M, n_max**M) complex, Hermitian by
    construction of the input (but see psd_penalty/psd_report -- symmetrize
    before reading eigenvalues), for a signed splat mixture:

        mixture: wigner_splat.forward.SplatMixture (M=1),
                 wigner_splat.forward2f.SplatMixture2F (M=2), or
                 wigner_splat.forward3f.SplatMixture3F (M=3).
        n_max:   per-mode Fock cutoff.
    """
    w, mu, Sigma = _mixture_arrays(mixture)
    M = mu.shape[1] // 2
    return rho_from_components(zip(w, mu, Sigma), n_max, M)


def rho_component(mixture, k, n_max):
    """The k-th splat's WEIGHTED contribution w_k * rho_component_k to
    rho_from_splat(mixture, n_max), i.e. rho_from_splat(mixture, n_max) ==
    sum(rho_component(mixture, k, n_max) for k in range(len(mixture.w))).

    Lets a caller that perturbs only ONE splat's parameters -- e.g. the
    finite-difference psd_penalty gradient used by a fit's PSD-polish stage
    (wigner_splat.fit.fit_psd, wigner_splat.fit3f.fit3f_psd) -- recompute just
    that one term and add it to a cached sum of the other K-1 components,
    instead of rebuilding the whole O(K) sum per perturbation. _rho_component
    is the expensive step (a size-n_max**(2M) Hermite recurrence); caching it
    per-component turns an O(K) rebuild into O(1) per finite-difference call.
    """
    w, mu, Sigma = _mixture_arrays(mixture)
    M = mu.shape[1] // 2
    return w[k] * _rho_component(mu[k], Sigma[k], n_max, M)


def psd_penalty(rho):
    """Sum of squared NEGATIVE eigenvalues of the Hermitian part of rho.
    Chosen over a bare min-eigenvalue penalty because it does not go flat /
    discontinuous at eigenvalue crossings (see module docstring reference in
    the issue brief)."""
    rho_h = (rho + rho.conj().T) / 2
    ev = np.linalg.eigvalsh(rho_h)
    neg = ev[ev < 0]
    return float(np.sum(neg ** 2))


def psd_report(rho):
    """trace, min/max eigenvalue, and negativity (= |sum of negative
    eigenvalues|) of the Hermitian part of rho."""
    rho_h = (rho + rho.conj().T) / 2
    ev = np.linalg.eigvalsh(rho_h)
    neg = ev[ev < 0]
    return dict(
        trace=float(np.real(np.trace(rho))),
        min_eig=float(ev.min()),
        max_eig=float(ev.max()),
        negativity=float(np.abs(neg.sum())),
    )
