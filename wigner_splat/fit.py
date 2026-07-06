"""v0 reconstructor: fit a signed splat mixture to binned homodyne data.

Loss = sum_theta L2(model marginal, histogram density)
     + lambda_neg * sum_theta mean(relu(-model)^2)   (marginals must be nonnegative)
     + lambda_sum * (sum_k w_k - 1)^2                (total probability)

The forward model (forward.radon) is a closed-form Gaussian projection, so
the loss gradient is closed-form too: for each angle theta with direction
u = (cos theta, sin theta), each splat contributes w_k N(x; m_k, var_k)
with m_k = mu_k . u and var_k = e^{2 s1} cos^2(phi - theta)
+ e^{2 s2} sin^2(phi - theta), and the chain rule through (m_k, var_k)
gives every parameter gradient in one vectorized pass per angle. K stays
fixed; gradient-norm-driven densification/pruning is the next milestone.
"""

import numpy as np

from .forward import SplatMixture


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
    """
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


def fit(data, K=8, iters=800, lr=0.05, seed=0, bins=80, callback=None):
    """Adam on the analytic loss gradient. Returns the fitted mixture."""
    centers, targets = histogram_targets(data, bins=bins)
    mix = SplatMixture.random_init(K, rng=seed)
    v = _pack(mix)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        cur, grad = loss_and_grad(_unpack(v, K), centers, targets)
        m1 = 0.9 * m1 + 0.1 * grad
        m2 = 0.999 * m2 + 0.001 * grad ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 100 == 0:
            callback(t, loss(_unpack(v, K), centers, targets))
    return _unpack(v, K)
