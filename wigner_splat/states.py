"""Reference quantum states: Wigner functions, homodyne distributions, samplers.

Conventions: dimensionless quadratures with vacuum variance 1/2, i.e.
W_vac(x, p) = (1/pi) exp(-x^2 - p^2), marginal N(0, 1/2).
Coherent state |alpha> (complex alpha) sits at (x, p) = sqrt(2) (Re a, Im a).
"""

import numpy as np


def coherent_wavefunction(x, beta):
    """Position wavefunction <x|beta> of a coherent state, complex beta."""
    br, bi = np.real(beta), np.imag(beta)
    return (
        np.pi ** -0.25
        * np.exp(-((x - np.sqrt(2) * br) ** 2) / 2)
        * np.exp(1j * (np.sqrt(2) * bi * x - br * bi))
    )


class CatState:
    """Even (+) or odd (-) Schroedinger cat state ~ |alpha> +/- |-alpha>, real alpha."""

    def __init__(self, alpha, parity=+1):
        self.alpha = float(alpha)
        self.parity = int(parity)
        self.norm = 2 * (1 + self.parity * np.exp(-2 * self.alpha ** 2))

    def wigner(self, x, p):
        a = self.alpha
        blobs = np.exp(-((x - np.sqrt(2) * a) ** 2) - p ** 2) + np.exp(
            -((x + np.sqrt(2) * a) ** 2) - p ** 2
        )
        fringe = 2 * np.cos(2 * np.sqrt(2) * a * p) * np.exp(-(x ** 2) - p ** 2)
        return (blobs + self.parity * fringe) / (np.pi * self.norm)

    def homodyne_pdf(self, x, theta):
        """P_theta(x) = |<x_theta|cat>|^2; rotation maps alpha -> alpha e^{-i theta}."""
        beta = self.alpha * np.exp(-1j * theta)
        psi = coherent_wavefunction(x, beta) + self.parity * coherent_wavefunction(x, -beta)
        return np.abs(psi) ** 2 / self.norm

    def sample_homodyne(self, thetas, shots_per_angle, rng=None, x_max=None, grid=4096):
        """Simulate homodyne data: for each LO phase, draw quadrature samples
        by inverse-CDF on a fine grid. Returns list of (theta, samples)."""
        rng = np.random.default_rng(rng)
        x_max = x_max or (np.sqrt(2) * abs(self.alpha) + 5.0)
        xs = np.linspace(-x_max, x_max, grid)
        data = []
        for theta in np.atleast_1d(thetas):
            pdf = self.homodyne_pdf(xs, theta)
            cdf = np.cumsum(pdf)
            cdf /= cdf[-1]
            u = rng.uniform(size=shots_per_angle)
            data.append((float(theta), np.interp(u, cdf, xs)))
        return data
