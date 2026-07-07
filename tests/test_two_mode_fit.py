"""Tests for the separable two-mode splat forward model and fitter.

Mirrors test_forward.py: closed-form Radon vs numeric marginal, closed-form
fidelity vs brute-force 4D integration and the exact vacuum overlap, analytic
gradient vs central differences, densification/birth bookkeeping, and the
acceptance smoke test.

FALSIFICATION FINDING (two-mode scaling test, docs/two-mode-plan.md): the
separable-splat + histogram-MSE reconstructor does NOT reach the plan's
fidelity > 0.9 target on TwoModeCat(alpha=1.5). It recovers the two coherent
blobs (fid ~0.5, the classical-mixture overlap) but not the entangled fringe.
Investigated exhaustively (see test_smoke_fit_target_fidelity_is_unreached's
xfail reason): the loss minimum itself sits at fid ~0.80-0.85 (MSE overfits
the weak ~2% fringe signal), and separable splats cannot align to the p1-p2
fringe ridge. The forward model, closed-form fidelity, analytic gradient,
adapt, and birth are all correct and verified below; the ceiling is a property
of the representation + loss, not a bug.
"""

import time

import numpy as np
import pytest

from wigner_splat.data2 import histogram_targets2
from wigner_splat.forward2 import SplatMixture2, fidelity_vs_cat
from wigner_splat.fit2 import (
    _pack2,
    _unpack2,
    adapt2,
    birth_field2,
    fit2,
    loss2,
    loss_and_grad2,
)
from wigner_splat.states2 import TwoModeCat


def _small_mixture():
    return SplatMixture2(
        w=[0.7, 0.5, -0.2],
        mu=[[1.0, 0.5, -0.5, 0.2], [-1.5, 0.0, 1.0, -0.3], [0.0, 0.0, 0.0, 0.0]],
        s=np.log(
            [
                [[0.5, 1.2], [0.8, 0.6]],
                [[0.8, 0.8], [0.5, 1.1]],
                [[0.4, 0.9], [0.7, 0.7]],
            ]
        ),
        phi=[[0.3, 1.0], [0.0, 0.5], [1.1, 0.2]],
    )


def test_radon2_matches_numeric_marginal():
    """radon2 must equal the 2D Radon transform of wigner4 (integrate out the
    orthogonal direction of each mode) -- the identity the fit rests on."""
    mix = _small_mixture()
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
    mix = _small_mixture()
    mix.w = mix.w / mix.w.sum()  # normalize for a representative overlap
    g = np.linspace(-4.5, 4.5, 41)
    x1, p1, x2, p2 = np.meshgrid(g, g, g, g, indexing="ij")
    Wmix = mix.wigner4(x1, p1, x2, p2)
    Wcat = cat.wigner(x1, p1, x2, p2)
    dv = (g[1] - g[0]) ** 4
    brute = (2 * np.pi) ** 2 * np.sum(Wmix * Wcat) * dv
    closed = fidelity_vs_cat(mix, a, parity=+1)
    assert closed == pytest.approx(brute, rel=1e-3, abs=1e-4)


def test_fidelity_vs_cat_vacuum_exact():
    """A single splat = two-mode vacuum (each mode sigma^2 = 1/2, w=1) against
    the cat gives |<00|cat>|^2. Derived from the cat Fock c_00 amplitude:

        <00|(|a,a>+P|-a,-a>) = e^{-a^2}(1 + P), norm = 2(1 + P e^{-4 a^2}),
        |<00|cat>|^2 = e^{-2 a^2} (1 + P)^2 / (2 (1 + P e^{-4 a^2})).
    """
    for a in [0.8, 1.5, 2.0]:
        for parity in (+1, -1):
            vac = SplatMixture2(
                w=[1.0],
                mu=[[0.0, 0.0, 0.0, 0.0]],
                s=[[[np.log(np.sqrt(0.5))] * 2, [np.log(np.sqrt(0.5))] * 2]],
                phi=[[0.0, 0.0]],
            )
            closed = fidelity_vs_cat(vac, a, parity=parity)
            exact = (
                np.exp(-2 * a ** 2)
                * (1 + parity) ** 2
                / (2 * (1 + parity * np.exp(-4 * a ** 2)))
            )
            assert closed == pytest.approx(exact, abs=1e-12)


def test_analytic_gradient_matches_central_difference():
    """loss_and_grad2 must agree with central differences (rtol 1e-5)."""
    cat = TwoModeCat(alpha=1.5, parity=+1)
    pairs = [(t1, t2) for t1 in np.linspace(0, np.pi, 3, endpoint=False)
             for t2 in np.linspace(0, np.pi, 3, endpoint=False)]
    data = cat.sample_homodyne(pairs, 500, rng=7)
    centers, targets = histogram_targets2(data, bins=20)
    K = 3
    rng = np.random.default_rng(3)
    mix = SplatMixture2.random_init(K, rng=3)
    mix.w = mix.w + np.array([-0.3, 0.1, 0.25])  # break symmetry, negative weight
    v = _pack2(mix)

    _, grad = loss_and_grad2(_unpack2(v, K), centers, targets)

    eps = 1e-6
    numeric = np.empty_like(v)
    for i in range(len(v)):
        vp, vm = v.copy(), v.copy()
        vp[i] += eps
        vm[i] -= eps
        numeric[i] = (
            loss2(_unpack2(vp, K), centers, targets)
            - loss2(_unpack2(vm, K), centers, targets)
        ) / (2 * eps)
    np.testing.assert_allclose(grad, numeric, rtol=1e-5, atol=1e-7)


def test_adapt2_prunes_and_splits_with_moment_bookkeeping():
    mix = SplatMixture2(
        w=[0.6, 0.25, 0.15, 1e-4],  # last splat below prune threshold
        mu=[[1.0, 0.0, 0.0, 0.0], [-1.0, 0.5, 0.3, 0.0],
            [0.5, -0.5, 0.1, 0.2], [0.0, 0.0, 0.0, 0.0]],
        s=np.log(
            [
                [[1.5, 0.4], [0.5, 0.5]],   # dominant axis: mode 0, axis 0 (s=1.5)
                [[0.5, 0.5], [0.5, 0.5]],
                [[0.6, 0.6], [0.6, 0.6]],
                [[0.5, 0.5], [0.5, 0.5]],
            ]
        ),
        phi=[[0.0, 0.0], [0.2, 0.1], [0.4, 0.3], [0.0, 0.0]],
    )
    m1 = _pack2(mix) * 0.1
    m2 = np.abs(_pack2(mix)) * 0.2
    gnorm = np.array([10.0, 0.1, 0.1, 0.1])  # only splat 0 far above median

    new, m1n, m2n = adapt2(mix, m1, m2, gnorm, K_max=5)

    assert len(new.w) == 4  # 4 kept - 1 pruned - 1 parent + 2 children
    np.testing.assert_allclose(new.w[:2], [0.3, 0.3])
    # split along mode 0 major axis (phi=0, x): children offset in x1 only
    assert new.mu[0, 0] < 1.0 < new.mu[1, 0]
    np.testing.assert_allclose(new.mu[:2, 1], 0.0)  # p1 unchanged
    np.testing.assert_allclose(new.mu[:2, 2:], 0.0)  # mode 1 unchanged
    np.testing.assert_allclose(np.exp(new.s[:2, 0, 0]), 1.5 / 1.6)
    np.testing.assert_allclose(new.w[2:], [0.25, 0.15])
    assert m1n.shape == m2n.shape == (11 * 4,)
    np.testing.assert_allclose(m1n[2], 0.25 * 0.1)  # w-moment of kept splat


def test_birth_splat_decreases_loss():
    """A splat born at the extremum of the weight-gradient field, with the
    descent sign, reduces loss2 -- the mechanism that grows negativity."""
    a = 1.5
    r2a = np.sqrt(2) * a
    cat = TwoModeCat(alpha=a, parity=+1)
    pairs = [(t1, t2) for t1 in np.linspace(0, np.pi, 4, endpoint=False)
             for t2 in np.linspace(0, np.pi, 4, endpoint=False)]
    data = cat.sample_homodyne(pairs, 3000, rng=5)
    centers, targets = histogram_targets2(data, bins=40)
    # two positive blobs only: the entangled fringe is entirely missing
    blobs = SplatMixture2(
        w=[0.5, 0.5],
        mu=[[r2a, 0.0, r2a, 0.0], [-r2a, 0.0, -r2a, 0.0]],
        s=np.full((2, 2, 2), np.log(np.sqrt(0.5))),
        phi=np.zeros((2, 2)),
    )
    xg = np.linspace(centers[0], centers[-1], 9)
    G1, G2, G3, G4 = np.meshgrid(xg, xg, xg, xg, indexing="ij")
    cand = np.stack([G1.ravel(), G2.ravel(), G3.ravel(), G4.ravel()], axis=1)
    field = birth_field2(blobs, centers, targets, cand)
    i = np.argmax(np.abs(field))
    born = SplatMixture2(
        np.append(blobs.w, -np.sign(field[i]) * 0.005),
        np.vstack([blobs.mu, cand[i]]),
        np.concatenate([blobs.s, np.full((1, 2, 2), np.log(0.5))], axis=0),
        np.vstack([blobs.phi, np.zeros((1, 2))]),
    )
    # birth_field2 is the DATA-residual gradient (like fit.birth_field it does
    # not see the sum-to-one term), so the descent guarantee is on the fit loss.
    # In 2D that residual field is O(1/B^2), far smaller than the fixed
    # lambda_sum (delta_w)^2 that adding any weight costs, so isolate the term
    # birth actually targets: the reconstruction (L2 + negativity) loss.
    assert loss2(born, centers, targets, lambda_sum=0.0) < loss2(
        blobs, centers, targets, lambda_sum=0.0
    )


@pytest.mark.slow
def test_smoke_fit_runs_and_recovers_classical_envelope():
    """Acceptance smoke test (kept under ~60 s): fit2 from K=6 with
    densification runs end-to-end on a 4x4 angle grid, stays normalized, and
    recovers the two-blob classical envelope of the entangled cat.

    NOTE -- the two-mode target fidelity > 0.9 is NOT reached by this
    reconstructor; see test_smoke_fit_target_fidelity_is_unreached (xfail) and
    the module docstring / handoff report for the falsification analysis. This
    test asserts the pipeline's actual, reproducible behavior: it recovers the
    two coherent blobs (tr(rho_fit rho_cat) ~ 0.5, the classical-mixture
    overlap) and reduces the reconstruction loss well below the untrained
    start.
    """
    a = 1.5
    cat = TwoModeCat(alpha=a, parity=+1)
    grid = np.linspace(0, np.pi, 4, endpoint=False)
    pairs = [(t1, t2) for t1 in grid for t2 in grid]
    data = cat.sample_homodyne(pairs, 3000, rng=42)
    centers, targets = histogram_targets2(data, bins=40)

    start = SplatMixture2.random_init(6, rng=42)
    l0 = loss2(start, centers, targets)

    t0 = time.time()
    mix = fit2(data, K=6, iters=600, lr=0.05, seed=42, bins=40,
               densify_every=60, K_max=16)
    wall = time.time() - t0

    fid = fidelity_vs_cat(mix, a, parity=+1)
    l1 = loss2(mix, centers, targets)
    print(f"\nsmoke: fidelity={fid:.4f} loss {l0:.5f}->{l1:.5f} "
          f"K={len(mix.w)} sumw={mix.w.sum():.3f} wall={wall:.1f}s")
    assert l1 < l0                       # optimization made progress
    assert abs(mix.w.sum() - 1.0) < 0.1  # stayed normalized
    assert fid > 0.4                     # recovered the classical two-blob envelope


@pytest.mark.slow
@pytest.mark.xfail(
    reason=(
        "FALSIFICATION FINDING: separable-splat + histogram-MSE cannot "
        "reconstruct the two-mode entangled cat at alpha=1.5. (1) The fringe is "
        "a ~2%-RMS joint-correlation signal; MSE overfits it, and the loss "
        "MINIMUM sits at fid ~0.80-0.85 -- a hand-built fid=0.997 mixture "
        "DEGRADES to ~0.85 under the loss, so no optimizer can exceed 0.9. "
        "(2) Separable (block-diagonal) splats cannot align to the p1-p2 ridge "
        "where cos(w(p1+p2)) is constant, needing ~80 axis-aligned splats to "
        "tile the fringe (in-splat entangled-correlation limit). (3) From "
        "random init, residual-birth chases the dominant blob residual, so the "
        "fit settles in the classical two-blob basin (fid ~0.5, no negativity) "
        "for every tested setting (shots up to 2e5, angles up to 6x6, K up to "
        "120, batched fringe-seeded birth, lambda_neg 0-10). See handoff report."
    ),
    strict=False,
)
def test_smoke_fit_target_fidelity_is_unreached():
    """The plan's aspirational target: fit2 recovers fidelity > 0.9 and a
    clearly negative (p1, p2) fringe at x1 = x2 = 0. Recorded as xfail -- this
    is the decisive two-mode scaling test and the splat side does not pass it
    at alpha=1.5 (the MLE side is the fair comparison in experiment 04)."""
    a = 1.5
    cat = TwoModeCat(alpha=a, parity=+1)
    grid = np.linspace(0, np.pi, 4, endpoint=False)
    pairs = [(t1, t2) for t1 in grid for t2 in grid]
    data = cat.sample_homodyne(pairs, 3000, rng=42)

    mix = fit2(data, K=6, iters=600, lr=0.05, seed=42, bins=40,
               densify_every=60, K_max=16, n_birth=6, birth_spread=1.3)

    fid = fidelity_vs_cat(mix, a, parity=+1)
    p = np.linspace(-3, 3, 121)
    P1, P2 = np.meshgrid(p, p)
    zero = np.zeros_like(P1)
    Wmin = mix.wigner4(zero, P1, zero, P2).min()
    assert fid > 0.9
    assert Wmin < -0.02
