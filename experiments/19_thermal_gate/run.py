"""Experiment 19 -- issue #38: the blind-generalization gate (thermal-noise
lossy cat, a full-rank held-out target).

Experiment 11 established FAMILY ADAPTABILITY (identify the failure
direction, extend the ansatz, win the like-metric comparison) and its scope
correction explicitly barred any "generalizing method" claim until the
extended family is tested against a held-out target NO finite-rank ket
mixture contains. This is that gate: the lossy cat followed by per-mode
classical Gaussian displacement noise (ThermalLossyThreeModeCat) is FULL
RANK, so it lies outside every FINITE-RANK KET MIXTURE in the lineup by
construction. FAMILY-BOUNDARY NOTE (PR-61 review): that guarantee covers
the pure-detection ket mixtures only -- the channel-composed member
loss_eta(B B^dagger) is itself a full-rank family with a free eta, and
whether the target lies outside THAT family is not established, so the
ruling below words its claim as blind held-out performance, not
out-of-family generalization.

PROTOCOL (declared before the run):
  * target: alpha = 1.5, parity = +1, eta = 0.8, sigma_add = 0.1 (added
    variance per quadrature; a substantial full-rank perturbation). Data:
    3x3x3 angle triples x 2000 shots, data seed 42 (exp11 conventions).
  * FIXED lineup -- the exp11/exp14 extensions, fitted BLIND (no
    reconstructor is told sigma_add; the lossy-family fit may spend its own
    eta knob however it likes, that freedom is part of the family):
      - bbdagM rank-2 coherent (R=2, K=2, iters=200)     [exp11 config]
      - bbdagS squeezed-product (K=4, iters=400)         [exp11 config]
      - bbdagS rank-R x squeezed x loss (R=2, K=4, eta fitted from 0.8,
        iters=400)                                       [exp14 primary]
      - purefock3 (n_max=8, iters=1000)                  [generic control]
      - mle3 (n_max=8, 900 s)                            [full-rank]
      - splat fit3f (overlap-score axis, closed-form thermal overlap;
        perfect score = target purity, non-PSD caveat as always)
  * init seeds {0,1,2} per stochastic fit, representative = best TRAIN
    objective (exp16's likelihood-blindness finding makes single-init
    headlines untrustworthy; this is declared as an exp11-protocol
    UPGRADE, not a deviation).
  * scoring: Uhlmann fidelity against the Fock-route thermal target at
    n_max = 8 (fock.thermal_lossy_cat3_fock; the truncated trace is quoted
    as the ceiling analog, and the target matrix is REAL symmetric, so the
    purefock3 conjugate-convention subtlety documented in
    tests/test_loss_deployment.py cannot bias it). BB-dagger states are
    projected to Fock by per-mode quadrature coefficients (projection norm
    quoted); the lossy-family model's density matrix is the LOSS-CHANNEL
    OUTPUT of its fitted ket mixture (truncated Kraus, exact downward).
  * rank-R fidelity ceilings, computed from the target's eigenvalues:
    max over rank-R sigma of F(sigma, rho) = sum of rho's top R
    eigenvalues (attained by the renormalized top-R truncation). Quoted
    for R = 1, 2, 4, 8 at n_max = 8 with an n_max = 10 stability check.
  * FALSIFICATION CONDITION (issue #38, declared): if the best
    fixed-family Uhlmann F falls short of its own rank ceiling by more
    than 0.05 AND is below the MLE's F, record "the BB-dagger family is
    effective for in-family adaptation only" and keep the generalizing
    claim barred. Conversely, coming within 0.05 of the rank ceiling
    (or beating MLE while near it) records the gate as PASSED for this
    target, with the usual single-data-seed scope note.

Numbering note: experiments 15-18 are taken (15_video_conf #48,
16_exp11_seeds #39, 17_loss_control #42, 18_gkp_saturation #40).
"""
import itertools
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagM import fit_bbdagM_mixed, nll_mixed  # noqa: E402
from wigner_splat.bbdagS import (  # noqa: E402
    fit_bbdagS, fit_bbdagS_lossy_mixed, nll as nll_sq, nll_lossy_mixed,
    sq_wavefunction,
)
from wigner_splat.data3 import histogram_targets3  # noqa: E402
from wigner_splat.fit3f import fit3f  # noqa: E402
from wigner_splat.fock import hermite_psi, thermal_lossy_cat3_fock  # noqa: E402
from wigner_splat.forward3f import overlap_vs_thermal_lossy_cat3  # noqa: E402
from wigner_splat.mle3 import mle3_reconstruct  # noqa: E402
from wigner_splat.purefock3 import fit_purefock3, nll_psi  # noqa: E402
from wigner_splat.states3x import ThermalLossyThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
ETA = 0.8
SIGMA_ADD = 0.1
SHOTS = 2000
DATA_SEED = 42
INIT_SEEDS = (0, 1, 2)
N_MAX = 8
BINS = 24
MLE_BUDGET_S = 900.0
CEILING_MARGIN = 0.05
ITERS = dict(bbdagM=200, bbdagS=400, lossy=400, purefock=1000)
N_INTERMEDIATE = 16
STABILITY_N = 10
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]


def uhlmann(rho, sigma):
    rho = (rho + rho.conj().T) / 2
    sigma = (sigma + sigma.conj().T) / 2
    w, U = np.linalg.eigh(rho)
    sq = (U * np.sqrt(np.maximum(w, 0.0))) @ U.conj().T
    inner = sq @ sigma @ sq
    inner = (inner + inner.conj().T) / 2
    ev = np.maximum(np.linalg.eigvalsh(inner), 0.0)
    return float(np.sum(np.sqrt(ev)) ** 2)


# ------------------------- fitted state -> Fock -------------------------

_XGRID = np.linspace(-(np.sqrt(2) * (ALPHA + 2.0) + 8.0),
                     np.sqrt(2) * (ALPHA + 2.0) + 8.0, 4001)
_HPSI = hermite_psi(_XGRID, N_MAX)                       # (n, G)


def mode_coeffs(alpha, xi):
    """<n|D(alpha)S(xi)|0> for n < N_MAX by quadrature (exact to trapz)."""
    f = sq_wavefunction(_XGRID, alpha, xi)
    return np.trapezoid(_HPSI * f[None, :], _XGRID, axis=1)


def ket_to_fock(z, alpha, xi):
    """Flat Fock ket of sum_c z_c prod_m D(alpha_cm) S(xi_cm)|0>."""
    K, M = alpha.shape
    out = np.zeros((N_MAX,) * 3, complex)
    for c in range(K):
        v = [mode_coeffs(alpha[c, m], xi[c, m]) for m in range(M)]
        out += z[c] * np.einsum("i,j,k->ijk", v[0], v[1], v[2])
    return out.reshape(-1)


def bb_state_to_fock_rho(cols_z, cols_alpha, cols_xi, Z):
    """rho = sum_r |col_r><col_r| / Z in the truncated Fock basis.

    Z is the CLOSED-FORM norm (state.norm_sq()); the returned trace is the
    projection retention (quoted alongside the fidelity)."""
    dim = N_MAX ** 3
    rho = np.zeros((dim, dim), complex)
    for z, a, x in zip(cols_z, cols_alpha, cols_xi):
        col = ket_to_fock(z, a, x)
        rho += np.outer(col, col.conj())
    return rho / Z


def ket_to_fock_wide(z, alpha, xi, n_big):
    """ket_to_fock at an arbitrary cutoff (the lossy-row scoring needs a
    wide intermediate truncation; see the call site)."""
    H = hermite_psi(_XGRID, n_big)
    K, M = alpha.shape
    out = np.zeros((n_big,) * 3, complex)
    for c in range(K):
        v = [np.trapezoid(H * sq_wavefunction(_XGRID, alpha[c, m],
                                              xi[c, m])[None, :],
                          _XGRID, axis=1) for m in range(M)]
        out += z[c] * np.einsum("i,j,k->ijk", v[0], v[1], v[2])
    return out


def apply_loss_channel_wide(rho6, eta, n):
    """Truncated per-mode loss Kraus on a 6-index tensor (exact downward)."""
    from math import comb
    As = []
    for k in range(n):
        A = np.zeros((n, n))
        idx = np.arange(k, n)
        A[idx - k, idx] = [np.sqrt(comb(m, k) * eta ** (m - k)
                                   * (1 - eta) ** k) for m in idx]
        As.append(A)
    out = rho6
    for mode in range(3):
        acc = np.zeros_like(out)
        for A in As:
            t = np.tensordot(A, out, axes=([1], [mode]))
            t = np.moveaxis(t, 0, mode)
            t = np.tensordot(t, A, axes=([mode + 3], [1]))
            acc += np.moveaxis(t, -1, mode + 3)
        out = acc
    return out


def apply_loss_channel_3mode(rho, eta):
    """Truncated per-mode loss Kraus (exact downward in the truncation)."""
    from math import comb
    n = N_MAX
    As = []
    for k in range(n):
        A = np.zeros((n, n))
        idx = np.arange(k, n)
        A[idx - k, idx] = [np.sqrt(comb(m, k) * eta ** (m - k)
                                   * (1 - eta) ** k) for m in idx]
        As.append(A)
    shape6 = (n,) * 6
    out = np.asarray(rho, complex).reshape(shape6)
    for mode in range(3):
        acc = np.zeros(shape6, complex)
        for A in As:
            t = np.tensordot(A, out, axes=([1], [mode]))
            t = np.moveaxis(t, 0, mode)
            t = np.tensordot(t, A, axes=([mode + 3], [1]))
            acc += np.moveaxis(t, -1, mode + 3)
        out = acc
    return out.reshape(n ** 3, n ** 3)


def main():
    print("=== exp19: issue #38 -- the blind-generalization gate "
          "(thermal-noise lossy cat) ===")
    print(f"target alpha={ALPHA} parity={PARITY} eta={ETA} "
          f"sigma_add={SIGMA_ADD}; {len(GRID)} triples x {SHOTS} shots, "
          f"data seed {DATA_SEED}; init seeds {INIT_SEEDS} best-by-train",
          flush=True)

    target = ThermalLossyThreeModeCat(ALPHA, PARITY, ETA, SIGMA_ADD)
    data = target.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)

    print("building the Fock-route target (n_max=8 + n_max=10 stability "
          "check)...", flush=True)
    rho_t = thermal_lossy_cat3_fock(ALPHA, PARITY, ETA, SIGMA_ADD, N_MAX)
    trace8 = float(np.trace(rho_t).real)
    ev8 = np.sort(np.linalg.eigvalsh((rho_t + rho_t.conj().T) / 2))[::-1]
    rho_t10 = thermal_lossy_cat3_fock(ALPHA, PARITY, ETA, SIGMA_ADD, STABILITY_N)
    ev10 = np.sort(np.linalg.eigvalsh(
        (rho_t10 + rho_t10.conj().T) / 2))[::-1]
    purity = float(np.sum(ev8 ** 2))
    print(f"  truncated trace: n8={trace8:.5f} n{STABILITY_N}={np.sum(ev10):.5f}; "
          f"purity(n8)={purity:.4f}")
    ceil = {R: float(np.sum(ev8[:R])) for R in (1, 2, 4, 8)}
    ceil10 = {R: float(np.sum(ev10[:R])) for R in (1, 2, 4, 8)}
    print("  rank-R fidelity ceilings (sum of top-R eigenvalues):")
    for R in (1, 2, 4, 8):
        print(f"    R={R}: {ceil[R]:.4f} (n10 check {ceil10[R]:.4f})")

    rows = []

    # ---------------- bbdagM rank-2 coherent (exp11 config) ----------------
    fits = []
    for s in INIT_SEEDS:
        t0 = time.perf_counter()
        st = fit_bbdagM_mixed(data, R=2, K=2, M=3, iters=ITERS['bbdagM'], seed=s)
        fits.append((nll_mixed(st, data),
                     (st, time.perf_counter() - t0, s)))
    st, wall, s = min(fits, key=lambda t: t[0])[1]
    rho_f = bb_state_to_fock_rho(
        st.z, st.alpha, np.zeros_like(st.alpha), st.norm_sq())
    F = uhlmann(rho_f, rho_t)
    rows.append(("bbdagM R2K2", 2, F, float(np.trace(rho_f).real), None,
                 wall, s))
    print(f"  bbdagM R2K2      F={F:.4f} (proj trace "
          f"{np.trace(rho_f).real:.4f}, init {s}, wall={wall:.0f}s)",
          flush=True)

    # ---------------- bbdagS squeezed K=4 (exp11 config) -------------------
    fits = []
    for s in INIT_SEEDS:
        t0 = time.perf_counter()
        st = fit_bbdagS(data, K=4, M=3, iters=ITERS['bbdagS'], seed=s)
        fits.append((nll_sq(st, data), (st, time.perf_counter() - t0, s)))
    st, wall, s = min(fits, key=lambda t: t[0])[1]
    rho_f = bb_state_to_fock_rho(
        [st.z], [st.alpha], [st.xi], st.norm_sq())
    F = uhlmann(rho_f, rho_t)
    rows.append(("bbdagS K4", 1, F, float(np.trace(rho_f).real), None,
                 wall, s))
    print(f"  bbdagS K4        F={F:.4f} (proj trace "
          f"{np.trace(rho_f).real:.4f}, init {s}, wall={wall:.0f}s)",
          flush=True)

    # -------- bbdagS rank-2 x squeezed x loss (exp14 primary config) -------
    fits = []
    for s in INIT_SEEDS:
        t0 = time.perf_counter()
        st, eta_f = fit_bbdagS_lossy_mixed(data, R=2, K=4, M=3, eta0=ETA,
                                           fit_eta=True, iters=ITERS['lossy'], seed=s)
        fits.append((nll_lossy_mixed(st, data, eta_f),
                     (st, eta_f, time.perf_counter() - t0, s)))
    st, eta_f, wall, s = min(fits, key=lambda t: t[0])[1]
    # the fitted model is loss_eta(B B^dagger): project the PRE-loss kets at
    # a WIDE cutoff (a low fitted eta scales the pre-loss amplitudes up by
    # 1/sqrt(eta), which overflows n_max=8 -- the first run's scoring
    # artifact), apply the channel there, then cut the output back to the
    # scoring block. The model is FULL RANK by the channel (rank=None: the
    # finite-rank ceilings do not bound it; its ceiling is the trace).
    rho_pre6 = np.zeros((N_INTERMEDIATE,) * 6, complex)
    for z, a, x in zip(st.z, st.alpha, st.xi):
        col = ket_to_fock_wide(z, a, x, N_INTERMEDIATE)
        rho_pre6 += np.einsum("ijk,lmn->ijklmn", col, col.conj())
    rho_pre6 /= st.norm_sq()
    rho_out6 = apply_loss_channel_wide(rho_pre6, eta_f, N_INTERMEDIATE)
    rho_f = rho_out6[:N_MAX, :N_MAX, :N_MAX,
                     :N_MAX, :N_MAX, :N_MAX].reshape(N_MAX ** 3, N_MAX ** 3)
    F = uhlmann(rho_f, rho_t)
    rows.append(("bbdagS lossy R2K4", None, F, float(np.trace(rho_f).real),
                 eta_f, wall, s))
    print(f"  bbdagS lossyR2K4 F={F:.4f} eta={eta_f:.4f} (proj trace "
          f"{np.trace(rho_f).real:.4f}, init {s}, wall={wall:.0f}s)",
          flush=True)

    # ---------------- purefock3 (generic rank-1 control) -------------------
    fits = []
    for s in INIT_SEEDS:
        t0 = time.perf_counter()
        pf = fit_purefock3(data, n_max=N_MAX, iters=ITERS['purefock'], seed=s)
        fits.append((nll_psi(pf, data), (pf, time.perf_counter() - t0, s)))
    pf, wall, s = min(fits, key=lambda t: t[0])[1]
    flat = pf.ravel() / np.linalg.norm(pf)
    F = float(np.real(np.conj(flat) @ rho_t @ flat))
    rows.append(("purefock3", 1, F, 1.0, None, wall, s))
    print(f"  purefock3        F={F:.4f} (init {s}, wall={wall:.0f}s)",
          flush=True)

    # ---------------- mle3 (full rank) --------------------------------------
    centers, targets_h = histogram_targets3(data, bins=BINS)
    t0 = time.perf_counter()
    rho_m, iters, conv = mle3_reconstruct(centers, targets_h, n_max=N_MAX,
                                          time_budget_s=MLE_BUDGET_S)
    wall = time.perf_counter() - t0
    F_mle = uhlmann(rho_m, rho_t)
    rows.append(("mle3", None, F_mle, None, None, wall, None))
    print(f"  mle3             F={F_mle:.4f} (converged={conv}, "
          f"wall={wall:.0f}s)", flush=True)

    # ---------------- splat (overlap axis) ---------------------------------
    t0 = time.perf_counter()
    mix = fit3f(data, bins=BINS)
    wall = time.perf_counter() - t0
    score = overlap_vs_thermal_lossy_cat3(mix, ALPHA, PARITY, ETA, SIGMA_ADD)
    rows.append(("splat", None, score, None, None, wall, None))
    print(f"  splat            overlap={score:.4f} (perfect={purity:.4f}, "
          f"non-PSD axis, wall={wall:.0f}s)", flush=True)

    out = pathlib.Path(__file__).parent / "results.json"
    out.write_text(json.dumps(dict(
        ceilings=ceil, ceilings_n10=ceil10, trace8=trace8, purity=purity,
        rows=[dict(model=m, rank=R, value=v, proj_trace=pt, eta=e,
                   wall_s=w, init=s)
              for m, R, v, pt, e, w, s in rows]), indent=1))
    print(f"\nraw results -> {out}")

    # ---------------- gate ruling -------------------------------------------
    print("\n=== gate ruling (falsification condition declared in the "
          "docstring) ===")
    print(f"rank ceilings: R=1 {ceil[1]:.4f}, R=2 {ceil[2]:.4f} "
          f"(margin {CEILING_MARGIN})")
    best_name, best_F, best_gap = None, -1.0, None
    for m, R, v, *_ in rows:
        if m in ("mle3", "splat"):
            continue
        c = ceil[R] if R is not None else trace8   # channel rows: full rank
        rank_s = f"rank {R}" if R is not None else "full rank (channel)"
        gap = c - v
        flag = "NEAR CEILING" if gap <= CEILING_MARGIN else             f"short of ceiling by {gap:.4f}"
        beats = "beats MLE" if v > F_mle else "below MLE"
        print(f"  {m:18s} {rank_s}: F={v:.4f} vs ceiling {c:.4f} "
              f"-> {flag}; {beats}")
        if v > best_F:
            best_name, best_F, best_gap = m, v, gap
    fires = (best_gap > CEILING_MARGIN) and (best_F < F_mle)
    if fires:
        print("-> falsification condition FIRES: the fixed extended family "
              "neither approaches its rank ceiling nor matches the "
              "full-rank MLE on this held-out full-rank target. Recorded: "
              "in-family adaptation only; the generalizing claim stays "
              "barred.")
    else:
        print(f"-> falsification condition does NOT fire: best fixed-family "
              f"fit {best_name} F={best_F:.4f} (gap to its ceiling "
              f"{best_gap:.4f}; MLE {F_mle:.4f}). FAMILY-BOUNDARY NOTE "
              f"(PR-61 review): the target lies outside every finite-rank "
              f"ket mixture, but the winning member is the CHANNEL-COMPOSED "
              f"model, itself a full-rank family with a free eta -- whether "
              f"the target lies outside THAT family is not established. "
              f"What this run records is therefore BLIND HELD-OUT "
              f"PERFORMANCE on one synthetic full-rank target (single data "
              f"seed), not proven out-of-family generalization.")


if __name__ == "__main__":
    main()
