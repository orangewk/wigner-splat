"""Synthetic gates for the Stage 1 train objective packet."""

from __future__ import annotations

from importlib import import_module

import numpy as np
import pytest

from wigner_splat.bbdagS import (
    MixedSqueezedKetState,
    nll_and_grad_lossy_mixed,
)


fixed = import_module("experiments.33_negativity_budget.fixed_beta")
packet2 = import_module("experiments.33_negativity_budget.packet2")
stage1_setup_module = import_module(
    "experiments.33_negativity_budget.stage1_setup"
)
objective_module = import_module(
    "experiments.33_negativity_budget.stage1_objective"
)


def _eta_logit(eta=0.8):
    return float(np.log(eta / (1.0 - eta)))


def _positive_train_groups():
    return [
        (np.array([0.0]), np.array([[1.8], [3.0], [4.0]])),
    ]


def _signed_probe_vector(candidate):
    positive = MixedSqueezedKetState(
        z=np.pad(np.ones((1, 1), complex), ((0, 3), (0, 3))),
        alpha=np.pad(
            np.array([[[2.5 + 0.0j]]]), ((0, 3), (0, 3), (0, 0))
        ),
        xi=np.zeros((4, 4, 1), complex),
    )
    negative = MixedSqueezedKetState(
        z=np.array([[1.0, 0.0]], complex),
        alpha=np.zeros((1, 2, 1), complex),
        xi=np.zeros((1, 2, 1), complex),
    )
    model = fixed.FixedBetaDifferenceModel(
        positive, negative, candidate.beta
    )
    return candidate.parameterization.pack(model)


def test_objective_value_composes_declared_train_nll_and_grid_barrier():
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _positive_train_groups(), beta=0.4, seed=0
    )
    vector = _signed_probe_vector(candidate)
    eta_logit = _eta_logit()
    eta = 0.8
    objective = objective_module.Stage1Objective(candidate, barrier_weight=10.0)
    evaluation = objective.value(vector, eta_logit)
    model = candidate.parameterization.unpack(vector)
    expected_nll = fixed.mean_nll(model, candidate.train_groups, eta)
    expected_barrier = packet2.dense_grid_barrier(
        candidate.parameterization,
        vector,
        candidate.grid_groups,
        eta,
    )
    assert expected_barrier > 0.0
    assert evaluation.train_nll == pytest.approx(expected_nll, rel=2e-14)
    assert evaluation.barrier == pytest.approx(expected_barrier, rel=2e-14)
    assert evaluation.objective == pytest.approx(
        expected_nll + 10.0 * expected_barrier, rel=2e-14
    )
    assert evaluation.eta == pytest.approx(eta)


def test_state_and_eta_logit_gradients_match_independent_central_difference():
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _positive_train_groups(), beta=0.4, seed=0
    )
    vector = _signed_probe_vector(candidate)
    eta_logit = _eta_logit()
    objective = objective_module.Stage1Objective(candidate, barrier_weight=10.0)
    result = objective.value_and_grad(vector, eta_logit)
    combined = np.concatenate([vector, [eta_logit]])
    gradient_fd = np.zeros_like(combined)
    eps = 1e-5
    for index in range(len(combined)):
        plus = combined.copy()
        plus[index] += eps
        minus = combined.copy()
        minus[index] -= eps
        gradient_fd[index] = (
            objective.value(plus[:-1], plus[-1]).objective
            - objective.value(minus[:-1], minus[-1]).objective
        ) / (2.0 * eps)
    scale = np.maximum(
        np.abs(gradient_fd), 1e-3 * np.max(np.abs(gradient_fd))
    )
    assert np.max(np.abs(result.gradient - gradient_fd) / scale) < 8e-7
    assert result.eta_fd_step == objective_module.ETA_FD_STEP
    assert not result.gradient.flags.writeable


def test_beta_zero_weight_zero_matches_existing_strict_component_objective():
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _positive_train_groups(), beta=0.0, seed=7
    )
    objective = objective_module.Stage1Objective(candidate, barrier_weight=0.0)
    eta_logit = _eta_logit()
    result = objective.value_and_grad(candidate.initial_parameters, eta_logit)
    model = candidate.parameterization.unpack(candidate.initial_parameters)
    expected_value, expected_gradient = nll_and_grad_lossy_mixed(
        model.positive, candidate.train_groups, eta=0.8
    )
    assert result.evaluation.objective == pytest.approx(expected_value, rel=2e-14)
    assert result.evaluation.train_nll == pytest.approx(expected_value, rel=2e-14)
    assert result.evaluation.barrier == 0.0
    np.testing.assert_allclose(
        result.gradient[:-1], expected_gradient, rtol=3e-13, atol=3e-14
    )
    gradient_fd = np.zeros_like(candidate.initial_parameters)
    eps = 1e-5
    for index in range(len(gradient_fd)):
        plus = candidate.initial_parameters.copy()
        plus[index] += eps
        minus = candidate.initial_parameters.copy()
        minus[index] -= eps
        gradient_fd[index] = (
            objective.value(plus, eta_logit).objective
            - objective.value(minus, eta_logit).objective
        ) / (2.0 * eps)
    scale = np.maximum(
        np.abs(gradient_fd), 1e-3 * np.max(np.abs(gradient_fd))
    )
    assert np.max(np.abs(result.gradient[:-1] - gradient_fd) / scale) < 5e-7


def test_nonpositive_train_density_uses_packet1_strict_error():
    train = [(np.array([0.0]), np.array([[-0.1], [0.1]]))]
    candidate = stage1_setup_module.prepare_stage1_candidate(
        train, beta=0.4, seed=0
    )
    objective = objective_module.Stage1Objective(candidate, barrier_weight=1.0)
    with pytest.raises(fixed.NonPositiveDensityError):
        objective.value(_signed_probe_vector(candidate), _eta_logit())


@pytest.mark.parametrize("barrier_weight", [-1.0, np.nan, np.inf, True])
def test_barrier_weight_fails_closed(barrier_weight):
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _positive_train_groups(), beta=0.0, seed=0
    )
    with pytest.raises((TypeError, ValueError)):
        objective_module.Stage1Objective(candidate, barrier_weight)


@pytest.mark.parametrize("eta_logit", [np.nan, np.inf, -np.inf, True, 40.0])
def test_eta_logit_fails_closed(eta_logit):
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _positive_train_groups(), beta=0.0, seed=0
    )
    objective = objective_module.Stage1Objective(candidate, barrier_weight=0.0)
    with pytest.raises((fixed.LossParameterError, FloatingPointError)):
        objective.value(candidate.initial_parameters, eta_logit)


def test_invalid_setup_and_parameter_vector_fail_closed():
    with pytest.raises(TypeError, match="Stage1CandidateSetup"):
        objective_module.Stage1Objective(object(), 1.0)
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _positive_train_groups(), beta=0.0, seed=0
    )
    objective = objective_module.Stage1Objective(candidate, barrier_weight=0.0)
    invalid = candidate.initial_parameters.copy()
    invalid[0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        objective.value(invalid, _eta_logit())


def test_eta_gradient_halves_to_first_valid_symmetric_step(monkeypatch):
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _positive_train_groups(), beta=0.0, seed=0
    )
    objective = objective_module.Stage1Objective(candidate, barrier_weight=0.0)

    def fake_value(self, _parameters, eta_logit):
        if abs(eta_logit) > 5e-5:
            raise fixed.NonPositiveDensityError(0, 1, 1)
        return objective_module.Stage1ObjectiveEvaluation(
            objective=eta_logit ** 2,
            train_nll=eta_logit ** 2,
            barrier=0.0,
            eta=objective_module._sigmoid(eta_logit),
        )

    def fake_state_gradient(self, _parameters, _eta, _barrier):
        return np.zeros(self.setup.parameterization.parameter_count)

    monkeypatch.setattr(objective_module.Stage1Objective, "value", fake_value)
    monkeypatch.setattr(
        objective_module.Stage1Objective, "_state_gradient", fake_state_gradient
    )
    result = objective.value_and_grad(candidate.initial_parameters, 0.0)
    assert result.eta_fd_step == pytest.approx(5e-5)


def test_eta_gradient_unavailable_after_declared_halvings(monkeypatch):
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _positive_train_groups(), beta=0.0, seed=0
    )
    objective = objective_module.Stage1Objective(candidate, barrier_weight=0.0)

    def fake_value(self, _parameters, eta_logit):
        if eta_logit != 0.0:
            raise fixed.NonPositiveDensityError(0, 1, 1)
        return objective_module.Stage1ObjectiveEvaluation(
            objective=0.0,
            train_nll=0.0,
            barrier=0.0,
            eta=0.5,
        )

    def fake_state_gradient(self, _parameters, _eta, _barrier):
        return np.zeros(self.setup.parameterization.parameter_count)

    monkeypatch.setattr(objective_module.Stage1Objective, "value", fake_value)
    monkeypatch.setattr(
        objective_module.Stage1Objective, "_state_gradient", fake_state_gradient
    )
    with pytest.raises(objective_module.EtaGradientUnavailable):
        objective.value_and_grad(candidate.initial_parameters, 0.0)
