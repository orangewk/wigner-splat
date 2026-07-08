"""Experiment 08 (positivity) — observation step, single mode.

Issue #8: a signed Gaussian splat mixture is NOT guaranteed to correspond to a
positive-semidefinite density operator. Before choosing a fix (Kenfack-type
constraint / eigenvalue penalty / post-hoc projection) we MEASURE how unphysical
the current fitter's output actually is.

Route (single mode, cheap): the Weyl transform is a bijection between phase-space
functions and operators, so a splat's Hermitian operator rho_mix has well-defined
Fock matrix elements even when it is not a state:

    rho[n, m] = tr(rho_mix |m><n|) = 2 pi * integral W_mix(z) W_{|m><n|}(z) dz

with W_{|m><n|} = wigner_from_rho(E_mn).  We build rho_mix this way, then read
its eigenvalues.  min eig < 0 => not a physical state.

Two checks:
  (A) VALIDATE the numerical W->rho inversion on a KNOWN physical state (cat):
      round-trip rho_cat -> W_cat -> rho_rec must recover rho_cat and stay PSD.
  (B) OBSERVE min eigenvalue of the fitted splat's rho_mix.
"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fit import fit, histogram_targets  # noqa: E402
from wigner_splat.fock import cat_fock, wigner_from_rho, wigner_overlap  # noqa: E402
from wigner_splat.states import CatState  # noqa: E402

N_MAX = 16
ALPHA = 1.5
GRID_LIM = 5.0
GRID_N = 161


def operator_wigner_basis(n_max, X, P):
    """W_{|m><n|}(z) for all m, n < n_max on the grid. Returns (n_max, n_max, *X)."""
    basis = np.empty((n_max, n_max) + X.shape)
    for m in range(n_max):
        for n in range(n_max):
            E = np.zeros((n_max, n_max), dtype=complex)
            E[m, n] = 1.0
            basis[m, n] = wigner_from_rho(E, X, P)
    return basis


def rho_from_wigner(W_state, basis, xs):
    """rho[n, m] = 2 pi * integral W_state * W_{|m><n|}."""
    n_max = basis.shape[0]
    rho = np.empty((n_max, n_max), dtype=complex)
    for m in range(n_max):
        for n in range(n_max):
            rho[n, m] = wigner_overlap(W_state, basis[m, n], xs)
    return rho


def report(tag, rho):
    ev = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    neg = ev[ev < 0]
    print(f"[{tag}] trace={np.real(np.trace(rho)):+.4f}  "
          f"min_eig={ev.min():+.4e}  max_eig={ev.max():+.4f}")
    print(f"        negative eigs: count={len(neg)}  "
          f"sum={neg.sum():+.4e}  (negativity = |sum of neg eigs|)")
    return ev


def main():
    xs = np.linspace(-GRID_LIM, GRID_LIM, GRID_N)
    X, P = np.meshgrid(xs, xs)

    print(f"single-mode cat alpha={ALPHA}, n_max={N_MAX}, "
          f"grid={GRID_N}^2 on [-{GRID_LIM},{GRID_LIM}]")
    print("building operator Wigner basis W_{|m><n|} ...")
    basis = operator_wigner_basis(N_MAX, X, P)

    # (A) validation: known physical state must round-trip and stay PSD
    psi_cat = cat_fock(ALPHA, parity=+1, n_max=N_MAX)  # Fock state vector
    rho_cat = np.outer(psi_cat, psi_cat.conj())        # pure-state density matrix
    W_cat = wigner_from_rho(rho_cat, X, P)
    rho_rec = rho_from_wigner(W_cat, basis, xs)
    err = np.linalg.norm(rho_rec - rho_cat) / np.linalg.norm(rho_cat)
    print("\n=== (A) VALIDATION: rho_cat -> W -> rho_rec ===")
    print(f"relative Frobenius error ||rho_rec - rho_cat|| / ||rho_cat|| = {err:.3e}")
    report("rho_cat  (exact)", rho_cat)
    report("rho_rec  (round-trip)", rho_rec)

    # (B) observation: fitted splat's operator
    print("\n=== (B) OBSERVATION: fitted splat -> rho_mix ===")
    cat = CatState(ALPHA, parity=+1)
    angles = np.linspace(0, np.pi, 12, endpoint=False)
    data = cat.sample_homodyne(angles, 4000, rng=42)
    mix = fit(data, K=4, iters=800, seed=0, densify_every=100, K_max=12)
    W_splat = mix.wigner(X, P)
    rho_splat = rho_from_wigner(W_splat, basis, xs)
    f = wigner_overlap(W_splat, W_cat, xs)
    print(f"splat: K={len(mix.w)}  fidelity_vs_cat={f:.4f}")
    report("rho_splat", rho_splat)


if __name__ == "__main__":
    main()
