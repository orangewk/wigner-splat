"""Pins for the exp16 round-2 alpha-compositing renderer.

Same discipline as test_splatvid: central-difference pins for EVERY
analytic gradient, a brute-force per-pixel Jacobian check, plus the two
physical sanity checks that distinguish compositing from the additive
round-1 renderer: occlusion (an opaque front splat hides a back splat)
and the small-alpha additive limit.
"""
import importlib.util
import pathlib

import numpy as np
import pytest

_here = pathlib.Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cp = _load("composite", _here / "experiments" / "16_real_video"
           / "composite.py")
sv = _load("splatvid", _here / "experiments" / "16_real_video"
           / "splatvid.py")


def _problem(seed=13, K=4, img=16):
    rng = np.random.default_rng(seed)
    cam = sv.make_camera((0.15, -0.1, 0.0), (0.0, 0.0, 5.0), 18.0,
                         (img, img))
    mu = np.column_stack([rng.uniform(-1, 1, (K, 2)),
                          rng.uniform(3.0, 7.0, K)])
    s = rng.uniform(-1.0, -0.3, K)
    w = rng.normal(size=K)
    o = rng.uniform(-1.5, 1.5, K)
    b = 0.42
    s_blur = -0.8
    target = rng.normal(size=img * img)
    return mu, s, w, o, b, cam, target, s_blur


def test_all_gradients_match_central_difference():
    mu, s, w, o, b, cam, T, s_blur = _problem()
    _, _, g = cp.render_and_grad(mu, s, w, b, cam, T, s_blur=s_blur, o=o)
    eps = 1e-6

    def loss_of(mu2=None, s2=None, w2=None, o2=None, b2=None, c2=None,
                d=None, logf2=None, sb2=None):
        cam2 = dict(cam)
        if c2 is not None:
            cam2["c"] = c2
        if d is not None:
            cam2["R"] = sv.rot_exp(d) @ cam["R"]
        if logf2 is not None:
            cam2["f"] = float(np.exp(logf2))
        L, _, _ = cp.render_and_grad(
            mu if mu2 is None else mu2, s if s2 is None else s2,
            w if w2 is None else w2, b if b2 is None else b2, cam2, T,
            s_blur=s_blur if sb2 is None else sb2,
            o=o if o2 is None else o2)
        return L

    K = len(w)
    for k in range(K):
        for j in range(3):
            m2 = mu.copy(); m2[k, j] += eps
            m3 = mu.copy(); m3[k, j] -= eps
            fd = (loss_of(mu2=m2) - loss_of(mu2=m3)) / (2 * eps)
            assert g["mu"][k, j] == pytest.approx(fd, rel=2e-4, abs=1e-9)
        for key, vec, gk in (("s2", s, "s"), ("w2", w, "w"),
                             ("o2", o, "o")):
            v2 = vec.copy(); v2[k] += eps
            v3 = vec.copy(); v3[k] -= eps
            fd = (loss_of(**{key: v2}) - loss_of(**{key: v3})) / (2 * eps)
            assert g[gk][k] == pytest.approx(fd, rel=2e-4, abs=1e-9)
    fd = (loss_of(b2=b + eps) - loss_of(b2=b - eps)) / (2 * eps)
    assert g["b"] == pytest.approx(fd, rel=2e-4, abs=1e-9)
    for j in range(3):
        cpp = cam["c"].copy(); cpp[j] += eps
        cmm = cam["c"].copy(); cmm[j] -= eps
        fd = (loss_of(c2=cpp) - loss_of(c2=cmm)) / (2 * eps)
        assert g["c"][j] == pytest.approx(fd, rel=2e-4, abs=1e-9)
        dp = np.zeros(3); dp[j] = eps
        dm = np.zeros(3); dm[j] = -eps
        fd = (loss_of(d=dp) - loss_of(d=dm)) / (2 * eps)
        assert g["rot"][j] == pytest.approx(fd, rel=2e-4, abs=1e-9)
    lf = np.log(cam["f"])
    fd = (loss_of(logf2=lf + eps) - loss_of(logf2=lf - eps)) / (2 * eps)
    assert g["logf"] == pytest.approx(fd, rel=2e-4, abs=1e-9)
    fd = (loss_of(sb2=s_blur + eps) - loss_of(sb2=s_blur - eps)) / (2 * eps)
    assert g["s_blur"] == pytest.approx(fd, rel=2e-4, abs=1e-9)


def test_frame_jacobian_matches_render_fd():
    mu, s, w, o, b, cam, _, s_blur = _problem(seed=6, K=2, img=12)
    J = cp.frame_jacobian(mu, s, w, b, cam, s_blur=s_blur, o=o)
    eps = 1e-6
    K = len(w)
    for i in range(6 * K + 1):
        def img(delta, i=i):
            mu2, s2, w2, o2, b2 = (mu.copy(), s.copy(), w.copy(),
                                   o.copy(), b)
            if i == 6 * K:
                b2 += delta
            else:
                k, j = divmod(i, 6)
                if j < 3:
                    mu2[k, j] += delta
                elif j == 3:
                    s2[k] += delta
                elif j == 4:
                    w2[k] += delta
                else:
                    o2[k] += delta
            return cp.render(mu2, s2, w2, b2, cam, s_blur=s_blur, o=o2)
        col_fd = (img(eps) - img(-eps)) / (2 * eps)
        assert np.max(np.abs(J[:, i] - col_fd)) < 2e-5 * max(
            1e-6, np.max(np.abs(col_fd)))


def test_opaque_front_splat_occludes_back_splat():
    """The physics round 1 lacked: what is behind an occluder is dimmed."""
    cam = sv.make_camera((0.0, 0.0, 0.0), (0.0, 0.0, 5.0), 40.0, (32, 32))
    mu = np.array([[0.0, 0.0, 4.0],     # front
                   [0.0, 0.0, 8.0]])    # back, same line of sight
    s = np.log(np.array([0.6, 0.6]))
    w = np.array([0.2, 1.0])
    center = 32 * 16 + 16
    # back splat alone (front fully transparent)
    img_open = cp.render(mu, s, w, 0.0, cam, o=np.array([-30.0, 8.0]))
    # front splat nearly opaque
    img_hidden = cp.render(mu, s, w, 0.0, cam, o=np.array([8.0, 8.0]))
    back_contrib_open = img_open[center]
    assert back_contrib_open > 0.5          # back splat clearly visible
    assert abs(img_hidden[center] - 0.2 * cp.ALPHA_MAX) < 0.05
    # additive round-1 renderer CANNOT do this: contributions just add
    img_add = sv.render(mu, s, w, 0.0, cam)
    assert img_add[center] > 1.0


def test_small_alpha_limit_is_additive():
    """alpha -> 0: to first order in a, I = b + sum a_k (c_k - b) -- the
    additive model with effective weights (c - b) * alpha, because even a
    faint splat OCCLUDES the background behind it (the term the additive
    renderer lacks)."""
    mu, s, w, o, b, cam, _, _ = _problem(seed=2, K=3)
    o_tiny = np.full(3, -9.0)
    alpha = cp.ALPHA_MAX / (1.0 + np.exp(-o_tiny))
    img_comp = cp.render(mu, s, w, b, cam, o=o_tiny)
    img_add = sv.render(mu, s, (w - b) * alpha, b, cam)
    signal = np.max(np.abs(img_add - b))
    assert signal > 0
    assert np.max(np.abs(img_comp - img_add)) < 1e-3 * signal


def test_depth_sort_handles_permuted_input():
    """Gradients and values must not depend on the input ordering."""
    mu, s, w, o, b, cam, T, s_blur = _problem(seed=9, K=5)
    perm = np.array([3, 0, 4, 1, 2])
    L1, img1, g1 = cp.render_and_grad(mu, s, w, b, cam, T,
                                      s_blur=s_blur, o=o)
    L2, img2, g2 = cp.render_and_grad(mu[perm], s[perm], w[perm], b, cam,
                                      T, s_blur=s_blur, o=o[perm])
    assert L1 == pytest.approx(L2, rel=1e-12)
    assert np.allclose(img1, img2)
    assert np.allclose(g1["mu"][perm], g2["mu"])
    assert np.allclose(g1["w"][perm], g2["w"])
    assert np.allclose(g1["o"][perm], g2["o"])
