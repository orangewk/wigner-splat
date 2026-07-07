"""Two-mode iterative maximum-likelihood tomography (Lvovsky R rho R).

The product-Fock lift of mle.py: measurement operators are rank-one
projectors onto |x1_th1>|x2_th2> = kron(<.|x1_th1>, <.|x2_th2>) at the 2D
bin centers, in a truncated product Fock basis (n_max per mode, dimension
n_max**2). Consumes the SAME shared 2D histograms as fit2 via
data2.histogram_targets2 -- the fairness rule in docs/two-mode-plan.md.

Same hardened stop condition as mle.py: R rho R ascends the likelihood
monotonically, so a real decrease means broken operators or truncation, not
convergence, and raises RuntimeError. The MLE ceiling is the truncation
fidelity of the TRUE cat at n_max (fock.cat2_truncation_fidelity).
"""

import numpy as np

from .fock import quadrature_vectors


def mle2_reconstruct(centers, targets, n_max=12, max_iters=2000, tol=1e-10,
                     callback=None):
    """R rho R fixed-point iteration on binned joint homodyne data.

    centers, targets: as returned by data2.histogram_targets2 -- targets is
    a list of ((theta1, theta2), hist) with hist[i, j] the density at
    (x1 = centers[i], x2 = centers[j]). Returns (rho, iterations_run) with
    rho on the product Fock basis (n_max**2, n_max**2), flat index m*n_max+n.
    """
    dx = centers[1] - centers[0]
    dx2 = dx * dx
    n_pairs = len(targets)
    n2 = n_max * n_max

    # Stack all (pair, bin) outcomes with nonzero counts. Each measurement
    # vector is |v>_(mn) = <m|x1_th1><n|x2_th2> = kron(v1_i, v2_j), a row of V.
    V, f = [], []
    for (theta1, theta2), hist in targets:
        keep = hist > 0
        i_idx, j_idx = np.nonzero(keep)
        v1 = quadrature_vectors(centers, theta1, n_max)  # (B, n_max), <m|x1>
        v2 = quadrature_vectors(centers, theta2, n_max)  # (B, n_max), <n|x2>
        # kron per outcome, vectorized: (nnz, n_max, n_max) -> (nnz, n_max**2)
        rows = v1[i_idx][:, :, None] * v2[j_idx][:, None, :]
        V.append(rows.reshape(len(i_idx), n2))
        f.append(hist[i_idx, j_idx] * dx2 / n_pairs)
    V = np.concatenate(V)  # (M, n_max**2)
    f = np.concatenate(f)
    f = f / f.sum()

    rho = np.eye(n2, dtype=complex) / n2
    prev_ll = -np.inf
    for it in range(1, max_iters + 1):
        # p_m = <v_m| rho |v_m> dx^2 = sum_ij conj(V_mi) rho_ij V_mj
        p = np.real(np.einsum("mj,mj->m", V.conj() @ rho, V)) * dx2
        p = np.maximum(p, 1e-300)
        ll = float(f @ np.log(p))
        # R = sum_m (f_m / p_m) |v_m><v_m| dx^2, with |v_m>_i = <i|x_m>
        R = (V * (f / p * dx2)[:, None]).T @ V.conj()
        rho = R @ rho @ R
        rho = (rho + rho.conj().T) / 2
        rho /= np.real(np.trace(rho))
        if callback and it % 50 == 0:
            callback(it, ll)
        if it > 10:
            delta = ll - prev_ll
            scale = max(1.0, abs(ll))
            # monotonic ascent; a real decrease means broken operators
            if delta < -100 * tol * scale:
                raise RuntimeError(
                    f"R rho R likelihood decreased at iteration {it} "
                    f"(delta={delta:.3e}); monotonic ascent violated"
                )
            if abs(delta) < tol * scale:
                return rho, it
        prev_ll = ll
    return rho, max_iters
