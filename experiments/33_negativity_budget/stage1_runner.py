"""Fixed-schedule runner for one train-only Stage 1 candidate."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib import import_module

import numpy as np


_objective = import_module(
    "experiments.33_negativity_budget.stage1_objective"
)
_fixed = import_module("experiments.33_negativity_budget.fixed_beta")
_orchestration = import_module(
    "experiments.33_negativity_budget.stage1_orchestration"
)
_adam = import_module(
    "experiments.33_negativity_budget.stage1_adam_step"
)
Stage1CandidateCell = _orchestration.Stage1CandidateCell
Stage1CellIdentity = _orchestration.Stage1CellIdentity
Stage1Objective = _objective.Stage1Objective
Stage1ObjectiveEvaluation = _objective.Stage1ObjectiveEvaluation
Stage1AdamState = _adam.Stage1AdamState
Stage1AdamStepResult = _adam.Stage1AdamStepResult


STAGE1_ITERATIONS = 100
ETA0 = 0.8


class Stage1RunStatus(str, Enum):
    COMPLETED = "completed"
    NO_FEASIBLE_STEP = "no_feasible_step"
    ETA_GRADIENT_UNAVAILABLE = "eta_gradient_unavailable"
    NONFINITE_UPDATE = "nonfinite_update"
    UNSUPPORTED_GRADIENT = "unsupported_gradient"


def _nonnegative_int(value, label: str) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, np.integer))
        or value < 0
    ):
        raise ValueError(f"{label} must be a nonnegative integer")
    return int(value)


def _validate_evaluation(
    evaluation: Stage1ObjectiveEvaluation,
    label: str,
) -> None:
    values = (
        evaluation.objective,
        evaluation.train_nll,
        evaluation.barrier,
        evaluation.eta,
    )
    if not all(np.isfinite(value) for value in values):
        raise ValueError(f"{label} must contain finite values")
    if evaluation.barrier < 0.0:
        raise ValueError(f"{label} barrier must be nonnegative")
    if not 0.0 < evaluation.eta < 1.0:
        raise ValueError(f"{label} eta must be strictly inside (0, 1)")


@dataclass(frozen=True)
class Stage1CandidateRun:
    status: Stage1RunStatus
    cell_identity: Stage1CellIdentity
    barrier_weight: float
    state: Stage1AdamState
    initial_evaluation: Stage1ObjectiveEvaluation
    terminal_evaluation: Stage1ObjectiveEvaluation
    backtracked_steps: int
    total_backtracks: int
    max_backtracks_used: int
    min_eta_fd_step: float | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, Stage1RunStatus):
            raise TypeError("status must be a Stage1RunStatus")
        if not isinstance(self.cell_identity, Stage1CellIdentity):
            raise TypeError("cell_identity must be a Stage1CellIdentity")
        barrier_weight = _fixed._as_loss_scalar(
            self.barrier_weight, "barrier_weight"
        )
        if barrier_weight < 0.0:
            raise ValueError("barrier_weight must be nonnegative")
        if not isinstance(self.state, Stage1AdamState):
            raise TypeError("state must be a Stage1AdamState")
        if not isinstance(self.initial_evaluation, Stage1ObjectiveEvaluation):
            raise TypeError(
                "initial_evaluation must be a Stage1ObjectiveEvaluation"
            )
        if not isinstance(self.terminal_evaluation, Stage1ObjectiveEvaluation):
            raise TypeError(
                "terminal_evaluation must be a Stage1ObjectiveEvaluation"
            )
        _validate_evaluation(self.initial_evaluation, "initial_evaluation")
        _validate_evaluation(self.terminal_evaluation, "terminal_evaluation")
        if self.initial_evaluation.eta != ETA0:
            raise ValueError("initial_evaluation eta differs from eta0")
        _, expected_terminal_eta = _objective._eta_from_logit(
            self.state.eta_logit
        )
        if self.terminal_evaluation.eta != expected_terminal_eta:
            raise ValueError("terminal_evaluation eta differs from state")

        backtracked_steps = _nonnegative_int(
            self.backtracked_steps, "backtracked_steps"
        )
        total_backtracks = _nonnegative_int(
            self.total_backtracks, "total_backtracks"
        )
        max_backtracks_used = _nonnegative_int(
            self.max_backtracks_used, "max_backtracks_used"
        )
        if backtracked_steps > self.state.iteration:
            raise ValueError("backtracked_steps exceeds accepted iterations")
        if max_backtracks_used > _adam.MAX_BACKTRACKS:
            raise ValueError("max_backtracks_used exceeds the Adam contract")
        if backtracked_steps == 0:
            if total_backtracks != 0 or max_backtracks_used != 0:
                raise ValueError("zero backtracked steps has inconsistent counters")
        elif (
            total_backtracks < backtracked_steps
            or total_backtracks > backtracked_steps * _adam.MAX_BACKTRACKS
            or max_backtracks_used < 1
            or max_backtracks_used > total_backtracks
        ):
            raise ValueError("positive backtrack counters are inconsistent")

        if self.state.iteration > STAGE1_ITERATIONS:
            raise ValueError("state iteration exceeds the Stage 1 schedule")
        completed = self.state.iteration == STAGE1_ITERATIONS
        if (self.status is Stage1RunStatus.COMPLETED) != completed:
            raise ValueError("completed status differs from accepted iterations")

        min_eta_fd_step = self.min_eta_fd_step
        if min_eta_fd_step is None:
            if self.state.iteration != 0:
                raise ValueError("accepted iterations need an eta FD step")
        else:
            min_eta_fd_step = float(min_eta_fd_step)
            if not np.isfinite(min_eta_fd_step) or min_eta_fd_step <= 0.0:
                raise ValueError("min_eta_fd_step must be finite and positive")

        object.__setattr__(self, "barrier_weight", barrier_weight)
        object.__setattr__(self, "backtracked_steps", backtracked_steps)
        object.__setattr__(self, "total_backtracks", total_backtracks)
        object.__setattr__(self, "max_backtracks_used", max_backtracks_used)
        object.__setattr__(self, "min_eta_fd_step", min_eta_fd_step)


def _run_result(
    status: Stage1RunStatus,
    cell_identity: Stage1CellIdentity,
    barrier_weight: float,
    state: Stage1AdamState,
    initial_evaluation: Stage1ObjectiveEvaluation,
    terminal_evaluation: Stage1ObjectiveEvaluation,
    backtracked_steps: int,
    total_backtracks: int,
    max_backtracks_used: int,
    min_eta_fd_step: float | None,
) -> Stage1CandidateRun:
    return Stage1CandidateRun(
        status=status,
        cell_identity=cell_identity,
        barrier_weight=barrier_weight,
        state=state,
        initial_evaluation=initial_evaluation,
        terminal_evaluation=terminal_evaluation,
        backtracked_steps=backtracked_steps,
        total_backtracks=total_backtracks,
        max_backtracks_used=max_backtracks_used,
        min_eta_fd_step=min_eta_fd_step,
    )


def run_stage1_candidate(
    cell: Stage1CandidateCell,
    barrier_weight: float,
) -> Stage1CandidateRun:
    """Run one cell for 100 accepted steps or a declared numerical stop."""
    if not isinstance(cell, Stage1CandidateCell):
        raise TypeError("cell must be a Stage1CandidateCell")
    setup = cell.setup
    objective = Stage1Objective(setup, barrier_weight)
    gradient_count = setup.parameterization.parameter_count + 1
    eta_logit = float(np.log(ETA0 / (1.0 - ETA0)))
    state = Stage1AdamState(
        parameters=setup.initial_parameters,
        eta_logit=eta_logit,
        moment1=np.zeros(gradient_count),
        moment2=np.zeros(gradient_count),
        iteration=0,
    )
    initial_evaluation = objective.value(state.parameters, state.eta_logit)
    terminal_evaluation = initial_evaluation
    backtracked_steps = 0
    total_backtracks = 0
    max_backtracks_used = 0
    min_eta_fd_step = None

    for _ in range(STAGE1_ITERATIONS):
        previous_iteration = state.iteration
        try:
            step = _adam.stage1_adam_step(objective, state)
        except _adam.NoFeasibleAdamStep:
            status = Stage1RunStatus.NO_FEASIBLE_STEP
            break
        except _objective.EtaGradientUnavailable:
            status = Stage1RunStatus.ETA_GRADIENT_UNAVAILABLE
            break
        except FloatingPointError:
            status = Stage1RunStatus.NONFINITE_UPDATE
            break
        except NotImplementedError:
            status = Stage1RunStatus.UNSUPPORTED_GRADIENT
            break

        if not isinstance(step, Stage1AdamStepResult):
            raise TypeError("stage1_adam_step returned an invalid result")
        if step.state.iteration != previous_iteration + 1:
            raise RuntimeError("Adam step did not advance exactly one iteration")
        state = step.state
        terminal_evaluation = step.candidate_evaluation
        if step.backtracks > 0:
            backtracked_steps += 1
            total_backtracks += step.backtracks
            max_backtracks_used = max(max_backtracks_used, step.backtracks)
        min_eta_fd_step = (
            step.eta_fd_step
            if min_eta_fd_step is None
            else min(min_eta_fd_step, step.eta_fd_step)
        )
    else:
        status = Stage1RunStatus.COMPLETED

    return _run_result(
        status=status,
        cell_identity=cell.identity,
        barrier_weight=objective.barrier_weight,
        state=state,
        initial_evaluation=initial_evaluation,
        terminal_evaluation=terminal_evaluation,
        backtracked_steps=backtracked_steps,
        total_backtracks=total_backtracks,
        max_backtracks_used=max_backtracks_used,
        min_eta_fd_step=min_eta_fd_step,
    )
