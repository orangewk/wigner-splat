"""Two-mode reference states: 4D Wigner functions, joint homodyne pdfs, samplers.

Same conventions as states.py: dimensionless quadratures with vacuum variance
1/2, coherent |beta> sitting at (x, p) = sqrt(2) (Re beta, Im beta), and the
LO phase of mode j rotating its amplitude alpha -> alpha e^{-i theta_j}.

The target is the entangled two-mode cat |a, a> + parity |-a, -a> (real a).
"""

import numpy as np

from .states import coherent_wavefunction


class TwoModeCat:
    """Entangled two-mode cat |a, a> + parity |-a, -a>, real alpha.

    The single-mode fringe cos(2 sqrt(2) a p) of states.CatState lifts to a
    joint fringe cos(2 sqrt(2) a (p1 + p2)): the two modes are correlated only
    through the sign of their coherent amplitudes, which is the entanglement.
    """

    def __init__(self, alpha, parity=+1):
        self.alpha = float(alpha)
        self.parity = int(parity)
        # <a,a|-a,-a> = <a|-a>^2 = exp(-4 a^2); pure-state norm below.
        self.norm = 2 * (1 + self.parity * np.exp(-4 * self.alpha ** 2))

    def wigner(self, x1, p1, x2, p2):
        """Closed-form 4D Wigner W(x1, p1, x2, p2), broadcasting over the grid.

        Four terms of |A><A| + |B><B| + parity(|A><B| + |B><A|) with
        A = |a,a>, B = |-a,-a>. Diagonal terms are products of single-mode
        coherent Wigner Gaussians; the cross terms are products of the
        single-mode cross-Wigner of |a><-a|,

            W_{a,-a}(x, p) = (1/pi) exp(-x^2 - p^2 - 2 sqrt(2) a i p),

        so parity(W_{a,-a}(z1)W_{a,-a}(z2) + c.c.) is a central Gaussian times
        2 cos(2 sqrt(2) a (p1 + p2)).
        """
        a = self.alpha
        r2a = np.sqrt(2) * a
        x1, p1, x2, p2 = np.broadcast_arrays(x1, p1, x2, p2)
        # diagonal blobs at (x1, x2) = (+r2a, +r2a) and (-r2a, -r2a), p = 0
        blob_pp = np.exp(
            -((x1 - r2a) ** 2) - p1 ** 2 - (x2 - r2a) ** 2 - p2 ** 2
        )
        blob_mm = np.exp(
            -((x1 + r2a) ** 2) - p1 ** 2 - (x2 + r2a) ** 2 - p2 ** 2
        )
        fringe = (
            2
            * np.exp(-(x1 ** 2) - p1 ** 2 - x2 ** 2 - p2 ** 2)
            * np.cos(2 * r2a * (p1 + p2))
        )
        return (blob_pp + blob_mm + self.parity * fringe) / (np.pi ** 2 * self.norm)

    def homodyne_pdf(self, x1, x2, theta1, theta2):
        """Joint quadrature pdf P(x1, x2) with mode j at LO phase theta_j.

        psi(x1, x2) = [psi_{b1}(x1) psi_{b2}(x2)
                       + parity psi_{-b1}(x1) psi_{-b2}(x2)] / sqrt(norm),
        b_j = alpha e^{-i theta_j}. The norm 2(1 + parity e^{-4 a^2}) is
        theta-independent because <b_j|-b_j> = e^{-2 a^2} for every phase.
        """
        b1 = self.alpha * np.exp(-1j * theta1)
        b2 = self.alpha * np.exp(-1j * theta2)
        psi = coherent_wavefunction(x1, b1) * coherent_wavefunction(x2, b2) + (
            self.parity
            * coherent_wavefunction(x1, -b1)
            * coherent_wavefunction(x2, -b2)
        )
        return np.abs(psi) ** 2 / self.norm

    def sample_homodyne(
        self, angle_pairs, shots_per_pair, rng=None, x_max=None, grid=257
    ):
        """Simulate joint homodyne data, one 2D inverse-CDF draw per angle pair.

        For each pair, sample x1 from the x1-marginal, then x2 from the
        conditional given the sampled x1 (conditional CDFs interpolated across
        the grid rows). Deterministic given rng. Returns a list of
        ((theta1, theta2), samples) with samples of shape (shots, 2).
        """
        rng = np.random.default_rng(rng)
        x_max = x_max or (np.sqrt(2) * abs(self.alpha) + 5.0)
        xs = np.linspace(-x_max, x_max, grid)
        dx = xs[1] - xs[0]
        data = []
        for theta1, theta2 in angle_pairs:
            X1, X2 = np.meshgrid(xs, xs, indexing="ij")  # X1 varies along axis 0
            P = self.homodyne_pdf(X1, X2, theta1, theta2)  # (grid, grid)

            # x1-marginal inverse CDF
            m1 = P.sum(axis=1)
            cdf1 = np.cumsum(m1)
            cdf1 /= cdf1[-1]
            u1 = rng.uniform(size=shots_per_pair)
            x1s = np.interp(u1, cdf1, xs)

            # per-row conditional CDFs over x2
            Ccond = np.cumsum(P, axis=1)
            denom = Ccond[:, -1:]
            Ccond = Ccond / np.where(denom > 0, denom, 1.0)

            # linearly interpolate the conditional CDF at each sampled x1
            pos = np.clip((x1s - xs[0]) / dx, 0.0, grid - 1.0)
            i0 = np.clip(np.floor(pos).astype(int), 0, grid - 2)
            f = (pos - i0)[:, None]
            Cq = (1 - f) * Ccond[i0] + f * Ccond[i0 + 1]  # (shots, grid)

            # invert each interpolated conditional CDF for x2
            u2 = rng.uniform(size=shots_per_pair)
            idx = np.clip((Cq < u2[:, None]).sum(axis=1), 1, grid - 1)
            rows = np.arange(shots_per_pair)
            c_lo, c_hi = Cq[rows, idx - 1], Cq[rows, idx]
            frac = np.where(c_hi > c_lo, (u2 - c_lo) / (c_hi - c_lo), 0.0)
            x2s = xs[idx - 1] + frac * (xs[idx] - xs[idx - 1])

            samples = np.stack([x1s, x2s], axis=1)
            data.append(((float(theta1), float(theta2)), samples))
        return data
