"""Multimode rho=BB^dagger reconstructor (coherent-product kets), issue #8.

The multimode lift of bbdag.py, specialized to COHERENT product kets (no
squeeze) -- the minimal ansatz that can represent the entangled three-mode cat,
which is exactly a rank-2 superposition of two product coherent states
|a,a,a> + parity|-a,-a,-a> (see states3.ThreeModeCat.homodyne_pdf). Squeeze is a
strict generalization added later if this is not enough.

Ansatz (M modes):

    |psi> = sum_c z_c  prod_m |alpha_c^m>,      |alpha_c^m> coherent

    p_theta(x) = |psi_theta(x)|^2 / Z,    Z = <psi|psi>

with psi_theta(x) = sum_c z_c prod_m <x_m | alpha_c^m e^{-i theta_m}> and every
quantity closed-form: the coherent overlap <alpha|beta> =
exp(-|alpha|^2/2 - |beta|^2/2 + conj(alpha) beta) gives Z and the state fidelity
against any coherent-superposition target WITHOUT a phase-space grid. Physicality
is automatic (rho = |psi><psi|/Z is rank-1 PSD).

Loss is the per-sample NLL (no binning): the marginal is |.|^2/Z >= 0 and
normalized by construction, so unlike forward3f there is no nonnegativity or
sum penalty to add.
"""

import numpy as np

from .states import coherent_wavefunction


def coherent_overlap(a, b):
    """<a|b> = exp(-|a|^2/2 - |b|^2/2 + conj(a) b), elementwise on complex arrays."""
    return np.exp(-0.5 * np.abs(a) ** 2 - 0.5 * np.abs(b) ** 2 + np.conj(a) * b)


class CoherentKetState:
    """|psi> = sum_c z_c prod_m |alpha[c, m]>, M-mode coherent-product superposition.

    z: (K,) complex amplitudes. alpha: (K, M) complex per-mode displacements.
    """

    def __init__(self, z, alpha):
        self.z = np.asarray(z, complex)
        self.alpha = np.asarray(alpha, complex)  # (K, M)

    @property
    def K(self):
        return len(self.z)

    @property
    def M(self):
        return self.alpha.shape[1]

    @classmethod
    def random_init(cls, K, M, scale=1.5, rng=None):
        rng = np.random.default_rng(rng)
        a = rng.uniform(-scale, scale, (K, M)) + 1j * rng.uniform(-scale, scale, (K, M))
        return cls(z=np.ones(K, complex) / np.sqrt(K), alpha=a)

    def norm_sq(self):
        """Z = <psi|psi> = sum_{c,d} conj(z_c) z_d prod_m <alpha_c^m|alpha_d^m>."""
        # G[c, d] = prod_m <alpha[c,m]|alpha[d,m]>
        ov = coherent_overlap(self.alpha[:, None, :], self.alpha[None, :, :])  # (K,K,M)
        G = np.prod(ov, axis=2)  # (K, K)
        return np.real(np.conj(self.z) @ G @ self.z)

    def psi_at(self, X, theta):
        """psi_theta(X) for samples X (S, M) at LO phases theta (M,).

        Returns (S,) complex amplitude sum_c z_c prod_m <x_m|alpha_c^m e^{-i theta_m}>.
        """
        rot = self.alpha * np.exp(-1j * np.asarray(theta))[None, :]  # (K, M)
        # f[s, c, m] = <X[s,m] | rot[c,m]>
        S = X.shape[0]
        prod = np.ones((S, self.K), complex)
        for m in range(self.M):
            # coherent_wavefunction broadcasts (S,1) x (1,K) -> (S,K)
            fm = coherent_wavefunction(X[:, m][:, None], rot[None, :, m])
            prod *= fm
        return prod @ self.z  # (S,)

    def overlap_with(self, kets_z, kets_alpha):
        """<psi | phi> for phi = sum_j kets_z[j] prod_m |kets_alpha[j, m]>.

        Closed form via coherent overlaps; used for exact state fidelity.
        """
        ka = np.asarray(kets_alpha, complex)  # (J, M)
        kz = np.asarray(kets_z, complex)      # (J,)
        ov = coherent_overlap(self.alpha[:, None, :], ka[None, :, :])  # (K, J, M)
        G = np.prod(ov, axis=2)  # (K, J)
        return np.conj(self.z) @ G @ kz


def _pack(state):
    return np.concatenate([
        np.real(state.z), np.imag(state.z),
        np.real(state.alpha).ravel(), np.imag(state.alpha).ravel(),
    ])


def _unpack(v, K, M):
    z = v[0:K] + 1j * v[K:2 * K]
    ar = v[2 * K:2 * K + K * M].reshape(K, M)
    ai = v[2 * K + K * M:2 * K + 2 * K * M].reshape(K, M)
    return CoherentKetState(z=z, alpha=ar + 1j * ai)


def nll(state, data):
    """Mean per-sample negative log likelihood over all angle triples."""
    Z = state.norm_sq()
    tot = 0.0
    n = 0
    for theta, X in data:
        p = np.abs(state.psi_at(X, theta)) ** 2 / Z
        tot += -np.sum(np.log(np.maximum(p, 1e-300)))
        n += len(X)
    return tot / n


def _nll_grad_fd(v, K, M, data, eps=1e-5):
    g = np.zeros_like(v)
    for i in range(len(v)):
        vp = v.copy(); vp[i] += eps
        vm = v.copy(); vm[i] -= eps
        g[i] = (nll(_unpack(vp, K, M), data) - nll(_unpack(vm, K, M), data)) / (2 * eps)
    return g


def fit_bbdagM(data, K=8, M=3, iters=200, lr=0.05, seed=0, callback=None,
               grad_eps=1e-5):
    """Adam on the FD NLL gradient. Returns a physical CoherentKetState."""
    state = CoherentKetState.random_init(K, M, rng=seed)
    v = _pack(state)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        g = _nll_grad_fd(v, K, M, data, eps=grad_eps)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 25 == 0:
            callback(t, nll(_unpack(v, K, M), data))
    return _unpack(v, K, M)


def fidelity_vs_cat3(state, alpha, parity=+1):
    """Exact state fidelity F = |<psi|cat3>|^2 for cat3 = |a,a,a>+parity|-a,-a,-a>.

    cat3 is a 2-ket coherent superposition, so this is closed form (no grid).
    """
    M = state.M
    a = float(alpha)
    kets_alpha = np.array([[a] * M, [-a] * M], complex)  # (2, M)
    kets_z = np.array([1.0, parity], complex)
    ov = state.overlap_with(kets_z, kets_alpha)
    Z = state.norm_sq()
    # <cat3|cat3> = sum_{i,j} z_i* z_j prod_m <ket_i^m|ket_j^m>
    g = coherent_overlap(kets_alpha[:, None, :], kets_alpha[None, :, :])
    Gt = np.prod(g, axis=2)
    Ncat = np.real(np.conj(kets_z) @ Gt @ kets_z)
    return np.abs(ov) ** 2 / (Z * Ncat)
