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
from wigner_splat.fit3f import fit3f, fit3f_psd, loss3f
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
