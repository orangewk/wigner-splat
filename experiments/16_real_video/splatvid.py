"""Real-video splatting for issue #48 Phase 1 (numpy only).

Extends the exp15 renderer (isotropic signed 3D Gaussians, ADDITIVE
emission, pinhole + paraxial footprints -- same declared simplifications)
with what real hand-held video needs:

  * a global constant background b (real frames don't start from 0);
  * the eta-style BLUR KNOB: one global PSF scale sigma_b = exp(s_blur),
    composed with each footprint in CLOSED FORM -- a Gaussian splat blurred
    by a normalized Gaussian PSF is again a Gaussian:
        si^2 = a^2 + sigma_b^2,   amplitude factor a^2 / si^2,
    with a = f * exp(s) / z the unblurred footprint scale (exp13's "model
    the corruption inside the forward model with one knob", exported);
  * CAMERA POSE GRADIENTS for joint pose+splat fitting (no COLMAP in this
    environment). Both are closed form: translation dL/dc = -sum_k g_mu_k
    (translation symmetry), rotation (left perturbation R <- exp([d]x) R)
    dL/dd = sum_k p_k x gp_k; plus a global log-focal gradient.

With s_blur = None the model reduces exactly to the exp15 renderer plus
background. All gradients are pinned against central differences in
tests/test_splatvid.py.
"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]
                       / "15_video_conf"))
from gauss3d import _Z_MIN, make_camera, spearman  # noqa: F401,E402


def _footprints(mu, s, cam, s_blur):
    """Projection + blurred footprint pieces shared by value and grad."""
    p = (mu - cam["c"]) @ cam["R"].T
    z = p[:, 2]
    vis = z > _Z_MIN
    zs = np.where(vis, z, 1.0)
    f = cam["f"]
    u0 = f * p[:, 0] / zs + cam["cx"]
    v0 = f * p[:, 1] / zs + cam["cy"]
    a = f * np.exp(s) / zs
    sb = 0.0 if s_blur is None else np.exp(s_blur)
    si = np.sqrt(a ** 2 + sb ** 2)
    return p, zs, vis, u0, v0, a, sb, si


def render(mu, s, w, b, cam, s_blur=None):
    """Forward render: flattened (H*W,) image."""
    _, _, vis, u0, v0, a, _, si = _footprints(mu, s, cam, s_blur)
    du = cam["U"][None, :] - u0[:, None]
    dv = cam["V"][None, :] - v0[:, None]
    amp = (a / si) ** 2
    e = amp[:, None] * np.exp(-0.5 * (du ** 2 + dv ** 2) / si[:, None] ** 2)
    e[~vis] = 0.0
    return w @ e + b


def render_and_grad(mu, s, w, b, cam, target, s_blur=None):
    """Per-frame MSE loss, image, and analytic gradients.

    Returns (loss, image, grads) with grads for the splats ('mu' (K,3),
    's' (K,), 'w' (K,)), the background 'b', the pose ('c' (3,), 'rot'
    (3,) -- axis-angle left perturbation of R at identity), the global
    'logf', and 's_blur' (None when the knob is off).
    """
    p, zs, vis, u0, v0, a, sb, si = _footprints(mu, s, cam, s_blur)
    f = cam["f"]
    du = cam["U"][None, :] - u0[:, None]
    dv = cam["V"][None, :] - v0[:, None]
    r2px = (du ** 2 + dv ** 2) / si[:, None] ** 2   # rho
    G = np.exp(-0.5 * r2px)
    amp = (a / si) ** 2
    e = amp[:, None] * G
    e[~vis] = 0.0
    image = w @ e + b
    r = image - target
    n = len(cam["U"])
    loss = float(np.mean(r ** 2))
    r2 = (2.0 / n) * r

    g_w = e @ r2
    we = w[:, None] * e
    inv2 = 1.0 / si[:, None] ** 2
    Su = (we * du * inv2) @ r2                       # dL/du0
    Sv = (we * dv * inv2) @ r2                       # dL/dv0
    # dL/dsi at fixed a: e * (-2/si + rho/si)
    T = (we * (r2px - 2.0) / si[:, None]) @ r2
    E = w * (e @ r2)                                  # sum r2 * w * e
    # dL/da = (2/a) E + T * (a/si)
    dLda = np.where(vis, 2.0 * E / np.where(vis, a, 1.0) + T * a / si, 0.0)

    gp = np.stack([
        f / zs * Su,
        f / zs * Sv,
        -f / zs ** 2 * (p[:, 0] * Su + p[:, 1] * Sv) - a / zs * dLda,
    ], axis=1)
    gp[~vis] = 0.0
    g_mu = gp @ cam["R"]
    g_s = np.where(vis, dLda * a, 0.0)
    g_b = float(np.sum(r2))
    g_c = -np.sum(g_mu, axis=0)
    g_rot = np.sum(np.cross(p, gp), axis=0)
    g_logf = float(np.sum(np.where(vis, Su * (u0 - cam["cx"])
                                   + Sv * (v0 - cam["cy"])
                                   + dLda * a, 0.0)))
    grads = {"mu": g_mu, "s": g_s, "w": g_w, "b": g_b, "c": g_c,
             "rot": g_rot, "logf": g_logf, "s_blur": None}
    if s_blur is not None:
        grads["s_blur"] = float(np.sum(np.where(vis, T * sb / si, 0.0)) * sb)
    return loss, image, grads


def rot_exp(d):
    """SO(3) exponential of an axis-angle vector (Rodrigues)."""
    th = np.linalg.norm(d)
    if th < 1e-12:
        return np.eye(3)
    k = d / th
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * (K @ K)


def frame_jacobian(mu, s, w, b, cam, s_blur=None):
    """Per-pixel Jacobian dImage/dtheta over the SPLAT parameters + b:
    (H*W, 5K + 1), order [mu(3), s, w] per splat, then b. Poses and the
    global knobs are held fixed (declared in the Phase 1 protocol)."""
    K = len(w)
    p, zs, vis, u0, v0, a, sb, si = _footprints(mu, s, cam, s_blur)
    f = cam["f"]
    du = cam["U"][None, :] - u0[:, None]
    dv = cam["V"][None, :] - v0[:, None]
    r2px = (du ** 2 + dv ** 2) / si[:, None] ** 2
    G = np.exp(-0.5 * r2px)
    amp = (a / si) ** 2
    e = amp[:, None] * G
    e[~vis] = 0.0
    n = len(cam["U"])
    J = np.zeros((n, 5 * K + 1))
    for k in range(K):
        if not vis[k]:
            continue
        dMdu0 = w[k] * e[k] * du[k] / si[k] ** 2
        dMdv0 = w[k] * e[k] * dv[k] / si[k] ** 2
        # dM/da (total) = w e [2/a + (rho - 2)/si * (a/si)]
        dMda = w[k] * e[k] * (2.0 / a[k]
                              + (r2px[k] - 2.0) / si[k] * (a[k] / si[k]))
        Jp = np.stack([
            f / zs[k] * dMdu0,
            f / zs[k] * dMdv0,
            -f / zs[k] ** 2 * (p[k, 0] * dMdu0 + p[k, 1] * dMdv0)
            - a[k] / zs[k] * dMda,
        ], axis=1)
        J[:, 5 * k:5 * k + 3] = Jp @ cam["R"]
        J[:, 5 * k + 3] = dMda * a[k]
        J[:, 5 * k + 4] = e[k]
    J[:, 5 * K] = 1.0  # background
    return J
