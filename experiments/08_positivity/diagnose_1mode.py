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

Weyl-symbol subtlety (why the basis is decomposed below): |m><n| for m != n is
NOT Hermitian, so its Weyl/Wigner transform is genuinely COMPLEX-valued -- but
fock.wigner_from_rho unconditionally takes np.real(term) at every accumulation
step (it is designed for Hermitian density matrices, where that is exact).
Handing it |m><n| directly silently drops the imaginary part of that operator's
Weyl symbol, so a naive rho[n, m] recovers only Re[tr(rho_mix |m><n|)] for the
off-diagonals -- wrong (not merely imprecise) whenever rho_mix has genuinely
complex off-diagonals, i.e. whenever a splat component has mu_p != 0.  We avoid
that by splitting each |m><n| into its Hermitian part ((A + A^dagger)/2) and its
"i-Hermitian" part ((A - A^dagger)/(2i)) and calling wigner_from_rho only on
those genuinely-Hermitian inputs (where it is exact), then recombining as
Ws + i*Wa.  This lifts part (B) from min_eig=-2.02e-2 / negativity=4.52e-2 (the
np.real()-truncated values) to the correct -2.42e-2 / 5.28e-2.  Full writeup and
a machine-precision cross-check against the closed-form fock_project.rho_from_splat
live in tests/test_fock_project.py (_corrected_operator_wigner_basis).  Part (A)
is a real state, so its off-diagonals are real and the correction is a no-op for
it (the cat round-trip is unaffected either way).

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
    """Real (Ws) and imaginary (Wa) parts of the Weyl symbol of |m><n|.

    Weyl(|m><n|) = Ws + i*Wa, obtained by feeding wigner_from_rho only the
    genuinely-Hermitian pieces of |m><n| (see module docstring). For m == n the
    operator is already Hermitian, so Wa[m, m] stays zero. Returns two
    (n_max, n_max, *X) arrays.
    """
    Ws = np.empty((n_max, n_max) + X.shape)
    Wa = np.zeros((n_max, n_max) + X.shape)
    for m in range(n_max):
        for n in range(n_max):
            Hs = np.zeros((n_max, n_max), dtype=complex)  # (|m><n| + |n><m|)/2
            Hs[m, n] += 0.5
            Hs[n, m] += 0.5
            Ws[m, n] = wigner_from_rho(Hs, X, P)
            if m != n:
                Ha = np.zeros((n_max, n_max), dtype=complex)  # (|m><n| - |n><m|)/(2i)
                Ha[m, n] += 1 / (2j)
                Ha[n, m] += -1 / (2j)
                Wa[m, n] = wigner_from_rho(Ha, X, P)
    return Ws, Wa


def rho_from_wigner(W_state, Ws, Wa, xs):
    """rho[n, m] = tr(rho_state |m><n|) = 2 pi * integral W_state * Weyl(|m><n|).

    Weyl(|m><n|) is complex for m != n, so both its real (Ws) and imaginary
    (Wa) parts are integrated against W_state and recombined.
    """
    n_max = Ws.shape[0]
    rho = np.empty((n_max, n_max), dtype=complex)
    for m in range(n_max):
        for n in range(n_max):
            re = wigner_overlap(W_state, Ws[m, n], xs)
            im = wigner_overlap(W_state, Wa[m, n], xs)
            rho[n, m] = re + 1j * im
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
    Ws, Wa = operator_wigner_basis(N_MAX, X, P)

    # (A) validation: known physical state must round-trip and stay PSD
    psi_cat = cat_fock(ALPHA, parity=+1, n_max=N_MAX)  # Fock state vector
    rho_cat = np.outer(psi_cat, psi_cat.conj())        # pure-state density matrix
    W_cat = wigner_from_rho(rho_cat, X, P)
    rho_rec = rho_from_wigner(W_cat, Ws, Wa, xs)
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
    rho_splat = rho_from_wigner(W_splat, Ws, Wa, xs)
    f = wigner_overlap(W_splat, W_cat, xs)
    print(f"splat: K={len(mix.w)}  fidelity_vs_cat(Wigner overlap)={f:.4f}")
    report("rho_splat (raw)", rho_splat)
    f_raw = np.real(psi_cat.conj() @ rho_splat @ psi_cat)
    print(f"        <cat|rho_splat|cat> = {f_raw:.4f}")

    # --- candidate fix (c): post-hoc projection onto the PSD cone ---
    # clip negative eigenvalues to 0, renormalize trace to 1.
    print("\n=== (C) POST-HOC PSD PROJECTION of rho_splat ===")
    rho_h = (rho_splat + rho_splat.conj().T) / 2
    ev, U = np.linalg.eigh(rho_h)
    ev_clip = np.clip(ev, 0.0, None)
    rho_proj = (U * ev_clip) @ U.conj().T
    rho_proj = rho_proj / np.real(np.trace(rho_proj))  # renormalize
    report("rho_proj", rho_proj)
    f_proj = np.real(psi_cat.conj() @ rho_proj @ psi_cat)
    print(f"        <cat|rho_proj|cat> = {f_proj:.4f}   "
          f"dF vs raw overlap = {f_proj - f:+.4f}")


if __name__ == "__main__":
    main()
