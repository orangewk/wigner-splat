"""Finite-energy square-GKP Bargmann zeros for Gate E.

The state is the standard position-comb approximation to logical |0>:

    sum_s exp(-2 pi Delta**2 s**2) D(s sqrt(2 pi)) S(-log Delta) |0>.

Here [q, p] = i and the vacuum q variance is 1/2.  The finite lattice sum is
only a numerical realization of the exponentially convergent comb; its
omitted envelope is recorded by ``build_gkp_state``.  Fock truncation is
handled separately and conservatively by ``fock_tail_upper_bound``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, lgamma, pi, sqrt

import numpy as np


@dataclass(frozen=True)
class GKPState:
    delta: float
    n_max: int
    coefficients: np.ndarray
    mean_photon_reference: float
    fock_tail_upper_bound: float
    lattice_envelope_amplitude_bound: float
    s_max: int
    reference_cutoff: int


def _squeezed_coherent_coefficients(alpha: float, r: float, n_max: int) -> np.ndarray:
    """Fock coefficients of D(alpha) S(r)|0>, for real alpha and r.

    The recurrence follows from (a + tanh(r) a^dagger
    - alpha * (1 + tanh(r))) |psi> = 0.  Its initial coefficient has the
    usual squeezed-coherent normalization and fixes the otherwise ambiguous
    recurrence scale.
    """
    t = np.tanh(r)
    beta = alpha * (1.0 + t)
    coeff = np.zeros(n_max + 1, dtype=np.complex128)
    coeff[0] = exp(-0.5 * alpha * alpha * (1.0 + t)) / sqrt(np.cosh(r))
    if n_max:
        coeff[1] = beta * coeff[0]
    for n in range(1, n_max):
        coeff[n + 1] = (beta * coeff[n] - t * sqrt(n) * coeff[n - 1]) / sqrt(n + 1)
    return coeff


def _factorial_second_moment(alpha: float, r: float) -> float:
    """Exact <N(N-1)> for D(alpha)S(r)|0> (real parameters)."""
    n_bar = np.sinh(r) ** 2
    anomalous = -np.sinh(r) * np.cosh(r)
    return float(alpha**4 + 4 * alpha**2 * n_bar + 2 * alpha**2 * anomalous + 2 * n_bar**2 + anomalous**2)


def _component_tail_upper_bound(coeff: np.ndarray, alpha: float, r: float, n_max: int, reference_cutoff: int) -> float:
    """Bound P(N > n_max), retaining a rigorous factorial-moment remainder."""
    resolved = float(np.sum(np.abs(coeff[n_max + 1 :]) ** 2))
    # Markov on N(N-1): P(N > c) = P(N(N-1) >= c(c+1)) <= <N(N-1)> / (c(c+1)).
    moment_remainder = _factorial_second_moment(alpha, r) / (reference_cutoff * (reference_cutoff + 1))
    return resolved + moment_remainder


def build_gkp_state(delta: float, n_max: int, *, lattice_tolerance: float = 1e-15, reference_cutoff: int | None = None) -> GKPState:
    """Construct a normalized finite-energy square-GKP |0> Fock vector.

    The reported Fock tail is an upper bound for the *finite lattice sum*:
    triangle inequality combines each component's resolved tail with its exact
    second-factorial-moment Markov bound beyond ``reference_cutoff``.
    """
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0, 1)")
    if n_max < 8:
        raise ValueError("n_max is too small for a robust-zero calculation")
    reference_cutoff = reference_cutoff or max(4 * n_max, 512)
    if reference_cutoff <= n_max:
        raise ValueError("reference_cutoff must exceed n_max")
    kappa = 2.0 * pi * delta**2
    s_max = 0
    while 2.0 * exp(-kappa * (s_max + 1) ** 2) / (1.0 - exp(-kappa * (2 * s_max + 3))) > lattice_tolerance:
        s_max += 1
    r = -np.log(delta)
    unnormalized = np.zeros(reference_cutoff + 1, dtype=np.complex128)
    tail_norm_sum = 0.0
    for s in range(-s_max, s_max + 1):
        weight = exp(-kappa * s * s)
        alpha = s * sqrt(2.0 * pi)
        component = _squeezed_coherent_coefficients(alpha, r, reference_cutoff)
        unnormalized += weight * component
        tail_norm_sum += abs(weight) * sqrt(_component_tail_upper_bound(component, alpha, r, n_max, reference_cutoff))
    projection_norm_sq = float(np.vdot(unnormalized, unnormalized).real)
    assert projection_norm_sq > 0.0
    tail_upper = (tail_norm_sum**2) / projection_norm_sq
    coeff = unnormalized[: n_max + 1].copy()
    coeff /= np.linalg.norm(coeff)
    envelope_bound = 2.0 * exp(-kappa * (s_max + 1) ** 2) / (1.0 - exp(-kappa * (2 * s_max + 3)))
    return GKPState(
        delta=delta,
        n_max=n_max,
        coefficients=coeff,
        mean_photon_reference=float(np.dot(np.arange(reference_cutoff + 1), np.abs(unnormalized) ** 2) / projection_norm_sq),
        fock_tail_upper_bound=tail_upper,
        lattice_envelope_amplitude_bound=envelope_bound,
        s_max=s_max,
        reference_cutoff=reference_cutoff,
    )


def bargmann_polynomial_coefficients(fock_coefficients: np.ndarray) -> np.ndarray:
    n = np.arange(len(fock_coefficients))
    scale = np.exp(-0.5 * np.array([lgamma(int(k) + 1) for k in n]))
    return fock_coefficients * scale


def bargmann_value(coefficients: np.ndarray, z: np.ndarray | complex) -> np.ndarray | complex:
    return np.polynomial.polynomial.polyval(z, bargmann_polynomial_coefficients(coefficients))


def bargmann_derivative_upper_bound(coefficients: np.ndarray, radius: float) -> float:
    """Proven upper bound for ``sup_|z|<=radius |F'(z)|`` from Fock coefficients."""
    if radius < 0.0:
        raise ValueError("radius must be non-negative")
    n = np.arange(1, len(coefficients), dtype=float)
    if not len(n):
        return 0.0
    log_scale = -0.5 * np.array([lgamma(int(k) + 1) for k in n])
    terms = np.abs(coefficients[1:]) * n * radius ** (n - 1.0) * np.exp(log_scale)
    return float(np.sum(terms))


def circle_minimum_lower_bound(
    coefficients: np.ndarray, center: complex, delta: float, samples: int
) -> tuple[float, float, float]:
    """Return sampled minimum, derivative bound, and a proven circle lower bound.

    Every circle point is within one sample-arc length of a sample. The
    mean-value inequality gives the lower bound; a full arc is conservative.
    """
    if delta <= 0.0 or samples < 1:
        raise ValueError("delta must be positive and samples must be nonzero")
    phases = np.linspace(0.0, 2.0 * pi, samples, endpoint=False)
    sampled_minimum = float(np.min(np.abs(bargmann_value(coefficients, center + delta * np.exp(1j * phases)))))
    derivative_bound = bargmann_derivative_upper_bound(coefficients, abs(center) + delta)
    lower_bound = max(0.0, sampled_minimum - (2.0 * pi * delta / samples) * derivative_bound)
    return sampled_minimum, derivative_bound, lower_bound

def find_zeros(coefficients: np.ndarray, radius: float, *, residual_tolerance: float = 1e-7) -> np.ndarray:
    """Find polynomial zeros and independently reject inaccurate root solves."""
    polynomial = bargmann_polynomial_coefficients(coefficients)
    roots = np.polynomial.polynomial.polyroots(polynomial)
    scale = max(1.0, float(np.max(np.abs(polynomial))))
    roots = roots[np.abs(roots) <= radius]
    residuals = np.abs(bargmann_value(coefficients, roots)) / scale
    assert np.all(residuals < residual_tolerance), float(np.max(residuals, initial=0.0))
    return roots[np.lexsort((roots.imag, roots.real))]


def winding_number(coefficients: np.ndarray, center: complex, half_width: float, samples_per_edge: int = 96) -> int:
    """Argument-principle count on a square, used to cross-check root finding."""
    t = np.linspace(-half_width, half_width, samples_per_edge, endpoint=False)
    contour = np.concatenate((
        center + t - 1j * half_width,
        center + half_width + 1j * t,
        center - t + 1j * half_width,
        center - half_width - 1j * t,
    ))
    values = bargmann_value(coefficients, contour)
    assert np.min(np.abs(values)) > 1e-10, "zero too close to winding contour"
    return int(np.rint(np.sum(np.angle(values[1:] / values[:-1])) / (2.0 * pi) + np.angle(values[0] / values[-1]) / (2.0 * pi)))


def validate_zero_count(coefficients: np.ndarray, radius: float, roots: np.ndarray) -> None:
    """Cross-check root counts by tiled argument-principle counts.

    Coverage note (#71 exp23 merge review, point 3): only cells fully inside
    the window (|center| + sqrt(2)*cell/2 <= radius) are checked, so the
    annulus near |z| = radius is NOT covered by this cross-check.
    """
    cell = 0.45
    centers = np.arange(-radius + cell / 2, radius, cell)
    checked_cells = 0
    for x in centers:
        for y in centers:
            center = complex(x, y)
            if abs(center) + sqrt(2.0) * cell / 2 <= radius:
                expected = sum(abs(root.real - x) < cell / 2 and abs(root.imag - y) < cell / 2 for root in roots)
                observed = winding_number(coefficients, center, cell / 2)
                assert observed == expected, (center, observed, expected)
                checked_cells += 1
    assert checked_cells > 0


def robust_zero_rows(
    coefficients: np.ndarray,
    roots: np.ndarray,
    delta: float,
    epsilons: tuple[float, ...],
    *,
    tail_norm: float = 0.0,
    lattice_envelope_amplitude_bound: float = 0.0,
    circle_samples: int = 1440,
) -> list[dict]:
    """Evaluate sampled and interval-bounded Rouché conditions on each disk."""
    if len(roots) > 1:
        separations = np.abs(roots[:, None] - roots[None, :])
        np.fill_diagonal(separations, np.inf)
        assert float(np.min(separations)) > 2.0 * delta, "robustness disks are not disjoint"
    rows: list[dict] = []
    for root in roots:
        minimum, derivative_bound, lower_bound = circle_minimum_lower_bound(coefficients, root, delta, circle_samples)
        for epsilon in epsilons:
            d_epsilon = sqrt(2.0 - 2.0 * sqrt(1.0 - epsilon))
            threshold = exp((abs(root) + delta) ** 2 / 2.0) * d_epsilon
            lifted_threshold = exp((abs(root) + delta) ** 2 / 2.0) * (
                d_epsilon + tail_norm + lattice_envelope_amplitude_bound
            )
            rows.append({
                "zero": [float(root.real), float(root.imag)],
                "delta": delta,
                "epsilon": epsilon,
                "circle_minimum_sampled": minimum,
                "circle_derivative_upper_bound": derivative_bound,
                "circle_minimum_interval_lower_bound": lower_bound,
                "rouche_threshold": threshold,
                "sampled_robust": bool(minimum > threshold),
                "interval_bounded_robust": bool(lower_bound > threshold),
                "lifted_rouche_threshold": lifted_threshold,
                "sampled_lifted_robust": bool(minimum > lifted_threshold),
                "interval_bounded_lifted_robust": bool(lower_bound > lifted_threshold),
            })
    return rows
