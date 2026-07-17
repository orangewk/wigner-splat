"""Pins for the exp16 real-video splatting module (issue #48 Phase 1).

Central-difference pins for EVERY analytic gradient the joint fit uses:
splats (mu, s, w), background b, camera pose (translation c and rotation
in the identity chart), global log-focal, and the blur knob s_blur; plus
the closed-form blur composition against a brute-force convolution and
the no-blur reduction to the exp15 renderer.
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


sv = _load("splatvid", _here / "experiments" / "16_real_video"
           / "splatvid.py")
g3 = _load("gauss3d", _here / "experiments" / "15_video_conf"
           / "gauss3d.py")


def _problem(seed=11, K=3, img=18):
    rng = np.random.default_rng(seed)
    cam = sv.make_camera((0.2, -0.1, 0.0), (0.0, 0.0, 5.0), 20.0,
                         (img, img))
    mu = np.column_stack([rng.uniform(-1, 1, (K, 2)),
                          rng.uniform(3.0, 7.0, K)])
    s = rng.uniform(-1.2, -0.4, K)
    w = rng.normal(size=K)
    b = 0.37
    s_blur = -0.9
    target = rng.normal(size=img * img)
    return mu, s, w, b, cam, target, s_blur


def test_all_gradients_match_central_difference():
    mu, s, w, b, cam, T, s_blur = _problem()
    _, _, g = sv.render_and_grad(mu, s, w, b, cam, T, s_blur=s_blur)
    eps = 1e-6

    def loss_of(mu2=None, s2=None, w2=None, b2=None, c2=None, d=None,
                logf2=None, sb2=None):
        cam2 = dict(cam)
        if c2 is not None:
            cam2["c"] = c2
        if d is not None:
            cam2["R"] = sv.rot_exp(d) @ cam["R"]
        if logf2 is not None:
            cam2["f"] = float(np.exp(logf2))
        L, _, _ = sv.render_and_grad(
            mu if mu2 is None else mu2, s if s2 is None else s2,
            w if w2 is None else w2, b if b2 is None else b2, cam2, T,
            s_blur=s_blur if sb2 is None else sb2)
        return L

    # splats
    K = len(w)
    for k in range(K):
        for j in range(3):
            m2 = mu.copy(); m2[k, j] += eps
            m3 = mu.copy(); m3[k, j] -= eps
            fd = (loss_of(mu2=m2) - loss_of(mu2=m3)) / (2 * eps)
            assert g["mu"][k, j] == pytest.approx(fd, rel=1e-4, abs=1e-9)
        s2 = s.copy(); s2[k] += eps
        s3 = s.copy(); s3[k] -= eps
        fd = (loss_of(s2=s2) - loss_of(s2=s3)) / (2 * eps)
        assert g["s"][k] == pytest.approx(fd, rel=1e-4, abs=1e-9)
        w2 = w.copy(); w2[k] += eps
        w3 = w.copy(); w3[k] -= eps
        fd = (loss_of(w2=w2) - loss_of(w2=w3)) / (2 * eps)
        assert g["w"][k] == pytest.approx(fd, rel=1e-4, abs=1e-9)
    # background
    fd = (loss_of(b2=b + eps) - loss_of(b2=b - eps)) / (2 * eps)
    assert g["b"] == pytest.approx(fd, rel=1e-4, abs=1e-9)
    # camera translation
    for j in range(3):
        cp = cam["c"].copy(); cp[j] += eps
        cm = cam["c"].copy(); cm[j] -= eps
        fd = (loss_of(c2=cp) - loss_of(c2=cm)) / (2 * eps)
        assert g["c"][j] == pytest.approx(fd, rel=1e-4, abs=1e-9)
    # camera rotation (identity chart)
    for j in range(3):
        dp = np.zeros(3); dp[j] = eps
        dm = np.zeros(3); dm[j] = -eps
        fd = (loss_of(d=dp) - loss_of(d=dm)) / (2 * eps)
        assert g["rot"][j] == pytest.approx(fd, rel=1e-4, abs=1e-9)
    # global log-focal
    lf = np.log(cam["f"])
    fd = (loss_of(logf2=lf + eps) - loss_of(logf2=lf - eps)) / (2 * eps)
    assert g["logf"] == pytest.approx(fd, rel=1e-4, abs=1e-9)
    # blur knob
    fd = (loss_of(sb2=s_blur + eps) - loss_of(sb2=s_blur - eps)) / (2 * eps)
    assert g["s_blur"] == pytest.approx(fd, rel=1e-4, abs=1e-9)


def test_no_blur_reduces_to_exp15_renderer():
    mu, s, w, b, cam, T, _ = _problem(seed=4)
    img_new = sv.render(mu, s, w, 0.0, cam, s_blur=None)
    img_old = g3.render(mu, s, w, cam)
    assert np.max(np.abs(img_new - img_old)) < 1e-12
    _, _, g_new = sv.render_and_grad(mu, s, w, 0.0, cam, T, s_blur=None)
    _, _, g_old = g3.render_and_grad(mu, s, w, cam, T)
    for k in ("mu", "s", "w"):
        assert np.max(np.abs(g_new[k] - g_old[k])) < 1e-10


def test_blur_composition_matches_brute_force_convolution():
    """One splat rendered with the closed-form blur must match the sharp
    render convolved with the normalized Gaussian PSF."""
    img = 96
    cam = sv.make_camera((0.0, 0.0, 0.0), (0.0, 0.0, 5.0), 60.0,
                         (img, img))
    mu = np.array([[0.1, -0.05, 5.0]])
    s = np.array([np.log(0.35)])
    w = np.array([0.8])
    s_blur = np.log(2.2)  # PSF sigma in pixels
    blurred = sv.render(mu, s, w, 0.0, cam, s_blur=s_blur).reshape(img, img)
    sharp = sv.render(mu, s, w, 0.0, cam, s_blur=None).reshape(img, img)
    sb = np.exp(s_blur)
    half = int(np.ceil(6 * sb))
    t = np.arange(-half, half + 1)
    k1 = np.exp(-t ** 2 / (2 * sb ** 2))
    k1 /= k1.sum()  # normalized (mass-preserving) PSF
    pad = np.pad(sharp, half, mode="constant")
    rows = np.stack([np.convolve(row, k1, mode="valid") for row in pad])
    conv = np.stack([np.convolve(col, k1, mode="valid")
                     for col in rows.T]).T
    # interior comparison (padding effects near the border)
    m = slice(half, img - half)
    assert np.max(np.abs(blurred[m, m] - conv[m, m])) < 2e-4 * np.max(sharp)


def test_frame_jacobian_matches_render_fd():
    mu, s, w, b, cam, _, s_blur = _problem(seed=8, K=2, img=12)
    J = sv.frame_jacobian(mu, s, w, b, cam, s_blur=s_blur)
    eps = 1e-6
    K = len(w)
    for i in range(5 * K + 1):
        def img(delta, i=i):
            mu2, s2, w2, b2 = mu.copy(), s.copy(), w.copy(), b
            if i == 5 * K:
                b2 += delta
            else:
                k, j = divmod(i, 5)
                if j < 3:
                    mu2[k, j] += delta
                elif j == 3:
                    s2[k] += delta
                else:
                    w2[k] += delta
            return sv.render(mu2, s2, w2, b2, cam, s_blur=s_blur)
        col_fd = (img(eps) - img(-eps)) / (2 * eps)
        assert np.max(np.abs(J[:, i] - col_fd)) < 1e-5 * max(
            1e-6, np.max(np.abs(col_fd)))


def test_precondition_hard_stop_never_loads_holdout(monkeypatch, capsys,
                                                    tmp_path):
    """PR #59 review item 1: a DNF run must return BEFORE the held-out
    frames are loaded. fit_video is faked (fast, terrible PSNR) and
    load_holdout is booby-trapped."""
    run = _load("run16", _here / "experiments" / "16_real_video"
                / "run.py")
    assert run.precondition_met([18.0, 18.5, 19.0])
    assert not run.precondition_met([18.5, 17.9, 19.0])
    assert not run.precondition_met([])

    def fake_fit(frames, shape, f0, K=1, seed=0, use_blur=False, **kw):
        st = {"mu": np.array([[0.0, 0.0, 5.0]]), "s": np.array([-1.0]),
              "w": np.array([0.0]), "o": np.array([-2.0]), "b": 0.0,
              "logf": float(np.log(f0)),
              "s_blur": float(np.log(0.8)) if use_blur else None}
        poses = [(np.eye(3), np.zeros(3)) for _ in frames]
        return st, poses, {"stage": [], "loss": []}

    def trapped_holdout():
        raise AssertionError("held-out frames were loaded on a DNF run")

    monkeypatch.setattr(run, "fit_video", fake_fit)
    monkeypatch.setattr(run, "fit_pose", lambda *a, **k: None)
    monkeypatch.setattr(run, "load_holdout", trapped_holdout)
    monkeypatch.setattr(run, "CKPT", tmp_path)  # never real checkpoints
    run.main([])  # must return at the precondition stop, silently OK
    out = capsys.readouterr().out
    assert "PRECONDITION NOT MET" in out
    assert "Gate B" not in out.split("PRECONDITION NOT MET")[1]


def test_rot_exp_is_rotation():
    d = np.array([0.3, -0.2, 0.5])
    R = sv.rot_exp(d)
    assert np.allclose(R @ R.T, np.eye(3), atol=1e-12)
    assert np.linalg.det(R) == pytest.approx(1.0)
    assert np.allclose(sv.rot_exp(np.zeros(3)), np.eye(3))
