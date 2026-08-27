"""Packet-2 analytic density Jacobian and explicit-grid negativity barrier."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

import numpy as np

from wigner_splat.bbdagS import (
    _pack_mixed,
    _unpack_mixed,
    lossy_pdf_and_jac_mixed,
)


_fixed = import_module("experiments.33_negativity_budget.fixed_beta")
FixedBetaDifferenceModel = _fixed.FixedBetaDifferenceModel
MAX_BETA = _fixed.MAX_BETA
ObservationInputError = _fixed.ObservationInputError


ComponentShape = tuple[int, int, int]


def _validate_shape(shape: ComponentShape, label: str) -> ComponentShape:
    if not isinstance(shape, tuple) or len(shape) != 3:
        raise TypeError(f"{label} shape must be an (R, K, M) tuple")
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, np.integer))
        or value < 1
        for value in shape
    ):
        raise ValueError(f"{label} shape entries must be positive integers")
    return tuple(int(value) for value in shape)


def _parameter_count(shape: ComponentShape) -> int:
    R, K, M = shape
    return 2 * R * K + 4 * R * K * M


def _state_shape(state) -> ComponentShape:
    return state.R, state.K, state.M


@dataclass(frozen=True)
class FixedBetaParameterization:
    """Shape-only adapter between packed parameters and packet-1 models.

    The adapter owns no mutable state arrays.  Each density/Jacobian evaluation
    unpacks fresh component objects from the supplied real vector.
    """

    beta: float
    positive_shape: ComponentShape
    negative_shape: ComponentShape | None

    def __post_init__(self) -> None:
        if isinstance(self.beta, bool) or not isinstance(
            self.beta, (int, float, np.integer, np.floating)
        ):
            raise TypeError("beta must be a real scalar")
        beta = float(self.beta)
        if not np.isfinite(beta) or not 0.0 <= beta <= MAX_BETA:
            raise ValueError(f"beta must be finite and in [0, {MAX_BETA}]")
        positive_shape = _validate_shape(self.positive_shape, "positive")
        negative_shape = self.negative_shape
        if beta == 0.0 and negative_shape is not None:
            raise ValueError("negative shape must be absent when beta == 0")
        if beta > 0.0 and negative_shape is None:
            raise ValueError("negative shape is required when beta > 0")
        if negative_shape is not None:
            negative_shape = _validate_shape(negative_shape, "negative")
            if negative_shape[2] != positive_shape[2]:
                raise ValueError("positive and negative mode counts differ")
        object.__setattr__(self, "beta", beta)
        object.__setattr__(self, "positive_shape", positive_shape)
        object.__setattr__(self, "negative_shape", negative_shape)

    @classmethod
    def from_model(
        cls, model: FixedBetaDifferenceModel
    ) -> FixedBetaParameterization:
        if not isinstance(model, FixedBetaDifferenceModel):
            raise TypeError("model must be a FixedBetaDifferenceModel")
        model = FixedBetaDifferenceModel(
            model.positive, model.negative, model.beta
        )
        return cls(
            beta=model.beta,
            positive_shape=_state_shape(model.positive),
            negative_shape=(
                None if model.negative is None else _state_shape(model.negative)
            ),
        )

    @property
    def parameter_count(self) -> int:
        count = _parameter_count(self.positive_shape)
        if self.negative_shape is not None:
            count += _parameter_count(self.negative_shape)
        return count

    def pack(self, model: FixedBetaDifferenceModel) -> np.ndarray:
        if not isinstance(model, FixedBetaDifferenceModel):
            raise TypeError("model must be a FixedBetaDifferenceModel")
        # Revalidate because the frozen model contains mutable ndarray objects.
        model = FixedBetaDifferenceModel(
            model.positive, model.negative, model.beta
        )
        if model.beta != self.beta:
            raise ValueError("model beta differs from parameterization beta")
        if _state_shape(model.positive) != self.positive_shape:
            raise ValueError("positive component shape differs")
        if self.negative_shape is None:
            return _pack_mixed(model.positive).copy()
        if model.negative is None or _state_shape(model.negative) != self.negative_shape:
            raise ValueError("negative component shape differs")
        return np.concatenate([
            _pack_mixed(model.positive), _pack_mixed(model.negative)
        ])

    def unpack(self, parameters) -> FixedBetaDifferenceModel:
        array = np.asarray(parameters)
        if (
            array.ndim != 1
            or np.iscomplexobj(array)
            or not np.issubdtype(array.dtype, np.number)
        ):
            raise TypeError("parameters must be a one-dimensional real array")
        vector = np.asarray(array, float)
        if len(vector) != self.parameter_count:
            raise ValueError(
                f"parameters have length {len(vector)}, expected "
                f"{self.parameter_count}"
            )
        if not np.all(np.isfinite(vector)):
            raise ValueError("parameters must be finite")

        positive_count = _parameter_count(self.positive_shape)
        positive = _unpack_mixed(vector[:positive_count], *self.positive_shape)
        negative = None
        if self.negative_shape is not None:
            negative = _unpack_mixed(
                vector[positive_count:], *self.negative_shape
            )
        return FixedBetaDifferenceModel(positive, negative, self.beta)

    def density_and_jacobian(
        self,
        parameters,
        X,
        theta,
        eta: float,
        extra_noise_var: float = 0.0,
        chunk: int = 8192,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Signed density and state-parameter Jacobian for one angle group."""
        model = self.unpack(parameters)
        X_array = np.asarray(X)
        theta_array = np.asarray(theta)
        modes = self.positive_shape[2]
        if (
            X_array.ndim != 2
            or X_array.shape[0] < 1
            or X_array.shape[1] != modes
        ):
            raise ObservationInputError(
                f"X must have shape (samples >= 1, {modes})"
            )
        if theta_array.shape != (modes,):
            raise ObservationInputError(f"theta must have shape ({modes},)")
        X_array = _fixed._as_real_finite(X_array, "X")
        theta_array = _fixed._as_real_finite(theta_array, "theta")
        eta, extra_noise_var = _fixed._validate_loss_parameters(
            eta, extra_noise_var
        )

        positive, J_positive = lossy_pdf_and_jac_mixed(
            model.positive,
            X_array,
            theta_array,
            eta,
            extra_noise_var,
            chunk,
        )
        if model.negative is None:
            density, jacobian = positive, J_positive
        else:
            negative, J_negative = lossy_pdf_and_jac_mixed(
                model.negative,
                X_array,
                theta_array,
                eta,
                extra_noise_var,
                chunk,
            )
            c_positive, c_negative = model.density_coefficients
            density = c_positive * positive + c_negative * negative
            jacobian = np.concatenate(
                [c_positive * J_positive, c_negative * J_negative], axis=1
            )
        if not np.all(np.isfinite(density)) or not np.all(np.isfinite(jacobian)):
            raise FloatingPointError("density and Jacobian must be finite")
        return density, jacobian


def _reduce_grid_barrier(group_outputs) -> tuple[float, np.ndarray | None]:
    """Apply the declared equal-group squared-hinge reduction once."""
    group_values = []
    group_gradients = []
    gradient_mode = None
    for density, jacobian in group_outputs:
        density = np.asarray(density, dtype=float)
        if density.ndim != 1 or len(density) < 1:
            raise ValueError("grid density must be a nonempty vector")
        if not np.all(np.isfinite(density)):
            raise FloatingPointError("grid density must be finite")
        negative = np.minimum(density, 0.0)
        group_values.append(float(np.mean(negative ** 2)))
        has_gradient = jacobian is not None
        if gradient_mode is None:
            gradient_mode = has_gradient
        elif gradient_mode != has_gradient:
            raise RuntimeError("grid barrier groups mixed value and gradient modes")
        if has_gradient:
            jacobian = np.asarray(jacobian, dtype=float)
            if jacobian.ndim != 2 or jacobian.shape[0] != len(density):
                raise ValueError("grid Jacobian has invalid shape")
            if not np.all(np.isfinite(jacobian)):
                raise FloatingPointError("grid Jacobian must be finite")
            group_gradients.append(
                np.mean(2.0 * negative[:, None] * jacobian, axis=0)
            )
    if not group_values:
        raise ValueError("grid_groups must contain at least one group")
    value = float(np.mean(group_values))
    if not gradient_mode:
        return value, None
    return value, np.mean(np.stack(group_gradients), axis=0)


def _dense_grid_barrier_value(
    parameterization: FixedBetaParameterization,
    parameters,
    grid_groups,
    eta: float,
    extra_noise_var: float = 0.0,
) -> float:
    """Internal value-only evaluation of the declared grid barrier."""
    if not isinstance(parameterization, FixedBetaParameterization):
        raise TypeError("parameterization must be a FixedBetaParameterization")
    vector = np.asarray(parameters)
    model = parameterization.unpack(vector)
    value, gradient = _reduce_grid_barrier(
        (
            (model.pdf(X, theta, eta, extra_noise_var), None)
            for theta, X in grid_groups
        )
    )
    if gradient is not None:
        raise RuntimeError("value-only grid barrier produced a gradient")
    return value


def dense_grid_barrier_and_grad(
    parameterization: FixedBetaParameterization,
    parameters,
    grid_groups,
    eta: float,
    extra_noise_var: float = 0.0,
    chunk: int = 8192,
) -> tuple[float, np.ndarray]:
    """Equal-group mean of ``min(p, 0)^2`` and its analytic gradient."""
    if not isinstance(parameterization, FixedBetaParameterization):
        raise TypeError("parameterization must be a FixedBetaParameterization")
    vector = np.asarray(parameters)
    # Validate the vector even when grid_groups is empty.
    parameterization.unpack(vector)
    value, gradient = _reduce_grid_barrier(
        (
            parameterization.density_and_jacobian(
                vector, X, theta, eta, extra_noise_var, chunk
            )
            for theta, X in grid_groups
        )
    )
    if gradient is None:
        raise RuntimeError("gradient grid barrier did not produce a gradient")
    return value, gradient
