"""Exact two-mode Gaussian-unitary action on finite-stellar-rank states.

Experiment 26 toolkit (see experiments/26_gauss_invariance/derivation.md for
the derivation of the closed forms and the invariance claims this code is
meant to test).

A finite-stellar-rank state is carried as exact (P, A, b) data,

    f(w) = P(w) * exp((1/2) w^T A w + b^T w),

P a complex polynomial in the raw MONOMIAL basis (P[m, n] multiplies
w1^m w2^n, with NO 1/sqrt(m! n!) -- the Fock-normalized c_mn of
stellar2.fock_stellar live one basis change away, see fock_coeffs), A a 2x2
complex symmetric matrix, b in C^2. Every operation keeps the exact overall
constant folded into P, so Gaussian unitaries preserve the Hilbert norm
exactly (tested, not assumed).

Why this exists: applying a Gaussian unitary in a truncated Fock basis is
approximate and cutoff-dependent, which poisons any claim about invariants of
the transformed state. Here each unitary is split into disentangled
Bloch-Messiah factors (passive rotations, single- and two-mode squeezers,
displacements) and each factor acts in closed form. The only nontrivial
factor is the normally-ordered annihilation part exp(-(s*/2) a^2), which on
stellar data is a Gaussian-conjugated heat flow exp((tau/2) d^T S d); its
closed form (heat_step) is a finite Hermite-type smoothing of P composed
with an affine substitution and an exact scalar. That closed form is
validated in tests/test_gaussact.py against two independent referees: a
direct tau-series of the generator built from scratch inside the test, and a
truncated-Fock brute force (expm via eigendecomposition at cutoff 42).

Epistemic status of top_partition: the (P, A, b) arithmetic is exact up to
float rounding, but the root-multiplicity clustering of the top form is a
NUMERICAL operation -- np.roots scatters an exact m-fold root by roughly
eps^(1/m). Every top_partition result therefore carries its ambiguity
margin (min_intercluster_distance); callers must check it and distrust any
partition whose margin sits within a decade of the clustering tolerance.
"""

from __future__ import annotations

import math
from collections import namedtuple

import numpy as np

from .stellar2 import gaussian_term_fock_coeffs, random_u2


_OFFDIAG = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


class GaussActError(RuntimeError):
    """Raised when an input leaves the exact-action domain (asymmetric A,
    focal det K ~ 0, non-unitary U, ...)."""


# ---------------------------------------------------------------------------
# state container and polynomial helpers
# ---------------------------------------------------------------------------

PQState = namedtuple("PQState", ["P", "A", "b"])
PQState.__doc__ = """Stellar data f(w) = P(w) exp((1/2) w^T A w + b^T w).

P: 2-D complex monomial coefficients, A: 2x2 complex symmetric, b: C^2.
Build through pq_state(), which validates and trims.
"""


def pq_state(P, A=None, b=None):
    """Validated PQState: symmetrize A (error above 1e-12 relative asymmetry)
    and trim trailing all-zero rows/cols of P (1e-15 relative, keep >= (1,1)).

    Normalizability (operator norm ||A|| < 1) is a CALLER invariant, not
    checked here: heat_step and the squeezer factors assume it for their
    focal-point domain argument (derivation.md Lemma C), and norm() is the
    runtime handle for verifying it when in doubt.
    """
    p = np.array(P, dtype=complex)
    if p.ndim != 2:
        raise GaussActError("P must be a 2-D monomial coefficient array")
    a = np.zeros((2, 2), dtype=complex) if A is None else np.array(A, dtype=complex)
    if a.shape != (2, 2):
        raise GaussActError("A must be 2x2")
    scale = np.max(np.abs(a))
    if scale > 0.0 and np.max(np.abs(a - a.T)) > 1e-12 * scale:
        raise GaussActError("A is not symmetric (relative asymmetry > 1e-12)")
    a = (a + a.T) / 2.0
    bv = np.zeros(2, dtype=complex) if b is None else np.asarray(b, dtype=complex)
    bv = bv.reshape(2).astype(complex)
    return PQState(_trim(p), a, bv)


def _trim(p):
    """Drop trailing rows/cols with all |entries| <= 1e-15 max|P|."""
    mx = np.max(np.abs(p))
    if mx == 0.0:
        return np.zeros((1, 1), dtype=complex)
    keep = np.abs(p) > 1e-15 * mx
    m = int(np.max(np.nonzero(keep.any(axis=1))[0])) + 1
    n = int(np.max(np.nonzero(keep.any(axis=0))[0])) + 1
    return p[:m, :n].copy()


def _poly_mul(a, b):
    """Product of two 2-D monomial coefficient arrays (2-D convolution)."""
    out = np.zeros(
        (a.shape[0] + b.shape[0] - 1, a.shape[1] + b.shape[1] - 1), dtype=complex
    )
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if a[i, j] != 0.0:
                out[i : i + b.shape[0], j : j + b.shape[1]] += a[i, j] * b
    return out


def _poly_affine_sub(p, mat, shift):
    """Coefficients of P(M w + m), by expanding powers of the two affine
    forms M[0,0] w1 + M[0,1] w2 + m[0] and M[1,0] w1 + M[1,1] w2 + m[1]."""
    mat = np.asarray(mat, dtype=complex)
    shift = np.asarray(shift, dtype=complex).reshape(2)
    l1 = np.array([[shift[0], mat[0, 1]], [mat[0, 0], 0.0]], dtype=complex)
    l2 = np.array([[shift[1], mat[1, 1]], [mat[1, 0], 0.0]], dtype=complex)
    pw1 = [np.ones((1, 1), dtype=complex)]
    for _ in range(p.shape[0] - 1):
        pw1.append(_poly_mul(pw1[-1], l1))
    pw2 = [np.ones((1, 1), dtype=complex)]
    for _ in range(p.shape[1] - 1):
        pw2.append(_poly_mul(pw2[-1], l2))
    d = p.shape[0] + p.shape[1] - 1
    out = np.zeros((d, d), dtype=complex)
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            if p[i, j] != 0.0:
                t = _poly_mul(pw1[i], pw2[j])
                out[: t.shape[0], : t.shape[1]] += p[i, j] * t
    return out


def _poly_diff_quadform(p, sigma):
    """(1/2)(S11 d1^2 + 2 S12 d1 d2 + S22 d2^2) P on monomial coefficients."""
    m, n = p.shape
    out = np.zeros_like(p)
    if m >= 3:
        i = np.arange(m - 2, dtype=float)
        out[:-2, :] += 0.5 * sigma[0, 0] * ((i + 1.0) * (i + 2.0))[:, None] * p[2:, :]
    if n >= 3:
        j = np.arange(n - 2, dtype=float)
        out[:, :-2] += 0.5 * sigma[1, 1] * ((j + 1.0) * (j + 2.0))[None, :] * p[:, 2:]
    if m >= 2 and n >= 2:
        i = np.arange(m - 1, dtype=float)
        j = np.arange(n - 1, dtype=float)
        out[:-1, :-1] += sigma[0, 1] * np.outer(i + 1.0, j + 1.0) * p[1:, 1:]
    return out


def _hermite_smooth(p, sigma):
    """H_Sigma P = sum_k (1/k!) ((1/2) d^T Sigma d)^k P.

    Finite sum: each application lowers total degree by 2, so it stops on its
    own after at most ceil(deg/2) + 1 terms.
    """
    acc = p.copy()
    term = p
    k = 0
    while True:
        k += 1
        term = _poly_diff_quadform(term, sigma) / k
        if not np.any(term):
            return acc
        acc = acc + term


# ---------------------------------------------------------------------------
# the one nontrivial factor: Gaussian-conjugated heat flow
# ---------------------------------------------------------------------------

def heat_step(state, S, tau):
    """Exact exp((tau/2) d^T S d) on P e^Q, S symmetric, d = (d/dw1, d/dw2).

    Closed form (derivation.md of experiment 26, cross-checked by
    characteristics/Riccati):

        K  = I - tau S A                (focal point if det K = 0)
        A' = A K^-1                     (symmetric)
        b' = (I - tau A S)^-1 b
        Sigma = tau K^-1 S              (symmetric smoothing matrix)
        scalar = det(K)^(-1/2) exp((tau/2) b^T K^-1 S b)
        P'(w) = scalar [H_Sigma P](K^-1 (w + tau S b))

    det(K)^(-1/2) takes the principal branch of the square root; the branch
    choice only affects a global phase of the state, which no downstream
    quantity (norms, zeros, top forms, censuses) uses.
    """
    P, A, b = state
    S = np.asarray(S, dtype=complex)
    s_scale = np.max(np.abs(S))
    if s_scale > 0.0 and np.max(np.abs(S - S.T)) > 1e-12 * s_scale:
        raise GaussActError("S must be symmetric")
    tau = complex(tau)
    K = np.eye(2, dtype=complex) - tau * (S @ A)
    det_k = K[0, 0] * K[1, 1] - K[0, 1] * K[1, 0]
    if abs(det_k) < 1e-12:
        raise GaussActError("heat_step at a focal point: |det K| < 1e-12")
    k_inv = np.linalg.inv(K)
    a_new = A @ k_inv
    scale = np.max(np.abs(a_new))
    if scale > 0.0 and np.max(np.abs(a_new - a_new.T)) > 1e-10 * scale:
        raise GaussActError("A K^-1 lost symmetry (ill-conditioned K)")
    a_new = (a_new + a_new.T) / 2.0
    b_new = np.linalg.inv(np.eye(2, dtype=complex) - tau * (A @ S)) @ b
    sigma = tau * (k_inv @ S)
    sigma = (sigma + sigma.T) / 2.0
    scalar = np.exp((tau / 2.0) * (b @ (k_inv @ (S @ b)))) / np.sqrt(det_k)
    shift = tau * (k_inv @ (S @ b))
    p_new = scalar * _poly_affine_sub(_hermite_smooth(P, sigma), k_inv, shift)
    return pq_state(p_new, a_new, b_new)


# ---------------------------------------------------------------------------
# elementary Gaussian factors
# ---------------------------------------------------------------------------

def linear_sub(state, M):
    """f(w) -> f(M w) for invertible M (passive rotations, sech scalings)."""
    P, A, b = state
    M = np.asarray(M, dtype=complex)
    if abs(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]) < 1e-12:
        raise GaussActError("linear_sub needs invertible M")
    p_new = _poly_affine_sub(P, M, np.zeros(2, dtype=complex))
    return pq_state(p_new, M.T @ A @ M, M.T @ b)


def displace(state, alpha):
    """Bargmann displacement D(alpha) = exp(alpha . a^dag - h.c.):

        f'(w) = exp(alpha^T w - |alpha|^2 / 2) f(w - conj(alpha)),

    so A is untouched, b -> b + alpha - A conj(alpha), and P absorbs the
    shifted-exponent constant exactly.
    """
    P, A, b = state
    a = np.asarray(alpha, dtype=complex).reshape(2)
    ac = np.conj(a)
    const = np.exp(
        -0.5 * float(np.sum(np.abs(a) ** 2)) + 0.5 * (ac @ (A @ ac)) - b @ ac
    )
    p_new = const * _poly_affine_sub(P, np.eye(2, dtype=complex), -ac)
    return pq_state(p_new, A, b + a - A @ ac)


def passive(state, U):
    """Passive U(2) rotation: the new stellar function is g(w) = f(U w).

    Same U-versus-U^T bookkeeping caveat as stellar2.rotated (which this
    matches by construction): whether U or U^T is "the" beamsplitter matrix
    is a labeling choice no census invariant depends on.
    """
    U = np.asarray(U, dtype=complex)
    if np.linalg.norm(U @ U.conj().T - np.eye(2)) >= 1e-10:
        raise GaussActError("U is not unitary")
    return linear_sub(state, U)


def squeeze1(state, mode, zeta):
    """Single-mode squeezer exp((zeta/2) a_i^dag^2 - (zeta*/2) a_i^2), i = mode.

    With zeta = rho e^{i theta}, s = e^{i theta} tanh(rho), mu = 1/cosh(rho),
    the disentangled order e^{(s/2) a^dag^2} mu^{a^dag a + 1/2} e^{-(s*/2) a^2}
    acts on f as: heat_step(S = E_ii, tau = -s*), then w_i -> mu w_i, then
    A[i,i] += s, then P *= sqrt(mu).

    Sanity anchor: on vacuum this gives sqrt(mu) e^{(s/2) w_i^2}, i.e. the
    standard squeezed vacuum (1 - |s|^2)^{1/4} e^{(s/2) w^2}.
    """
    if mode not in (0, 1):
        raise GaussActError("mode must be 0 or 1")
    zeta = complex(zeta)
    rho = abs(zeta)
    if rho == 0.0:
        return pq_state(state.P, state.A, state.b)
    s = (zeta / rho) * math.tanh(rho)
    mu = 1.0 / math.cosh(rho)
    S = np.zeros((2, 2), dtype=complex)
    S[mode, mode] = 1.0
    out = heat_step(state, S, -np.conj(s))
    M = np.eye(2, dtype=complex)
    M[mode, mode] = mu
    out = linear_sub(out, M)
    a_new = out.A.copy()
    a_new[mode, mode] += s
    return pq_state(out.P * math.sqrt(mu), a_new, out.b)


def squeeze2(state, zeta):
    """Two-mode squeezer exp(zeta a1^dag a2^dag - zeta* a1 a2).

    With zeta = rho e^{i theta}, Lam = e^{i theta} tanh(rho),
    mu = 1/cosh(rho): heat_step(S = offdiag, tau = -Lam*) (= exp(-Lam* d1 d2)),
    then w -> mu w, then A += Lam offdiag (adds Lam w1 w2), then P *= mu.

    Sanity anchors: on vacuum -> mu e^{Lam w1 w2}, matching the
    stellar2.tmsv_term normalization sqrt(1 - lam^2) = sech(rho); on |1,1>
    with real zeta = r the polynomial comes out proportional to
    w1 w2 - sinh(r) cosh(r) (pinned exactly in tests).
    """
    zeta = complex(zeta)
    rho = abs(zeta)
    if rho == 0.0:
        return pq_state(state.P, state.A, state.b)
    lam = (zeta / rho) * math.tanh(rho)
    mu = 1.0 / math.cosh(rho)
    out = heat_step(state, _OFFDIAG, -np.conj(lam))
    out = linear_sub(out, mu * np.eye(2, dtype=complex))
    return pq_state(out.P * mu, out.A + lam * _OFFDIAG, out.b)


# ---------------------------------------------------------------------------
# full Gaussian unitary
# ---------------------------------------------------------------------------

def gauss_unitary(state, params):
    """Apply G = D(alpha) U_post S2(zeta12) S1(zeta1 on 0) S1(zeta2 on 1) U_pre.

    params keys: "U_pre", "U_post" (2x2 unitary or None), "zeta1", "zeta2",
    "zeta12" (complex, 0/None for identity), "alpha" (C^2 or None). Operator
    order above means the state sees passive(U_pre) first, then the three
    squeezers, then passive(U_post), then displace(alpha).
    """
    out = state
    u_pre = params.get("U_pre")
    if u_pre is not None:
        out = passive(out, u_pre)
    out = squeeze1(out, 0, params.get("zeta1") or 0.0)
    out = squeeze1(out, 1, params.get("zeta2") or 0.0)
    out = squeeze2(out, params.get("zeta12") or 0.0)
    u_post = params.get("U_post")
    if u_post is not None:
        out = passive(out, u_post)
    alpha = params.get("alpha")
    if alpha is not None:
        out = displace(out, alpha)
    return out


def random_gauss_params(seed, r_max=0.6, alpha_max=1.0):
    """Seeded generic gauss_unitary parameters: Haar-ish U(2) pre/post frames
    (via stellar2.random_u2), squeezing magnitudes uniform on [0, r_max] with
    uniform phases, displacement components uniform on the |alpha| <= alpha_max
    disk."""
    rng = np.random.default_rng(seed)

    def zeta():
        return rng.uniform(0.0, r_max) * np.exp(2j * math.pi * rng.uniform())

    def disk():
        # sqrt radius for area-uniform sampling of the disk
        return alpha_max * math.sqrt(rng.uniform()) * np.exp(2j * math.pi * rng.uniform())

    return {
        "U_pre": random_u2(int(rng.integers(1 << 32))),
        "zeta1": zeta(),
        "zeta2": zeta(),
        "zeta12": zeta(),
        "U_post": random_u2(int(rng.integers(1 << 32))),
        "alpha": np.array([disk(), disk()]),
    }


# ---------------------------------------------------------------------------
# readouts
# ---------------------------------------------------------------------------

def _fact_roots(cutoff):
    fact = np.ones(cutoff)
    for k in range(1, cutoff):
        fact[k] = fact[k - 1] * k
    return np.sqrt(fact)


def fock_coeffs(state, cutoff):
    """Fock coefficients c_mn (stellar2 convention f = sum c_mn w1^m w2^n /
    sqrt(m! n!)) of P e^Q: pure-Gaussian coefficients from the stellar2
    Taylor recursion, multiplied by P in the Taylor basis."""
    P, A, b = state
    term = (1.0, b[0], b[1], A[0, 0] / 2.0, A[0, 1], A[1, 1] / 2.0)
    c = gaussian_term_fock_coeffs(term, cutoff)
    root = _fact_roots(cutoff)
    t = c / np.outer(root, root)
    out = np.zeros((cutoff, cutoff), dtype=complex)
    for i in range(min(P.shape[0], cutoff)):
        for j in range(min(P.shape[1], cutoff)):
            if P[i, j] != 0.0:
                out[i:, j:] += P[i, j] * t[: cutoff - i, : cutoff - j]
    return out * np.outer(root, root)


def norm(state, cutoff=48):
    """Hilbert norm sqrt(sum |c_mn|^2) over the cutoff block.

    Returns (value, last_shell_mass): last_shell_mass is the |c|^2 mass on
    the outermost L-shaped shell (m = cutoff-1 or n = cutoff-1) -- the
    convergence handle callers must check before trusting value.
    """
    c = fock_coeffs(state, cutoff)
    total = float(np.sum(np.abs(c) ** 2))
    shell = float(np.sum(np.abs(c[-1, :]) ** 2) + np.sum(np.abs(c[:-1, -1]) ** 2))
    return math.sqrt(total), shell


def stellar_callable(state):
    """Vectorized f(w1, w2) = P(w1, w2) exp((1/2) w^T A w + b^T w), shaped for
    stellar2.census."""
    P, A, b = state

    def f(w1, w2):
        w1 = np.asarray(w1, dtype=complex)
        w2 = np.asarray(w2, dtype=complex)
        v1 = np.stack([w1**m for m in range(P.shape[0])])
        v2 = np.stack([w2**n for n in range(P.shape[1])])
        poly = np.einsum("mn,m...,n...->...", P, v1, v2)
        expo = (
            0.5 * (A[0, 0] * w1 * w1 + A[1, 1] * w2 * w2)
            + A[0, 1] * w1 * w2
            + b[0] * w1
            + b[1] * w2
        )
        return poly * np.exp(expo)

    return f


# ---------------------------------------------------------------------------
# top form and its root-multiplicity partition
# ---------------------------------------------------------------------------

def top_form(state, rel_tol=1e-9):
    """Top total-degree homogeneous part of P.

    d is the largest m + n with |P[m, n]| > rel_tol max|P| (the threshold
    keeps trailing numerical dust from masquerading as top degree). Returns
    (d, coeffs) with coeffs[j] the coefficient of w1^(d-j) w2^j.
    """
    P = state.P
    mx = np.max(np.abs(P))
    if mx == 0.0:
        return 0, np.zeros(1, dtype=complex)
    m_idx, n_idx = np.nonzero(np.abs(P) > rel_tol * mx)
    d = int(np.max(m_idx + n_idx))
    coeffs = np.zeros(d + 1, dtype=complex)
    for j in range(d + 1):
        i = d - j
        if i < P.shape[0] and j < P.shape[1]:
            coeffs[j] = P[i, j]
    return d, coeffs


def top_partition(state, tol=1e-6):
    """Root-multiplicity partition of the top form on CP^1.

    The form sum_j coeffs[j] w1^(d-j) w2^j factors over CP^1; in the chart
    t = w2 / w1 its roots are the roots of p(t) = sum_j coeffs[j] t^j, plus
    a root at infinity with multiplicity d - deg(p) when the t-degree is
    deficient (near-zero leading coefficients, <= 1e-12 relative, are
    trimmed into the infinity multiplicity). Roots are compared in the
    Fubini-Study chordal metric d(t, u) = |t - u| / sqrt((1+|t|^2)(1+|u|^2)),
    distance-to-infinity 1/sqrt(1+|t|^2), and single-linkage clustered at
    threshold tol.

    Returns (multiplicities, min_intercluster_distance) with multiplicities
    a descending tuple of cluster sizes and the distance np.inf when there
    is at most one cluster. NUMERICAL caveat: np.roots scatters an exact
    m-fold root by ~eps^(1/m), so tol must sit above that scatter, and a
    min_intercluster_distance below ~10 tol means the clustering was
    ambiguous -- callers must check it.
    """
    d, coeffs = top_form(state)
    if d == 0:
        return (), np.inf
    mx = np.max(np.abs(coeffs))
    deg = int(np.max(np.nonzero(np.abs(coeffs) > 1e-12 * mx)[0]))
    finite = np.roots(coeffs[deg::-1]) if deg > 0 else np.array([], dtype=complex)
    # normalized projective representatives; chordal distance = |cross product|
    reps = [
        np.array([t, 1.0], dtype=complex) / math.sqrt(1.0 + abs(t) ** 2)
        for t in finite
    ]
    reps += [np.array([1.0, 0.0], dtype=complex)] * (d - deg)
    n = len(reps)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist[i, j] = dist[j, i] = abs(
                reps[i][0] * reps[j][1] - reps[i][1] * reps[j][0]
            )

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):  # single linkage = components of the dist < tol graph
        for j in range(i + 1, n):
            if dist[i, j] < tol:
                parent[find(i)] = find(j)

    labels = [find(i) for i in range(n)]
    sizes = sorted((labels.count(r) for r in set(labels)), reverse=True)
    inter = np.inf
    for i in range(n):
        for j in range(i + 1, n):
            if labels[i] != labels[j]:
                inter = min(inter, dist[i, j])
    return tuple(sizes), float(inter)
