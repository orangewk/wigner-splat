"""Experiment 30 alignment toolkit (derivation.md §3 and §6).

Closed forms only: the Autonne-Takagi factorization behind A1's converse,
the b <-> alpha translation, A1's constructive recipe assembled from
gaussact's tested Bloch-Messiah factors, the undisplaced-atom norm closed
form with its certified geometric tail bound (A1(iii), E2), and the exact
Fraction-arithmetic epsilon-convention conversions (A5). No epistemic
status is authored here (derivation.md §9 is the sole authoring
location); no evaluated run output lives here.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from wigner_splat import gaussact


def takagi(A):
    """Autonne-Takagi `A = V diag(s) V^T` for complex symmetric 2x2:
    returns (V unitary, s descending >= 0).

    Route: SVD `A = W S X^H`; for symmetric A the matrix `D = W^H bar(X)`
    is unitary, commutes with S blockwise, and is symmetric on degenerate
    blocks, so `V = W D^{1/2}` (principal square root of the symmetrized
    D) satisfies `V S V^T = W S D W^T = A`. Correctness is refereed at
    runtime by E1 (gate F1) and pinned in tests, not assumed."""
    A = np.asarray(A, dtype=complex)
    if A.shape != (2, 2) or np.max(np.abs(A - A.T)) > 1e-10 * max(
        1.0, float(np.max(np.abs(A)))
    ):
        raise ValueError("takagi needs a symmetric 2x2 matrix")
    W, s, Xh = np.linalg.svd(A)
    X = Xh.conj().T
    D = W.conj().T @ X.conj()
    D = (D + D.T) / 2.0
    evals, evecs = np.linalg.eig(D)
    evals = np.where(np.abs(evals) < 1e-14, 1.0, evals)
    sqrtD = evecs @ np.diag(np.sqrt(evals.astype(complex))) @ np.linalg.inv(evecs)
    V = W @ sqrtD
    return V, s


def alpha_from_b(A, b):
    """A1(ii): `alpha = (I - A bar(A))^{-1} (b + A bar(b))`."""
    A = np.asarray(A, dtype=complex)
    b = np.asarray(b, dtype=complex).reshape(2)
    return np.linalg.solve(np.eye(2) - A @ A.conj(), b + A @ np.conj(b))


def b_from_alpha(A, alpha):
    """A1(ii): `b = alpha - A bar(alpha)`."""
    A = np.asarray(A, dtype=complex)
    alpha = np.asarray(alpha, dtype=complex).reshape(2)
    return alpha - A @ np.conj(alpha)


def recipe_state(A, b):
    """A1's constructive route for target stellar data `(A, b)`:
    Takagi -> two single-mode squeezers `r_i = artanh sigma_i` -> passive
    `V^T` -> displacement `alpha_from_b(A, b)`. Returns a gaussact
    PQState whose data must equal `(A, b)` up to float error (refereed
    by E1 and tests)."""
    V, s = takagi(A)
    if s[0] >= 1.0:
        raise ValueError("||A|| >= 1 admits no normalizable state (A1(iii))")
    st = gaussact.pq_state(np.array([[1.0 + 0j]]))
    st = gaussact.squeeze1(st, 0, math.atanh(float(s[0])))
    st = gaussact.squeeze1(st, 1, math.atanh(float(s[1])))
    st = gaussact.passive(st, V.T)
    return gaussact.displace(st, alpha_from_b(A, b))


def norm_sq_closed(sigma1, sigma2):
    """A1(iii): squared Fock norm of the undisplaced atom
    `exp((sigma1/2) w1^2 + (sigma2/2) w2^2)` = prod (1 - sigma_i^2)^{-1/2}."""
    return 1.0 / math.sqrt((1.0 - sigma1 * sigma1) * (1.0 - sigma2 * sigma2))


def mode_tail_bound(last_term_sq, sigma):
    """Certified per-mode tail bound (E2): the term ratio
    `t_{n+1}/t_n = sigma^2 (2n+1)/(2n+2) < sigma^2` makes the tail after
    the last computed term dominated by the geometric series
    `last * sigma^2 / (1 - sigma^2)`."""
    return last_term_sq * sigma * sigma / (1.0 - sigma * sigma)


# --- exact epsilon-convention conversions (A5) -----------------------------


def fidelity_of_delta_sq(d2):
    """Exact `F = (1 - d2/2)^2` for rational `d2 = delta^2`."""
    d2 = Fraction(d2)
    return (1 - d2 / 2) ** 2


def delta_sq_of_fidelity(F):
    """Exact `delta^2 = 2 (1 - sqrt(F))` for rational perfect-square `F`
    (the E4 grid feeds squares, so sqrt is exact; raises otherwise)."""
    F = Fraction(F)
    num, den = F.numerator, F.denominator
    rn, rd = math.isqrt(num), math.isqrt(den)
    if rn * rn != num or rd * rd != den:
        raise ValueError("delta_sq_of_fidelity needs an exact-square Fraction")
    return 2 * (1 - Fraction(rn, rd))


def eps_note_exact(delta_star):
    """Exact note-convention threshold `1 - (1 - delta*^2/2)^2` from a
    committed float radius (binary value taken exactly)."""
    d = Fraction(delta_star)
    return 1 - (1 - d * d / 2) ** 2


def float_down(exact):
    """Largest float <= the exact Fraction (safe rounding for 'for all
    eps < threshold' claims: down weakens)."""
    f = float(exact)
    while Fraction(f) > Fraction(exact):
        f = math.nextafter(f, -math.inf)
    return f


def float_up(exact):
    """Smallest float >= the exact Fraction (safe for upper bounds)."""
    f = float(exact)
    while Fraction(f) < Fraction(exact):
        f = math.nextafter(f, math.inf)
    return f
