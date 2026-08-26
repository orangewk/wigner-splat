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


def _convex_mixture(states, weights):
    weights = np.asarray(weights, float)
    assert np.all(weights >= 0.0)
    assert np.sum(weights) == pytest.approx(1.0)
    return MixedSqueezedKetState(
        z=np.concatenate(
            [
                np.sqrt(weight / state.norm_sq()) * state.z
                for state, weight in zip(states, weights, strict=True)
            ],
            axis=0,
        ),
        alpha=np.concatenate([state.alpha for state in states], axis=0),
        xi=np.concatenate([state.xi for state in states], axis=0),
    )


def _group(xs, theta=0.0):
    return [(np.array([theta]), np.asarray(xs, float)[:, None])]


@pytest.mark.parametrize(
    "beta",
    [-0.1, np.nextafter(0.4, np.inf), 0.49, 0.5, 0.7, np.nan, np.inf],
)
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
    assert np.min(expected) > 1e-300
    np.testing.assert_array_equal(model.pdf(xs, theta, eta=0.8), expected)

    data = [(theta, xs)]
    assert fixed.mean_nll(model, data, eta=0.8) == pytest.approx(
        nll_lossy_mixed(positive, data, eta=0.8), abs=1e-15
    )


def test_beta_zero_strict_nll_diverges_when_legacy_floor_binds():
    positive = _component()
    model = fixed.FixedBetaDifferenceModel(positive, None, 0.0)
    theta = np.array([0.0])

    positive_below_floor = [(theta, np.array([[27.0]]))]
    density = model.pdf(positive_below_floor[0][1], theta, eta=0.8)[0]
    assert 0.0 < density < 1e-300
    strict = fixed.mean_nll(model, positive_below_floor, eta=0.8)
    legacy = nll_lossy_mixed(positive, positive_below_floor, eta=0.8)
    assert strict == pytest.approx(-np.log(density))
    assert legacy == pytest.approx(-np.log(1e-300))
    assert strict > legacy

    underflow_to_zero = [(theta, np.array([[28.0]]))]
    assert model.pdf(underflow_to_zero[0][1], theta, eta=0.8)[0] == 0.0
    assert nll_lossy_mixed(
        positive, underflow_to_zero, eta=0.8
    ) == pytest.approx(-np.log(1e-300))
    with pytest.raises(fixed.NonPositiveDensityError):
        fixed.mean_nll(model, underflow_to_zero, eta=0.8)


def test_fixed_mass_formula_and_density_normalization():
    beta = 0.4
    positive = _component(alpha=-0.8)
    negative = _component(alpha=0.9)
    model = fixed.FixedBetaDifferenceModel(positive, negative, beta)
    assert model.pre_normalization_masses == pytest.approx((0.6, 0.4))
    assert model.density_coefficients == pytest.approx((3.0, -2.0))

    xs = np.linspace(-10.0, 10.0, 20001)
    density = model.pdf(xs[:, None], np.array([0.0]), eta=0.8)
    p_positive = lossy_pdf_mixed(
        positive, xs[:, None], np.array([0.0]), eta=0.8
    )
    p_negative = lossy_pdf_mixed(
        negative, xs[:, None], np.array([0.0]), eta=0.8
    )
    np.testing.assert_allclose(
        density,
        3.0 * p_positive - 2.0 * p_negative,
        rtol=5e-14,
        atol=np.finfo(float).eps,
    )
    assert np.trapezoid(density, xs) == pytest.approx(1.0, abs=2e-8)


@pytest.mark.parametrize(
    ("beta_1", "beta_2"), [(0.0, 0.1), (0.1, 0.3), (0.3, 0.4)]
)
def test_larger_beta_class_reproduces_smaller_beta_with_rank_expansion(
    beta_1, beta_2
):
    positive_1 = _component(alpha=-0.6 + 0.2j)
    negative_1 = None if beta_1 == 0.0 else _component(alpha=0.7)
    auxiliary = _component(alpha=1.3 - 0.4j)
    model_1 = fixed.FixedBetaDifferenceModel(
        positive_1, negative_1, beta_1
    )

    c_pos_1 = (1.0 - beta_1) / (1.0 - 2.0 * beta_1)
    c_neg_1 = beta_1 / (1.0 - 2.0 * beta_1)
    c_pos_2 = (1.0 - beta_2) / (1.0 - 2.0 * beta_2)
    c_neg_2 = beta_2 / (1.0 - 2.0 * beta_2)
    added_mass = c_pos_2 - c_pos_1
    assert added_mass == pytest.approx(c_neg_2 - c_neg_1)

    positive_2 = _convex_mixture(
        [positive_1, auxiliary],
        [c_pos_1 / c_pos_2, added_mass / c_pos_2],
    )
    if negative_1 is None:
        negative_2 = auxiliary
    else:
        negative_2 = _convex_mixture(
            [negative_1, auxiliary],
            [c_neg_1 / c_neg_2, added_mass / c_neg_2],
        )
    model_2 = fixed.FixedBetaDifferenceModel(
        positive_2, negative_2, beta_2
    )

    xs = np.linspace(-5.0, 5.0, 4001)[:, None]
    theta = np.array([0.31])
    np.testing.assert_allclose(
        model_2.pdf(xs, theta, eta=0.8),
        model_1.pdf(xs, theta, eta=0.8),
        rtol=2e-13,
        atol=2e-15,
    )
    assert positive_2.R > positive_1.R
    if negative_1 is not None:
        assert negative_2.R > negative_1.R


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
    p_positive = lossy_pdf_mixed(
        positive, data[0][1], data[0][0], eta=0.8
    )
    p_negative = lossy_pdf_mixed(
        negative, data[0][1], data[0][0], eta=0.8
    )
    expected_density = (0.99 * p_positive - 0.01 * p_negative) / 0.98
    assert np.all(expected_density > 0.0)
    np.testing.assert_allclose(
        fixed.per_sample_nll(model, data, eta=0.8),
        -np.log(expected_density),
        rtol=0.0,
        atol=4.0 * np.finfo(float).eps,
    )


@pytest.mark.parametrize(
    ("component", "X", "theta"),
    [
        (_component(), np.zeros((2, 2)), np.zeros(1)),
        (_component(), np.zeros(2), np.zeros(1)),
        (_component(), np.empty((0, 1)), np.zeros(1)),
        (_component(modes=2), np.zeros((2, 2)), np.zeros(1)),
        (_component(), np.zeros((2, 1)), np.array(0.0)),
    ],
)
def test_observation_shapes_are_fail_closed(component, X, theta):
    model = fixed.FixedBetaDifferenceModel(component, None, 0.0)
    with pytest.raises(fixed.ObservationInputError):
        model.pdf(X, theta, eta=0.8)
    with pytest.raises(fixed.ObservationInputError):
        fixed.per_sample_nll(model, [(theta, X)], eta=0.8)


@pytest.mark.parametrize(
    ("X", "theta"),
    [
        (np.array([[0.3 + 7.7j]]), np.array([0.5])),
        (np.array([[0.3]]), np.array([0.5 + 9.9j])),
        (np.array([[np.nan]]), np.array([0.5])),
        (np.array([[0.3]]), np.array([np.inf])),
        (np.array([["0.3"]]), np.array([0.5])),
    ],
)
def test_observation_values_are_real_finite_numeric(X, theta):
    model = fixed.FixedBetaDifferenceModel(_component(), None, 0.0)
    with pytest.raises(fixed.ObservationInputError):
        model.pdf(X, theta, eta=0.8)
    with pytest.raises(fixed.ObservationInputError):
        fixed.per_sample_nll(model, [(theta, X)], eta=0.8)


def test_empty_data_is_rejected():
    model = fixed.FixedBetaDifferenceModel(_component(), None, 0.0)
    with pytest.raises(ValueError):
        fixed.per_sample_nll(model, [], eta=0.8)
    with pytest.raises(ValueError):
        fixed.per_sample_nll(model, _group([]), eta=0.8)


def test_nonfinite_density_after_component_mutation_is_rejected():
    model = fixed.FixedBetaDifferenceModel(_component(), None, 0.0)
    model.positive.z[:] = 0.0
    with np.errstate(divide="ignore", invalid="ignore"):
        with pytest.raises(fixed.NonPositiveDensityError):
            fixed.per_sample_nll(model, _group([0.0]), eta=0.8)
