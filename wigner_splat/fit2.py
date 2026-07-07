"""Two-mode reconstructor: fit a separable signed splat mixture to binned
joint homodyne data. Mirrors fit.py with per-mode bookkeeping.

Loss = sum_{th1,th2} L2(model grid, 2D histogram density)
     + lambda_neg * sum mean(relu(-model)^2)   (joint marginals nonnegative)
     + lambda_sum * (sum_k w_k - 1)^2           (total probability)

The forward model (forward2.radon2) is a product of two closed-form Gaussian
projections, so the loss gradient is closed-form and fully vectorized over
angle pairs: for each pair the joint kernel g1_{p,i,k} g2_{p,j,k} contracts
against the per-cell residual, and mode-1 / mode-2 parameters see the SAME
1D chain rule as fit.py, with the OTHER mode's kernel contracted into the
effective residual. adapt2 / birth lift from fit.py: split by relative-median
4D positional gradient norm along the dominant mode's major axis, born splats
placed at the extremum of the weight-gradient field on a coarse 4D candidate
grid with the descent sign (so negativity can emerge from positive weights).
"""

import numpy as np

from .data2 import histogram_targets2
from .forward2 import SplatMixture2


def _pack2(m):
    return np.concatenate([m.w, m.mu.ravel(), m.s.ravel(), m.phi.ravel()])


def _unpack2(v, K):
    w = v[:K]
    mu = v[K : 5 * K].reshape(K, 4)
    s = v[5 * K : 9 * K].reshape(K, 2, 2)
    phi = v[9 * K : 11 * K].reshape(K, 2)
    return SplatMixture2(w, mu, s, phi)


def loss2(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0):
    total = 0.0
    for (th1, th2), hist in targets:
        model = mixture.radon2(centers, centers, th1, th2)
        total += np.mean((model - hist) ** 2)
        total += lambda_neg * np.mean(np.minimum(model, 0.0) ** 2)
    total += lambda_sum * (mixture.w.sum() - 1.0) ** 2
    return total


def loss_and_grad2(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0):
    """Loss and its analytic gradient, packed like _pack2, vectorized over pairs.

    Builds the (P, B, K) per-mode kernels once and contracts them. The full
    (P, B, B, K) tensor is never materialized: model and residual live on
    (P, B, B), and each mode's gradient uses the other mode's kernel folded
    into the effective residual S (P, B, K).
    """
    K = len(mixture.w)
    B = len(centers)
    w = mixture.w

    th = np.array([a for a, _ in targets])                # (P, 2)
    hist = np.array([h for _, h in targets])              # (P, B, B)
    th1, th2 = th[:, 0], th[:, 1]
    P = len(th)

    # per-mode projected moments, (P, K)
    u1 = np.stack([np.cos(th1), np.sin(th1)], axis=1)     # (P, 2)
    u2 = np.stack([np.cos(th2), np.sin(th2)], axis=1)
    m1 = u1 @ mixture.mu[:, 0:2].T                        # (P, K)
    m2 = u2 @ mixture.mu[:, 2:4].T
    dphi1 = mixture.phi[None, :, 0] - th1[:, None]        # (P, K)
    dphi2 = mixture.phi[None, :, 1] - th2[:, None]
    c1, s1 = np.cos(dphi1), np.sin(dphi1)
    c2, s2 = np.cos(dphi2), np.sin(dphi2)
    e1a, e1b = np.exp(2 * mixture.s[:, 0, 0]), np.exp(2 * mixture.s[:, 0, 1])  # (K,)
    e2a, e2b = np.exp(2 * mixture.s[:, 1, 0]), np.exp(2 * mixture.s[:, 1, 1])
    var1 = e1a * c1 ** 2 + e1b * s1 ** 2                  # (P, K)
    var2 = e2a * c2 ** 2 + e2b * s2 ** 2

    d1 = centers[None, :, None] - m1[:, None, :]          # (P, B, K)
    d2 = centers[None, :, None] - m2[:, None, :]
    g1 = np.exp(-(d1 ** 2) / (2 * var1[:, None, :])) / np.sqrt(2 * np.pi * var1[:, None, :])
    g2 = np.exp(-(d2 ** 2) / (2 * var2[:, None, :])) / np.sqrt(2 * np.pi * var2[:, None, :])

    model = np.einsum("pik,pjk->pij", g1 * w, g2)         # (P, B, B)
    resid = model - hist
    neg = np.minimum(model, 0.0)
    total = np.sum(np.mean(resid ** 2, axis=(1, 2))) + lambda_neg * np.sum(
        np.mean(neg ** 2, axis=(1, 2))
    )
    D = (2.0 / (B * B)) * (resid + lambda_neg * neg)      # (P, B, B) = dL/dmodel

    # effective residuals: fold the other mode's kernel into D
    S2 = np.einsum("pij,pjk->pik", D, g2)                 # (P, B, K), for mode-1 params
    S1 = np.einsum("pij,pik->pjk", D, g1)                 # (P, B, K), for mode-2 params

    # weight gradient: dmodel/dw = g1 g2 -> sum D g1 g2
    gw = np.einsum("pik,pik->k", g1, S2)

    def mode_grads(S, g, d, var, c, s, ea, eb, dphi, ucos, usin):
        eff = w * S                                       # (P, B, K) = dL/dg
        dL_dm = np.sum(eff * g * d, axis=1) / var         # (P, K)
        gmux = np.einsum("pk,p->k", dL_dm, ucos)          # (K,)
        gmup = np.einsum("pk,p->k", dL_dm, usin)
        dvar_kernel = g * (d ** 2 / (2 * var[:, None, :] ** 2) - 1 / (2 * var[:, None, :]))
        dL_dvar = np.sum(eff * dvar_kernel, axis=1)       # (P, K)
        gsa = 2 * ea * np.sum(dL_dvar * c ** 2, axis=0)   # (K,)
        gsb = 2 * eb * np.sum(dL_dvar * s ** 2, axis=0)
        gphi = np.sum(dL_dvar * (eb - ea) * np.sin(2 * dphi), axis=0)
        return gmux, gmup, gsa, gsb, gphi

    g1mux, g1mup, g1sa, g1sb, g1phi = mode_grads(
        S2, g1, d1, var1, c1, s1, e1a, e1b, dphi1, np.cos(th1), np.sin(th1)
    )
    g2mux, g2mup, g2sa, g2sb, g2phi = mode_grads(
        S1, g2, d2, var2, c2, s2, e2a, e2b, dphi2, np.cos(th2), np.sin(th2)
    )

    gmu = np.stack([g1mux, g1mup, g2mux, g2mup], axis=1)  # (K, 4)
    gs = np.stack(
        [np.stack([g1sa, g1sb], axis=1), np.stack([g2sa, g2sb], axis=1)], axis=1
    )                                                     # (K, 2, 2)
    gphi = np.stack([g1phi, g2phi], axis=1)               # (K, 2)

    wsum = w.sum() - 1.0
    total += lambda_sum * wsum ** 2
    gw = gw + 2 * lambda_sum * wsum
    return total, np.concatenate([gw, gmu.ravel(), gs.ravel(), gphi.ravel()])


def adapt2(mixture, m1, m2, gnorm, K_max, prune_weight=5e-3, split_rel=2.0,
           split_factor=1.6, split_offset=0.6):
    """One densification/pruning step (fit.adapt lifted to two modes).

    Prunes |w| < prune_weight. Splits splats whose accumulated 4D positional
    gradient norm exceeds split_rel * median. A split replaces the parent with
    two half-weight children, offset by split_offset sigma along the major
    principal axis of the splat's DOMINANT mode (the (mode, axis) with the
    largest log-std s), in that mode's 2D phase-space plane, with that axis
    shrunk by split_factor. Adam moment rows follow the same selection and the
    children INHERIT the parent's moments unchanged (warm start), exactly the
    policy documented in fit.adapt. Returns (mixture, m1, m2).
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
        return SplatMixture2(m.w[parents], m.mu[parents], m.s[parents], m.phi[parents])

    new = gather(mixture)
    m1n, m2n = gather(_unpack2(m1, K)), gather(_unpack2(m2, K))
    child = signs != 0.0
    if child.any():
        rows = np.arange(len(parents))
        # dominant (mode, axis) = argmax over the 4 flattened log-stds
        flat = new.s.reshape(len(parents), 4)
        dom = np.argmax(flat, axis=1)
        mode = dom // 2                                    # 0 or 1
        axis = dom % 2                                     # 0 or 1
        sigma = np.exp(flat[rows, dom])
        # major principal axis in that mode's plane: R(phi_mode) e_axis
        phi_mode = new.phi[rows, mode]
        cph, sph = np.cos(phi_mode), np.sin(phi_mode)
        direction = np.where(
            axis[:, None] == 0, np.stack([cph, sph], 1), np.stack([-sph, cph], 1)
        )                                                  # (n, 2)
        new.w[child] *= 0.5
        # offset the two mu components of the dominant mode
        offset = (signs * split_offset * sigma)[:, None] * direction  # (n, 2)
        col0 = 2 * mode                                    # x-component index in mu
        new.mu[rows, col0] += offset[:, 0]
        new.mu[rows, col0 + 1] += offset[:, 1]
        new.s[rows[child], mode[child], axis[child]] -= np.log(split_factor)
    return new, _pack2(m1n), _pack2(m2n)


def _append_zero_splat2(vec, K):
    """Append one all-zero splat row to a packed (moment) vector of size K."""
    m = _unpack2(vec, K)
    return _pack2(SplatMixture2(
        np.append(m.w, 0.0),
        np.vstack([m.mu, np.zeros((1, 4))]),
        np.concatenate([m.s, np.zeros((1, 2, 2))], axis=0),
        np.vstack([m.phi, np.zeros((1, 2))]),
    ))


def _birth_batch(field, candidates, n_birth, spread):
    """Pick up to n_birth candidate indices at |field| maxima, greedily
    suppressing a radius `spread` around each pick so a batch spreads across
    the fringe instead of piling onto one extremum. Returns the index list."""
    fa = np.abs(field).copy()
    chosen = []
    for _ in range(n_birth):
        j = int(np.argmax(fa))
        if fa[j] <= 0.0:
            break
        chosen.append(j)
        fa[np.linalg.norm(candidates - candidates[j], axis=1) < spread] = 0.0
    return chosen


def birth_field2(mixture, centers, targets, candidates, s_probe=np.log(0.5),
                 lambda_neg=10.0, chunk=1024):
    """dL/dw for an isotropic separable probe splat at each 4D candidate.

    candidates: (G, 4) as (x1, p1, x2, p2). The probe has per-mode isotropic
    covariance var = exp(2 s_probe) I, so its projected variance is that value
    at every angle. The weight gradient is the current residual back-projected
    through the probe's product kernel, closed form. Where it is large and
    positive the model needs NEGATIVE mass (and vice versa), so the field both
    places and signs newborn splats -- pure splitting could never build the
    cat's negative fringe. Candidates chunked to bound memory. Returns (G,).
    """
    B = len(centers)
    var = np.exp(2 * s_probe)
    field = np.zeros(len(candidates))
    # precompute per-pair dL/dmodel once
    Ds = []
    for (th1, th2), hist in targets:
        model = mixture.radon2(centers, centers, th1, th2)
        D = (2.0 / (B * B)) * ((model - hist) + lambda_neg * np.minimum(model, 0.0))
        Ds.append((th1, th2, D))
    for lo in range(0, len(candidates), chunk):
        cand = candidates[lo : lo + chunk]                # (g, 4)
        acc = np.zeros(len(cand))
        for th1, th2, D in Ds:
            mp1 = cand[:, 0] * np.cos(th1) + cand[:, 1] * np.sin(th1)  # (g,)
            mp2 = cand[:, 2] * np.cos(th2) + cand[:, 3] * np.sin(th2)
            gp1 = np.exp(-((centers[None, :] - mp1[:, None]) ** 2) / (2 * var)) / np.sqrt(
                2 * np.pi * var
            )                                             # (g, B)
            gp2 = np.exp(-((centers[None, :] - mp2[:, None]) ** 2) / (2 * var)) / np.sqrt(
                2 * np.pi * var
            )
            # sum_{i,j} D[i,j] gp1[g,i] gp2[g,j]
            acc += np.einsum("gi,ij,gj->g", gp1, D, gp2)
        field[lo : lo + chunk] = acc
    return field


def fit2(data, K=6, iters=600, lr=0.05, seed=0, bins=40, callback=None,
         densify_every=80, K_max=16, densify_until=None, prune_weight=5e-3,
         birth_weight=0.05, birth_grid=7, lambda_neg=10.0, lambda_sum=1.0,
         n_birth=1, birth_spread=1.0):
    """Adam on the analytic loss gradient. Returns the fitted mixture.

    With densify_every set, every densify_every iterations (up to
    densify_until, default 0.6 * iters): adapt2 prunes/splits, and if capacity
    remains up to n_birth splats are born at the |field| extrema of the 4D
    weight-gradient field (birth_field2), each with the descent sign and
    greedily spread by birth_spread. The two-mode fringe is a delocalized 2D
    structure, so a single birth per event (n_birth=1, the fit.py policy)
    grows it very slowly; n_birth > 1 seeds a batch of signed fringe splats at
    once. K grows up to K_max.
    """
    centers, targets = histogram_targets2(data, bins=bins)
    mix = SplatMixture2.random_init(K, rng=seed)
    v = _pack2(mix)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    if densify_until is None:
        densify_until = int(0.6 * iters)

    xg = np.linspace(centers[0], centers[-1], birth_grid)
    G1, G2, G3, G4 = np.meshgrid(xg, xg, xg, xg, indexing="ij")
    candidates = np.stack([G1.ravel(), G2.ravel(), G3.ravel(), G4.ravel()], axis=1)

    gnorm = np.zeros(K)
    for t in range(1, iters + 1):
        cur, grad = loss_and_grad2(
            _unpack2(v, K), centers, targets, lambda_neg=lambda_neg, lambda_sum=lambda_sum
        )
        gnorm += np.linalg.norm(grad[K : 5 * K].reshape(K, 4), axis=1)
        m1 = 0.9 * m1 + 0.1 * grad
        m2 = 0.999 * m2 + 0.001 * grad ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if densify_every and t % densify_every == 0 and t <= densify_until:
            mix_t, m1, m2 = adapt2(
                _unpack2(v, K), m1, m2, gnorm / densify_every,
                K_max=K_max, prune_weight=prune_weight,
            )
            if len(mix_t.w) < K_max:
                field = birth_field2(
                    mix_t, centers, targets, candidates, lambda_neg=lambda_neg
                )
                room = K_max - len(mix_t.w)
                idx = _birth_batch(field, candidates, min(n_birth, room), birth_spread)
                for i in idx:
                    mix_t = SplatMixture2(
                        np.append(mix_t.w, -np.sign(field[i]) * birth_weight),
                        np.vstack([mix_t.mu, candidates[i]]),
                        np.concatenate([mix_t.s, np.full((1, 2, 2), np.log(0.5))], axis=0),
                        np.vstack([mix_t.phi, np.zeros((1, 2))]),
                    )
                    m1 = _append_zero_splat2(m1, len(mix_t.w) - 1)
                    m2 = _append_zero_splat2(m2, len(mix_t.w) - 1)
            K = len(mix_t.w)
            v = _pack2(mix_t)
            gnorm = np.zeros(K)
        if callback and t % 100 == 0:
            callback(t, loss2(_unpack2(v, K), centers, targets))
    return _unpack2(v, K)
