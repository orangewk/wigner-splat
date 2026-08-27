"""Train-only grid and feasible initialization for Stage 1 candidate fits."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

import numpy as np

from wigner_splat.bbdagS import MixedSqueezedKetState


_fixed = import_module("experiments.33_negativity_budget.fixed_beta")
_packet2 = import_module("experiments.33_negativity_budget.packet2")
FixedBetaDifferenceModel = _fixed.FixedBetaDifferenceModel
FixedBetaParameterization = _packet2.FixedBetaParameterization


POSITIVE_SHAPE = (4, 4, 1)
NEGATIVE_SHAPE = (1, 2, 1)
GRID_POINTS = 1025
GRID_SIGMA_EXTENT = 6.0
NEGATIVE_SEED_OFFSET = 1_000_003


@dataclass(frozen=True)
class GridRecord:
    group_index: int
    theta: float
    train_sample_count: int
    train_min: float
    train_max: float
    train_mean: float
    train_std: float
    lower: float
    upper: float
    points: int


@dataclass(frozen=True)
class Stage1CandidateSetup:
    beta: float
    seed: int
    train_groups: tuple[tuple[np.ndarray, np.ndarray], ...]
    grid_groups: tuple[tuple[np.ndarray, np.ndarray], ...]
    grid_records: tuple[GridRecord, ...]
    parameterization: FixedBetaParameterization
    initial_parameters: np.ndarray


def _is_finite_real(value) -> bool:
    array = np.asarray(value)
    return bool(
        array.ndim == 0
        and not np.issubdtype(array.dtype, np.bool_)
        and not np.iscomplexobj(array)
        and np.issubdtype(array.dtype, np.number)
        and np.isfinite(array.item())
    )


def _validate_seed(seed) -> int:
    if (
        isinstance(seed, bool)
        or not isinstance(seed, (int, np.integer))
        or seed < 0
    ):
        raise ValueError("seed must be a nonnegative integer")
    return int(seed)


def prepare_train_groups(data) -> tuple[tuple[np.ndarray, np.ndarray], ...]:
    """Validate and copy one-mode train groups without accepting test data."""
    groups = []
    seen_theta = set()
    for group_index, (theta, X) in enumerate(data):
        theta_array = np.asarray(theta)
        X_array = np.asarray(X)
        if theta_array.shape != (1,):
            raise ValueError(f"train theta group {group_index} must have shape (1,)")
        if X_array.ndim != 2 or X_array.shape[1] != 1 or len(X_array) < 2:
            raise ValueError(
                f"train X group {group_index} must have shape (N >= 2, 1)"
            )
        if (
            np.iscomplexobj(theta_array)
            or np.iscomplexobj(X_array)
            or not np.issubdtype(theta_array.dtype, np.number)
            or not np.issubdtype(X_array.dtype, np.number)
        ):
            raise ValueError("train groups must contain real numbers")
        theta_float = np.asarray(theta_array, float)
        X_float = np.asarray(X_array, float)
        if not np.all(np.isfinite(theta_float)) or not np.all(np.isfinite(X_float)):
            raise ValueError("train groups must contain finite numbers")
        theta_key = float(theta_float[0])
        if theta_key in seen_theta:
            raise ValueError("train measurement angles must be unique")
        seen_theta.add(theta_key)
        with np.errstate(over="ignore", invalid="ignore"):
            train_std = float(np.std(X_float[:, 0]))
        if not np.isfinite(train_std):
            raise ValueError("train statistics must be finite in float64")
        if train_std <= 0.0:
            raise ValueError("each train group must have positive variance")
        theta_copy = theta_float.copy()
        X_copy = X_float.copy()
        theta_copy.setflags(write=False)
        X_copy.setflags(write=False)
        groups.append((theta_copy, X_copy))
    if not groups:
        raise ValueError("train data must contain at least one group")
    return tuple(groups)


def build_train_grids(
    train_groups,
) -> tuple[
    tuple[tuple[np.ndarray, np.ndarray], ...], tuple[GridRecord, ...]
]:
    groups = prepare_train_groups(train_groups)
    grids = []
    records = []
    for group_index, (theta, X) in enumerate(groups):
        values = X[:, 0]
        with np.errstate(over="ignore", invalid="ignore"):
            mean = float(np.mean(values))
            std = float(np.std(values))
        train_min = float(np.min(values))
        train_max = float(np.max(values))
        if not np.isfinite(mean) or not np.isfinite(std):
            raise ValueError("train statistics must be finite in float64")
        with np.errstate(over="ignore", invalid="ignore"):
            lower = min(train_min, mean - GRID_SIGMA_EXTENT * std)
            upper = max(train_max, mean + GRID_SIGMA_EXTENT * std)
        if not np.isfinite(lower) or not np.isfinite(upper):
            raise ValueError("train-derived grid bounds must be finite")
        with np.errstate(over="ignore", invalid="ignore"):
            grid = np.linspace(lower, upper, GRID_POINTS).reshape(-1, 1).copy()
        if not np.all(np.isfinite(grid)):
            raise ValueError("train-derived grid must be finite")
        grid.setflags(write=False)
        theta_copy = theta.copy()
        theta_copy.setflags(write=False)
        grids.append((theta_copy, grid))
        records.append(
            GridRecord(
                group_index=group_index,
                theta=float(theta[0]),
                train_sample_count=len(values),
                train_min=train_min,
                train_max=train_max,
                train_mean=mean,
                train_std=std,
                lower=float(lower),
                upper=float(upper),
                points=GRID_POINTS,
            )
        )
    return tuple(grids), tuple(records)


def _normalized(state: MixedSqueezedKetState) -> MixedSqueezedKetState:
    norm = state.norm_sq()
    if not np.isfinite(norm) or norm <= 0.0:
        raise ValueError("initialization norm must be finite and positive")
    return MixedSqueezedKetState(
        z=state.z / np.sqrt(norm),
        alpha=state.alpha.copy(),
        xi=state.xi.copy(),
    )


def initialize_candidate_model(
    beta: float,
    seed: int,
) -> FixedBetaDifferenceModel:
    """Create the exact beta-zero or shared-column feasible initialization."""
    if not _is_finite_real(beta) or not 0.0 <= float(beta) <= _fixed.MAX_BETA:
        raise ValueError("beta is outside the supported range")
    beta = float(beta)
    seed = _validate_seed(seed)
    R, K, M = POSITIVE_SHAPE
    if beta == 0.0:
        positive = MixedSqueezedKetState.random_init(R, K, M, rng=seed)
        return FixedBetaDifferenceModel(positive, None, beta)

    _, negative_K, _ = NEGATIVE_SHAPE
    core = _normalized(
        MixedSqueezedKetState.random_init(R - 1, K, M, rng=seed)
    )
    negative = _normalized(
        MixedSqueezedKetState.random_init(
            *NEGATIVE_SHAPE, rng=seed + NEGATIVE_SEED_OFFSET
        )
    )
    gap = 1.0 - 2.0 * beta
    c_positive = (1.0 - beta) / gap
    c_negative = beta / gap
    shared_mass = 1.0 / R

    z = np.zeros((R, K), complex)
    alpha = np.zeros((R, K, M), complex)
    xi = np.zeros((R, K, M), complex)
    z[:R - 1] = np.sqrt((1.0 - shared_mass) / c_positive) * core.z
    alpha[:R - 1] = core.alpha
    xi[:R - 1] = core.xi
    z[-1, :negative_K] = (
        np.sqrt((shared_mass + c_negative) / c_positive) * negative.z[0]
    )
    alpha[-1, :negative_K] = negative.alpha[0]
    xi[-1, :negative_K] = negative.xi[0]
    positive = MixedSqueezedKetState(z=z, alpha=alpha, xi=xi)
    return FixedBetaDifferenceModel(positive, negative, beta)


def prepare_stage1_candidate(
    train_groups,
    beta: float,
    seed: int,
) -> Stage1CandidateSetup:
    """Build the single setup object consumed by the next objective packet."""
    prepared = prepare_train_groups(train_groups)
    grids, records = build_train_grids(prepared)
    model = initialize_candidate_model(beta, seed)
    parameterization = FixedBetaParameterization.from_model(model)
    initial_parameters = parameterization.pack(model)
    initial_parameters.setflags(write=False)
    return Stage1CandidateSetup(
        beta=float(beta),
        seed=_validate_seed(seed),
        train_groups=prepared,
        grid_groups=grids,
        grid_records=records,
        parameterization=parameterization,
        initial_parameters=initial_parameters,
    )
