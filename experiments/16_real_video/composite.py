"""Sorted alpha compositing renderer for exp16 round 2 (issue #48).

Round 1's DNF left a working diagnosis: the ADDITIVE renderer cannot dim
what is behind an occluder. This module is the test. Same isotropic
Gaussians, same pinhole/paraxial footprints, same closed-form blur knob
as splatvid.py, but pixels now composite front-to-back (standard 3DGS):

    a_k(px)  = alpha_k * A_k * G_k(px)          per-splat pixel opacity
    T_k(px)  = prod_{j<k} (1 - a_j(px))         transmittance (depth order)
    I(px)    = sum_k c_k a_k T_k + b * T_end    background composited last

with alpha_k = ALPHA_MAX * sigmoid(o_k) (capped away from 1 for stable
1/(1-a) terms), c_k a SIGNED intensity, A_k = a_f^2 / si^2 the blur
amplitude factor and G_k the unit-peak footprint (splatvid's pieces).
Splats are depth-sorted per frame by center depth (the usual 3DGS
approximation).

Analytic gradients throughout -- dI/da_k = c_k T_k - S_k / (1 - a_k)
with S_k the light arriving from behind k -- including the camera pose,
log-focal, background, and blur-knob gradients, so the round-1 joint
fitting machinery (jointfit.py) drives this renderer unchanged. All
pinned against central differences in tests/test_composite.py.
"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from splatvid import _footprints  # noqa: E402

ALPHA_MAX = 0.995


def _pieces(mu, s, o, cam, s_blur):
    p, zs, vis, u0, v0, af, sb, si = _footprints(mu, s, cam, s_blur)
    order = np.argsort(zs)                      # front-to-back
    du = cam["U"][None, :] - u0[:, None]
    dv = cam["V"][None, :] - v0[:, None]
    rho = (du ** 2 + dv ** 2) / si[:, None] ** 2
    G = np.exp(-0.5 * rho)
    amp = (af / si) ** 2
    e = amp[:, None] * G                        # geometric footprint
    e[~vis] = 0.0
    alpha = ALPHA_MAX / (1.0 + np.exp(-o))
    a = alpha[:, None] * e                      # per-splat pixel opacity
    return (p, zs, vis, u0, v0, af, sb, si, du, dv, rho, e, alpha, a,
            order)


def _composite(w, b, a, order):
    ao = a[order]
    T = np.ones_like(ao)
    np.cumprod(1.0 - ao[:-1], axis=0, out=T[1:])
    contrib = w[order][:, None] * ao * T
    T_end = T[-1] * (1.0 - ao[-1])
    image = contrib.sum(axis=0) + b * T_end
    return image, T, contrib, T_end


def render(mu, s, w, b, cam, s_blur=None, o=None):
    """Forward render; signature mirrors splatvid.render plus opacity
    logits o (required here)."""
    pieces = _pieces(mu, s, o, cam, s_blur)
    a, order = pieces[13], pieces[14]
    image, _, _, _ = _composite(w, b, a, order)
    return image


def render_and_grad(mu, s, w, b, cam, target, s_blur=None, o=None):
    """Loss, image, and analytic gradients (adds 'o' to splatvid's set)."""
    (p, zs, vis, u0, v0, af, sb, si, du, dv, rho, e, alpha, a,
     order) = _pieces(mu, s, o, cam, s_blur)
    K = len(w)
    image, T, contrib, T_end = _composite(w, b, a, order)
    r = image - target
    n = len(cam["U"])
    loss = float(np.mean(r ** 2))
    r2 = (2.0 / n) * r

    ao = a[order]
    wo = w[order]
    # S_k = light from behind k = sum_{m>k} contrib_m + b T_end
    rev = np.cumsum(contrib[::-1], axis=0)[::-1]
    S = rev - contrib + b * T_end
    dIda_o = wo[:, None] * T - S / (1.0 - ao)   # per pixel, sorted order
    W_o = r2[None, :] * dIda_o                  # dL/da_k(px), sorted
    inv = np.empty(K, dtype=int)
    inv[order] = np.arange(K)
    W = W_o[inv]                                 # back to original order

    g_w = (a * r2[None, :] * T[inv]).sum(axis=1)
    dalpha_do = alpha * (1.0 - alpha / ALPHA_MAX)
    g_o = (W * e).sum(axis=1) * dalpha_do
    g_b = float(np.sum(r2 * T_end))

    w_eff = W * alpha[:, None]                   # chain onto e
    base = w_eff * e
    inv2 = 1.0 / si[:, None] ** 2
    Su = (base * du * inv2).sum(axis=1)
    Sv = (base * dv * inv2).sum(axis=1)
    Tf = (base * (rho - 2.0) / si[:, None]).sum(axis=1)  # dL/dsi | af
    E = base.sum(axis=1)
    dLda_f = np.where(vis, 2.0 * E / np.where(vis, af, 1.0)
                      + Tf * af / si, 0.0)
    f = cam["f"]
    gp = np.stack([
        f / zs * Su,
        f / zs * Sv,
        -f / zs ** 2 * (p[:, 0] * Su + p[:, 1] * Sv) - af / zs * dLda_f,
    ], axis=1)
    gp[~vis] = 0.0
    g_mu = gp @ cam["R"]
    g_s = np.where(vis, dLda_f * af, 0.0)
    g_c = -np.sum(g_mu, axis=0)
    g_rot = np.sum(np.cross(p, gp), axis=0)
    g_logf = float(np.sum(np.where(vis, Su * (u0 - cam["cx"])
                                   + Sv * (v0 - cam["cy"])
                                   + dLda_f * af, 0.0)))
    grads = {"mu": g_mu, "s": g_s, "w": g_w, "o": g_o, "b": g_b,
             "c": g_c, "rot": g_rot, "logf": g_logf, "s_blur": None}
    if s_blur is not None:
        grads["s_blur"] = float(np.sum(np.where(vis, Tf * sb / si, 0.0))
                                * sb)
    return loss, image, grads


def frame_jacobian(mu, s, w, b, cam, s_blur=None, o=None):
    """Per-pixel dImage/dtheta over splat params + b: (H*W, 6K + 1),
    order [mu(3), s, w, o] per splat then b. Poses/global knobs fixed."""
    (p, zs, vis, u0, v0, af, sb, si, du, dv, rho, e, alpha, a,
     order) = _pieces(mu, s, o, cam, s_blur)
    K = len(w)
    _, T, contrib, T_end = _composite(w, b, a, order)
    ao = a[order]
    wo = w[order]
    rev = np.cumsum(contrib[::-1], axis=0)[::-1]
    S = rev - contrib + b * T_end
    dIda_o = wo[:, None] * T - S / (1.0 - ao)
    inv = np.empty(K, dtype=int)
    inv[order] = np.arange(K)
    dIda = dIda_o[inv]
    Tinv = T[inv]
    dalpha_do = alpha * (1.0 - alpha / ALPHA_MAX)
    f = cam["f"]

    n = len(cam["U"])
    J = np.zeros((n, 6 * K + 1))
    for k in range(K):
        if not vis[k]:
            continue
        wk = dIda[k] * alpha[k]                  # dI/de_k per pixel
        dedu0 = e[k] * du[k] / si[k] ** 2
        dedv0 = e[k] * dv[k] / si[k] ** 2
        deda_f = e[k] * (2.0 / af[k]
                         + (rho[k] - 2.0) / si[k] * (af[k] / si[k]))
        Jp = np.stack([
            f / zs[k] * wk * dedu0,
            f / zs[k] * wk * dedv0,
            -f / zs[k] ** 2 * (p[k, 0] * wk * dedu0
                               + p[k, 1] * wk * dedv0)
            - af[k] / zs[k] * wk * deda_f,
        ], axis=1)
        J[:, 6 * k:6 * k + 3] = Jp @ cam["R"]
        J[:, 6 * k + 3] = wk * deda_f * af[k]
        J[:, 6 * k + 4] = a[k] * Tinv[k]
        J[:, 6 * k + 5] = dIda[k] * e[k] * dalpha_do[k]
    J[:, 6 * K] = T_end
    return J
