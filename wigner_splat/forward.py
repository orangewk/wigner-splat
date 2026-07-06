"""Signed anisotropic Gaussian mixture in phase space + closed-form Radon forward model.

A splat k has weight w_k (may be negative), mean mu_k in R^2, and covariance
Sigma_k parameterized as R(phi) diag(exp(2 s1), exp(2 s2)) R(phi)^T.

The homodyne forward model is the Radon transform: measuring quadrature
x_theta marginalizes the phase-space distribution onto the unit vector
u = (cos theta, sin theta). For a Gaussian this is closed-form:

    p_theta(x) = sum_k w_k N(x; u.mu_k, u^T Sigma_k u)

which is exactly the splatting operation of 3DGS, one dimension down.
"""

import numpy as np


class SplatMixture:
    """Parameters as flat arrays for easy gradient bookkeeping.

    w:    (K,) signed weights (sum constrained to 1 by the fitter's loss)
    mu:   (K, 2) phase-space means
    s:    (K, 2) log standard deviations along principal axes
    phi:  (K,) rotation angles
    """

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
            mu=rng.uniform(-scale, scale, size=(K, 2)),
            s=np.full((K, 2), np.log(0.8)),
            phi=rng.uniform(0, np.pi, size=K),
        )

    def projected_moments(self, theta):
        """Mean and variance of each splat along quadrature direction theta."""
        u = np.array([np.cos(theta), np.sin(theta)])
        m = self.mu @ u  # (K,)
        c, s_ = np.cos(self.phi - theta), np.sin(self.phi - theta)
        # u^T R diag(v1,v2) R^T u with v_i = exp(2 s_i)
        var = np.exp(2 * self.s[:, 0]) * c ** 2 + np.exp(2 * self.s[:, 1]) * s_ ** 2
        return m, var

    def radon(self, x, theta):
        """p_theta(x): signed-mixture quadrature density (closed form)."""
        x = np.atleast_1d(x)
        m, var = self.projected_moments(theta)
        g = np.exp(-((x[:, None] - m) ** 2) / (2 * var)) / np.sqrt(2 * np.pi * var)
        return g @ self.w

    def wigner(self, x, p):
        """Evaluate the mixture on a phase-space grid (for plots/fidelity)."""
        pts = np.stack(np.broadcast_arrays(x, p), axis=-1)  # (..., 2)
        out = np.zeros(pts.shape[:-1])
        for k in range(len(self.w)):
            c, s_ = np.cos(self.phi[k]), np.sin(self.phi[k])
            R = np.array([[c, -s_], [s_, c]])
            cov = R @ np.diag(np.exp(2 * self.s[k])) @ R.T
            d = pts - self.mu[k]
            prec = np.linalg.inv(cov)
            quad = np.einsum("...i,ij,...j->...", d, prec, d)
            out += (
                self.w[k]
                * np.exp(-quad / 2)
                / (2 * np.pi * np.sqrt(np.linalg.det(cov)))
            )
        return out
