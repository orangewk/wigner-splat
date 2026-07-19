"""Exp19 follow-up: two corrections + one exploratory addendum.

Declared before running:

1. RESCORE the lossy-family row. The main run scored the fitted
   loss_eta(B B^dagger) model by projecting its PRE-loss ket mixture at
   n_max = 8 and then applying the loss channel -- but the fit drove eta
   down to 0.36, which scales the pre-loss amplitudes up by 1/sqrt(eta)
   and pushes half the mass past the truncation (projection trace 0.53 in
   the committed log). That is a SCORING-PIPELINE artifact, not a model
   property: the channel OUTPUT lives at ordinary amplitudes. Fix: refit
   with the identical protocol (deterministic seeds), project the
   pre-loss kets at n_max = 16, apply the truncated Kraus channel there,
   and cut the output back to the n_max = 8 block for the Uhlmann score
   (quoting the post-cut trace, which should now be near 1).

2. RECLASSIFY the lossy-family row in the ruling. loss_eta(rank-2
   B B^dagger) is FULL RANK (a CPTP channel output), so the rank-2
   fidelity ceiling does not bound it; comparing it against that ceiling
   in the main log's ruling table was a labeling error. Its honest
   comparison axes are the MLE and the trace ceiling.

3. EXPLORATORY ADDENDUM (labeled as such; single config, outside the
   pre-declared fixed lineup): the main result's texture is that rank-1
   models sit AT their rank-1 ceiling (0.369/0.371 vs 0.378) and rank-2
   coherent reaches 86% of its rank-2 ceiling -- the binding constraint
   looks like RANK CAPACITY, not fit quality. One blind bbdagM rank-8
   coherent fit (R=8, K=2, iters=300, init seeds {0,1,2} best-by-train)
   probes whether the family keeps tracking its ceiling (R=8 ceiling
   0.9513) when given the rank a full-rank target needs. This feeds the
   decision on a follow-up issue; it does not change the exp19 gate
   ruling, which stands as declared.
"""
import importlib.util
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagM import fit_bbdagM_mixed, nll_mixed  # noqa: E402
from wigner_splat.bbdagS import (  # noqa: E402
    fit_bbdagS_lossy_mixed, nll_lossy_mixed, sq_wavefunction,
)
from wigner_splat.fock import hermite_psi, thermal_lossy_cat3_fock  # noqa: E402
from wigner_splat.states3x import ThermalLossyThreeModeCat  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "run19", pathlib.Path(__file__).parent / "run.py")
run19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run19)

N_BIG = 16


def ket_to_fock_big(z, alpha, xi, n_big):
    xg = run19._XGRID
    H = hermite_psi(xg, n_big)
    K, M = alpha.shape
    out = np.zeros((n_big,) * 3, complex)
    for c in range(K):
        v = [np.trapezoid(H * sq_wavefunction(xg, alpha[c, m],
                                              xi[c, m])[None, :], xg, axis=1)
             for m in range(M)]
        out += z[c] * np.einsum("i,j,k->ijk", v[0], v[1], v[2])
    return out


def apply_loss_big(rho6, eta, n_big):
    from math import comb
    As = []
    for k in range(n_big):
        A = np.zeros((n_big, n_big))
        idx = np.arange(k, n_big)
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


def main():
    print("=== exp19 follow-up: lossy-row rescore + rank-8 exploratory "
          "addendum ===")
    target = ThermalLossyThreeModeCat(run19.ALPHA, run19.PARITY, run19.ETA,
                                      run19.SIGMA_ADD)
    data = target.sample_homodyne(run19.GRID, run19.SHOTS,
                                  rng=run19.DATA_SEED)
    rho_t = thermal_lossy_cat3_fock(run19.ALPHA, run19.PARITY, run19.ETA,
                                    run19.SIGMA_ADD, run19.N_MAX)
    ev = np.sort(np.linalg.eigvalsh((rho_t + rho_t.conj().T) / 2))[::-1]

    # ---- 1. rescore the lossy-family fit at a wide intermediate cutoff ----
    fits = []
    for s in run19.INIT_SEEDS:
        st, eta_f = fit_bbdagS_lossy_mixed(
            data, R=2, K=4, M=3, eta0=run19.ETA, fit_eta=True,
            iters=run19.ITERS["lossy"], seed=s)
        fits.append((nll_lossy_mixed(st, data, eta_f), (st, eta_f, s)))
    st, eta_f, s = min(fits, key=lambda t: t[0])[1]
    print(f"  refit reproduced: init {s}, eta={eta_f:.4f}", flush=True)
    rho_pre = np.zeros((N_BIG,) * 6, complex)
    for z, a, x in zip(st.z, st.alpha, st.xi):
        col = ket_to_fock_big(z, a, x, N_BIG)
        rho_pre += np.einsum("ijk,lmn->ijklmn", col, col.conj())
    rho_pre /= st.norm_sq()
    pre_trace = float(np.real(np.einsum("ijkijk->", rho_pre)))
    rho_out6 = apply_loss_big(rho_pre, eta_f, N_BIG)
    n8 = run19.N_MAX
    rho_out = rho_out6[:n8, :n8, :n8, :n8, :n8, :n8].reshape(n8 ** 3, n8 ** 3)
    out_trace = float(np.trace(rho_out).real)
    F = run19.uhlmann(rho_out, rho_t)
    print(f"  lossy R2K4 rescored: F={F:.4f} (pre-loss n16 trace "
          f"{pre_trace:.4f}, post-channel n8 trace {out_trace:.4f}; the "
          f"committed main-log value 0.4256 at proj trace 0.5345 is "
          f"superseded)", flush=True)

    # ---- 3. exploratory rank-8 coherent addendum -------------------------
    fits = []
    for s in run19.INIT_SEEDS:
        t0 = time.perf_counter()
        st8 = fit_bbdagM_mixed(data, R=8, K=2, M=3, iters=300, seed=s)
        fits.append((nll_mixed(st8, data),
                     (st8, time.perf_counter() - t0, s)))
    st8, wall, s = min(fits, key=lambda t: t[0])[1]
    rho8 = run19.bb_state_to_fock_rho(
        st8.z, st8.alpha, np.zeros_like(st8.alpha), st8.norm_sq())
    F8 = run19.uhlmann(rho8, rho_t)
    ceil8 = float(np.sum(ev[:8]))
    print(f"  [EXPLORATORY] bbdagM R8K2 blind: F={F8:.4f} vs rank-8 "
          f"ceiling {ceil8:.4f} (proj trace {np.trace(rho8).real:.4f}, "
          f"init {s}, wall={wall:.0f}s)", flush=True)

    out = pathlib.Path(__file__).parent / "results_followup.json"
    out.write_text(json.dumps(dict(
        lossy_rescore=dict(F=F, eta=eta_f, pre_trace=pre_trace,
                           out_trace=out_trace),
        addendum_R8=dict(F=F8, ceiling=ceil8, wall_s=wall, init=s),
    ), indent=1))
    print(f"raw results -> {out}")


if __name__ == "__main__":
    main()
