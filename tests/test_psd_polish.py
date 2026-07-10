"""Tests for the issue #8 PSD-polish stage: fit.fit_psd (1-mode, full-param
finite-difference) and fit3f.fit3f_psd (3-mode, weight-only), plus the
finite-difference gradient helper both build on.

See experiments/08_positivity/penalty_sweep_1mode.py for the actual
falsification-condition verdict; these tests pin fit_psd/fit3f_psd's
mechanics (no-op at lambda_psd=0, finite-difference gradient correctness,
"the polish stage measurably reduces min_eig") and guard fit()/fit3f()
against regression (fit_psd/fit3f_psd call them UNMODIFIED).
"""

import numpy as np
import pytest

from wigner_splat.data3 import histogram_targets3
from wigner_splat.fit import (
    _pack,
    _pack_splat_index,
    _psd_penalty_grad_fd,
    _unpack,
    fit,
    fit_psd,
)
from wigner_splat.fit3f import (
    apply_shape_knobs,
    fit3f,
    fit3f_psd,
    fit3f_shape_psd,
    identify_stripes,
    loss3f,
    _cov_to_chol,
    _probe_cov,
)
from wigner_splat.fock_project import psd_penalty, psd_report, rho_from_splat
from wigner_splat.forward import SplatMixture
from wigner_splat.states import CatState
from wigner_splat.states3 import ThreeModeCat

ALPHA = 1.5
PARITY = +1
FIT_KWARGS = dict(K=4, iters=800, seed=0, densify_every=100, K_max=12)


def _cat1_data():
    cat = CatState(ALPHA, parity=PARITY)
    angles = np.linspace(0, np.pi, 12, endpoint=False)
    return cat.sample_homodyne(angles, 4000, rng=42)


# ---------------------------------------------------------------------------
# fit() regression pin (fit_psd must not have altered fit()'s own behavior).

def test_fit_baseline_is_unchanged():
    """Pins fit()'s output on the issue brief's exact config (same as
    diagnose_1mode.py part B / test_fock_project's fitted-splat tests) --
    guards against fit_psd's addition silently perturbing fit() itself."""
    mix = fit(_cat1_data(), **FIT_KWARGS)
    assert len(mix.w) == 9
    assert mix.w.sum() == pytest.approx(1.0, abs=1e-3)

    rho = rho_from_splat(mix, n_max=28)
    report = psd_report(rho)
    # Values measured directly from fit() before fit_psd existed (see the
    # issue brief's "n_max>=28" baseline: F~0.991, min_eig~-0.034).
    assert report["min_eig"] == pytest.approx(-0.03403, abs=2e-4)
    assert report["trace"] == pytest.approx(1.0, abs=1e-3)


# ---------------------------------------------------------------------------
# fit_psd no-op cases (purely additive: never re-runs or re-weights fit()).

def test_fit_psd_lambda_zero_matches_fit_exactly():
    data = _cat1_data()
    mix_fit = fit(data, **FIT_KWARGS)
    mix_psd = fit_psd(data, lambda_psd=0.0, **FIT_KWARGS)
    np.testing.assert_array_equal(mix_fit.w, mix_psd.w)
    np.testing.assert_array_equal(mix_fit.mu, mix_psd.mu)
    np.testing.assert_array_equal(mix_fit.s, mix_psd.s)
    np.testing.assert_array_equal(mix_fit.phi, mix_psd.phi)


def test_fit_psd_zero_iters_matches_fit_exactly():
    data = _cat1_data()
    mix_fit = fit(data, **FIT_KWARGS)
    mix_psd = fit_psd(data, lambda_psd=5.0, psd_polish_iters=0, **FIT_KWARGS)
    np.testing.assert_array_equal(mix_fit.w, mix_psd.w)


# ---------------------------------------------------------------------------
# _psd_penalty_grad_fd: the per-component-cached finite-difference gradient
# must match a brute-force (full O(K) rebuild per index) central difference.

def _brute_force_psd_grad(v, K, n_max, eps):
    g = np.zeros_like(v)
    for i in range(len(v)):
        vp, vm = v.copy(), v.copy()
        vp[i] += eps
        vm[i] -= eps
        pen_p = psd_penalty(rho_from_splat(_unpack(vp, K), n_max))
        pen_m = psd_penalty(rho_from_splat(_unpack(vm, K), n_max))
        g[i] = (pen_p - pen_m) / (2 * eps)
    return g


def test_psd_penalty_grad_fd_matches_brute_force():
    rng = np.random.default_rng(0)
    K = 3
    mix = SplatMixture(
        w=rng.uniform(-0.5, 0.8, K),
        mu=rng.uniform(-1.5, 1.5, (K, 2)),
        s=np.log(rng.uniform(0.4, 1.2, (K, 2))),
        phi=rng.uniform(0, np.pi, K),
    )
    v = _pack(mix)
    n_max = 8
    eps = 1e-4

    g_cached = _psd_penalty_grad_fd(v, K, n_max, eps)
    g_brute = _brute_force_psd_grad(v, K, n_max, eps)
    np.testing.assert_allclose(g_cached, g_brute, atol=1e-10)


def test_pack_splat_index_covers_every_packed_entry():
    """Every packed index must resolve to a valid splat in [0, K) -- the
    identity _psd_penalty_grad_fd's caching depends on."""
    K = 5
    n_params = 6 * K  # w(K) + mu(2K) + s(2K) + phi(K)
    for i in range(n_params):
        k = _pack_splat_index(i, K)
        assert 0 <= k < K


# ---------------------------------------------------------------------------
# fit_psd must measurably move rho toward PSD (the whole point of #8).

def test_fit_psd_reduces_min_eig():
    data = _cat1_data()
    mix0 = fit(data, **FIT_KWARGS)
    min_eig0 = psd_report(rho_from_splat(mix0, n_max=28))["min_eig"]

    mix1 = fit_psd(data, lambda_psd=20.0, n_max_psd=28,
                    psd_polish_iters=60, psd_polish_lr=0.01, **FIT_KWARGS)
    min_eig1 = psd_report(rho_from_splat(mix1, n_max=28))["min_eig"]

    # min_eig is negative; "reduced violation" means LARGER (closer to 0).
    assert min_eig1 > min_eig0 + 0.01


# ---------------------------------------------------------------------------
# fit3f_psd (3-mode, weight-only polish) -- expensive (fit3f + n_max=8 rho
# materialization), so kept small and marked slow.

@pytest.mark.slow
def test_fit3f_psd_lambda_zero_matches_fit3f_exactly():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    import itertools
    angles = [t for t in itertools.product(
        np.linspace(0, np.pi, 3, endpoint=False), repeat=3)]
    data = cat.sample_homodyne(angles, 2000, rng=42)

    mix_fit = fit3f(data)
    mix_psd = fit3f_psd(data, lambda_psd=0.0)
    np.testing.assert_array_equal(mix_fit.w, mix_psd.w)
    np.testing.assert_array_equal(mix_fit.mu, mix_psd.mu)


@pytest.mark.slow
def test_fit3f_psd_reduces_min_eig():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    import itertools
    angles = [t for t in itertools.product(
        np.linspace(0, np.pi, 3, endpoint=False), repeat=3)]
    data = cat.sample_homodyne(angles, 2000, rng=42)

    mix0 = fit3f(data)
    min_eig0 = psd_report(rho_from_splat(mix0, n_max=8))["min_eig"]

    mix1 = fit3f_psd(data, lambda_psd=5.0, n_max_psd=8,
                      psd_polish_iters=15, psd_polish_lr=0.02)
    min_eig1 = psd_report(rho_from_splat(mix1, n_max=8))["min_eig"]

    assert min_eig1 > min_eig0 + 0.01


# ---------------------------------------------------------------------------
# fit3f_shape_psd (3-mode, JOINT weight + 3 global fringe-shape knobs polish,
# issue #8 follow-up to the weight-only polish above -- see its docstring).
# A small, cheap 3-triple/300-shot dataset (not exp06's official 27x2000
# condition) keeps identify_stripes/apply_shape_knobs mechanics tests fast;
# the actual falsification-condition numbers live in
# experiments/08_positivity/shape_polish_3mode.py, run separately.

def _small3f_data():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    angles = [(0.0, 0.0, 0.0), (1.0, 0.5, 0.2), (0.3, 1.2, 0.7)]
    return cat.sample_homodyne(angles, 300, rng=1)


def _fit3f_with_direction(data, **kwargs):
    box = {}

    def cb(name, mix, *rest):
        if name == "stripes":
            box["direction"] = rest[-1]

    mix = fit3f(data, callback=cb, **kwargs)
    return mix, box["direction"]


def test_identify_stripes_partitions_all_components():
    data = _small3f_data()
    mix, direction = _fit3f_with_direction(data, bins=12)
    ld0, lo0 = _cov_to_chol(_probe_cov(direction, 0.03))
    is_stripe = identify_stripes(mix, ld0, lo0)

    K = len(mix.w)
    assert is_stripe.shape == (K,)
    # both groups present for this data (a blob envelope AND matched-filter
    # fringe stripes both survive weight_ls pruning at the default threshold)
    assert 0 < is_stripe.sum() < K
    # every stripe row's own (ld, lo) exactly reproduces the shared template
    n_stripe = int(is_stripe.sum())
    np.testing.assert_allclose(mix.ld[is_stripe], np.tile(ld0, (n_stripe, 1)),
                               atol=1e-9)
    np.testing.assert_allclose(mix.lo[is_stripe], np.tile(lo0, (n_stripe, 1)),
                               atol=1e-9)
    # no blob row accidentally matches the stripe template
    assert not np.any(
        np.all(np.isclose(mix.ld[~is_stripe], ld0, atol=1e-9), axis=1)
        & np.all(np.isclose(mix.lo[~is_stripe], lo0, atol=1e-9), axis=1)
    )


def test_apply_shape_knobs_identity_is_noop():
    data = _small3f_data()
    mix, direction = _fit3f_with_direction(data, bins=12)
    ld0, lo0 = _cov_to_chol(_probe_cov(direction, 0.03))
    is_stripe = identify_stripes(mix, ld0, lo0)

    identity = apply_shape_knobs(mix, is_stripe, direction, thin=0.03)
    np.testing.assert_array_equal(identity.mu, mix.mu)
    np.testing.assert_array_equal(identity.ld, mix.ld)
    np.testing.assert_array_equal(identity.lo, mix.lo)
    np.testing.assert_array_equal(identity.w, mix.w)


def test_apply_shape_knobs_touches_only_stripe_rows():
    data = _small3f_data()
    mix, direction = _fit3f_with_direction(data, bins=12)
    ld0, lo0 = _cov_to_chol(_probe_cov(direction, 0.03))
    is_stripe = identify_stripes(mix, ld0, lo0)

    scaled = apply_shape_knobs(mix, is_stripe, direction, thin=0.03,
                               thin_mult=2.0, base_mult=1.5,
                               center_scale=0.7)
    # blob rows (mu, ld, lo) are bit-for-bit unchanged
    np.testing.assert_array_equal(scaled.mu[~is_stripe], mix.mu[~is_stripe])
    np.testing.assert_array_equal(scaled.ld[~is_stripe], mix.ld[~is_stripe])
    np.testing.assert_array_equal(scaled.lo[~is_stripe], mix.lo[~is_stripe])
    # stripe rows moved
    assert not np.allclose(scaled.ld[is_stripe], mix.ld[is_stripe])
    assert not np.allclose(scaled.mu[is_stripe], mix.mu[is_stripe])
    # weights untouched by shape knobs
    np.testing.assert_array_equal(scaled.w, mix.w)


def test_fit3f_shape_psd_lambda_zero_matches_fit3f_exactly():
    data = _small3f_data()
    mix_fit = fit3f(data, bins=12)
    mix_shape = fit3f_shape_psd(data, lambda_psd=0.0, bins=12)
    np.testing.assert_array_equal(mix_fit.w, mix_shape.w)
    np.testing.assert_array_equal(mix_fit.mu, mix_shape.mu)
    np.testing.assert_array_equal(mix_fit.ld, mix_shape.ld)
    np.testing.assert_array_equal(mix_fit.lo, mix_shape.lo)


def test_fit3f_shape_psd_zero_iters_matches_fit3f_exactly():
    data = _small3f_data()
    mix_fit = fit3f(data, bins=12)
    mix_shape = fit3f_shape_psd(data, lambda_psd=5.0, shape_polish_iters=0,
                                bins=12)
    np.testing.assert_array_equal(mix_fit.w, mix_shape.w)


def test_apply_shape_knobs_rejects_nonpositive_scales():
    data = _small3f_data()
    mix, direction = _fit3f_with_direction(data, bins=12)
    ld0, lo0 = _cov_to_chol(_probe_cov(direction, 0.03))
    is_stripe = identify_stripes(mix, ld0, lo0)

    with pytest.raises(ValueError, match="positive"):
        apply_shape_knobs(mix, is_stripe, direction, thin_mult=0.0)


def test_fit3f_shape_psd_rejects_nonlinear_polish():
    with pytest.raises(ValueError, match="polish_iters=0"):
        fit3f_shape_psd(
            _small3f_data(), bins=12, polish_iters=1, shape_polish_iters=1
        )


@pytest.mark.slow
def test_fit3f_shape_psd_reduces_min_eig():
    # n_max_psd=4 (not the official 8) keeps this mechanics test's rho
    # rebuilds (dominant cost, ~(1+2*3)*S per iteration -- see
    # fit3f_shape_psd's docstring) fast; the official n_max_psd=8 numbers are
    # measured separately in experiments/08_positivity/shape_polish_3mode.py.
    data = _small3f_data()
    mix0 = fit3f(data, bins=12)
    min_eig0 = psd_report(rho_from_splat(mix0, n_max=4))["min_eig"]

    mix1 = fit3f_shape_psd(data, lambda_psd=5.0, n_max_psd=4,
                           shape_polish_iters=4, bins=12)
    min_eig1 = psd_report(rho_from_splat(mix1, n_max=4))["min_eig"]

    assert min_eig1 > min_eig0 + 0.01
