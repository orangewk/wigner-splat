"""Global train-only barrier-weight selection for Stage 1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib import import_module

import numpy as np


_setup = import_module(
    "experiments.33_negativity_budget.stage1_setup"
)
_orchestration = import_module(
    "experiments.33_negativity_budget.stage1_orchestration"
)
_runner = import_module(
    "experiments.33_negativity_budget.stage1_runner"
)
Stage1CandidateSetup = _setup.Stage1CandidateSetup
Stage1CandidateCell = _orchestration.Stage1CandidateCell
Stage1CellIdentity = _orchestration.Stage1CellIdentity
Stage1CandidateRun = _runner.Stage1CandidateRun


BARRIER_WEIGHT_CANDIDATES = (0.0,) + tuple(
    10.0**exponent for exponent in range(-1, 13)
)


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
    cell_identity: Stage1CellIdentity
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
        if not isinstance(self.cell_identity, Stage1CellIdentity):
            raise TypeError("cell_identity must be a Stage1CellIdentity")
        if not isinstance(self.grid, GridDiagnostics):
            raise TypeError("grid must be GridDiagnostics")
        barrier_weight = _finite_real_scalar(
            self.barrier_weight, "barrier_weight"
        )
        if barrier_weight not in BARRIER_WEIGHT_CANDIDATES:
            raise ValueError("barrier_weight is outside the declared ladder")
        if self.run.barrier_weight != barrier_weight:
            raise ValueError("run barrier_weight differs from assessment")
        if self.run.cell_identity != self.cell_identity:
            raise ValueError("run cell identity differs from assessment")
        if self.cell_identity.beta <= 0.0:
            raise ValueError("barrier selection assessments require beta > 0")
        object.__setattr__(self, "setup_index", int(self.setup_index))
        object.__setattr__(self, "barrier_weight", barrier_weight)

    @property
    def beta(self) -> float:
        return self.cell_identity.beta

    @property
    def seed(self) -> int:
        return self.cell_identity.init_seed

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


def _attempted_weights(
    assessments: tuple[Stage1BarrierAssessment, ...],
    setup_count: int,
) -> tuple[float, ...]:
    if len(assessments) % setup_count != 0:
        raise ValueError("assessment count is not a whole-weight prefix")
    attempted_count = len(assessments) // setup_count
    if not 2 <= attempted_count <= len(BARRIER_WEIGHT_CANDIDATES):
        raise ValueError("assessment count is not a valid attempted prefix")
    attempted = BARRIER_WEIGHT_CANDIDATES[:attempted_count]
    expected_order = [
        (setup_index, weight)
        for weight in attempted
        for setup_index in range(setup_count)
    ]
    observed_order = [
        (row.setup_index, row.barrier_weight) for row in assessments
    ]
    if observed_order != expected_order:
        raise ValueError("assessment order differs from the attempted prefix")
    for setup_index in range(setup_count):
        identities = {
            row.cell_identity
            for row in assessments
            if row.setup_index == setup_index
        }
        if len(identities) != 1:
            raise ValueError("barrier assessment cell identity differs by weight")
    return attempted


def _admissible_weights(
    assessments: tuple[Stage1BarrierAssessment, ...],
    setup_count: int,
) -> tuple[float, ...]:
    attempted = _attempted_weights(assessments, setup_count)
    admissible = []
    for weight_index, weight in enumerate(attempted):
        start = weight_index * setup_count
        rows = assessments[start : start + setup_count]
        if all(row.admissible for row in rows):
            admissible.append(weight)
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
        expected_identities = _orchestration.barrier_selection_identities()
        if int(self.setup_count) != len(expected_identities):
            raise ValueError("setup_count differs from the declared cell view")
        assessments = tuple(self.assessments)
        if any(
            not isinstance(row, Stage1BarrierAssessment)
            for row in assessments
        ):
            raise TypeError("assessments must contain Stage1BarrierAssessment")
        if tuple(
            row.cell_identity for row in assessments[: int(self.setup_count)]
        ) != expected_identities:
            raise ValueError("assessment identities differ from the cell view")
        attempted = _attempted_weights(assessments, int(self.setup_count))
        admissible = _admissible_weights(assessments, int(self.setup_count))
        expected_selected = _selected_weight(admissible)
        if expected_selected is None:
            if attempted != BARRIER_WEIGHT_CANDIDATES:
                raise ValueError("assessment prefix stopped before a verdict")
        else:
            selected_index = BARRIER_WEIGHT_CANDIDATES.index(expected_selected)
            expected_prefix = BARRIER_WEIGHT_CANDIDATES[: selected_index + 2]
            if attempted != expected_prefix:
                raise ValueError(
                    "assessment prefix did not stop at the first stable pair"
                )
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

    @property
    def attempted_weights(self) -> tuple[float, ...]:
        return _attempted_weights(self.assessments, self.setup_count)


def run_stage1_barrier_selection(cells) -> Stage1BarrierSelection:
    """Run the declared prefix and select one global train-only value."""
    cells = tuple(cells)
    if not cells:
        raise ValueError("barrier selection requires at least one cell")
    if any(not isinstance(cell, Stage1CandidateCell) for cell in cells):
        raise TypeError("cells must contain only Stage1CandidateCell objects")
    if any(cell.identity.beta <= 0.0 for cell in cells):
        raise ValueError("barrier selection accepts only beta > 0 cells")
    if len({cell.identity for cell in cells}) != len(cells):
        raise ValueError("each cell identity may appear only once")
    if len({id(cell.setup) for cell in cells}) != len(cells):
        raise ValueError("each setup object may appear only once")
    if tuple(cell.identity for cell in cells) != (
        _orchestration.barrier_selection_identities()
    ):
        raise ValueError("cells differ from the declared barrier-selection view")

    assessments = []
    selected = None
    previous_weight = None
    previous_admissible = False
    for barrier_weight in BARRIER_WEIGHT_CANDIDATES:
        weight_assessments = []
        for setup_index, cell in enumerate(cells):
            run = _runner.run_stage1_candidate(cell, barrier_weight)
            if not isinstance(run, Stage1CandidateRun):
                raise TypeError("candidate runner returned an invalid result")
            weight_assessments.append(
                Stage1BarrierAssessment(
                    setup_index=setup_index,
                    cell_identity=cell.identity,
                    barrier_weight=barrier_weight,
                    run=run,
                    grid=_terminal_grid_diagnostics(cell.setup, run),
                )
            )
        assessments.extend(weight_assessments)
        current_admissible = all(
            assessment.admissible for assessment in weight_assessments
        )
        if previous_admissible and current_admissible:
            selected = previous_weight
            break
        previous_weight = barrier_weight
        previous_admissible = current_admissible
    assessments = tuple(assessments)
    status = (
        Stage1BarrierSelectionStatus.SELECTED
        if selected is not None
        else Stage1BarrierSelectionStatus.NO_STABLE_ADMISSIBLE_PAIR
    )
    return Stage1BarrierSelection(
        status=status,
        selected_weight=selected,
        assessments=assessments,
        setup_count=len(cells),
    )
