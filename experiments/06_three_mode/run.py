"""Experiment 06: the final verdict of the three-mode scaling campaign.

This is the decisive scaling point of issue #7. The campaign's logic, one mode
at a time:

  * 1 mode (exp 03): splat wins FIDELITY, product-Fock MLE wins SPEED (2x) ->
    no net computational gain, the surviving hypothesis was SCALING.
  * 2 modes (exp 04 / 07): 144-dim Fock, ~32 s/seed MLE, fidelity TIE (paired
    t, p=0.121), splat ~7.4x faster. Scaling advantage begins to bite.
  * 3 modes (HERE): 512-dim Fock (n_max=8). n_max^modes explodes while the
    full-covariance splat stays O(K) at 28 params/splat. If the Fock MLE simply
    cannot finish, THAT is the result -- measured honestly, not by crippling
    either side.

Both reconstructors consume the IDENTICAL binned histograms
(data3.histogram_targets3, bins=24) of the same ThreeModeCat homodyne data on
the official 3x3x3 angle grid over [0, pi)^3, 2000 shots/triple.

Budget dictates the asymmetry, and we state it plainly: the splat (fit3f) is a
deterministic ~15 s solve, so all three data seeds (42, 1, 2) are run. The MLE
is a ~0.7 s/iteration fixed point that does NOT converge in a 15-minute wall
budget (underdetermined: ~17.7k histogram rows vs 262k density-matrix params),
so it is run for seed 42 ONLY, to a 900 s soft wall clock, with its full
fidelity-vs-walltime trajectory recorded. The killer metric is "time to
splat-quality": the wall time at which the MLE fidelity trajectory first
crosses the splat's final fidelity for the same seed -- if it ever does.

Fidelity is the same tr(rho_recon rho_cat3) on both sides:
  splat -> fidelity_vs_cat3 (closed-form 6D Wigner overlap),
  MLE   -> fidelity_pure(cat3_fock, rho) = <psi|rho|psi>.

The Wigner minimum / figure slice is read on the (p1, p2) plane at
x1=x2=x3=0, p3=0, where the entangled fringe cos(2 sqrt2 a (p1+p2+p3))
reduces to cos(2 sqrt2 a (p1+p2)) and drives the negativity. The splat side
evaluates the 6D mixture directly (wigner6); the MLE side uses the three-mode
displaced-parity slice helper below, validated once against states3 at startup.

Threading note: the whole script is pinned to single-threaded BLAS
(OMP/OPENBLAS/MKL/NUMEXPR = 1, set BEFORE importing numpy). fit3f is a batch of
many small 3x3/6x6 solves and per-triple 24^3 tensors; multithreaded BLAS
OVERSUBSCRIBES on these and runs SLOWER (measured: single-thread fit3f ~15 s,
faster than multithreaded). The MLE's one big (M x 512) BLAS call per iteration
is likewise stable single-threaded. Pinning also makes both walls reproducible.
"""

import os

# Pin BLAS to one thread BEFORE numpy is imported (see module docstring).
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from wigner_splat.data3 import histogram_targets3  # noqa: E402
from wigner_splat.fit3f import fit3f  # noqa: E402
from wigner_splat.fock import (  # noqa: E402
    _genlaguerre,
    cat3_fock,
    cat3_truncation_fidelity,
    fidelity_pure,
)
from wigner_splat.forward3f import fidelity_vs_cat3  # noqa: E402
from wigner_splat.mle3 import mle3_reconstruct  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
BINS = 24
N_MAX = 8            # MLE Fock cutoff per mode -> 512 dims (ceiling ~0.99321)
SHOTS = 2000        # per angle triple
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]                  # 3x3x3 = 27 triples over [0, pi)^3
SEEDS = [42, 1, 2]  # splat: all three; MLE: seed 42 only (budget)
MLE_SEED = 42
MLE_BUDGET_S = 900  # 15-minute soft wall clock for the DNF measurement

# (p1, p2) plane at x1=x2=x3=0, p3=0 for the Wigner minimum / figure
PG = np.linspace(-2.8, 2.8, 101)


# ---------------------------------------------------------------------------
# Three-mode displaced-parity Wigner slice for a product-Fock density matrix.
# The 3-mode lift of exp04's validated two-mode helper. Kept in the experiment
# file (not the library), as the task instructs.

def _displacement_matrix(b, n_max):
    """<m|D(b)|n> for each scalar in b: (len(b), n_max, n_max) complex.

    Same closed form used inside fock.wigner_from_rho:
      m >= n: sqrt(n!/m!) b^{m-n} e^{-|b|^2/2} L_n^{(m-n)}(|b|^2)
      m <  n: sqrt(m!/n!) (-b*)^{n-m} e^{-|b|^2/2} L_m^{(n-m)}(|b|^2)
    """
    b = np.atleast_1d(np.asarray(b, complex))
    A = len(b)
    y = np.abs(b) ** 2
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

    The single-mode displaced-parity kernel implicit in fock.wigner_from_rho,
    so that W_single = (1/pi) sum_{r,c} rho[r,c] K[c,r].
    """
    b = np.sqrt(2.0) * (1j * np.asarray(pg, float))     # 2 a_c with x = 0
    D = _displacement_matrix(b, n_max)                  # (A, n_max, n_max)
    par = (-1.0) ** np.arange(n_max)
    return D * par[None, None, :]                       # weight the column index


def wigner_slice_ppp(rho, pg, n_max):
    """W(x=0, p1, x=0, p2, x=0, p3=0) = (1/pi^3) tr[rho kron(K1,K2,K3)].

    rho is the product-Fock density matrix, flat index (m1*N+m2)*N+m3 = the
    cat3_fock layout. Reshape to R6[m1,m2,m3,n1,n2,n3] and contract:

      * mode 1 kernel K1[a, n1, m1] over the p1 grid,
      * mode 2 kernel K2[b, n2, m2] over the p2 grid,
      * mode 3 kernel K3[n3, m3] FIXED at p3=0 (D(0)=I -> diagonal parity),

      W[a, b] = (1/pi^3) Re einsum('ijklpq,ali,bpj,qk->ab', R6, K1, K2, K3),
      with (i,j,k)=(m1,m2,m3) rows and (l,p,q)=(n1,n2,n3) columns.
    """
    R6 = rho.reshape((n_max,) * 6)
    K = _parity_kernel(pg, n_max)                       # (A, n_max, n_max)
    K3 = _parity_kernel([0.0], n_max)[0]                # (n_max, n_max) at p3=0
    W = np.einsum("ijklpq,ali,bpj,qk->ab", R6, K, K, K3, optimize=True)
    return np.real(W) / np.pi ** 3


def validate_slice(n_max=12, atol=1e-4):
    """allclose(atol) of the helper vs states3.ThreeModeCat.wigner on a coarse
    grid, using the FAITHFUL cat rho = outer(cat3_fock, cat3_fock) at n_max=12.

    This checks the KERNEL math, so rho must be a faithful cat. At n_max=12 the
    pure-Fock truncation error is ~1e-5 (the state is genuinely missing
    amplitude, nothing to do with the helper), so atol=1e-4 isolates the kernel
    while tolerating truncation. The 1728x1728 rho is 24 MB complex -- fine. The
    identical helper is then used at N_MAX=8 for the MLE rho (where the state's
    own truncation ceiling is 0.99321 and the slice's absolute accuracy is
    ~1e-3, documented, acceptable for a figure/Wmin readout).
    """
    psi = cat3_fock(ALPHA, PARITY, n_max)
    rho = np.outer(psi, psi.conj())
    coarse = np.linspace(-2.8, 2.8, 13)
    W_helper = wigner_slice_ppp(rho, coarse, n_max)
    P1, P2 = np.meshgrid(coarse, coarse, indexing="ij")
    cat = ThreeModeCat(ALPHA, PARITY)
    W_true = cat.wigner(0.0, P1, 0.0, P2, 0.0, 0.0)
    ok = np.allclose(W_helper, W_true, atol=atol)
    return ok, float(np.abs(W_helper - W_true).max())


# ---------------------------------------------------------------------------
# Cross-mode scaling context (modes 1-2 from the campaign's measured runs; the
# 3-mode row is filled from THIS run). Cited for the printed SCALING SUMMARY
# and the cost-scaling figure panel.
SCALING_REF = {
    1: dict(exp="exp03", dims=20, splat_wall=1.4, mle_wall=0.7, mle_dnf=False,
            fidelity="splat wins", verdict="split (MLE 2x faster -> no gain)"),
    2: dict(exp="exp04/07", dims=144, splat_wall=4.3, mle_wall=32.0,
            mle_dnf=False, fidelity="tie (paired t p=0.121)",
            verdict="splat wins speed (7.4x); fidelity tie"),
    # mode 3 filled in main() from measurements
}


# ---------------------------------------------------------------------------

def main():
    t_script = time.perf_counter()
    cat = ThreeModeCat(ALPHA, PARITY)
    psi = cat3_fock(ALPHA, PARITY, N_MAX)
    ceiling = cat3_truncation_fidelity(ALPHA, PARITY, N_MAX)

    print("=" * 96)
    print("EXPERIMENT 06 -- three-mode final verdict of the scaling campaign")
    print("=" * 96)
    print(f"three-mode cat |a,a,a>+parity|-a,-a,-a>  alpha={ALPHA} "
          f"parity={PARITY:+d}")
    print(f"official budget: {len(GRID)} triples (3x3x3 over [0,pi)^3), "
          f"{SHOTS} shots/triple, bins={BINS}")
    print(f"splat fit3f: seeds {SEEDS} (deterministic ~15 s each)")
    print(f"MLE mle3: seed {MLE_SEED} ONLY, n_max={N_MAX} ({N_MAX**3} dims), "
          f"{MLE_BUDGET_S} s soft wall  (budget dictates single-seed)")
    print(f"MLE truncation ceiling (Fock n_max={N_MAX}): {ceiling:.6f}")
    print(f"BLAS threads pinned to 1 (OMP/OPENBLAS/MKL/NUMEXPR) -- "
          f"faster here than multithreaded\n", flush=True)

    ok, maxdev = validate_slice()
    print(f"[validate] Wigner-slice helper vs states3.ThreeModeCat.wigner "
          f"(faithful n_max=12 rho): allclose(atol=1e-4) = {ok}  "
          f"(max |dev| = {maxdev:.2e})\n", flush=True)

    P1, P2 = np.meshgrid(PG, PG, indexing="ij")
    W_true_pp = cat.wigner(0.0, P1, 0.0, P2, 0.0, 0.0)

    # ---- splat: all three seeds ----
    splat_rows = []
    saved_mix = {}
    for seed in SEEDS:
        print(f"[splat seed={seed}] sampling {len(GRID)} triples x {SHOTS} "
              f"shots ...", flush=True)
        data = cat.sample_homodyne(GRID, SHOTS, rng=seed)
        print(f"[splat seed={seed}] fitting fit3f (bins={BINS}) ...", flush=True)
        t0 = time.perf_counter()
        mix = fit3f(data, bins=BINS)
        t_splat = time.perf_counter() - t0
        f_splat = fidelity_vs_cat3(mix, ALPHA, PARITY)
        W_splat = mix.wigner6(0.0, P1, 0.0, P2, 0.0, 0.0)
        wmin = float(W_splat.min())
        K = len(mix.w)
        print(f"[splat seed={seed}] F={f_splat:.4f}  wall={t_splat:.1f}s  "
              f"K={K}  Wmin={wmin:.4f}\n", flush=True)
        splat_rows.append(dict(seed=seed, F=f_splat, wall=t_splat, K=K,
                               wmin=wmin))
        saved_mix[seed] = mix

    splat42 = next(r for r in splat_rows if r["seed"] == MLE_SEED)
    splat_target_F = splat42["F"]

    # ---- MLE: seed 42 only, 900 s budget, full trajectory ----
    print(f"[MLE seed={MLE_SEED}] sampling + binning (same data rule) ...",
          flush=True)
    data = cat.sample_homodyne(GRID, SHOTS, rng=MLE_SEED)
    centers, targets = histogram_targets3(data, bins=BINS)

    traj_t, traj_f = [], []          # (elapsed_s, fidelity) every ~20 iters
    prints = []                      # printed excerpts every ~50 iters
    cross_time = [None]              # time-to-splat-quality
    last = {"it": 0, "ll": 0.0, "elapsed": 0.0}

    def callback(it, ll, elapsed, rho):
        last.update(it=it, ll=ll, elapsed=elapsed)
        if it % 20 == 0 or it == 1:
            f = fidelity_pure(psi, rho)
            traj_t.append(elapsed)
            traj_f.append(f)
            if cross_time[0] is None and f >= splat_target_F:
                cross_time[0] = elapsed
            if it % 50 == 0 or it == 1:
                s_per = elapsed / it
                line = (f"  it={it:>4}  ll={ll:.5f}  F={f:.5f}  "
                        f"elapsed={elapsed:6.1f}s  ({s_per:.3f} s/it)")
                prints.append(line)
                print("[MLE]" + line, flush=True)

    print(f"[MLE seed={MLE_SEED}] running mle3_reconstruct "
          f"(n_max={N_MAX}, budget={MLE_BUDGET_S}s) ...", flush=True)
    t0 = time.perf_counter()
    rho, iters, converged = mle3_reconstruct(
        centers, targets, n_max=N_MAX, time_budget_s=MLE_BUDGET_S,
        callback=callback)
    t_mle = time.perf_counter() - t0
    f_mle = fidelity_pure(psi, rho)
    if traj_t and traj_f[-1] != f_mle:
        traj_t.append(last["elapsed"])
        traj_f.append(f_mle)
    W_mle_pp = wigner_slice_ppp(rho, PG, N_MAX)
    wmin_mle = float(W_mle_pp.min())
    s_per_iter = t_mle / max(iters, 1)
    print(f"[MLE seed={MLE_SEED}] DONE  F={f_mle:.5f}  iters={iters}  "
          f"converged={converged}  wall={t_mle:.1f}s  "
          f"({s_per_iter:.3f} s/it)\n", flush=True)

    # fill the 3-mode scaling row from measurements
    mle_verdict_fid = "splat" if splat_target_F > f_mle else "MLE"
    mle_verdict_spd = "splat" if splat42["wall"] < t_mle else "MLE"
    SCALING_REF[3] = dict(
        exp="exp06", dims=N_MAX ** 3, splat_wall=splat42["wall"],
        mle_wall=t_mle, mle_dnf=(not converged),
        fidelity=f"splat wins ({splat_target_F:.3f} vs {f_mle:.3f})"
        if mle_verdict_fid == "splat" else f"MLE wins",
        verdict=f"splat wins BOTH (F+speed)"
        if (mle_verdict_fid == "splat" and mle_verdict_spd == "splat")
        else "splat does NOT sweep")

    # =====================================================================
    # PRINTED OUTPUT
    # =====================================================================
    print("=" * 96)
    print("PER-SEED SPLAT TABLE  (fit3f, official budget)")
    print("=" * 96)
    print(f"true (p1,p2)@x=0,p3=0 Wigner min: {W_true_pp.min():.4f}\n")
    hdr = f"{'seed':>4} | {'F_splat':>8} {'wall':>8} {'K':>4} {'Wmin':>8}"
    print(hdr)
    print("-" * len(hdr))
    for r in splat_rows:
        print(f"{r['seed']:>4} | {r['F']:8.4f} {r['wall']:7.1f}s {r['K']:>4} "
              f"{r['wmin']:8.4f}")
    Fs = np.array([r["F"] for r in splat_rows])
    ts = np.array([r["wall"] for r in splat_rows])
    print("-" * len(hdr))
    print(f"mean | {Fs.mean():8.4f} {ts.mean():7.1f}s")
    neg = all(r["wmin"] < 0 for r in splat_rows)
    print(f"\nNegativity (Wmin<0) recovered every seed: {neg}")

    print("\n" + "=" * 96)
    print(f"MLE BLOCK  (mle3, seed {MLE_SEED} only, n_max={N_MAX} "
          f"= {N_MAX**3} dims, {MLE_BUDGET_S}s budget)")
    print("=" * 96)
    print("underdetermined: ~17.7k histogram rows vs "
          f"{N_MAX**3}^2 = {N_MAX**6} density-matrix params; loglik plateaus "
          "early while fidelity creeps.")
    print(f"\ntrajectory excerpts (F via <psi|rho|psi> on the callback rho):")
    for line in prints:
        print(line)
    print(f"\nfinal:  F={f_mle:.5f}  iters={iters}  converged={converged}  "
          f"wall={t_mle:.1f}s  s/iter={s_per_iter:.3f}")
    print(f"MLE ceiling (unreachable in budget): {ceiling:.5f}   "
          f"Wmin(slice)={wmin_mle:.4f}")
    status = "DID NOT FINISH (DNF)" if not converged else "converged"
    print(f"status: {status}  "
          f"(converged=False -> hit the {MLE_BUDGET_S}s soft wall)")

    print(f"\n*** time-to-splat-quality ***")
    print(f"splat seed {MLE_SEED} final F = {splat_target_F:.4f} (reached in "
          f"{splat42['wall']:.1f}s).")
    if cross_time[0] is not None:
        print(f"MLE fidelity first crossed {splat_target_F:.4f} at "
              f"{cross_time[0]:.1f}s of iteration -- splat still "
              f"{cross_time[0]/max(splat42['wall'],1e-9):.1f}x faster to that "
              f"quality.")
    else:
        print(f"MLE NEVER reached splat quality: after {t_mle:.0f}s / {iters} "
              f"iters it plateaued at F={f_mle:.4f} < {splat_target_F:.4f}. "
              f"Time-to-splat-quality = infinity (DNF).")

    # ---- SCALING SUMMARY across 1/2/3 modes ----
    print("\n" + "=" * 96)
    print("SCALING SUMMARY  (1 vs 2 vs 3 modes; modes 1-2 from exp03/exp04-07, "
          "mode 3 measured here)")
    print("=" * 96)
    sh = (f"{'modes':>5} {'exp':>9} {'Fock dims':>9} {'splat wall':>11} "
          f"{'MLE wall':>12} | {'fidelity':>24} | verdict")
    print(sh)
    print("-" * len(sh))
    for modes in (1, 2, 3):
        s = SCALING_REF[modes]
        mle_wall = (f"{s['mle_wall']:.0f}s DNF" if s["mle_dnf"]
                    else f"{s['mle_wall']:.1f}s")
        splat_wall = f"{s['splat_wall']:.1f}s"
        print(f"{modes:>5} {s['exp']:>9} {s['dims']:>9} {splat_wall:>11} "
              f"{mle_wall:>12} | {s['fidelity']:>24} | {s['verdict']}")
    print("\n(1 mode: n_max=20; 2 mode: 12^2; 3 mode: 8^3. MLE dim = "
          "n_max^modes -- the exponential wall. Splat = O(K), 28 params/splat.)")

    # ---- FINAL VERDICT ----
    print("\n" + "=" * 96)
    print("FINAL VERDICT")
    print("=" * 96)
    win_fid = splat_target_F > f_mle
    win_spd = splat42["wall"] < t_mle
    both = win_fid and win_spd
    print(f"At 3 modes (seed {MLE_SEED}):")
    print(f"  fidelity: splat {splat_target_F:.4f}  vs  MLE {f_mle:.4f}"
          f"{' (DNF)' if not converged else ''}   -> "
          f"{'SPLAT' if win_fid else 'MLE'} wins")
    print(f"  speed:    splat {splat42['wall']:.1f}s  vs  MLE {t_mle:.1f}s"
          f"{' (DNF)' if not converged else ''}   -> "
          f"{'SPLAT' if win_spd else 'MLE'} wins "
          f"({t_mle/max(splat42['wall'],1e-9):.0f}x)")
    print(f"\nDoes the splat win BOTH at 3 modes?  "
          f"{'YES' if both else 'NO'}")
    if both:
        print("The campaign's SCALING hypothesis is confirmed: the tie flips to "
              "a clean sweep once the Fock dimension (n_max^modes) makes MLE\n"
              "intractable. 1 mode split -> 2 modes tie+speed -> 3 modes splat "
              "wins fidelity AND speed, against an MLE that cannot even finish.")
    else:
        print("Falsification watch: splat did not sweep -- inspect the numbers "
              "above.")
    print(f"\nmean splat fidelity over seeds {SEEDS}: {Fs.mean():.4f} "
          f"(all seeds recovered negativity: {neg})")

    # =====================================================================
    # FIGURE
    # =====================================================================
    mix42 = saved_mix[MLE_SEED]
    W_splat_pp = mix42.wigner6(0.0, P1, 0.0, P2, 0.0, 0.0)
    vmax = max(np.abs(W_true_pp).max(), np.abs(W_splat_pp).max(),
               np.abs(W_mle_pp).max())
    ext = [PG[0], PG[-1], PG[0], PG[-1]]

    fig = plt.figure(figsize=(15, 9.5))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.95], hspace=0.32,
                          wspace=0.30)

    # --- row 1: three Wigner slices, shared RdBu scale ---
    panels = [
        (W_true_pp, "true", None, None),
        (W_splat_pp, "splat", splat_target_F, splat42["wall"]),
        (W_mle_pp, "MLE" + (" (DNF)" if not converged else ""), f_mle, t_mle),
    ]
    for col, (W, name, F, wall) in enumerate(panels):
        ax = fig.add_subplot(gs[0, col])
        im = ax.imshow(W.T, origin="lower", extent=ext, cmap="RdBu_r",
                       vmin=-vmax, vmax=vmax, aspect="equal")
        if F is None:
            title = f"{name}  W(p1,p2)@x=0,p3=0"
        else:
            title = f"{name}  F={F:.4f}  {wall:.0f}s"
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("p1")
        ax.set_ylabel("p2")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # --- row 2 left: MLE fidelity-vs-walltime trajectory ---
    axl = fig.add_subplot(gs[1, 0:2])
    axl.plot(traj_t, traj_f, "-o", ms=3, color="#1f77b4",
             label="MLE fidelity trajectory")
    axl.axhline(splat_target_F, color="#d62728", ls="--", lw=1.6,
                label=f"splat final F={splat_target_F:.3f}")
    axl.axvline(splat42["wall"], color="#2ca02c", ls=":", lw=1.6,
                label=f"splat wall={splat42['wall']:.1f}s")
    axl.axhline(ceiling, color="gray", ls="-.", lw=1.0, alpha=0.7,
                label=f"MLE ceiling={ceiling:.3f}")
    axl.set_xscale("log")
    axl.set_xlabel("MLE wall time (s, log)")
    axl.set_ylabel("fidelity <psi|rho|psi>")
    txt = ("MLE never reaches splat quality (DNF)"
           if cross_time[0] is None
           else f"crosses splat F at {cross_time[0]:.0f}s")
    axl.set_title(f"MLE fidelity vs wall time -- {txt}", fontsize=11)
    axl.legend(fontsize=8, loc="lower right")
    axl.grid(True, which="both", alpha=0.25)

    # --- row 2 right: cost-scaling chart ---
    axr = fig.add_subplot(gs[1, 2])
    modes = [1, 2, 3]
    splat_w = [SCALING_REF[m]["splat_wall"] for m in modes]
    mle_w = [SCALING_REF[m]["mle_wall"] for m in modes]
    axr.plot(modes, splat_w, "-s", color="#2ca02c", label="splat (fit)")
    # MLE: solid up to mode 2, open marker + annotation for the 3-mode DNF
    axr.plot(modes[:2], mle_w[:2], "-o", color="#1f77b4", label="MLE")
    axr.plot([3], [mle_w[2]], "o", mfc="none", mec="#1f77b4", ms=11, mew=2)
    axr.plot([2, 3], mle_w[1:], "--", color="#1f77b4", alpha=0.6)
    axr.annotate("DNF\n(>=900s,\nlower bound)", xy=(3, mle_w[2]),
                 xytext=(2.35, mle_w[2] * 2.1), fontsize=8, color="#1f77b4",
                 ha="center")
    axr.set_yscale("log")
    axr.set_xticks(modes)
    axr.set_xlabel("modes")
    axr.set_ylabel("wall time (s, log)")
    axr.set_title("cost scaling: Fock dim = n_max^modes", fontsize=11)
    axr.legend(fontsize=8, loc="upper left")
    axr.grid(True, which="both", alpha=0.25)

    fig.suptitle(
        f"Three-mode cat alpha={ALPHA}: splat vs product-Fock MLE -- the "
        f"scaling verdict (seed {MLE_SEED}; row-1 panels share RdBu scale)",
        fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    outdir = pathlib.Path(__file__).resolve().parent / "out"
    outdir.mkdir(parents=True, exist_ok=True)
    figpath = outdir / "three_mode_verdict.png"
    fig.savefig(figpath, dpi=130)
    print(f"\nfigure written to {figpath}")
    print(f"total script runtime: {time.perf_counter() - t_script:.0f}s")


if __name__ == "__main__":
    main()
