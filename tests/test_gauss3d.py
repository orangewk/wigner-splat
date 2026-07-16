"""Pins for the exp15 minimal 3D splatting module (issue #48 Phase 0).

Everything in gauss3d is analytic; these tests pin the render gradient and
the probe information matrix against finite differences, and check the one
physical claim the confidence score rests on: parallax breaks the
monocular size-distance degeneracy, so information rises with baseline.
"""
import importlib.util
import pathlib

import numpy as np
import pytest

_spec = importlib.util.spec_from_file_location(
    "gauss3d",
    pathlib.Path(__file__).resolve().parents[1]
    / "experiments" / "15_video_conf" / "gauss3d.py",
)
g3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g3)


def _problem(seed=5, K=3, img=20):
    rng = np.random.default_rng(seed)
    cam = g3.make_camera((0.3, -0.2, 0.0), (0.0, 0.0, 5.0), 22.0, (img, img))
    mu = np.column_stack([rng.uniform(-1, 1, (K, 2)),
                          rng.uniform(3.0, 7.0, K)])
    s = rng.uniform(-1.2, -0.4, K)
    w = rng.normal(size=K)
    target = rng.normal(size=img * img)
    return mu, s, w, cam, target


def test_gradient_matches_central_difference():
    mu, s, w, cam, T = _problem()
    _, _, g = g3.render_and_grad(mu, s, w, cam, T)
    flat = np.concatenate([mu.ravel(), s, w])
    g_an = np.concatenate([g["mu"].ravel(), g["s"], g["w"]])
    K = len(w)

    def unflat(v):
        return v[:3 * K].reshape(K, 3), v[3 * K:4 * K], v[4 * K:]

    eps = 1e-6
    g_fd = np.zeros_like(flat)
    for i in range(len(flat)):
        vp = flat.copy(); vp[i] += eps
        vm = flat.copy(); vm[i] -= eps
        lp, _, _ = g3.render_and_grad(*unflat(vp), cam, T)
        lm, _, _ = g3.render_and_grad(*unflat(vm), cam, T)
        g_fd[i] = (lp - lm) / (2 * eps)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g_an - g_fd) / scale) < 1e-5


def test_probe_information_matches_brute_force():
    """H must equal sum_pixels J J^T with J from finite differences of the
    rendered probe image (nondimensionalized parameters)."""
    cams = [g3.make_camera((0.4 * t, 0.0, 0.0), (0.0, 0.0, 5.0), 22.0,
                           (24, 24)) for t in (-1.0, 1.0)]
    x = np.array([0.3, -0.2, 5.5])
    sp = 0.5
    H = g3.probe_information(x, sp, cams)

    eps = 1e-5
    H_fd = np.zeros((5, 5))
    for cam in cams:
        cols = []
        for i in range(5):
            def img(delta, i=i):
                mu = x.copy(); s = np.log(sp); w = 1.0
                if i < 3:
                    mu[i] += delta * sp   # mu measured in probe-scale units
                elif i == 3:
                    s += delta
                else:
                    w += delta
                return g3.render(mu[None, :], np.array([s]), np.array([w]),
                                 cam)
            cols.append((img(eps) - img(-eps)) / (2 * eps))
        J = np.stack(cols, axis=1)
        H_fd += J.T @ J
    assert np.max(np.abs(H - H_fd)) < 1e-4 * np.max(np.abs(H_fd))


def test_parallax_raises_confidence():
    """The physical claim under the score: with one view the size-distance
    degeneracy leaves lambda_min tiny; a wide baseline breaks it."""
    x = np.array([0.0, 0.0, 6.0])
    sp = 0.4
    one = [g3.make_camera((0.0, 0.0, 0.0), x, 64.0, (64, 64))]
    wide = one + [g3.make_camera((3.0, 0.0, 0.0), x, 64.0, (64, 64))]
    lam_one = np.linalg.eigvalsh(g3.probe_information(x, sp, one))[0]
    lam_wide = np.linalg.eigvalsh(g3.probe_information(x, sp, wide))[0]
    assert lam_wide > 20 * lam_one


def test_behind_camera_contributes_nothing():
    cam = g3.make_camera((0.0, 0.0, 0.0), (0.0, 0.0, 5.0), 22.0, (16, 16))
    mu = np.array([[0.0, 0.0, -3.0]])
    img = g3.render(mu, np.array([-0.5]), np.array([1.0]), cam)
    assert np.all(img == 0.0)
    _, _, g = g3.render_and_grad(mu, np.array([-0.5]), np.array([1.0]),
                                 cam, np.ones(16 * 16))
    assert np.all(g["mu"] == 0.0) and np.all(g["s"] == 0.0)


def test_fit_recovers_single_splat():
    cams = [g3.make_camera((0.5 * t, 0.0, 0.0), (0.0, 0.0, 5.0), 32.0,
                           (32, 32)) for t in np.linspace(-1, 1, 6)]
    mu_t = np.array([[0.2, -0.1, 5.0]])
    s_t = np.array([np.log(0.5)])
    w_t = np.array([-0.8])
    frames = [g3.render(mu_t, s_t, w_t, cam) for cam in cams]
    params, losses = g3.fit(frames, cams, K=1, iters=800, lr=0.05, seed=3,
                            init_box=((-1, 1), (-1, 1), (4, 6)))
    assert losses[-1] < 1e-4 * max(losses[0], 1e-12) or losses[-1] < 1e-6


def test_frame_jacobian_matches_render_fd():
    mu, s, w, cam, _ = _problem(seed=9, K=2, img=14)
    J = g3.frame_jacobian(mu, s, w, cam)
    eps = 1e-6
    K = len(w)
    for i in range(5 * K):
        k, j = divmod(i, 5)

        def img(delta, k=k, j=j):
            mu2, s2, w2 = mu.copy(), s.copy(), w.copy()
            if j < 3:
                mu2[k, j] += delta
            elif j == 3:
                s2[k] += delta
            else:
                w2[k] += delta
            return g3.render(mu2, s2, w2, cam)
        col_fd = (img(eps) - img(-eps)) / (2 * eps)
        assert np.max(np.abs(J[:, i] - col_fd)) < 1e-5 * max(
            1e-6, np.max(np.abs(col_fd)))


def test_density_grad_matches_fd():
    rng = np.random.default_rng(2)
    mu = rng.normal(size=(2, 3))
    s = rng.uniform(-1, 0, 2)
    w = rng.normal(size=2)
    pts = rng.normal(size=(4, 3))
    Jr = g3.density_grad(pts, mu, s, w)
    eps = 1e-6
    for i in range(10):
        k, j = divmod(i, 5)

        def rho(delta, k=k, j=j):
            mu2, s2, w2 = mu.copy(), s.copy(), w.copy()
            if j < 3:
                mu2[k, j] += delta
            elif j == 3:
                s2[k] += delta
            else:
                w2[k] += delta
            return g3.density3d(pts, mu2, s2, w2)
        col_fd = (rho(eps) - rho(-eps)) / (2 * eps)
        assert np.max(np.abs(Jr[:, i] - col_fd)) < 1e-6 + 1e-5 * np.max(
            np.abs(col_fd))


def test_predicted_sigma_falls_with_parallax():
    """Score v2 sanity: the delta-method uncertainty of the density near a
    splat must shrink when a wide-baseline view breaks the size-distance
    degeneracy."""
    params = {"mu": np.array([[0.0, 0.0, 6.0]]),
              "s": np.array([np.log(0.5)]), "w": np.array([1.0])}
    pts = np.array([[0.0, 0.0, 6.4]])  # probe just behind the center
    one = [g3.make_camera((0.0, 0.0, 0.0), (0, 0, 6.0), 64.0, (64, 64))]
    wide = one + [g3.make_camera((3.0, 0.0, 0.0), (0, 0, 6.0), 64.0,
                                 (64, 64))]
    sig_one = g3.predicted_sigma(pts, params, one)[0]
    sig_wide = g3.predicted_sigma(pts, params, wide)[0]
    assert sig_wide < 0.5 * sig_one


def test_spearman_helper():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    assert g3.spearman(a, a ** 3) == pytest.approx(1.0)
    assert g3.spearman(a, -a) == pytest.approx(-1.0)
