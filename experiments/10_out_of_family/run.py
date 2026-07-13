"""Experiment 10 -- BB-dagger out-of-family validation + rank>1 (issue #28).

The exp08 result was target-aligned: the cat IS two coherent-product kets, so
high fidelity is an existence statement, not a method. Here the coherent
rank-1 ansatz is taken out of its family in two orthogonal directions:

* MIXEDNESS -- LossyThreeModeCat (per-mode loss channel, transmissivity eta).
  Rank 2, so any rank-1 ket must plateau; the rank-2 BB-dagger extension
  (bbdagM.MixedCoherentKetState) can be exact. Fidelity is the exact Uhlmann
  fidelity on the coherent-product span (states3x, no truncation).
  This is the gate for real decohered data (issue #28 point 2).

* NON-GAUSSIAN KET SHAPE -- SqueezedThreeModeCat (per-mode squeeze r on the
  cat's kets). Still pure, but squeezed kets are outside the coherent
  dictionary at any finite K: the question is how gracefully fidelity
  degrades with K (finite-K approximation), measured against the exact pure
  fidelity via per-mode quadrature overlaps.

Falsification framing (issue #28): if BB-dagger cannot recover the lossy cat
at rank 2 (its own extended family), or squeezed-cat fidelity does not improve
with K, the ansatz is target-aligned-only and the representation needs a
different extension (multimode squeezed kets first).

purefock3 (generic pure Fock ket, issue #27's fair baseline) runs on the
squeezed target as the constraint-matched control; on the lossy target a
pure control is wrong-rank by construction (its plateau is reported for
completeness). Full-rank mixed MLE at 512 dims is out of scope here (the
historical 900 s DNF applies); the splat side has no lossy/squeezed pipeline
yet -- recorded as remaining scope in the log.
"""
import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagM import (  # noqa: E402
    fit_bbdagM, fit_bbdagM_mixed, nll, nll_mixed,
)
from wigner_splat.purefock3 import (  # noqa: E402
    fit_purefock3, nll_psi,
)
from wigner_splat.states3x import (  # noqa: E402
    LossyThreeModeCat, SqueezedThreeModeCat, fidelity_vs_squeezed_cat3,
    uhlmann_fidelity_vs_lossy_cat3,
)

ALPHA = 1.5
PARITY = +1
ETA = 0.8
SQUEEZE_R = 0.4
SHOTS = 2000
DATA_SEED = 42
INIT_SEED = 0
ITERS = 200
LEARNING_RATE = 0.05
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]


def lossy_block():
    target = LossyThreeModeCat(ALPHA, PARITY, eta=ETA)
    print(f"--- lossy cat: eta={ETA} (mixed, rank 2; cross damping "
          f"{target.cross:.4f}) ---")
    data = target.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)

    runs = [
        ("bbdag rank1 K=2", lambda: fit_bbdagM(
            data, K=2, M=3, iters=ITERS, lr=LEARNING_RATE, seed=INIT_SEED)),
        ("bbdag rank1 K=4", lambda: fit_bbdagM(
            data, K=4, M=3, iters=ITERS, lr=LEARNING_RATE, seed=INIT_SEED)),
        ("bbdag rank2 K=2", lambda: fit_bbdagM_mixed(
            data, R=2, K=2, M=3, iters=ITERS, lr=LEARNING_RATE, seed=INIT_SEED)),
        ("bbdag rank2 K=4", lambda: fit_bbdagM_mixed(
            data, R=2, K=4, M=3, iters=ITERS, lr=LEARNING_RATE, seed=INIT_SEED)),
    ]
    out = []
    for label, fit in runs:
        t0 = time.perf_counter()
        state = fit()
        wall = time.perf_counter() - t0
        F = uhlmann_fidelity_vs_lossy_cat3(state, target)
        n = nll(state, data) if "rank1" in label else nll_mixed(state, data)
        print(f"  {label:18s} Uhlmann F={F:.4f}  NLL={n:.4f}  wall={wall:.1f}s",
              flush=True)
        out.append((label, F))
    return out


def squeezed_block():
    target = SqueezedThreeModeCat(ALPHA, PARITY, r=SQUEEZE_R)
    print(f"\n--- squeezed cat: r={SQUEEZE_R} (pure, coherent-dictionary "
          "out-of-family) ---")
    data = target.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)

    out = []
    for K in (2, 4, 8):
        t0 = time.perf_counter()
        state = fit_bbdagM(data, K=K, M=3, iters=ITERS, lr=LEARNING_RATE,
                           seed=INIT_SEED)
        wall = time.perf_counter() - t0
        F = fidelity_vs_squeezed_cat3(state, target)
        print(f"  bbdag rank1 K={K}:  F={F:.4f}  NLL={nll(state, data):.4f}  "
              f"wall={wall:.1f}s", flush=True)
        out.append((f"K={K}", F))

    # constraint-matched generic control (same pure constraint, same NLL)
    t0 = time.perf_counter()
    pf = fit_purefock3(data, n_max=8, iters=1000, lr=LEARNING_RATE,
                       seed=INIT_SEED)
    wall = time.perf_counter() - t0
    # exact pure fidelity via 1D mode overlaps of the Fock ket vs target:
    # <psi_fock|target> = sum over the two target branches of products of
    # per-mode integrals conj(hermite_n) g_branch -- evaluate by quadrature.
    from wigner_splat.fock import hermite_psi
    x_max = np.sqrt(2) * (ALPHA + 2.0) + 8.0
    grid = np.linspace(-x_max, x_max, 4001)
    from wigner_splat.bbdag import sq_coherent_wavefunction
    gp = sq_coherent_wavefunction(grid, ALPHA, SQUEEZE_R)
    gm = sq_coherent_wavefunction(grid, -ALPHA, SQUEEZE_R)
    H = hermite_psi(grid, pf.shape[0])                       # (n_max, X)
    ovp = np.trapezoid(H * gp[None, :], grid, axis=1)        # <n|g_+>
    ovm = np.trapezoid(H * gm[None, :], grid, axis=1)
    amp = (np.einsum("mnq,m,n,q->", np.conj(pf), ovp, ovp, ovp)
           + PARITY * np.einsum("mnq,m,n,q->", np.conj(pf), ovm, ovm, ovm))
    F_pf = float(np.abs(amp) ** 2
                 / (np.sum(np.abs(pf) ** 2) * target.norm))
    print(f"  purefock n_max=8:  F={F_pf:.4f}  NLL={nll_psi(pf, data):.4f}  "
          f"wall={wall:.1f}s", flush=True)
    out.append(("purefock", F_pf))
    return out


def main():
    print("=== exp10: out-of-family targets + rank>1 BB-dagger (issue #28) ===")
    print(f"alpha={ALPHA} parity={PARITY}, {len(GRID)} triples x {SHOTS} shots, "
          f"data seed {DATA_SEED}, Adam(lr={LEARNING_RATE}, iters={ITERS})\n")
    lossy = lossy_block()
    squeezed = squeezed_block()

    print("\n=== verdict (issue #28 falsification framing) ===")
    r1 = max(F for label, F in lossy if "rank1" in label)
    r2 = max(F for label, F in lossy if "rank2" in label)
    print(f"lossy: best rank1 F={r1:.4f} vs best rank2 F={r2:.4f} -> "
          + ("rank-2 extension RECOVERS the mixed target"
             if r2 > 0.97 and r2 - r1 > 0.2 else "rank-2 did NOT separate"))
    ks = [F for label, F in squeezed if label.startswith("K=")]
    print(f"squeezed: F(K=2,4,8) = {ks} -> "
          + ("fidelity improves with K (graceful out-of-family degradation)"
             if ks == sorted(ks) and ks[-1] > ks[0] else
             "no monotone improvement with K"))


if __name__ == "__main__":
    main()
