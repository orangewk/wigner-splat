"""Strict train objective and gradients for one Stage 1 candidate setup."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

import numpy as np


_fixed = import_module("experiments.33_negativity_budget.fixed_beta")
_packet2 = import_module("experiments.33_negativity_budget.packet2")
_setup = import_module("experiments.33_negativity_budget.stage1_setup")
Stage1CandidateSetup = _setup.Stage1CandidateSetup


ETA_FD_STEP = 1e-4
ETA_FD_HALVINGS = 12
ETA_FD_CONSISTENCY_RTOL = 1e-2
ETA_FD_CONSISTENCY_ATOL = 1e-8


class EtaGradientUnavailable(RuntimeError):
    """No valid symmetric eta-logit finite difference was found."""


@dataclass(frozen=True)
class Stage1ObjectiveEvaluation:
    objective: float
    train_nll: float
    barrier: float
    eta: float


@dataclass(frozen=True)
class Stage1ObjectiveResult:
    evaluation: Stage1ObjectiveEvaluation
    gradient: np.ndarray
    eta_fd_step: float


def _sigmoid(value: float) -> float:
    if value >= 0.0:
        return float(1.0 / (1.0 + np.exp(-value)))
    exp_value = np.exp(value)
    return float(exp_value / (1.0 + exp_value))


def _eta_from_logit(eta_logit) -> tuple[float, float]:
    eta_logit = _fixed._as_loss_scalar(eta_logit, "eta_logit")
    eta = _sigmoid(eta_logit)
    if not 0.0 < eta < 1.0:
        raise FloatingPointError(
            "eta_logit must map to a float64 eta strictly inside (0, 1)"
        )
    return eta_logit, eta


@dataclass(frozen=True)
class Stage1Objective:
    setup: Stage1CandidateSetup
    barrier_weight: float

    def __post_init__(self) -> None:
        if not isinstance(self.setup, Stage1CandidateSetup):
            raise TypeError("setup must be a Stage1CandidateSetup")
        barrier_weight = _fixed._as_loss_scalar(
            self.barrier_weight, "barrier_weight"
        )
        if barrier_weight < 0.0:
            raise ValueError("barrier_weight must be nonnegative")
        if self.setup.parameterization.beta != self.setup.beta:
            raise ValueError("setup beta differs from parameterization beta")
        self.setup.parameterization.unpack(self.setup.initial_parameters)
        object.__setattr__(self, "barrier_weight", barrier_weight)

    def value(self, parameters, eta_logit) -> Stage1ObjectiveEvaluation:
        """Evaluate strict train NLL plus the weighted grid barrier."""
        _, eta = _eta_from_logit(eta_logit)
        model = self.setup.parameterization.unpack(parameters)
        train_nll = _fixed.mean_nll(model, self.setup.train_groups, eta)
        barrier = _packet2._dense_grid_barrier_value(
            self.setup.parameterization,
            parameters,
            self.setup.grid_groups,
            eta,
        )
        objective = train_nll + self.barrier_weight * barrier
        if not np.isfinite(objective):
            raise FloatingPointError("objective must be finite")
        return Stage1ObjectiveEvaluation(
            objective=float(objective),
            train_nll=float(train_nll),
            barrier=float(barrier),
            eta=eta,
        )

    def _state_gradient(
        self,
        parameters,
        eta: float,
        expected_barrier: float,
    ) -> np.ndarray:
        parameterization = self.setup.parameterization
        gradient_sum = np.zeros(parameterization.parameter_count)
        sample_count = 0
        for group_index, (theta, X) in enumerate(self.setup.train_groups):
            density, jacobian = parameterization.density_and_jacobian(
                parameters, X, theta, eta
            )
            invalid = ~np.isfinite(density) | (density <= 0.0)
            if np.any(invalid):
                raise _fixed.NonPositiveDensityError(
                    group_index,
                    int(np.count_nonzero(invalid)),
                    len(density),
                )
            gradient_sum += np.sum(-jacobian / density[:, None], axis=0)
            sample_count += len(density)
        if sample_count < 1:
            raise ValueError("train groups must contain at least one sample")
        barrier, barrier_gradient = _packet2.dense_grid_barrier_and_grad(
            parameterization,
            parameters,
            self.setup.grid_groups,
            eta,
        )
        if not np.isclose(
            barrier, expected_barrier, rtol=2e-13, atol=1e-15
        ):
            raise RuntimeError("grid barrier value and gradient paths disagree")
        gradient = (
            gradient_sum / sample_count
            + self.barrier_weight * barrier_gradient
        )
        if not np.all(np.isfinite(gradient)):
            raise FloatingPointError("state gradient must be finite")
        return gradient

    def value_and_grad(self, parameters, eta_logit) -> Stage1ObjectiveResult:
        """Return value metrics and the packed state-plus-logit gradient."""
        eta_logit, eta = _eta_from_logit(eta_logit)
        evaluation = self.value(parameters, eta_logit)
        state_gradient = self._state_gradient(
            parameters, eta, evaluation.barrier
        )

        step = ETA_FD_STEP
        eta_gradient = None
        for _ in range(ETA_FD_HALVINGS + 1):
            try:
                plus = self.value(parameters, eta_logit + step).objective
                minus = self.value(parameters, eta_logit - step).objective
                plus_wide = self.value(
                    parameters, eta_logit + 2.0 * step
                ).objective
                minus_wide = self.value(
                    parameters, eta_logit - 2.0 * step
                ).objective
            except (_fixed.NonPositiveDensityError, FloatingPointError):
                step *= 0.5
                continue
            candidate = (plus - minus) / (2.0 * step)
            wide_candidate = (plus_wide - minus_wide) / (4.0 * step)
            if not np.isfinite(candidate) or not np.isfinite(wide_candidate):
                step *= 0.5
                continue
            if not np.isclose(
                candidate,
                wide_candidate,
                rtol=ETA_FD_CONSISTENCY_RTOL,
                atol=ETA_FD_CONSISTENCY_ATOL,
            ):
                raise EtaGradientUnavailable(
                    "eta-logit finite differences are inconsistent across steps"
                )
            eta_gradient = float(candidate)
            break
        if eta_gradient is None:
            raise EtaGradientUnavailable(
                "no valid symmetric eta-logit finite difference was found"
            )

        gradient = np.concatenate([state_gradient, [eta_gradient]])
        gradient.setflags(write=False)
        return Stage1ObjectiveResult(
            evaluation=evaluation,
            gradient=gradient,
            eta_fd_step=float(step),
        )
