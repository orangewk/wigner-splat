"""Exp16 optional MLE arm (issue #39): the data-seed axis only.

The main run exposed strong init sensitivity in the lossy-target rank-2
fit (best-by-NLL F = 0.9524 on data seed 1, near exp11's single MLE
reference 0.9554), so the issue's optional MLE runs become decision
relevant: without per-data-seed MLE values the exp11 "does not lose"
verdict cannot be checked off seed 42. Protocol: exp11's MLE config
unchanged (n_max=8, bins=24, 900 s budget, deterministic given the binned
data), one run per (target, data seed) -- 6 runs. Compared against the
main run's best-init-by-NLL BB-dagger values per data seed.
"""
import importlib.util
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.data3 import histogram_targets3  # noqa: E402
from wigner_splat.fock import lossy_cat3_fock  # noqa: E402
from wigner_splat.mle3 import mle3_reconstruct  # noqa: E402
from wigner_splat.states3x import (  # noqa: E402
    LossyThreeModeCat, SqueezedThreeModeCat,
)

spec = importlib.util.spec_from_file_location(
    "run15", pathlib.Path(__file__).parent / "run.py")
run15 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run15)


def main():
    print("=== exp16 optional MLE arm (issue #39): data-seed axis ===")
    print(f"exp11 MLE config unchanged: n_max={run15.N_MAX}, "
          f"bins={run15.BINS}, budget {run15.MLE_BUDGET_S:.0f}s", flush=True)
    rho_t_lossy = lossy_cat3_fock(run15.ALPHA, run15.PARITY, run15.ETA,
                                  run15.N_MAX)
    psi_t, retention = run15.squeezed_cat3_fock_psi(
        run15.ALPHA, run15.PARITY, run15.SQUEEZE_R, run15.N_MAX)
    psi_tn = psi_t / np.linalg.norm(psi_t)
    results = []
    for ds in run15.DATA_SEEDS:
        target = LossyThreeModeCat(run15.ALPHA, run15.PARITY, eta=run15.ETA)
        data = target.sample_homodyne(run15.GRID, run15.SHOTS, rng=ds)
        centers, targets_h = histogram_targets3(data, bins=run15.BINS)
        rho, iters, conv = mle3_reconstruct(
            centers, targets_h, n_max=run15.N_MAX,
            time_budget_s=run15.MLE_BUDGET_S)
        F = run15.uhlmann(rho, rho_t_lossy)
        results.append(dict(target="lossy", data_seed=ds, F=F,
                            converged=bool(conv)))
        print(f"  mle3 lossy    data={ds:2d} F={F:.4f} converged={conv} "
              f"({iters} iters)", flush=True)
    for ds in run15.DATA_SEEDS:
        target = SqueezedThreeModeCat(run15.ALPHA, run15.PARITY,
                                      r=run15.SQUEEZE_R)
        data = target.sample_homodyne(run15.GRID, run15.SHOTS, rng=ds)
        centers, targets_h = histogram_targets3(data, bins=run15.BINS)
        rho, iters, conv = mle3_reconstruct(
            centers, targets_h, n_max=run15.N_MAX,
            time_budget_s=run15.MLE_BUDGET_S)
        F = float(np.real(np.conj(psi_tn) @ rho @ psi_tn)) * retention
        results.append(dict(target="squeezed", data_seed=ds, F=F,
                            converged=bool(conv)))
        print(f"  mle3 squeezed data={ds:2d} F={F:.4f} converged={conv} "
              f"({iters} iters)", flush=True)
    out = pathlib.Path(__file__).parent / "results_mle.json"
    out.write_text(json.dumps(results, indent=1))
    print(f"raw results -> {out}")
    print("\nBB-dagger best-init-by-NLL per data seed, from the main run: "
          "lossy rank-2 {42: 0.9947, 1: 0.9524, 2: 0.9948}; "
          "squeezed K=4 {42: 0.9700, 1: 0.9690, 2: 0.9761}")


if __name__ == "__main__":
    main()
