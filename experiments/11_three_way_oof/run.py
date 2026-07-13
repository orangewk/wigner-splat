"""Experiment 11 -- issue #28 FORMAL RULING: BB-dagger vs splat vs MLE
on out-of-family targets.

Experiment 10 established the supporting evidence (rank-2 recovers the lossy
cat; coherent-K fidelity improves monotonically on the squeezed cat) but left
the falsification condition UNDECIDED because the splat and MLE sides had no
pipeline for the new targets. This experiment closes that gap:

targets (data seed 42, 3x3x3 triples x 2000 shots, exp06/exp10 conventions):
  * lossy cat    (eta = 0.8; MIXED, rank 2)  -- decoherence direction
  * squeezed cat (r = 0.4; pure, non-coherent kets) -- ket-shape direction

methods and metrics (each method uses its established best practice):
  * BB-dagger -- lossy: rank-2 coherent-product (exp10); squeezed: the NEW
    squeezed-product ansatz (bbdagS, issue #28 step 2). Exact Uhlmann /
    exact pure fidelity, closed form. Per-sample NLL objective.
  * splat (fit3f) -- histogram-L2 staged fit on binned data (bins=24).
    Score: closed-form target Wigner overlap tr(rho_mix rho_target)
    (forward3f.overlap_vs_*_cat3). NON-PSD representation, so this is an
    overlap score, not a state fidelity; for the mixed lossy target a perfect
    reconstruction scores the target PURITY, quoted alongside.
  * MLE (mle3) -- full-rank R rho R on the same binned data, n_max=8,
    900 s budget (exp06 protocol). Fidelity: Uhlmann vs the truncated target
    (lossy: fock.lossy_cat3_fock; squeezed: quadrature-projected pure ket),
    with the truncation ceiling quoted.
  * purefock (rank-1 Fock gradient ML, issue #27 control) -- for context.

Falsification condition (issue #28, now decidable): if BB-dagger's fidelity
is consistently below BOTH the splat score and the MLE fidelity on the
out-of-family targets, record "BB-dagger is target-aligned only" and split
off ansatz strengthening as its own workstream.
"""
import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagM import fit_bbdagM_mixed, nll_mixed  # noqa: E402
from wigner_splat.bbdagS import (  # noqa: E402
    fit_bbdagS, fidelity_vs_squeezed_cat3 as fid_sq_ansatz, nll as nll_sq,
    sq_wavefunction,
)
from wigner_splat.data3 import histogram_targets3  # noqa: E402
from wigner_splat.fit3f import fit3f  # noqa: E402
from wigner_splat.fock import hermite_psi, lossy_cat3_fock  # noqa: E402
from wigner_splat.forward3f import (  # noqa: E402
    lossy_cat3_purity, overlap_vs_lossy_cat3, overlap_vs_squeezed_cat3,
)
from wigner_splat.mle3 import mle3_reconstruct  # noqa: E402
from wigner_splat.purefock3 import fit_purefock3, nll_psi  # noqa: E402
from wigner_splat.states3x import (  # noqa: E402
    LossyThreeModeCat, SqueezedThreeModeCat, uhlmann_fidelity_vs_lossy_cat3,
)

ALPHA = 1.5
PARITY = +1
ETA = 0.8
SQUEEZE_R = 0.4
SHOTS = 2000
DATA_SEED = 42
INIT_SEED = 0
N_MAX = 8
BINS = 24
MLE_BUDGET_S = 900.0
LEARNING_RATE = 0.05
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]


def uhlmann(rho, sigma):
    """(tr sqrt(sqrt(rho) sigma sqrt(rho)))^2 via Hermitian eigendecomposition."""
    rho = (rho + rho.conj().T) / 2
    sigma = (sigma + sigma.conj().T) / 2
    w, U = np.linalg.eigh(rho)
    sq = (U * np.sqrt(np.maximum(w, 0.0))) @ U.conj().T
    inner = sq @ sigma @ sq
    inner = (inner + inner.conj().T) / 2
    ev = np.maximum(np.linalg.eigvalsh(inner), 0.0)
    return float(np.sum(np.sqrt(ev)) ** 2)


def squeezed_cat3_fock_psi(alpha, parity, r, n_max):
    """Quadrature-projected truncated Fock ket of the squeezed cat.

    <n|g_+-> by 1D quadrature per mode; the 3-mode ket is the parity
    combination of the tensor cubes. Returns (psi (n_max^3,), retention),
    retention = ||psi_trunc||^2 / <psi|psi> (the MLE ceiling analog).
    """
    x_max = np.sqrt(2) * (abs(alpha) + 2.0) + 8.0
    grid = np.linspace(-x_max, x_max, 4001)
    H = hermite_psi(grid, n_max)
    gp = sq_wavefunction(grid, alpha, complex(r))
    gm = sq_wavefunction(grid, -alpha, complex(r))
    ovp = np.trapezoid(H * gp[None, :], grid, axis=1)
    ovm = np.trapezoid(H * gm[None, :], grid, axis=1)
    P = (ovp[:, None, None] * ovp[None, :, None] * ovp[None, None, :]).reshape(-1)
    Q = (ovm[:, None, None] * ovm[None, :, None] * ovm[None, None, :]).reshape(-1)
    psi = P + parity * Q
    ov = np.trapezoid(np.conj(gm) * gp, grid)
    full_norm = float(2 * (1 + parity * np.real(ov ** 3)))
    retention = float(np.real(np.vdot(psi, psi)) / full_norm)
    return psi, retention


def run_mle(data, label):
    centers, targets = histogram_targets3(data, bins=BINS)
    t0 = time.perf_counter()
    rho, iters, converged = mle3_reconstruct(
        centers, targets, n_max=N_MAX, time_budget_s=MLE_BUDGET_S,
    )
    wall = time.perf_counter() - t0
    print(f"  [mle3 {label}] {iters} iters, converged={converged}, "
          f"wall={wall:.0f}s", flush=True)
    return rho, wall, converged


def lossy_block():
    target = LossyThreeModeCat(ALPHA, PARITY, eta=ETA)
    purity = lossy_cat3_purity(ALPHA, PARITY, ETA)
    print(f"--- target: lossy cat eta={ETA} (mixed; purity={purity:.4f} = "
          "perfect overlap score) ---", flush=True)
    data = target.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)
    rows = []

    t0 = time.perf_counter()
    bb = fit_bbdagM_mixed(data, R=2, K=2, M=3, iters=200, lr=LEARNING_RATE,
                          seed=INIT_SEED)
    wall = time.perf_counter() - t0
    F = uhlmann_fidelity_vs_lossy_cat3(bb, target)
    rows.append(("bbdag rank2 K=2", "Uhlmann F", F, wall,
                 f"NLL={nll_mixed(bb, data):.4f}"))

    t0 = time.perf_counter()
    mix = fit3f(data, bins=BINS)
    wall = time.perf_counter() - t0
    score = overlap_vs_lossy_cat3(mix, ALPHA, PARITY, ETA)
    rows.append(("splat fit3f", "overlap score", score, wall,
                 f"(perfect={purity:.4f}, non-PSD)"))

    rho_t = lossy_cat3_fock(ALPHA, PARITY, ETA, N_MAX)
    ceiling_note = f"target trunc trace={np.real(np.trace(rho_t)):.4f}"
    rho, wall, converged = run_mle(data, "lossy")
    F_mle = uhlmann(rho, rho_t)
    rows.append(("mle3 full-rank", "Uhlmann F", F_mle, wall,
                 f"converged={converged}, {ceiling_note}"))

    t0 = time.perf_counter()
    pf = fit_purefock3(data, n_max=N_MAX, iters=1000, lr=LEARNING_RATE,
                       seed=INIT_SEED)
    wall = time.perf_counter() - t0
    flat = pf.ravel()
    F_pf = float(np.real(np.conj(flat) @ rho_t @ flat)
                 / np.real(np.vdot(flat, flat)))
    rows.append(("purefock rank-1", "Uhlmann F", F_pf, wall,
                 f"NLL={nll_psi(pf, data):.4f} (wrong-rank control)"))
    return rows


def squeezed_block():
    target = SqueezedThreeModeCat(ALPHA, PARITY, r=SQUEEZE_R)
    print(f"\n--- target: squeezed cat r={SQUEEZE_R} (pure; perfect score = 1) "
          "---", flush=True)
    data = target.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)
    rows = []

    t0 = time.perf_counter()
    bb = fit_bbdagS(data, K=4, M=3, iters=400, lr=LEARNING_RATE, seed=INIT_SEED)
    wall = time.perf_counter() - t0
    F = fid_sq_ansatz(bb, ALPHA, PARITY, r=SQUEEZE_R)
    rows.append(("bbdag squeezed K=4", "exact F", F, wall,
                 f"NLL={nll_sq(bb, data):.4f}"))

    t0 = time.perf_counter()
    mix = fit3f(data, bins=BINS)
    wall = time.perf_counter() - t0
    score = overlap_vs_squeezed_cat3(mix, ALPHA, PARITY, SQUEEZE_R)
    rows.append(("splat fit3f", "overlap score", score, wall, "(non-PSD)"))

    psi_t, retention = squeezed_cat3_fock_psi(ALPHA, PARITY, SQUEEZE_R, N_MAX)
    psi_tn = psi_t / np.linalg.norm(psi_t)
    rho, wall, converged = run_mle(data, "squeezed")
    F_mle = float(np.real(np.conj(psi_tn) @ rho @ psi_tn)) * retention
    rows.append(("mle3 full-rank", "exact F", F_mle, wall,
                 f"converged={converged}, trunc ceiling={retention:.4f}"))

    t0 = time.perf_counter()
    pf = fit_purefock3(data, n_max=N_MAX, iters=1000, lr=LEARNING_RATE,
                       seed=INIT_SEED)
    wall = time.perf_counter() - t0
    flat = pf.ravel()
    F_pf = (float(np.abs(np.vdot(psi_tn, flat)) ** 2
                  / np.real(np.vdot(flat, flat))) * retention)
    rows.append(("purefock rank-1", "exact F", F_pf, wall,
                 f"NLL={nll_psi(pf, data):.4f}"))
    return rows


def show(rows):
    for name, metric, val, wall, note in rows:
        print(f"  {name:20s} {metric:14s} {val:.4f}  wall={wall:.0f}s  {note}",
              flush=True)


def main():
    print("=== exp11: issue #28 formal ruling -- BB-dagger vs splat vs MLE, "
          "out-of-family ===")
    print(f"alpha={ALPHA} parity={PARITY}, {len(GRID)} triples x {SHOTS} "
          f"shots, data seed {DATA_SEED}; binned methods use bins={BINS}, "
          f"Fock methods n_max={N_MAX}, MLE budget {MLE_BUDGET_S:.0f}s\n",
          flush=True)
    lossy = lossy_block()
    show(lossy)
    squeezed = squeezed_block()
    show(squeezed)

    print("\n=== ruling (issue #28 falsification condition) ===")
    verdicts = []
    for label, rows in (("lossy", lossy), ("squeezed", squeezed)):
        bb = next(v for n, _, v, _, _ in rows if n.startswith("bbdag"))
        splat = next(v for n, _, v, _, _ in rows if n.startswith("splat"))
        mle = next(v for n, _, v, _, _ in rows if n.startswith("mle3"))
        loses_both = bb < splat and bb < mle
        verdicts.append(loses_both)
        print(f"{label}: bbdag={bb:.4f} vs splat={splat:.4f} (overlap score) "
              f"vs mle={mle:.4f} -> bbdag "
              + ("LOSES to both" if loses_both else "does NOT lose to both"))
    print("NOTE: the splat column is a Wigner-overlap score of a non-PSD "
          "reconstruction (perfect = target purity on the mixed target), the "
          "other columns are state fidelities of physical states -- the "
          "cross-method comparison is therefore score-vs-fidelity, as in "
          "exp06/exp08, and is quoted with that caveat.")
    if all(verdicts):
        print("-> falsification condition FIRES on every target: record "
              "'BB-dagger is target-aligned only' and split off ansatz "
              "strengthening.")
    else:
        print("-> falsification condition does NOT fire: BB-dagger (with its "
              "rank-2 / squeezed-ket extensions) is not consistently beaten "
              "by splat and MLE out of family. Single data seed; see log for "
              "per-target detail.")


if __name__ == "__main__":
    main()
