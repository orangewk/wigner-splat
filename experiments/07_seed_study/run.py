"""Experiment 07: seed-bolstering study for issue #9.

Experiment 04 left the two-mode fidelity comparison "statistically tied": at
3000 shots/pair the fidelity gap between the full-covariance splat and the
product-Fock MLE (0.003-0.006) was smaller than the seed-to-seed noise
(0.015-0.018), so neither method was shown to truly win fidelity. Issue #9
asks: bolster the seed count to ~20 and settle whether MLE holds a small but
real fidelity edge or the two are genuinely tied.

Protocol (identical to experiment 04's 3000 shots/pair arm)
-----------------------------------------------------------
TwoModeCat alpha=1.5 parity=+1, 4x4 angle-pair grid over [0, pi)^2, 3000
shots/pair, bins=40 shared 2D histograms. For each of 20 data seeds
(rng = 0..19):

  splat: fit2f(data, bins=40)          -> fidelity_vs_cat   (timed)
  MLE:   histogram_targets2 + mle2_reconstruct(n_max=12)
                                        -> fidelity_pure     (timed, hist
                                           build inside the timed block, same
                                           fairness rule as experiment 04)

Statistics
----------
Per method: mean, std (population), min/max of fidelity. Paired per-seed
differences d_i = F_mle_i - F_splat_i: mean, std (ddof=1), a paired
t-statistic t = mean(d) / (std(d, ddof=1) / sqrt(n)) and its two-sided
p-value. The p-value is computed WITHOUT scipy via the regularized incomplete
beta function (Numerical Recipes continued fraction), the exact Student-t CDF;
the t_19 critical values 2.093 (5%) / 2.861 (1%) are also printed as a check.
Sign count (how many seeds MLE > splat) and wall-time stats for both methods
are reported.
"""

import itertools
import math
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from wigner_splat.data2 import histogram_targets2  # noqa: E402
from wigner_splat.fit2f import fit2f  # noqa: E402
from wigner_splat.fock import (  # noqa: E402
    cat2_fock,
    cat2_truncation_fidelity,
    fidelity_pure,
)
from wigner_splat.forward2f import fidelity_vs_cat  # noqa: E402
from wigner_splat.mle2 import mle2_reconstruct  # noqa: E402
from wigner_splat.states2 import TwoModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
N_MAX = 12
BINS = 40
BUDGET = 3000            # shots per angle pair (exp 04's 3000-shot arm)
SEEDS = list(range(20))  # rng = 0..19
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 4, endpoint=False),
    np.linspace(0, np.pi, 4, endpoint=False),
)]

# t-distribution 19-dof critical values (two-sided)
T19_CRIT_5 = 2.093
T19_CRIT_1 = 2.861


# ---------------------------------------------------------------------------
# Student-t two-sided p-value via the regularized incomplete beta function.
# No scipy: betacf is the Numerical Recipes continued fraction for I_x(a, b),
# and the two-sided t p-value is exactly I_{x}(nu/2, 1/2) with x = nu/(nu+t^2).

def _betacf(a, b, x, itmax=200, eps=3e-12):
    fpmin = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def _betai(a, b, x):
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    bt = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_sf_twosided(t, nu):
    """Two-sided Student-t p-value P(|T| >= |t|) for nu dof."""
    t = abs(float(t))
    if t == 0.0:
        return 1.0
    x = nu / (nu + t * t)
    return _betai(nu / 2.0, 0.5, x)


# ---------------------------------------------------------------------------

def main():
    cat = TwoModeCat(ALPHA, PARITY)
    psi = cat2_fock(ALPHA, PARITY, N_MAX)
    ceiling = cat2_truncation_fidelity(ALPHA, PARITY, N_MAX)

    print(f"experiment 07 (issue #9): seed-bolstering study, two-mode cat "
          f"alpha={ALPHA} parity={PARITY:+d}")
    print(f"{len(GRID)} angle pairs (4x4 over [0,pi)^2), n_max={N_MAX}, "
          f"bins={BINS}, budget={BUDGET} shots/pair")
    print(f"seeds = {SEEDS[0]}..{SEEDS[-1]}  (n={len(SEEDS)})")
    print(f"MLE truncation ceiling (Fock n_max={N_MAX}): {ceiling:.6f}\n")

    rows = []
    wall0 = time.perf_counter()
    for k, seed in enumerate(SEEDS):
        data = cat.sample_homodyne(GRID, BUDGET, rng=seed)

        # --- splat: fit2f(data) internally builds histogram_targets2 ---
        t0 = time.perf_counter()
        mix = fit2f(data, bins=BINS)
        t_splat = time.perf_counter() - t0
        f_splat = fidelity_vs_cat(mix, ALPHA, PARITY)

        # --- MLE: histogram build timed INSIDE the block, same work ---
        t0 = time.perf_counter()
        centers, targets = histogram_targets2(data, bins=BINS)
        rho, iters = mle2_reconstruct(centers, targets, n_max=N_MAX)
        t_mle = time.perf_counter() - t0
        f_mle = fidelity_pure(psi, rho)

        d = f_mle - f_splat
        rows.append(dict(seed=seed, f_splat=f_splat, t_splat=t_splat,
                         f_mle=f_mle, t_mle=t_mle, iters=iters, d=d))
        elapsed = time.perf_counter() - wall0
        print(f"[{k + 1:>2}/{len(SEEDS)} seed={seed:>2}] "
              f"F_splat={f_splat:.4f} ({t_splat:4.1f}s)  "
              f"F_mle={f_mle:.4f} ({t_mle:5.1f}s, {iters} it)  "
              f"d={d:+.4f}  | cum {elapsed:5.1f}s", flush=True)

    total_wall = time.perf_counter() - wall0

    fs = np.array([r["f_splat"] for r in rows])
    fm = np.array([r["f_mle"] for r in rows])
    ts = np.array([r["t_splat"] for r in rows])
    tm = np.array([r["t_mle"] for r in rows])
    dd = np.array([r["d"] for r in rows])
    n = len(rows)

    # ---- full per-seed table ----
    print("\n" + "=" * 78)
    print("per-seed table")
    hdr = (f"{'seed':>4} | {'F_splat':>8} {'t_splat':>8} | "
           f"{'F_mle':>8} {'t_mle':>8} {'iters':>5} | {'d=Fm-Fs':>9}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['seed']:>4} | {r['f_splat']:8.4f} {r['t_splat']:7.2f}s | "
              f"{r['f_mle']:8.4f} {r['t_mle']:7.2f}s {r['iters']:>5} | "
              f"{r['d']:+9.4f}")

    # ---- per-method statistics ----
    print("\n" + "=" * 78)
    print("per-method fidelity statistics (n = {})".format(n))
    print(f"{'method':>6} | {'mean':>8} {'std':>8} {'min':>8} {'max':>8}")
    print("-" * 46)
    print(f"{'splat':>6} | {fs.mean():8.4f} {fs.std():8.4f} "
          f"{fs.min():8.4f} {fs.max():8.4f}")
    print(f"{'MLE':>6} | {fm.mean():8.4f} {fm.std():8.4f} "
          f"{fm.min():8.4f} {fm.max():8.4f}")

    # ---- paired difference statistics ----
    d_mean = dd.mean()
    d_std = dd.std(ddof=1)                    # sample std
    se = d_std / math.sqrt(n)
    t_stat = d_mean / se
    nu = n - 1
    p_val = t_sf_twosided(t_stat, nu)
    ci_half = T19_CRIT_5 * se                 # 95% CI half-width (t_19)
    n_mle_gt = int(np.sum(dd > 0))
    n_splat_gt = int(np.sum(dd < 0))
    n_tie = int(np.sum(dd == 0))

    print("\n" + "=" * 78)
    print("paired per-seed difference  d_i = F_mle_i - F_splat_i")
    print(f"  mean(d)            = {d_mean:+.5f}")
    print(f"  std(d, ddof=1)     = {d_std:.5f}")
    print(f"  std error          = {se:.5f}")
    print(f"  95% CI (t_19)      = [{d_mean - ci_half:+.5f}, "
          f"{d_mean + ci_half:+.5f}]  (+-{ci_half:.5f})")
    print(f"  paired t (df={nu})   = {t_stat:+.4f}")
    print(f"  two-sided p-value  = {p_val:.4f}   "
          f"(incomplete-beta t-CDF, no scipy)")
    print(f"  t_19 crit: 5% = {T19_CRIT_5}  1% = {T19_CRIT_1}   "
          f"-> |t| {'>=' if abs(t_stat) >= T19_CRIT_5 else '<'} 2.093 "
          f"({'sig' if abs(t_stat) >= T19_CRIT_5 else 'n.s.'} at 5%)")
    print(f"  sign count: MLE>splat {n_mle_gt}/{n}, "
          f"splat>MLE {n_splat_gt}/{n}, tie {n_tie}/{n}")

    # ---- wall-time statistics ----
    speedup = tm.mean() / ts.mean()
    print("\n" + "=" * 78)
    print("wall-time statistics (seconds)")
    print(f"{'method':>6} | {'mean':>8} {'std':>8} {'min':>8} {'max':>8} "
          f"{'total':>9}")
    print("-" * 58)
    print(f"{'splat':>6} | {ts.mean():8.2f} {ts.std():8.2f} "
          f"{ts.min():8.2f} {ts.max():8.2f} {ts.sum():8.1f}s")
    print(f"{'MLE':>6} | {tm.mean():8.2f} {tm.std():8.2f} "
          f"{tm.min():8.2f} {tm.max():8.2f} {tm.sum():8.1f}s")
    print(f"  MLE / splat mean compute ratio = {speedup:.1f}x")
    print(f"  total sweep wall time = {total_wall:.1f}s")

    # ---- verdict ----
    sig5 = abs(t_stat) >= T19_CRIT_5
    print("\n" + "=" * 78)
    print("VERDICT (issue #9: is the fidelity difference significant at 5%?)")
    if sig5:
        winner = "MLE" if d_mean > 0 else "splat"
        print(f"  YES -- significant at 5% (|t|={abs(t_stat):.3f} >= 2.093, "
              f"p={p_val:.4f}).")
        print(f"  {winner} edges fidelity by {abs(d_mean):.4f} +- "
              f"{ci_half:.4f} (95% CI), at {speedup:.0f}x the compute "
              f"({tm.mean():.0f}s vs {ts.mean():.0f}s per seed).")
        print(f"  Practical: the fidelity edge is real but tiny; splat buys "
              f"~equal quality for ~1/{speedup:.0f} the cost.")
    else:
        print(f"  NO -- not significant at 5% (|t|={abs(t_stat):.3f} < 2.093, "
              f"p={p_val:.4f}).")
        print(f"  TIE CONFIRMED: mean gap {d_mean:+.4f} (95% CI includes 0: "
              f"[{d_mean - ci_half:+.4f}, {d_mean + ci_half:+.4f}]).")
        print(f"  splat matches MLE fidelity at {speedup:.0f}x less compute "
              f"({ts.mean():.0f}s vs {tm.mean():.0f}s per seed) -- the "
              f"computational gain stands.")

    # ---- figure ----
    outdir = pathlib.Path(__file__).resolve().parent / "out"
    outdir.mkdir(parents=True, exist_ok=True)
    figpath = outdir / "seed_study.png"

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    # panel 1: slope-graph, splat vs MLE per seed
    x_s, x_m = 0.0, 1.0
    for r in rows:
        color = "#c0392b" if r["f_mle"] > r["f_splat"] else "#2471a3"
        ax1.plot([x_s, x_m], [r["f_splat"], r["f_mle"]], "-",
                 color=color, alpha=0.45, lw=1.2, zorder=1)
    ax1.scatter([x_s] * n, fs, s=42, color="#2471a3", zorder=3,
                label="splat", edgecolor="white", linewidth=0.6)
    ax1.scatter([x_m] * n, fm, s=42, color="#c0392b", zorder=3,
                label="MLE", edgecolor="white", linewidth=0.6)
    ax1.plot([x_s - 0.18, x_s + 0.05], [fs.mean(), fs.mean()], "-",
             color="#154360", lw=2.5, zorder=4)
    ax1.plot([x_m - 0.05, x_m + 0.18], [fm.mean(), fm.mean()], "-",
             color="#7b241c", lw=2.5, zorder=4)
    ax1.text(x_s - 0.20, fs.mean(), f"{fs.mean():.4f}", ha="right",
             va="center", fontsize=9, color="#154360")
    ax1.text(x_m + 0.20, fm.mean(), f"{fm.mean():.4f}", ha="left",
             va="center", fontsize=9, color="#7b241c")
    ax1.set_xlim(-0.55, 1.55)
    ax1.set_xticks([x_s, x_m])
    ax1.set_xticklabels(["splat", "MLE"])
    ax1.set_ylabel("fidelity")
    ax1.set_title(f"Paired per-seed fidelity, n={n} seeds\n"
                  f"(red = MLE>splat, blue = splat>MLE; thick = mean)",
                  fontsize=10)
    ax1.legend(loc="lower center", ncol=2, fontsize=9)
    ax1.grid(axis="y", alpha=0.3)

    # panel 2: histogram of paired differences with zero line and mean +- CI
    ax2.hist(dd, bins=10, color="#95a5a6", edgecolor="white", alpha=0.85)
    ax2.axvline(0.0, color="black", lw=1.5, ls="-", label="zero (tie)")
    ax2.axvline(d_mean, color="#c0392b", lw=2.0,
                label=f"mean d = {d_mean:+.4f}")
    ax2.axvspan(d_mean - ci_half, d_mean + ci_half, color="#c0392b",
                alpha=0.15, label=f"95% CI +-{ci_half:.4f}")
    ax2.set_xlabel("d = F_mle - F_splat  (per seed)")
    ax2.set_ylabel("count")
    verdict = ("significant" if sig5 else "n.s.") + " at 5%"
    ax2.set_title(f"Paired differences   t_{nu}={t_stat:+.2f}, "
                  f"p={p_val:.3f} ({verdict})\n"
                  f"MLE>splat in {n_mle_gt}/{n} seeds", fontsize=10)
    ax2.legend(loc="upper right", fontsize=8)
    ax2.grid(axis="y", alpha=0.3)

    fig.suptitle(
        f"Experiment 07 (issue #9): seed-bolstering study, two-mode cat "
        f"alpha={ALPHA}, {BUDGET} shots/pair, seeds 0-{SEEDS[-1]}",
        fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(figpath, dpi=130)
    print(f"\nfigure written to {figpath}")

    return rows, dict(
        fs=fs, fm=fm, ts=ts, tm=tm, dd=dd, d_mean=d_mean, d_std=d_std,
        se=se, t_stat=t_stat, p_val=p_val, ci_half=ci_half,
        n_mle_gt=n_mle_gt, speedup=speedup, sig5=sig5, ceiling=ceiling,
        total_wall=total_wall)


if __name__ == "__main__":
    main()
