"""Minimal signed 3D Gaussian splatting with analytic gradients (numpy only).

Core module for issue #48 Phase 0 (confidence certificate for few-view
reconstruction). Deliberate simplifications, declared on the issue before
implementation:

  * ISOTROPIC 3D Gaussians: mu in R^3, one log-scale s, SIGNED weight w.
  * ADDITIVE emission imaging (X-ray / emission style): a frame is the sum
    of projected 2D Gaussian footprints. No alpha compositing, no occlusion.
  * Pinhole projection, paraxial footprint: projected center
    (u0, v0) = f * (px, py) / pz + (cx, cy), projected scale
    sigma_img = f * sigma / pz, footprint exp(-r^2 / (2 sigma_img^2)).

The physics that survives the simplification -- and that Phase 0 tests --
is the monocular SIZE-DISTANCE DEGENERACY: a single view constrains only
sigma / pz, so depth and scale trade off exactly until parallax breaks the
degeneracy. `probe_information` turns that into a closed-form per-point
confidence score (Gauss-Newton information of a hypothetical unit probe
splat -- the 3D sibling of the 2D demo's birth field, one derivative up).

Everything analytic; gradients and the information matrix are pinned
against finite differences in tests/test_gauss3d.py.
"""
import numpy as np

_Z_MIN = 0.2  # splats at or behind this camera depth contribute nothing


def make_camera(c, look_at, f, shape, up=(0.0, 1.0, 0.0)):
    """Pinhole camera at position c looking at point look_at.

    Returns a dict with rotation R (world->camera rows: right, up, forward),
    position c, focal f (pixels), principal point, and flattened pixel-center
    coordinate arrays U, V for the (H, W) image.
    """
    c = np.asarray(c, float)
    fwd = np.asarray(look_at, float) - c
    fwd = fwd / np.linalg.norm(fwd)
    right = np.cross(fwd, np.asarray(up, float))
    right = right / np.linalg.norm(right)
    upv = np.cross(right, fwd)
    R = np.stack([right, upv, fwd])
    H, W = shape
    vs, us = np.meshgrid(np.arange(H, dtype=float),
                         np.arange(W, dtype=float), indexing="ij")
    return {"R": R, "c": c, "f": float(f), "cx": (W - 1) / 2.0,
            "cy": (H - 1) / 2.0, "shape": (H, W),
            "U": us.ravel(), "V": vs.ravel()}


def _project(mu, cam):
    """Camera-frame points, projected centers and per-splat visibility."""
    p = (mu - cam["c"]) @ cam["R"].T
    z = p[:, 2]
    vis = z > _Z_MIN
    zs = np.where(vis, z, 1.0)  # placeholder depth; masked out downstream
    u0 = cam["f"] * p[:, 0] / zs + cam["cx"]
    v0 = cam["f"] * p[:, 1] / zs + cam["cy"]
    return p, zs, vis, u0, v0


def render(mu, s, w, cam):
    """Forward render: flattened (H*W,) image of the K splats."""
    p, zs, vis, u0, v0 = _project(mu, cam)
    si = cam["f"] * np.exp(s) / zs
    du = cam["U"][None, :] - u0[:, None]
    dv = cam["V"][None, :] - v0[:, None]
    G = np.exp(-0.5 * (du ** 2 + dv ** 2) / si[:, None] ** 2)
    G[~vis] = 0.0
    return w @ G


def render_and_grad(mu, s, w, cam, target):
    """Per-frame MSE loss, image, and analytic gradients for all K splats.

    mu (K,3), s (K,) log-scales, w (K,) signed weights; target (H*W,).
    Returns (loss, image, grads dict with 'mu' (K,3), 's' (K,), 'w' (K,)).
    """
    p, zs, vis, u0, v0 = _project(mu, cam)
    f = cam["f"]
    si = f * np.exp(s) / zs
    du = cam["U"][None, :] - u0[:, None]
    dv = cam["V"][None, :] - v0[:, None]
    rho = (du ** 2 + dv ** 2) / si[:, None] ** 2
    G = np.exp(-0.5 * rho)
    G[~vis] = 0.0
    image = w @ G
    r = image - target
    n = len(cam["U"])
    loss = float(np.mean(r ** 2))

    r2 = (2.0 / n) * r
    g_w = G @ r2
    wG = w[:, None] * G
    inv2 = 1.0 / si[:, None] ** 2
    Su = (wG * du * inv2) @ r2          # dL/du0 per splat
    Sv = (wG * dv * inv2) @ r2          # dL/dv0
    Ssig = (wG * rho / si[:, None]) @ r2  # dL/dsigma_img
    gp = np.stack([
        f / zs * Su,
        f / zs * Sv,
        -f / zs ** 2 * (p[:, 0] * Su + p[:, 1] * Sv) - si / zs * Ssig,
    ], axis=1)
    gp[~vis] = 0.0
    g_mu = gp @ cam["R"]                # g_mu = R^T g_p, row-wise
    g_s = np.where(vis, Ssig * si, 0.0)  # dsigma_img/ds = sigma_img
    return loss, image, {"mu": g_mu, "s": g_s, "w": g_w}


def probe_information(x, sigma_p, cams):
    """Gauss-Newton information matrix of a unit probe splat at position x.

    The probe has parameters theta = (mu / sigma_p, s, w) -- position
    nondimensionalized by the probe scale so the 5x5 matrix
    H = sum_cams sum_pixels J J^T is comparable across directions. The
    CONFIDENCE score used in Phase 0 is lambda_min(H): the worst-constrained
    parameter direction. It sees only camera geometry -- never the video
    data, never the ground truth. Footprints are evaluated on a +-6
    sigma_img crop (truncation < 1e-8 relative).
    """
    x = np.asarray(x, float)
    H5 = np.zeros((5, 5))
    for cam in cams:
        p = cam["R"] @ (x - cam["c"])
        z = p[2]
        if z <= _Z_MIN:
            continue
        f = cam["f"]
        u0 = f * p[0] / z + cam["cx"]
        v0 = f * p[1] / z + cam["cy"]
        si = f * sigma_p / z
        Himg, Wimg = cam["shape"]
        half = 6.0 * si
        ulo, uhi = int(max(0, np.floor(u0 - half))), int(
            min(Wimg - 1, np.ceil(u0 + half)))
        vlo, vhi = int(max(0, np.floor(v0 - half))), int(
            min(Himg - 1, np.ceil(v0 + half)))
        if ulo > uhi or vlo > vhi:
            continue
        uu, vv = np.meshgrid(np.arange(ulo, uhi + 1, dtype=float),
                             np.arange(vlo, vhi + 1, dtype=float))
        du = (uu - u0).ravel()
        dv = (vv - v0).ravel()
        rho = (du ** 2 + dv ** 2) / si ** 2
        G = np.exp(-0.5 * rho)
        Ju0 = G * du / si ** 2
        Jv0 = G * dv / si ** 2
        Jsi = G * rho / si
        Jp = np.stack([
            f / z * Ju0,
            f / z * Jv0,
            -f / z ** 2 * (p[0] * Ju0 + p[1] * Jv0) - si / z * Jsi,
        ], axis=1)
        Jmu = Jp @ cam["R"]
        Jn = np.concatenate([Jmu * sigma_p, (Jsi * si)[:, None],
                             G[:, None]], axis=1)
        H5 += Jn.T @ Jn
    return H5


def density3d(pts, mu, s, w):
    """Signed 3D mixture density at pts (N,3)."""
    d2 = np.sum((pts[:, None, :] - mu[None, :, :]) ** 2, axis=2)
    return np.exp(-0.5 * d2 / np.exp(2 * s)[None, :]) @ w


def frame_jacobian(mu, s, w, cam):
    """Per-pixel Jacobian dImage/dtheta, theta = (mu(3), s, w) per splat.

    Returns (H*W, 5K) with parameter order [mu_x, mu_y, mu_z, s, w] blocked
    by splat. Same projection model as render_and_grad; splats behind the
    camera contribute zero columns.
    """
    K = len(w)
    p, zs, vis, u0, v0 = _project(mu, cam)
    f = cam["f"]
    si = f * np.exp(s) / zs
    du = cam["U"][None, :] - u0[:, None]
    dv = cam["V"][None, :] - v0[:, None]
    rho = (du ** 2 + dv ** 2) / si[:, None] ** 2
    G = np.exp(-0.5 * rho)
    G[~vis] = 0.0
    n = len(cam["U"])
    J = np.zeros((n, 5 * K))
    for k in range(K):
        if not vis[k]:
            continue
        dMdu0 = w[k] * G[k] * du[k] / si[k] ** 2
        dMdv0 = w[k] * G[k] * dv[k] / si[k] ** 2
        dMdsi = w[k] * G[k] * rho[k] / si[k]
        Jp = np.stack([
            f / zs[k] * dMdu0,
            f / zs[k] * dMdv0,
            -f / zs[k] ** 2 * (p[k, 0] * dMdu0 + p[k, 1] * dMdv0)
            - si[k] / zs[k] * dMdsi,
        ], axis=1)
        J[:, 5 * k:5 * k + 3] = Jp @ cam["R"]
        J[:, 5 * k + 3] = dMdsi * si[k]
        J[:, 5 * k + 4] = G[k]
    return J


def model_gn(params, cams):
    """Gauss-Newton matrix of the FITTED model over all frames:
    H = sum_frames J^T J, (5K, 5K)."""
    K = len(params["w"])
    H = np.zeros((5 * K, 5 * K))
    for cam in cams:
        J = frame_jacobian(params["mu"], params["s"], params["w"], cam)
        H += J.T @ J
    return H


def density_grad(pts, mu, s, w):
    """d density3d / d theta at pts (N,3): returns (N, 5K), same parameter
    order as frame_jacobian."""
    N, K = len(pts), len(w)
    d = pts[:, None, :] - mu[None, :, :]           # (N, K, 3)
    sig2 = np.exp(2 * s)[None, :]
    d2 = np.sum(d ** 2, axis=2)
    g = np.exp(-0.5 * d2 / sig2)                   # (N, K)
    out = np.zeros((N, 5 * K))
    for k in range(K):
        out[:, 5 * k:5 * k + 3] = (w[k] * g[:, k] / sig2[0, k])[:, None] \
            * d[:, k, :]
        out[:, 5 * k + 3] = w[k] * g[:, k] * d2[:, k] / sig2[0, k]
        out[:, 5 * k + 4] = g[:, k]
    return out


def predicted_sigma(pts, params, cams, eps_frac=1e-9, H=None):
    """Score v2 (issue #48 round 2, declared before running): delta-method
    predicted uncertainty of the fitted density,

        sigma_pred(x)^2 = J_rho(x)^T (H + eps I)^{-1} J_rho(x),

    H = model_gn over all frames, eps = eps_frac * tr(H) / P. Sees the
    video (through the fit and H) and the model -- never the ground truth.
    Degenerate parameter directions blow sigma_pred up through H's null
    space; coupling to model amplitude enters through J_rho.
    """
    if H is None:
        H = model_gn(params, cams)
    P = H.shape[0]
    eps = eps_frac * np.trace(H) / P
    Jr = density_grad(pts, params["mu"], params["s"], params["w"])
    Hi_Jr = np.linalg.solve(H + eps * np.eye(P), Jr.T)
    return np.sqrt(np.maximum(np.sum(Jr.T * Hi_Jr, axis=0), 0.0))


def fit(frames, cams, K, iters=2000, lr=0.03, seed=0,
        init_box=((-2.5, 2.5), (-2.5, 2.5), (2.5, 9.5)), s_init=None):
    """Adam fit of K splats to the frame stack (list of flattened images).

    Fixed K (no densification -- growth rules are out of Phase 0 scope).
    Returns (params dict, per-iteration mean-over-frames losses).
    """
    rng = np.random.default_rng(seed)
    lo = np.array([b[0] for b in init_box])
    hi = np.array([b[1] for b in init_box])
    mu = rng.uniform(lo, hi, (K, 3))
    s = np.full(K, np.log(0.5) if s_init is None else s_init)
    w = 0.1 * rng.uniform(-1.0, 1.0, K)
    m = {k: (np.zeros(v.shape), np.zeros(v.shape))
         for k, v in (("mu", mu), ("s", s), ("w", w))}
    F = len(frames)
    losses = []
    for it in range(1, iters + 1):
        g = {"mu": np.zeros_like(mu), "s": np.zeros_like(s),
             "w": np.zeros_like(w)}
        loss = 0.0
        for frame, cam in zip(frames, cams):
            lf, _, gf = render_and_grad(mu, s, w, cam, frame)
            loss += lf / F
            for k in g:
                g[k] += gf[k] / F
        losses.append(loss)
        params = {"mu": mu, "s": s, "w": w}
        for k in params:
            m1, m2 = m[k]
            m1[:] = 0.9 * m1 + 0.1 * g[k]
            m2[:] = 0.999 * m2 + 0.001 * g[k] ** 2
            params[k] -= lr * (m1 / (1 - 0.9 ** it)) / (
                np.sqrt(m2 / (1 - 0.999 ** it)) + 1e-8)
    return {"mu": mu, "s": s, "w": w}, losses


def _rank_avg(x):
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x))
    sx = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and sx[j + 1] == sx[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j)
        i = j + 1
    return ranks


def spearman(a, b):
    """Spearman rank correlation (tie-aware average ranks, no scipy)."""
    ra, rb = _rank_avg(np.asarray(a, float)), _rank_avg(np.asarray(b, float))
    ra -= ra.mean()
    rb -= rb.mean()
    return float((ra @ rb) / np.sqrt((ra @ ra) * (rb @ rb)))
