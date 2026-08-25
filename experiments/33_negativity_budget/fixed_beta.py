"""Packet-1 forward interface declared in ``protocol.md`` section 2-3."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from wigner_splat.bbdagS import MixedSqueezedKetState, lossy_pdf_mixed


class NonPositiveDensityError(ValueError):
    """A strict likelihood encountered a nonfinite or nonpositive density."""

    def __init__(self, group_index: int, invalid_count: int, sample_count: int):
        self.group_index = group_index
        self.invalid_count = invalid_count
        self.sample_count = sample_count
        super().__init__(
            f"density group {group_index} has {invalid_count}/{sample_count} "
            "nonfinite or nonpositive samples"
        )


def _validate_component(state, label: str) -> None:
    if not isinstance(state, MixedSqueezedKetState):
        raise TypeError(f"{label} must be a MixedSqueezedKetState")
    if state.z.ndim != 2 or state.alpha.ndim != 3 or state.xi.ndim != 3:
        raise ValueError(f"{label} arrays have invalid ranks")
    if state.alpha.shape != state.xi.shape:
        raise ValueError(f"{label} alpha/xi shapes differ")
    if state.z.shape != state.alpha.shape[:2]:
        raise ValueError(f"{label} z and ket shapes differ")
    if min(state.R, state.K, state.M) < 1:
        raise ValueError(f"{label} must contain at least one mode and ket")
    norm = state.norm_sq()
    if not np.isfinite(norm) or norm <= 0.0:
        raise ValueError(f"{label} norm must be finite and positive")


@dataclass(frozen=True)
class FixedBetaDifferenceModel:
    """Signed model implementing the fixed-beta protocol interface."""

    positive: MixedSqueezedKetState
    negative: MixedSqueezedKetState | None
    beta: float

    def __post_init__(self) -> None:
        if isinstance(self.beta, bool) or not isinstance(
            self.beta, (int, float, np.integer, np.floating)
        ):
            raise TypeError("beta must be a real scalar")
        beta = float(self.beta)
        if not np.isfinite(beta) or not 0.0 <= beta < 0.5:
            raise ValueError("beta must be finite and in [0, 0.5)")
        object.__setattr__(self, "beta", beta)
        _validate_component(self.positive, "positive")
        if beta == 0.0 and self.negative is not None:
            raise ValueError("negative component must be absent when beta == 0")
        if beta > 0.0 and self.negative is None:
            raise ValueError("negative component is required when beta > 0")
        if self.negative is not None:
            _validate_component(self.negative, "negative")
            if self.negative.M != self.positive.M:
                raise ValueError("positive and negative mode counts differ")

    @property
    def pre_normalization_masses(self) -> tuple[float, float]:
        return 1.0 - self.beta, self.beta

    @property
    def density_coefficients(self) -> tuple[float, float]:
        gap = 1.0 - 2.0 * self.beta
        return (1.0 - self.beta) / gap, -self.beta / gap

    def pdf(self, X, theta, eta, extra_noise_var=0.0) -> np.ndarray:
        X = np.asarray(X)
        theta = np.asarray(theta)
        if X.ndim != 2 or X.shape[1] != self.positive.M:
            raise ValueError(
                f"X must have shape (samples, {self.positive.M})"
            )
        if theta.ndim != 1 or len(theta) != self.positive.M:
            raise ValueError(f"theta must have shape ({self.positive.M},)")
        positive = np.asarray(
            lossy_pdf_mixed(
                self.positive, X, theta, eta, extra_noise_var
            ),
            dtype=float,
        )
        if self.beta == 0.0:
            return positive
        negative = np.asarray(
            lossy_pdf_mixed(
                self.negative, X, theta, eta, extra_noise_var
            ),
            dtype=float,
        )
        if negative.shape != positive.shape:
            raise ValueError("positive and negative pdf shapes differ")
        c_positive, c_negative = self.density_coefficients
        return c_positive * positive + c_negative * negative


def per_sample_nll(
    model: FixedBetaDifferenceModel,
    data,
    eta: float,
    extra_noise_var: float = 0.0,
) -> np.ndarray:
    """Strict per-sample NLL; no clipping or flooring is permitted."""
    rows = []
    for group_index, (theta, X) in enumerate(data):
        X = np.asarray(X)
        if X.ndim > 0 and len(X) == 0:
            raise ValueError(
                f"density group {group_index} must contain at least one sample"
            )
        density = np.asarray(
            model.pdf(X, theta, eta, extra_noise_var), dtype=float
        )
        sample_count = len(X)
        if density.ndim != 1 or len(density) != sample_count:
            raise ValueError(f"density group {group_index} has invalid shape")
        invalid = ~np.isfinite(density) | (density <= 0.0)
        if np.any(invalid):
            raise NonPositiveDensityError(
                group_index, int(np.count_nonzero(invalid)), sample_count
            )
        rows.append(-np.log(density))
    if not rows:
        raise ValueError("data must contain at least one measurement group")
    return np.concatenate(rows)


def mean_nll(
    model: FixedBetaDifferenceModel,
    data,
    eta: float,
    extra_noise_var: float = 0.0,
) -> float:
    return float(np.mean(per_sample_nll(model, data, eta, extra_noise_var)))
