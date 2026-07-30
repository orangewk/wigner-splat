"""Two-mode stellar functions and the topology of their zero links on S^3.

Experiment 24 toolkit (see experiments/24_hopf_stellar/derivation.md for the
propositions and the pre-declared predictions this code is meant to test).

Conventions
-----------
Stellar function of |psi> = sum c_mn |m,n>:

    f(w1, w2) = sum_mn c_mn w1^m w2^n / sqrt(m! n!)        (entire on C^2)
    <gamma1, gamma2|psi> = exp(-(|gamma1|^2+|gamma2|^2)/2) f(conj g1, conj g2)

Husimi zeros correspond to zeros of f. Building blocks:

  * two-mode coherent |g1, g2>:  f = exp(g1 w1 + g2 w2) * const
  * two-mode squeezed vacuum T(lam), lam = tanh r: f = sqrt(1-lam^2) exp(lam w1 w2)

The zero link of a state is  L_r = f^{-1}(0) ∩ S3_r,  S3_r the sphere
|w1|^2 + |w2|^2 = r^2. census() measures, per component: point count and core
windings (winding of arg w1 / arg w2, equal to linking numbers with the two
core great circles {w1=0}, {w2=0} when disjoint from them), plus the pairwise
signed linking matrix. Components carry the boundary orientation induced by
the complex orientation of the analytic curve inside the ball
(outward-normal-first); the ambient sign convention is pinned by the
calibration test in tests/test_stellar2.py (standard Hopf pair -> +1).

Epistemic status of the census: numerically supported, not certified. Zero
curves thinner than the grid are invisible; completeness near the two excluded
coordinate-core caps is checked only by a |f| floor heuristic recorded in the
diagnostics. Detection itself (phase winding around plaquettes) is robust to
amplitude noise because it is purely topological on the grid.

Algorithm
---------
1. Apply a seeded generic U(2) frame rotation (passive invariance,
   derivation.md P2, makes this harmless; it moves curves off the coordinate
   degeneracies of the Hopf-angle grid).
2. Grid S3_r in Hopf angles  w1 = r cos(eta) e^{i xi1},  w2 = r sin(eta)
   e^{i xi2}, eta in [margin, pi/2 - margin], xi periodic.
3. A zero curve pierces a grid plaquette iff the phase of f winds by +-2pi
   around it; pierced faces are chained cell-by-cell into closed loops.
4. Loop points are Newton-polished onto f = 0, canonically oriented from the
   local holomorphic tangent, and linking numbers are counted exactly from
   signed crossings of a generic stereographic projection.
"""

from __future__ import annotations

import math

import numpy as np


TWO_PI = 2.0 * math.pi


# ---------------------------------------------------------------------------
# stellar function builders
# ---------------------------------------------------------------------------

def fock_stellar(coeffs):
    """Stellar function of sum c_mn |m,n> from a 2-D coefficient array.

    Normalization of the state is irrelevant for zeros; coefficients are used
    as given, divided by sqrt(m! n!) per the convention above.
    """
    c = np.asarray(coeffs, dtype=complex)
    m_idx = np.arange(c.shape[0])
    n_idx = np.arange(c.shape[1])
    fact = np.vectorize(math.factorial, otypes=[float])
    scaled = c / np.sqrt(np.outer(fact(m_idx), fact(n_idx)))

    def f(w1, w2):
        w1 = np.asarray(w1, dtype=complex)
        w2 = np.asarray(w2, dtype=complex)
        v1 = np.stack([w1**m for m in m_idx])
        v2 = np.stack([w2**n for n in n_idx])
        return np.einsum("mn,m...,n...->...", scaled, v1, v2)

    return f


def gaussian_sum_stellar(terms):
    """Stellar function sum_k z_k exp(l1 w1 + l2 w2 + q11 w1^2 + q12 w1 w2 + q22 w2^2).

    `terms` is an iterable of 6-tuples (z, l1, l2, q11, q12, q22). Use
    coherent_term / tmsv_term to build entries with physical constants folded
    into z (constants never move zeros, but keeping them makes overlaps of the
    same tuples meaningful elsewhere).
    """
    terms = [tuple(complex(x) for x in t) for t in terms]
    if not terms:
        raise ValueError("empty Gaussian sum")

    def f(w1, w2):
        w1 = np.asarray(w1, dtype=complex)
        w2 = np.asarray(w2, dtype=complex)
        out = np.zeros(np.broadcast(w1, w2).shape, dtype=complex)
        for z, l1, l2, q11, q12, q22 in terms:
            out = out + z * np.exp(
                l1 * w1 + l2 * w2 + q11 * w1 * w1 + q12 * w1 * w2 + q22 * w2 * w2
            )
        return out

    return f


def coherent_term(g1, g2, z=1.0):
    """Gaussian-sum term for z |g1, g2> (two-mode coherent)."""
    g1 = complex(g1)
    g2 = complex(g2)
    zc = complex(z) * math.exp(-(abs(g1) ** 2 + abs(g2) ** 2) / 2.0)
    return (zc, g1, g2, 0.0, 0.0, 0.0)


def tmsv_term(lam, z=1.0):
    """Gaussian-sum term for z T(lam) (two-mode squeezed vacuum), |lam| < 1."""
    lam = complex(lam)
    if abs(lam) >= 1.0:
        raise ValueError("TMSV parameter must satisfy |lam| < 1")
    zc = complex(z) * math.sqrt(1.0 - abs(lam) ** 2)
    return (zc, 0.0, 0.0, 0.0, lam, 0.0)


def rotated(f, u):
    """Stellar function in a linearly rotated frame: g(w) = f(U w), U in U(2).

    This is the stellar function of a passively transformed state (up to the
    U-versus-U^T bookkeeping, which no census invariant depends on).
    """
    u = np.asarray(u, dtype=complex)

    def g(w1, w2):
        return f(u[0, 0] * w1 + u[0, 1] * w2, u[1, 0] * w1 + u[1, 1] * w2)

    return g


def random_u2(seed):
    """Haar-ish random U(2) from QR of a seeded complex Gaussian matrix."""
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(a)
    return q * (np.diag(r) / np.abs(np.diag(r)))


# ---------------------------------------------------------------------------
# zero-curve tracing on the Hopf-angle grid
# ---------------------------------------------------------------------------

class TraceError(RuntimeError):
    """Raised when a census attempt is not interpretable (retry another frame)."""


def _wrap(d):
    return (d + math.pi) % TWO_PI - math.pi


def _plaquette_windings(phase, n_eta, n_xi):
    """Integer phase windings of the three plaquette families.

    phase has shape (n_eta + 1, n_xi, n_xi); xi axes periodic.
    Returns (w_eta_normal, w_xi1_normal, w_xi2_normal) integer arrays:
      w_eta_normal[a, b, c]  : face spanned by xi1, xi2 at eta-vertex a
      w_xi1_normal[a, b, c]  : face spanned by eta, xi2 at xi1-vertex b
      w_xi2_normal[a, b, c]  : face spanned by eta, xi1 at xi2-vertex c
    """
    d_eta = _wrap(phase[1:, :, :] - phase[:-1, :, :])
    d_xi1 = _wrap(np.roll(phase, -1, axis=1) - phase)
    d_xi2 = _wrap(np.roll(phase, -1, axis=2) - phase)

    def integerize(total):
        w = total / TWO_PI
        w_int = np.rint(w).astype(int)
        if np.max(np.abs(w - w_int)) > 1e-6:
            raise TraceError("non-integer plaquette winding")
        return w_int

    # face spanned by (xi1, xi2): edges xi1@c, xi2@(b+1), -xi1@(c+1), -xi2@b
    w_en = integerize(
        d_xi1 + np.roll(d_xi2, -1, axis=1) - np.roll(d_xi1, -1, axis=2) - d_xi2
    )
    # face spanned by (eta, xi2): edges eta@b,c, xi2@(a+1), -eta@(c+1), -xi2@a
    w_x1 = integerize(
        d_eta + d_xi2[1:, :, :] - np.roll(d_eta, -1, axis=2) - d_xi2[:-1, :, :]
    )
    # face spanned by (eta, xi1): edges eta@b,c, xi1@(a+1), -eta@(b+1), -xi1@a
    w_x2 = integerize(
        d_eta + d_xi1[1:, :, :] - np.roll(d_eta, -1, axis=1) - d_xi1[:-1, :, :]
    )
    return w_en, w_x1, w_x2


def _face_center(face, etas, xis, d_eta, d_xi):
    axis, a, b, c = face
    if axis == 0:  # spanned by xi1, xi2 at eta-vertex a
        return etas[a], xis[b] + d_xi / 2.0, xis[c] + d_xi / 2.0
    if axis == 1:  # spanned by eta, xi2 at xi1-vertex b
        return etas[a] + d_eta / 2.0, xis[b], xis[c] + d_xi / 2.0
    # axis == 2: spanned by eta, xi1 at xi2-vertex c
    return etas[a] + d_eta / 2.0, xis[b] + d_xi / 2.0, xis[c]


def _cell_faces(a, b, c, n_xi):
    return (
        (0, a, b, c),
        (0, a + 1, b, c),
        (1, a, b, c),
        (1, a, (b + 1) % n_xi, c),
        (2, a, b, c),
        (2, a, b, (c + 1) % n_xi),
    )


def _face_cells(face, n_eta, n_xi):
    axis, a, b, c = face
    if axis == 0:
        cells = []
        if a > 0:
            cells.append((a - 1, b, c))
        if a < n_eta:
            cells.append((a, b, c))
        return cells
    if axis == 1:
        return [(a, (b - 1) % n_xi, c), (a, b, c)]
    return [(a, b, (c - 1) % n_xi), (a, b, c)]


def _trace_loops(w_en, w_x1, w_x2, n_eta, n_xi):
    """Chain pierced faces into closed loops of face ids."""
    if np.any(w_en[0] != 0) or np.any(w_en[-1] != 0):
        raise TraceError("zero curve crosses the eta margin caps")
    if max(np.max(np.abs(w_en)), np.max(np.abs(w_x1)), np.max(np.abs(w_x2))) > 1:
        raise TraceError("|winding| >= 2 on a face (two strands in one plaquette)")

    pierced = {}
    for axis, arr in ((0, w_en), (1, w_x1), (2, w_x2)):
        for a, b, c in zip(*np.nonzero(arr)):
            pierced[(axis, int(a), int(b), int(c))] = int(arr[a, b, c])

    cell_to_faces = {}
    for face in pierced:
        for cell in _face_cells(face, n_eta, n_xi):
            cell_to_faces.setdefault(cell, []).append(face)
    bad = [cell for cell, faces in cell_to_faces.items() if len(faces) != 2]
    if bad:
        raise TraceError(f"{len(bad)} cells with face count != 2 (refine grid)")

    loops = []
    unused = set(pierced)
    while unused:
        start = next(iter(unused))
        loop = [start]
        unused.discard(start)
        cell = _face_cells(start, n_eta, n_xi)[0]
        while True:
            fa, fb = cell_to_faces[cell]
            nxt = fb if fa == loop[-1] else fa
            if nxt == start:
                break
            loop.append(nxt)
            unused.discard(nxt)
            cells = _face_cells(nxt, n_eta, n_xi)
            if len(cells) != 2:
                raise TraceError("curve reached a boundary face")
            cell = cells[1] if cells[0] == cell else cells[0]
        loops.append(loop)
    return loops, pierced


# ---------------------------------------------------------------------------
# geometry on the loops
# ---------------------------------------------------------------------------

def _embed(eta, xi1, xi2, radius):
    w1 = radius * np.cos(eta) * np.exp(1j * xi1)
    w2 = radius * np.sin(eta) * np.exp(1j * xi2)
    return w1, w2


def _grad(f, w1, w2, h):
    d1 = (f(w1 + h, w2) - f(w1 - h, w2)) / (2.0 * h)
    d2 = (f(w1, w2 + h) - f(w1, w2 - h)) / (2.0 * h)
    return d1, d2


def _polish(f, w1, w2, radius, iters, max_step):
    """Newton-polish points onto f = 0, then re-project to the sphere.

    Steps larger than max_step (in C^2 norm) are rejected pointwise: a huge
    step means the local linearization crossed to another strand.
    """
    for _ in range(iters):
        g = f(w1, w2)
        d1, d2 = _grad(f, w1, w2, 1e-5 * radius)
        norm2 = np.abs(d1) ** 2 + np.abs(d2) ** 2
        norm2 = np.where(norm2 == 0.0, 1.0, norm2)
        s1 = -g * np.conj(d1) / norm2
        s2 = -g * np.conj(d2) / norm2
        step = np.sqrt(np.abs(s1) ** 2 + np.abs(s2) ** 2)
        ok = step < max_step
        w1 = np.where(ok, w1 + s1, w1)
        w2 = np.where(ok, w2 + s2, w2)
        scale = radius / np.sqrt(np.abs(w1) ** 2 + np.abs(w2) ** 2)
        w1 = w1 * scale
        w2 = w2 * scale
    return w1, w2


def _orient_boundary(f, w1, w2, radius):
    """Return +1/-1: does point order follow the complex boundary orientation?

    At each loop point the holomorphic tangent of {f=0} is
    u = (-df/dw2, df/dw1); the analytic-piece boundary orientation demands
    that (outward radial, traversal tangent) be positively oriented in the
    oriented real plane (u, iu). Majority vote over the loop, weighted by the
    determinant magnitude, decides; near-degenerate points contribute little.
    """
    d1, d2 = _grad(f, w1, w2, 1e-5 * radius)
    u = np.stack([-d2, d1])                      # (2, N) complex tangent
    nrm = np.sqrt(np.sum(np.abs(u) ** 2, axis=0))
    nrm = np.where(nrm == 0.0, 1.0, nrm)
    u = u / nrm
    w = np.stack([w1, w2])                       # (2, N) points = outward radial
    t = np.roll(w, -1, axis=1) - np.roll(w, 1, axis=1)  # traversal tangent

    def coords(x):
        a = np.real(np.sum(np.conj(u) * x, axis=0))
        b = np.real(np.sum(np.conj(1j * u) * x, axis=0))
        return a, b

    aw, bw = coords(w)
    at, bt = coords(t)
    det = aw * bt - bw * at
    score = float(np.sum(det))
    if score == 0.0:
        raise TraceError("orientation vote degenerate")
    return 1 if score > 0 else -1


def _winding_of(values):
    """Winding number of a closed sequence of nonzero complex values."""
    ang = np.angle(values)
    total = np.sum(_wrap(np.diff(np.concatenate([ang, ang[:1]]))))
    w = total / TWO_PI
    w_int = int(np.rint(w))
    if abs(w - w_int) > 0.25:
        raise TraceError("non-integer core winding")
    return w_int


def _stereographic(points4, pole):
    """Stereographic projection of unit S^3 points from `pole` to R^3.

    The R^3 basis is oriented so that (e1, e2, e3, pole) is positively
    oriented in R^4 — without this the projected frame is mirror-ambiguous
    and linking signs flip pole-by-pole.
    """
    basis = np.linalg.svd(np.eye(4) - np.outer(pole, pole))[0][:, :3]
    if np.linalg.det(np.column_stack([basis, pole])) < 0:
        basis = basis.copy()
        basis[:, 0] = -basis[:, 0]
    dots = points4 @ pole
    if np.max(dots) > 0.99:
        raise TraceError("projection pole too close to a curve")
    return (points4 @ basis) / (1.0 - dots)[:, None]


# Global linking-sign calibration: chosen so that the standard positively
# oriented Hopf pair (e^{it}, 0), (0, e^{is}) measures +1 (pinned by
# tests/test_stellar2.py::test_linking_calibration).
LK_SIGN = 1


def linking_number(pa, pb, seed=0):
    """Signed linking number of two closed polylines in R^3.

    Exact crossing count in a generic planar projection; both over/under
    counts are computed and must agree. Retries a few seeded random rotations
    when the projection is degenerate.
    """
    rng = np.random.default_rng(seed)
    for _ in range(8):
        q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
        if np.linalg.det(q) < 0:
            q[:, 0] = -q[:, 0]
        a = pa @ q
        b = pb @ q
        try:
            lk_ab = _crossing_sum(a, b)
            lk_ba = _crossing_sum(b, a)
        except TraceError:
            continue
        if lk_ab != lk_ba:
            continue
        return LK_SIGN * lk_ab
    raise TraceError("no valid projection found for linking number")


def _crossing_sum(a, b):
    """Sum of crossing signs where polyline a passes OVER polyline b."""
    a2 = np.roll(a, -1, axis=0)
    b2 = np.roll(b, -1, axis=0)
    da = a2 - a
    db = b2 - b
    total = 0
    for i in range(len(a)):
        # segment i of a against all segments of b, in the xy plane
        r = b[:, :2] - a[i, :2]
        denom = da[i, 0] * db[:, 1] - da[i, 1] * db[:, 0]
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (r[:, 0] * db[:, 1] - r[:, 1] * db[:, 0]) / denom
            s = (r[:, 0] * da[i, 1] - r[:, 1] * da[i, 0]) / -denom
        scale = np.abs(denom) / (
            np.linalg.norm(da[i, :2]) * np.linalg.norm(db[:, :2], axis=1) + 1e-300
        )
        hit = (np.abs(denom) > 0) & (t > 0) & (t < 1) & (s > 0) & (s < 1)
        near = hit & (
            (t < 1e-3) | (t > 1 - 1e-3) | (s < 1e-3) | (s > 1 - 1e-3) | (scale < 1e-4)
        )
        if np.any(near):
            raise TraceError("degenerate projection (near-endpoint crossing)")
        if not np.any(hit):
            continue
        za = a[i, 2] + t[hit] * da[i, 2]
        zb = b[hit, 2] + s[hit] * db[hit, 2]
        if np.min(np.abs(za - zb)) < 1e-9:
            raise TraceError("degenerate projection (equal depth)")
        sign = np.sign(denom[hit]).astype(int)
        total += int(np.sum(sign[za > zb]))
    return total


# ---------------------------------------------------------------------------
# the census
# ---------------------------------------------------------------------------

def census(
    f,
    *,
    radius=1.0,
    n_eta=90,
    n_xi=96,
    eta_margin=0.05,
    frame_seed=0,
    max_frame_tries=6,
    polish_iters=3,
    return_loops=False,
):
    """Measure the zero link of stellar function f on the sphere S3_radius.

    Returns a dict with per-component point counts and core windings (in the
    ORIGINAL, un-rotated frame), the signed linking matrix, the frame seed
    that succeeded, and diagnostics. With return_loops=True the dict also
    carries "loops_r3" (stereographic R^3 polylines per component, numpy
    arrays — strip before JSON dumping). Raises TraceError if no frame works.
    """
    last = None
    for attempt in range(max_frame_tries):
        seed = frame_seed + attempt
        try:
            return _census_once(
                f, radius, n_eta, n_xi, eta_margin, seed, polish_iters,
                return_loops,
            )
        except TraceError as err:
            last = err
    raise TraceError(f"census failed after {max_frame_tries} frames: {last}")


def _census_once(f, radius, n_eta, n_xi, eta_margin, seed, polish_iters,
                 return_loops=False):
    u = random_u2(seed)
    g = rotated(f, u)

    etas = np.linspace(eta_margin, math.pi / 2.0 - eta_margin, n_eta + 1)
    xis = np.arange(n_xi) * (TWO_PI / n_xi)
    d_eta = etas[1] - etas[0]
    d_xi = TWO_PI / n_xi

    ee, x1, x2 = np.meshgrid(etas, xis, xis, indexing="ij")
    w1, w2 = _embed(ee, x1, x2, radius)
    vals = g(w1, w2)
    if np.min(np.abs(vals)) == 0.0:
        raise TraceError("exact zero on a grid vertex")
    phase = np.angle(vals)

    w_en, w_x1, w_x2 = _plaquette_windings(phase, n_eta, n_xi)
    loops, _ = _trace_loops(w_en, w_x1, w_x2, n_eta, n_xi)

    # cap heuristic: |g| floor on eta bands beyond the margins
    cap_etas = np.array([eta_margin / 3.0, math.pi / 2.0 - eta_margin / 3.0])
    ce, c1, c2 = np.meshgrid(cap_etas, xis, xis, indexing="ij")
    cw1, cw2 = _embed(ce, c1, c2, radius)
    min_abs_caps = float(np.min(np.abs(g(cw1, cw2))))
    med_abs = float(np.median(np.abs(vals)))

    components = []
    loop_points4 = []
    max_step = 1.5 * math.hypot(d_eta, d_xi) * radius
    for loop in loops:
        cents = np.array([_face_center(fc, etas, xis, d_eta, d_xi) for fc in loop])
        lw1, lw2 = _embed(cents[:, 0], cents[:, 1], cents[:, 2], radius)
        lw1, lw2 = _polish(g, lw1, lw2, radius, polish_iters, max_step)
        if _orient_boundary(g, lw1, lw2, radius) < 0:
            lw1, lw2 = lw1[::-1], lw2[::-1]
        # original-frame coordinates for the core windings; a winding is
        # undefined (None) when the component runs along that core circle
        v = u @ np.stack([lw1, lw2])
        windings = []
        for vi in v:
            if np.min(np.abs(vi)) < 1e-3 * radius:
                windings.append(None)
            else:
                windings.append(_winding_of(vi))
        components.append({"n_points": int(len(loop)), "windings": windings})
        pts = np.stack(
            [np.real(lw1), np.imag(lw1), np.real(lw2), np.imag(lw2)], axis=1
        )
        loop_points4.append(pts / radius)

    n = len(components)
    lk = np.zeros((n, n), dtype=int)
    loops3 = []
    if n > 0:
        pole = _pick_pole(loop_points4, seed)
        loops3 = [_stereographic(p, pole) for p in loop_points4]
        for i in range(n):
            for j in range(i + 1, n):
                val = linking_number(loops3[i], loops3[j], seed=seed)
                lk[i, j] = lk[j, i] = val

    result = {
        "radius": radius,
        "grid": {"n_eta": n_eta, "n_xi": n_xi, "eta_margin": eta_margin},
        "frame_seed_used": seed,
        "components": components,
        "linking_matrix": lk.tolist(),
        "diagnostics": {
            "min_abs_on_caps": min_abs_caps,
            "median_abs_on_grid": med_abs,
            "caps_clear": bool(min_abs_caps > 1e-3 * med_abs),
            "min_component_points": int(min((c["n_points"] for c in components), default=0)),
        },
    }
    if return_loops:
        result["loops_r3"] = loops3
    return result


def _pick_pole(loop_points4, seed):
    rng = np.random.default_rng(seed)
    allpts = np.concatenate(loop_points4)
    best, best_d = None, -1.0
    for _ in range(32):
        p = rng.normal(size=4)
        p /= np.linalg.norm(p)
        d = float(np.min(np.linalg.norm(allpts - p, axis=1)))
        if d > best_d:
            best, best_d = p, d
    if best_d < 0.1:
        raise TraceError("no good projection pole")
    return best
