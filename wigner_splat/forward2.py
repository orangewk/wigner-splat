"""Separable two-mode signed Gaussian mixture + closed-form joint Radon model.

A two-mode splat k is a PRODUCT of two single-mode phase-space Gaussians
(block-diagonal 4x4 covariance): weight w_k (may be negative), mean mu_k in
R^4 as (x1, p1, x2, p2), and a per-mode covariance

    Sigma_{k,j} = R(phi_{k,j}) diag(exp(2 s_{k,j,0}), exp(2 s_{k,j,1})) R(phi_{k,j})^T

for j = 1, 2. The joint homodyne forward model factorizes exactly like the
single-mode case (forward.py): measuring quadratures (x_theta1, x_theta2)
marginalizes each mode onto its own unit vector u_j = (cos theta_j, sin
theta_j), and for a separable Gaussian the joint density is the product of
two closed-form 1D Radon projections,

    p_{th1,th2}(x1, x2) = sum_k w_k N(x1; m1_k, v1_k) N(x2; m2_k, v2_k),

with (m_j, v_j) from the SAME projected-moments formula as forward.py per
mode. So all of the single-mode machinery (loss gradients, densification
split, signed birth) lifts with per-mode bookkeeping. A single splat cannot
carry entangled Gaussian correlations between the modes, but a MIXTURE of
separable splats spans the cat's cross term because that term factorizes
into products of single-mode fringes (see states2 / docs/two-mode-plan.md).

Parameter layout (11 numbers per splat):
    w:   (K,)      signed weights (sum constrained to 1 by the fitter's loss)
    mu:  (K, 4)    joint means (x1, p1, x2, p2)
    s:   (K, 2, 2) log stds, s[k, j, :] = (log-std axis0, axis1) of mode j
    phi: (K, 2)    principal-axis rotation of each mode
"""

import numpy as np


def _cov(s_row, phi_val):
    """2x2 covariance R(phi) diag(exp(2 s0), exp(2 s1)) R(phi)^T."""
    c, sn = np.cos(phi_val), np.sin(phi_val)
    R = np.array([[c, -sn], [sn, c]])
    return R @ np.diag(np.exp(2 * np.asarray(s_row))) @ R.T


class SplatMixture2:
    """Separable two-mode splat mixture with flat-array parameters."""

    def __init__(self, w, mu, s, phi):
        self.w = np.asarray(w, float)
        self.mu = np.asarray(mu, float)
        self.s = np.asarray(s, float)
        self.phi = np.asarray(phi, float)

    @classmethod
    def random_init(cls, K, scale=2.0, rng=None):
        rng = np.random.default_rng(rng)
        return cls(
            w=np.full(K, 1.0 / K),
            mu=rng.uniform(-scale, scale, size=(K, 4)),
            s=np.full((K, 2, 2), np.log(0.8)),
            phi=rng.uniform(0, np.pi, size=(K, 2)),
        )

    def projected_moments(self, theta1, theta2):
        """Per-mode projected (mean, variance) of every splat: each (K,)."""
        u1 = np.array([np.cos(theta1), np.sin(theta1)])
        u2 = np.array([np.cos(theta2), np.sin(theta2)])
        m1 = self.mu[:, 0:2] @ u1
        m2 = self.mu[:, 2:4] @ u2
        c1, s1 = np.cos(self.phi[:, 0] - theta1), np.sin(self.phi[:, 0] - theta1)
        c2, s2 = np.cos(self.phi[:, 1] - theta2), np.sin(self.phi[:, 1] - theta2)
        v1 = np.exp(2 * self.s[:, 0, 0]) * c1 ** 2 + np.exp(2 * self.s[:, 0, 1]) * s1 ** 2
        v2 = np.exp(2 * self.s[:, 1, 0]) * c2 ** 2 + np.exp(2 * self.s[:, 1, 1]) * s2 ** 2
        return m1, v1, m2, v2

    def radon2(self, x1, x2, theta1, theta2):
        """Joint quadrature density on the (x1, x2) grid: (len(x1), len(x2))."""
        x1 = np.atleast_1d(x1)
        x2 = np.atleast_1d(x2)
        m1, v1, m2, v2 = self.projected_moments(theta1, theta2)
        g1 = np.exp(-((x1[:, None] - m1) ** 2) / (2 * v1)) / np.sqrt(2 * np.pi * v1)
        g2 = np.exp(-((x2[:, None] - m2) ** 2) / (2 * v2)) / np.sqrt(2 * np.pi * v2)
        # density[i, j] = sum_k w_k g1[i, k] g2[j, k]
        return np.einsum("ik,jk->ij", g1 * self.w, g2)

    def wigner4(self, x1, p1, x2, p2):
        """Evaluate the 4D mixture (product of two 2D Gaussians per splat)."""
        X1, P1, X2, P2 = np.broadcast_arrays(x1, p1, x2, p2)
        pts1 = np.stack([X1, P1], axis=-1)  # (..., 2)
        pts2 = np.stack([X2, P2], axis=-1)
        out = np.zeros(X1.shape)
        for k in range(len(self.w)):
            cov1 = _cov(self.s[k, 0], self.phi[k, 0])
            cov2 = _cov(self.s[k, 1], self.phi[k, 1])
            d1 = pts1 - self.mu[k, 0:2]
            d2 = pts2 - self.mu[k, 2:4]
            q1 = np.einsum("...i,ij,...j->...", d1, np.linalg.inv(cov1), d1)
            q2 = np.einsum("...i,ij,...j->...", d2, np.linalg.inv(cov2), d2)
            g1 = np.exp(-q1 / 2) / (2 * np.pi * np.sqrt(np.linalg.det(cov1)))
            g2 = np.exp(-q2 / 2) / (2 * np.pi * np.sqrt(np.linalg.det(cov2)))
            out += self.w[k] * g1 * g2
        return out


def _gaussian_overlap(mu, Sigma, c):
    """integral_{R^2} G(z; mu, Sigma) exp(-(z - c)^T (z - c)) dz, vectorized over K.

    G is the normalized 2D Gaussian. c may be COMPLEX (the cat's fringe term
    is a Gaussian with imaginary mean). Closed form: with P = Sigma^{-1},
    Q = P + 2I, b = P mu + 2c,

        overlap = exp( 1/2 b^T Q^{-1} b - 1/2 mu^T P mu - c^T c )
                  / sqrt(det(I + 2 Sigma)).

    mu: (K, 2) real, Sigma: (K, 2, 2) real, c: (2,) real or complex.
    Returns (K,) complex.
    """
    K = mu.shape[0]
    c = np.asarray(c, complex)
    P = np.linalg.inv(Sigma)                                  # (K, 2, 2)
    Q = P + 2 * np.eye(2)
    Qinv = np.linalg.inv(Q)
    b = np.einsum("kij,kj->ki", P, mu).astype(complex) + 2 * c  # (K, 2)
    term1 = 0.5 * np.einsum("ki,kij,kj->k", b, Qinv, b)
    const = -0.5 * np.einsum("ki,kij,kj->k", mu, P, mu)
    cc = c @ c
    detfac = np.sqrt(np.linalg.det(np.eye(2) + 2 * Sigma))    # (K,)
    return np.exp(term1 + const - cc) / detfac


def fidelity_vs_cat(mixture, alpha, parity=+1):
    """(2 pi)^2 * integral W_mix W_cat d^4z = tr(rho_mix rho_cat), closed form.

    The cat Wigner (states2) is a sum of four per-mode-separable pieces:
    two displaced blobs and a fringe. Writing cos(2 sqrt2 a (p1+p2)) =
    cos(.)cos(.) - sin(.)sin(.) makes the fringe separable too, and each
    single-mode fringe factor exp(-x^2 - p^2) {cos,sin}(2 sqrt2 a p) is a
    Gaussian with imaginary mean (real prefactor e^{-2 a^2}). The 4D overlap
    then factorizes into products of per-mode 2D Gaussian overlaps
    (_gaussian_overlap), each closed form. Validated in tests against
    brute-force numerical integration and the exact |<00|cat>|^2 value.
    """
    a = float(alpha)
    r2a = np.sqrt(2) * a
    norm = 2 * (1 + parity * np.exp(-4 * a ** 2))

    K = len(mixture.w)
    Sig1 = np.array([_cov(mixture.s[k, 0], mixture.phi[k, 0]) for k in range(K)])
    Sig2 = np.array([_cov(mixture.s[k, 1], mixture.phi[k, 1]) for k in range(K)])
    mu1 = mixture.mu[:, 0:2]
    mu2 = mixture.mu[:, 2:4]

    # per-mode overlaps with each cat factor
    pref = np.exp(-r2a ** 2)  # = e^{-2 a^2}, the fringe Gaussian prefactor
    c_p = np.array([r2a, 0.0])       # + blob center (mode j)
    c_m = np.array([-r2a, 0.0])      # - blob center
    c_f = np.array([0.0, 1j * r2a])  # fringe Gaussian imaginary mean

    def per_mode(mu, Sig):
        fpp = _gaussian_overlap(mu, Sig, c_p).real
        gmm = _gaussian_overlap(mu, Sig, c_m).real
        z = _gaussian_overlap(mu, Sig, c_f)
        hc = pref * z.real
        hs = pref * z.imag
        return fpp, gmm, hc, hs

    f1, g1, hc1, hs1 = per_mode(mu1, Sig1)
    f2, g2, hc2, hs2 = per_mode(mu2, Sig2)

    per_k = (
        f1 * f2
        + g1 * g2
        + parity * 2.0 * (hc1 * hc2 - hs1 * hs2)
    )
    # (2 pi)^2 / pi^2 = 4; the 1/norm is the cat normalization.
    return float(4.0 / norm * np.sum(mixture.w * per_k))
