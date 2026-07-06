"""Iterative maximum-likelihood tomography baseline (Lvovsky R rho R).

This is the comparison target for the falsification condition in the
README: if the splat fitter cannot beat this on both fidelity and speed
at equal shot counts, the splatting approach brings no computational gain.

Works on the SAME binned histograms as fit.py (histogram_targets output),
so both methods see identical data. Measurement operators are rank-one
quadrature projectors |x_theta><x_theta| dx at the bin centers, in a Fock
basis truncated at n_max.
"""

import numpy as np

from .fock import quadrature_vectors


def mle_reconstruct(centers, targets, n_max=20, max_iters=2000, tol=1e-10,
                    callback=None):
    """R rho R fixed-point iteration on binned homodyne data.

    centers, targets: as returned by fit.histogram_targets (per-angle
    density histograms). Returns (rho, iterations_run).
    """
    dx = centers[1] - centers[0]
    n_angles = len(targets)
    # stack all (angle, bin) outcomes with nonzero counts: V rows are <n|x_theta>
    V, f = [], []
    for theta, hist in targets:
        keep = hist > 0
        V.append(quadrature_vectors(centers[keep], theta, n_max))
        # frequency of each outcome among all shots (equal shots per angle)
        f.append(hist[keep] * dx / n_angles)
    V = np.concatenate(V)  # (M, n_max)
    f = np.concatenate(f)
    f = f / f.sum()

    rho = np.eye(n_max, dtype=complex) / n_max
    prev_ll = -np.inf
    for it in range(1, max_iters + 1):
        p = np.real(np.einsum("mi,ij,mj->m", V.conj(), rho, V)) * dx
        p = np.maximum(p, 1e-300)
        ll = float(f @ np.log(p))
        # R = sum_m (f_m / p_m) |v_m><v_m| dx, with |v_m>_i = <i|x_m>
        R = (V * (f / p * dx)[:, None]).T @ V.conj()
        rho = R @ rho @ R
        rho = (rho + rho.conj().T) / 2
        rho /= np.real(np.trace(rho))
        if callback and it % 50 == 0:
            callback(it, ll)
        if ll - prev_ll < tol * max(1.0, abs(ll)) and it > 10:
            return rho, it
        prev_ll = ll
    return rho, max_iters
