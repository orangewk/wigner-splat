"""Fit-free checks for issue #28: out-of-family targets + rank-R BB-dagger.

Pins (a) the lossy-cat closed form (loss-channel algebra), (b) the squeezed-cat
pdf, (c) the rank-R mixed NLL/gradient machinery, and (d) the exact Uhlmann
fidelity on coherent-product spans -- everything exp10 relies on.
"""
import numpy as np
import pytest

from wigner_splat.bbdagM import (
    CoherentKetState, MixedCoherentKetState, _pack_mixed, _unpack_mixed,
    nll, nll_and_grad_mixed, nll_mixed,
)
from wigner_splat.states3 import ThreeModeCat
from wigner_splat.states3x import (
    LossyThreeModeCat, SqueezedThreeModeCat, fidelity_vs_squeezed_cat3,
    uhlmann_fidelity_vs_lossy_cat3,
)


def _grid3(x_max=6.0, n=81):
    xs = np.linspace(-x_max, x_max, n)
    return xs, (xs[:, None, None], xs[None, :, None], xs[None, None, :])


# ---------------------------------------------------------------- lossy cat

def test_lossy_cat_reduces_to_pure_cat_at_full_transmission():
    cat = ThreeModeCat(1.5, +1)
    lossy = LossyThreeModeCat(1.5, +1, eta=1.0)
    xs, (X1, X2, X3) = _grid3(n=41)
    th = (0.4, 1.3, 2.6)
    assert np.allclose(
        lossy.homodyne_pdf(X1, X2, X3, *th),
        cat.homodyne_pdf(X1, X2, X3, *th),
        rtol=1e-12, atol=1e-15,
    )


@pytest.mark.parametrize("eta", [0.6, 0.8])
def test_lossy_cat_pdf_is_normalized_and_nonnegative(eta):
    lossy = LossyThreeModeCat(1.5, +1, eta=eta)
    xs, (X1, X2, X3) = _grid3(x_max=7.0, n=101)
    dx = xs[1] - xs[0]
    P = lossy.homodyne_pdf(X1, X2, X3, 0.7, 1.9, 0.1)
    assert P.min() >= -1e-15                    # physical rho => nonnegative
    assert np.sum(P) * dx ** 3 == pytest.approx(1.0, abs=1e-6)


def test_lossy_cat_is_exactly_rank2_bbdag():
    """rho = B B^dagger with 2 columns built from its own coherent span."""
    target = LossyThreeModeCat(1.5, +1, eta=0.8)
    kets, M = target.coherent_span()
    # factor M = C C^dagger (Hermitian PSD, 2x2)
    w, U = np.linalg.eigh(M)
    C = U * np.sqrt(np.maximum(w, 0.0))        # columns c_r
    state = MixedCoherentKetState(z=C.T, alpha=np.array([kets, kets]))
    assert state.norm_sq() == pytest.approx(1.0, abs=1e-12)  # tr rho = 1
    assert uhlmann_fidelity_vs_lossy_cat3(state, target) == pytest.approx(
        1.0, abs=1e-6
    )
    # model pdf equals the closed-form target pdf
    rng = np.random.default_rng(5)
    X = rng.normal(scale=1.3, size=(48, 3))
    theta = np.array([0.2, 1.0, 2.4])
    dens = np.zeros(len(X))
    for col in state.columns():
        dens += np.abs(col.psi_at(X, theta)) ** 2
    p_model = dens / state.norm_sq()
    p_ref = target.homodyne_pdf(X[:, 0], X[:, 1], X[:, 2], *theta)
    assert np.allclose(p_model, p_ref, rtol=1e-10, atol=1e-13)


def test_rank1_cannot_reach_unit_uhlmann_on_lossy_cat():
    """The best in-span rank-1 ket stays strictly below F = 1 (mixed target)."""
    target = LossyThreeModeCat(1.5, +1, eta=0.8)
    kets, M = target.coherent_span()
    # dominant eigenvector of the span matrix = best rank-1 candidate in span
    w, U = np.linalg.eigh(M)
    best = CoherentKetState(z=U[:, -1] * np.sqrt(w[-1]), alpha=kets)
    z_norm = best.norm_sq()
    best = CoherentKetState(z=best.z / np.sqrt(z_norm), alpha=kets)
    F = uhlmann_fidelity_vs_lossy_cat3(best, target)
    assert F < 0.999                            # genuinely mixed target
    assert F > 0.5


# ------------------------------------------------------------- squeezed cat

def test_squeezed_cat_reduces_to_cat_at_zero_squeeze():
    cat = ThreeModeCat(1.2, -1)
    sq = SqueezedThreeModeCat(1.2, -1, r=0.0)
    xs, (X1, X2, X3) = _grid3(n=41)
    th = (0.9, 0.0, 1.7)
    assert np.allclose(
        sq.homodyne_pdf(X1, X2, X3, *th),
        cat.homodyne_pdf(X1, X2, X3, *th),
        rtol=1e-10, atol=1e-13,
    )


def test_squeezed_cat_pdf_is_normalized():
    sq = SqueezedThreeModeCat(1.5, +1, r=0.4)
    xs, (X1, X2, X3) = _grid3(x_max=7.5, n=101)
    dx = xs[1] - xs[0]
    P = sq.homodyne_pdf(X1, X2, X3, 0.5, 1.2, 2.8)
    assert P.min() >= -1e-15
    assert np.sum(P) * dx ** 3 == pytest.approx(1.0, abs=1e-6)


def test_squeezed_fidelity_helper_recovers_exact_cat_at_zero_squeeze():
    a = 1.5
    target = SqueezedThreeModeCat(a, +1, r=0.0)
    exact = CoherentKetState(
        z=np.array([1.0, 1.0], complex),
        alpha=np.array([[a, a, a], [-a, -a, -a]], complex),
    )
    assert fidelity_vs_squeezed_cat3(exact, target) == pytest.approx(
        1.0, abs=1e-8
    )


# --------------------------------------------- splat-side closed-form scoring

def test_lossy_overlap_reduces_to_pure_cat_overlap_at_eta_one():
    from wigner_splat.fit3f import fit3f
    from wigner_splat.forward3f import (
        fidelity_vs_cat3, overlap_vs_lossy_cat3,
    )
    from wigner_splat.states3 import ThreeModeCat

    grid = [(0.0, 0.5, 1.0), (1.2, 2.1, 0.3)]
    data = ThreeModeCat(1.2, +1).sample_homodyne(grid, 400, rng=7)
    mix = fit3f(data, bins=16)
    a = fidelity_vs_cat3(mix, 1.2, +1)
    b = overlap_vs_lossy_cat3(mix, 1.2, +1, eta=1.0)
    assert b == pytest.approx(a, rel=1e-12)


def test_squeezed_overlap_reduces_to_pure_cat_overlap_at_zero_squeeze():
    from wigner_splat.fit3f import fit3f
    from wigner_splat.forward3f import (
        fidelity_vs_cat3, overlap_vs_squeezed_cat3,
    )
    from wigner_splat.states3 import ThreeModeCat

    grid = [(0.0, 0.5, 1.0), (1.2, 2.1, 0.3)]
    data = ThreeModeCat(1.2, +1).sample_homodyne(grid, 400, rng=7)
    mix = fit3f(data, bins=16)
    a = fidelity_vs_cat3(mix, 1.2, +1)
    b = overlap_vs_squeezed_cat3(mix, 1.2, +1, r=0.0)
    assert b == pytest.approx(a, rel=1e-12)


def test_lossy_purity_limits():
    from wigner_splat.forward3f import lossy_cat3_purity
    # eta = 1: pure state, purity 1
    assert lossy_cat3_purity(1.5, +1, eta=1.0) == pytest.approx(1.0, abs=1e-12)
    # strong loss on a big cat: approaches an equal mixture of two coherent
    # states, purity -> 1/2
    assert lossy_cat3_purity(2.5, +1, eta=0.5) == pytest.approx(0.5, abs=1e-3)


def test_lossy_cat3_fock_matches_span_quantities():
    from wigner_splat.fock import cat3_fock, lossy_cat3_fock
    from wigner_splat.forward3f import lossy_cat3_purity

    # eta = 1 reduces to the pure-cat projector
    rho1 = lossy_cat3_fock(1.2, +1, eta=1.0, n_max=10)
    c = cat3_fock(1.2, +1, n_max=10)
    # cat3_fock is normalized on the truncated space; rho1's trace is the
    # truncation retention t, and rho1/t should equal the projector
    t = np.real(np.trace(rho1))
    assert np.allclose(rho1 / t, np.outer(c, c), atol=1e-10)

    # eta < 1: trace ~= 1 (truncation deficit only) and purity matches the
    # exact span value
    rho = lossy_cat3_fock(1.5, +1, eta=0.8, n_max=12)
    assert np.real(np.trace(rho)) == pytest.approx(1.0, abs=2e-3)
    purity = np.real(np.trace(rho @ rho))
    assert purity == pytest.approx(lossy_cat3_purity(1.5, +1, 0.8), abs=5e-3)


# ------------------------------------------------------ rank-R NLL machinery

def test_rank1_mixed_nll_equals_pure_nll():
    rng = np.random.default_rng(9)
    K, M = 3, 2
    z = rng.normal(size=K) + 1j * rng.normal(size=K)
    alpha = rng.normal(size=(K, M)) + 1j * rng.normal(size=(K, M))
    data = [
        (rng.uniform(0, np.pi, M), rng.normal(scale=1.4, size=(30, M)))
        for _ in range(2)
    ]
    pure = CoherentKetState(z, alpha)
    mixed = MixedCoherentKetState(z[None, :], alpha[None, :, :])
    assert nll_mixed(mixed, data) == pytest.approx(nll(pure, data), rel=1e-12)


@pytest.mark.parametrize("R,K,M", [(1, 2, 2), (2, 2, 3)])
def test_mixed_analytic_grad_matches_central_difference(R, K, M):
    rng = np.random.default_rng(20260714)
    state = MixedCoherentKetState(
        z=rng.normal(size=(R, K)) + 1j * rng.normal(size=(R, K)),
        alpha=rng.normal(size=(R, K, M)) + 1j * rng.normal(size=(R, K, M)),
    )
    data = [
        (rng.uniform(0, np.pi, M), rng.normal(scale=1.5, size=(30, M)))
        for _ in range(2)
    ]
    value, g = nll_and_grad_mixed(state, data)
    assert value == pytest.approx(nll_mixed(state, data), rel=1e-12)

    v = _pack_mixed(state)
    eps = 1e-6
    g_fd = np.zeros_like(v)
    for i in range(len(v)):
        vp = v.copy(); vp[i] += eps
        vm = v.copy(); vm[i] -= eps
        g_fd[i] = (
            nll_mixed(_unpack_mixed(vp, R, K, M), data)
            - nll_mixed(_unpack_mixed(vm, R, K, M), data)
        ) / (2 * eps)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g - g_fd) / scale) < 1e-7
