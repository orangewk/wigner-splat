"""Tests for the FULL-COVARIANCE two-mode splat forward model and fitter.

Mirrors test_two_mode_fit.py, but this is the decisive positive result of the
two-mode scaling test. Where the SEPARABLE fitter (test_two_mode_fit.py) is
xfail at fid ~0.50 -- a block-diagonal splat cannot tilt in the measurement
plane to carry the entangled fringe -- the full-covariance splat reaches
fidelity > 0.92 on TwoModeCat(alpha=1.5), BEATING the iterative-MLE baseline
(0.9236) on the same rng=42 data in a small fraction of its wall time, with the
Wigner negativity recovered.

Covered: closed-form radon vs numeric marginal, closed-form fidelity vs
brute-force 4D integration / the exact vacuum overlap / the separable module on
a block-diagonal mixture, analytic gradient vs central differences,
densification (3DGS split) bookkeeping, the anisotropic weight-gradient field,
the convex matched-filter stripe fit, and the acceptance experiment.
"""

import time

import numpy as np
import pytest

from wigner_splat.data2 import histogram_targets2
from wigner_splat.forward2 import SplatMixture2, fidelity_vs_cat as fid_sep
from wigner_splat.forward2f import (
    SplatMixture2F,
    fidelity_vs_cat,
    _TRIL_I,
    _TRIL_J,
)
from wigner_splat.fit2f import (
    _pack2f,
    _unpack2f,
    adapt2f,
    birth_field2f,
    fit2f,
    loss2f,
    loss_and_grad2f,
    matched_stripes,
    weight_ls,
    _probe_cov,
)
from wigner_splat.states2 import TwoModeCat


def _full_mixture():
    """A representative full-covariance mixture with real cross-correlations."""
    rng = np.random.default_rng(11)
    K = 3
    return SplatMixture2F(
        w=[0.7, 0.5, -0.2],
        mu=[[1.0, 0.5, -0.5, 0.2], [-1.5, 0.0, 1.0, -0.3], [0.0, 0.0, 0.0, 0.0]],
        ld=rng.uniform(np.log(0.5), np.log(1.2), size=(K, 4)),
        lo=rng.uniform(-0.4, 0.4, size=(K, 6)),
    )


def test_radon2_matches_numeric_marginal():
    """radon2 must equal the 2D Radon transform of wigner4 (integrate out the
    orthogonal direction of each mode) -- the identity the fit rests on. With a
    FULL covariance this now includes the cross term the separable model lacked.
    """
    mix = _full_mixture()
    xs = np.linspace(-5, 5, 9)
    ss = np.linspace(-8, 8, 201)
    for th1, th2 in [(0.0, 0.0), (0.4, 1.3), (1.1, np.pi / 2)]:
        c1, s1 = np.cos(th1), np.sin(th1)
        c2, s2 = np.cos(th2), np.sin(th2)
        q1 = xs[:, None, None, None]
        b1 = ss[None, :, None, None]
        q2 = xs[None, None, :, None]
        b2 = ss[None, None, None, :]
        x1, p1 = q1 * c1 - b1 * s1, q1 * s1 + b1 * c1
        x2, p2 = q2 * c2 - b2 * s2, q2 * s2 + b2 * c2
        W = mix.wigner4(x1, p1, x2, p2)
        numeric = np.trapezoid(np.trapezoid(W, ss, axis=3), ss, axis=1)
        np.testing.assert_allclose(mix.radon2(xs, xs, th1, th2), numeric, atol=1e-6)


def test_fidelity_vs_cat_matches_bruteforce():
    """Closed-form fidelity must match a coarse brute-force 4D integral."""
    a = 1.2
    cat = TwoModeCat(alpha=a, parity=+1)
    mix = _full_mixture()
    mix.w = mix.w / mix.w.sum()
    g = np.linspace(-4.5, 4.5, 41)
    x1, p1, x2, p2 = np.meshgrid(g, g, g, g, indexing="ij")
    Wmix = mix.wigner4(x1, p1, x2, p2)
    Wcat = cat.wigner(x1, p1, x2, p2)
    dv = (g[1] - g[0]) ** 4
    brute = (2 * np.pi) ** 2 * np.sum(Wmix * Wcat) * dv
    closed = fidelity_vs_cat(mix, a, parity=+1)
    assert closed == pytest.approx(brute, rel=1e-3, abs=1e-4)


def test_fidelity_vs_cat_vacuum_exact():
    """A single splat = two-mode vacuum (Sigma = I/2, w=1) against the cat gives
    the exact |<00|cat>|^2."""
    for a in [0.8, 1.5, 2.0]:
        for parity in (+1, -1):
            vac = SplatMixture2F(
                w=[1.0], mu=[[0.0, 0.0, 0.0, 0.0]],
                ld=[[np.log(np.sqrt(0.5))] * 4], lo=[[0.0] * 6],
            )
            closed = fidelity_vs_cat(vac, a, parity=parity)
            exact = (
                np.exp(-2 * a ** 2)
                * (1 + parity) ** 2
                / (2 * (1 + parity * np.exp(-4 * a ** 2)))
            )
            assert closed == pytest.approx(exact, abs=1e-12)


def test_fidelity_matches_separable_on_block_diagonal():
    """On a block-diagonal (separable) mixture, the full-cov fidelity must equal
    forward2's -- the full-cov overlap correctly generalizes the separable one.
    """
    sep = SplatMixture2(
        w=[0.7, 0.5, -0.2],
        mu=[[1.0, 0.5, -0.5, 0.2], [-1.5, 0.0, 1.0, -0.3], [0.0, 0.0, 0.0, 0.0]],
        s=np.log([[[0.5, 1.2], [0.8, 0.6]], [[0.8, 0.8], [0.5, 1.1]],
                  [[0.4, 0.9], [0.7, 0.7]]]),
        phi=[[0.3, 1.0], [0.0, 0.5], [1.1, 0.2]],
    )
    sep.w = sep.w / sep.w.sum()
    full = SplatMixture2F.from_separable(sep)
    for a in [0.9, 1.5]:
        for parity in (+1, -1):
            assert fidelity_vs_cat(full, a, parity=parity) == pytest.approx(
                fid_sep(sep, a, parity=parity), abs=1e-12
            )


def test_analytic_gradient_matches_central_difference():
    """loss_and_grad2f must agree with central differences (rtol 1e-5) -- with
    nonzero Cholesky off-diagonals exercising the full cross-covariance chain."""
    cat = TwoModeCat(alpha=1.5, parity=+1)
    pairs = [(t1, t2) for t1 in np.linspace(0, np.pi, 3, endpoint=False)
             for t2 in np.linspace(0, np.pi, 3, endpoint=False)]
    data = cat.sample_homodyne(pairs, 500, rng=7)
    centers, targets = histogram_targets2(data, bins=20)
    K = 3
    rng = np.random.default_rng(3)
    mix = SplatMixture2F(
        w=np.array([0.7, 0.5, -0.2]) + np.array([-0.3, 0.1, 0.25]),
        mu=rng.uniform(-1.5, 1.5, size=(K, 4)),
        ld=rng.uniform(np.log(0.5), np.log(1.2), size=(K, 4)),
        lo=rng.uniform(-0.4, 0.4, size=(K, 6)),
    )
    v = _pack2f(mix)
    _, grad = loss_and_grad2f(_unpack2f(v, K), centers, targets)

    eps = 1e-6
    numeric = np.empty_like(v)
    for i in range(len(v)):
        vp, vm = v.copy(), v.copy()
        vp[i] += eps
        vm[i] -= eps
        numeric[i] = (
            loss2f(_unpack2f(vp, K), centers, targets)
            - loss2f(_unpack2f(vm, K), centers, targets)
        ) / (2 * eps)
    np.testing.assert_allclose(grad, numeric, rtol=1e-5, atol=1e-7)


def test_adapt2f_prunes_and_splits_with_moment_bookkeeping():
    """adapt2f prunes a negligible splat and splits the high-gradient one into
    two half-weight children (the 3DGS split), with Adam moments carried."""
    mix = SplatMixture2F(
        w=[0.6, 0.25, 0.15, 1e-4],
        mu=[[1.0, 0.0, 0.0, 0.0], [-1.0, 0.5, 0.3, 0.0],
            [0.5, -0.5, 0.1, 0.2], [0.0, 0.0, 0.0, 0.0]],
        ld=np.log([[1.5, 0.4, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5],
                   [0.6, 0.6, 0.6, 0.6], [0.5, 0.5, 0.5, 0.5]]),
        lo=np.zeros((4, 6)),
    )
    m1 = _pack2f(mix) * 0.1
    m2 = np.abs(_pack2f(mix)) * 0.2
    gnorm = np.array([10.0, 0.1, 0.1, 0.1])  # only splat 0 far above median

    new, m1n, m2n = adapt2f(mix, m1, m2, gnorm, K_max=5)

    assert len(new.w) == 4  # 4 kept - 1 pruned - 1 parent + 2 children
    np.testing.assert_allclose(new.w[:2], [0.3, 0.3])       # half-weight children
    np.testing.assert_allclose(new.w[2:], [0.25, 0.15])     # untouched kept splats
    # the two children are offset symmetrically about the parent mean
    np.testing.assert_allclose(new.mu[0] + new.mu[1], 2 * mix.mu[0], atol=1e-9)
    assert not np.allclose(new.mu[0], new.mu[1])
    assert m1n.shape == m2n.shape == (15 * 4,)
    np.testing.assert_allclose(m1n[2], 0.25 * 0.1)          # kept splat's w-moment


def test_birth_field_anisotropic_beats_isotropic_on_fringe():
    """After fitting the two blobs, a THIN stripe probe aligned to p1+p2 detects
    the residual fringe (strong, sign-oscillating) an isotropic probe smears
    over -- the mechanism the separable fitter's isotropic field lacked."""
    a = 1.5
    r2a = np.sqrt(2) * a
    cat = TwoModeCat(alpha=a, parity=+1)
    pairs = [(t1, t2) for t1 in np.linspace(0, np.pi, 4, endpoint=False)
             for t2 in np.linspace(0, np.pi, 4, endpoint=False)]
    data = cat.sample_homodyne(pairs, 3000, rng=5)
    centers, targets = histogram_targets2(data, bins=40)
    blobs = SplatMixture2F(
        w=[0.5, 0.5],
        mu=[[r2a, 0, r2a, 0], [-r2a, 0, -r2a, 0]],
        ld=np.full((2, 4), np.log(np.sqrt(0.5))), lo=np.zeros((2, 6)),
    )
    # candidates along the p1+p2 line through the origin (x1=x2=0, p1=p2)
    ts = np.linspace(-3, 3, 61)
    vh = np.array([0, 1, 0, 1.0]) / np.sqrt(2)
    cand = ts[:, None] * vh[None, :]

    thin = birth_field2f(blobs, centers, targets, cand, _probe_cov([0, 1, 0, 1], 0.05))
    iso = birth_field2f(blobs, centers, targets, cand, 0.5 * np.eye(4))
    assert np.abs(thin).max() > 5 * np.abs(iso).max()   # resonance
    assert np.sum(np.diff(np.sign(thin)) != 0) >= 4     # oscillating fringe stripes


def test_matched_stripes_recovers_fringe_direction_and_reduces_loss():
    """matched_stripes picks the p1+p2 correlation direction from data, and
    appending its stripe basis + a convex weight solve drops the loss below the
    blob-only envelope -- the signed fringe emerging from the residual."""
    a = 1.5
    r2a = np.sqrt(2) * a
    cat = TwoModeCat(alpha=a, parity=+1)
    grid = np.linspace(0, np.pi, 4, endpoint=False)
    pairs = [(t1, t2) for t1 in grid for t2 in grid]
    data = cat.sample_homodyne(pairs, 3000, rng=5)
    centers, targets = histogram_targets2(data, bins=40)
    hist_stack = np.array([h for _, h in targets]).ravel()
    blobs = SplatMixture2F(
        w=[0.5, 0.5],
        mu=[[r2a, 0, r2a, 0], [-r2a, 0, -r2a, 0]],
        ld=np.full((2, 4), np.log(np.sqrt(0.5))), lo=np.zeros((2, 6)),
    )
    mus, ld0, lo0, direction = matched_stripes(blobs, centers, targets)
    # the recovered direction is +-(p1+p2)/sqrt2
    assert np.abs(np.abs(direction) - np.array([0, 1, 0, 1]) / np.sqrt(2)).max() < 1e-9

    m = len(mus)
    dic = SplatMixture2F(
        np.ones(2 + m), np.vstack([blobs.mu, mus]),
        np.vstack([blobs.ld, np.tile(ld0, (m, 1))]),
        np.vstack([blobs.lo, np.tile(lo0, (m, 1))]),
    )
    fitted = weight_ls(dic, centers, targets, hist_stack)
    assert loss2f(fitted, centers, targets, lambda_sum=0.0) < loss2f(
        blobs, centers, targets, lambda_sum=0.0
    )
    assert (fitted.w < -0.01).any()   # signed fringe splats present


@pytest.mark.slow
def test_acceptance_beats_mle_on_fidelity_speed_and_negativity():
    """THE decisive two-mode scaling test. On the SAME data the MLE baseline
    uses -- TwoModeCat(alpha=1.5, +1), 4x4 angle pairs, 3000 shots, rng=42,
    bins=40 -- the full-covariance splat fitter must exceed the MLE fidelity
    (0.9236), recover the (p1, p2) Wigner negativity, and do so far under the
    MLE's ~55 s wall time. This is the falsification condition met on the splat
    side; experiment 04 pairs it with the MLE run for the head-to-head verdict.
    """
    a = 1.5
    cat = TwoModeCat(alpha=a, parity=+1)
    grid = np.linspace(0, np.pi, 4, endpoint=False)
    pairs = [(t1, t2) for t1 in grid for t2 in grid]
    data = cat.sample_homodyne(pairs, 3000, rng=42)
    centers, targets = histogram_targets2(data, bins=40)

    start = fit2f(data, polish_iters=0) if False else None  # (no-op placeholder)
    t0 = time.time()
    mix = fit2f(data)
    wall = time.time() - t0

    fid = fidelity_vs_cat(mix, a, parity=+1)
    p = np.linspace(-3, 3, 121)
    P1, P2 = np.meshgrid(p, p)
    zero = np.zeros_like(P1)
    Wmin = mix.wigner4(zero, P1, zero, P2).min()
    print(f"\nacceptance: fidelity={fid:.4f} (MLE 0.9236)  K={len(mix.w)}  "
          f"sumw={mix.w.sum():.3f}  Wmin={Wmin:.4f}  wall={wall:.1f}s (MLE ~55s)")

    assert abs(mix.w.sum() - 1.0) < 0.15     # stayed normalized
    assert fid > 0.9236                      # beats the MLE fidelity
    assert Wmin < -0.02                      # recovered the entangled fringe
    assert wall < 40.0                       # far under the MLE wall time
