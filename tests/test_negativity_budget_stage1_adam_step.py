"""Synthetic gates for one immutable Stage 1 Adam transition."""

from __future__ import annotations

from importlib import import_module

import numpy as np
import pytest


fixed = import_module("experiments.33_negativity_budget.fixed_beta")
stage1_setup_module = import_module(
    "experiments.33_negativity_budget.stage1_setup"
)
objective_module = import_module(
    "experiments.33_negativity_budget.stage1_objective"
)
adam_module = import_module(
    "experiments.33_negativity_budget.stage1_adam_step"
)


def _train_groups():
    return [(np.array([0.0]), np.array([[1.8], [3.0], [4.0]]))]


def _eta_logit(eta=0.8):
    return float(np.log(eta / (1.0 - eta)))


def _objective_and_state(*, beta=0.0, barrier_weight=0.0, iteration=0):
    candidate = stage1_setup_module.prepare_stage1_candidate(
        _train_groups(), beta=beta, seed=0
    )
    objective = objective_module.Stage1Objective(candidate, barrier_weight)
    count = candidate.parameterization.parameter_count + 1
    state = adam_module.Stage1AdamState(
        parameters=candidate.initial_parameters,
        eta_logit=_eta_logit(),
        moment1=np.zeros(count),
        moment2=np.zeros(count),
        iteration=iteration,
    )
    return candidate, objective, state


def test_optimizer_contract_constants_and_state_are_fixed_and_read_only():
    assert adam_module.LEARNING_RATE == 0.05
    assert adam_module.ADAM_BETA1 == 0.9
    assert adam_module.ADAM_BETA2 == 0.999
    assert adam_module.ADAM_GRADIENT_WEIGHT1 == 0.1
    assert adam_module.ADAM_GRADIENT_WEIGHT2 == 0.001
    assert adam_module.ADAM_EPSILON == 1e-8
    assert adam_module.BACKTRACK_FACTOR == 0.5
    assert adam_module.MAX_BACKTRACKS == 16

    parameters = np.array([1.0, 2.0])
    moment1 = np.array([0.1, 0.2, 0.3])
    moment2 = np.array([0.4, 0.5, 0.6])
    state = adam_module.Stage1AdamState(
        parameters, 0.2, moment1, moment2, iteration=3
    )
    parameters[:] = 9.0
    moment1[:] = 9.0
    moment2[:] = 9.0
    np.testing.assert_array_equal(state.parameters, np.array([1.0, 2.0]))
    np.testing.assert_array_equal(state.moment1, np.array([0.1, 0.2, 0.3]))
    np.testing.assert_array_equal(state.moment2, np.array([0.4, 0.5, 0.6]))
    assert not state.parameters.flags.writeable
    assert not state.moment1.flags.writeable
    assert not state.moment2.flags.writeable


def test_beta_zero_first_step_matches_existing_exp18_adam_formula():
    _, objective, state = _objective_and_state()
    objective_result = objective.value_and_grad(
        state.parameters, state.eta_logit
    )
    gradient = objective_result.gradient
    expected_moment1 = 0.1 * gradient
    expected_moment2 = 0.001 * gradient ** 2
    expected_update = adam_module.LEARNING_RATE * gradient / (
        np.abs(gradient) + adam_module.ADAM_EPSILON
    )

    result = adam_module.stage1_adam_step(objective, state)
    assert result.backtracks == 0
    assert result.scale == 1.0
    assert result.state.iteration == 1
    np.testing.assert_allclose(
        result.state.parameters,
        state.parameters - expected_update[:-1],
        rtol=0.0,
        atol=2e-14,
    )
    assert result.state.eta_logit == pytest.approx(
        state.eta_logit - expected_update[-1], abs=2e-14
    )
    np.testing.assert_array_equal(result.state.moment1, expected_moment1)
    np.testing.assert_array_equal(result.state.moment2, expected_moment2)


def test_nonzero_moments_and_iteration_match_independent_bias_correction():
    candidate, objective, zero_state = _objective_and_state(iteration=4)
    count = candidate.parameterization.parameter_count + 1
    state = adam_module.Stage1AdamState(
        parameters=zero_state.parameters,
        eta_logit=zero_state.eta_logit,
        moment1=np.linspace(-1e-3, 1e-3, count),
        moment2=np.linspace(1e-3, 2e-3, count),
        iteration=4,
    )
    gradient = objective.value_and_grad(
        state.parameters, state.eta_logit
    ).gradient
    trial1 = 0.9 * state.moment1 + 0.1 * gradient
    trial2 = 0.999 * state.moment2 + 0.001 * gradient ** 2
    corrected1 = trial1 / (1.0 - 0.9 ** 5)
    corrected2 = trial2 / (1.0 - 0.999 ** 5)
    update = 0.05 * corrected1 / (np.sqrt(corrected2) + 1e-8)

    result = adam_module.stage1_adam_step(objective, state)
    assert result.backtracks == 0
    np.testing.assert_allclose(
        result.state.parameters,
        state.parameters - update[:-1],
        rtol=0.0,
        atol=2e-14,
    )
    assert result.state.eta_logit == pytest.approx(
        state.eta_logit - update[-1], abs=2e-14
    )
    np.testing.assert_array_equal(result.state.moment1, trial1)
    np.testing.assert_array_equal(result.state.moment2, trial2)
    assert result.state.iteration == 5


def test_backtracking_commits_first_valid_scale_and_full_moments(monkeypatch):
    _, objective, state = _objective_and_state()
    count = len(state.moment1)
    gradient = np.ones(count)
    source = objective_module.Stage1ObjectiveEvaluation(
        objective=1.0, train_nll=1.0, barrier=0.0, eta=0.8
    )

    def fake_value_and_grad(self, _parameters, _eta_logit):
        return objective_module.Stage1ObjectiveResult(
            evaluation=source,
            gradient=gradient,
            eta_fd_step=1e-4,
        )

    def fake_value(self, parameters, eta_logit):
        parameter_delta = state.parameters[0] - np.asarray(parameters)[0]
        logit_delta = state.eta_logit - eta_logit
        assert parameter_delta == pytest.approx(logit_delta)
        if parameter_delta > 0.02:
            raise fixed.NonPositiveDensityError(0, 1, 1)
        return objective_module.Stage1ObjectiveEvaluation(
            objective=99.0, train_nll=99.0, barrier=0.0, eta=0.8
        )

    monkeypatch.setattr(
        objective_module.Stage1Objective,
        "value_and_grad",
        fake_value_and_grad,
    )
    monkeypatch.setattr(objective_module.Stage1Objective, "value", fake_value)

    result = adam_module.stage1_adam_step(objective, state)
    expected_full_update = 0.05 / (1.0 + 1e-8)
    assert result.backtracks == 2
    assert result.scale == 0.25
    assert state.parameters[0] - result.state.parameters[0] == pytest.approx(
        0.25 * expected_full_update
    )
    assert result.candidate_evaluation.objective > source.objective
    np.testing.assert_array_equal(result.state.moment1, np.full(count, 0.1))
    np.testing.assert_array_equal(result.state.moment2, np.full(count, 0.001))


def test_all_invalid_candidates_raise_without_mutating_input(monkeypatch):
    _, objective, state = _objective_and_state()
    original = (
        state.parameters.copy(),
        state.moment1.copy(),
        state.moment2.copy(),
        state.eta_logit,
        state.iteration,
    )
    count = len(state.moment1)
    calls = []

    def fake_value_and_grad(self, _parameters, _eta_logit):
        return objective_module.Stage1ObjectiveResult(
            evaluation=objective_module.Stage1ObjectiveEvaluation(
                objective=1.0, train_nll=1.0, barrier=0.0, eta=0.8
            ),
            gradient=np.ones(count),
            eta_fd_step=1e-4,
        )

    def fake_value(self, _parameters, _eta_logit):
        calls.append(1)
        raise fixed.NonPositiveDensityError(0, 1, 1)

    monkeypatch.setattr(
        objective_module.Stage1Objective,
        "value_and_grad",
        fake_value_and_grad,
    )
    monkeypatch.setattr(objective_module.Stage1Objective, "value", fake_value)

    with pytest.raises(adam_module.NoFeasibleAdamStep) as exc:
        adam_module.stage1_adam_step(objective, state)
    assert exc.value.attempts == 17
    assert len(calls) == 17
    np.testing.assert_array_equal(state.parameters, original[0])
    np.testing.assert_array_equal(state.moment1, original[1])
    np.testing.assert_array_equal(state.moment2, original[2])
    assert state.eta_logit == original[3]
    assert state.iteration == original[4]


@pytest.mark.parametrize("gradient_value", [np.nan, 1e308])
def test_nonfinite_gradient_or_update_fails_before_candidate(monkeypatch, gradient_value):
    _, objective, state = _objective_and_state()
    count = len(state.moment1)

    def fake_value_and_grad(self, _parameters, _eta_logit):
        return objective_module.Stage1ObjectiveResult(
            evaluation=objective_module.Stage1ObjectiveEvaluation(
                objective=1.0, train_nll=1.0, barrier=0.0, eta=0.8
            ),
            gradient=np.full(count, gradient_value),
            eta_fd_step=1e-4,
        )

    def unexpected_value(*_args, **_kwargs):
        raise AssertionError("candidate value must not be evaluated")

    monkeypatch.setattr(
        objective_module.Stage1Objective,
        "value_and_grad",
        fake_value_and_grad,
    )
    monkeypatch.setattr(
        objective_module.Stage1Objective, "value", unexpected_value
    )
    with pytest.raises(FloatingPointError):
        adam_module.stage1_adam_step(objective, state)


def test_invalid_state_and_lengths_fail_closed():
    with pytest.raises(ValueError):
        adam_module.Stage1AdamState(
            np.array([1.0]), 0.0, np.array([0.0]), np.array([-1.0]), 0
        )
    with pytest.raises(ValueError):
        adam_module.Stage1AdamState(
            np.array([1.0]), 0.0, np.array([0.0]), np.array([0.0]), True
        )
    _, objective, state = _objective_and_state()
    short_moment_state = adam_module.Stage1AdamState(
        state.parameters,
        state.eta_logit,
        state.moment1[:-1],
        state.moment2[:-1],
        0,
    )
    with pytest.raises(ValueError, match="moment1 length"):
        adam_module.stage1_adam_step(objective, short_moment_state)
    with pytest.raises(TypeError):
        adam_module.stage1_adam_step(object(), state)
    with pytest.raises(TypeError):
        adam_module.stage1_adam_step(objective, object())
