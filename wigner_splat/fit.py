"""v0 reconstructor: fit a signed splat mixture to binned homodyne data.

Loss = sum_theta L2(model marginal, histogram density)
     + lambda_neg * sum_theta mean(relu(-model)^2)   (marginals must be nonnegative)
     + lambda_sum * (sum_k w_k - 1)^2                (total probability)

The forward model (forward.radon) is a closed-form Gaussian projection, so
the loss gradient is closed-form too: for each angle theta with direction
u = (cos theta, sin theta), each splat contributes w_k N(x; m_k, var_k)
with m_k = mu_k . u and var_k = e^{2 s1} cos^2(phi - theta)
+ e^{2 s2} sin^2(phi - theta), and the chain rule through (m_k, var_k)
gives every parameter gradient in one vectorized pass per angle.

The mixture can also grow and shrink during the fit (fit(densify_every=...)):
adapt() prunes negligible-weight splats and splits splats with large
accumulated positional-gradient norm, and birth_field() places signed
newborn splats at the extremum of the weight-gradient field.
"""

import numpy as np

from .forward import SplatMixture
from .fock_project import psd_penalty, rho_component


def _pack(m):
    return np.concatenate([m.w, m.mu.ravel(), m.s.ravel(), m.phi])


def _unpack(v, K):
    w = v[:K]
    mu = v[K : 3 * K].reshape(K, 2)
    s = v[3 * K : 5 * K].reshape(K, 2)
    phi = v[5 * K :]
    return SplatMixture(w, mu, s, phi)


def histogram_targets(data, bins=80, x_max=None):
    """Bin homodyne samples per angle into density histograms."""
    x_max = x_max or max(np.abs(s).max() for _, s in data) * 1.05
    edges = np.linspace(-x_max, x_max, bins + 1)
    centers = (edges[:-1] + edges[1:]) / 2
    targets = []
    for theta, samples in data:
        hist, _ = np.histogram(samples, bins=edges, density=True)
        targets.append((theta, hist))
    return centers, targets


def loss(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0):
    total = 0.0
    for theta, hist in targets:
        model = mixture.radon(centers, theta)
        total += np.mean((model - hist) ** 2)
        total += lambda_neg * np.mean(np.minimum(model, 0.0) ** 2)
    total += lambda_sum * (mixture.w.sum() - 1.0) ** 2
    return total


def loss_and_grad(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0):
    """Loss and its analytic gradient w.r.t. (w, mu, s, phi).

    Returns (loss, grad) with grad packed in the same layout as _pack.

    Fully vectorized over the angle axis: the per-angle math of
    _loss_and_grad_looped is broadcast/einsum'd over (A, B, K) so the whole
    target set is one pass with no Python loop (fair timing vs the vectorized
    MLE baseline). See _loss_and_grad_looped for the annotated scalar version.
    """
    K = len(mixture.w)
    B = len(centers)
    # Stack the targets once per call (cheap next to the (A, B, K) math).
    theta = np.array([t for t, _ in targets])            # (A,)
    hist = np.array([h for _, h in targets])             # (A, B)

    u = np.stack([np.cos(theta), np.sin(theta)], axis=1)  # (A, 2)
    m = u @ mixture.mu.T                                  # (A, K) = mu_k . u
    dphi = mixture.phi[None, :] - theta[:, None]          # (A, K)
    c, s_ = np.cos(dphi), np.sin(dphi)                    # (A, K)
    e1, e2 = np.exp(2 * mixture.s[:, 0]), np.exp(2 * mixture.s[:, 1])  # (K,)
    var = e1 * c ** 2 + e2 * s_ ** 2                      # (A, K)
    d = centers[None, :, None] - m[:, None, :]            # (A, B, K)
    g = np.exp(-(d ** 2) / (2 * var[:, None, :])) / np.sqrt(
        2 * np.pi * var[:, None, :]
    )                                                     # (A, B, K)
    model = g @ mixture.w                                 # (A, B)
    resid = model - hist
    neg = np.minimum(model, 0.0)                          # mask broadcasts over (A, B)
    total = np.sum(np.mean(resid ** 2, axis=1)) + lambda_neg * np.sum(
        np.mean(neg ** 2, axis=1)
    )
    dL_dmodel = (2.0 / B) * (resid + lambda_neg * neg)    # (A, B)

    gw = np.einsum("ab,abk->k", dL_dmodel, g)             # (K,)
    # d model / d m_k = w_k g d / var; m_k = mu_k . u
    dL_dm = np.einsum("ab,abk->ak", dL_dmodel, g * d) * mixture.w / var  # (A, K)
    gmu = np.einsum("ak,ai->ki", dL_dm, u)               # (K, 2)
    # d g / d var = g (d^2 / (2 var^2) - 1 / (2 var))
    dvar_kernel = g * (d ** 2 / (2 * var[:, None, :] ** 2) - 1 / (2 * var[:, None, :]))
    dL_dvar = np.einsum("ab,abk->ak", dL_dmodel, dvar_kernel) * mixture.w  # (A, K)
    gs = np.empty((K, 2))
    gs[:, 0] = 2 * e1 * np.sum(dL_dvar * c ** 2, axis=0)
    gs[:, 1] = 2 * e2 * np.sum(dL_dvar * s_ ** 2, axis=0)
    gphi = np.sum(dL_dvar * (e2 - e1) * np.sin(2 * dphi), axis=0)  # (K,)

    wsum = mixture.w.sum() - 1.0
    total += lambda_sum * wsum ** 2
    gw += 2 * lambda_sum * wsum
    return total, np.concatenate([gw, gmu.ravel(), gs.ravel(), gphi])


def _loss_and_grad_looped(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0):
    """Reference (pre-vectorization) implementation, kept for equivalence tests."""
    K = len(mixture.w)
    gw = np.zeros(K)
    gmu = np.zeros((K, 2))
    gs = np.zeros((K, 2))
    gphi = np.zeros(K)
    total = 0.0
    B = len(centers)
    for theta, hist in targets:
        u = np.array([np.cos(theta), np.sin(theta)])
        m = mixture.mu @ u  # (K,)
        c, s_ = np.cos(mixture.phi - theta), np.sin(mixture.phi - theta)
        e1, e2 = np.exp(2 * mixture.s[:, 0]), np.exp(2 * mixture.s[:, 1])
        var = e1 * c ** 2 + e2 * s_ ** 2  # (K,)
        d = centers[:, None] - m  # (B, K)
        g = np.exp(-(d ** 2) / (2 * var)) / np.sqrt(2 * np.pi * var)  # (B, K)
        model = g @ mixture.w  # (B,)
        resid = model - hist
        neg = np.minimum(model, 0.0)
        total += np.mean(resid ** 2) + lambda_neg * np.mean(neg ** 2)
        dL_dmodel = (2.0 / B) * (resid + lambda_neg * neg)  # (B,)
        gw += dL_dmodel @ g
        # d model / d m_k = w_k g d / var; m_k = mu_k . u
        dL_dm = (dL_dmodel @ (g * d)) * mixture.w / var  # (K,)
        gmu += dL_dm[:, None] * u
        # d g / d var = g (d^2 / (2 var^2) - 1 / (2 var))
        dL_dvar = (dL_dmodel @ (g * (d ** 2 / (2 * var ** 2) - 1 / (2 * var)))) * mixture.w
        gs[:, 0] += dL_dvar * 2 * e1 * c ** 2
        gs[:, 1] += dL_dvar * 2 * e2 * s_ ** 2
        gphi += dL_dvar * (e2 - e1) * np.sin(2 * (mixture.phi - theta))
    wsum = mixture.w.sum() - 1.0
    total += lambda_sum * wsum ** 2
    gw += 2 * lambda_sum * wsum
    return total, np.concatenate([gw, gmu.ravel(), gs.ravel(), gphi])


def adapt(mixture, m1, m2, gnorm, K_max, prune_weight=5e-3, split_rel=2.0,
          split_factor=1.6, split_offset=0.6):
    """One densification/pruning step, 3DGS-style but driven by relative norms.

    Prunes splats with |w| < prune_weight. Splits splats whose accumulated
    positional gradient norm exceeds split_rel * median (absolute thresholds
    do not work here: near convergence all norms shrink together while their
    ratios keep pointing at under-resolved splats). A split replaces the
    parent with two children at half weight, offset by split_offset sigma
    along the major axis, with that axis shrunk by split_factor. Adam moment
    vectors (m1, m2, packed like _pack) follow the same row selection, and
    split children deliberately INHERIT the parent's moment rows unchanged
    as a warm start: zeroing them instead lets the near-empty second moment
    produce large uncontrolled steps right after the split (measured on the
    cat-state experiment: 2 of 5 seeds degrade from L2 ~ 0.07 to ~ 0.4).

    Returns (mixture, m1, m2).
    """
    K = len(mixture.w)
    keep = np.abs(mixture.w) >= prune_weight
    if not keep.any():
        keep[np.argmax(np.abs(mixture.w))] = True
    kept = np.flatnonzero(keep)
    budget = max(K_max - len(kept), 0)
    thresh = split_rel * np.median(gnorm[kept])
    by_norm = kept[np.argsort(-gnorm[kept])]
    split = set(k for k in by_norm[:budget] if gnorm[k] > thresh)

    parents, signs = [], []
    for k in kept:
        if k in split:
            parents += [k, k]
            signs += [-1.0, 1.0]
        else:
            parents.append(k)
            signs.append(0.0)
    parents, signs = np.array(parents), np.array(signs)

    def gather(m):
        return SplatMixture(m.w[parents], m.mu[parents], m.s[parents], m.phi[parents])

    new = gather(mixture)
    m1n, m2n = gather(_unpack(m1, K)), gather(_unpack(m2, K))
    child = signs != 0.0
    if child.any():
        rows = np.arange(len(parents))
        axis = np.argmax(new.s, axis=1)
        sigma = np.exp(new.s[rows, axis])
        c, s_ = np.cos(new.phi), np.sin(new.phi)
        # major principal axis in phase space: R(phi) e_axis
        direction = np.where(axis[:, None] == 0, np.stack([c, s_], 1), np.stack([-s_, c], 1))
        new.w[child] *= 0.5
        new.mu += (signs * split_offset * sigma)[:, None] * direction
        new.s[rows[child], axis[child]] -= np.log(split_factor)
    return new, _pack(m1n), _pack(m2n)


def _append_zero_splat(vec, K):
    """Append one all-zero splat row to a packed (moment) vector of size K."""
    m = _unpack(vec, K)
    return _pack(SplatMixture(
        np.append(m.w, 0.0),
        np.vstack([m.mu, np.zeros((1, 2))]),
        np.vstack([m.s, np.zeros((1, 2))]),
        np.append(m.phi, 0.0),
    ))


def birth_field(mixture, centers, targets, grid, s_probe=np.log(0.5),
                lambda_neg=10.0):
    """dL/dw for a probe splat at each phase-space grid point (G, 2).

    The weight gradient of a hypothetical new isotropic splat at mu is the
    residual back-projected through the splat kernel — closed form, like
    everything else here. Where it is large and positive the model needs
    NEGATIVE mass (and vice versa), so this field both places and signs
    newborn splats. Pure split/clone densification cannot do that: two
    positive children can never create the negative fringe of a cat state.
    """
    B = len(centers)
    field = np.zeros(len(grid))
    var = np.exp(2 * s_probe)
    for theta, hist in targets:
        u = np.array([np.cos(theta), np.sin(theta)])
        model = mixture.radon(centers, theta)
        dL_dmodel = (2.0 / B) * (
            (model - hist) + lambda_neg * np.minimum(model, 0.0)
        )
        m = grid @ u  # (G,)
        g = np.exp(-((centers[:, None] - m) ** 2) / (2 * var)) / np.sqrt(
            2 * np.pi * var
        )  # (B, G)
        field += dL_dmodel @ g
    return field


def fit(data, K=8, iters=800, lr=0.05, seed=0, bins=80, callback=None,
        densify_every=None, K_max=None, densify_until=None, prune_weight=5e-3,
        birth_weight=0.05, birth_grid=40):
    """Adam on the analytic loss gradient. Returns the fitted mixture.

    With densify_every set, every densify_every iterations (up to
    densify_until, default 0.6 * iters):
    - adapt() prunes negligible-|w| splats and splits splats with large
      accumulated positional gradient norm (relative to the median);
    - if capacity remains, one splat is born at the extremum of the
      weight-gradient field (birth_field), with the descent sign — this is
      what lets negativity emerge when no splat has a negative weight yet.
    K grows up to K_max (default 2 * K).
    """
    centers, targets = histogram_targets(data, bins=bins)
    mix = SplatMixture.random_init(K, rng=seed)
    v = _pack(mix)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    if densify_until is None:
        densify_until = int(0.6 * iters)
    if K_max is None:
        K_max = 2 * K
    xg = np.linspace(centers[0], centers[-1], birth_grid)
    grid = np.stack(np.meshgrid(xg, xg), axis=-1).reshape(-1, 2)
    gnorm = np.zeros(K)
    for t in range(1, iters + 1):
        cur, grad = loss_and_grad(_unpack(v, K), centers, targets)
        gnorm += np.linalg.norm(grad[K : 3 * K].reshape(K, 2), axis=1)
        m1 = 0.9 * m1 + 0.1 * grad
        m2 = 0.999 * m2 + 0.001 * grad ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if densify_every and t % densify_every == 0 and t <= densify_until:
            mix_t, m1, m2 = adapt(
                _unpack(v, K), m1, m2, gnorm / densify_every,
                K_max=K_max, prune_weight=prune_weight,
            )
            if len(mix_t.w) < K_max:
                field = birth_field(mix_t, centers, targets, grid)
                i = np.argmax(np.abs(field))
                mix_t = SplatMixture(
                    np.append(mix_t.w, -np.sign(field[i]) * birth_weight),
                    np.vstack([mix_t.mu, grid[i]]),
                    np.vstack([mix_t.s, np.full(2, np.log(0.5))]),
                    np.append(mix_t.phi, 0.0),
                )
                m1 = _append_zero_splat(m1, len(mix_t.w) - 1)
                m2 = _append_zero_splat(m2, len(mix_t.w) - 1)
            K = len(mix_t.w)
            v = _pack(mix_t)
            gnorm = np.zeros(K)
        if callback and t % 100 == 0:
            callback(t, loss(_unpack(v, K), centers, targets))
    return _unpack(v, K)


def _pack_splat_index(i, K):
    """Splat index k that packed-vector entry i belongs to (see _pack's
    layout: w (K,), mu.ravel() (2K,), s.ravel() (2K,), phi (K,))."""
    if i < K:
        return i
    if i < 3 * K:
        return (i - K) // 2
    if i < 5 * K:
        return (i - 3 * K) // 2
    return i - 5 * K


def _psd_penalty_grad_fd(v, K, n_max, eps=1e-4):
    """Central-difference gradient of fock_project.psd_penalty(rho_from_splat)
    w.r.t. the packed parameter vector v.

    Perturbing packed index i changes exactly ONE splat's (w_k, mu_k, Sigma_k)
    (see _pack_splat_index), so rho only needs its k-th term rebuilt per
    perturbation, not the whole K-term sum: cache all K components once, then
    for each index re-add just fock_project.rho_component(., k, n_max) on top
    of the cached sum of the OTHER K-1 components. This turns an O(K) rho
    rebuild per finite-difference evaluation into O(1) -- see the module-level
    docstring of fock_project.rho_component for why that matters (K rho
    rebuilds already cost tens of seconds at the three-mode n_max=8 cutoff).
    """
    mix = _unpack(v, K)
    comps = [rho_component(mix, k, n_max) for k in range(K)]
    total = sum(comps)

    g = np.zeros_like(v)
    for i in range(len(v)):
        k = _pack_splat_index(i, K)
        rest = total - comps[k]

        vp = v.copy()
        vp[i] += eps
        pen_p = psd_penalty(rest + rho_component(_unpack(vp, K), k, n_max))

        vm = v.copy()
        vm[i] -= eps
        pen_m = psd_penalty(rest + rho_component(_unpack(vm, K), k, n_max))

        g[i] = (pen_p - pen_m) / (2 * eps)
    return g


def fit_psd(data, lambda_psd=1.0, n_max_psd=28, psd_polish_iters=200,
            psd_polish_lr=0.01, psd_grad_eps=1e-4, lambda_neg=10.0,
            lambda_sum=1.0, bins=80, **fit_kwargs):
    """fit() followed by a PSD-polish stage (issue #8): extra Adam iterations
    on (original histogram loss) + lambda_psd * fock_project.psd_penalty(
    rho_from_splat(mixture, n_max_psd)), the latter's gradient by finite
    differences (see _psd_penalty_grad_fd) since fock_project has no analytic
    drho/dtheta.

    fit()'s own recipe (init/densify/histogram-loss) is untouched -- this
    function calls it unmodified and ADDS a second stage on its output, so
    fit()'s existing behavior and callers are unaffected (no regression).

    lambda_psd=0 or psd_polish_iters=0 returns fit()'s output unchanged (the
    polish stage is purely additive, never re-runs or re-weights the first).

    n_max_psd defaults to 28: experiments/08_positivity/diagnose_1mode.py's
    fitted-cat splat's rho eigenvalues are converged by n_max~28 (see that
    module and tests/test_fock_project.py).

    See experiments/08_positivity/penalty_sweep_1mode.py for the fidelity-vs-
    min_eig sweep this was built to measure (issue #8's falsification test).
    """
    mix = fit(data, bins=bins, **fit_kwargs)
    if psd_polish_iters == 0 or lambda_psd == 0.0:
        return mix

    centers, targets = histogram_targets(data, bins=bins)
    K = len(mix.w)
    v = _pack(mix)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, psd_polish_iters + 1):
        _, g_loss = loss_and_grad(_unpack(v, K), centers, targets,
                                   lambda_neg=lambda_neg, lambda_sum=lambda_sum)
        g_psd = _psd_penalty_grad_fd(v, K, n_max_psd, psd_grad_eps)
        g = g_loss + lambda_psd * g_psd
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        step = psd_polish_lr * (m1 / (1 - 0.9 ** t)) / (
            np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8
        )
        v = v - step
    return _unpack(v, K)
