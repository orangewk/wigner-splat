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
