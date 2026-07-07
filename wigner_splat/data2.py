"""Shared 2D binning for two-mode homodyne data.

Both two-mode reconstructors (fit2 and mle2) must consume IDENTICAL
histograms — the fairness rule in docs/two-mode-plan.md — so the binning
lives here, owned by neither.
"""

import numpy as np


def histogram_targets2(data, bins=40, x_max=None):
    """Bin joint samples per angle pair into 2D density histograms.

    data: [((theta1, theta2), samples (shots, 2))] as produced by
    states2.TwoModeCat.sample_homodyne. Returns (centers, targets) with
    centers (bins,) shared by both axes and targets a list of
    ((theta1, theta2), hist) where hist[i, j] is the density at
    (x1 = centers[i], x2 = centers[j]).
    """
    x_max = x_max or max(np.abs(s).max() for _, s in data) * 1.05
    edges = np.linspace(-x_max, x_max, bins + 1)
    centers = (edges[:-1] + edges[1:]) / 2
    targets = []
    for angles, samples in data:
        hist, _, _ = np.histogram2d(
            samples[:, 0], samples[:, 1], bins=[edges, edges], density=True
        )
        targets.append((tuple(angles), hist))
    return centers, targets
