"""Full-covariance two-mode signed Gaussian mixture + closed-form joint Radon
model -- the faithful 3DGS analog for two modes.

Where forward2.SplatMixture2 restricted every splat to a block-diagonal 4x4
covariance (a PRODUCT of two per-mode 2D Gaussians), a splat here carries a
FULL anisotropic 4x4 covariance, exactly as a 3DGS Gaussian is fully
anisotropic in 3D. That single change is the whole point of this module: the
projected covariance of the measured pair (x_theta1, x_theta2) then keeps the
CROSS term C[0,1] that a separable splat cannot produce, so ONE signed splat
can stretch along the p1-p2 ridge (where the entangled fringe
cos(2 sqrt2 a (p1+p2)) is constant) and oscillate along p1+p2. The separable
representation needed ~80 axis-aligned splats to tile that ridge; a full-cov
mixture should need ~K=8 signed splats, like the 1D cat.

Parameterization (Cholesky, 15 numbers per splat):
    w:   (K,)     signed weights (sum constrained to 1 by the fitter's loss)
    mu:  (K, 4)   joint means (x1, p1, x2, p2)
    ld:  (K, 4)   log of the Cholesky diagonal; L[i, i] = exp(ld[i]) > 0
    lo:  (K, 6)   the 6 strictly-lower entries of L, order
                  (1,0),(2,0),(2,1),(3,0),(3,1),(3,2)
Sigma = L L^T is symmetric positive definite for any (ld, lo) because the
diagonal exp(ld) > 0 makes L invertible. This is the 3DGS covariance
parameterization (scale = exp(ld), the strictly-lower entries play the role of
the rotation) lifted from 3D to 4D phase space.

Projection: measuring (x_theta1, x_theta2) is the linear map U (4x2),
U[:,0] = (cos th1, sin th1, 0, 0), U[:,1] = (0, 0, cos th2, sin th2). The
projected mean is m = U^T mu (2,) and the projected covariance is
C = U^T Sigma U (2x2, WITH the cross term). The joint quadrature density on
the (x1, x2) bin grid is the correlated 2D Gaussian N(x; m, C) -- the closed
form the whole fit rests on (test: equals the numeric 2D Radon of wigner4).
"""

import numpy as np

# strictly-lower-triangular index order for the 6 free off-diagonal entries
_TRIL_I = np.array([1, 2, 2, 3, 3, 3])
_TRIL_J = np.array([0, 0, 1, 0, 1, 2])
_DIAG = np.arange(4)


def build_L(ld, lo):
    """Lower-triangular Cholesky factors L (K,4,4) from (ld (K,4), lo (K,6))."""
    ld = np.atleast_2d(ld)
    lo = np.atleast_2d(lo)
    K = ld.shape[0]
    L = np.zeros((K, 4, 4))
    L[:, _DIAG, _DIAG] = np.exp(ld)
    L[:, _TRIL_I, _TRIL_J] = lo
    return L


def _U(theta1, theta2):
    """The 4x2 measurement projection U for a single angle pair."""
    U = np.zeros((4, 2))
    U[0, 0], U[1, 0] = np.cos(theta1), np.sin(theta1)
    U[2, 1], U[3, 1] = np.cos(theta2), np.sin(theta2)
    return U


class SplatMixture2F:
    """Full-covariance two-mode splat mixture with flat-array parameters."""

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
            mu=rng.uniform(-scale, scale, size=(K, 4)),
            ld=np.full((K, 4), log_std),
            lo=np.zeros((K, 6)),
        )

    @classmethod
    def from_separable(cls, mix2):
        """Lift a forward2.SplatMixture2 to an equivalent full-cov mixture.

        The block-diagonal covariance is Cholesky-factored per 2x2 block, so
        this is a lossless embedding -- used to cross-check fidelity_vs_cat and
        wigner4 against the separable module.
        """
        from .forward2 import _cov

        K = len(mix2.w)
        ld = np.zeros((K, 4))
        lo = np.zeros((K, 6))
        for k in range(K):
            Sig = np.zeros((4, 4))
            Sig[0:2, 0:2] = _cov(mix2.s[k, 0], mix2.phi[k, 0])
            Sig[2:4, 2:4] = _cov(mix2.s[k, 1], mix2.phi[k, 1])
            L = np.linalg.cholesky(Sig)
            ld[k] = np.log(np.diag(L))
            lo[k] = L[_TRIL_I, _TRIL_J]
        return cls(mix2.w.copy(), mix2.mu.copy(), ld, lo)

    def L(self):
        return build_L(self.ld, self.lo)

    def Sigma(self):
        L = self.L()
        return L @ L.transpose(0, 2, 1)

    def projected(self, theta1, theta2):
        """Projected means m (K,2) and covariances C (K,2,2) at one angle pair."""
        U = _U(theta1, theta2)
        Sigma = self.Sigma()
        m = self.mu @ U                                  # (K, 2)
        C = np.einsum("ar,kab,bs->krs", U, Sigma, U)     # (K, 2, 2)
        return m, C

    def radon2(self, x1, x2, theta1, theta2):
        """Joint quadrature density on the (x1, x2) grid: (len(x1), len(x2))."""
        x1 = np.atleast_1d(x1)
        x2 = np.atleast_1d(x2)
        m, C = self.projected(theta1, theta2)
        P = np.linalg.inv(C)                             # (K, 2, 2)
        det = np.linalg.det(C)                           # (K,)
        d1 = x1[:, None] - m[:, 0]                       # (Bx, K)
        d2 = x2[:, None] - m[:, 1]                       # (By, K)
        # quad[i, j, k] = P00 d1^2 + 2 P01 d1 d2 + P11 d2^2
        quad = (
            P[:, 0, 0] * d1[:, None, :] ** 2
            + 2 * P[:, 0, 1] * d1[:, None, :] * d2[None, :, :]
            + P[:, 1, 1] * d2[None, :, :] ** 2
        )
        N = np.exp(-quad / 2) / (2 * np.pi * np.sqrt(det))  # (Bx, By, K)
        return N @ self.w

    def wigner4(self, x1, p1, x2, p2):
        """Evaluate the 4D mixture (full-cov Gaussians) on a broadcast grid."""
        X1, P1, X2, P2 = np.broadcast_arrays(x1, p1, x2, p2)
        pts = np.stack([X1, P1, X2, P2], axis=-1)        # (..., 4)
        Sigma = self.Sigma()
        out = np.zeros(X1.shape)
        for k in range(len(self.w)):
            d = pts - self.mu[k]
            prec = np.linalg.inv(Sigma[k])
            quad = np.einsum("...i,ij,...j->...", d, prec, d)
            out += (
                self.w[k]
                * np.exp(-quad / 2)
                / ((2 * np.pi) ** 2 * np.sqrt(np.linalg.det(Sigma[k])))
            )
        return out


def _gaussian_overlap4(mu, Sigma, c):
    """integral_{R^4} G(z; mu, Sigma) exp(-(z - c)^T (z - c)) dz, over K.

    The 4D generalization of forward2._gaussian_overlap (identical closed
    form, dimension 4). G is the normalized 4D Gaussian; c may be COMPLEX
    (the cat fringe is a Gaussian with imaginary mean). With P = Sigma^{-1},
    Q = P + 2I, b = P mu + 2c,

        overlap = exp( 1/2 b^T Q^{-1} b - 1/2 mu^T P mu - c^T c )
                  / sqrt(det(I + 2 Sigma)).

    mu: (K, 4) real, Sigma: (K, 4, 4) real, c: (4,) real or complex.
    Returns (K,) complex.
    """
    c = np.asarray(c, complex)
    P = np.linalg.inv(Sigma)                                    # (K, 4, 4)
    Q = P + 2 * np.eye(4)
    Qinv = np.linalg.inv(Q)
    b = np.einsum("kij,kj->ki", P, mu).astype(complex) + 2 * c  # (K, 4)
    term1 = 0.5 * np.einsum("ki,kij,kj->k", b, Qinv, b)
    const = -0.5 * np.einsum("ki,kij,kj->k", mu, P, mu)
    cc = c @ c
    detfac = np.sqrt(np.linalg.det(np.eye(4) + 2 * Sigma))      # (K,)
    return np.exp(term1 + const - cc) / detfac


def fidelity_vs_cat(mixture, alpha, parity=+1):
    """(2 pi)^2 * integral W_mix W_cat d^4z = tr(rho_mix rho_cat), closed form.

    The two-mode cat Wigner (states2) is, up to 1/(pi^2 norm), the sum of two
    coherent blobs exp(-|z - c_pp|^2), exp(-|z - c_mm|^2) and a fringe
    2 e^{-2 r2a^2} Re exp(-|z - c_f|^2) (= 2 e^{-4 a^2} Re ...) with
    c_pp = (r2a,0,r2a,0),
    c_mm = -c_pp, c_f = (0, i r2a, 0, i r2a), r2a = sqrt2 a (completing the
    square on exp(-|z|^2) cos(2 r2a (p1+p2))). The overlap of a splat
    N(mu, Sigma) with each such exp(-|z - c|^2) is _gaussian_overlap4, so

        fidelity = 4 / norm * sum_k w_k [ O_pp + O_mm
                                          + parity * 2 e^{-2 r2a^2} Re O_f ],

    the exact 4D generalization of forward2.fidelity_vs_cat ((2 pi)^2/pi^2 = 4).
    Validated in tests against brute-force 4D integration, the exact
    |<00|cat>|^2 vacuum value, and forward2 on a block-diagonal mixture.
    """
    a = float(alpha)
    r2a = np.sqrt(2) * a
    norm = 2 * (1 + parity * np.exp(-4 * a ** 2))

    mu = mixture.mu
    Sigma = mixture.Sigma()

    c_pp = np.array([r2a, 0.0, r2a, 0.0])
    c_mm = np.array([-r2a, 0.0, -r2a, 0.0])
    c_f = np.array([0.0, 1j * r2a, 0.0, 1j * r2a])

    O_pp = _gaussian_overlap4(mu, Sigma, c_pp).real
    O_mm = _gaussian_overlap4(mu, Sigma, c_mm).real
    O_f = _gaussian_overlap4(mu, Sigma, c_f)

    per_k = O_pp + O_mm + parity * 2.0 * np.exp(-2 * r2a ** 2) * O_f.real
    return float(4.0 / norm * np.sum(mixture.w * per_k))
