"""Three-mode iterative maximum-likelihood tomography (Lvovsky R rho R).

The three-mode lift of mle2.py and the "opponent" side of the decisive scaling
point (issue #7): measurement operators are rank-one projectors onto
|x1_th1>|x2_th2>|x3_th3| = kron(<.|x1_th1>, <.|x2_th2>, <.|x3_th3>) at the 3D
bin centers, in a truncated product Fock basis (n_max per mode, dimension
n_max**3). Consumes the SAME shared 3D histograms as fit3 via
data3.histogram_targets3 -- the fairness rule in docs/three-mode-plan.md.

Cost, not a fidelity pass/fail, is the headline of this baseline: at n_max=8
the density matrix is 512 x 512, at n_max=10 it is 1000 x 1000, and the
per-iteration work is O(M N^2) with N = n_max**3 and M ~ 50k measurement rows.
See tests/test_three_mode_mle.py for the measured seconds/iteration and the
honest extrapolation to convergence.

Same hardened stop condition as mle.py/mle2.py: R rho R ascends the likelihood
monotonically, so a real decrease means broken operators or truncation, not
convergence, and raises RuntimeError. The MLE ceiling is the truncation
fidelity of the TRUE cat at n_max (fock.cat3_truncation_fidelity: n_max=8 ->
0.99321, 10 -> 0.99964, 12 -> 0.99999 at alpha=1.5).

Differences from mle2.mle2_reconstruct (all documented, deliberate):

* Richer return signature (rho, iterations_run, converged): converged is True
  only when the |delta ll| < tol stop condition fired; a time-budget or
  iteration-cap return yields False. mle2 returns just (rho, iters).
* time_budget_s: a soft wall clock. Checked at each iteration boundary; if the
  loop has already run past it, the current rho is returned with converged=False
  rather than starting another (multi-second) iteration. None disables it.
* callback(it, loglik, elapsed_s, rho) is called at the END OF EVERY iteration
  (not throttled to every 50 like mle2). The caller throttles -- e.g.
  ``if it % 20 == 0: ...`` -- which lets a driver both time each iteration
  (elapsed_s deltas) and sample a fidelity trajectory (from rho) without the
  library committing to one cadence. elapsed_s is measured from the start of
  the iteration loop, i.e. it EXCLUDES the one-off V build.
* Memory-aware V assembly: the concatenated measurement matrix V is
  (M, n_max**3) complex128. At the official budget (27 triples x 2000 shots,
  bins=24) only ~656 cells/triple are nonzero, so M ~ 17.7k and V is ~0.15 GB
  at n_max=8, ~0.28 GB at n_max=10 -- denser data scales this linearly. It is
  built per-triple and concatenated only if the estimate (plus one working copy
  for V.conj() @ rho) fits comfortably in RAM; otherwise the per-triple blocks
  are kept in a list and p / R are accumulated block by block. Either way the
  arithmetic is identical; concatenation just trades memory for one big BLAS
  call per iteration instead of a loop.
"""

import numpy as np

from .fock import quadrature_vectors


def _available_bytes():
    """Best-effort free RAM in bytes (Linux /proc/meminfo MemAvailable).

    Returns None if it cannot be read; callers then default to the safe
    per-triple path.
    """
    try:
        with open("/proc/meminfo") as fh:
            for line in fh:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        return None
    return None


def _build_blocks(centers, targets, n_max):
    """Per-triple (V_t, f_t): measurement rows and globally-normalized freqs.

    Each row of V_t is the triple kron <m|x1_th><n|x2_th><q|x3_th> at a nonzero
    3D cell, flattened with index (m*n_max + n)*n_max + q -- the SAME layout as
    fock.cat3_fock, so a reconstructed rho lines up with cat3_fock's coefficient
    vector for fidelity_pure. f_t are the cell densities times dx^3, divided by
    the number of triples; the returned blocks' f's already sum to 1 across all
    triples.
    """
    dx = centers[1] - centers[0]
    dx3 = dx ** 3
    n_triples = len(targets)
    n3 = n_max ** 3
    blocks = []
    for (theta1, theta2, theta3), hist in targets:
        keep = hist > 0
        i_idx, j_idx, k_idx = np.nonzero(keep)
        v1 = quadrature_vectors(centers, theta1, n_max)  # (B, n_max), <m|x1>
        v2 = quadrature_vectors(centers, theta2, n_max)  # <n|x2>
        v3 = quadrature_vectors(centers, theta3, n_max)  # <q|x3>
        # triple kron per outcome: (nnz, n_max, n_max, n_max) -> (nnz, n3)
        rows = (
            v1[i_idx][:, :, None, None]
            * v2[j_idx][:, None, :, None]
            * v3[k_idx][:, None, None, :]
        )
        V_t = rows.reshape(len(i_idx), n3)
        f_t = hist[i_idx, j_idx, k_idx] * dx3 / n_triples
        blocks.append((V_t, f_t))
    total = sum(f_t.sum() for _, f_t in blocks)
    blocks = [(V_t, f_t / total) for V_t, f_t in blocks]
    return blocks


def mle3_reconstruct(centers, targets, n_max=8, max_iters=2000, tol=1e-10,
                     callback=None, time_budget_s=None):
    """R rho R fixed-point iteration on binned three-mode homodyne data.

    centers, targets: as returned by data3.histogram_targets3 -- targets is a
    list of ((theta1, theta2, theta3), hist) with hist[i, j, k] the density at
    (x1 = centers[i], x2 = centers[j], x3 = centers[k]).

    Returns (rho, iterations_run, converged). rho is on the product Fock basis
    (n_max**3, n_max**3), flat index (m*n_max + n)*n_max + q. converged is True
    only if the |delta loglik| < tol stop condition fired; a time-budget or
    iteration-cap return yields False.

    n_max: Fock cutoff per mode (dimension n_max**3). time_budget_s: optional
    soft wall clock checked at iteration boundaries. callback: see the module
    docstring -- called (it, loglik, elapsed_s, rho) every iteration.
    """
    import time

    dx = centers[1] - centers[0]
    dx3 = dx ** 3
    n3 = n_max ** 3

    blocks = _build_blocks(centers, targets, n_max)
    M = sum(len(f_t) for _, f_t in blocks)

    # Decide whether to concatenate. The concatenated V is M*n3 complex128; the
    # per-iteration V.conj() @ rho needs a second array of the same size, so
    # budget ~2x plus headroom. Fall back to per-triple accumulation otherwise.
    concat_bytes = M * n3 * 16
    avail = _available_bytes()
    concatenate = avail is not None and 2.5 * concat_bytes < 0.6 * avail
    if concatenate:
        V = np.concatenate([V_t for V_t, _ in blocks])
        f = np.concatenate([f_t for _, f_t in blocks])
        blocks = [(V, f)]  # single-block: same loop below, one big BLAS call

    rho = np.eye(n3, dtype=complex) / n3
    prev_ll = -np.inf
    t_loop = time.perf_counter()
    for it in range(1, max_iters + 1):
        # p_m = <v_m| rho |v_m> dx^3 and R = sum_m (f_m / p_m) |v_m><v_m| dx^3,
        # accumulated over blocks (one block if concatenated).
        ll = 0.0
        R = np.zeros((n3, n3), dtype=complex)
        for V_t, f_t in blocks:
            Vc_rho = V_t.conj() @ rho  # (nnz, n3)
            p = np.real(np.einsum("mj,mj->m", Vc_rho, V_t)) * dx3
            p = np.maximum(p, 1e-300)
            ll += float(f_t @ np.log(p))
            R += (V_t * (f_t / p * dx3)[:, None]).T @ V_t.conj()
        rho = R @ rho @ R
        rho = (rho + rho.conj().T) / 2
        rho /= np.real(np.trace(rho))

        elapsed = time.perf_counter() - t_loop
        if callback:
            callback(it, ll, elapsed, rho)

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
                return rho, it, True
        prev_ll = ll

        # Soft wall clock: stop at the boundary rather than begin another
        # multi-second iteration. converged=False -- this is a DNF return.
        if time_budget_s is not None and elapsed >= time_budget_s:
            return rho, it, False

    return rho, max_iters, False
