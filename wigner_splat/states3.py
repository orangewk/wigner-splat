"""Three-mode reference states: 6D Wigner functions, joint homodyne pdfs, samplers.

Same conventions as states.py / states2.py: dimensionless quadratures with
vacuum variance 1/2, coherent |beta> sitting at (x, p) = sqrt(2) (Re beta,
Im beta), and the LO phase of mode j rotating alpha -> alpha e^{-i theta_j}.

The target is the entangled three-mode cat |a, a, a> + parity |-a, -a, -a>
(real a). This is the decisive scaling point of issue #7: n_max**3 Fock
dimensions versus O(K) full-covariance splats.
"""

import numpy as np

from .states import coherent_wavefunction


class ThreeModeCat:
    """Entangled three-mode cat |a, a, a> + parity |-a, -a, -a>, real alpha.

    The single-mode fringe cos(2 sqrt(2) a p) lifts to a joint fringe
    cos(2 sqrt(2) a (p1 + p2 + p3)): the three modes are correlated only
    through the common sign of their coherent amplitudes, which is the
    entanglement.
    """

    def __init__(self, alpha, parity=+1):
        self.alpha = float(alpha)
        self.parity = int(parity)
        # <a,a,a|-a,-a,-a> = <a|-a>^3 = exp(-6 a^2); pure-state norm below.
        self.norm = 2 * (1 + self.parity * np.exp(-6 * self.alpha ** 2))

    def wigner(self, x1, p1, x2, p2, x3, p3):
        """Closed-form 6D Wigner W(x1, p1, x2, p2, x3, p3), broadcasting.

        Four terms of |A><A| + |B><B| + parity(|A><B| + |B><A|) with
        A = |a,a,a>, B = |-a,-a,-a>. The diagonal terms are products of
        single-mode coherent Wigner Gaussians; the cross terms are products
        of the single-mode cross-Wigner of |a><-a|,

            W_{a,-a}(x, p) = (1/pi) exp(-x^2 - p^2 - 2 sqrt(2) a i p),

        which carries NO alpha-dependent prefactor. Their sum
        parity(W_{a,-a}(z1)W_{a,-a}(z2)W_{a,-a}(z3) + c.c.) is a product of
        three central Gaussians times 2 cos(2 sqrt(2) a (p1 + p2 + p3)); the
        per-mode e^{-2 a^2} suppression lives entirely in the norm
        2(1 + parity e^{-6 a^2}), not in the fringe envelope.
        """
        a = self.alpha
        r2a = np.sqrt(2) * a
        x1, p1, x2, p2, x3, p3 = np.broadcast_arrays(x1, p1, x2, p2, x3, p3)
        # diagonal blobs at (x1, x2, x3) = (+r2a,)*3 and (-r2a,)*3, p = 0
        blob_ppp = np.exp(
            -((x1 - r2a) ** 2) - p1 ** 2
            - (x2 - r2a) ** 2 - p2 ** 2
            - (x3 - r2a) ** 2 - p3 ** 2
        )
        blob_mmm = np.exp(
            -((x1 + r2a) ** 2) - p1 ** 2
            - (x2 + r2a) ** 2 - p2 ** 2
            - (x3 + r2a) ** 2 - p3 ** 2
        )
        fringe = (
            2
            * np.exp(
                -(x1 ** 2) - p1 ** 2 - x2 ** 2 - p2 ** 2 - x3 ** 2 - p3 ** 2
            )
            * np.cos(2 * r2a * (p1 + p2 + p3))
        )
        return (blob_ppp + blob_mmm + self.parity * fringe) / (
            np.pi ** 3 * self.norm
        )

    def homodyne_pdf(self, x1, x2, x3, theta1, theta2, theta3):
        """Joint quadrature pdf P(x1, x2, x3), mode j at LO phase theta_j.

        psi(x1, x2, x3) = [psi_{b1}(x1) psi_{b2}(x2) psi_{b3}(x3)
                           + parity psi_{-b1}(x1) psi_{-b2}(x2) psi_{-b3}(x3)]
                          / sqrt(norm),
        b_j = alpha e^{-i theta_j}. The norm 2(1 + parity e^{-6 a^2}) is
        theta-independent because <b_j|-b_j> = e^{-2 a^2} for every phase.
        """
        b1 = self.alpha * np.exp(-1j * theta1)
        b2 = self.alpha * np.exp(-1j * theta2)
        b3 = self.alpha * np.exp(-1j * theta3)
        psi = (
            coherent_wavefunction(x1, b1)
            * coherent_wavefunction(x2, b2)
            * coherent_wavefunction(x3, b3)
        ) + self.parity * (
            coherent_wavefunction(x1, -b1)
            * coherent_wavefunction(x2, -b2)
            * coherent_wavefunction(x3, -b3)
        )
        return np.abs(psi) ** 2 / self.norm

    def sample_homodyne(
        self, angle_triples, shots_per_triple, rng=None, x_max=None, grid=161
    ):
        """Simulate joint homodyne data via the shared grid sampler below."""
        x_max = x_max or (np.sqrt(2) * abs(self.alpha) + 5.0)
        return sample_homodyne_pdf3(
            self.homodyne_pdf, angle_triples, shots_per_triple,
            rng=rng, x_max=x_max, grid=grid,
        )


def sample_homodyne_pdf3(
    pdf, angle_triples, shots_per_triple, rng=None, x_max=7.0, grid=161
):
    """Joint homodyne sampler for ANY three-mode pdf(x1, x2, x3, th1, th2, th3).

    One 3D inverse-CDF draw per triple: chain conditional inverse-CDF sampling
    on a grid**3 lattice -- draw x1 from the x1-marginal, then x2 from the
    conditional given x1, then x3 from the conditional given (x1, x2).
    Conditional CDFs are interpolated across the grid (linear in x1 for the x2
    step, bilinear in (x1, x2) for the x3 step). Only one triple's grid is held
    at a time. Deterministic given rng.
    Returns [((theta1, theta2, theta3), samples (shots, 3))].

    Factored out of ThreeModeCat.sample_homodyne (which delegates here) so
    out-of-family targets (states3x) reuse the identical, already-tested
    sampling path.
    """
    rng = np.random.default_rng(rng)
    xs = np.linspace(-x_max, x_max, grid)
    dx = xs[1] - xs[0]
    rows = np.arange(shots_per_triple)
    data = []
    for theta1, theta2, theta3 in angle_triples:
        # sparse broadcasting keeps intermediates cheap; P is (grid,)*3
        P = pdf(
            xs[:, None, None],
            xs[None, :, None],
            xs[None, None, :],
            theta1,
            theta2,
            theta3,
        )

        # --- x1 from the marginal ---
        m1 = P.sum(axis=(1, 2))
        cdf1 = np.cumsum(m1)
        cdf1 /= cdf1[-1]
        u1 = rng.uniform(size=shots_per_triple)
        x1s = np.interp(u1, cdf1, xs)
        pos1 = np.clip((x1s - xs[0]) / dx, 0.0, grid - 1.0)
        i1 = np.clip(np.floor(pos1).astype(int), 0, grid - 2)
        f1 = pos1 - i1

        # --- x2 | x1 ---
        P12 = P.sum(axis=2)  # (grid, grid) joint (x1, x2)
        C2 = np.cumsum(P12, axis=1)
        C2 = C2 / np.where(C2[:, -1:] > 0, C2[:, -1:], 1.0)
        # linear interpolation of the conditional CDF in x1
        Cq2 = (1 - f1)[:, None] * C2[i1] + f1[:, None] * C2[i1 + 1]
        u2 = rng.uniform(size=shots_per_triple)
        idx2 = np.clip((Cq2 < u2[:, None]).sum(axis=1), 1, grid - 1)
        lo2, hi2 = Cq2[rows, idx2 - 1], Cq2[rows, idx2]
        frac2 = np.where(hi2 > lo2, (u2 - lo2) / (hi2 - lo2), 0.0)
        x2s = xs[idx2 - 1] + frac2 * (xs[idx2] - xs[idx2 - 1])
        pos2 = np.clip((x2s - xs[0]) / dx, 0.0, grid - 1.0)
        i2 = np.clip(np.floor(pos2).astype(int), 0, grid - 2)
        f2 = pos2 - i2

        # --- x3 | x1, x2 ---
        C3 = np.cumsum(P, axis=2)  # (grid, grid, grid) over x3
        C3 = C3 / np.where(C3[:, :, -1:] > 0, C3[:, :, -1:], 1.0)
        # bilinear interpolation of the conditional CDF over (x1, x2)
        w00 = ((1 - f1) * (1 - f2))[:, None]
        w01 = ((1 - f1) * f2)[:, None]
        w10 = (f1 * (1 - f2))[:, None]
        w11 = (f1 * f2)[:, None]
        Cq3 = (
            w00 * C3[i1, i2]
            + w01 * C3[i1, i2 + 1]
            + w10 * C3[i1 + 1, i2]
            + w11 * C3[i1 + 1, i2 + 1]
        )
        u3 = rng.uniform(size=shots_per_triple)
        idx3 = np.clip((Cq3 < u3[:, None]).sum(axis=1), 1, grid - 1)
        lo3, hi3 = Cq3[rows, idx3 - 1], Cq3[rows, idx3]
        frac3 = np.where(hi3 > lo3, (u3 - lo3) / (hi3 - lo3), 0.0)
        x3s = xs[idx3 - 1] + frac3 * (xs[idx3] - xs[idx3 - 1])

        samples = np.stack([x1s, x2s, x3s], axis=1)
        data.append(
            ((float(theta1), float(theta2), float(theta3)), samples)
        )
    return data
