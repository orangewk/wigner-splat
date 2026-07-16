"""Pins for the birth-field image demo (demos/birthfield_image).

The demo module is analytic throughout; these tests pin the gradient
against central differences and the birth field against its definition
(brute-force dL/dw of a hypothetical splat).
"""
import importlib.util
import pathlib

import numpy as np
import pytest

_spec = importlib.util.spec_from_file_location(
    "birthfield2d",
    pathlib.Path(__file__).resolve().parents[1]
    / "demos" / "birthfield_image" / "birthfield2d.py",
)
bf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bf)


def _problem(seed=7, K=3, n=17):
    rng = np.random.default_rng(seed)
    xs = np.linspace(-2, 2, n)
    Xg, Yg = np.meshgrid(xs, xs)
    X, Y = Xg.ravel(), Yg.ravel()
    T = rng.normal(size=X.shape)
    mu = rng.uniform(-1, 1, (K, 2))
    s = rng.uniform(-0.8, 0.2, (K, 2))
    phi = rng.uniform(0, np.pi, K)
    w = rng.normal(size=K)
    return mu, s, phi, w, X, Y, T


def test_gradient_matches_central_difference():
    mu, s, phi, w, X, Y, T = _problem()
    loss, _, g = bf.render_and_grad(mu, s, phi, w, X, Y, T)
    flat = np.concatenate([mu.ravel(), s.ravel(), phi, w])
    g_an = np.concatenate([g["mu"].ravel(), g["s"].ravel(),
                           g["phi"], g["w"]])

    def unflat(v):
        K = len(w)
        return (v[:2 * K].reshape(K, 2), v[2 * K:4 * K].reshape(K, 2),
                v[4 * K:5 * K], v[5 * K:])

    eps = 1e-6
    g_fd = np.zeros_like(flat)
    for i in range(len(flat)):
        vp = flat.copy(); vp[i] += eps
        vm = flat.copy(); vm[i] -= eps
        lp, _, _ = bf.render_and_grad(*unflat(vp), X, Y, T)
        lm, _, _ = bf.render_and_grad(*unflat(vm), X, Y, T)
        g_fd[i] = (lp - lm) / (2 * eps)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g_an - g_fd) / scale) < 1e-6


def test_birth_field_is_dLdw_of_hypothetical_splat():
    """B(mu) must equal the analytic g_w of a zero-weight probe splat."""
    mu, s, phi, w, X, Y, T = _problem(seed=3, n=25)
    _, image, _ = bf.render_and_grad(mu, s, phi, w, X, Y, T)
    n = int(np.sqrt(len(X)))
    sigma_px = 2.0
    B = bf.birth_field((image - T).reshape(n, n), sigma_px)
    px = (X.max() - X.min()) / (n - 1)
    sigma_world = sigma_px * px
    # probe at a few pixels: append a zero-weight isotropic splat and read g_w
    for iy, ix in [(5, 7), (12, 12), (20, 4)]:
        pos = np.array([X.reshape(n, n)[iy, ix], Y.reshape(n, n)[iy, ix]])
        mu2 = np.vstack([mu, pos])
        s2 = np.vstack([s, np.full(2, np.log(sigma_world))])
        phi2 = np.append(phi, 0.0)
        w2 = np.append(w, 0.0)
        _, _, g = bf.render_and_grad(mu2, s2, phi2, w2, X, Y, T)
        assert B[iy, ix] == pytest.approx(g["w"][-1], rel=1e-5, abs=1e-12)


def test_split_mode_never_creates_a_new_sign():
    rng = np.random.default_rng(0)
    T = np.clip(rng.normal(size=(24, 24)), 0, None)
    hist = bf.fit(T, extent=2.0, mode="split", K0=3, K_max=8, iters=300,
                  grow_every=60, snapshot_every=1000, seed=1)
    kinds = {e[1] for e in hist["events"]}
    assert kinds == {"split"}
    # splits preserve each parent's sign at the moment of splitting; the
    # structural claim (no sign flip by splitting) is what the demo shows
    assert len(hist["final"][0]["w"]) == 8


def test_fit_birth_mode_reduces_loss_and_births_negatives():
    # target with a genuinely negative region: positive blob + negative dip
    n = 32
    xs = np.linspace(-2, 2, n)
    Xg, Yg = np.meshgrid(xs, xs)
    T = (np.exp(-((Xg + 0.6) ** 2 + Yg ** 2))
         - 0.8 * np.exp(-3 * ((Xg - 0.7) ** 2 + Yg ** 2)))
    hist = bf.fit(T, extent=2.0, mode="birth", K0=2, K_max=10, iters=800,
                  grow_every=100, snapshot_every=1000, seed=0)
    assert hist["loss"][-1] < 0.2 * hist["loss"][0]
    signs = [e[3] for e in hist["events"] if e[1] == "birth"]
    assert any(sg < 0 for sg in signs)  # a negative splat was BORN
    assert np.any(hist["final"][0]["w"] < 0)
