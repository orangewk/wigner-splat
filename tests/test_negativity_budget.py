"""Packet-1 gates for experiment 33's fixed-beta difference model."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

from wigner_splat.bbdagS import (
    MixedSqueezedKetState,
    lossy_pdf_mixed,
    nll_lossy_mixed,
)


ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "33_negativity_budget"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "negativity_budget_fixed_beta", EXP / "fixed_beta.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


fixed = _load_module()


def _component(alpha=0.0, *, modes=1):
    return MixedSqueezedKetState(
        z=np.ones((1, 1), complex),
        alpha=np.full((1, 1, modes), complex(alpha)),
        xi=np.zeros((1, 1, modes), complex),
    )


def _group(xs, theta=0.0):
    return [(np.array([theta]), np.asarray(xs, float)[:, None])]


@pytest.mark.parametrize("beta", [-0.1, 0.5, 0.7, np.nan, np.inf])
def test_beta_domain_is_fail_closed(beta):
    with pytest.raises(ValueError):
        fixed.FixedBetaDifferenceModel(_component(), _component(), beta)


def test_beta_rejects_bool_and_requires_negative_component():
    with pytest.raises(TypeError):
        fixed.FixedBetaDifferenceModel(_component(), None, True)
    with pytest.raises(ValueError):
        fixed.FixedBetaDifferenceModel(_component(), _component(), 0.0)
    with pytest.raises(ValueError):
        fixed.FixedBetaDifferenceModel(_component(), None, 0.1)


def test_component_shape_mode_and_norm_validation():
    malformed = _component()
    malformed.alpha = np.zeros((1, 2, 1), complex)
    with pytest.raises(ValueError):
        fixed.FixedBetaDifferenceModel(malformed, None, 0.0)

    zero = _component()
    zero.z[:] = 0.0
    with pytest.raises(ValueError):
        fixed.FixedBetaDifferenceModel(zero, None, 0.0)

    with pytest.raises(ValueError):
        fixed.FixedBetaDifferenceModel(_component(), _component(modes=2), 0.1)


def test_beta_zero_is_exact_existing_positive_model():
    positive = _component(alpha=0.4 + 0.2j)
    model = fixed.FixedBetaDifferenceModel(positive, None, 0.0)
    xs = np.linspace(-3.0, 3.0, 101)[:, None]
    theta = np.array([0.37])
    expected = lossy_pdf_mixed(positive, xs, theta, eta=0.8)
    np.testing.assert_array_equal(model.pdf(xs, theta, eta=0.8), expected)

    data = [(theta, xs)]
    assert fixed.mean_nll(model, data, eta=0.8) == pytest.approx(
        nll_lossy_mixed(positive, data, eta=0.8), abs=1e-15
    )


def test_fixed_mass_formula_and_density_normalization():
    beta = 0.2
    positive = _component(alpha=-0.8)
    negative = _component(alpha=0.9)
    model = fixed.FixedBetaDifferenceModel(positive, negative, beta)
    assert model.pre_normalization_masses == pytest.approx((0.8, 0.2))
    assert model.density_coefficients == pytest.approx((4.0 / 3.0, -1.0 / 3.0))

    xs = np.linspace(-10.0, 10.0, 20001)
    density = model.pdf(xs[:, None], np.array([0.0]), eta=0.8)
    assert np.trapezoid(density, xs) == pytest.approx(1.0, abs=2e-8)


def test_signed_density_is_not_clipped_and_strict_nll_rejects_it():
    positive = _component(alpha=2.5)
    negative = _component(alpha=0.0)
    model = fixed.FixedBetaDifferenceModel(positive, negative, beta=0.4)
    data = _group([0.0, 0.1, -0.1])
    density = model.pdf(data[0][1], data[0][0], eta=0.8)
    assert np.min(density) < 0.0
    with pytest.raises(fixed.NonPositiveDensityError) as exc:
        fixed.per_sample_nll(model, data, eta=0.8)
    assert exc.value.invalid_count > 0


def test_strict_nll_returns_unfloored_per_sample_values_when_positive():
    positive = _component(alpha=0.0)
    negative = _component(alpha=0.15)
    model = fixed.FixedBetaDifferenceModel(positive, negative, beta=0.01)
    data = _group(np.linspace(-1.0, 1.0, 21))
    density = model.pdf(data[0][1], data[0][0], eta=0.8)
    assert np.all(density > 0.0)
    np.testing.assert_allclose(
        fixed.per_sample_nll(model, data, eta=0.8),
        -np.log(density),
        rtol=0.0,
        atol=0.0,
    )


def test_empty_data_is_rejected():
    model = fixed.FixedBetaDifferenceModel(_component(), None, 0.0)
    with pytest.raises(ValueError):
        fixed.per_sample_nll(model, [], eta=0.8)
    with pytest.raises(ValueError):
        fixed.per_sample_nll(model, _group([]), eta=0.8)


def test_nonfinite_density_is_rejected():
    model = fixed.FixedBetaDifferenceModel(_component(), None, 0.0)
    with pytest.raises(fixed.NonPositiveDensityError):
        fixed.per_sample_nll(model, _group([np.nan]), eta=0.8)
