"""Global train-only barrier-weight selection for Stage 1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib import import_module

import numpy as np


_setup = import_module(
    "experiments.33_negativity_budget.stage1_setup"
)
_runner = import_module(
    "experiments.33_negativity_budget.stage1_runner"
)
Stage1CandidateSetup = _setup.Stage1CandidateSetup
Stage1CandidateRun = _runner.Stage1CandidateRun


BARRIER_WEIGHT_CANDIDATES = (0.0, 0.1, 1.0, 10.0, 100.0, 1000.0)


class Stage1BarrierSelectionStatus(str, Enum):
    SELECTED = "selected"
    NO_STABLE_ADMISSIBLE_PAIR = "no_stable_admissible_pair"


def _finite_real_scalar(value, label: str) -> float:
    array = np.asarray(value)
    if (
        array.ndim != 0
        or np.issubdtype(array.dtype, np.bool_)
        or np.iscomplexobj(array)
        or not np.issubdtype(array.dtype, np.number)
    ):
        raise ValueError(f"{label} must be a real numeric scalar")
    result = float(array.item())
    if not np.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


@dataclass(frozen=True)
class GridDiagnostics:
    point_count: int
    nonpositive_count: int
    nonfinite_count: int
    minimum_finite_density: float | None

    def __post_init__(self) -> None:
        counts = (
            self.point_count,
            self.nonpositive_count,
            self.nonfinite_count,
        )
        if any(
            isinstance(value, bool)
            or not isinstance(value, (int, np.integer))
            or value < 0
            for value in counts
        ):
            raise ValueError("grid diagnostic counts must be nonnegative integers")
        point_count, nonpositive_count, nonfinite_count = map(int, counts)
        if point_count < 1:
            raise ValueError("grid diagnostics need at least one point")
        if nonpositive_count + nonfinite_count > point_count:
            raise ValueError("invalid grid counts exceed the point count")

        minimum = self.minimum_finite_density
        finite_count = point_count - nonfinite_count
        if finite_count == 0:
            if minimum is not None or nonpositive_count != 0:
                raise ValueError("an all-nonfinite grid has no finite minimum")
        else:
            if minimum is None:
                raise ValueError("a partly finite grid needs a finite minimum")
            minimum = _finite_real_scalar(
                minimum, "minimum_finite_density"
            )
            if (nonpositive_count == 0) != (minimum > 0.0):
                raise ValueError("grid minimum and nonpositive count disagree")

        object.__setattr__(self, "point_count", point_count)
        object.__setattr__(self, "nonpositive_count", nonpositive_count)
        object.__setattr__(self, "nonfinite_count", nonfinite_count)
        object.__setattr__(self, "minimum_finite_density", minimum)

    @property
    def strictly_positive(self) -> bool:
        return self.nonpositive_count == 0 and self.nonfinite_count == 0


@dataclass(frozen=True)
class Stage1BarrierAssessment:
    setup_index: int
    beta: float
    seed: int
    barrier_weight: float
    run: Stage1CandidateRun
    grid: GridDiagnostics

    def __post_init__(self) -> None:
        if (
            isinstance(self.setup_index, bool)
            or not isinstance(self.setup_index, (int, np.integer))
            or self.setup_index < 0
        ):
            raise ValueError("setup_index must be a nonnegative integer")
        if not isinstance(self.run, Stage1CandidateRun):
            raise TypeError("run must be a Stage1CandidateRun")
        if not isinstance(self.grid, GridDiagnostics):
            raise TypeError("grid must be GridDiagnostics")
        barrier_weight = _finite_real_scalar(
            self.barrier_weight, "barrier_weight"
        )
        if barrier_weight not in BARRIER_WEIGHT_CANDIDATES:
            raise ValueError("barrier_weight is outside the declared ladder")
        beta = _finite_real_scalar(self.beta, "beta")
        if beta <= 0.0:
            raise ValueError("barrier selection assessments require beta > 0")
        if (
            isinstance(self.seed, bool)
            or not isinstance(self.seed, (int, np.integer))
            or self.seed < 0
        ):
            raise ValueError("seed must be a nonnegative integer")
        object.__setattr__(self, "setup_index", int(self.setup_index))
        object.__setattr__(self, "beta", beta)
        object.__setattr__(self, "seed", int(self.seed))
        object.__setattr__(self, "barrier_weight", barrier_weight)

    @property
    def admissible(self) -> bool:
        return (
            self.run.status is _runner.Stage1RunStatus.COMPLETED
            and self.grid.strictly_positive
        )

    @property
    def terminal_train_nll(self) -> float:
        return self.run.terminal_evaluation.train_nll

    @property
    def terminal_eta(self) -> float:
        return self.run.terminal_evaluation.eta


def _summarize_grid_densities(density_groups) -> GridDiagnostics:
    point_count = 0
    nonpositive_count = 0
    nonfinite_count = 0
    minima = []
    for density in density_groups:
        raw = np.asarray(density)
        if raw.ndim != 1 or len(raw) < 1:
            raise ValueError("each grid density must be a nonempty vector")
        if (
            np.issubdtype(raw.dtype, np.bool_)
            or np.iscomplexobj(raw)
            or not np.issubdtype(raw.dtype, np.number)
        ):
            raise ValueError("grid density must contain real numeric values")
        values = np.asarray(raw, dtype=float)
        finite = np.isfinite(values)
        point_count += len(values)
        nonfinite_count += int(np.count_nonzero(~finite))
        finite_values = values[finite]
        if len(finite_values):
            nonpositive_count += int(np.count_nonzero(finite_values <= 0.0))
            minima.append(float(np.min(finite_values)))
    if point_count == 0:
        raise ValueError("grid diagnostics require at least one group")
    return GridDiagnostics(
        point_count=point_count,
        nonpositive_count=nonpositive_count,
        nonfinite_count=nonfinite_count,
        minimum_finite_density=(None if not minima else min(minima)),
    )


def _terminal_grid_diagnostics(
    setup: Stage1CandidateSetup,
    run: Stage1CandidateRun,
) -> GridDiagnostics:
    model = setup.parameterization.unpack(run.state.parameters)
    eta = run.terminal_evaluation.eta

    def densities():
        for theta, X in setup.grid_groups:
            density = np.asarray(model.pdf(X, theta, eta))
            if density.shape != (len(X),):
                raise ValueError("terminal grid density has an invalid shape")
            yield density

    return _summarize_grid_densities(densities())


def _admissible_weights(
    assessments: tuple[Stage1BarrierAssessment, ...],
    setup_count: int,
) -> tuple[float, ...]:
    expected_indices = set(range(setup_count))
    admissible = []
    for weight in BARRIER_WEIGHT_CANDIDATES:
        rows = [row for row in assessments if row.barrier_weight == weight]
        if len(rows) != setup_count:
            raise RuntimeError("barrier assessment matrix is incomplete")
        if {row.setup_index for row in rows} != expected_indices:
            raise RuntimeError("barrier assessment setup coverage differs by weight")
        if all(row.admissible for row in rows):
            admissible.append(weight)
    for setup_index in expected_indices:
        identity = {
            (row.beta, row.seed)
            for row in assessments
            if row.setup_index == setup_index
        }
        if len(identity) != 1:
            raise RuntimeError("barrier assessment setup identity differs by weight")
    return tuple(admissible)


def _selected_weight(admissible: tuple[float, ...]) -> float | None:
    return next(
        (
            lower
            for lower, upper in zip(
                BARRIER_WEIGHT_CANDIDATES,
                BARRIER_WEIGHT_CANDIDATES[1:],
            )
            if lower in admissible and upper in admissible
        ),
        None,
    )


@dataclass(frozen=True)
class Stage1BarrierSelection:
    status: Stage1BarrierSelectionStatus
    selected_weight: float | None
    assessments: tuple[Stage1BarrierAssessment, ...]
    setup_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.status, Stage1BarrierSelectionStatus):
            raise TypeError("status must be a Stage1BarrierSelectionStatus")
        if (
            isinstance(self.setup_count, bool)
            or not isinstance(self.setup_count, (int, np.integer))
            or self.setup_count < 1
        ):
            raise ValueError("setup_count must be a positive integer")
        assessments = tuple(self.assessments)
        if any(
            not isinstance(row, Stage1BarrierAssessment)
            for row in assessments
        ):
            raise TypeError("assessments must contain Stage1BarrierAssessment")
        expected_count = int(self.setup_count) * len(BARRIER_WEIGHT_CANDIDATES)
        if len(assessments) != expected_count:
            raise ValueError("assessment count differs from the declared matrix")
        expected_order = [
            (setup_index, weight)
            for setup_index in range(int(self.setup_count))
            for weight in BARRIER_WEIGHT_CANDIDATES
        ]
        observed_order = [
            (row.setup_index, row.barrier_weight) for row in assessments
        ]
        if observed_order != expected_order:
            raise ValueError("assessment order differs from the declared matrix")
        admissible = _admissible_weights(assessments, int(self.setup_count))
        expected_selected = _selected_weight(admissible)
        expected_status = (
            Stage1BarrierSelectionStatus.SELECTED
            if expected_selected is not None
            else Stage1BarrierSelectionStatus.NO_STABLE_ADMISSIBLE_PAIR
        )
        selected_weight = self.selected_weight
        if selected_weight is not None:
            selected_weight = _finite_real_scalar(
                selected_weight, "selected_weight"
            )
            if selected_weight not in BARRIER_WEIGHT_CANDIDATES:
                raise ValueError("selected_weight is outside the declared ladder")
        if (
            selected_weight != expected_selected
            or self.status is not expected_status
        ):
            raise ValueError("selection verdict differs from the assessment data")
        object.__setattr__(self, "assessments", assessments)
        object.__setattr__(self, "setup_count", int(self.setup_count))
        object.__setattr__(self, "selected_weight", selected_weight)

    @property
    def admissible_weights(self) -> tuple[float, ...]:
        return _admissible_weights(self.assessments, self.setup_count)


def run_stage1_barrier_selection(setups) -> Stage1BarrierSelection:
    """Run every declared weight and select one global train-only value."""
    setups = tuple(setups)
    if not setups:
        raise ValueError("barrier selection requires at least one setup")
    if any(not isinstance(setup, Stage1CandidateSetup) for setup in setups):
        raise TypeError("setups must contain only Stage1CandidateSetup objects")
    if any(setup.beta <= 0.0 for setup in setups):
        raise ValueError("barrier selection accepts only beta > 0 setups")
    if len({id(setup) for setup in setups}) != len(setups):
        raise ValueError("each setup object may appear only once")

    assessments = []
    for setup_index, setup in enumerate(setups):
        for barrier_weight in BARRIER_WEIGHT_CANDIDATES:
            run = _runner.run_stage1_candidate(setup, barrier_weight)
            if not isinstance(run, Stage1CandidateRun):
                raise TypeError("candidate runner returned an invalid result")
            assessments.append(
                Stage1BarrierAssessment(
                    setup_index=setup_index,
                    beta=setup.beta,
                    seed=setup.seed,
                    barrier_weight=barrier_weight,
                    run=run,
                    grid=_terminal_grid_diagnostics(setup, run),
                )
            )
    assessments = tuple(assessments)
    admissible = _admissible_weights(assessments, len(setups))
    selected = _selected_weight(admissible)
    status = (
        Stage1BarrierSelectionStatus.SELECTED
        if selected is not None
        else Stage1BarrierSelectionStatus.NO_STABLE_ADMISSIBLE_PAIR
    )
    return Stage1BarrierSelection(
        status=status,
        selected_weight=selected,
        assessments=assessments,
        setup_count=len(setups),
    )
