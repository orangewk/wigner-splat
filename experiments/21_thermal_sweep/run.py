"""Experiment 21 -- issue #67: sigma_add / data-seed sweep of the
thermal gate (robustness of exp19's blind result).

Preprint prerequisite: exp19's headline (the channel-composed model
beating the converged full-rank MLE blind) is a SINGLE data seed, and
exp16 demonstrated that this very fit family is init-fragile enough to
flip verdicts on the pure-cat target (best-by-train-NLL selection can
pick an F-collapsed init because the likelihood is blind to the
collapse, dNLL ~ 1e-4 vs dF ~ 0.4). This sweep measures both failure
axes on the exp19 thermal target.

PROTOCOL (pre-declared on issue #67):
  * configs: data seeds {42, 1, 2} at sigma_add = 0.1, plus
    sigma_add {0.05, 0.2} at data seed 42 (5 configs; alpha = 1.5,
    parity = +1, eta = 0.8, 27 triples x 2000 shots -- exp19
    conventions; the 42/0.10 config is exp19 reproduced under the
    new metric).
  * per config: bbdagS lossy R2K4 (iters 400, init seeds {0,1,2},
    representative = best TRAIN NLL) vs mle3 (n_max 8, 900 s).
  * scoring: Fock-route target at n_max 8; the lossy model goes
    through the exp19 wide-intermediate pipeline (pre-loss kets at
    n=16, channel, crop). Fidelity = the GENERALIZED Uhlmann fidelity
    for subnormalized matrices (PR-64 round-2 metric; both traces
    quoted), so the crop's trace deficit no longer penalizes the
    lossy row -- the one row that carries it.
  * recorded per config: F of ALL THREE lossy inits (not just the
    representative -- the exp16 blindness diagnostic needs the spread),
    train-NLL spread, representative F, fitted eta', F_mle, verdict.
  * PRE-DECLARED READING: representative lossy F < F_mle on >= 1
    config -> the README/preprint wording gains an exp16-style
    init-fragility note on the thermal gate. All 5 hold -> the wording
    may add "robust across 3 data seeds and a 4x sigma_add range"
    (still one target class, still exploratory).
"""
import importlib.util
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagS import (  # noqa: E402
    fit_bbdagS_lossy_mixed, nll_lossy_mixed,
)
from wigner_splat.data3 import histogram_targets3  # noqa: E402
from wigner_splat.fock import thermal_lossy_cat3_fock  # noqa: E402
from wigner_splat.mle3 import mle3_reconstruct  # noqa: E402
from wigner_splat.states3x import ThermalLossyThreeModeCat  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "run19", pathlib.Path(__file__).resolve().parents[1]
    / "19_thermal_gate" / "run.py")
run19 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run19)

CONFIGS = [(42, 0.10), (1, 0.10), (2, 0.10), (42, 0.05), (42, 0.20)]
INIT_SEEDS = (0, 1, 2)
ITERS_LOSSY = 400
MLE_BUDGET_S = 900.0


def gen_fidelity(rho, sigma):
    """Generalized Uhlmann fidelity for subnormalized matrices
    (PR-64 round-2 metric; identical to exp20 routeB.gen_fidelity)."""
    rho = (rho + rho.conj().T) / 2
    sigma = (sigma + sigma.conj().T) / 2
    w, U = np.linalg.eigh(rho)
    sq = (U * np.sqrt(np.maximum(w, 0.0))) @ U.conj().T
    inner = sq @ sigma @ sq
    ev = np.maximum(np.linalg.eigvalsh((inner + inner.conj().T) / 2), 0.0)
    root = float(np.sum(np.sqrt(ev)))
    miss_r = max(0.0, 1.0 - float(np.trace(rho).real))
    miss_s = max(0.0, 1.0 - float(np.trace(sigma).real))
    return float((root + np.sqrt(miss_r * miss_s)) ** 2)


def score_lossy(st, eta_f, rho_t):
    """exp19 wide-intermediate scoring pipeline, generalized fidelity."""
    n_int, n_max = run19.N_INTERMEDIATE, run19.N_MAX
    rho_pre6 = np.zeros((n_int,) * 6, complex)
    for z, a, x in zip(st.z, st.alpha, st.xi):
        col = run19.ket_to_fock_wide(z, a, x, n_int)
        rho_pre6 += np.einsum("ijk,lmn->ijklmn", col, col.conj())
    rho_pre6 /= st.norm_sq()
    rho_out6 = run19.apply_loss_channel_wide(rho_pre6, eta_f, n_int)
    rho_f = rho_out6[:n_max, :n_max, :n_max,
                     :n_max, :n_max, :n_max].reshape(n_max ** 3, n_max ** 3)
    return gen_fidelity(rho_f, rho_t), float(np.trace(rho_f).real)


def main():
    print("=== exp21: issue #67 -- sigma_add / data-seed sweep of the "
          "thermal gate ===")
    print(f"configs (data_seed, sigma_add): {CONFIGS}; lossy R2K4 x init "
          f"seeds {INIT_SEEDS} best-by-train vs mle3 ({MLE_BUDGET_S:.0f}s); "
          f"generalized fidelity (PR-64 metric)", flush=True)
    out = dict(configs=[])
    verdicts = []
    for data_seed, sigma_add in CONFIGS:
        print(f"\n--- config: data seed {data_seed}, sigma_add "
              f"{sigma_add} ---", flush=True)
        target = ThermalLossyThreeModeCat(run19.ALPHA, run19.PARITY,
                                          run19.ETA, sigma_add)
        data = target.sample_homodyne(run19.GRID, run19.SHOTS, rng=data_seed)
        rho_t = thermal_lossy_cat3_fock(run19.ALPHA, run19.PARITY, run19.ETA,
                                        sigma_add, run19.N_MAX)
        trace_t = float(np.trace(rho_t).real)

        fits = []
        for s in INIT_SEEDS:
            t0 = time.perf_counter()
            st, eta_f = fit_bbdagS_lossy_mixed(
                data, R=2, K=4, M=3, eta0=run19.ETA, fit_eta=True,
                iters=ITERS_LOSSY, seed=s)
            nll = nll_lossy_mixed(st, data, eta_f)
            F, tr = score_lossy(st, eta_f, rho_t)
            fits.append(dict(seed=s, nll=float(nll), F=F, eta=float(eta_f),
                             model_trace=tr,
                             wall=round(time.perf_counter() - t0)))
            print(f"  lossy init {s}: F={F:.4f} eta'={eta_f:.4f} "
                  f"trainNLL={nll:.5f} (wall={fits[-1]['wall']}s)",
                  flush=True)
        rep = min(fits, key=lambda f: f["nll"])
        nlls = [f["nll"] for f in fits]
        Fs = [f["F"] for f in fits]
        nll_spread = max(nlls) - min(nlls)
        f_spread = max(Fs) - min(Fs)

        centers, targets_h = histogram_targets3(data, bins=run19.BINS)
        t0 = time.perf_counter()
        rho_m, iters, conv = mle3_reconstruct(centers, targets_h,
                                              n_max=run19.N_MAX,
                                              time_budget_s=MLE_BUDGET_S)
        F_mle = gen_fidelity(rho_m, rho_t)
        wall_m = round(time.perf_counter() - t0)
        verdict = bool(rep["F"] >= F_mle)
        verdicts.append(verdict)
        print(f"  representative (best train NLL): init {rep['seed']} "
              f"F={rep['F']:.4f}; NLL spread {nll_spread:.5f} vs "
              f"F spread {f_spread:.4f}")
        print(f"  mle3: F={F_mle:.4f} (converged={conv}, wall={wall_m}s)")
        print(f"  -> verdict: lossy {'>=' if verdict else '<'} mle "
              f"({rep['F']:.4f} vs {F_mle:.4f})", flush=True)
        out["configs"].append(dict(
            data_seed=data_seed, sigma_add=sigma_add, target_trace=trace_t,
            lossy_inits=fits, representative_seed=rep["seed"],
            F_lossy=rep["F"], eta=rep["eta"], F_mle=F_mle,
            mle_converged=bool(conv), mle_wall=wall_m,
            nll_spread=float(nll_spread), F_spread=float(f_spread),
            verdict_lossy_ge_mle=verdict))

    n_hold = sum(verdicts)
    out["ruling"] = dict(holds=n_hold, total=len(verdicts))
    print("\n=== sweep ruling (pre-declared reading, issue #67) ===")
    print(f"  verdict holds on {n_hold}/{len(verdicts)} configs")
    if n_hold == len(verdicts):
        print("-> all configs hold: the wording may add 'robust across 3 "
              "data seeds and a 4x sigma_add range' (one target class, "
              "exploratory -- unchanged).")
    else:
        print("-> at least one config flips: the README/preprint wording "
              "gains an exp16-style init-fragility note on the thermal "
              "gate, and the flipped configs are quoted.")

    path = pathlib.Path(__file__).parent / "results.json"
    path.write_text(json.dumps(out, indent=1))
    print(f"\nraw results -> {path}")


if __name__ == "__main__":
    main()
