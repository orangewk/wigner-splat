"""Experiment 17 -- issue #42: the noise-aware vs noise-ignorant control.

The loss forward model is now deployed across every reconstructor (bbdagS in
exp13; bbdagM / purefock3 / splat in this PR). This experiment measures, on
synthetic data with KNOWN detector noise, (a) the systematic error of
ignoring the noise, (b) how much of it the known-eta forward correction
recovers, and (c) how close jointly-FITTED eta comes to the known-eta fit --
the controlled comparison the issue scoped.

PROTOCOL (declared before the run):
  * target: pure three-mode cat, alpha = 1.5, parity = +1 (exactly in-family
    for bbdagM K=2; exp06/exp11 conventions).
  * detector: eta = 0.8, electronic noise variance 0.02 -- applied to ideal
    samples by data3.apply_detection_noise (measured x = sqrt(eta) x +
    N(0, (1-eta)/2 + 0.02)). Data: 3x3x3 angle triples x 1000 shots, data
    seed 42 (noise stream seed 1042). Small-scale by design (the issue asks
    for a small controlled log, not a benchmark).
  * conditions per reconstructor -- IGNORE (pure model on noisy data),
    KNOWN (lossy model, true eta and noise given, eta not fitted), and for
    the bbdag family FITTED (eta fitted from a deliberately wrong start
    0.6, electronic noise still given):
      - bbdagM  K=2: fit_bbdagM iters=200 | fit_bbdagM_lossy iters=300,
        fit_eta False / True. Init seeds {0,1,2}.
      - purefock3 n_max=8: fit_purefock3 iters=1000 | fit_purefock3_lossy
        iters=600 (the lossy path costs more per iteration; the asymmetry
        disadvantages the AWARE arm, so it is conservative for the claim
        that awareness helps). Init seeds {0,1,2}.
      - splat fit3f: default staged fit | eta/extra passed through.
        Deterministic (no init seed).
  * representative fit per condition: best TRAIN objective across init
    seeds (NLL for the likelihood fits at the condition's own eta;
    histogram loss for splat) -- never selected on fidelity.
  * metrics: exact state fidelity vs the pure cat (closed form for bbdagM;
    truncation-corrected for purefock3). The splat number is the Wigner
    overlap score (non-PSD representation, separate axis, perfect = 1 on
    this pure target). Fitted eta values are recorded.
  * declared readings: IGNORE arms should show a systematic deficit; KNOWN
    arms should recover most of it (the noise-aware model estimates the
    PRE-loss state); FITTED eta should land near 0.8 with fidelity close
    to the KNOWN arm. Descriptive, single data seed -- no significance
    claims.
"""
import itertools
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat import bbdagM  # noqa: E402
from wigner_splat import purefock3  # noqa: E402
from wigner_splat.data3 import apply_detection_noise  # noqa: E402
from wigner_splat.fit3f import fit3f, loss3f  # noqa: E402
from wigner_splat.forward3f import fidelity_vs_cat3 as splat_score  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
ETA = 0.8
EXTRA = 0.02
SHOTS = 1000
DATA_SEED = 42
INIT_SEEDS = [0, 1, 2]
N_MAX = 8
BINS = 24
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]


def best_of(fits):
    """fits: [(train_objective, payload)] -> payload of the lowest objective."""
    return min(fits, key=lambda t: t[0])


def main():
    print("=== exp17: issue #42 -- noise-aware vs noise-ignorant control ===")
    print(f"target: pure cat3 alpha={ALPHA} parity={PARITY}; detector "
          f"eta={ETA} extra_noise_var={EXTRA}; {len(GRID)} triples x "
          f"{SHOTS} shots, data seed {DATA_SEED}", flush=True)

    target = ThreeModeCat(ALPHA, PARITY)
    ideal = target.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)
    data = apply_detection_noise(ideal, ETA, EXTRA, rng=DATA_SEED + 1000)
    rows = []

    # ---------------------------------------------------------- bbdagM ----
    print("\n--- bbdagM K=2 ---", flush=True)
    fits = []
    for s in INIT_SEEDS:
        t0 = time.perf_counter()
        st = bbdagM.fit_bbdagM(data, K=2, M=3, iters=200, seed=s)
        w = time.perf_counter() - t0
        fits.append((bbdagM.nll(st, data), (st, None, w, s)))
    st, _, w, s = best_of(fits)[1]
    F = bbdagM.fidelity_vs_cat3(st, ALPHA, PARITY)
    rows.append(("bbdagM", "ignore", F, None, w, s))
    print(f"  ignore  F={F:.4f} (init {s}, wall={w:.0f}s)", flush=True)

    for label, fit_eta, eta0 in (("known", False, ETA), ("fitted", True, 0.6)):
        fits = []
        for s in INIT_SEEDS:
            t0 = time.perf_counter()
            st, eta_f = bbdagM.fit_bbdagM_lossy(
                data, K=2, M=3, eta0=eta0, fit_eta=fit_eta,
                extra_noise_var=EXTRA, iters=300, seed=s)
            w = time.perf_counter() - t0
            fits.append((bbdagM.nll_lossy(st, data, eta_f, EXTRA),
                         (st, eta_f, w, s)))
        st, eta_f, w, s = best_of(fits)[1]
        F = bbdagM.fidelity_vs_cat3(st, ALPHA, PARITY)
        rows.append(("bbdagM", label, F, eta_f, w, s))
        print(f"  {label:7s} F={F:.4f} eta={eta_f:.4f} (init {s}, "
              f"wall={w:.0f}s)", flush=True)

    # -------------------------------------------------------- purefock3 ----
    print("\n--- purefock3 n_max=8 ---", flush=True)
    fits = []
    for s in INIT_SEEDS:
        t0 = time.perf_counter()
        pf = purefock3.fit_purefock3(data, n_max=N_MAX, iters=1000, seed=s)
        w = time.perf_counter() - t0
        fits.append((purefock3.nll_psi(pf, data), (pf, w, s)))
    pf, w, s = best_of(fits)[1]
    _, F = purefock3.fidelity_vs_cat3(pf, ALPHA, PARITY)
    rows.append(("purefock3", "ignore", F, None, w, s))
    print(f"  ignore  F={F:.4f} (init {s}, wall={w:.0f}s)", flush=True)

    fits = []
    for s in INIT_SEEDS:
        t0 = time.perf_counter()
        pf = purefock3.fit_purefock3_lossy(data, n_max=N_MAX, eta=ETA,
                                           extra_noise_var=EXTRA, iters=600,
                                           seed=s)
        w = time.perf_counter() - t0
        fits.append((purefock3.lossy_nll_psi(pf, data, ETA, EXTRA),
                     (pf, w, s)))
    pf, w, s = best_of(fits)[1]
    _, F = purefock3.fidelity_vs_cat3(pf, ALPHA, PARITY)
    rows.append(("purefock3", "known", F, None, w, s))
    print(f"  known   F={F:.4f} (init {s}, wall={w:.0f}s)", flush=True)

    # ------------------------------------------------------------ splat ----
    print("\n--- splat fit3f ---", flush=True)
    from wigner_splat.data3 import histogram_targets3
    centers, targets_h = histogram_targets3(data, bins=BINS)
    for label, kw in (("ignore", {}),
                      ("known", dict(eta=ETA, extra_noise_var=EXTRA))):
        t0 = time.perf_counter()
        mix = fit3f(data, bins=BINS, **kw)
        w = time.perf_counter() - t0
        score = splat_score(mix, ALPHA, PARITY)
        hloss = loss3f(mix, centers, targets_h, **kw)
        rows.append(("splat", label, score, None, w, None))
        print(f"  {label:7s} overlap-score={score:.4f} (non-PSD axis; "
              f"hist-loss={hloss:.3e}, wall={w:.0f}s)", flush=True)

    # ---------------------------------------------------------- summary ----
    out = pathlib.Path(__file__).parent / "results.json"
    out.write_text(json.dumps(
        [dict(method=m, condition=c, value=v, eta=e, wall_s=w, init=s)
         for m, c, v, e, w, s in rows], indent=1))
    print(f"\nraw results -> {out}")
    print("\n=== summary (fidelity axis; splat = overlap score, separate "
          "axis) ===")
    for m, c, v, e, w, s in rows:
        eta_s = f" eta={e:.4f}" if e is not None else ""
        print(f"  {m:10s} {c:7s} {v:.4f}{eta_s}")
    print("\nreadings (declared in the docstring): ignore-arm deficit vs "
          "known-arm recovery vs fitted-eta gap; single data seed, "
          "descriptive only.")


if __name__ == "__main__":
    main()
