"""Truncated Fock-basis tools: reference density matrices, quadrature
projectors, Wigner functions, fidelity.

Same conventions as states.py: vacuum marginal N(0, 1/2), coherent |beta>
at (x, p) = sqrt(2) (Re b, Im b). The LO phase rotates alpha -> alpha
e^{-i theta} (states.homodyne_pdf), which fixes <x_theta|n> =
psi_n(x) e^{-i n theta} — validated against states.py in the tests.
"""

import numpy as np


def hermite_psi(x, n_max):
    """Harmonic-oscillator eigenfunctions psi_n(x), n = 0..n_max-1, (n_max, len(x)).

    Stable three-term recurrence; psi_0(x) = pi^{-1/4} exp(-x^2/2).
    """
    x = np.atleast_1d(x)
    psi = np.empty((n_max, len(x)))
    psi[0] = np.pi ** -0.25 * np.exp(-(x ** 2) / 2)
    if n_max > 1:
        psi[1] = np.sqrt(2.0) * x * psi[0]
    for n in range(2, n_max):
        psi[n] = np.sqrt(2.0 / n) * x * psi[n - 1] - np.sqrt((n - 1) / n) * psi[n - 2]
    return psi


def quadrature_vectors(x, theta, n_max):
    """<n|x_theta> for each sample point: (len(x), n_max) complex."""
    psi = hermite_psi(x, n_max)  # (n_max, B)
    phase = np.exp(-1j * theta * np.arange(n_max))
    return psi.T * phase  # <n|x_theta> = psi_n(x) e^{-i n theta}


def cat_fock(alpha, parity=+1, n_max=25):
    """Normalized Fock coefficients of |alpha> + parity |-alpha> (real alpha)."""
    n = np.arange(n_max)
    log_fact = np.cumsum(np.log(np.maximum(n, 1)))
    c = np.exp(-(alpha ** 2) / 2 + n * np.log(np.abs(alpha) + 1e-300) - log_fact / 2)
    c *= np.sign(alpha) ** n
    c = c + parity * c * (-1.0) ** n
    return c / np.linalg.norm(c)


def marginal_from_rho(rho, x, theta):
    """p_theta(x) = <x_theta| rho |x_theta>."""
    v = quadrature_vectors(x, theta, len(rho))  # (B, n_max), rows <n|x>
    return np.real(np.einsum("bm,mn,bn->b", v.conj(), rho, v))


def _genlaguerre(n_max, k, y):
    """L_n^{(k)}(y) for n = 0..n_max-1 via the standard recurrence, (n_max, ...)."""
    out = np.empty((n_max,) + y.shape)
    out[0] = 1.0
    if n_max > 1:
        out[1] = 1.0 + k - y
    for n in range(2, n_max):
        out[n] = ((2 * n - 1 + k - y) * out[n - 1] - (n - 1 + k) * out[n - 2]) / n
    return out


def wigner_from_rho(rho, x, p):
    """W(x, p) of a Fock-basis density matrix on a phase-space grid.

    Uses the displaced-parity form W = (1/pi) tr[rho D(2a) P] with
    a = (x + ip)/sqrt(2) and the closed-form displacement matrix elements
    <m|D(b)|n> = sqrt(n!/m!) b^{m-n} e^{-|b|^2/2} L_n^{(m-n)}(|b|^2), m >= n.
    """
    N = len(rho)
    X, P = np.broadcast_arrays(x, p)
    b = np.sqrt(2.0) * (X + 1j * P)  # 2a
    y = np.abs(b) ** 2
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, N)))])
    W = np.zeros(X.shape)
    env = np.exp(-y / 2)
    for d in range(N):  # d = m - n >= 0
        L = _genlaguerre(N - d, d, y)  # L_n^{(d)}, n = 0..N-d-1
        bd = b ** d
        for n_ in range(N - d):
            m_ = n_ + d
            amp = np.exp((log_fact[n_] - log_fact[m_]) / 2)
            Dmn = amp * bd * env * L[n_]  # <m|D(2a)|n>
            # tr[rho D P] = sum_{mn} rho_{nm} (-1)^n <m|D|n>
            term = rho[n_, m_] * (-1) ** n_ * Dmn
            if d > 0:
                term = term + rho[m_, n_] * (-1) ** m_ * np.conj(Dmn) * (-1.0) ** d
            W += np.real(term)
    return W / np.pi


def fidelity_pure(psi, rho):
    """<psi| rho |psi> for a pure target state (Fock coefficients psi)."""
    return float(np.real(psi.conj() @ rho @ psi))


def wigner_overlap(Wa, Wb, xs):
    """tr(rho_a rho_b) = 2 pi * double integral of W_a W_b on a square grid.

    With a pure state on one side this is the same fidelity as
    fidelity_pure, but usable for a splat mixture that only exists as a
    Wigner function. xs is the 1D grid both W arrays were evaluated on.
    """
    d = xs[1] - xs[0]
    return float(2 * np.pi * np.sum(Wa * Wb) * d * d)


def displacement_matrix(beta, n_max):
    """<m|D(beta)|n> for scalar complex beta, (n_max, n_max) complex.

    Closed form <m|D(b)|n> = sqrt(n!/m!) b^{m-n} e^{-|b|^2/2} L_n^{(m-n)}(|b|^2)
    for m >= n, and <m|D(b)|n> = conj(<n|D(-b)|m>) below the diagonal --
    the same matrix elements wigner_from_rho uses, materialized as a matrix.
    """
    beta = complex(beta)
    y = np.abs(beta) ** 2
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    D = np.zeros((n_max, n_max), complex)
    env = np.exp(-y / 2.0)
    yarr = np.array([y])
    for d in range(n_max):
        L = _genlaguerre(n_max - d, d, yarr)[:, 0]     # L_n^{(d)}(y)
        for n in range(n_max - d):
            m = n + d
            amp = np.exp((log_fact[n] - log_fact[m]) / 2.0)
            D[m, n] = amp * beta ** d * env * L[n]
            if d > 0:
                D[n, m] = amp * (-np.conj(beta)) ** d * env * L[n]
    return D


def _noise_quadrature(sigma_add, n_max, n_r, n_phi):
    """Displacement nodes and weights of the random-displacement channel.

    N_sigma(rho) = integral d^2beta P(beta) D(beta) rho D(beta)^dag with
    P a symmetric Gaussian of variance sigma_add/2 per real component
    (a displacement beta shifts x by sqrt2 Re beta, so this adds sigma_add
    to every quadrature variance). Radial: Gauss-Laguerre in t = |beta|^2 /
    sigma_add (the P weight becomes e^{-t} exactly); angular: a uniform
    grid, exact for the e^{i k phi} harmonics (|k| <= 2 n_max - 2) once
    n_phi > 4 n_max.
    """
    n_phi = n_phi or (4 * n_max + 2)
    t, wt = np.polynomial.laguerre.laggauss(n_r)
    r = np.sqrt(sigma_add * t)
    phi = 2.0 * np.pi * np.arange(n_phi) / n_phi
    betas = r[:, None] * np.exp(1j * phi)[None, :]
    weights = (wt / n_phi)[:, None] * np.ones(n_phi)[None, :]
    return betas.ravel(), weights.ravel()


def gaussian_noise_channel_1mode(rho, sigma_add, n_r=32, n_phi=None):
    """N_sigma(rho) for a single-mode Fock density matrix (numeric, tested
    against the closed-form pdf convolution). sigma_add <= 0 is identity."""
    if sigma_add <= 0.0:
        return rho.copy()
    n_max = len(rho)
    betas, weights = _noise_quadrature(sigma_add, n_max, n_r, n_phi)
    out = np.zeros_like(rho, dtype=complex)
    for b, w in zip(betas, weights):
        D = displacement_matrix(b, n_max)
        out += w * (D @ rho @ D.conj().T)
    return out


def gaussian_noise_channel_3mode(rho, sigma_add, n_max, n_r=32, n_phi=None):
    """Per-mode N_sigma applied to a flat (n_max^3, n_max^3) 3-mode rho."""
    if sigma_add <= 0.0:
        return rho.copy()
    betas, weights = _noise_quadrature(sigma_add, n_max, n_r, n_phi)
    Ds = [displacement_matrix(b, n_max) for b in betas]
    shape6 = (n_max,) * 6
    out = np.asarray(rho, complex).reshape(shape6)
    for mode in range(3):
        acc = np.zeros(shape6, complex)
        for D, w in zip(Ds, weights):
            t = np.tensordot(D, out, axes=([1], [mode]))
            t = np.moveaxis(t, 0, mode)
            t = np.tensordot(t, D.conj(), axes=([mode + 3], [1]))
            acc += w * np.moveaxis(t, -1, mode + 3)
        out = acc
    return out.reshape(n_max ** 3, n_max ** 3)


def thermal_lossy_cat3_fock(alpha, parity=+1, eta=0.8, sigma_add=0.1,
                            n_max=8, n_r=32, n_phi=None):
    """Truncated Fock rho of the thermal-noise lossy cat (issue #38 target).

    gaussian_noise_channel_3mode applied to lossy_cat3_fock. FULL RANK for
    sigma_add > 0. Truncation: the noise channel moves population upward,
    so quote np.trace as the ceiling analog (it is < the lossy cat's).
    """
    rho = lossy_cat3_fock(alpha, parity, eta, n_max)
    return gaussian_noise_channel_3mode(rho, sigma_add, n_max, n_r, n_phi)


def _coherent_coeffs(alpha, n_max):
    """Fock coefficients <m|alpha> = e^{-a^2/2} a^m / sqrt(m!), m = 0..n_max-1.

    Same construction (and 1e-12-validated convention) as cat_fock and the
    product-Fock cat matrix in tests/test_two_mode_state.py.
    """
    m = np.arange(n_max)
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    coh = np.exp(-(alpha ** 2) / 2 + m * np.log(np.abs(alpha) + 1e-300) - log_fact / 2)
    coh *= np.sign(alpha) ** m
    return coh


def cat2_fock(alpha, parity=+1, n_max=12):
    """Normalized product-Fock coefficients of the two-mode entangled cat.

    |a, a> + parity |-a, -a| (real alpha) in the product basis |m>|n>,
    returned as a FLAT vector of length n_max**2 with index m*n_max + n:

        c_{mn} proportional to (c_+)_m (c_+)_n + parity (c_-)_m (c_-)_n,

    where c_+ = <.|alpha> and c_- = <.|-alpha> = (-1)^. c_+ are the 1D
    coherent coefficients. Cross-validated against
    states2.TwoModeCat.homodyne_pdf in tests/test_two_mode_mle.py.
    """
    cp = _coherent_coeffs(alpha, n_max)
    cm = cp * (-1.0) ** np.arange(n_max)
    C = np.outer(cp, cp) + parity * np.outer(cm, cm)
    C = C / np.linalg.norm(C)
    return C.reshape(-1)


def cat2_truncation_fidelity(alpha, parity=+1, n_max=12):
    """Fidelity of the exact two-mode cat with its Fock truncation at n_max.

    This is the MLE ceiling: no density matrix on the n_max x n_max product
    basis can exceed it. Equals the fraction of the exact (unnormalized)
    coefficient norm retained by the truncation,

        ||C_trunc||^2 / (2 (1 + parity e^{-4 a^2})),

    since the exact single-mode coherent norm is 1 and <alpha|-alpha> =
    e^{-2 a^2}, giving the full norm 2(1 + parity e^{-4 a^2}).
    """
    cp = _coherent_coeffs(alpha, n_max)
    cm = cp * (-1.0) ** np.arange(n_max)
    C = np.outer(cp, cp) + parity * np.outer(cm, cm)
    full_norm2 = 2 * (1 + parity * np.exp(-4 * alpha ** 2))
    return float(np.sum(np.abs(C) ** 2) / full_norm2)


def cat3_fock(alpha, parity=+1, n_max=8):
    """Normalized product-Fock coefficients of the three-mode entangled cat.

    |a, a, a> + parity |-a, -a, -a| (real alpha) in the product basis
    |m>|n>|q>, returned as a FLAT vector of length n_max**3 with index
    (m*n_max + n)*n_max + q:

        c_{mnq} proportional to (c_+)_m (c_+)_n (c_+)_q
                              + parity (c_-)_m (c_-)_n (c_-)_q,

    where c_+ = <.|alpha> and c_- = <.|-alpha> = (-1)^. c_+ are the 1D
    coherent coefficients. Follows the cat2_fock pattern exactly.
    """
    cp = _coherent_coeffs(alpha, n_max)
    cm = cp * (-1.0) ** np.arange(n_max)
    C = (
        cp[:, None, None] * cp[None, :, None] * cp[None, None, :]
        + parity * cm[:, None, None] * cm[None, :, None] * cm[None, None, :]
    )
    C = C / np.linalg.norm(C)
    return C.reshape(-1)


def lossy_cat3_fock(alpha, parity=+1, eta=0.8, n_max=8):
    """Truncated Fock density matrix of the three-mode cat after per-mode loss.

    The loss channel maps coherent dyads to coherent dyads,
    E(|a><b|) = <b|a>^{1-eta} |sqrt(eta)a><sqrt(eta)b|, so the lossy cat is
    rank 2 on the span of A' = |sqrt(eta)a>^{x3}, B' = |-sqrt(eta)a>^{x3}:

        rho = [ A'A'^dag + B'B'^dag + parity c' (A'B'^dag + B'A'^dag) ] / norm

    with c' = e^{-6 a^2 (1-eta)} and norm = 2(1 + parity e^{-6 a^2}) (trace
    preserving; the truncated trace is < 1 by the truncation deficit, the MLE
    ceiling analog). Flat index layout matches cat3_fock. At eta = 1 this is
    the pure-cat projector.
    """
    a_out = np.sqrt(eta) * float(alpha)
    cp = _coherent_coeffs(a_out, n_max)
    cm = cp * (-1.0) ** np.arange(n_max)
    A = (cp[:, None, None] * cp[None, :, None] * cp[None, None, :]).reshape(-1)
    B = (cm[:, None, None] * cm[None, :, None] * cm[None, None, :]).reshape(-1)
    cross = parity * np.exp(-6.0 * alpha ** 2 * (1.0 - eta))
    norm = 2 * (1 + parity * np.exp(-6 * alpha ** 2))
    rho = (
        np.outer(A, A) + np.outer(B, B)
        + cross * (np.outer(A, B) + np.outer(B, A))
    ) / norm
    return rho


def cat3_truncation_fidelity(alpha, parity=+1, n_max=8):
    """Fidelity of the exact three-mode cat with its Fock truncation at n_max.

    This is the MLE ceiling: no density matrix on the n_max**3 product basis
    can exceed it. Equals the fraction of the exact (unnormalized) coefficient
    norm retained by the truncation,

        ||C_trunc||^2 / (2 (1 + parity e^{-6 a^2})),

    since the exact single-mode coherent norm is 1 and <alpha|-alpha> =
    e^{-2 a^2}, giving the full norm 2(1 + parity e^{-6 a^2}).
    """
    cp = _coherent_coeffs(alpha, n_max)
    cm = cp * (-1.0) ** np.arange(n_max)
    C = (
        cp[:, None, None] * cp[None, :, None] * cp[None, None, :]
        + parity * cm[:, None, None] * cm[None, :, None] * cm[None, None, :]
    )
    full_norm2 = 2 * (1 + parity * np.exp(-6 * alpha ** 2))
    return float(np.sum(np.abs(C) ** 2) / full_norm2)
