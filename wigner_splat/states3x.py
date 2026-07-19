"""Out-of-family three-mode reference targets (issue #28).

Two targets that are NOT in the rank-1 coherent-product family bbdagM fits:

* LossyThreeModeCat -- the entangled cat after a per-mode pure-loss channel of
  transmissivity eta. The state is MIXED (rank 2), so it is out-of-family for
  any rank-1 ket ansatz but inside the rank-2 rho = BB^dagger span: the loss
  channel maps coherent dyads to coherent dyads,
      E(|a><b|) = <b|a>^{1-eta} |sqrt(eta) a><sqrt(eta) b|,
  so the lossy cat lives on span{|sqrt(eta)A>, |sqrt(eta)B>} with the cross
  term damped by e^{-6 a^2 (1 - eta)}. This makes it the sharp test for the
  rank-R extension: rank 1 must plateau, rank 2 can be exact.

* SqueezedThreeModeCat -- |psi> = (D(a)S(xi))^{x3} |0> + parity (D(-a)S(xi))^{x3} |0>
  per mode (same real squeeze xi on every mode). PURE, but squeezed kets are
  outside the coherent-product dictionary at any finite K, so this probes how
  the coherent ansatz degrades out of family (finite-K approximation error).

Both expose homodyne_pdf(x1, x2, x3, th1, th2, th3) and delegate sampling to
states3.sample_homodyne_pdf3, the identical tested path used by ThreeModeCat.
Conventions unchanged: vacuum variance 1/2, LO rotation alpha -> alpha
e^{-i theta}, xi -> xi e^{-2 i theta} (bbdag.sq_coherent_wavefunction).
"""

import numpy as np

from .bbdag import sq_coherent_wavefunction
from .states import coherent_wavefunction
from .states3 import sample_homodyne_pdf3


class LossyThreeModeCat:
    """|a,a,a> + parity |-a,-a,-a> after per-mode loss of transmissivity eta.

    rho = [ |A'><A'| + |B'><B'| + parity c^{1-eta} (|A'><B'| + |B'><A'|) ] / norm
    with A' = |sqrt(eta) a>^{x3}, B' = |-sqrt(eta) a>^{x3}, c = <B|A> = e^{-6 a^2},
    norm = 2 (1 + parity e^{-6 a^2}) (the loss channel is trace preserving, so
    the norm is the input cat's). At eta = 1 this is exactly ThreeModeCat.
    """

    def __init__(self, alpha, parity=+1, eta=0.8):
        if not 0.0 < eta <= 1.0:
            raise ValueError(f"eta must be in (0, 1], got {eta}")
        self.alpha = float(alpha)
        self.parity = int(parity)
        self.eta = float(eta)
        self.a_out = np.sqrt(self.eta) * self.alpha    # surviving amplitude
        self.cross = np.exp(-6 * self.alpha ** 2 * (1 - self.eta))
        self.norm = 2 * (1 + self.parity * np.exp(-6 * self.alpha ** 2))

    def coherent_span(self):
        """(kets_alpha (2, 3), M (2, 2)) with rho = sum_ij M_ij |ket_i><ket_j|."""
        a = self.a_out
        kets = np.array([[a, a, a], [-a, -a, -a]], complex)
        M = np.array([
            [1.0, self.parity * self.cross],
            [self.parity * self.cross, 1.0],
        ]) / self.norm
        return kets, M

    def homodyne_pdf(self, x1, x2, x3, theta1, theta2, theta3):
        b1 = self.a_out * np.exp(-1j * theta1)
        b2 = self.a_out * np.exp(-1j * theta2)
        b3 = self.a_out * np.exp(-1j * theta3)
        psiA = (
            coherent_wavefunction(x1, b1)
            * coherent_wavefunction(x2, b2)
            * coherent_wavefunction(x3, b3)
        )
        psiB = (
            coherent_wavefunction(x1, -b1)
            * coherent_wavefunction(x2, -b2)
            * coherent_wavefunction(x3, -b3)
        )
        dens = (
            np.abs(psiA) ** 2
            + np.abs(psiB) ** 2
            + self.parity * self.cross * 2 * np.real(psiA * np.conj(psiB))
        )
        return dens / self.norm

    def sample_homodyne(self, angle_triples, shots_per_triple, rng=None,
                        x_max=None, grid=161):
        x_max = x_max or (np.sqrt(2) * abs(self.alpha) + 5.0)
        return sample_homodyne_pdf3(
            self.homodyne_pdf, angle_triples, shots_per_triple,
            rng=rng, x_max=x_max, grid=grid,
        )


class ThermalLossyThreeModeCat:
    """Lossy cat followed by per-mode classical Gaussian displacement noise:
    a FULL-RANK held-out target (issue #38, the blind-generalization gate).

    rho = N_sigma(E_eta(|cat3><cat3|)) with N_sigma the isotropic
    random-displacement channel adding ``sigma_add`` variance to EVERY
    quadrature (a Gaussian mixture of displaced lossy cats -- full rank, so
    no finite-rank ket mixture contains it). The homodyne pdf is the lossy
    cat's pdf convolved per mode with N(0, sigma_add), and each of the four
    span terms stays closed form: the per-mode pair densities are the
    bbdagS loss machinery evaluated at eta = 1, sigma2 = sigma_add (the
    same Gaussian-convolution mathematics as issue #42, used here on the
    TARGET side). sigma_add = 0 reduces exactly to LossyThreeModeCat.
    """

    def __init__(self, alpha, parity=+1, eta=0.8, sigma_add=0.1):
        if sigma_add < 0.0:
            raise ValueError(f"sigma_add must be >= 0, got {sigma_add}")
        self._lossy = LossyThreeModeCat(alpha, parity, eta)
        self.alpha = self._lossy.alpha
        self.parity = self._lossy.parity
        self.eta = self._lossy.eta
        self.a_out = self._lossy.a_out
        self.cross = self._lossy.cross
        self.norm = self._lossy.norm
        self.sigma_add = float(sigma_add)

    def _mode_pair_terms(self, x, theta):
        """Convolved per-mode pair densities O[..., i, j] on x's own shape.

        O[i, j](x) = integral f_i(y) conj(f_j)(y) N(x - y; sigma_add) dy for
        the two rotated kets (+b, -b) -- via bbdagS's tilted pair-density at
        eta = 1 (conj(f_c) f_d ordering, transposed here to psi_i conj_j).
        """
        from .bbdagS import _gauss_params, _lossy_mode_pair_density
        b = self.a_out * np.exp(-1j * theta)
        kets = np.array([b, -b], complex)
        params = _gauss_params(kets, np.zeros(2, complex))
        x = np.asarray(x, float)
        O, _, _ = _lossy_mode_pair_density(
            params, x.ravel(), 1.0, self.sigma_add)
        # transpose (c, d) -> psi_d conj(psi_c) ordering used by the span sum
        O = np.transpose(O, (0, 2, 1))
        return O.reshape(x.shape + (2, 2))

    def homodyne_pdf(self, x1, x2, x3, theta1, theta2, theta3):
        if self.sigma_add <= 1e-14:
            return self._lossy.homodyne_pdf(x1, x2, x3, theta1, theta2,
                                            theta3)
        pc = self.parity * self.cross
        M = np.array([[1.0, pc], [pc, 1.0]]) / self.norm
        O1 = self._mode_pair_terms(np.asarray(x1, float), theta1)
        O2 = self._mode_pair_terms(np.asarray(x2, float), theta2)
        O3 = self._mode_pair_terms(np.asarray(x3, float), theta3)
        dens = 0.0
        for i in range(2):
            for j in range(2):
                dens = dens + M[i, j] * np.real(
                    O1[..., i, j] * O2[..., i, j] * O3[..., i, j])
        return np.maximum(np.real(dens), 0.0)

    def sample_homodyne(self, angle_triples, shots_per_triple, rng=None,
                        x_max=None, grid=161):
        x_max = x_max or (np.sqrt(2) * abs(self.alpha) + 5.0
                          + 3.0 * np.sqrt(self.sigma_add))
        return sample_homodyne_pdf3(
            self.homodyne_pdf, angle_triples, shots_per_triple,
            rng=rng, x_max=x_max, grid=grid,
        )


class SqueezedThreeModeCat:
    """Pure squeezed cat: sum_c parity^c prod_m D(±a) S(xi) |0>, real a, xi.

    xi = r (real, r > 0 squeezes x at theta = 0). The per-mode kets rotate as
    alpha -> alpha e^{-i theta}, xi -> xi e^{-2 i theta}. The norm is computed
    once by 1D quadrature of the per-mode overlap <g_-|g_+> (theta-independent:
    a global LO rotation is unitary on each mode).
    """

    def __init__(self, alpha, parity=+1, r=0.4, norm_grid=None):
        self.alpha = float(alpha)
        self.parity = int(parity)
        self.r = float(r)
        if norm_grid is None:
            x_max = np.sqrt(2) * abs(self.alpha) + 8.0
            norm_grid = np.linspace(-x_max, x_max, 4001)
        gp = sq_coherent_wavefunction(norm_grid, self.alpha, self.r)
        gm = sq_coherent_wavefunction(norm_grid, -self.alpha, self.r)
        ov = np.trapezoid(np.conj(gm) * gp, norm_grid)   # <g_-|g_+>, real target
        # <psi|psi> = 2 (1 + parity Re<g_-|g_+>^3) for equal-weight two kets
        self.norm = float(2 * (1 + self.parity * np.real(ov ** 3)))

    def _mode_psis(self, x, theta):
        a = self.alpha * np.exp(-1j * theta)
        xi = self.r * np.exp(-2j * theta)
        return (
            sq_coherent_wavefunction(x, a, xi),
            sq_coherent_wavefunction(x, -a, xi),
        )

    def homodyne_pdf(self, x1, x2, x3, theta1, theta2, theta3):
        g1p, g1m = self._mode_psis(x1, theta1)
        g2p, g2m = self._mode_psis(x2, theta2)
        g3p, g3m = self._mode_psis(x3, theta3)
        psi = g1p * g2p * g3p + self.parity * (g1m * g2m * g3m)
        return np.abs(psi) ** 2 / self.norm

    def psi_mode_factors(self, x, theta):
        """Per-mode (plus, minus) wavefunction factors at LO phase theta.

        Exposed for closed-ish-form fidelity: the target is a 2-term product
        superposition, so overlaps with any product ket factorize per mode.
        """
        return self._mode_psis(x, theta)

    def sample_homodyne(self, angle_triples, shots_per_triple, rng=None,
                        x_max=None, grid=161):
        x_max = x_max or (np.sqrt(2) * abs(self.alpha) + 5.0 + 3.0 * self.r)
        return sample_homodyne_pdf3(
            self.homodyne_pdf, angle_triples, shots_per_triple,
            rng=rng, x_max=x_max, grid=grid,
        )


def fidelity_vs_squeezed_cat3(state, target, grid=None):
    """Exact-state fidelity |<psi_fit|target>|^2 / (Z_fit Z_target).

    state: CoherentKetState (K coherent-product kets). target:
    SqueezedThreeModeCat. Each cross overlap factorizes into per-mode 1D
    integrals <coherent alpha_km | g_(+/-)>, evaluated by quadrature.
    """
    if grid is None:
        x_max = np.sqrt(2) * (abs(target.alpha) + 2.0) + 8.0
        grid = np.linspace(-x_max, x_max, 4001)
    gp = sq_coherent_wavefunction(grid, target.alpha, target.r)
    gm = sq_coherent_wavefunction(grid, -target.alpha, target.r)
    # ov[k, m, +/-] = <alpha_km | g_(+/-)> = integral conj(coh) g
    K, M = state.alpha.shape
    ov = np.empty((K, M, 2), complex)
    for k in range(K):
        for m in range(M):
            coh = coherent_wavefunction(grid, state.alpha[k, m])
            ov[k, m, 0] = np.trapezoid(np.conj(coh) * gp, grid)
            ov[k, m, 1] = np.trapezoid(np.conj(coh) * gm, grid)
    # <psi_fit | target> = sum_k conj(z_k) [prod_m ov+ + parity prod_m ov-]
    amp = np.sum(
        np.conj(state.z)
        * (np.prod(ov[:, :, 0], axis=1)
           + target.parity * np.prod(ov[:, :, 1], axis=1))
    )
    return float(np.abs(amp) ** 2 / (state.norm_sq() * target.norm))


def overlap_matrix_coherent_products(kets_a, kets_b):
    """G[i, j] = <prod_m kets_a[i, m] | prod_m kets_b[j, m]>, closed form."""
    from .bbdagM import coherent_overlap
    ov = coherent_overlap(
        np.asarray(kets_a, complex)[:, None, :],
        np.asarray(kets_b, complex)[None, :, :],
    )
    return np.prod(ov, axis=2)


def uhlmann_fidelity_vs_lossy_cat3(state, target):
    """Exact Uhlmann fidelity F = (tr sqrt(sqrt(rho) sigma sqrt(rho)))^2.

    target: LossyThreeModeCat (rho, rank 2 on a coherent-product span).
    state: MixedCoherentKetState or CoherentKetState (sigma = BB^dagger / Z).
    Both operators live in the finite span of their coherent-product kets, so
    the computation is EXACT: build the joint (non-orthogonal) ket basis, its
    Gram matrix S, Loewdin-orthonormalize with S^{1/2}, and run the Uhlmann
    formula on the resulting small Hermitian matrices. No Fock truncation.
    """
    t_kets, t_M = target.coherent_span()

    if hasattr(state, "columns"):        # MixedCoherentKetState
        cols = state.columns()
    else:                                # CoherentKetState (rank 1)
        cols = [state]
    f_kets = np.concatenate([np.asarray(c.alpha, complex) for c in cols])
    # sigma coefficient matrix on f_kets: sum_r outer(z_r, conj(z_r)) / Z
    Z = sum(c.norm_sq() for c in cols)
    K_each = [len(c.z) for c in cols]
    f_M = np.zeros((len(f_kets), len(f_kets)), complex)
    at = 0
    for c, k in zip(cols, K_each):
        f_M[at:at + k, at:at + k] = np.outer(c.z, np.conj(c.z)) / Z
        at += k

    kets = np.concatenate([t_kets, f_kets])          # (n, M) joint basis
    n_t = len(t_kets)
    M_rho = np.zeros((len(kets), len(kets)), complex)
    M_rho[:n_t, :n_t] = t_M
    M_sig = np.zeros_like(M_rho)
    M_sig[n_t:, n_t:] = f_M

    S = overlap_matrix_coherent_products(kets, kets)  # Gram, Hermitian PSD
    w, U = np.linalg.eigh(S)
    w = np.maximum(w, 0.0)
    sqrtS = (U * np.sqrt(w)) @ U.conj().T
    # orthonormal-frame representations: rho_o = S^{1/2} M S^{1/2}
    rho_o = sqrtS @ M_rho @ sqrtS
    sig_o = sqrtS @ M_sig @ sqrtS
    rho_o = (rho_o + rho_o.conj().T) / 2
    sig_o = (sig_o + sig_o.conj().T) / 2

    wr, Ur = np.linalg.eigh(rho_o)
    wr = np.maximum(wr, 0.0)
    sqrt_rho = (Ur * np.sqrt(wr)) @ Ur.conj().T
    inner = sqrt_rho @ sig_o @ sqrt_rho
    inner = (inner + inner.conj().T) / 2
    wi = np.maximum(np.linalg.eigvalsh(inner), 0.0)
    return float(np.sum(np.sqrt(wi)) ** 2)
