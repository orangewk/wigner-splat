"""Experiment 16 -- issue #39: multi-seed replication of experiment 11.

Experiment 11's ruling (BB-dagger family adaptability, issue #28) rests on a
single run: data seed 42, init seed 0. On the squeezed target the margin over
the purefock control is only +0.0089, small enough to drown in seed noise.
This experiment reruns the seed-sensitive fits over data seeds {42, 1, 2} x
init seeds {0, 1, 2} and reports whether exp11's single numbers are
representative. MLE (900 s/run) is optional per the issue: pass --mle to add
one MLE run per (target, data seed); it is deterministic given the binned
data, so the init axis does not apply.

PROTOCOL (declared before the run; exp11 conventions and configs unchanged):
  * targets: lossy cat (eta=0.8, mixed) and squeezed cat (r=0.4, pure),
    alpha=1.5 parity=+1, 3x3x3 angle triples x 2000 shots per data seed.
  * fits per (data seed, init seed) cell:
      - lossy:    fit_bbdagM_mixed R=2 K=2 iters=200 lr=0.05
                  fit_purefock3 n_max=8 iters=1000 lr=0.05
      - squeezed: fit_bbdagS K=4 iters=400 lr=0.05
                  fit_bbdagS K=2 iters=400 lr=0.05   (issue item 3: the
                  K=2 init-sensitivity quantification; exp11 itself used K=4)
                  fit_purefock3 n_max=8 iters=1000 lr=0.05
  * metrics: identical to exp11 (Uhlmann F vs the lossy target through
    states3x; exact closed-form F vs the squeezed cat; purefock scored
    against the truncated Fock target with its ceiling).
  * init selection rule: per data seed the representative fit is the init
    with the LOWEST TRAIN NLL (the fitting objective; never fidelity --
    fidelity uses target knowledge no method would have on real data).
  * K=2 success criterion, pre-declared: F >= 0.9 counts as success (the
    recorded failures sit at F ~ 0.00/0.15, cleanly separated).
  * significance: the primary comparison (bbdagS K=4 vs purefock on the
    squeezed target) is paired per data seed on best-init-by-NLL values,
    n=3. A one-sided sign test at n=3 bottoms out at p=1/8=0.125, so this
    design CANNOT reach conventional significance; per the issue's
    acceptance criteria, a consistent sign is reported descriptively and
    anything less downgrades the exp11 wording to "on par with the generic
    control on the squeezed target". The 9 per-cell paired differences are
    reported as a secondary descriptive view (cells share data seeds, so
    they are not 9 independent draws).
"""
import argparse
import itertools
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagM import fit_bbdagM_mixed, nll_mixed  # noqa: E402
from wigner_splat.bbdagS import (  # noqa: E402
    fidelity_vs_squeezed_cat3 as fid_sq_ansatz, fit_bbdagS, nll as nll_sq,
)
from wigner_splat.data3 import histogram_targets3  # noqa: E402
from wigner_splat.fock import hermite_psi, lossy_cat3_fock  # noqa: E402
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
DATA_SEEDS = [42, 1, 2]
INIT_SEEDS = [0, 1, 2]
N_MAX = 8
BINS = 24
MLE_BUDGET_S = 900.0
LR = 0.05
K2_SUCCESS_F = 0.9
EXP11_SINGLE = {  # the exp11 committed-log values under scrutiny
    ("lossy", "bbdagM_R2K2"): 0.9947,
    ("lossy", "purefock"): 0.5169,
    ("squeezed", "bbdagS_K4"): 0.9700,
    ("squeezed", "purefock"): 0.9611,
}
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
    """Quadrature-projected truncated Fock ket of the squeezed cat (exp11)."""
    from wigner_splat.bbdagS import sq_wavefunction
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


def purefock_fidelity_lossy(pf, rho_t):
    flat = pf.ravel()
    return float(np.real(np.conj(flat) @ rho_t @ flat)
                 / np.real(np.vdot(flat, flat)))


def purefock_fidelity_squeezed(pf, psi_tn, retention):
    flat = pf.ravel()
    return (float(np.abs(np.vdot(psi_tn, flat)) ** 2
                  / np.real(np.vdot(flat, flat))) * retention)


def run_cell(fit_fn, metric_fn, nll_fn, label, data_seed, init_seed, results):
    t0 = time.perf_counter()
    fitted = fit_fn(init_seed)
    wall = time.perf_counter() - t0
    F = metric_fn(fitted)
    train_nll = nll_fn(fitted)
    results.append(dict(method=label, data_seed=data_seed,
                        init_seed=init_seed, F=F, train_nll=train_nll,
                        wall_s=wall))
    print(f"  {label:14s} data={data_seed:2d} init={init_seed} "
          f"F={F:.4f} NLL={train_nll:.4f} wall={wall:.0f}s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mle", action="store_true",
                    help="also run MLE once per (target, data seed)")
    args = ap.parse_args()

    print("=== exp16: issue #39 -- multi-seed replication of exp11 ===")
    print(f"data seeds {DATA_SEEDS} x init seeds {INIT_SEEDS}, exp11 configs "
          f"unchanged; alpha={ALPHA} parity={PARITY}, {len(GRID)} triples x "
          f"{SHOTS} shots; K=2 success threshold F>={K2_SUCCESS_F}",
          flush=True)

    results = []
    rho_t_lossy = lossy_cat3_fock(ALPHA, PARITY, ETA, N_MAX)
    psi_t, retention = squeezed_cat3_fock_psi(ALPHA, PARITY, SQUEEZE_R, N_MAX)
    psi_tn = psi_t / np.linalg.norm(psi_t)

    for ds in DATA_SEEDS:
        print(f"\n--- data seed {ds}: lossy cat eta={ETA} ---", flush=True)
        target = LossyThreeModeCat(ALPHA, PARITY, eta=ETA)
        data = target.sample_homodyne(GRID, SHOTS, rng=ds)
        for isd in INIT_SEEDS:
            run_cell(lambda s: fit_bbdagM_mixed(data, R=2, K=2, M=3,
                                                iters=200, lr=LR, seed=s),
                     lambda st: uhlmann_fidelity_vs_lossy_cat3(st, target),
                     lambda st: nll_mixed(st, data),
                     "bbdagM_R2K2", ds, isd, results)
        for isd in INIT_SEEDS:
            run_cell(lambda s: fit_purefock3(data, n_max=N_MAX, iters=1000,
                                             lr=LR, seed=s),
                     lambda pf: purefock_fidelity_lossy(pf, rho_t_lossy),
                     lambda pf: nll_psi(pf, data),
                     "purefock", ds, isd, results)
        if args.mle:
            centers, targets_h = histogram_targets3(data, bins=BINS)
            t0 = time.perf_counter()
            rho, iters, conv = mle3_reconstruct(
                centers, targets_h, n_max=N_MAX, time_budget_s=MLE_BUDGET_S)
            wall = time.perf_counter() - t0
            F = uhlmann(rho, rho_t_lossy)
            results.append(dict(method="mle3", data_seed=ds, init_seed=None,
                                F=F, train_nll=None, wall_s=wall,
                                converged=bool(conv), target="lossy"))
            print(f"  mle3           data={ds:2d} F={F:.4f} "
                  f"converged={conv} wall={wall:.0f}s", flush=True)

    for ds in DATA_SEEDS:
        print(f"\n--- data seed {ds}: squeezed cat r={SQUEEZE_R} ---",
              flush=True)
        target = SqueezedThreeModeCat(ALPHA, PARITY, r=SQUEEZE_R)
        data = target.sample_homodyne(GRID, SHOTS, rng=ds)
        for K, label in ((4, "bbdagS_K4"), (2, "bbdagS_K2")):
            for isd in INIT_SEEDS:
                run_cell(lambda s, K=K: fit_bbdagS(data, K=K, M=3, iters=400,
                                                   lr=LR, seed=s),
                         lambda st: fid_sq_ansatz(st, ALPHA, PARITY,
                                                  r=SQUEEZE_R),
                         lambda st: nll_sq(st, data),
                         label, ds, isd, results)
        for isd in INIT_SEEDS:
            run_cell(lambda s: fit_purefock3(data, n_max=N_MAX, iters=1000,
                                             lr=LR, seed=s),
                     lambda pf: purefock_fidelity_squeezed(pf, psi_tn,
                                                           retention),
                     lambda pf: nll_psi(pf, data),
                     "purefock_sq", ds, isd, results)
        if args.mle:
            centers, targets_h = histogram_targets3(data, bins=BINS)
            t0 = time.perf_counter()
            rho, iters, conv = mle3_reconstruct(
                centers, targets_h, n_max=N_MAX, time_budget_s=MLE_BUDGET_S)
            wall = time.perf_counter() - t0
            F = float(np.real(np.conj(psi_tn) @ rho @ psi_tn)) * retention
            results.append(dict(method="mle3_sq", data_seed=ds,
                                init_seed=None, F=F, train_nll=None,
                                wall_s=wall, converged=bool(conv),
                                target="squeezed"))
            print(f"  mle3           data={ds:2d} F={F:.4f} "
                  f"converged={conv} wall={wall:.0f}s", flush=True)

    out = pathlib.Path(__file__).parent / "results.json"
    out.write_text(json.dumps(results, indent=1))
    print(f"\nraw results -> {out}", flush=True)
    summarize(results)


def summarize(results):
    def cells(method):
        return [r for r in results if r["method"] == method]

    def best_by_nll(method, ds):
        cs = [r for r in cells(method) if r["data_seed"] == ds]
        return min(cs, key=lambda r: r["train_nll"])

    exp11_key = {"bbdagM_R2K2": ("lossy", "bbdagM_R2K2"),
                 "purefock": ("lossy", "purefock"),
                 "bbdagS_K4": ("squeezed", "bbdagS_K4"),
                 "purefock_sq": ("squeezed", "purefock")}

    print("\n=== summary (all 9 cells; representative = best train NLL per "
          "data seed) ===")
    for method in ("bbdagM_R2K2", "purefock", "bbdagS_K4", "bbdagS_K2",
                   "purefock_sq"):
        cs = cells(method)
        if not cs:
            continue
        Fs = np.array([r["F"] for r in cs])
        reps = [best_by_nll(method, ds)["F"] for ds in DATA_SEEDS]
        line = (f"{method:14s} all9: mean={Fs.mean():.4f} "
                f"range=[{Fs.min():.4f}, {Fs.max():.4f}]  "
                f"best-init/seed: {', '.join(f'{v:.4f}' for v in reps)}")
        if method in exp11_key:
            v11 = EXP11_SINGLE[exp11_key[method]]
            inside = Fs.min() <= v11 <= Fs.max()
            line += f"  exp11={v11:.4f} ({'inside' if inside else 'OUTSIDE'} range)"
        print(line)

    print("\n=== primary comparison: bbdagS K=4 vs purefock (squeezed), "
          "paired per data seed on best-init-by-NLL ===")
    diffs = []
    for ds in DATA_SEEDS:
        d = best_by_nll("bbdagS_K4", ds)["F"] - best_by_nll("purefock_sq",
                                                            ds)["F"]
        diffs.append(d)
        print(f"  data seed {ds:2d}: diff = {d:+.4f}")
    signs = set(np.sign(diffs))
    consistent = len(signs) == 1 and 0.0 not in signs
    print(f"  sign-consistent: {consistent} (n=3; one-sided sign-test floor "
          "p=0.125 -- CANNOT reach 0.05, descriptive only)")
    sec = []
    for ds in DATA_SEEDS:
        for isd in INIT_SEEDS:
            a = next(r for r in cells("bbdagS_K4")
                     if r["data_seed"] == ds and r["init_seed"] == isd)
            b = next(r for r in cells("purefock_sq")
                     if r["data_seed"] == ds and r["init_seed"] == isd)
            sec.append(a["F"] - b["F"])
    sec = np.array(sec)
    print(f"  secondary (9 per-cell diffs, not independent): mean={sec.mean():+.4f} "
          f"range=[{sec.min():+.4f}, {sec.max():+.4f}], "
          f"{int((sec > 0).sum())}/9 positive")

    print("\n=== issue item 3: bbdagS K=2 vs K=4 init sensitivity "
          f"(success = F >= {K2_SUCCESS_F}) ===")
    for method in ("bbdagS_K2", "bbdagS_K4"):
        cs = cells(method)
        ok = [r for r in cs if r["F"] >= K2_SUCCESS_F]
        print(f"  {method}: {len(ok)}/{len(cs)} success; failures: "
              + (", ".join(f"(data={r['data_seed']},init={r['init_seed']},"
                           f"F={r['F']:.4f})"
                           for r in cs if r["F"] < K2_SUCCESS_F) or "none"))

    mle_rows = [r for r in results if r["method"].startswith("mle3")]
    if mle_rows:
        print("\n=== optional MLE (one per target x data seed) ===")
        for r in mle_rows:
            print(f"  {r['method']:8s} data={r['data_seed']:2d} F={r['F']:.4f} "
                  f"converged={r['converged']} wall={r['wall_s']:.0f}s")


if __name__ == "__main__":
    main()
