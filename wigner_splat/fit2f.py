"""Full-covariance two-mode reconstructor.

The separable fitter (fit2) failed the two-mode scaling test at fid ~0.50: a
block-diagonal splat cannot tilt in the measurement plane, so it cannot carry
the entangled fringe, and residual-driven birth chased the blobs. The
full-covariance splat (forward2f) removes that limit -- ONE signed splat can
stretch along the p1-p2 ridge and oscillate along p1+p2. Two facts, measured
here and recorded in tests/test_two_mode_full.py, set the strategy:

  * The MSE histogram loss does NOT cap full-cov fidelity at the blob envelope
    (unlike the separable case). A hand-built fid=0.99 mixture beats the
    blob-only solution on loss at every shot budget, and optimizing from it
    settles near fid ~0.93 -- the same shot-noise ceiling the MLE hits
    (0.9236). So the barrier is purely reaching that basin (root cause (c)).

  * The fringe is LINEAR in the splat weights and lives on stripes
    perpendicular to a single generic correlation direction (p1+p2 for this
    cat). Probing the post-blob residual with a THIN anisotropic stripe probe
    resonates ~10x more strongly than an isotropic one; a convex least-squares
    solve for the stripe weights then constructs the whole fringe at once.

Recipe (data-driven and generic -- no true-state knowledge):
  1. Blob span from the max per-angle quadrature variance; init 4 positive
     blobs (diagonal + anti-diagonal) and Adam-fit their shapes.
  2. Prune spurious blobs with a convex weight solve.
  3. Matched filter: for each generic correlation direction, fit the
     measurement residual with a thin-stripe line basis; keep the best
     direction (data picks it).
  4. Joint convex weight least-squares over blobs + stripes; prune.
  5. Nonlinear Adam polish (analytic full-cov gradient) to refine shapes.
  6. Final convex weight cleanup (removes weight overfit the polish can add;
     the loss's global min at finite shots slightly favours overfitting, so the
     convex solution on the polished shapes is the honest weight vector).

Loss is identical to fit2 (histogram L2 + negativity + sum-to-1) for a fair
comparison. adapt2f (the real 3DGS split along the 4D principal eigenvector)
and birth_field2f (the anisotropic weight-gradient field) are provided and
tested as densification primitives.
"""

import numpy as np

from .data2 import histogram_targets2
from .forward2f import SplatMixture2F, _U, _TRIL_I, _TRIL_J, _DIAG


def _pack2f(m):
    return np.concatenate([m.w, m.mu.ravel(), m.ld.ravel(), m.lo.ravel()])


def _unpack2f(v, K):
    w = v[:K]
    mu = v[K : 5 * K].reshape(K, 4)
    ld = v[5 * K : 9 * K].reshape(K, 4)
    lo = v[9 * K : 15 * K].reshape(K, 6)
    return SplatMixture2F(w, mu, ld, lo)


def loss2f(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0):
    total = 0.0
    for (th1, th2), hist in targets:
        model = mixture.radon2(centers, centers, th1, th2)
        total += np.mean((model - hist) ** 2)
        total += lambda_neg * np.mean(np.minimum(model, 0.0) ** 2)
    total += lambda_sum * (mixture.w.sum() - 1.0) ** 2
    return total


def loss_and_grad2f(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0):
    """Loss and its analytic gradient, packed like _pack2f, vectorized over pairs.

    For a 2D Gaussian N(x; m, C): dN/dm = N P d, dN/dC = (N/2)(P d d^T P - P),
    P = C^{-1}, d = x - m. Chain: dL/dmu = sum_pairs U dL/dm,
    dL/dSigma = sum_pairs U (dL/dC) U^T, and Sigma = L L^T gives
    dL/dL = 2 (dL/dSigma) L (lower triangle; diagonal scaled by exp(ld)). The
    per-cell moment sums of the (P, B, B, K) Gaussian tensor are contracted with
    einsum. Central-difference tested to rtol 1e-5.
    """
    K = len(mixture.w)
    B = len(centers)
    w = mixture.w

    th = np.array([a for a, _ in targets])                # (P, 2)
    hist = np.array([h for _, h in targets])              # (P, B, B)
    th1, th2 = th[:, 0], th[:, 1]
    P = len(th)

    U = np.zeros((P, 4, 2))
    U[:, 0, 0], U[:, 1, 0] = np.cos(th1), np.sin(th1)
    U[:, 2, 1], U[:, 3, 1] = np.cos(th2), np.sin(th2)

    L = mixture.L()                                       # (K, 4, 4)
    Sigma = L @ L.transpose(0, 2, 1)

    m = np.einsum("par,ka->pkr", U, mixture.mu)           # (P, K, 2)
    C = np.einsum("par,kab,pbs->pkrs", U, Sigma, U)       # (P, K, 2, 2)
    Prec = np.linalg.inv(C)
    detC = np.linalg.det(C)
    P00, P01, P11 = Prec[..., 0, 0], Prec[..., 0, 1], Prec[..., 1, 1]

    d1 = centers[None, :, None] - m[:, None, :, 0]        # (P, B, K)
    d2 = centers[None, :, None] - m[:, None, :, 1]
    quad = (
        P00[:, None, None, :] * d1[:, :, None, :] ** 2
        + 2 * P01[:, None, None, :] * d1[:, :, None, :] * d2[:, None, :, :]
        + P11[:, None, None, :] * d2[:, None, :, :] ** 2
    )                                                     # (P, B, B, K)
    Nker = np.exp(-quad / 2) / (2 * np.pi * np.sqrt(detC)[:, None, None, :])

    model = np.einsum("pijk,k->pij", Nker, w)
    resid = model - hist
    neg = np.minimum(model, 0.0)
    total = np.sum(np.mean(resid ** 2, axis=(1, 2))) + lambda_neg * np.sum(
        np.mean(neg ** 2, axis=(1, 2))
    )
    r = (2.0 / (B * B)) * (resid + lambda_neg * neg)      # (P, B, B) = dL/dmodel

    rN = r[..., None] * Nker
    rNi = rN.sum(axis=2)                                  # (P, B, K)
    rNj = rN.sum(axis=1)

    A = rNi.sum(axis=1)                                   # (P, K)
    Sd1 = np.einsum("pik,pik->pk", d1, rNi)
    Sd11 = np.einsum("pik,pik->pk", d1 ** 2, rNi)
    Sd2 = np.einsum("pjk,pjk->pk", d2, rNj)
    Sd22 = np.einsum("pjk,pjk->pk", d2 ** 2, rNj)
    Sd12 = np.einsum("pik,pjk,pijk->pk", d1, d2, rN)

    gw = A.sum(axis=0)

    gm0 = w * (P00 * Sd1 + P01 * Sd2)
    gm1 = w * (P01 * Sd1 + P11 * Sd2)
    gm = np.stack([gm0, gm1], axis=-1)                    # (P, K, 2)

    M00 = P00 ** 2 * Sd11 + 2 * P00 * P01 * Sd12 + P01 ** 2 * Sd22
    M01 = P00 * P01 * Sd11 + (P00 * P11 + P01 ** 2) * Sd12 + P01 * P11 * Sd22
    M11 = P01 ** 2 * Sd11 + 2 * P01 * P11 * Sd12 + P11 ** 2 * Sd22
    gC = np.empty((P, K, 2, 2))
    gC[..., 0, 0] = 0.5 * w * (M00 - P00 * A)
    gC[..., 0, 1] = gC[..., 1, 0] = 0.5 * w * (M01 - P01 * A)
    gC[..., 1, 1] = 0.5 * w * (M11 - P11 * A)

    gmu = np.einsum("par,pkr->ka", U, gm)                 # (K, 4)
    gSigma = np.einsum("par,pkrs,pbs->kab", U, gC, U)     # (K, 4, 4)
    gL = 2 * np.einsum("kab,kbc->kac", gSigma, L)
    gld = gL[:, _DIAG, _DIAG] * np.exp(mixture.ld)
    glo = gL[:, _TRIL_I, _TRIL_J]

    wsum = w.sum() - 1.0
    total += lambda_sum * wsum ** 2
    gw = gw + 2 * lambda_sum * wsum
    return total, np.concatenate([gw, gmu.ravel(), gld.ravel(), glo.ravel()])


# ----------------------------------------------------------------------------
# densification primitives (tested; the recipe below uses the convex matched
# filter, but these are the direct 3DGS analogs)

def _principal_axis(Sigma_k):
    """Unit eigenvector of the largest eigenvalue and its sqrt-eigenvalue."""
    vals, vecs = np.linalg.eigh(Sigma_k)
    i = int(np.argmax(vals))
    return vecs[:, i], np.sqrt(max(vals[i], 1e-12))


def adapt2f(mixture, m1, m2, gnorm, K_max, prune_weight=5e-3, split_rel=2.0,
            split_factor=1.6, split_offset=0.6):
    """One densification/pruning step: the real 3DGS split in 4D phase space.

    Prunes |w| < prune_weight. Splits splats whose accumulated 4D positional
    gradient norm exceeds split_rel * median into two half-weight children,
    offset by split_offset * sqrt(lambda_max) along the PRINCIPAL EIGENVECTOR of
    the 4D covariance (fit2 could only split inside one mode's plane), with the
    covariance shrunk along that axis by split_factor (rank-1 downdate). Adam
    moments follow the row selection and children inherit the parent's moments
    (fit.adapt warm-start policy). Returns (mixture, m1, m2).
    """
    K = len(mixture.w)
    keep = np.abs(mixture.w) >= prune_weight
    if not keep.any():
        keep[np.argmax(np.abs(mixture.w))] = True
    kept = np.flatnonzero(keep)
    budget = max(K_max - len(kept), 0)
    thresh = split_rel * np.median(gnorm[kept])
    by_norm = kept[np.argsort(-gnorm[kept])]
    split = set(k for k in by_norm[:budget] if gnorm[k] > thresh)

    parents, signs = [], []
    for k in kept:
        if k in split:
            parents += [k, k]
            signs += [-1.0, 1.0]
        else:
            parents.append(k)
            signs.append(0.0)
    parents, signs = np.array(parents), np.array(signs)

    def gather_v(v):
        m = _unpack2f(v, K)
        return _pack2f(SplatMixture2F(m.w[parents], m.mu[parents],
                                      m.ld[parents], m.lo[parents]))

    new = SplatMixture2F(mixture.w[parents], mixture.mu[parents].copy(),
                         mixture.ld[parents].copy(), mixture.lo[parents].copy())
    m1n, m2n = gather_v(m1), gather_v(m2)
    child = signs != 0.0
    if child.any():
        Sigma = new.Sigma()
        for row in np.flatnonzero(child):
            axis, sig = _principal_axis(Sigma[row])
            new.mu[row] += signs[row] * split_offset * sig * axis
            c = (1.0 - 1.0 / split_factor ** 2) * sig ** 2
            Sig_new = Sigma[row] - c * np.outer(axis, axis) + 1e-9 * np.eye(4)
            Ln = np.linalg.cholesky(Sig_new)
            new.ld[row] = np.log(np.diag(Ln))
            new.lo[row] = Ln[_TRIL_I, _TRIL_J]
        new.w[child] *= 0.5
    return new, m1n, m2n


# generic two-mode correlation directions: pairwise sums/differences of the two
# modes' quadratures, plus the single-mode axes. No knowledge of the true state
# -- these are the natural anisotropy axes of ANY two-mode Gaussian correlation,
# and the residual (data) picks which one resonates.
STRIPE_DIRS = [
    np.array([0.0, 1.0, 0.0, 1.0]),   # p1 + p2
    np.array([0.0, 1.0, 0.0, -1.0]),  # p1 - p2
    np.array([1.0, 0.0, 1.0, 0.0]),   # x1 + x2
    np.array([1.0, 0.0, -1.0, 0.0]),  # x1 - x2
    np.array([0.0, 1.0, 0.0, 0.0]),   # p1
    np.array([0.0, 0.0, 0.0, 1.0]),   # p2
    np.array([1.0, 0.0, 0.0, 0.0]),   # x1
    np.array([0.0, 0.0, 1.0, 0.0]),   # x2
]


def _probe_cov(direction, thin=0.05, base=0.5):
    """A stripe covariance: variance `thin` along `direction`, `base` across.

    A splat with this covariance is a thin sheet perpendicular to `direction`
    (broad along the ridge, narrow across it), the shape a single fringe stripe
    needs. Returns a (4, 4) SPD matrix.
    """
    v = np.asarray(direction, float)
    v = v / np.linalg.norm(v)
    return base * np.eye(4) - (base - thin) * np.outer(v, v)


def _cov_to_chol(Sigma):
    L = np.linalg.cholesky(Sigma + 1e-9 * np.eye(4))
    return np.log(np.diag(L)), L[_TRIL_I, _TRIL_J]


def _col(mu0, ld0, lo0, centers, targets):
    """Flattened radon2 of a unit-weight splat over all (pair, bin, bin)."""
    sp = SplatMixture2F([1.0], [mu0], [ld0], [lo0])
    return np.array(
        [sp.radon2(centers, centers, t1, t2) for (t1, t2), _ in targets]
    ).ravel()


def weight_ls(mixture, centers, targets, hist_stack=None, reg=1e-5, thr=0.02):
    """Convex least-squares refit of the weights (shapes fixed), then prune.

    Solves min_w || A w - hist ||^2 + reg||w||^2 with A the columns of each
    splat's flattened radon2, then drops splats with |w| < thr * max|w|. This is
    the linear (hence non-overfitting-in-shape) core: it sets blob vs fringe
    amplitudes optimally and cleans up any weight drift from the nonlinear
    polish. Returns a new mixture.
    """
    if hist_stack is None:
        hist_stack = np.array([h for _, h in targets]).ravel()
    K = len(mixture.w)
    A = np.array([_col(mixture.mu[k], mixture.ld[k], mixture.lo[k], centers, targets)
                  for k in range(K)]).T
    n = A.shape[1]
    lam = reg * np.trace(A.T @ A) / n
    w = np.linalg.solve(A.T @ A + lam * np.eye(n), A.T @ hist_stack)
    keep = np.abs(w) >= thr * np.abs(w).max()
    if not keep.any():
        keep[np.argmax(np.abs(w))] = True
    idx = np.flatnonzero(keep)
    return SplatMixture2F(w[idx], mixture.mu[idx], mixture.ld[idx], mixture.lo[idx])


def matched_stripes(mixture, centers, targets, thin=0.05, T=2.8, M=21,
                    dirs=STRIPE_DIRS, hist_stack=None):
    """Fit the current measurement residual with a thin-stripe line basis.

    For each generic direction, the candidate stripe centers are a line through
    the origin along that direction (the natural locus for a probe thin along
    it); a least-squares fit of the residual over that basis measures how well
    the direction explains the fringe. The best direction is kept (the data
    chooses it). Returns (stripe_mus (m,4), stripe_ld (4,), stripe_lo (6,),
    direction (4,)). The caller appends these stripes and refits weights.
    """
    if hist_stack is None:
        hist_stack = np.array([h for _, h in targets]).ravel()
    model = np.array(
        [mixture.radon2(centers, centers, t1, t2) for (t1, t2), _ in targets]
    ).ravel()
    resid = hist_stack - model
    ts = np.linspace(-T, T, M)
    best = None
    for d in dirs:
        vh = np.asarray(d, float)
        vh = vh / np.linalg.norm(vh)
        ld0, lo0 = _cov_to_chol(_probe_cov(d, thin))
        A = np.array([_col(t * vh, ld0, lo0, centers, targets) for t in ts]).T
        lam = 1e-5 * np.trace(A.T @ A) / A.shape[1]
        c = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ resid)
        red = np.linalg.norm(resid - A @ c)
        if best is None or red < best[0]:
            best = (red, vh, ld0, lo0)
    _, vh, ld0, lo0 = best
    mus = np.array([t * vh for t in ts])
    return mus, ld0, lo0, vh


# ----------------------------------------------------------------------------

def birth_field2f(mixture, centers, targets, candidates, Sigma_probe,
                  lambda_neg=10.0, chunk=2048, _Ds=None):
    """dL/dw for a probe splat with covariance Sigma_probe at each 4D candidate.

    The weight gradient of a hypothetical new splat is the current residual
    back-projected through the probe's (correlated) kernel -- closed form. With
    a thin anisotropic probe this resonates with fringe stripes an isotropic
    probe would smear over. Where large and positive the model needs NEGATIVE
    mass, so the field both places and signs newborn splats. Returns (G,).
    """
    if _Ds is None:
        B = len(centers)
        _Ds = []
        for (th1, th2), hist in targets:
            model = mixture.radon2(centers, centers, th1, th2)
            D = (2.0 / (B * B)) * ((model - hist) + lambda_neg * np.minimum(model, 0.0))
            _Ds.append((th1, th2, D))
    field = np.zeros(len(candidates))
    for lo in range(0, len(candidates), chunk):
        cand = candidates[lo : lo + chunk]
        acc = np.zeros(len(cand))
        for th1, th2, D in _Ds:
            U = _U(th1, th2)
            C = U.T @ Sigma_probe @ U
            Prec = np.linalg.inv(C)
            det = np.linalg.det(C)
            mp = cand @ U
            d1 = centers[None, :] - mp[:, 0:1]
            d2 = centers[None, :] - mp[:, 1:2]
            q = (
                Prec[0, 0] * d1[:, :, None] ** 2
                + 2 * Prec[0, 1] * d1[:, :, None] * d2[:, None, :]
                + Prec[1, 1] * d2[:, None, :] ** 2
            )
            gk = np.exp(-q / 2) / (2 * np.pi * np.sqrt(det))
            acc += np.einsum("gij,ij->g", gk, D)
        field[lo : lo + chunk] = acc
    return field


# ----------------------------------------------------------------------------

def _adam(v, K, centers, targets, iters, lr, lr_late=None, lambda_neg=10.0,
          lambda_sum=1.0):
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    half = iters // 2
    for t in range(1, iters + 1):
        step_lr = lr if (lr_late is None or t < half) else lr_late
        _, g = loss_and_grad2f(_unpack2f(v, K), centers, targets,
                               lambda_neg=lambda_neg, lambda_sum=lambda_sum)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        v = v - step_lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
    return v


def blob_span(data):
    """Data-driven blob half-separation from the max per-angle x-variance.

    Two blobs at +-span plus vacuum give Var(x_theta) = span^2 + 1/2 at the
    angle measuring their separation axis; the max over angle pairs estimates
    span without any knowledge of the true amplitude. Floored for robustness.
    """
    return float(np.sqrt(max(max(np.var(s[:, 0]) for _, s in data) - 0.5, 0.25)))


def fit2f(data, bins=40, blob_iters=350, blob_lr=0.05, blob_prune=0.08,
          stripe_thin=0.05, stripe_T=2.8, stripe_M=21, ls_prune=0.02,
          polish_iters=350, polish_lr=0.02, polish_lr_late=0.008,
          lambda_neg=10.0, lambda_sum=1.0, callback=None):
    """Fit a full-covariance signed splat mixture to two-mode homodyne data.

    Deterministic given the data (the blob envelope is initialized from the
    measured variance, not a random seed). See the module docstring for the
    staged recipe. Returns the fitted SplatMixture2F.
    """
    centers, targets = histogram_targets2(data, bins=bins)
    hist_stack = np.array([h for _, h in targets]).ravel()

    # 1. positive blob envelope, initialized from the data
    span = blob_span(data)
    mix = SplatMixture2F(
        w=np.full(4, 0.25),
        mu=[[span, 0, span, 0], [-span, 0, -span, 0],
            [span, 0, -span, 0], [-span, 0, span, 0]],
        ld=np.full((4, 4), np.log(0.8)), lo=np.zeros((4, 6)),
    )
    K = 4
    v = _adam(_pack2f(mix), K, centers, targets, blob_iters, blob_lr,
              lambda_neg=lambda_neg, lambda_sum=lambda_sum)
    mix = _unpack2f(v, K)

    # 2. prune spurious blobs
    mix = weight_ls(mix, centers, targets, hist_stack, thr=blob_prune)
    if callback:
        callback("blobs", mix, len(mix.w))

    # 3-4. matched-filter fringe + joint convex weight solve
    mus, ld0, lo0, _ = matched_stripes(mix, centers, targets, thin=stripe_thin,
                                       T=stripe_T, M=stripe_M, hist_stack=hist_stack)
    m = len(mus)
    dic = SplatMixture2F(
        np.ones(len(mix.w) + m),
        np.vstack([mix.mu, mus]),
        np.vstack([mix.ld, np.tile(ld0, (m, 1))]),
        np.vstack([mix.lo, np.tile(lo0, (m, 1))]),
    )
    mix = weight_ls(dic, centers, targets, hist_stack, thr=ls_prune)
    K = len(mix.w)
    if callback:
        callback("stripes", mix, K)

    # 5. nonlinear polish
    v = _adam(_pack2f(mix), K, centers, targets, polish_iters, polish_lr,
              lr_late=polish_lr_late, lambda_neg=lambda_neg, lambda_sum=lambda_sum)
    mix = _unpack2f(v, K)

    # 6. convex weight cleanup
    mix = weight_ls(mix, centers, targets, hist_stack, thr=ls_prune)
    if callback:
        callback("polished", mix, len(mix.w))
    return mix
