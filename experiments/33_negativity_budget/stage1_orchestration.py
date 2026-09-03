"""Canonical Stage 1 cell registry and train-only construction."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

import numpy as np


_fixed = import_module("experiments.33_negativity_budget.fixed_beta")
_setup = import_module("experiments.33_negativity_budget.stage1_setup")
Stage1CandidateSetup = _setup.Stage1CandidateSetup


DATASET_ID = "dryad:10.5061/dryad.t76hdr86j:gkp-six-phase-npy"
MEASUREMENT_DEGREES = (0, 30, 60, -30, -60, -90)
RESHUFFLE_SEEDS = (0, 1)
STAGE1_BETAS = (0.0, 0.02, 0.05, 0.1, 0.2, 0.4)
INIT_SEEDS = (0, 1, 2)
TRAIN_FRACTION = 0.8
BIT_GENERATOR = np.random.PCG64


def _declared_integer(value, allowed: tuple[int, ...], label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{label} must be a declared integer")
    result = int(value)
    if result not in allowed:
        raise ValueError(f"{label} is outside the declared registry")
    return result


@dataclass(frozen=True)
class Stage1CellIdentity:
    dataset_id: str
    reshuffle_seed: int
    beta: float
    init_seed: int

    def __post_init__(self) -> None:
        if not isinstance(self.dataset_id, str) or self.dataset_id != DATASET_ID:
            raise ValueError("dataset_id differs from the declared source")
        reshuffle_seed = _declared_integer(
            self.reshuffle_seed, RESHUFFLE_SEEDS, "reshuffle_seed"
        )
        beta = _fixed._as_loss_scalar(self.beta, "beta")
        if beta not in STAGE1_BETAS:
            raise ValueError("beta is outside the declared Stage 1 registry")
        init_seed = _declared_integer(
            self.init_seed, INIT_SEEDS, "init_seed"
        )
        object.__setattr__(self, "reshuffle_seed", reshuffle_seed)
        object.__setattr__(self, "beta", beta)
        object.__setattr__(self, "init_seed", init_seed)


@dataclass(frozen=True)
class Stage1CandidateCell:
    identity: Stage1CellIdentity
    setup: Stage1CandidateSetup

    def __post_init__(self) -> None:
        if not isinstance(self.identity, Stage1CellIdentity):
            raise TypeError("identity must be a Stage1CellIdentity")
        if not isinstance(self.setup, Stage1CandidateSetup):
            raise TypeError("setup must be a Stage1CandidateSetup")
        if self.setup.beta != self.identity.beta:
            raise ValueError("cell beta differs from setup")
        if self.setup.seed != self.identity.init_seed:
            raise ValueError("cell init seed differs from setup")


def stage1_cell_identities() -> tuple[Stage1CellIdentity, ...]:
    return tuple(
        Stage1CellIdentity(DATASET_ID, reshuffle_seed, beta, init_seed)
        for reshuffle_seed in RESHUFFLE_SEEDS
        for beta in STAGE1_BETAS
        for init_seed in INIT_SEEDS
    )


def barrier_selection_identities() -> tuple[Stage1CellIdentity, ...]:
    return tuple(
        identity
        for identity in stage1_cell_identities()
        if identity.beta > 0.0
    )


def _source_groups(data) -> tuple[tuple[float, np.ndarray], ...]:
    groups = tuple(data)
    if len(groups) != len(MEASUREMENT_DEGREES):
        raise ValueError("source must contain the declared six phases")
    normalized = []
    for group_index, ((theta, samples), degrees) in enumerate(
        zip(groups, MEASUREMENT_DEGREES, strict=True)
    ):
        theta_array = np.asarray(theta)
        sample_array = np.asarray(samples)
        if (
            theta_array.ndim != 0
            or np.issubdtype(theta_array.dtype, np.bool_)
            or np.iscomplexobj(theta_array)
            or not np.issubdtype(theta_array.dtype, np.number)
        ):
            raise ValueError(f"source theta group {group_index} is invalid")
        theta_value = float(theta_array.item())
        expected_theta = float(np.deg2rad(degrees))
        if not np.isfinite(theta_value) or theta_value != expected_theta:
            raise ValueError("source phase order differs from the declaration")
        if (
            sample_array.ndim != 1
            or len(sample_array) < 3
            or np.issubdtype(sample_array.dtype, np.bool_)
            or np.iscomplexobj(sample_array)
            or not np.issubdtype(sample_array.dtype, np.number)
        ):
            raise ValueError(f"source sample group {group_index} is invalid")
        values = np.array(sample_array, dtype=float, copy=True)
        if not np.all(np.isfinite(values)):
            raise ValueError(f"source sample group {group_index} is nonfinite")
        values.setflags(write=False)
        normalized.append((theta_value, values))
    return tuple(normalized)


def _train_groups(
    source_groups: tuple[tuple[float, np.ndarray], ...],
    reshuffle_seed: int,
) -> tuple[tuple[np.ndarray, np.ndarray], ...]:
    generator = np.random.Generator(BIT_GENERATOR(reshuffle_seed))
    train = []
    for theta, samples in source_groups:
        indices = generator.permutation(len(samples))
        train_count = int(TRAIN_FRACTION * len(samples))
        train.append(
            (
                np.array([theta], dtype=float),
                np.array(samples[indices[:train_count], None], copy=True),
            )
        )
    return tuple(train)


def prepare_stage1_cells(data) -> tuple[Stage1CandidateCell, ...]:
    """Build the declared 36-cell registry without returning test samples."""
    source_groups = _source_groups(data)
    train_by_reshuffle = {
        seed: _train_groups(source_groups, seed) for seed in RESHUFFLE_SEEDS
    }
    return tuple(
        Stage1CandidateCell(
            identity=identity,
            setup=_setup.prepare_stage1_candidate(
                train_by_reshuffle[identity.reshuffle_seed],
                beta=identity.beta,
                seed=identity.init_seed,
            ),
        )
        for identity in stage1_cell_identities()
    )


def barrier_selection_cells(
    cells,
) -> tuple[Stage1CandidateCell, ...]:
    """Validate a canonical registry and return its beta-positive view."""
    cells = tuple(cells)
    if any(not isinstance(cell, Stage1CandidateCell) for cell in cells):
        raise TypeError("cells must contain only Stage1CandidateCell objects")
    if tuple(cell.identity for cell in cells) != stage1_cell_identities():
        raise ValueError("cells differ from the declared Stage 1 registry")
    if len({id(cell.setup) for cell in cells}) != len(cells):
        raise ValueError("each Stage 1 cell must own a distinct setup")
    selected = tuple(cell for cell in cells if cell.identity.beta > 0.0)
    if tuple(cell.identity for cell in selected) != barrier_selection_identities():
        raise RuntimeError("barrier-selection cell derivation is inconsistent")
    return selected
