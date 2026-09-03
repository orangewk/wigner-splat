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
orchestration = import_module(
    "experiments.33_negativity_budget.stage1_orchestration"
)
packet2 = import_module("experiments.33_negativity_budget.packet2")
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


def _identity(seed=0, beta=0.1, reshuffle_seed=0):
    return orchestration.Stage1CellIdentity(
        orchestration.DATASET_ID, reshuffle_seed, beta, seed
    )


def _cell(seed=0, offset=0.0, beta=0.1, reshuffle_seed=0):
    return orchestration.Stage1CandidateCell(
        _identity(seed, beta, reshuffle_seed),
        _setup(seed, offset, beta),
    )


def _barrier_cells():
    return tuple(
        _cell(
            seed=identity.init_seed,
            offset=cell_index / 100.0,
            beta=identity.beta,
            reshuffle_seed=identity.reshuffle_seed,
        )
        for cell_index, identity in enumerate(
            orchestration.barrier_selection_identities()
        )
    )


def _run(
    setup,
    weight,
    status=runner_module.Stage1RunStatus.COMPLETED,
    terminal_train_nll=None,
    terminal_eta=runner_module.ETA0,
    cell_identity=None,
):
    if cell_identity is None:
        cell_identity = _identity(setup.seed, setup.beta)
    completed = status is runner_module.Stage1RunStatus.COMPLETED
    iteration = runner_module.STAGE1_ITERATIONS if completed else 0
    count = setup.parameterization.parameter_count + 1
    eta_logit = float(np.log(terminal_eta / (1.0 - terminal_eta)))
    _, terminal_eta = objective_module._eta_from_logit(eta_logit)
    state = adam_module.Stage1AdamState(
        parameters=setup.initial_parameters,
        eta_logit=eta_logit,
        moment1=np.zeros(count),
        moment2=np.zeros(count),
        iteration=iteration,
    )
    initial_evaluation = objective_module.Stage1ObjectiveEvaluation(
        objective=float(weight),
        train_nll=float(weight),
        barrier=0.0,
        eta=runner_module.ETA0,
    )
    terminal_train_nll = (
        float(weight)
        if terminal_train_nll is None
        else float(terminal_train_nll)
    )
    terminal_evaluation = objective_module.Stage1ObjectiveEvaluation(
        objective=terminal_train_nll,
        train_nll=terminal_train_nll,
        barrier=0.0,
        eta=terminal_eta,
    )
    return runner_module.Stage1CandidateRun(
        status=status,
        cell_identity=cell_identity,
        barrier_weight=weight,
        state=state,
        initial_evaluation=initial_evaluation,
        terminal_evaluation=terminal_evaluation,
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


def test_declared_ladder_stops_at_first_global_pair_in_weight_major_order(
    monkeypatch,
):
    assert selection.BARRIER_WEIGHT_CANDIDATES == (
        0.0,
        0.1,
        1.0,
        10.0,
        100.0,
        1_000.0,
        10_000.0,
        100_000.0,
        1_000_000.0,
        10_000_000.0,
        100_000_000.0,
        1_000_000_000.0,
        10_000_000_000.0,
        100_000_000_000.0,
        1_000_000_000_000.0,
    )
    cells = _barrier_cells()
    calls = []

    def fake_run(cell, weight):
        calls.append((cell, weight))
        return _run(cell.setup, weight, cell_identity=cell.identity)

    def fake_diagnostics(setup, run):
        weight = run.terminal_evaluation.train_nll
        allowed = {1.0, 10.0}
        return _diagnostic(weight in allowed)

    monkeypatch.setattr(
        runner_module, "run_stage1_candidate", fake_run
    )
    monkeypatch.setattr(
        selection, "_terminal_grid_diagnostics", fake_diagnostics
    )

    result = selection.run_stage1_barrier_selection(cells)
    expected_weights = (0.0, 0.1, 1.0, 10.0)
    assert calls == [
        (cell, weight) for weight in expected_weights for cell in cells
    ]
    assert result.attempted_weights == expected_weights
    assert result.admissible_weights == (1.0, 10.0)
    assert result.status is selection.Stage1BarrierSelectionStatus.SELECTED
    assert result.selected_weight == 1.0
    assert len(result.assessments) == 120


def test_isolated_admissible_weights_return_no_selection(monkeypatch):
    cells = _barrier_cells()
    allowed = {0.1, 10.0, 1000.0}
    monkeypatch.setattr(
        runner_module,
        "run_stage1_candidate",
        lambda cell, weight: _run(
            cell.setup, weight, cell_identity=cell.identity
        ),
    )
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, run: _diagnostic(
            run.terminal_evaluation.train_nll in allowed
        ),
    )

    result = selection.run_stage1_barrier_selection(cells)
    assert result.admissible_weights == (0.1, 10.0, 1000.0)
    assert result.attempted_weights == selection.BARRIER_WEIGHT_CANDIDATES
    assert (
        result.status
        is selection.Stage1BarrierSelectionStatus.NO_STABLE_ADMISSIBLE_PAIR
    )
    assert result.selected_weight is None


def test_numerical_stop_is_not_admissible_even_when_grid_is_positive(
    monkeypatch,
):
    cells = _barrier_cells()

    def fake_run(cell, weight):
        status = (
            runner_module.Stage1RunStatus.NO_FEASIBLE_STEP
            if weight == 0.1
            else runner_module.Stage1RunStatus.COMPLETED
        )
        return _run(
            cell.setup,
            weight,
            status=status,
            cell_identity=cell.identity,
        )

    monkeypatch.setattr(runner_module, "run_stage1_candidate", fake_run)
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, _run: _diagnostic(True),
    )

    result = selection.run_stage1_barrier_selection(cells)
    assert 0.1 not in result.admissible_weights
    assert result.attempted_weights == (0.0, 0.1, 1.0, 10.0)
    assert result.selected_weight == 1.0


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
    with pytest.raises(ValueError, match="real numeric scalar"):
        selection.GridDiagnostics(3, 0, 0, True)


@pytest.mark.parametrize(
    "density",
    [
        np.array([1.0 + 2.0j]),
        np.array([True]),
        np.array(["1.0"]),
        np.array([1.0], dtype=object),
    ],
)
def test_grid_diagnostics_reject_non_real_or_coercible_density(density):
    with pytest.raises(ValueError, match="real numeric"):
        selection._summarize_grid_densities([density])


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


def test_terminal_grid_diagnostic_uses_real_fixed_beta_model():
    setup = _setup()
    run = _run(setup, 0.1)

    model = setup.parameterization.unpack(run.state.parameters)
    assert isinstance(model, packet2.FixedBetaDifferenceModel)
    grid = selection._terminal_grid_diagnostics(setup, run)
    expected = selection._summarize_grid_densities(
        model.pdf(X, theta, run.terminal_evaluation.eta)
        for theta, X in setup.grid_groups
    )

    assert grid == expected
    assert grid.point_count == sum(len(X) for _theta, X in setup.grid_groups)
    assert grid.strictly_positive
    assert (
        packet2._dense_grid_barrier_value(
            setup.parameterization,
            run.state.parameters,
            setup.grid_groups,
            run.terminal_evaluation.eta,
        )
        == 0.0
    )


@pytest.mark.parametrize(
    ("value", "dtype"),
    [
        (1.0 + 2.0j, None),
        (True, None),
        ("1.0", None),
        (1.0, object),
    ],
)
def test_terminal_grid_path_rejects_coercible_density(
    monkeypatch, value, dtype
):
    setup = _setup()
    run = _run(setup, 0.1)

    class CoercibleModel:
        @staticmethod
        def pdf(X, _theta, _eta):
            return np.full(len(X), value, dtype=dtype)

    monkeypatch.setattr(
        type(setup.parameterization),
        "unpack",
        lambda _self, _parameters: CoercibleModel(),
    )
    with pytest.raises(ValueError, match="real numeric"):
        selection._terminal_grid_diagnostics(setup, run)


def test_input_boundary_is_train_cell_only_and_identity_unique():
    positive = _cell()
    beta_zero = _cell(beta=0.0)
    with pytest.raises(ValueError, match="at least one"):
        selection.run_stage1_barrier_selection([])
    with pytest.raises(TypeError, match="Stage1CandidateCell"):
        selection.run_stage1_barrier_selection([object()])
    with pytest.raises(ValueError, match="beta > 0"):
        selection.run_stage1_barrier_selection([beta_zero])
    with pytest.raises(ValueError, match="cell identity"):
        selection.run_stage1_barrier_selection([positive, positive])
    with pytest.raises(ValueError, match="declared barrier-selection view"):
        selection.run_stage1_barrier_selection([positive])


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
    assert "cell_identity" in assessment_fields
    assert assessment_fields.isdisjoint({"beta", "seed", "reshuffle_seed"})
    assert assessment_fields.isdisjoint(forbidden)
    assert result_fields.isdisjoint(forbidden)


def test_selection_verdict_cannot_be_replaced_independently_of_data(
    monkeypatch,
):
    cells = _barrier_cells()
    monkeypatch.setattr(
        runner_module,
        "run_stage1_candidate",
        lambda cell, weight: _run(
            cell.setup, weight, cell_identity=cell.identity
        ),
    )
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, _run: _diagnostic(True),
    )
    result = selection.run_stage1_barrier_selection(cells)
    assert result.selected_weight == 0.0
    with pytest.raises(ValueError, match="verdict"):
        replace(result, selected_weight=1.0)
    with pytest.raises(ValueError, match="real numeric scalar"):
        replace(result, selected_weight=np.array([0.0]))
    with pytest.raises(ValueError, match="verdict"):
        replace(
            result,
            status=(
                selection.Stage1BarrierSelectionStatus.NO_STABLE_ADMISSIBLE_PAIR
            ),
            selected_weight=None,
        )
    with pytest.raises(ValueError, match="assessment identities"):
        replace(result, assessments=tuple(reversed(result.assessments)))
    with pytest.raises(ValueError, match="declared cell view"):
        replace(
            result,
            setup_count=1,
            assessments=(result.assessments[0], result.assessments[30]),
        )


def test_result_rejects_incomplete_or_overrun_assessment_prefix(monkeypatch):
    cells = _barrier_cells()
    monkeypatch.setattr(
        runner_module,
        "run_stage1_candidate",
        lambda cell, weight: _run(
            cell.setup, weight, cell_identity=cell.identity
        ),
    )
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, _run: _diagnostic(False),
    )
    no_pair = selection.run_stage1_barrier_selection(cells)
    with pytest.raises(ValueError, match="before a verdict"):
        replace(
            no_pair,
            assessments=no_pair.assessments[: 2 * no_pair.setup_count],
        )

    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, _run: _diagnostic(True),
    )
    selected = selection.run_stage1_barrier_selection(cells)
    extra_weight = selection.BARRIER_WEIGHT_CANDIDATES[2]
    extra = tuple(
        replace(
            selected.assessments[setup_index],
            barrier_weight=extra_weight,
            run=_run(
                cell.setup,
                extra_weight,
                cell_identity=cell.identity,
            ),
        )
        for setup_index, cell in enumerate(cells)
    )
    with pytest.raises(ValueError, match="first stable pair"):
        replace(selected, assessments=selected.assessments + extra)


def test_assessment_rejects_run_from_a_different_weight(monkeypatch):
    cells = _barrier_cells()
    monkeypatch.setattr(
        runner_module,
        "run_stage1_candidate",
        lambda cell, weight: _run(
            cell.setup, weight, cell_identity=cell.identity
        ),
    )
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, _run: _diagnostic(True),
    )
    result = selection.run_stage1_barrier_selection(cells)

    with pytest.raises(ValueError, match="differs from assessment"):
        replace(
            result.assessments[0],
            run=_run(
                cells[0].setup,
                selection.BARRIER_WEIGHT_CANDIDATES[1],
                cell_identity=cells[0].identity,
            ),
        )

    other_identity = cells[1].identity
    with pytest.raises(ValueError, match="cell identity differs"):
        replace(
            result.assessments[0],
            run=_run(
                cells[1].setup,
                selection.BARRIER_WEIGHT_CANDIDATES[0],
                cell_identity=other_identity,
            ),
        )

    drifted_run = replace(
        result.assessments[-1].run,
        cell_identity=cells[-2].identity,
    )
    drifted_row = replace(
        result.assessments[-1],
        cell_identity=cells[-2].identity,
        run=drifted_run,
    )
    with pytest.raises(ValueError, match="identity differs by weight"):
        replace(
            result,
            assessments=result.assessments[:-1] + (drifted_row,),
        )


def test_train_nll_and_eta_do_not_select_the_weight(monkeypatch):
    cells = _barrier_cells()
    monkeypatch.setattr(
        selection,
        "_terminal_grid_diagnostics",
        lambda _setup, _run: _diagnostic(True),
    )

    def first_metrics(cell, weight):
        return _run(
            cell.setup,
            weight,
            terminal_train_nll=1000.0 - weight,
            terminal_eta=0.6 + weight / 3000.0,
            cell_identity=cell.identity,
        )

    monkeypatch.setattr(
        runner_module, "run_stage1_candidate", first_metrics
    )
    first = selection.run_stage1_barrier_selection(cells)

    def reversed_metrics(cell, weight):
        return _run(
            cell.setup,
            weight,
            terminal_train_nll=weight,
            terminal_eta=0.95 - weight / 20000.0,
            cell_identity=cell.identity,
        )

    monkeypatch.setattr(
        runner_module, "run_stage1_candidate", reversed_metrics
    )
    second = selection.run_stage1_barrier_selection(cells)
    assert first.selected_weight == second.selected_weight == 0.0


def test_unexpected_runner_and_diagnostic_exceptions_propagate(monkeypatch):
    cells = _barrier_cells()

    def runner_bug(*_args):
        raise RuntimeError("runner bug")

    monkeypatch.setattr(runner_module, "run_stage1_candidate", runner_bug)
    with pytest.raises(RuntimeError, match="runner bug"):
        selection.run_stage1_barrier_selection(cells)

    monkeypatch.setattr(
        runner_module,
        "run_stage1_candidate",
        lambda cell, weight: _run(
            cell.setup, weight, cell_identity=cell.identity
        ),
    )

    def diagnostic_bug(*_args):
        raise RuntimeError("diagnostic bug")

    monkeypatch.setattr(
        selection, "_terminal_grid_diagnostics", diagnostic_bug
    )
    with pytest.raises(RuntimeError, match="diagnostic bug"):
        selection.run_stage1_barrier_selection(cells)
