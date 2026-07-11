"""rho = B B^dagger reconstructor: fit a CONSTRUCTIVELY PHYSICAL state to
homodyne data (issue #8).

Motivation (issue #8): a signed Gaussian splat mixture is not guaranteed to
correspond to a positive-semidefinite density operator, so its fitted "Wigner"
can be unphysical (min eigenvalue < 0). forward.py places signed Gaussians in
phase space directly; here we instead build a STATE and derive its homodyne
marginals, so physicality is automatic.

For a PURE target we use a rank-1 ansatz (single-column B):

    |psi> = sum_c z_c |g_c>,   |g_c> = D(alpha_c) S(xi_c) |0>

a superposition of displaced squeezed vacua. Because coherent states are
overcomplete, enough such kets represent any pure state (oracle-confirmed;
displaced-squeezed includes coherent at xi=0). The homodyne marginal is

    p_theta(x) = |psi_theta(x)|^2 / Z,   Z = <psi|psi>

with psi_theta the position wavefunction after rotating the local oscillator by
theta (alpha -> alpha e^{-i theta}, xi -> xi e^{-2 i theta}). Two consequences
vs forward.SplatMixture:
  * p_theta(x) = |.|^2 >= 0 by construction  -> no lambda_neg penalty needed;
  * dividing by Z normalizes the marginal    -> no lambda_sum constraint needed.
Physicality (rho = |psi><psi|/Z is rank-1 PSD, min_eig = 0) comes for free.

The prototype evaluates Z by finite-grid quadrature rather than a closed-form
overlap. Normalization is therefore approximate. norm_sq() rejects malformed
grids, invalid Z, and material density remaining at the grid boundaries. This
boundary diagnostic catches ordinary tail truncation without another integral,
but is not a formal convergence proof.

Single-mode only for now (prototype). Multimode is the follow-up.

Wavefunction convention (states.py / fock.py): dimensionless quadratures,
vacuum marginal N(0, 1/2), <x|0> = pi^{-1/4} exp(-x^2/2), coherent |alpha> at
(x, p) = sqrt(2) (Re alpha, Im alpha). The displaced-squeezed wavefunction
below reduces to states.coherent_wavefunction at xi = 0 (checked in tests).
"""

import numpy as np


def sq_coherent_wavefunction(x, alpha, xi):
    """<x | D(alpha) S(xi) |0>, displaced squeezed vacuum position wavefunction.

    alpha (complex) is the displacement; xi = r e^{i phi} (complex) the squeeze.
    Closed form (vacuum-variance-1/2 convention):

        f(x) = pi^{-1/4} (mu - nu)^{-1/2}
               * exp[ -(q/2)(x - x0)^2 + i p0 x - i Re(alpha) Im(alpha) ]

    with mu = cosh r, nu = e^{i phi} sinh r, q = (mu + nu)/(mu - nu),
    x0 = sqrt(2) Re(alpha), p0 = sqrt(2) Im(alpha). At xi = 0 (mu = 1, nu = 0,
    q = 1) this is exactly states.coherent_wavefunction. For phi = 0, r > 0 the
    position variance of |f|^2 is e^{-2r}/2 (x-squeezed).
    """
    r = np.abs(xi)
    phi = np.angle(xi)
    mu = np.cosh(r)
    nu = np.exp(1j * phi) * np.sinh(r)
    q = (mu + nu) / (mu - nu)
    ar, ai = np.real(alpha), np.imag(alpha)
    x0 = np.sqrt(2) * ar
    p0 = np.sqrt(2) * ai
    pref = np.pi ** -0.25 * (mu - nu) ** -0.5
    return pref * np.exp(-(q / 2) * (x - x0) ** 2 + 1j * p0 * x - 1j * ar * ai)


def _validated_norm(Z):
    """Return scalar Z after rejecting invalid normalization factors."""
    value = np.asarray(Z)
    if value.ndim != 0 or not np.isrealobj(value):
        raise ValueError("state norm Z must be a real scalar")
    value = float(value)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"state norm Z must be finite and strictly positive, got {value!r}")
    return value


class PureKetState:
    """Pure state |psi> = sum_c z_c D(alpha_c) S(xi_c) |0> (single mode).

    z, alpha, xi are complex (K,) arrays. All observables are derived from the
    position wavefunction, so the represented density operator rho = |psi><psi|
    is physical by construction. Numerical marginal normalization uses the
    finite-grid quadrature returned by norm_sq().
    """

    def __init__(self, z, alpha, xi):
        self.z = np.asarray(z, complex)
        self.alpha = np.asarray(alpha, complex)
        self.xi = np.asarray(xi, complex)

    @classmethod
    def random_init(cls, K, scale=1.5, rng=None):
        rng = np.random.default_rng(rng)
        a = rng.uniform(-scale, scale, K) + 1j * rng.uniform(-scale, scale, K)
        return cls(
            z=np.ones(K, complex) / np.sqrt(K),
            alpha=a,
            xi=np.zeros(K, complex),  # start unsqueezed (coherent kets)
        )

    def psi(self, x, theta=0.0):
        """psi_theta(x) = sum_c z_c <x | D(alpha_c e^{-i theta}) S(xi_c e^{-2 i theta}) |0>."""
        x = np.atleast_1d(x)
        a = self.alpha * np.exp(-1j * theta)
        xr = self.xi * np.exp(-2j * theta)
        out = np.zeros(x.shape, complex)
        for c in range(len(self.z)):
            out += self.z[c] * sq_coherent_wavefunction(x, a[c], xr[c])
        return out

    def norm_sq(self, grid=None, tail_rtol=1e-8):
        """Finite-grid trapezoidal estimate of the theta-independent norm Z.

        The default grid is [-12, 12]. A dimensionless boundary-density
        indicator rejects grids whose wavefunction tails have not decayed.
        """
        if grid is None:
            grid = np.linspace(-12.0, 12.0, 2048)
        grid = np.asarray(grid)
        if grid.ndim != 1 or grid.size < 3 or not np.isrealobj(grid):
            raise ValueError("norm grid must be a one-dimensional real array with >= 3 points")
        grid = grid.astype(float, copy=False)
        if not np.all(np.isfinite(grid)) or not np.all(np.diff(grid) > 0.0):
            raise ValueError("norm grid must contain finite, strictly increasing points")
        if not np.isfinite(tail_rtol) or tail_rtol <= 0.0:
            raise ValueError("tail_rtol must be finite and strictly positive")

        psi = self.psi(grid, 0.0)
        density = np.abs(psi) ** 2
        Z = _validated_norm(np.trapezoid(density, grid))

        # Inspect a small boundary window so an accidental zero at one endpoint
        # cannot hide a still-rising tail. No expanded-grid reintegration.
        edge_count = min(8, max(2, grid.size // 100))
        edge_density = float(max(
            np.max(density[:edge_count]),
            np.max(density[-edge_count:]),
        ))
        tail_indicator = edge_density * float(grid[-1] - grid[0]) / Z
        if not np.isfinite(tail_indicator) or tail_indicator > tail_rtol:
            raise ValueError(
                "norm grid appears to truncate wavefunction tails: "
                f"boundary indicator {tail_indicator:.3e} > {tail_rtol:.3e}"
            )
        return Z

    def radon(self, x, theta, Z=None):
        """Homodyne marginal normalized by a validated finite-grid estimate Z."""
        if Z is None:
            Z = self.norm_sq()
        Z = _validated_norm(Z)
        return np.abs(self.psi(x, theta)) ** 2 / Z


def _pack(state):
    return np.concatenate([
        np.real(state.z), np.imag(state.z),
        np.real(state.alpha), np.imag(state.alpha),
        np.real(state.xi), np.imag(state.xi),
    ])


def _unpack(v, K):
    return PureKetState(
        z=v[0:K] + 1j * v[K:2 * K],
        alpha=v[2 * K:3 * K] + 1j * v[3 * K:4 * K],
        xi=v[4 * K:5 * K] + 1j * v[5 * K:6 * K],
    )


def loss(state, centers, targets, norm_grid=None):
    """L2 histogram match. No nonnegativity/sum penalty: |psi|^2/Z handles both."""
    Z = _validated_norm(state.norm_sq(norm_grid))
    total = 0.0
    for theta, hist in targets:
        model = state.radon(centers, theta, Z=Z)
        total += np.mean((model - hist) ** 2)
    return total


def _loss_grad_fd(v, K, centers, targets, norm_grid, eps=1e-5):
    """Central-difference gradient of loss w.r.t. packed real params."""
    g = np.zeros_like(v)
    for i in range(len(v)):
        vp = v.copy(); vp[i] += eps
        vm = v.copy(); vm[i] -= eps
        lp = loss(_unpack(vp, K), centers, targets, norm_grid)
        lm = loss(_unpack(vm, K), centers, targets, norm_grid)
        g[i] = (lp - lm) / (2 * eps)
    return g


def fit_bbdag(data, K=4, iters=400, lr=0.05, seed=0, bins=80, callback=None,
              grad_eps=1e-5):
    """Adam on the FD loss gradient. Returns a physical PureKetState.

    Deliberately simpler than forward-model fit(): no densify/prune/birth and no
    penalties -- the ansatz is physical by construction, and for the pure
    prototype a fixed K of displaced-squeezed kets is enough. FD gradient (6K
    params) matches the repo's fit_psd style; analytic gradients are a later
    optimization if the prototype gate passes.
    """
    from .fit import histogram_targets
    centers, targets = histogram_targets(data, bins=bins)
    x_max = centers[-1] + 4.0
    norm_grid = np.linspace(-x_max, x_max, 2048)

    state = PureKetState.random_init(K, rng=seed)
    v = _pack(state)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        g = _loss_grad_fd(v, K, centers, targets, norm_grid, eps=grad_eps)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 50 == 0:
            callback(t, loss(_unpack(v, K), centers, targets, norm_grid))
    return _unpack(v, K)


def fidelity_vs_pure(state, psi_target_fn, grid=None):
    """State fidelity F = |<psi_fit|psi_target>|^2, both as position wavefunctions.

    psi_target_fn(x) returns the (unnormalized) target position wavefunction at
    theta = 0. Everything is a 1D numeric x-integral, so no Fock truncation.
    """
    if grid is None:
        grid = np.linspace(-14.0, 14.0, 4096)
    pf = state.psi(grid, 0.0)
    pt = np.asarray(psi_target_fn(grid), complex)
    ov = np.trapezoid(np.conj(pf) * pt, grid)
    nf = np.trapezoid(np.abs(pf) ** 2, grid)
    nt = np.trapezoid(np.abs(pt) ** 2, grid)
    return np.abs(ov) ** 2 / (nf * nt)
