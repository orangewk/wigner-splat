"""Full-covariance three-mode signed Gaussian mixture + closed-form joint Radon
model -- the faithful 3DGS analog lifted from forward2f to 6D phase space.

A splat here carries a FULL anisotropic 6x6 covariance (21 numbers), exactly as
forward2f's splat carries a full 4x4 one. The projected covariance of the
measured triple (x_theta1, x_theta2, x_theta3) then keeps the CROSS terms a
separable splat cannot produce, so ONE signed splat can stretch along the 6D
ridge where the entangled fringe cos(2 sqrt2 a (p1+p2+p3)) is constant and
oscillate across it.

Parameterization (Cholesky, 27 numbers per splat -- 6 mean + 21 covariance):
    w:   (K,)     signed weights (sum constrained to 1 by the fitter's loss)
    mu:  (K, 6)   joint means (x1, p1, x2, p2, x3, p3)
    ld:  (K, 6)   log of the Cholesky diagonal; L[i, i] = exp(ld[i]) > 0
    lo:  (K, 15)  the 15 strictly-lower entries of L, row-major
                  (np.tril_indices(6, -1) order)
Sigma = L L^T is SPD for any (ld, lo). This is the 3DGS covariance
parameterization (scale = exp(ld), the strictly-lower entries the rotation)
lifted from 3D to 6D phase space.

Projection: measuring (x_theta1, x_theta2, x_theta3) is the linear map U (6x3),
U[:,0] = (cos th1, sin th1, 0, 0, 0, 0), U[:,1] = (0, 0, cos th2, sin th2, 0, 0),
U[:,2] = (0, 0, 0, 0, cos th3, sin th3). The projected mean is m = U^T mu (3,)
and the projected covariance is C = U^T Sigma U (3x3, WITH the cross terms). The
joint quadrature density on the (x1, x2, x3) bin grid is the correlated 3D
Gaussian N(x; m, C) -- the closed form the whole fit rests on (test: equals the
numeric 3D Radon of wigner6).
"""

import numpy as np

# strictly-lower-triangular index order for the 15 free off-diagonal entries
_TRIL_I, _TRIL_J = np.tril_indices(6, -1)
_DIAG = np.arange(6)


def build_L(ld, lo):
    """Lower-triangular Cholesky factors L (K,6,6) from (ld (K,6), lo (K,15))."""
    ld = np.atleast_2d(ld)
    lo = np.atleast_2d(lo)
    K = ld.shape[0]
    L = np.zeros((K, 6, 6))
    L[:, _DIAG, _DIAG] = np.exp(ld)
    L[:, _TRIL_I, _TRIL_J] = lo
    return L


def _U(theta1, theta2, theta3):
    """The 6x3 measurement projection U for a single angle triple."""
    U = np.zeros((6, 3))
    U[0, 0], U[1, 0] = np.cos(theta1), np.sin(theta1)
    U[2, 1], U[3, 1] = np.cos(theta2), np.sin(theta2)
    U[4, 2], U[5, 2] = np.cos(theta3), np.sin(theta3)
    return U


class SplatMixture3F:
    """Full-covariance three-mode splat mixture with flat-array parameters."""

    def __init__(self, w, mu, ld, lo):
        self.w = np.asarray(w, float)
        self.mu = np.asarray(mu, float)
        self.ld = np.asarray(ld, float)
        self.lo = np.asarray(lo, float)

    @classmethod
    def random_init(cls, K, scale=2.0, log_std=np.log(0.8), rng=None):
        rng = np.random.default_rng(rng)
        return cls(
            w=np.full(K, 1.0 / K),
            mu=rng.uniform(-scale, scale, size=(K, 6)),
            ld=np.full((K, 6), log_std),
            lo=np.zeros((K, 15)),
        )

    def L(self):
        return build_L(self.ld, self.lo)

    def Sigma(self):
        L = self.L()
        return L @ L.transpose(0, 2, 1)

    def projected(self, theta1, theta2, theta3):
        """Projected means m (K,3) and covariances C (K,3,3) at one triple."""
        U = _U(theta1, theta2, theta3)
        Sigma = self.Sigma()
        m = self.mu @ U                                   # (K, 3)
        C = np.einsum("ar,kab,bs->krs", U, Sigma, U)      # (K, 3, 3)
        return m, C

    def radon3(self, x1, x2, x3, theta1, theta2, theta3, chunk=None,
               cell_var=0.0):
        """Joint quadrature density on the (x1, x2, x3) grid.

        Returns array of shape (len(x1), len(x2), len(x3)). The correlated 3D
        Gaussian N(x; m, C) summed over splats. To bound memory the (Bx, K)
        moment tensor is chunked over the outer x1 axis when ``chunk`` is set.

        ``cell_var`` (= bin_width^2 / 12) inflates the projected covariance
        diagonal so the returned value is the model's cell-AVERAGE density
        rather than its point value at the bin center -- the exact-to-O(h^4)
        forward model for a density=True histogram (a box of width h has
        variance h^2/12; convolving the Gaussian with it matches the second
        moment). Leave at 0 for a point evaluation of the true marginal.
        """
        x1 = np.atleast_1d(x1)
        x2 = np.atleast_1d(x2)
        x3 = np.atleast_1d(x3)
        m, C = self.projected(theta1, theta2, theta3)
        if cell_var:
            C = C + cell_var * np.eye(3)
        P = np.linalg.inv(C)                              # (K, 3, 3)
        det = np.linalg.det(C)                            # (K,)
        d2 = x2[:, None] - m[:, 1]                        # (By, K)
        d3 = x3[:, None] - m[:, 2]                        # (Bz, K)
        pref = 1.0 / ((2 * np.pi) ** 1.5 * np.sqrt(det))  # (K,)
        Bx = len(x1)
        out = np.empty((Bx, len(x2), len(x3)))
        step = chunk or Bx
        for lo in range(0, Bx, step):
            d1 = x1[lo : lo + step, None] - m[:, 0]       # (bx, K)
            quad = (
                P[:, 0, 0] * d1[:, None, None, :] ** 2
                + P[:, 1, 1] * d2[None, :, None, :] ** 2
                + P[:, 2, 2] * d3[None, None, :, :] ** 2
                + 2 * P[:, 0, 1] * d1[:, None, None, :] * d2[None, :, None, :]
                + 2 * P[:, 0, 2] * d1[:, None, None, :] * d3[None, None, :, :]
                + 2 * P[:, 1, 2] * d2[None, :, None, :] * d3[None, None, :, :]
            )                                             # (bx, By, Bz, K)
            N = np.exp(-quad / 2) * pref
            out[lo : lo + step] = N @ self.w
        return out

    def wigner6(self, x1, p1, x2, p2, x3, p3):
        """Evaluate the 6D mixture (full-cov Gaussians) on a broadcast grid."""
        X1, P1, X2, P2, X3, P3 = np.broadcast_arrays(x1, p1, x2, p2, x3, p3)
        pts = np.stack([X1, P1, X2, P2, X3, P3], axis=-1)  # (..., 6)
        Sigma = self.Sigma()
        out = np.zeros(X1.shape)
        for k in range(len(self.w)):
            d = pts - self.mu[k]
            prec = np.linalg.inv(Sigma[k])
            quad = np.einsum("...i,ij,...j->...", d, prec, d)
            out += (
                self.w[k]
                * np.exp(-quad / 2)
                / ((2 * np.pi) ** 3 * np.sqrt(np.linalg.det(Sigma[k])))
            )
        return out


def _gaussian_overlap(mu, Sigma, c):
    """integral G(z; mu, Sigma) exp(-(z - c)^T (z - c)) dz, over K, ANY dim d.

    The dimension-agnostic form of forward2f._gaussian_overlap4 (identical
    closed form). G is the normalized d-dim Gaussian; c may be COMPLEX (the cat
    fringe is a Gaussian with imaginary mean). With P = Sigma^{-1},
    Q = P + 2I, b = P mu + 2c,

        overlap = exp( 1/2 b^T Q^{-1} b - 1/2 mu^T P mu - c^T c )
                  / sqrt(det(I + 2 Sigma)).

    mu: (K, d) real, Sigma: (K, d, d) real, c: (d,) real or complex.
    Returns (K,) complex.
    """
    c = np.asarray(c, complex)
    d = mu.shape[-1]
    I = np.eye(d)
    P = np.linalg.inv(Sigma)                                    # (K, d, d)
    Q = P + 2 * I
    Qinv = np.linalg.inv(Q)
    b = np.einsum("kij,kj->ki", P, mu).astype(complex) + 2 * c  # (K, d)
    term1 = 0.5 * np.einsum("ki,kij,kj->k", b, Qinv, b)
    const = -0.5 * np.einsum("ki,kij,kj->k", mu, P, mu)
    cc = c @ c
    detfac = np.sqrt(np.linalg.det(I + 2 * Sigma))              # (K,)
    return np.exp(term1 + const - cc) / detfac


def fidelity_vs_cat3(mixture, alpha, parity=+1):
    """(2 pi)^3 * integral W_mix W_cat3 d^6z = tr(rho_mix rho_cat3), closed form.

    The three-mode cat Wigner (states3) is, up to 1/(pi^3 norm), the sum of two
    coherent blobs exp(-|z - c_ppp|^2), exp(-|z - c_mmm|^2) and a fringe
    2 e^{-3 r2a^2} Re exp(-|z - c_f|^2) with c_ppp = (r2a,0,r2a,0,r2a,0),
    c_mmm = -c_ppp, c_f = (0, i r2a, 0, i r2a, 0, i r2a), r2a = sqrt2 a
    (completing the square on exp(-|z|^2) cos(2 r2a (p1+p2+p3)): each mode's
    -p^2 + 2 i r2a p contributes a factor e^{-r2a^2}, hence the real prefactor
    e^{-3 r2a^2} for three modes). The overlap of a splat N(mu, Sigma) with each
    exp(-|z - c|^2) is _gaussian_overlap, so

        fidelity = 8 / norm * sum_k w_k [ O_ppp + O_mmm
                                         + parity * 2 e^{-3 r2a^2} Re O_f ],

    the exact 6D generalization of forward2f.fidelity_vs_cat ((2 pi)^3/pi^3 = 8,
    norm = 2(1 + parity e^{-6 a^2})). Validated in tests against brute-force 6D
    integration and the exact |<000|cat3>|^2 vacuum value.
    """
    a = float(alpha)
    r2a = np.sqrt(2) * a
    norm = 2 * (1 + parity * np.exp(-6 * a ** 2))

    mu = mixture.mu
    Sigma = mixture.Sigma()

    c_ppp = np.array([r2a, 0.0, r2a, 0.0, r2a, 0.0])
    c_mmm = -c_ppp
    c_f = np.array([0.0, 1j * r2a, 0.0, 1j * r2a, 0.0, 1j * r2a])

    O_ppp = _gaussian_overlap(mu, Sigma, c_ppp).real
    O_mmm = _gaussian_overlap(mu, Sigma, c_mmm).real
    O_f = _gaussian_overlap(mu, Sigma, c_f)

    per_k = O_ppp + O_mmm + parity * 2.0 * np.exp(-3 * r2a ** 2) * O_f.real
    return float(8.0 / norm * np.sum(mixture.w * per_k))


def _cat3_overlap_sum(w, mu, Sigma, r2a, parity, cross_scale, norm):
    """Shared core of the cat-family overlaps: blobs at +-r2a, damped fringe.

    tr(rho_mix rho_target) for a target of the exact cat form whose Wigner is
    [blob(+r2a) + blob(-r2a) + parity * cross_scale * 2 cos(2 r2a sum p)
    e^{-|z|^2}] / (pi^3 norm). cross_scale = 1 is the pure cat
    (fidelity_vs_cat3); a lossy cat damps the fringe coefficient only.
    """
    c_ppp = np.array([r2a, 0.0, r2a, 0.0, r2a, 0.0])
    c_f = np.array([0.0, 1j * r2a, 0.0, 1j * r2a, 0.0, 1j * r2a])
    O_ppp = _gaussian_overlap(mu, Sigma, c_ppp).real
    O_mmm = _gaussian_overlap(mu, Sigma, -c_ppp).real
    O_f = _gaussian_overlap(mu, Sigma, c_f)
    per_k = (
        O_ppp + O_mmm
        + parity * cross_scale * 2.0 * np.exp(-3 * r2a ** 2) * O_f.real
    )
    return float(8.0 / norm * np.sum(w * per_k))


def overlap_vs_lossy_cat3(mixture, alpha, parity=+1, eta=0.8):
    """tr(rho_mix rho_lossy), closed form (issue #28 three-way scoring).

    The per-mode loss channel maps coherent dyads to coherent dyads
    (E(|a><b|) = <b|a>^{1-eta} |sqrt(eta)a><sqrt(eta)b|), so the lossy-cat
    Wigner keeps the exact cat form with amplitude sqrt(eta) alpha and fringe
    coefficient damped by e^{-6 alpha^2 (1-eta)}; the norm is the input cat's
    (trace preserved). NOTE: the target is MIXED, so a perfect reconstruction
    scores the target purity tr(rho_lossy^2) (lossy_cat3_purity), not 1.
    """
    a = float(alpha)
    r2a = np.sqrt(2.0) * np.sqrt(eta) * a
    cross = np.exp(-6.0 * a ** 2 * (1.0 - eta))
    norm = 2 * (1 + parity * np.exp(-6 * a ** 2))
    return _cat3_overlap_sum(
        mixture.w, mixture.mu, mixture.Sigma(), r2a, parity, cross, norm
    )


def lossy_cat3_purity(alpha, parity=+1, eta=0.8):
    """tr(rho_lossy^2) -- the overlap score a PERFECT reconstruction attains.

    Computed exactly on the 2-ket coherent span: rho = P M P^dag with
    M = [[1, pc], [pc, 1]]/norm, Gram S = [[1, g], [g, 1]],
    g = <A'|B'> = e^{-6 eta a^2}, pc = parity e^{-6 a^2 (1-eta)};
    tr(rho^2) = tr((M S)^2).
    """
    a = float(alpha)
    g = np.exp(-6.0 * eta * a ** 2)
    pc = parity * np.exp(-6.0 * a ** 2 * (1.0 - eta))
    norm = 2 * (1 + parity * np.exp(-6 * a ** 2))
    M = np.array([[1.0, pc], [pc, 1.0]]) / norm
    S = np.array([[1.0, g], [g, 1.0]])
    return float(np.trace(M @ S @ M @ S))


def overlap_vs_squeezed_cat3(mixture, alpha, parity=+1, r=0.0):
    """tr(rho_mix rho_sqcat), closed form via the symplectic squeeze map.

    D(a)S(r)|0> = S(r)D(a e^r)|0> for real a, r (x-variance e^{-2r}/2
    convention), so rho_sqcat = S(r)^{x3} rho_cat(a e^r) S(r)^{x3 dag}
    EXACTLY. Wigner transforms by the symplectic coordinate map
    (x, p) -> (e^r x, e^{-r} p) per mode (det 1), so
    tr(rho_mix rho_sqcat) = tr(rho_mix' rho_cat(a e^r)) with the mixture
    components mapped mu -> S mu, Sigma -> S Sigma S^T. Reuses the exact
    pure-cat overlap; the target is PURE, so a perfect score is 1.
    """
    a_eff = float(alpha) * np.exp(r)
    r2a = np.sqrt(2.0) * a_eff
    norm = 2 * (1 + parity * np.exp(-6 * a_eff ** 2))
    s = np.tile([np.exp(r), np.exp(-r)], 3)          # diag symplectic map, 6D
    mu = mixture.mu * s[None, :]
    Sigma = mixture.Sigma() * s[None, :, None] * s[None, None, :]
    return _cat3_overlap_sum(mixture.w, mu, Sigma, r2a, parity, 1.0, norm)
