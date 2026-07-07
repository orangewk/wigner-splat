"""Experiment 04: full-covariance splat vs product-Fock MLE at TWO modes.

This is the decisive scaling test the README's falsification condition points
to. At one mode (experiment 03) the verdict was: splat wins fidelity, MLE wins
speed -> no computational gain, so the surviving hypothesis was SCALING. The
Fock MLE dimension grows as n_max**modes while the splat parameter count stays
O(K). Two modes is the first place that can be tested: if the splat loses BOTH
fidelity and speed here too, the README commits to abandoning the approach.

Both reconstructors consume the IDENTICAL binned histograms
(data2.histogram_targets2, bins=40) of the same TwoModeCat homodyne data on a
4x4 angle-pair grid over [0, pi)^2, across two shot budgets x three data seeds.

Timing / fairness note
----------------------
fit2f(data) takes RAW data but internally calls histogram_targets2(data,
bins=40); mle2_reconstruct takes (centers, targets). To keep the comparison
fair, the 2D histogram build is timed on BOTH sides: the splat call includes it
internally, and on the MLE side histogram_targets2 is called INSIDE the timed
block. So both wall-clock numbers include identical binning work. Both run
single-threaded numpy in the same process (fit2f is deterministic given data;
mle2 is deterministic given the histograms).

Fidelity is the same definition on both sides (tr(rho_recon rho_cat)):
  splat -> fidelity_vs_cat (closed-form 4D Wigner overlap),
  MLE   -> fidelity_pure(cat2_fock, rho) = <psi|rho|psi>.

Wigner minimum is read on the (p1, p2) plane at x1 = x2 = 0, where the
entangled fringe cos(2 sqrt2 a (p1 + p2)) drives the negativity. The splat side
evaluates the 4D mixture directly (wigner4); the MLE side uses the two-mode
displaced-parity slice helper below, validated once against states2 at startup.
"""

import itertools
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
    _genlaguerre,
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
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 4, endpoint=False),
    np.linspace(0, np.pi, 4, endpoint=False),
)]
BUDGETS = [1000, 3000]   # shots per angle pair
SEEDS = [42, 0, 7]

# (p1, p2) plane at x1 = x2 = 0 for the Wigner minimum / figure
PG = np.linspace(-2.8, 2.8, 121)


# ---------------------------------------------------------------------------
# Two-mode displaced-parity Wigner slice for a product-Fock density matrix.
# Kept in the experiment file (not the library) per the task's instruction.

def _displacement_matrix(b, n_max):
    """<m|D(b)|n> for each scalar in b: (len(b), n_max, n_max) complex.

    Same closed form used inside fock.wigner_from_rho:
      m >= n: sqrt(n!/m!) b^{m-n} e^{-|b|^2/2} L_n^{(m-n)}(|b|^2)
      m <  n: sqrt(m!/n!) (-b*)^{n-m} e^{-|b|^2/2} L_m^{(n-m)}(|b|^2)
    """
    b = np.atleast_1d(np.asarray(b, complex))
    A = len(b)
    y = np.abs(b) ** 2                                  # (A,)
    env = np.exp(-y / 2)
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    D = np.zeros((A, n_max, n_max), complex)
    for d in range(n_max):                              # d = |m - n|
        L = _genlaguerre(n_max - d, d, y)               # (n_max-d, A)
        bd = b ** d
        mbcd = (-np.conj(b)) ** d
        for n_ in range(n_max - d):
            m_ = n_ + d
            amp = np.exp((log_fact[n_] - log_fact[m_]) / 2)
            D[:, m_, n_] = amp * bd * env * L[n_]        # lower (m>=n)
            if d > 0:
                D[:, n_, m_] = amp * mbcd * env * L[n_]  # upper (m<n)
    return D


def _parity_kernel(pg, n_max):
    """K[a, c, r] = (-1)^r <c|D(2a_c)|r> at x = 0, a_c = i p / sqrt2, over pg.

    This is the single-mode displaced-parity kernel implicit in
    fock.wigner_from_rho, so that W_single = (1/pi) sum_{r,c} rho[r,c] K[c,r].
    """
    b = np.sqrt(2.0) * (1j * np.asarray(pg, float))     # 2 a_c with x = 0
    D = _displacement_matrix(b, n_max)                  # (A, n_max, n_max)
    par = (-1.0) ** np.arange(n_max)
    return D * par[None, None, :]                       # weight the row index


def wigner_slice_pp(rho, pg, n_max):
    """W(x1=0, p1, x2=0, p2) = (1/pi^2) tr[rho kron(K1, K2)] on the pg x pg grid.

    rho is the product-Fock density matrix (flat index m*n_max + n = |m>|n>).
    Reshape to R[m, q, n, r] = rho[(m mode1 row, q mode2 row),
    (n mode1 col, r mode2 col)] and contract the per-gridpoint 12x12 kernels
    K1 (A,12,12), K2 (B,12,12):

        W[a, b] = (1/pi^2) Re einsum('mqnr,anm,brq->ab', R, K1, K2).
    """
    R = rho.reshape(n_max, n_max, n_max, n_max)
    K = _parity_kernel(pg, n_max)
    W = np.einsum("mqnr,anm,brq->ab", R, K, K, optimize=True)
    return np.real(W) / np.pi ** 2


def validate_slice(n_max=20):
    """allclose(atol 1e-6) of the helper vs states2.TwoModeCat.wigner on a
    coarse grid, using rho = outer(cat2_fock, cat2_fock).

    This checks the KERNEL math, so rho must be a faithful cat: at the run's
    N_MAX=12 the pure Fock truncation error is ~1e-4 (the state is genuinely
    missing amplitude, nothing to do with the helper), so the validation uses
    n_max=20 where truncation is ~3e-8 and the 1e-6 tolerance isolates the
    kernel. The identical helper is then used at N_MAX=12 for the MLE rho.
    """
    psi = cat2_fock(ALPHA, PARITY, n_max)
    rho = np.outer(psi, psi.conj())
    coarse = np.linspace(-2.8, 2.8, 15)
    W_helper = wigner_slice_pp(rho, coarse, n_max)
    P1, P2 = np.meshgrid(coarse, coarse, indexing="ij")
    cat = TwoModeCat(ALPHA, PARITY)
    W_true = cat.wigner(0.0, P1, 0.0, P2)
    ok = np.allclose(W_helper, W_true, atol=1e-6)
    return ok, float(np.abs(W_helper - W_true).max())


# ---------------------------------------------------------------------------

def main():
    cat = TwoModeCat(ALPHA, PARITY)
    psi = cat2_fock(ALPHA, PARITY, N_MAX)
    ceiling = cat2_truncation_fidelity(ALPHA, PARITY, N_MAX)

    print(f"experiment 04: two-mode cat alpha={ALPHA} parity={PARITY:+d}, "
          f"{len(GRID)} angle pairs (4x4 over [0,pi)^2), n_max={N_MAX}")
    print(f"budgets={BUDGETS} shots/pair, seeds={SEEDS}, bins={BINS}")
    print(f"MLE truncation ceiling (Fock n_max={N_MAX}): {ceiling:.6f}\n")

    ok, maxdev = validate_slice()
    print(f"Wigner-slice helper validation vs states2.TwoModeCat.wigner "
          f"(faithful n_max=20 rho): allclose(atol=1e-6) = {ok}  "
          f"(max |dev| = {maxdev:.2e})\n")

    P1, P2 = np.meshgrid(PG, PG, indexing="ij")
    W_true_pp = cat.wigner(0.0, P1, 0.0, P2)

    rows = []
    saved = {}   # (budget, seed) -> (mix, rho) for the figure
    for budget in BUDGETS:
        for seed in SEEDS:
            print(f"[budget={budget:>4} seed={seed:>2}] generating data ...",
                  flush=True)
            data = cat.sample_homodyne(GRID, budget, rng=seed)

            # --- splat: fit2f(data) internally builds histogram_targets2 ---
            print(f"[budget={budget:>4} seed={seed:>2}] fitting splat ...",
                  flush=True)
            t0 = time.perf_counter()
            mix = fit2f(data, bins=BINS)
            t_splat = time.perf_counter() - t0
            f_splat = fidelity_vs_cat(mix, ALPHA, PARITY)
            W_splat = mix.wigner4(0.0, P1, 0.0, P2)
            wmin_splat = float(W_splat.min())

            # --- MLE: histogram build timed INSIDE the block, same work ---
            print(f"[budget={budget:>4} seed={seed:>2}] running MLE ...",
                  flush=True)
            t0 = time.perf_counter()
            centers, targets = histogram_targets2(data, bins=BINS)
            rho, iters = mle2_reconstruct(centers, targets, n_max=N_MAX)
            t_mle = time.perf_counter() - t0
            f_mle = fidelity_pure(psi, rho)
            W_mle = wigner_slice_pp(rho, PG, N_MAX)
            wmin_mle = float(W_mle.min())

            print(f"[budget={budget:>4} seed={seed:>2}] "
                  f"F_splat={f_splat:.4f} ({t_splat:.1f}s)  "
                  f"F_mle={f_mle:.4f} ({t_mle:.1f}s, {iters} it)\n",
                  flush=True)

            rows.append(dict(budget=budget, seed=seed, f_splat=f_splat,
                             t_splat=t_splat, wmin_splat=wmin_splat,
                             f_mle=f_mle, t_mle=t_mle, iters=iters,
                             wmin_mle=wmin_mle))
            saved[(budget, seed)] = (mix, rho)

    # ---- per-run table ----
    print("=" * 96)
    print(f"true (p1,p2)@x=0 Wigner min: {W_true_pp.min():.3f}   "
          f"MLE ceiling: {ceiling:.6f}\n")
    hdr = (f"{'budget':>6} {'seed':>4} | {'F_splat':>7} {'t_splat':>8} "
           f"{'Wmin_s':>7} | {'F_mle':>7} {'t_mle':>8} {'iters':>5} {'Wmin_m':>7}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['budget']:>6} {r['seed']:>4} | "
              f"{r['f_splat']:7.4f} {r['t_splat']:7.2f}s {r['wmin_splat']:7.3f} | "
              f"{r['f_mle']:7.4f} {r['t_mle']:7.2f}s {r['iters']:>5} "
              f"{r['wmin_mle']:7.3f}")

    # ---- per-budget mean summary ----
    print("\nper-budget means (over seeds " + ", ".join(map(str, SEEDS)) + "):")
    sub = "budget"
    print(f"{sub:>6} | {'F_splat':>16} {'t_splat':>8} | "
          f"{'F_mle':>16} {'t_mle':>8}")
    print("-" * 62)
    means = {}
    for budget in BUDGETS:
        br = [r for r in rows if r["budget"] == budget]
        fs = np.array([r["f_splat"] for r in br])
        ts = np.array([r["t_splat"] for r in br])
        fm = np.array([r["f_mle"] for r in br])
        tm = np.array([r["t_mle"] for r in br])
        means[budget] = dict(fs=fs.mean(), fs_sd=fs.std(), ts=ts.mean(),
                             fm=fm.mean(), fm_sd=fm.std(), tm=tm.mean())
        print(f"{budget:>6} | {fs.mean():7.4f}+-{fs.std():.4f} {ts.mean():7.2f}s | "
              f"{fm.mean():7.4f}+-{fm.std():.4f} {tm.mean():7.2f}s")

    # ---- verdict block (mirrors exp 03; on per-budget MEANS) ----
    print("\nverdict per budget (falsification: splat must win BOTH):")
    for budget in BUDGETS:
        m = means[budget]
        fid = "splat" if m["fs"] > m["fm"] else "MLE"
        spd = "splat" if m["ts"] < m["tm"] else "MLE"
        both = "PASS" if (fid == "splat" and spd == "splat") else "FAIL"
        # honest noise note on the fidelity comparison
        diff = abs(m["fs"] - m["fm"])
        noise = m["fs_sd"] + m["fm_sd"]
        note = ""
        if diff < noise:
            note = (f"  [fidelity gap {diff:.4f} < seed noise {noise:.4f} "
                    f"-> WITHIN NOISE, not decisive]")
        print(f"  {budget:>5} shots/pair: fidelity -> {fid} "
              f"(splat {m['fs']:.4f} vs MLE {m['fm']:.4f}), "
              f"speed -> {spd} "
              f"(splat {m['ts']:.1f}s vs MLE {m['tm']:.1f}s)  [{both}]{note}")

    print("\ninterpretation: the surviving hypothesis was SCALING -- Fock MLE "
          f"dimension n_max^modes = {N_MAX}^2 = {N_MAX**2} here. If the splat "
          "wins BOTH fidelity and speed at two modes, the scaling advantage is "
          "real; if it loses both, the README abandons the approach.")

    # ---- figure: 3000-shot rng=42 run ----
    fig_budget, fig_seed = 3000, 42
    mix, rho = saved[(fig_budget, fig_seed)]
    fr = next(r for r in rows if r["budget"] == fig_budget and r["seed"] == fig_seed)
    W_splat_pp = mix.wigner4(0.0, P1, 0.0, P2)
    W_mle_pp = wigner_slice_pp(rho, PG, N_MAX)

    # shared symmetric RdBu scale across the three (p1,p2) panels
    vmax = max(np.abs(W_true_pp).max(), np.abs(W_splat_pp).max(),
               np.abs(W_mle_pp).max())
    ext = [PG[0], PG[-1], PG[0], PG[-1]]

    # fourth panel: (x1,x2)@p=0 splat reconstruction (its own plane / scale)
    XG = np.linspace(-3.5, 3.5, 121)
    X1, X2 = np.meshgrid(XG, XG, indexing="ij")
    W_splat_xx = mix.wigner4(X1, 0.0, X2, 0.0)
    vmax_xx = np.abs(W_splat_xx).max()
    ext_xx = [XG[0], XG[-1], XG[0], XG[-1]]

    fig, ax = plt.subplots(1, 4, figsize=(17, 4.4))
    panels = [
        (ax[0], W_true_pp, f"true W(p1,p2)@x=0", ext, vmax),
        (ax[1], W_splat_pp,
         f"splat  F={fr['f_splat']:.4f}  {fr['t_splat']:.1f}s", ext, vmax),
        (ax[2], W_mle_pp,
         f"MLE  F={fr['f_mle']:.4f}  {fr['t_mle']:.1f}s", ext, vmax),
    ]
    for a, W, title, extent, vm in panels:
        im = a.imshow(W.T, origin="lower", extent=extent, cmap="RdBu_r",
                      vmin=-vm, vmax=vm, aspect="equal")
        a.set_title(title, fontsize=11)
        a.set_xlabel("p1")
        a.set_ylabel("p2")
        fig.colorbar(im, ax=a, fraction=0.046, pad=0.04)

    im = ax[3].imshow(W_splat_xx.T, origin="lower", extent=ext_xx, cmap="RdBu_r",
                      vmin=-vmax_xx, vmax=vmax_xx, aspect="equal")
    ax[3].set_title("splat  W(x1,x2)@p=0", fontsize=11)
    ax[3].set_xlabel("x1")
    ax[3].set_ylabel("x2")
    fig.colorbar(im, ax=ax[3], fraction=0.046, pad=0.04)

    fig.suptitle(
        f"Two-mode cat alpha={ALPHA}: Wigner slices, {fig_budget} shots/pair, "
        f"seed {fig_seed}  (first 3 panels share RdBu scale)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    outdir = pathlib.Path(__file__).resolve().parent / "out"
    outdir.mkdir(parents=True, exist_ok=True)
    figpath = outdir / "two_mode_wigner.png"
    fig.savefig(figpath, dpi=130)
    print(f"\nfigure written to {figpath}")


if __name__ == "__main__":
    main()
