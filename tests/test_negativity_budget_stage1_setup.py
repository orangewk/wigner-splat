"""Synthetic gates for the train-only Stage 1 candidate setup packet."""

from __future__ import annotations

from importlib import import_module

import numpy as np
import pytest

from wigner_splat.bbdagS import (
    MixedSqueezedKetState,
    _pack_mixed,
    lossy_pdf_mixed,
)


setup = import_module("experiments.33_negativity_budget.stage1_setup")


def _train_groups():
    return [
        (np.array([0.0]), np.array([[-1.0], [-0.4], [0.1], [0.6], [1.2]])),
        (np.array([0.7]), np.array([[-0.8], [-0.2], [0.3], [0.9]])),
    ]


def _normalized(state):
    return MixedSqueezedKetState(
        z=state.z / np.sqrt(state.norm_sq()),
        alpha=state.alpha,
        xi=state.xi,
    )


def _independent_reference(seed):
    core = _normalized(MixedSqueezedKetState.random_init(3, 4, 1, rng=seed))
    negative = _normalized(
        MixedSqueezedKetState.random_init(
            1, 2, 1, rng=seed + setup.NEGATIVE_SEED_OFFSET
        )
    )
    z = np.zeros((4, 4), complex)
    alpha = np.zeros((4, 4, 1), complex)
    xi = np.zeros((4, 4, 1), complex)
    z[:3] = np.sqrt(3.0 / 4.0) * core.z
    alpha[:3] = core.alpha
    xi[:3] = core.xi
    z[3, :2] = 0.5 * negative.z[0]
    alpha[3, :2] = negative.alpha[0]
    xi[3, :2] = negative.xi[0]
    return MixedSqueezedKetState(z=z, alpha=alpha, xi=xi)


def test_default_setup_contract_is_predeclared():
    assert setup.GRID_POINTS == 1025
    assert setup.GRID_SIGMA_EXTENT == 6.0
    assert setup.NEGATIVE_SEED_OFFSET == 1_000_003
    assert setup.POSITIVE_SHAPE == (4, 4, 1)
    assert setup.NEGATIVE_SHAPE == (1, 2, 1)


def test_train_grid_uses_declared_statistics_and_copies_inputs():
    data = _train_groups()
    original_X = data[0][1].copy()
    candidate = setup.prepare_stage1_candidate(data, beta=0.0, seed=0)
    assert len(candidate.grid_groups) == len(candidate.grid_records) == 2
    for (theta, grid), (_, X), record in zip(
        candidate.grid_groups,
        candidate.train_groups,
        candidate.grid_records,
        strict=True,
    ):
        values = X[:, 0]
        expected_lower = min(
            float(np.min(values)),
            float(np.mean(values) - setup.GRID_SIGMA_EXTENT * np.std(values)),
        )
        expected_upper = max(
            float(np.max(values)),
            float(np.mean(values) + setup.GRID_SIGMA_EXTENT * np.std(values)),
        )
        np.testing.assert_array_equal(theta, np.array([record.theta]))
        assert grid.shape == (setup.GRID_POINTS, 1)
        assert grid[0, 0] == pytest.approx(expected_lower)
        assert grid[-1, 0] == pytest.approx(expected_upper)
        assert record.train_sample_count == len(values)

    data[0][0][0] = 99.0
    data[0][1][:] = 99.0
    np.testing.assert_array_equal(candidate.train_groups[0][0], np.array([0.0]))
    np.testing.assert_array_equal(candidate.train_groups[0][1], original_X)


@pytest.mark.parametrize(
    "data",
    [
        [],
        [(np.array(0.0), np.zeros((2, 1)))],
        [(np.array([0.0]), np.zeros((1, 1)))],
        [(np.array([0.0]), np.zeros((2, 2)))],
        [(np.array([0.0]), np.array([[0.0], [np.nan]]))],
        [(np.array([0.0]), np.array([[0.0j], [1.0j]]))],
        [(np.array([0.0]), np.array([[1.0], [1.0]]))],
    ],
)
def test_invalid_train_groups_fail_closed(data):
    with pytest.raises(ValueError):
        setup.prepare_train_groups(data)


def test_duplicate_measurement_angle_is_rejected():
    duplicate = _train_groups() + [_train_groups()[0]]
    with pytest.raises(ValueError, match="unique"):
        setup.prepare_train_groups(duplicate)


def test_float64_overflow_in_train_statistics_fails_closed():
    data = [(np.array([0.0]), np.array([[1.7e308], [-1.7e308]]))]
    with pytest.raises(ValueError, match="statistics must be finite"):
        setup.prepare_stage1_candidate(data, beta=0.0, seed=0)


def test_beta_zero_initial_vector_is_exact_existing_random_init():
    candidate = setup.prepare_stage1_candidate(
        _train_groups(), beta=0.0, seed=7
    )
    expected = MixedSqueezedKetState.random_init(4, 4, 1, rng=7)
    np.testing.assert_array_equal(
        candidate.initial_parameters, _pack_mixed(expected)
    )
    model = candidate.parameterization.unpack(candidate.initial_parameters)
    assert model.beta == 0.0
    assert model.negative is None


@pytest.mark.parametrize("beta", [0.02, 0.1, 0.4, 0.49])
def test_signed_initialization_matches_independent_rank4_physical_reference(beta):
    seed = 11
    candidate = setup.prepare_stage1_candidate(_train_groups(), beta=beta, seed=seed)
    model = candidate.parameterization.unpack(candidate.initial_parameters)
    reference = _independent_reference(seed)
    assert model.positive.norm_sq() == pytest.approx(1.0, abs=3e-14)
    assert model.negative.norm_sq() == pytest.approx(1.0, abs=3e-14)
    assert all(column.norm_sq() > 0.0 for column in model.positive.columns())
    X = np.linspace(-3.0, 3.0, 31)[:, None]
    for theta in (np.array([0.0]), np.array([0.63])):
        np.testing.assert_allclose(
            model.pdf(X, theta, eta=0.8),
            lossy_pdf_mixed(reference, X, theta, eta=0.8),
            rtol=4e-13,
            atol=4e-15,
        )


def test_setup_is_deterministic_for_same_train_beta_and_seed():
    first = setup.prepare_stage1_candidate(_train_groups(), beta=0.2, seed=5)
    second = setup.prepare_stage1_candidate(_train_groups(), beta=0.2, seed=5)
    np.testing.assert_array_equal(first.initial_parameters, second.initial_parameters)
    for first_group, second_group in zip(
        first.grid_groups, second.grid_groups, strict=True
    ):
        np.testing.assert_array_equal(first_group[0], second_group[0])
        np.testing.assert_array_equal(first_group[1], second_group[1])


def test_returned_setup_arrays_are_read_only():
    candidate = setup.prepare_stage1_candidate(_train_groups(), beta=0.2, seed=5)
    arrays = (
        candidate.train_groups[0][0],
        candidate.train_groups[0][1],
        candidate.grid_groups[0][0],
        candidate.grid_groups[0][1],
        candidate.initial_parameters,
    )
    assert all(not array.flags.writeable for array in arrays)
    for array in arrays:
        with pytest.raises(ValueError, match="read-only"):
            array.flat[0] = 0.0


@pytest.mark.parametrize(
    ("beta", "seed"),
    [(-0.1, 0), (0.5, 0), (np.nan, 0), (True, 0), (0.1, -1), (0.1, True)],
)
def test_beta_and_seed_fail_closed(beta, seed):
    with pytest.raises(ValueError):
        setup.prepare_stage1_candidate(_train_groups(), beta=beta, seed=seed)
