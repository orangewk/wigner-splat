"""Packet-2 gates for analytic signed-density and barrier gradients."""

from __future__ import annotations

from importlib import import_module

import numpy as np
import pytest

from wigner_splat.bbdagS import (
    MixedSqueezedKetState,
    lossy_pdf_and_jac_mixed,
)


fixed = import_module("experiments.33_negativity_budget.fixed_beta")
packet2 = import_module("experiments.33_negativity_budget.packet2")


def _component(alpha=0.0, *, kets=1, seed=23):
    if kets == 1:
        return MixedSqueezedKetState(
            z=np.ones((1, 1), complex),
            alpha=np.array([[[complex(alpha)]]]),
            xi=np.zeros((1, 1, 1), complex),
        )
    rng = np.random.default_rng(seed)
    return MixedSqueezedKetState(
        z=rng.normal(size=(1, kets)) + 1j * rng.normal(size=(1, kets)),
        alpha=(
            rng.normal(size=(1, kets, 1))
            + 1j * rng.normal(size=(1, kets, 1))
        ),
        xi=0.15 * (
            rng.normal(size=(1, kets, 1))
            + 1j * rng.normal(size=(1, kets, 1))
        ),
    )


def test_parameterization_unpacks_fresh_component_objects():
    model = fixed.FixedBetaDifferenceModel(
        _component(kets=2, seed=1), _component(kets=2, seed=2), 0.2
    )
    parameterization = packet2.FixedBetaParameterization.from_model(model)
    vector = parameterization.pack(model)
    first = parameterization.unpack(vector)
    second = parameterization.unpack(vector)
    assert first.positive is not second.positive
    assert first.negative is not second.negative
    first.positive.alpha[0, 0, 0] += 10.0
    assert first.positive.alpha[0, 0, 0] != second.positive.alpha[0, 0, 0]
    np.testing.assert_array_equal(parameterization.pack(second), vector)


def test_beta_zero_density_jacobian_is_exact_component_interface():
    positive = _component(kets=2, seed=3)
    model = fixed.FixedBetaDifferenceModel(positive, None, 0.0)
    parameterization = packet2.FixedBetaParameterization.from_model(model)
    vector = parameterization.pack(model)
    X = np.linspace(-1.3, 1.1, 7)[:, None]
    theta = np.array([0.31])
    expected_density, expected_jacobian = lossy_pdf_and_jac_mixed(
        positive, X, theta, eta=0.79
    )
    density, jacobian = parameterization.density_and_jacobian(
        vector, X, theta, eta=0.79
    )
    np.testing.assert_array_equal(density, expected_density)
    np.testing.assert_array_equal(
        density, model.pdf(X, theta, eta=0.79)
    )
    np.testing.assert_array_equal(jacobian, expected_jacobian)


def test_signed_density_jacobian_matches_packet1_and_central_difference():
    model = fixed.FixedBetaDifferenceModel(
        _component(kets=2, seed=4), _component(kets=2, seed=5), 0.3
    )
    parameterization = packet2.FixedBetaParameterization.from_model(model)
    vector = parameterization.pack(model)
    X = np.array([[-1.2], [-0.4], [0.1], [0.7], [1.3]])
    theta = np.array([0.43])
    eta = 0.77
    density, jacobian = parameterization.density_and_jacobian(
        vector, X, theta, eta
    )
    np.testing.assert_allclose(
        density, model.pdf(X, theta, eta), rtol=2e-14, atol=2e-15
    )

    jacobian_fd = np.zeros_like(jacobian)
    eps = 1e-5
    for i in range(len(vector)):
        vp = vector.copy(); vp[i] += eps
        vm = vector.copy(); vm[i] -= eps
        jacobian_fd[:, i] = (
            parameterization.density_and_jacobian(vp, X, theta, eta)[0]
            - parameterization.density_and_jacobian(vm, X, theta, eta)[0]
        ) / (2.0 * eps)
    scale = np.maximum(
        np.abs(jacobian_fd), 1e-3 * np.max(np.abs(jacobian_fd))
    )
    assert np.max(np.abs(jacobian - jacobian_fd) / scale) < 3e-7


def test_dense_grid_barrier_equal_weights_groups_and_matches_gradient_fd():
    model = fixed.FixedBetaDifferenceModel(
        _component(alpha=2.5), _component(alpha=0.0), 0.4
    )
    parameterization = packet2.FixedBetaParameterization.from_model(model)
    vector = parameterization.pack(model)
    groups = [
        (np.array([0.0]), np.array([[-0.15], [0.0], [0.15]])),
        (np.array([0.35]), np.linspace(-2.5, 2.5, 11)[:, None]),
    ]
    eta = 0.8
    value, gradient = packet2.dense_grid_barrier_and_grad(
        parameterization, vector, groups, eta
    )
    value_only = packet2.dense_grid_barrier(
        parameterization, vector, groups, eta
    )
    densities = [
        parameterization.density_and_jacobian(
            vector, X, theta, eta
        )[0]
        for theta, X in groups
    ]
    assert any(np.any(density < 0.0) for density in densities)
    expected = np.mean([
        np.mean(np.minimum(density, 0.0) ** 2) for density in densities
    ])
    assert value == pytest.approx(expected, rel=2e-14)
    assert value_only == pytest.approx(value, rel=2e-14)

    gradient_fd = np.zeros_like(vector)
    eps = 1e-5
    for i in range(len(vector)):
        vp = vector.copy(); vp[i] += eps
        vm = vector.copy(); vm[i] -= eps
        gradient_fd[i] = (
            packet2.dense_grid_barrier_and_grad(
                parameterization, vp, groups, eta
            )[0]
            - packet2.dense_grid_barrier_and_grad(
                parameterization, vm, groups, eta
            )[0]
        ) / (2.0 * eps)
    np.testing.assert_allclose(gradient, gradient_fd, rtol=2e-7, atol=2e-9)


def test_packet2_boundaries_fail_closed():
    model = fixed.FixedBetaDifferenceModel(_component(), None, 0.0)
    parameterization = packet2.FixedBetaParameterization.from_model(model)
    vector = parameterization.pack(model)
    with pytest.raises(ValueError, match="length"):
        parameterization.unpack(vector[:-1])
    invalid = vector.copy(); invalid[0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        parameterization.unpack(invalid)
    with pytest.raises(ValueError, match="grid_groups"):
        packet2.dense_grid_barrier_and_grad(
            parameterization, vector, [], eta=0.8
        )
    with pytest.raises(ValueError, match="grid_groups"):
        packet2.dense_grid_barrier(
            parameterization, vector, [], eta=0.8
        )
    with pytest.raises(NotImplementedError, match="sigma2"):
        parameterization.density_and_jacobian(
            vector, np.zeros((1, 1)), np.zeros(1), eta=1.0
        )
    with pytest.raises(fixed.ObservationInputError):
        parameterization.density_and_jacobian(
            vector, np.zeros((1, 2)), np.zeros(1), eta=0.8
        )
