"""Tests for wigner_splat/gaussact.py: exact Gaussian action on (P, A, b).

The heat_step closed form is the load-bearing piece, so it gets two
independent referees that share no code with the module: a tau-series of the
generator with all polynomial arithmetic rebuilt inside this file (T1), and
a truncated-Fock brute force where each Bloch-Messiah factor is exponentiated
by eigendecomposition at cutoff 42 and compared coefficient-by-coefficient
(T3). The remaining tests pin exact anchors (squeeze2 on |1,1>), unitarity of
composed random Gaussians, Fock/stellar consistency, invariance of the
top-form root partition, and the census-visible fixed-radius threshold
lam* = sqrt(2) - 1 of squeeze2(|1,1>).
"""

import math

import numpy as np
import pytest

from wigner_splat.gaussact import (
    GaussActError,
    displace,
    fock_coeffs,
    gauss_unitary,
    heat_step,
    norm,
    passive,
    pq_state,
    random_gauss_params,
    squeeze1,
    squeeze2,
    stellar_callable,
    top_partition,
)
from wigner_splat.stellar2 import census, fock_stellar, random_u2, rotated


# ---------------------------------------------------------------------------
# input states and independent polynomial arithmetic (no gaussact helpers)
# ---------------------------------------------------------------------------

def _state_11():
    p = np.zeros((2, 2), dtype=complex)
    p[1, 1] = 1.0
    return pq_state(p)


def _state_20():
    p = np.zeros((3, 1), dtype=complex)
    p[2, 0] = 1.0 / math.sqrt(2.0)
    return pq_state(p)


def _state_trefoil():
    p = np.zeros((3, 4), dtype=complex)
    p[2, 0] = 0.8 / math.sqrt(2.0)
    p[0, 3] = 0.6 / math.sqrt(6.0)
    return pq_state(p)


def _pmul(a, b):
    out = np.zeros(
        (a.shape[0] + b.shape[0] - 1, a.shape[1] + b.shape[1] - 1), dtype=complex
    )
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if a[i, j] != 0.0:
                out[i : i + b.shape[0], j : j + b.shape[1]] += a[i, j] * b
    return out


def _padd(a, b):
    m = max(a.shape[0], b.shape[0])
    n = max(a.shape[1], b.shape[1])
    out = np.zeros((m, n), dtype=complex)
    out[: a.shape[0], : a.shape[1]] += a
    out[: b.shape[0], : b.shape[1]] += b
    return out


def _pd(p, axis):
    if p.shape[axis] == 1:
        return np.zeros((1, 1), dtype=complex)
    if axis == 0:
        return np.arange(1, p.shape[0])[:, None] * p[1:, :]
    return np.arange(1, p.shape[1])[None, :] * p[:, 1:]


def _peval(p, w1, w2):
    out = np.zeros(np.broadcast(w1, w2).shape, dtype=complex)
    for m in range(p.shape[0]):
        for n in range(p.shape[1]):
            if p[m, n] != 0.0:
                out = out + p[m, n] * w1**m * w2**n
    return out


def _apply_generator(p, a, bv, s):
    """One application of D = (1/2) d^T S d to P e^Q, with e^Q factored out:

        D(P e^Q) = e^Q [ (1/2) d^T S d P + (grad P)^T S (A w + b)
                         + (P/2) ((A w + b)^T S (A w + b) + tr(S A)) ].
    """
    lin = []
    for i in range(2):
        li = np.zeros((2, 2), dtype=complex)
        li[0, 0] = bv[i]
        li[1, 0] = a[i, 0]
        li[0, 1] = a[i, 1]
        lin.append(li)
    out = np.zeros((1, 1), dtype=complex)
    for i in range(2):
        for j in range(2):
            if s[i, j] == 0.0:
                continue
            out = _padd(out, 0.5 * s[i, j] * _pd(_pd(p, i), j))
            out = _padd(out, s[i, j] * _pmul(_pd(p, i), lin[j]))
            out = _padd(out, 0.5 * s[i, j] * _pmul(p, _pmul(lin[i], lin[j])))
    return _padd(out, 0.5 * np.trace(s @ a) * p)


# ---------------------------------------------------------------------------
# T1: heat_step against an independent tau-series of the generator
# ---------------------------------------------------------------------------

def test_heat_step_matches_tau_series():
    """sum_k tau^k/k! D^k (P e^Q), with D and all polynomial arithmetic built
    from scratch above, must reproduce heat_step values to 1e-9 relative at
    random points, for both S = diag(1,0) and S = offdiag."""
    rng = np.random.default_rng(7)
    p = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
    for m in range(4):
        for n in range(4):
            if m + n > 3:
                p[m, n] = 0.0
    a0 = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    a0 = (a0 + a0.T) / 2.0
    a = 0.4 * a0 / np.linalg.norm(a0, 2)
    bv = 0.7 * (rng.normal(size=2) + 1j * rng.normal(size=2))
    st = pq_state(p, a, bv)
    w1 = 0.8 * (rng.normal(size=8) + 1j * rng.normal(size=8))
    w2 = 0.8 * (rng.normal(size=8) + 1j * rng.normal(size=8))
    tau = 0.15
    q = (
        0.5 * (st.A[0, 0] * w1**2 + st.A[1, 1] * w2**2)
        + st.A[0, 1] * w1 * w2
        + st.b[0] * w1
        + st.b[1] * w2
    )
    for s in (
        np.diag([1.0, 0.0]).astype(complex),
        np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex),
    ):
        got = stellar_callable(heat_step(st, s, tau))(w1, w2)
        term = st.P
        total = np.zeros(8, dtype=complex)
        for k in range(31):
            if k > 0:
                term = _apply_generator(term, st.A, st.b, s) / k
            total = total + tau**k * _peval(term, w1, w2)
        want = total * np.exp(q)
        assert np.max(np.abs(got - want)) <= 1e-9 * np.max(np.abs(want))


# ---------------------------------------------------------------------------
# T2: squeeze2 on |1,1> exact anchor
# ---------------------------------------------------------------------------

def test_squeeze2_on_11_exact_polynomial():
    """S2(r)|1,1> must carry P' proportional to w1 w2 - sinh(r) cosh(r) and
    exponent tanh(r) w1 w2: the exact constant is what moves the zero curve
    off w1 w2 = 0 and drives the census threshold test below."""
    for lam in (0.3, 0.5):
        r = math.atanh(lam)
        out = squeeze2(_state_11(), r)
        assert out.P.shape == (2, 2)
        assert abs(out.P[0, 1]) < 1e-12 and abs(out.P[1, 0]) < 1e-12
        ratio = out.P[0, 0] / out.P[1, 1]
        assert abs(ratio + math.sinh(r) * math.cosh(r)) < 1e-12
        expect_a = math.tanh(r) * np.array([[0.0, 1.0], [1.0, 0.0]])
        assert np.max(np.abs(out.A - expect_a)) < 1e-12
        assert np.max(np.abs(out.b)) < 1e-12


# ---------------------------------------------------------------------------
# T3: truncated-Fock brute force, factor by factor
# ---------------------------------------------------------------------------

N_BRUTE = 42


def test_input_states_are_the_claimed_fock_vectors():
    """The monomial-basis inputs are exactly |1,1> and 0.8|2,0> + 0.6|0,3>."""
    c = fock_coeffs(_state_11(), 5)
    expect = np.zeros((5, 5), dtype=complex)
    expect[1, 1] = 1.0
    assert np.max(np.abs(c - expect)) < 1e-12
    c = fock_coeffs(_state_trefoil(), 6)
    expect = np.zeros((6, 6), dtype=complex)
    expect[2, 0] = 0.8
    expect[0, 3] = 0.6
    assert np.max(np.abs(c - expect)) < 1e-12


def _brute_apply(x, vecs):
    """exp(x) @ vecs for anti-Hermitian x, via eigh of the Hermitian i x
    (symmetrized to kill truncation asymmetry); never forms the expm matrix."""
    h = 1j * x
    h = (h + h.conj().T) / 2.0
    w, v = np.linalg.eigh(h)
    return v @ (np.exp(-1j * w)[:, None] * (v.conj().T @ vecs))


def test_bruteforce_fock_validation_of_factors():
    """Each non-passive factor, exponentiated brute-force in the 42^2 Fock
    truncation, must agree with the closed-form action on the m, n <= 8
    coefficient block to 1e-6 relative (truncation error at these moderate
    parameters is far below that)."""
    am = np.diag(np.sqrt(np.arange(1.0, N_BRUTE)), 1)  # a|n> = sqrt(n)|n-1>
    ad = am.T
    eye = np.eye(N_BRUTE)
    z1 = 0.4 * np.exp(0.7j)
    z12 = 0.35 * np.exp(-0.4j)
    al = np.array([0.6 * np.exp(0.3j), -0.35 + 0.2j])
    sq = 0.5 * (z1 * ad @ ad - np.conj(z1) * am @ am)
    d0 = al[0] * ad - np.conj(al[0]) * am
    d1 = al[1] * ad - np.conj(al[1]) * am
    # mode 1 is the first kron factor: index layout m*N + n matches reshape
    factors = [
        (np.kron(sq, eye), lambda s: squeeze1(s, 0, z1)),
        (np.kron(eye, sq), lambda s: squeeze1(s, 1, z1)),
        (
            z12 * np.kron(ad, ad) - np.conj(z12) * np.kron(am, am),
            lambda s: squeeze2(s, z12),
        ),
        (np.kron(d0, eye) + np.kron(eye, d1), lambda s: displace(s, al)),
    ]
    states = [_state_11(), _state_trefoil()]
    vecs = np.stack([fock_coeffs(s, N_BRUTE).reshape(-1) for s in states], axis=1)
    for x, act in factors:
        out = _brute_apply(x, vecs)
        for col, s in enumerate(states):
            got = out[:, col].reshape(N_BRUTE, N_BRUTE)[:9, :9]
            want = fock_coeffs(act(s), 9)
            assert np.max(np.abs(got - want)) <= 1e-6 * np.max(np.abs(want))


def test_passive_matches_rotated_stellar_values():
    """passive() must agree with stellar2.rotated pointwise (same g = f(U w)
    convention), so no expm is needed for the passive factor."""
    u = random_u2(3)
    rng = np.random.default_rng(11)
    w1 = 0.9 * (rng.normal(size=6) + 1j * rng.normal(size=6))
    w2 = 0.9 * (rng.normal(size=6) + 1j * rng.normal(size=6))
    for st in (_state_11(), _state_trefoil()):
        got = stellar_callable(passive(st, u))(w1, w2)
        want = rotated(stellar_callable(st), u)(w1, w2)
        assert np.max(np.abs(got - want)) <= 1e-12 * np.max(np.abs(want))
    with pytest.raises(GaussActError):
        passive(_state_11(), 1.1 * u)


# ---------------------------------------------------------------------------
# T4: unitarity
# ---------------------------------------------------------------------------

def test_random_gauss_unitaries_preserve_norm():
    """Composed random Gaussians must keep ||psi|| = 1 exactly (up to Fock
    truncation, whose last-shell mass is checked to be negligible)."""
    st = _state_11()
    for seed in (5, 6, 8):
        out = gauss_unitary(st, random_gauss_params(seed))
        val, tail = norm(out, cutoff=48)
        assert tail < 1e-10
        assert abs(val - 1.0) < 1e-8


# ---------------------------------------------------------------------------
# T5: fock_coeffs consistency with stellar values
# ---------------------------------------------------------------------------

def test_fock_coeffs_reproduce_stellar_values():
    """fock_stellar(fock_coeffs(state)) is an independent evaluation path
    (Taylor recursion + Fock sum) and must match P e^Q pointwise."""
    st = gauss_unitary(_state_11(), random_gauss_params(2))
    rng = np.random.default_rng(4)
    pts = rng.normal(size=(6, 4))
    pts *= 1.2 * rng.uniform(size=(6, 1)) / np.linalg.norm(pts, axis=1, keepdims=True)
    w1 = pts[:, 0] + 1j * pts[:, 1]
    w2 = pts[:, 2] + 1j * pts[:, 3]
    want = stellar_callable(st)(w1, w2)
    got = fock_stellar(fock_coeffs(st, 24))(w1, w2)
    assert np.max(np.abs(got - want)) <= 1e-8 * np.max(np.abs(want))


# ---------------------------------------------------------------------------
# T6: top-form root partition is a Gaussian invariant
# ---------------------------------------------------------------------------

def test_top_partition_invariant_under_gauss_unitaries():
    """The multiplicity partition of the top form's roots on CP^1 must
    survive any Gaussian unitary (the top form only ever transforms by an
    invertible linear substitution, a Moebius map on the roots). Transformed
    states use tol=1e-3: np.roots scatters an exact triple root by
    ~eps^(1/3) ~ 5e-6, which the default 1e-6 threshold cannot absorb."""
    cases = [
        (_state_11(), (1, 1)),
        (_state_20(), (2,)),
        (_state_trefoil(), (3,)),
    ]
    for st, expect in cases:
        part, gap = top_partition(st)
        assert part == expect
        if expect == (1, 1):
            assert gap > 1e-2
        else:
            assert gap == np.inf  # single cluster: no intercluster distance
        for seed in (31, 32, 33, 34):
            img = gauss_unitary(st, random_gauss_params(seed))
            part, gap = top_partition(img, tol=1e-3)
            assert part == expect
            if expect == (1, 1):
                assert gap > 1e-2
            else:
                assert gap == np.inf


# ---------------------------------------------------------------------------
# T7: census integration and the fixed-radius threshold lam* = sqrt(2) - 1
# ---------------------------------------------------------------------------

def test_census_of_squeezed_11_pins_radius_threshold():
    """S2(r)|1,1> has zeros on w1 w2 = sinh(r) cosh(r) = lam/(1-lam^2), which
    meet S3_radius iff lam/(1-lam^2) <= radius^2/2. At radius 1 the Hopf pair
    survives lam = 0.3 but not lam = 0.5 (lam* = sqrt(2) - 1 sits between);
    enlarging the radius to 1.35 brings it back -- fixed-radius censuses are
    not Gaussian invariants, the threshold is pinned from both sides."""
    f_03 = stellar_callable(squeeze2(_state_11(), math.atanh(0.3)))
    res = census(f_03, radius=1.0, n_eta=60, n_xi=64)
    assert len(res["components"]) == 2
    assert res["linking_matrix"][0][1] == 1

    f_05 = stellar_callable(squeeze2(_state_11(), math.atanh(0.5)))
    res = census(f_05, radius=1.0, n_eta=60, n_xi=64)
    assert len(res["components"]) == 0

    # finer grid here: at radius 1.35 the 60x64 polylines are too coarse for
    # a clean crossing count (they report lk 2; 90x96 and a radius-1.5
    # control both give the topologically required 1)
    res = census(f_05, radius=1.35, n_eta=90, n_xi=96)
    assert len(res["components"]) == 2
    assert res["linking_matrix"][0][1] == 1
