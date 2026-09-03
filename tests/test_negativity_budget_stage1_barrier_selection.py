"""Synthetic gates for the global Stage 1 barrier-weight selector."""

from __future__ import annotations

from dataclasses import fields, replace
from importlib import import_module

import numpy as np
import pytest


stage1_setup = import_module(
    "experiments.33_negativity_budget.stage1_setup"
)
objective_module = import_module(
    "experiments.33_negativity_budget.stage1_objective"
)
adam_module = import_module(
    "experiments.33_negativity_budget.stage1_adam_step"
)
runner_module = import_module(
    "experiments.33_negativity_budget.stage1_runner"
)
selection = import_module(
    "experiments.33_negativity_budget.stage1_barrier_selection"
)


def _train_groups(offset=0.0):
    return [
        (
            np.array([0.0]),
            np.array([[1.8 + offset], [3.0 + offset], [4.0 + offset]]),
        )
    ]


def _setup(seed=0, offset=0.0, beta=0.1):
    return stage1_setup.prepare_stage1_candidate(
        _train_groups(offset), beta=beta, seed=seed
    )


def _run(setup, weight, status=runner_module.Stage1RunStatus.COMPLETED):
    completed = status is runner_module.Stage1RunStatus.COMPLETED
    iteration = runner_module.STAGE1_ITERATIONS if completed else 0
    count = setup.parameterization.parameter_count + 1
    state = adam_module.Stage1AdamState(
        parameters=setup.initial_parameters,
        eta_logit=float(np.log(4.0)),
        moment1=np.zeros(count),
        moment2=np.zeros(count),
        iteration=iteration,
    )
    evaluation = objective_module.Stage1ObjectiveEvaluation(
        objective=float(weight),
        train_nll=float(weight),
        barrier=0.0,
        eta=runner_module.ETA0,
    )
    return runner_module.Stage1CandidateRun(
        status=status,
        state=state,
        initial_evaluation=evaluation,
        terminal_evaluation=evaluation,
        backtracked_steps=0,
        total_backtracks=0,
        max_backtracks_used=0,
        min_eta_fd_step=(1e-4 if completed else None),
    )


def _diagnostic(admissible):
    return selection.GridDiagnostics(
        point_count=1025,
        nonpositive_count=0 if admissible else 1,
        nonfinite_count=0,
        minimum_finite_density=1e-9 if admissible else 0.0,
    )


def test_declared_ladder_runs_every_cell_and_selects_first_global_pair(
    monkeypatch,
):
    assert selection.BARRIER_WEIGHT_CANDIDATES == (
        0.0,
        0.1,
        1.0,
        10.0,
        100.0,
        1000.0,
    )
    setups = (_setup(seed=0), _setup(seed=1, offset=0.2))
    calls = []

    def fake_run(setup, weight):
        calls.append((setup, weight))
        return _run(setup, weight)

    def fake_diagnostics(setup, run):
        weight = run.terminal_evaluation.train_nll
        allowed = (
            {0.1, 1.0, 10.0, 100.0}
            if setup.seed == 0
            else {1.0, 10.0, 1000.0}
        )
        return _diagnostic(weight in allowed)

    monkeypatch.setattr(
        runner_module, "run_stage1_candidate", fake_run
    )
    monkeypatch.setattr(
        selection, "_terminal_grid_diagnostics", fake_diagnostics
    )

    result = selection.run_stage1_barrier_selection(setups)
    assert len(calls) == len(setups) * len(selection.BARRIER_WEIGHT_CANDIDATES)
    for setup in setups:
        assert [weight for seen, weight in calls if seen is setup] == list(
            selection.BARRIER_WEIGHT_CANDIDATES
        )
    assert result.admissible_weights == (1.0, 10.0)
    assert result.status is selection.Stage1BarrierSelectionStatus.SELECTED
    assert result.selected_weight == 1.0
    assert len(result.assessments) == 12


def test_isolated_admissible_weights_return_no_selection(monkeypatch):
    setup = _setup()
    allowed = {0.1, 10.0, 1000.0}
    monkeypatch.setattr(
        runner_module,
        "run_stage1_candidate",
        lambda setup, weight: _run(setup, weight),
    )
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, run: _diagnostic(
            run.terminal_evaluation.train_nll in allowed
        ),
    )

    result = selection.run_stage1_barrier_selection([setup])
    assert result.admissible_weights == (0.1, 10.0, 1000.0)
    assert (
        result.status
        is selection.Stage1BarrierSelectionStatus.NO_STABLE_ADMISSIBLE_PAIR
    )
    assert result.selected_weight is None


def test_numerical_stop_is_not_admissible_even_when_grid_is_positive(
    monkeypatch,
):
    setup = _setup()

    def fake_run(setup, weight):
        status = (
            runner_module.Stage1RunStatus.NO_FEASIBLE_STEP
            if weight == 1.0
            else runner_module.Stage1RunStatus.COMPLETED
        )
        return _run(setup, weight, status=status)

    monkeypatch.setattr(runner_module, "run_stage1_candidate", fake_run)
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, _run: _diagnostic(True),
    )

    result = selection.run_stage1_barrier_selection([setup])
    assert 1.0 not in result.admissible_weights
    assert result.selected_weight == 0.0


def test_grid_diagnostics_count_strict_and_nonfinite_failures_separately():
    grid = selection._summarize_grid_densities(
        [
            np.array([1e-9, 0.0, -0.2]),
            np.array([np.nan, np.inf]),
        ]
    )
    assert grid.point_count == 5
    assert grid.nonpositive_count == 2
    assert grid.nonfinite_count == 2
    assert grid.minimum_finite_density == -0.2
    assert not grid.strictly_positive

    all_nonfinite = selection._summarize_grid_densities(
        [np.array([np.nan, -np.inf])]
    )
    assert all_nonfinite.minimum_finite_density is None
    assert not all_nonfinite.strictly_positive

    with pytest.raises(ValueError, match="minimum"):
        selection.GridDiagnostics(3, 1, 0, 1e-9)
    with pytest.raises(ValueError, match="minimum"):
        selection.GridDiagnostics(3, 0, 0, 0.0)


def test_terminal_grid_diagnostic_rejects_wrong_pdf_shape(monkeypatch):
    setup = _setup()
    run = _run(setup, 0.1)

    class WrongShapeModel:
        @staticmethod
        def pdf(X, _theta, _eta):
            return np.ones(len(X) - 1)

    monkeypatch.setattr(
        type(setup.parameterization),
        "unpack",
        lambda _self, _parameters: WrongShapeModel(),
    )
    with pytest.raises(ValueError, match="invalid shape"):
        selection._terminal_grid_diagnostics(setup, run)


def test_input_boundary_is_train_setup_only_and_identity_unique():
    positive = _setup()
    beta_zero = _setup(beta=0.0)
    with pytest.raises(ValueError, match="at least one"):
        selection.run_stage1_barrier_selection([])
    with pytest.raises(TypeError, match="Stage1CandidateSetup"):
        selection.run_stage1_barrier_selection([object()])
    with pytest.raises(ValueError, match="beta > 0"):
        selection.run_stage1_barrier_selection([beta_zero])
    with pytest.raises(ValueError, match="only once"):
        selection.run_stage1_barrier_selection([positive, positive])


def test_result_scope_has_no_test_artifact_or_stage2_decision():
    assessment_fields = {field.name for field in fields(
        selection.Stage1BarrierAssessment
    )}
    result_fields = {field.name for field in fields(
        selection.Stage1BarrierSelection
    )}
    forbidden = {
        "test_data",
        "test_nll",
        "heldout_nll",
        "artifact",
        "stage2_beta",
        "scientific_verdict",
        "invalid_rate",
    }
    assert assessment_fields.isdisjoint(forbidden)
    assert result_fields.isdisjoint(forbidden)


def test_selection_verdict_cannot_be_replaced_independently_of_data(
    monkeypatch,
):
    setup = _setup()
    monkeypatch.setattr(
        runner_module,
        "run_stage1_candidate",
        lambda setup, weight: _run(setup, weight),
    )
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, _run: _diagnostic(True),
    )
    result = selection.run_stage1_barrier_selection([setup])
    assert result.selected_weight == 0.0
    with pytest.raises(ValueError, match="verdict"):
        replace(result, selected_weight=1.0)
    with pytest.raises(ValueError, match="verdict"):
        replace(
            result,
            status=(
                selection.Stage1BarrierSelectionStatus.NO_STABLE_ADMISSIBLE_PAIR
            ),
            selected_weight=None,
        )
