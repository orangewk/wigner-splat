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
