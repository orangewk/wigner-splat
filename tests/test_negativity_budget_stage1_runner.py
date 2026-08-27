"""Synthetic gates for the fixed-schedule Stage 1 candidate runner."""

from __future__ import annotations

from dataclasses import fields
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
runner = import_module(
    "experiments.33_negativity_budget.stage1_runner"
)


def _train_groups():
    return [(np.array([0.0]), np.array([[1.8], [3.0], [4.0]]))]


def _setup():
    return stage1_setup_module.prepare_stage1_candidate(
        _train_groups(), beta=0.0, seed=0
    )


def _evaluation(index: int, eta=0.8):
    value = float(index)
    return objective_module.Stage1ObjectiveEvaluation(
        objective=value,
        train_nll=value,
        barrier=0.0,
        eta=eta,
    )


def _successful_step(state, *, backtracks=0, eta_fd_step=1e-4):
    next_iteration = state.iteration + 1
    next_state = adam_module.Stage1AdamState(
        parameters=state.parameters + 1e-6,
        eta_logit=state.eta_logit,
        moment1=state.moment1 + 1e-4,
        moment2=state.moment2 + 1e-6,
        iteration=next_iteration,
    )
    return adam_module.Stage1AdamStepResult(
        state=next_state,
        source_evaluation=_evaluation(state.iteration),
        candidate_evaluation=_evaluation(next_iteration),
        backtracks=backtracks,
        scale=adam_module.BACKTRACK_FACTOR ** backtracks,
        eta_fd_step=eta_fd_step,
    )


def test_fixed_runner_starts_exactly_like_exp18_and_completes_100_steps(
    monkeypatch,
):
    seen = []

    def fake_value(self, _parameters, eta_logit):
        assert self.setup is setup
        assert eta_logit == float(
            np.log(runner.ETA0 / (1.0 - runner.ETA0))
        )
        return _evaluation(0)

    def fake_step(objective, state):
        assert objective.setup is setup
        if state.iteration == 0:
            np.testing.assert_array_equal(
                state.parameters, setup.initial_parameters
            )
            np.testing.assert_array_equal(
                state.moment1, np.zeros(len(state.moment1))
            )
            np.testing.assert_array_equal(
                state.moment2, np.zeros(len(state.moment2))
            )
        seen.append(state.iteration)
        next_iteration = state.iteration + 1
        backtracks = (
            2 if next_iteration % 25 == 0
            else 1 if next_iteration % 10 == 0
            else 0
        )
        eta_fd_step = 5e-5 if next_iteration % 2 == 0 else 1e-4
        return _successful_step(
            state,
            backtracks=backtracks,
            eta_fd_step=eta_fd_step,
        )

    setup = _setup()
    monkeypatch.setattr(objective_module.Stage1Objective, "value", fake_value)
    monkeypatch.setattr(adam_module, "stage1_adam_step", fake_step)

    result = runner.run_stage1_candidate(setup, barrier_weight=0.0)
    assert seen == list(range(100))
    assert result.status is runner.Stage1RunStatus.COMPLETED
    assert result.state.iteration == 100
    assert result.initial_evaluation.objective == 0.0
    assert result.terminal_evaluation.objective == 100.0
    assert result.backtracked_steps == 12
    assert result.total_backtracks == 16
    assert result.max_backtracks_used == 2
    assert result.min_eta_fd_step == 5e-5


@pytest.mark.parametrize(
    ("failure", "expected_status"),
    [
        (
            adam_module.NoFeasibleAdamStep(17),
            runner.Stage1RunStatus.NO_FEASIBLE_STEP,
        ),
        (
            objective_module.EtaGradientUnavailable("test"),
            runner.Stage1RunStatus.ETA_GRADIENT_UNAVAILABLE,
        ),
        (
            FloatingPointError("test"),
            runner.Stage1RunStatus.NONFINITE_UPDATE,
        ),
        (
            NotImplementedError("test"),
            runner.Stage1RunStatus.UNSUPPORTED_GRADIENT,
        ),
    ],
)
def test_declared_failure_keeps_last_committed_state_and_metrics(
    monkeypatch, failure, expected_status
):
    setup = _setup()

    def fake_value(_self, _parameters, _eta_logit):
        return _evaluation(0)

    def fake_step(_objective, state):
        if state.iteration == 0:
            return _successful_step(state, backtracks=3)
        raise failure

    monkeypatch.setattr(objective_module.Stage1Objective, "value", fake_value)
    monkeypatch.setattr(adam_module, "stage1_adam_step", fake_step)

    result = runner.run_stage1_candidate(setup, barrier_weight=1.0)
    assert result.status is expected_status
    assert result.state.iteration == 1
    assert result.terminal_evaluation.objective == 1.0
    assert result.backtracked_steps == 1
    assert result.total_backtracks == 3
    assert result.max_backtracks_used == 3
    assert result.min_eta_fd_step == 1e-4


@pytest.mark.parametrize("failure", [ValueError("bug"), RuntimeError("bug")])
def test_unexpected_step_failure_is_not_relabelled(monkeypatch, failure):
    setup = _setup()
    monkeypatch.setattr(
        objective_module.Stage1Objective,
        "value",
        lambda *_args: _evaluation(0),
    )

    def fake_step(*_args):
        raise failure

    monkeypatch.setattr(adam_module, "stage1_adam_step", fake_step)
    with pytest.raises(type(failure), match="bug"):
        runner.run_stage1_candidate(setup, barrier_weight=1.0)


def test_initial_failure_propagates_before_any_step(monkeypatch):
    setup = _setup()

    def invalid_initial(*_args):
        raise fixed.NonPositiveDensityError(0, 1, 3)

    def unexpected_step(*_args):
        raise AssertionError("step must not run after invalid initialization")

    monkeypatch.setattr(
        objective_module.Stage1Objective, "value", invalid_initial
    )
    monkeypatch.setattr(adam_module, "stage1_adam_step", unexpected_step)
    with pytest.raises(fixed.NonPositiveDensityError):
        runner.run_stage1_candidate(setup, barrier_weight=1.0)


def test_real_synthetic_candidate_completes_the_fixed_schedule():
    result = runner.run_stage1_candidate(_setup(), barrier_weight=0.0)
    assert result.status is runner.Stage1RunStatus.COMPLETED
    assert result.state.iteration == runner.STAGE1_ITERATIONS
    assert np.isfinite(result.terminal_evaluation.objective)
    assert np.isfinite(result.terminal_evaluation.train_nll)
    assert 0.0 < result.terminal_evaluation.eta < 1.0


def test_result_contract_rejects_inconsistent_completion_and_scope():
    setup = _setup()
    count = setup.parameterization.parameter_count + 1
    state = adam_module.Stage1AdamState(
        setup.initial_parameters,
        float(np.log(4.0)),
        np.zeros(count),
        np.zeros(count),
        0,
    )
    with pytest.raises(ValueError, match="completed status"):
        runner.Stage1CandidateRun(
            status=runner.Stage1RunStatus.COMPLETED,
            state=state,
            initial_evaluation=_evaluation(0),
            terminal_evaluation=_evaluation(0),
            backtracked_steps=0,
            total_backtracks=0,
            max_backtracks_used=0,
            min_eta_fd_step=None,
        )

    names = {field.name for field in fields(runner.Stage1CandidateRun)}
    assert names.isdisjoint(
        {
            "test_nll",
            "heldout_nll",
            "barrier_selection",
            "beta_grid",
            "artifact",
            "gkp_values",
        }
    )
