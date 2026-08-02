"""Experiment 28 toolkit: certified link-stability radii on the census sphere.

Implements the pre-declared quantities of derivation.md (this directory):
the Cauchy constant c1(h) of S2, the |1,1> closed-form margins of S4, the
eps0_cert grid search of §3, the phase-aligned distance of §1, the numeric
sigma_2 evaluator used by the one-sided E1 referee and by E5, and the E3
probe-direction builders. No epistemic status is authored here (§7 of
derivation.md is the sole authoring location); every function returns raw
numbers for run.py to record in isotopy_stability.json.

Distances: delta is the phase-aligned norm distance of derivation.md §1,
delta = sqrt(2 (1 - |<psi|T>|)) for unit states. Perturbation curves are
psi(s) = normalize(T + s v) with v a unit direction orthogonal to T, so
|<psi(s)|T>| = 1 / sqrt(1 + s^2) exactly.
"""

from __future__ import annotations

import math

import numpy as np

from wigner_splat.stellar2 import gaussian_term_fock_coeffs


# ---------------------------------------------------------------------------
# S2 / S4 closed forms and the eps0_cert grid search (E2)
# ---------------------------------------------------------------------------

def c1(h):
    """S2 derivative constant sqrt(2) exp((1+h)^2/2) / h for |w0| <= 1."""
    h = float(h)
    if h <= 0.0:
        raise ValueError("h must be positive")
    return math.sqrt(2.0) * math.exp((1.0 + h) ** 2 / 2.0) / h


def hopf_m(rho):
    """S4 clearance margin of |1,1> on S3_1: min |f| off the open tubes."""
    return math.sin(2.0 * rho) / 2.0


def hopf_sigma_lb(rho):
    """S4 transversality lower bound cos(2 rho) on the closed tubes."""
    return math.cos(2.0 * rho)


def cert_value(m_rho, sigma_rho, h):
    """The certified radius of one admissible (rho, h) pair (§3)."""
    return min(m_rho * math.exp(-0.5), sigma_rho / c1(h))


def eps0_cert_hopf(rho_grid, h_grid):
    """Best certified stability radius for |1,1> on the declared grid.

    Returns (eps0_cert, rho_star, h_star). Certified: the margins come from
    the proved S4 closed forms, so each grid pair's min is exact up to float
    rounding.
    """
    best = (0.0, None, None)
    for rho in rho_grid:
        rho = float(rho)
        if not (0.0 < rho < math.pi / 4.0):
            continue  # admissibility for the |1,1> tubes (§4)
        m_rho = hopf_m(rho)
        s_rho = hopf_sigma_lb(rho)
        if m_rho <= 0.0 or s_rho <= 0.0:
            continue
        for h in h_grid:
            val = cert_value(m_rho, s_rho, float(h))
            if val > best[0]:
                best = (val, rho, float(h))
    return best


def fidelity_bound(eps):
    """Exact inversion of delta^2 = 2(1 - sqrt F) at delta = eps (§5, E4).

    Computed exactly in Fraction and converted to float rounded toward
    +infinity, so the serialized upper bound is never strengthened by a
    nearest-rounding ULP (fix propagated from the exp29 Sol re-audit)."""
    from fractions import Fraction

    eps = float(eps)
    if not (0.0 <= eps <= math.sqrt(2.0)):
        raise ValueError("eps outside [0, sqrt 2]")
    exact = (1 - Fraction(eps) ** 2 / 2) ** 2
    f = float(exact)
    while Fraction(f) < exact:
        f = math.nextafter(f, math.inf)
    return f


# ---------------------------------------------------------------------------
# phase-aligned distance and the perturbation curve (E3)
# ---------------------------------------------------------------------------

def delta_of_s(s):
    """delta(psi(s), T) for psi(s) = normalize(T + s v), v unit, v ⊥ T."""
    return math.sqrt(2.0 * (1.0 - 1.0 / math.sqrt(1.0 + float(s) ** 2)))


def s_of_delta(delta):
    """Inverse of delta_of_s on 0 <= delta < sqrt(2)."""
    delta = float(delta)
    if not (0.0 <= delta < math.sqrt(2.0)):
        raise ValueError("delta outside [0, sqrt 2)")
    a = 1.0 - delta * delta / 2.0
    return math.sqrt(1.0 / (a * a) - 1.0)


def pad_to(c, shape):
    out = np.zeros(shape, dtype=complex)
    out[: c.shape[0], : c.shape[1]] = c
    return out


def perturbed_coeffs(target_c, v_c, s):
    """Fock coefficients of normalize(T + s v) on the union shape."""
    shape = (
        max(target_c.shape[0], v_c.shape[0]),
        max(target_c.shape[1], v_c.shape[1]),
    )
    c = pad_to(target_c, shape) + float(s) * pad_to(v_c, shape)
    return c / math.sqrt(float(np.sum(np.abs(c) ** 2)))


def unit_orthogonal(v_c, target_c):
    """Project v off the target and unit-normalize (both Fock arrays)."""
    shape = (
        max(target_c.shape[0], v_c.shape[0]),
        max(target_c.shape[1], v_c.shape[1]),
    )
    t = pad_to(target_c, shape)
    t = t / math.sqrt(float(np.sum(np.abs(t) ** 2)))
    v = pad_to(v_c, shape)
    v = v - np.vdot(t, v) * t
    norm = math.sqrt(float(np.sum(np.abs(v) ** 2)))
    if norm < 1e-12:
        raise ValueError("direction is parallel to the target")
    return v / norm


# ---------------------------------------------------------------------------
# E3 probe directions (constants pre-declared in derivation.md §6)
# ---------------------------------------------------------------------------

KERNEL_THETAS = (math.pi / 8.0, 3.0 * math.pi / 8.0)
KERNEL_PHASES = (0.0, math.pi / 2.0)
RANDOM_SEED = 137028
RANDOM_DIRECTIONS = 24
RANDOM_CUTOFF = 12
KERNEL_CUTOFF = 12


def kernel_direction(theta, a, b, target_c, cutoff=KERNEL_CUTOFF):
    """Coherent-kernel direction at w0 = (e^{ia} cos t0, e^{ib} sin t0):
    v_mn ∝ conj(w0_1^m w0_2^n) / sqrt(m! n!) (S1's equality direction),
    projected off the target and unit-normalized."""
    w1 = np.exp(1j * a) * math.cos(theta)
    w2 = np.exp(1j * b) * math.sin(theta)
    m = np.arange(cutoff)
    fact = np.vectorize(math.factorial, otypes=[float])
    v = np.outer(np.conj(w1**m), np.conj(w2**m.copy())) / np.sqrt(
        np.outer(fact(m), fact(m))
    )
    return unit_orthogonal(v, target_c)


def kernel_direction_list(target_c):
    dirs = []
    for t0 in KERNEL_THETAS:
        for a in KERNEL_PHASES:
            for b in KERNEL_PHASES:
                label = f"kernel(t0={t0:.6f},a={a:.6f},b={b:.6f})"
                dirs.append((label, kernel_direction(t0, a, b, target_c)))
    return dirs


def random_direction_list(target_c, seed=RANDOM_SEED, n=RANDOM_DIRECTIONS,
                          cutoff=RANDOM_CUTOFF):
    rng = np.random.default_rng(seed)
    dirs = []
    for k in range(n):
        v = rng.normal(size=(cutoff, cutoff)) + 1j * rng.normal(
            size=(cutoff, cutoff)
        )
        dirs.append((f"random({seed},{k})", unit_orthogonal(v, target_c)))
    return dirs


def exp25_endpoint_direction(cells, target_c, cutoff):
    """Direction toward the best-found |11>/D_coh/K=2 state of exp25,
    reconstructed from its recorded parameters (best_params + coeffs_z)."""
    cell = cells["t11/coherent/K=2"]
    x = np.asarray(cell["best_params"], dtype=float).reshape(-1, 4)
    z = np.array([complex(re, im) for re, im in cell["coeffs_z"]])
    state = np.zeros(cutoff * cutoff, dtype=complex)
    for row, zk in zip(x, z):
        term = (1.0, row[0] + 1j * row[1], row[2] + 1j * row[3], 0.0, 0.0, 0.0)
        c = gaussian_term_fock_coeffs(term, cutoff)
        total = math.sqrt(float(np.sum(np.abs(c) ** 2)))
        state += zk * c.ravel() / total
    state = state.reshape(cutoff, cutoff)
    state = state / math.sqrt(float(np.sum(np.abs(state) ** 2)))
    return "exp25_endpoint(t11/coherent/K=2)", unit_orthogonal(state, target_c)


# ---------------------------------------------------------------------------
# numeric sigma_2 evaluator (E1 referee, E5)
# ---------------------------------------------------------------------------

def _tangent_basis(w1, w2):
    """Orthonormal real basis of T_w S3_1 inside C^2 ~ R^4."""
    x = np.array([w1.real, w1.imag, w2.real, w2.imag], dtype=float)
    basis = []
    for k in range(4):
        e = np.zeros(4)
        e[k] = 1.0
        v = e - np.dot(e, x) * x
        for b in basis:
            v = v - np.dot(v, b) * b
        n = np.linalg.norm(v)
        if n > 1e-9:
            basis.append(v / n)
    if len(basis) != 3:
        raise RuntimeError("tangent basis construction failed")
    return basis


def sigma2_on_sphere(d1, d2, w1, w2):
    """Smallest singular value of d(f|S3): T_w S3 -> R^2, from the exact
    holomorphic partials d1 = d f/d w1, d2 = d f/d w2 at (w1, w2)."""
    rows = []
    for v in _tangent_basis(complex(w1), complex(w2)):
        v1 = complex(v[0], v[1])
        v2 = complex(v[2], v[3])
        dfv = d1 * v1 + d2 * v2
        rows.append((dfv.real, dfv.imag))
    jac = np.array(rows).T  # 2 x 3
    return float(np.linalg.svd(jac, compute_uv=False)[-1])


def sphere_point(theta, a, b):
    return (
        np.exp(1j * a) * math.cos(theta),
        np.exp(1j * b) * math.sin(theta),
    )


# ---------------------------------------------------------------------------
# polynomial stellar helpers (targets are Fock polynomials)
# ---------------------------------------------------------------------------

def poly_scaled(coeffs):
    """Monomial coefficients p_mn = c_mn / sqrt(m! n!) of the stellar poly."""
    c = np.asarray(coeffs, dtype=complex)
    fact = np.vectorize(math.factorial, otypes=[float])
    return c / np.sqrt(
        np.outer(fact(np.arange(c.shape[0])), fact(np.arange(c.shape[1])))
    )


def poly_eval(p, w1, w2):
    m = np.arange(p.shape[0])
    n = np.arange(p.shape[1])
    return np.einsum(
        "mn,m...,n...->...",
        p,
        np.stack([np.asarray(w1, dtype=complex) ** k for k in m]),
        np.stack([np.asarray(w2, dtype=complex) ** k for k in n]),
    )


def poly_partials(p):
    d1 = (p[1:, :].T * np.arange(1, p.shape[0])).T if p.shape[0] > 1 else np.zeros((1, p.shape[1]), dtype=complex)
    d2 = p[:, 1:] * np.arange(1, p.shape[1]) if p.shape[1] > 1 else np.zeros((p.shape[0], 1), dtype=complex)
    return d1, d2


# ---------------------------------------------------------------------------
# zero-point cloud + grid margins for targets without closed forms (E5)
# ---------------------------------------------------------------------------

def _project_sphere(w1, w2):
    n = math.sqrt(abs(w1) ** 2 + abs(w2) ** 2)
    return w1 / n, w2 / n


def polish_zero(p, d1p, d2p, w1, w2, iters=80, max_step=0.25):
    """Damped Gauss-Newton for f = 0 restricted to S3_1: least-norm tangent
    step -J^+ (Re f, Im f) with the 2x3 real Jacobian of f|S3, then
    reprojection to the sphere."""
    w1, w2 = complex(w1), complex(w2)
    for _ in range(iters):
        f = complex(poly_eval(p, w1, w2))
        if abs(f) < 1e-13:
            break
        d1 = complex(poly_eval(d1p, w1, w2))
        d2 = complex(poly_eval(d2p, w1, w2))
        try:
            basis = _tangent_basis(w1, w2)
        except RuntimeError:
            break
        rows = []
        for v in basis:
            dfv = d1 * complex(v[0], v[1]) + d2 * complex(v[2], v[3])
            rows.append((dfv.real, dfv.imag))
        jac = np.array(rows).T  # 2 x 3
        coeffs, *_ = np.linalg.lstsq(jac, -np.array([f.real, f.imag]), rcond=None)
        norm = float(np.linalg.norm(coeffs))
        if not math.isfinite(norm) or norm < 1e-16:
            break
        if norm > max_step:
            coeffs = coeffs * (max_step / norm)
        move = sum(c * np.asarray(v) for c, v in zip(coeffs, basis))
        w1, w2 = _project_sphere(
            w1 + complex(move[0], move[1]), w2 + complex(move[2], move[3])
        )
    return w1, w2, abs(complex(poly_eval(p, w1, w2)))


def zero_cloud(coeffs, n_theta=40, n_phase=24, keep_tol=1e-10, dedup=5e-3):
    """Polished, deduplicated zero points of the stellar polynomial on S3_1,
    as an (N, 4) real array."""
    p = poly_scaled(coeffs)
    d1p, d2p = poly_partials(p)
    pts = []
    thetas = np.linspace(0.02, math.pi / 2 - 0.02, n_theta)
    phases = np.arange(n_phase) * (2.0 * math.pi / n_phase)
    for th in thetas:
        for a in phases:
            for b in phases:
                w1, w2 = sphere_point(th, a, b)
                z1, z2, resid = polish_zero(p, d1p, d2p, w1, w2)
                if resid < keep_tol:
                    pts.append([z1.real, z1.imag, z2.real, z2.imag])
    if not pts:
        return np.zeros((0, 4))
    cloud = np.array(pts)
    kept: list[np.ndarray] = []
    for row in cloud:
        if not kept or np.min(
            np.linalg.norm(np.array(kept) - row, axis=1)
        ) > dedup:
            kept.append(row)
    return np.array(kept)


def geodesic_dists(x_rows, cloud):
    """Geodesic distances on S3_1 from each row of x_rows (N, 4) to the
    nearest cloud point (M, 4); vectorized arccos of the R^4 dot product.

    Contract: callers pass unit rows on both sides — this function does
    not normalize, and non-unit inputs make acos(p . c) a biased distance
    (exp29 round-5 audit). Certified users must additionally budget the
    float norm/dot/acos error (exp29 derivation §3 lemma)."""
    dots = np.clip(x_rows @ cloud.T, -1.0, 1.0)
    return np.arccos(np.max(dots, axis=1))


def grid_margins(coeffs, cloud, rho_list, n_theta=60, n_phase=8):
    """Grid estimates of (m(rho), sigma(rho)) relative to the zero cloud.

    Grid minima over-estimate true minima (unsafe direction), so results
    are numerically supported only, never certified (derivation.md E5).
    """
    p = poly_scaled(coeffs)
    d1p, d2p = poly_partials(p)
    thetas = np.linspace(0.01, math.pi / 2 - 0.01, n_theta)
    phases = np.arange(n_phase) * (2.0 * math.pi / n_phase)
    rows, fvals, sigs = [], [], []
    for th in thetas:
        for a in phases:
            for b in phases:
                w1, w2 = sphere_point(th, a, b)
                rows.append([w1.real, w1.imag, w2.real, w2.imag])
                fvals.append(abs(complex(poly_eval(p, w1, w2))))
                sigs.append(
                    sigma2_on_sphere(
                        complex(poly_eval(d1p, w1, w2)),
                        complex(poly_eval(d2p, w1, w2)),
                        w1,
                        w2,
                    )
                )
    dists = geodesic_dists(np.array(rows), cloud)
    fvals = np.array(fvals)
    sigs = np.array(sigs)
    out = {}
    for rho in rho_list:
        outside = fvals[dists >= rho]
        inside = sigs[dists <= rho]
        if outside.size == 0 or inside.size == 0:
            out[rho] = None
            continue
        out[rho] = (float(np.min(outside)), float(np.min(inside)))
    return out
