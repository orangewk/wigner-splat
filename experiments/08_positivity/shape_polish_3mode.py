"""Experiment 08 (positivity) -- shape-polish follow-up, three modes.

penalty_then_project_3mode.py measured that fit3f_psd's WEIGHT-ONLY PSD
polish cannot satisfy falsification conditions (a) dF > -0.03 and (b)
min_eig >= -1e-9 jointly at 3 modes: killing negativity by weight alone
collapses fidelity 0.75 -> ~0.4 for every tried lambda_psd. Full per-splat
shape polish (28 params/splat) is FD-computationally infeasible, so that
result left a genuine confound: is the tension INTRINSIC to a 3-mode signed
splat, or is it an artifact of weight-only polish specifically starving the
fringe stripes of the shape freedom they'd need to redistribute negativity
without losing fidelity?

This script tests the oracle-recommended middle ground: fit3f_shape_psd
jointly FD-polishes the weights AND 3 GLOBAL fringe-shape scalars (stripe
thin-width multiplier, stripe base-width multiplier, stripe center-scale --
see wigner_splat.fit3f.apply_shape_knobs/fit3f_shape_psd's docstrings), at
the SAME lambda_psd sweep and falsification conditions, with a weight-only
(fit3f_psd) comparison row at each lambda for a direct answer:

  - shape+weight polish finds a lambda satisfying (a) AND (b)  -> shape
    freedom SAVES the reconstruction; weight-only starvation was a
    confound, and issue #8 updates toward "resolvable" at 3 modes.
  - it does not                                                -> the
    negative-eigenvalue mass is load-bearing regardless of shape freedom;
    the tension is more fundamental, strengthening "3-mode signed-splat
    fidelity and PSD physicality are in tension" as the #8 finding.

Either outcome is a result worth recording (the issue brief's own framing).

Same official condition as penalty_sweep_3mode.py / penalty_then_project_
3mode.py / observe_3mode.py. lambda_psd grid trimmed from the earlier
scripts' [0, 10, 50, 200] to [0, 20, 100] and shape_polish_iters kept small
(10) -- fit3f_shape_psd's docstring notes each shape-polish iteration costs
~(1 + 2*3) * S rho_component rebuilds (S = fringe-stripe splat count,
~14 at this condition) vs weight-only's O(K) SETUP + cheap-per-iteration
cost; a full [0,10,50,200] x 40-iters shape sweep is tens of minutes PER
point and was judged not worth the marginal precision for a confound probe
(deviation from the brief's example grid, recorded here per this repo's
convention of noting compute-budget trade-offs rather than silently
shrinking scope).
"""
import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fit3f import fit3f, fit3f_psd, fit3f_shape_psd  # noqa: E402
from wigner_splat.fock import cat3_fock  # noqa: E402
from wigner_splat.fock_project import psd_report, rho_from_splat  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA, PARITY, BINS, SHOTS, DATA_SEED = 1.5, +1, 24, 2000, 42
GRID = list(itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
))  # 27 triples, exp06 official
N_MAX_PSD = 8
DF_THRESHOLD, MIN_EIG_THRESHOLD = -0.03, -1e-9
LAMBDAS = [0.0, 20.0, 100.0]

WEIGHT_POLISH_ITERS, WEIGHT_POLISH_LR = 25, 0.02  # fit3f_psd (weight-only)
SHAPE_POLISH_ITERS, SHAPE_POLISH_LR, SHAPE_WEIGHT_LR = 10, 0.05, 0.02  # fit3f_shape_psd


def project_psd(rho):
    rho_h = (rho + rho.conj().T) / 2
    ev, U = np.linalg.eigh(rho_h)
    rho_p = (U * np.clip(ev, 0.0, None)) @ U.conj().T
    return rho_p / np.real(np.trace(rho_p))


def fidelity(rho, psi):
    return float(np.real(psi.conj() @ rho @ psi))


def _row(label, lam, mix, psi, f0, wall):
    rho = rho_from_splat(mix, N_MAX_PSD)
    r_pen = psd_report(rho)
    rho_p = project_psd(rho)
    r_proj = psd_report(rho_p)
    f_proj = fidelity(rho_p, psi)
    dF = f_proj - f0
    ok_a, ok_b = dF > DF_THRESHOLD, r_proj["min_eig"] >= MIN_EIG_THRESHOLD
    print(f"{label:>12} {lam:>7.1f} {fidelity(rho, psi):>8.4f} "
          f"{r_pen['min_eig']:>12.4e} {r_pen['negativity']:>9.4f} "
          f"{f_proj:>8.4f} {dF:>+9.4f} {r_proj['min_eig']:>13.4e} "
          f"{'yes' if ok_a else 'no':>4} {'yes' if ok_b else 'no':>4} "
          f"{'YES' if (ok_a and ok_b) else 'no':>5} {wall:>7.1f}s")
    return dict(label=label, lam=lam, dF=dF, min_eig_proj=r_proj["min_eig"],
                ok_a=ok_a, ok_b=ok_b)


def main():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    psi = cat3_fock(ALPHA, PARITY, N_MAX_PSD)
    print(f"3-mode cat alpha={ALPHA}, {len(GRID)} triples, {SHOTS} shots, "
          f"n_max_psd={N_MAX_PSD}. (a) dF>{DF_THRESHOLD}, (b) proj min_eig>="
          f"{MIN_EIG_THRESHOLD:.0e}")
    print(f"lambda grid={LAMBDAS}  weight-only iters={WEIGHT_POLISH_ITERS}  "
          f"shape+weight iters={SHAPE_POLISH_ITERS}\n")

    t0 = time.time()
    data = cat.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)
    mix0 = fit3f(data, bins=BINS)
    f0 = fidelity(rho_from_splat(mix0, N_MAX_PSD), psi)
    print(f"baseline F={f0:.4f}  K={len(mix0.w)}  "
          f"(fit3f+rho wall={time.time()-t0:.1f}s)\n")

    header = (f"{'method':>12} {'lambda':>7} {'F_pen':>8} {'min_eig_pen':>12} "
              f"{'neg_pen':>9} {'F_proj':>8} {'dF_proj':>9} "
              f"{'min_eig_proj':>13} {'(a)':>4} {'(b)':>4} {'both':>5} "
              f"{'wall_s':>7}")
    print(header)
    print("-" * len(header))

    rows = []
    for lam in LAMBDAS:
        t0 = time.time()
        mix_w = mix0 if lam == 0.0 else fit3f_psd(
            data, lambda_psd=lam, n_max_psd=N_MAX_PSD,
            psd_polish_iters=WEIGHT_POLISH_ITERS,
            psd_polish_lr=WEIGHT_POLISH_LR, bins=BINS)
        rows.append(_row("weight-only", lam, mix_w, psi, f0, time.time() - t0))

        t0 = time.time()
        mix_s = mix0 if lam == 0.0 else fit3f_shape_psd(
            data, lambda_psd=lam, n_max_psd=N_MAX_PSD,
            shape_polish_iters=SHAPE_POLISH_ITERS,
            shape_polish_lr=SHAPE_POLISH_LR,
            weight_polish_lr=SHAPE_WEIGHT_LR, bins=BINS)
        rows.append(_row("shape+weight", lam, mix_s, psi, f0, time.time() - t0))

    any_shape_both = any(r["ok_a"] and r["ok_b"] for r in rows
                         if r["label"] == "shape+weight" and r["lam"] > 0)
    any_weight_both = any(r["ok_a"] and r["ok_b"] for r in rows
                          if r["label"] == "weight-only" and r["lam"] > 0)

    print()
    print(f"weight-only satisfies (a) AND (b) at any swept lambda: "
          f"{'YES' if any_weight_both else 'no'}")
    print(f"shape+weight satisfies (a) AND (b) at any swept lambda: "
          f"{'YES' if any_shape_both else 'no'}")
    print()
    if any_shape_both:
        print("VERDICT: shape freedom SAVES the polish -- fit3f_shape_psd "
              "finds a lambda_psd where (a) and (b) hold jointly even "
              "though weight-only cannot. Weight-only starvation was a "
              "confound; issue #8 updates toward RESOLVABLE at 3 modes "
              "given a few global fringe-shape degrees of freedom.")
    else:
        print("VERDICT (negative result): even with 3 global fringe-shape "
              "knobs jointly polished with the weights, no swept lambda_psd "
              "satisfies (a) and (b) simultaneously. The negative-eigenvalue "
              "mass is load-bearing for 3-mode fidelity regardless of this "
              "shape freedom -- the physicality/fidelity tension is more "
              "fundamental than a weight-only-polish artifact (though a "
              "full 28-param/splat FD polish remains untested and "
              "computationally infeasible; see fit3f_psd's docstring).")


if __name__ == "__main__":
    main()
