"""v0 reconstructor: fit a signed splat mixture to binned homodyne data.

Loss = sum_theta L2(model marginal, histogram density)
     + lambda_neg * sum_theta mean(relu(-model)^2)   (marginals must be nonnegative)
     + lambda_sum * (sum_k w_k - 1)^2                (total probability)

v0 keeps K fixed and uses numerical gradients + Adam: with K ~ 10 the
parameter count is ~60 and each loss evaluation is closed-form, so this
is fast enough to validate the representation. Analytic gradients and
gradient-norm-driven densification/pruning are the next milestones.
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


def fit(data, K=8, iters=800, lr=0.05, seed=0, bins=80, callback=None):
    """Adam on numerically-differentiated loss. Returns the fitted mixture."""
    centers, targets = histogram_targets(data, bins=bins)
    mix = SplatMixture.random_init(K, rng=seed)
    v = _pack(mix)
    eps = 1e-4
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    for t in range(1, iters + 1):
        grad = np.empty_like(v)
        base_plus = np.empty_like(v)
        for i in range(len(v)):
            vp, vm = v.copy(), v.copy()
            vp[i] += eps
            vm[i] -= eps
            grad[i] = (
                loss(_unpack(vp, K), centers, targets)
                - loss(_unpack(vm, K), centers, targets)
            ) / (2 * eps)
        m1 = 0.9 * m1 + 0.1 * grad
        m2 = 0.999 * m2 + 0.001 * grad ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step
        if callback and t % 100 == 0:
            callback(t, loss(_unpack(v, K), centers, targets))
    return _unpack(v, K)
