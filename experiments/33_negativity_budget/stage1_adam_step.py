"""One immutable Adam transition with feasibility-only backtracking."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

import numpy as np


_fixed = import_module("experiments.33_negativity_budget.fixed_beta")
_objective = import_module(
    "experiments.33_negativity_budget.stage1_objective"
)
Stage1Objective = _objective.Stage1Objective
Stage1ObjectiveEvaluation = _objective.Stage1ObjectiveEvaluation
Stage1ObjectiveResult = _objective.Stage1ObjectiveResult


LEARNING_RATE = 0.05
ADAM_BETA1 = 0.9
ADAM_BETA2 = 0.999
ADAM_GRADIENT_WEIGHT1 = 0.1
ADAM_GRADIENT_WEIGHT2 = 0.001
ADAM_EPSILON = 1e-8
BACKTRACK_FACTOR = 0.5
MAX_BACKTRACKS = 16


class NoFeasibleAdamStep(RuntimeError):
    """No scaled candidate had a defined finite strict objective."""

    def __init__(self, attempts: int):
        self.attempts = attempts
        super().__init__(
            f"no feasible Adam candidate was found in {attempts} attempts"
        )


def _finite_vector(value, label: str) -> np.ndarray:
    array = np.asarray(value)
    if (
        array.ndim != 1
        or np.issubdtype(array.dtype, np.bool_)
        or np.iscomplexobj(array)
        or not np.issubdtype(array.dtype, np.number)
    ):
        raise ValueError(f"{label} must be a real one-dimensional vector")
    result = np.asarray(array, dtype=float).copy()
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{label} must contain finite values")
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class Stage1AdamState:
    parameters: np.ndarray
    eta_logit: float
    moment1: np.ndarray
    moment2: np.ndarray
    iteration: int

    def __post_init__(self) -> None:
        parameters = _finite_vector(self.parameters, "parameters")
        moment1 = _finite_vector(self.moment1, "moment1")
        moment2 = _finite_vector(self.moment2, "moment2")
        if np.any(moment2 < 0.0):
            raise ValueError("moment2 must be nonnegative")
        eta_logit = _fixed._as_loss_scalar(self.eta_logit, "eta_logit")
        if (
            isinstance(self.iteration, bool)
            or not isinstance(self.iteration, (int, np.integer))
            or self.iteration < 0
        ):
            raise ValueError("iteration must be a nonnegative integer")
        object.__setattr__(self, "parameters", parameters)
        object.__setattr__(self, "eta_logit", eta_logit)
        object.__setattr__(self, "moment1", moment1)
        object.__setattr__(self, "moment2", moment2)
        object.__setattr__(self, "iteration", int(self.iteration))


@dataclass(frozen=True)
class Stage1AdamStepResult:
    state: Stage1AdamState
    source_evaluation: Stage1ObjectiveEvaluation
    candidate_evaluation: Stage1ObjectiveEvaluation
    backtracks: int
    scale: float
    eta_fd_step: float


def stage1_adam_step(
    objective: Stage1Objective,
    state: Stage1AdamState,
) -> Stage1AdamStepResult:
    """Advance one accepted Adam step, shrinking only for feasibility."""
    if not isinstance(objective, Stage1Objective):
        raise TypeError("objective must be a Stage1Objective")
    if not isinstance(state, Stage1AdamState):
        raise TypeError("state must be a Stage1AdamState")

    parameter_count = objective.setup.parameterization.parameter_count
    gradient_count = parameter_count + 1
    if len(state.parameters) != parameter_count:
        raise ValueError("state parameter length differs from objective")
    if len(state.moment1) != gradient_count:
        raise ValueError("moment1 length differs from state-plus-logit gradient")
    if len(state.moment2) != gradient_count:
        raise ValueError("moment2 length differs from state-plus-logit gradient")

    objective_result = objective.value_and_grad(
        state.parameters, state.eta_logit
    )
    if not isinstance(objective_result, Stage1ObjectiveResult):
        raise TypeError("objective value_and_grad returned an invalid result")
    gradient = np.asarray(objective_result.gradient, dtype=float)
    if gradient.shape != (gradient_count,):
        raise ValueError("objective gradient has invalid length")
    if not np.all(np.isfinite(gradient)):
        raise FloatingPointError("objective gradient must be finite")

    next_iteration = state.iteration + 1
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        trial_moment1 = (
            ADAM_BETA1 * state.moment1 + ADAM_GRADIENT_WEIGHT1 * gradient
        )
        trial_moment2 = (
            ADAM_BETA2 * state.moment2
            + ADAM_GRADIENT_WEIGHT2 * gradient ** 2
        )
        corrected1 = trial_moment1 / (1.0 - ADAM_BETA1 ** next_iteration)
        corrected2 = trial_moment2 / (1.0 - ADAM_BETA2 ** next_iteration)
        update = LEARNING_RATE * corrected1 / (
            np.sqrt(corrected2) + ADAM_EPSILON
        )
    if (
        not np.all(np.isfinite(trial_moment1))
        or not np.all(np.isfinite(trial_moment2))
        or not np.all(np.isfinite(update))
    ):
        raise FloatingPointError("Adam moments and update must be finite")

    for backtracks in range(MAX_BACKTRACKS + 1):
        scale = BACKTRACK_FACTOR ** backtracks
        candidate_parameters = state.parameters - scale * update[:-1]
        candidate_logit = state.eta_logit - scale * update[-1]
        try:
            candidate_evaluation = objective.value(
                candidate_parameters, candidate_logit
            )
        except (ValueError, FloatingPointError, NotImplementedError):
            continue
        if not isinstance(candidate_evaluation, Stage1ObjectiveEvaluation):
            raise TypeError("objective value returned an invalid evaluation")
        next_state = Stage1AdamState(
            parameters=candidate_parameters,
            eta_logit=candidate_logit,
            moment1=trial_moment1,
            moment2=trial_moment2,
            iteration=next_iteration,
        )
        return Stage1AdamStepResult(
            state=next_state,
            source_evaluation=objective_result.evaluation,
            candidate_evaluation=candidate_evaluation,
            backtracks=backtracks,
            scale=float(scale),
            eta_fd_step=objective_result.eta_fd_step,
        )

    raise NoFeasibleAdamStep(MAX_BACKTRACKS + 1)
