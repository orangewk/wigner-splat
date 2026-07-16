"""Shared 3D binning for three-mode homodyne data.

The exact analog of data2.histogram_targets2: both three-mode reconstructors
(fit3 and mle3) must consume IDENTICAL histograms — the fairness rule in
docs/three-mode-plan.md — so the binning lives here, owned by neither.
"""

import numpy as np


def histogram_targets3(data, bins=24, x_max=None):
    """Bin joint samples per angle triple into 3D density histograms.

    data: [((theta1, theta2, theta3), samples (shots, 3))] as produced by
    states3.ThreeModeCat.sample_homodyne. Returns (centers, targets) with
    centers (bins,) shared by all three axes and targets a list of
    ((theta1, theta2, theta3), hist) where hist[i, j, k] is the density at
    (x1 = centers[i], x2 = centers[j], x3 = centers[k]).
    """
    x_max = x_max or max(np.abs(s).max() for _, s in data) * 1.05
    edges = np.linspace(-x_max, x_max, bins + 1)
    centers = (edges[:-1] + edges[1:]) / 2
    targets = []
    for angles, samples in data:
        hist, _ = np.histogramdd(
            samples, bins=[edges, edges, edges], density=True
        )
        targets.append((tuple(angles), hist))
    return centers, targets


def apply_detection_noise(data, eta, extra_noise_var=0.0, rng=None):
    """Detector-side noise on ideal homodyne samples (issue #42 simulator).

    Maps every sample x -> sqrt(eta) x + N(0, sigma2), sigma2 = (1 - eta)/2 +
    extra_noise_var: efficiency-eta homodyne detection (the vacuum port
    contributes (1 - eta)/2 in this repo's vacuum-variance-1/2 convention)
    plus electronic noise. This is exactly the measured-pdf convolution the
    noise-aware reconstructors model, and it works on samples from ANY
    target. data: [(theta (M,), X (S, M))]; returns the same structure.
    """
    if not (0.0 <= eta <= 1.0):
        raise ValueError(f"eta must be in [0, 1], got {eta}")
    if extra_noise_var < 0.0:
        raise ValueError(f"extra_noise_var must be >= 0, got {extra_noise_var}")
    rng = np.random.default_rng(rng)
    sigma2 = (1.0 - eta) / 2.0 + extra_noise_var
    out = []
    for theta, X in data:
        X = np.asarray(X, float)
        noisy = np.sqrt(eta) * X + rng.normal(scale=np.sqrt(sigma2),
                                              size=X.shape)
        out.append((theta, noisy))
    return out
