"""Full-covariance three-mode reconstructor -- fit2f lifted to 6D phase space.

The staged recipe is identical to fit2f (the two-mode result that reached
fid ~0.92-0.93, beating the Fock MLE): a data-initialized positive blob
envelope, a convex matched-filter over a thin-stripe basis aligned to the
entangled fringe ridge (the fringe is LINEAR in the stripe weights), an Adam
polish with the analytic full-covariance gradient, and a convex weight cleanup.

The one genuinely new ingredient is ridge DETECTION. In two modes the fringe
cos(2 sqrt2 a (p1+p2)) is constant along p1+p2, a single generic axis. In three
modes cos(2 sqrt2 a (p1+p2+p3)) is constant on the 2D plane orthogonal to
(p1+p2+p3)/sqrt3 within p-space, and that ridge direction must be found from the
data: matched_stripes scores every generic candidate axis (all sign patterns of
(p_i +- p_j +- p_k)/sqrt3 plus the per-mode p and x axes) by residual reduction
and keeps the best -- the data picks (p1+p2+p3)/sqrt3, it is never hardcoded.

Loss is the same histogram L2 + negativity + sum-to-1 as fit2f. The loss pass
holds one triple's (B,B,B,K) Gaussian tensor at a time (chunked over the 27
triples) to bound memory. The analytic gradient is central-difference tested to
rtol 1e-5.
"""

import numpy as np

from .data3 import histogram_targets3
from .fock_project import psd_penalty, rho_component
from .forward3f import SplatMixture3F, _U, _TRIL_I, _TRIL_J, _DIAG


def _pack3f(m):
    return np.concatenate([m.w, m.mu.ravel(), m.ld.ravel(), m.lo.ravel()])


def _unpack3f(v, K):
    w = v[:K]
    mu = v[K : 7 * K].reshape(K, 6)
    ld = v[7 * K : 13 * K].reshape(K, 6)
    lo = v[13 * K : 28 * K].reshape(K, 15)
    return SplatMixture3F(w, mu, ld, lo)


def cell_var(centers):
    """Bin-average variance h^2/12 for the shared histogram grid (see radon3)."""
    h = float(centers[1] - centers[0])
    return h ** 2 / 12.0


def loss3f(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0,
           cvar=None, eta=1.0, extra_noise_var=0.0):
    cvar = cell_var(centers) if cvar is None else cvar
    total = 0.0
    for (th1, th2, th3), hist in targets:
        model = mixture.radon3(centers, centers, centers, th1, th2, th3,
                               cell_var=cvar, eta=eta,
                               extra_noise_var=extra_noise_var)
        total += np.mean((model - hist) ** 2)
        total += lambda_neg * np.mean(np.minimum(model, 0.0) ** 2)
    total += lambda_sum * (mixture.w.sum() - 1.0) ** 2
    return total


def loss_and_grad3f(mixture, centers, targets, lambda_neg=10.0, lambda_sum=1.0,
                    cvar=None, eta=1.0, extra_noise_var=0.0):
    """Loss and its analytic gradient, packed like _pack3f, chunked over triples.

    For a 3D Gaussian N(x; m, C): dN/dm = N P d, dN/dC = (N/2)(P d d^T P - P),
    P = C^{-1}, d = x - m. Chain: dL/dmu = sum_triples U dL/dm,
    dL/dSigma = sum_triples U (dL/dC) U^T, and Sigma = L L^T gives
    dL/dL = 2 (dL/dSigma) L (diagonal scaled by exp(ld)). One triple's
    (B,B,B,K) Gaussian tensor is held at a time; its per-axis moment marginals
    are contracted with einsum. Central-difference tested to rtol 1e-5.

    eta / extra_noise_var (issue #42): the measurement map of radon3,
    m -> sqrt(eta) m, C -> eta C + sigma2 I. The chain rule only scales the
    back-projected gradients: dL/dmu picks up sqrt(eta), dL/dSigma picks up
    eta (sigma2 I is parameter free).
    """
    cvar = cell_var(centers) if cvar is None else cvar
    if eta != 1.0 or extra_noise_var != 0.0:
        from .bbdagS import _check_loss_params
        _check_loss_params(eta, extra_noise_var)
    sqrt_eta = np.sqrt(eta)
    sigma2 = (1.0 - eta) / 2.0 + extra_noise_var
    K = len(mixture.w)
    B = len(centers)
    w = mixture.w
    L = mixture.L()                                       # (K, 6, 6)
    Sigma = L @ L.transpose(0, 2, 1)

    total = 0.0
    gmu = np.zeros((K, 6))
    gSigma = np.zeros((K, 6, 6))
    gw = np.zeros(K)
    norm3 = B ** 3

    for (th1, th2, th3), hist in targets:
        U = _U(th1, th2, th3)                             # (6, 3)
        m = sqrt_eta * (mixture.mu @ U)                   # (K, 3)
        C = eta * np.einsum("ar,kab,bs->krs", U, Sigma, U)  # (K, 3, 3)
        C = C + (sigma2 + cvar) * np.eye(3) if (sigma2 or cvar) else C
        Prec = np.linalg.inv(C)
        det = np.linalg.det(C)
        pref = 1.0 / ((2 * np.pi) ** 1.5 * np.sqrt(det))  # (K,)

        d1 = centers[:, None] - m[:, 0]                   # (B, K)
        d2 = centers[:, None] - m[:, 1]
        d3 = centers[:, None] - m[:, 2]

        quad = (
            Prec[:, 0, 0] * d1[:, None, None, :] ** 2
            + Prec[:, 1, 1] * d2[None, :, None, :] ** 2
            + Prec[:, 2, 2] * d3[None, None, :, :] ** 2
            + 2 * Prec[:, 0, 1] * d1[:, None, None, :] * d2[None, :, None, :]
            + 2 * Prec[:, 0, 2] * d1[:, None, None, :] * d3[None, None, :, :]
            + 2 * Prec[:, 1, 2] * d2[None, :, None, :] * d3[None, None, :, :]
        )                                                 # (B, B, B, K)
        Nker = np.exp(-quad / 2) * pref

        model = np.einsum("ijlk,k->ijl", Nker, w)
        resid = model - hist
        neg = np.minimum(model, 0.0)
        total += np.mean(resid ** 2) + lambda_neg * np.mean(neg ** 2)
        r = (2.0 / norm3) * (resid + lambda_neg * neg)    # (B, B, B)

        rN = r[..., None] * Nker                          # (B, B, B, K)
        A = rN.sum(axis=(0, 1, 2))                        # (K,)
        rN_i = rN.sum(axis=(1, 2))                        # (B, K)
        rN_j = rN.sum(axis=(0, 2))
        rN_l = rN.sum(axis=(0, 1))
        rN_ij = rN.sum(axis=2)                            # (B, B, K)
        rN_il = rN.sum(axis=1)
        rN_jl = rN.sum(axis=0)

        Sd1 = np.einsum("ik,ik->k", d1, rN_i)
        Sd2 = np.einsum("jk,jk->k", d2, rN_j)
        Sd3 = np.einsum("lk,lk->k", d3, rN_l)
        Sd11 = np.einsum("ik,ik->k", d1 ** 2, rN_i)
        Sd22 = np.einsum("jk,jk->k", d2 ** 2, rN_j)
        Sd33 = np.einsum("lk,lk->k", d3 ** 2, rN_l)
        Sd12 = np.einsum("ik,jk,ijk->k", d1, d2, rN_ij)
        Sd13 = np.einsum("ik,lk,ilk->k", d1, d3, rN_il)
        Sd23 = np.einsum("jk,lk,jlk->k", d2, d3, rN_jl)

        S1 = np.stack([Sd1, Sd2, Sd3], axis=-1)           # (K, 3)
        Mmat = np.empty((K, 3, 3))
        Mmat[:, 0, 0] = Sd11
        Mmat[:, 1, 1] = Sd22
        Mmat[:, 2, 2] = Sd33
        Mmat[:, 0, 1] = Mmat[:, 1, 0] = Sd12
        Mmat[:, 0, 2] = Mmat[:, 2, 0] = Sd13
        Mmat[:, 1, 2] = Mmat[:, 2, 1] = Sd23

        gm = w[:, None] * np.einsum("kab,kb->ka", Prec, S1)          # (K, 3)
        PMP = np.einsum("kab,kbc,kcd->kad", Prec, Mmat, Prec)
        gC = 0.5 * w[:, None, None] * (PMP - A[:, None, None] * Prec)  # (K,3,3)

        gmu += sqrt_eta * np.einsum("ar,kr->ka", U, gm)
        gSigma += eta * np.einsum("ar,krs,bs->kab", U, gC, U)
        gw += A

    gL = 2 * np.einsum("kab,kbc->kac", gSigma, L)
    gld = gL[:, _DIAG, _DIAG] * np.exp(mixture.ld)
    glo = gL[:, _TRIL_I, _TRIL_J]

    wsum = w.sum() - 1.0
    total += lambda_sum * wsum ** 2
    gw = gw + 2 * lambda_sum * wsum
    return total, np.concatenate([gw, gmu.ravel(), gld.ravel(), glo.ravel()])


# ----------------------------------------------------------------------------
# generic three-mode correlation directions in p-space. All distinct sign
# patterns of (p1 +- p2 +- p3)/sqrt3 (up to overall sign, 4 of them), plus the
# three per-mode p axes and the three per-mode x axes. No knowledge of the true
# state -- the fringe of ANY three-mode entangled cat lives on stripes
# perpendicular to ONE of these, and the residual (data) picks which resonates.
# For this cat the answer is (p1+p2+p3)/sqrt3, but it is scored, not assumed.
def _p(*signs):
    v = np.zeros(6)
    v[1], v[3], v[5] = signs
    return v


STRIPE_DIRS = [
    _p(1, 1, 1),   # p1 + p2 + p3   (the true ridge for |a,a,a>+|-a,-a,-a>)
    _p(1, 1, -1),  # p1 + p2 - p3
    _p(1, -1, 1),  # p1 - p2 + p3
    _p(1, -1, -1), # p1 - p2 - p3
    _p(1, 0, 0),   # p1
    _p(0, 1, 0),   # p2
    _p(0, 0, 1),   # p3
    np.array([1.0, 0, 0, 0, 0, 0]),   # x1
    np.array([0, 0, 1.0, 0, 0, 0]),   # x2
    np.array([0, 0, 0, 0, 1.0, 0]),   # x3
]


def _probe_cov(direction, thin=0.05, base=0.5):
    """A 6D stripe covariance: variance `thin` along `direction`, `base` across.

    A splat with this covariance is a thin sheet perpendicular to `direction`
    (broad along the orthogonal p-plane and the x-directions, narrow across the
    ridge), the shape a single fringe stripe needs. Returns a (6, 6) SPD matrix.
    """
    v = np.asarray(direction, float)
    v = v / np.linalg.norm(v)
    return base * np.eye(6) - (base - thin) * np.outer(v, v)


def _cov_to_chol(Sigma):
    L = np.linalg.cholesky(Sigma + 1e-9 * np.eye(6))
    return np.log(np.diag(L)), L[_TRIL_I, _TRIL_J]


def _col(mu0, ld0, lo0, centers, targets, cvar=0.0, eta=1.0,
         extra_noise_var=0.0):
    """Flattened radon3 of a unit-weight splat over all (triple, bin, bin, bin)."""
    sp = SplatMixture3F([1.0], [mu0], [ld0], [lo0])
    return np.concatenate(
        [sp.radon3(centers, centers, centers, t1, t2, t3, cell_var=cvar,
                   eta=eta, extra_noise_var=extra_noise_var).ravel()
         for (t1, t2, t3), _ in targets]
    )


def weight_ls(mixture, centers, targets, hist_stack=None, reg=1e-5, thr=0.02,
              cvar=None, eta=1.0, extra_noise_var=0.0):
    """Convex least-squares refit of the weights (shapes fixed), then prune.

    Solves min_w || A w - hist ||^2 + reg||w||^2 with A the columns of each
    splat's flattened radon3, then drops splats with |w| < thr * max|w|. The
    linear (non-overfitting-in-shape) core: it sets blob vs fringe amplitudes
    optimally. Returns a new mixture.
    """
    cvar = cell_var(centers) if cvar is None else cvar
    if hist_stack is None:
        hist_stack = np.concatenate([h.ravel() for _, h in targets])
    K = len(mixture.w)
    A = np.array([_col(mixture.mu[k], mixture.ld[k], mixture.lo[k], centers,
                       targets, cvar, eta, extra_noise_var)
                  for k in range(K)]).T
    n = A.shape[1]
    lam = reg * np.trace(A.T @ A) / n
    w = np.linalg.solve(A.T @ A + lam * np.eye(n), A.T @ hist_stack)
    keep = np.abs(w) >= thr * np.abs(w).max()
    if not keep.any():
        keep[np.argmax(np.abs(w))] = True
    idx = np.flatnonzero(keep)
    return SplatMixture3F(w[idx], mixture.mu[idx], mixture.ld[idx], mixture.lo[idx])


def matched_stripes(mixture, centers, targets, thin=0.05, T=2.8, M=17,
                    dirs=STRIPE_DIRS, hist_stack=None, cvar=None, eta=1.0,
                    extra_noise_var=0.0):
    """Fit the current measurement residual with a thin-stripe line basis.

    For each generic candidate direction the stripe centers are a line through
    the origin along that direction (the natural locus for a probe thin along
    it); a least-squares fit of the residual over that basis measures how well
    the direction explains the fringe. The best direction is kept (the DATA
    chooses the ridge -- (p1+p2+p3)/sqrt3 here, never hardcoded). Returns
    (stripe_mus (M,6), stripe_ld (6,), stripe_lo (15,), direction (6,)).
    """
    cvar = cell_var(centers) if cvar is None else cvar
    if hist_stack is None:
        hist_stack = np.concatenate([h.ravel() for _, h in targets])
    model = np.concatenate(
        [mixture.radon3(centers, centers, centers, t1, t2, t3,
                        cell_var=cvar, eta=eta,
                        extra_noise_var=extra_noise_var).ravel()
         for (t1, t2, t3), _ in targets]
    )
    resid = hist_stack - model
    ts = np.linspace(-T, T, M)
    best = None
    for d in dirs:
        vh = np.asarray(d, float)
        vh = vh / np.linalg.norm(vh)
        ld0, lo0 = _cov_to_chol(_probe_cov(d, thin))
        A = np.array([_col(t * vh, ld0, lo0, centers, targets, cvar, eta,
                           extra_noise_var)
                      for t in ts]).T
        lam = 1e-5 * np.trace(A.T @ A) / A.shape[1]
        c = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ resid)
        red = np.linalg.norm(resid - A @ c)
        if best is None or red < best[0]:
            best = (red, vh, ld0, lo0)
    _, vh, ld0, lo0 = best
    mus = np.array([t * vh for t in ts])
    return mus, ld0, lo0, vh


# ----------------------------------------------------------------------------

def _adam(v, K, centers, targets, iters, lr, lr_late=None, lambda_neg=10.0,
          lambda_sum=1.0, cvar=None, eta=1.0, extra_noise_var=0.0):
    m1, m2 = np.zeros_like(v), np.zeros_like(v)
    half = iters // 2
    for t in range(1, iters + 1):
        step_lr = lr if (lr_late is None or t < half) else lr_late
        _, g = loss_and_grad3f(_unpack3f(v, K), centers, targets,
                               lambda_neg=lambda_neg, lambda_sum=lambda_sum,
                               cvar=cvar, eta=eta,
                               extra_noise_var=extra_noise_var)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        v = v - step_lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
    return v


def blob_span(data, eta=1.0, extra_noise_var=0.0):
    """Data-driven blob half-separation from the max per-triple x-variance.

    Two blobs at +-span (per mode) plus vacuum give Var(x_theta) = span^2 + 1/2
    at the angle measuring their separation axis; the max over triples/modes
    estimates span without any knowledge of the true amplitude. Floored.

    Under detection loss the measured variance is eta (span^2 + 1/2) + sigma2,
    so the PRE-loss span the noise-aware model needs is recovered by
    inverting that map (identity at eta = 1, sigma2 = 0).
    """
    sigma2 = (1.0 - eta) / 2.0 + extra_noise_var
    v = max(np.var(s[:, j]) for _, s in data for j in range(3))
    return float(np.sqrt(max((v - sigma2) / eta - 0.5, 0.25)))


def fit3f(data, bins=24, blob_iters=250, blob_lr=0.05, blob_prune=0.08,
          stripe_thin=0.03, stripe_T=2.8, stripe_M=17, ls_prune=0.02,
          polish_iters=0, polish_lr=0.02, polish_lr_late=0.008,
          lambda_neg=10.0, lambda_sum=1.0, callback=None, eta=1.0,
          extra_noise_var=0.0):
    """Fit a full-covariance signed splat mixture to three-mode homodyne data.

    Deterministic given the data (the blob envelope is initialized from the
    measured variance, not a random seed). See the module docstring for the
    staged recipe. Returns the fitted SplatMixture3F.

    ``polish_iters`` defaults to 0 -- the nonlinear Adam SHAPE polish is DISABLED
    for the three-mode default. This is a measured finding, not an oversight:
    at the plan's budget (24^3 = 13824 cells, 2000 shots/triple => ~0.14
    counts/cell) the histogram-MSE loss minimum sits BELOW the true state, so a
    nonlinear polish reliably lowers the loss while lowering the fidelity
    (fitting shot noise with shape distortions). The convex matched-filter +
    weight solve -- linear in the splat weights, hence non-overfitting in shape
    -- is the honest estimator here. The polish machinery (loss_and_grad3f,
    _adam) is fully implemented and gradient-checked; set polish_iters > 0 to
    re-enable it for denser data. See tests/test_three_mode_full.py for the
    ceiling analysis (loss-min fidelity ~0.75-0.84; the true state is not the
    loss minimum at this shot budget).

    ``eta`` / ``extra_noise_var`` (issue #42): known detection efficiency and
    electronic noise of the data. Every stage then fits through the measured
    forward model (radon3's loss map), so the returned mixture estimates the
    PRE-loss Wigner function. Defaults reproduce the ideal-detector fit
    exactly.
    """
    centers, targets = histogram_targets3(data, bins=bins)
    hist_stack = np.concatenate([h.ravel() for _, h in targets])
    cvar = cell_var(centers)
    noise = dict(eta=eta, extra_noise_var=extra_noise_var)

    # 1. positive blob envelope on the (x1,x2,x3) diagonal, data-initialized
    span = blob_span(data, eta=eta, extra_noise_var=extra_noise_var)
    mix = SplatMixture3F(
        w=np.full(2, 0.5),
        mu=[[span, 0, span, 0, span, 0], [-span, 0, -span, 0, -span, 0]],
        ld=np.full((2, 6), np.log(0.8)), lo=np.zeros((2, 15)),
    )
    K = 2
    v = _adam(_pack3f(mix), K, centers, targets, blob_iters, blob_lr,
              lambda_neg=lambda_neg, lambda_sum=lambda_sum, cvar=cvar,
              **noise)
    mix = _unpack3f(v, K)

    # 2. prune spurious blobs
    mix = weight_ls(mix, centers, targets, hist_stack, thr=blob_prune,
                    cvar=cvar, **noise)
    if callback:
        callback("blobs", mix, len(mix.w))

    # 3-4. matched-filter fringe (ridge detected from data) + convex weight solve
    mus, ld0, lo0, direction = matched_stripes(
        mix, centers, targets, thin=stripe_thin, T=stripe_T, M=stripe_M,
        hist_stack=hist_stack, cvar=cvar, **noise)
    m = len(mus)
    dic = SplatMixture3F(
        np.ones(len(mix.w) + m),
        np.vstack([mix.mu, mus]),
        np.vstack([mix.ld, np.tile(ld0, (m, 1))]),
        np.vstack([mix.lo, np.tile(lo0, (m, 1))]),
    )
    mix = weight_ls(dic, centers, targets, hist_stack, thr=ls_prune,
                    cvar=cvar, **noise)
    K = len(mix.w)
    if callback:
        callback("stripes", mix, K, direction)

    # 5. nonlinear polish (disabled by default for thin three-mode data; see
    #    the docstring -- it lowers the loss but overfits shot noise into shapes)
    if polish_iters:
        v = _adam(_pack3f(mix), K, centers, targets, polish_iters, polish_lr,
                  lr_late=polish_lr_late, lambda_neg=lambda_neg,
                  lambda_sum=lambda_sum, cvar=cvar, **noise)
        mix = _unpack3f(v, K)

    # 6. convex weight cleanup
    mix = weight_ls(mix, centers, targets, hist_stack, thr=ls_prune,
                    cvar=cvar, **noise)
    if callback:
        callback("polished", mix, len(mix.w))
    return mix


def fit3f_psd(data, lambda_psd=1.0, n_max_psd=8, psd_polish_iters=100,
              psd_polish_lr=0.02, lambda_neg=10.0, lambda_sum=1.0, bins=24,
              **fit3f_kwargs):
    """fit3f() followed by a WEIGHT-ONLY PSD-polish stage (issue #8).

    Unlike fit_psd (1-mode: full-parameter finite-difference polish over
    weight, mean, AND shape), this touches only each splat's WEIGHT and holds
    mu/covariance FIXED at fit3f()'s matched-filter shapes. Measured cost of
    ONE fock_project.rho_component call at n_max=8, M=3 (this experiment's
    Fock cutoff) is ~1 s; with fit3f()'s typical K~16 splats and 28 shape
    params each, fit_psd's approach (finite-difference every packed entry)
    would cost tens of minutes PER ITERATION here. Holding shapes fixed makes
    rho LINEAR in the free variables: each component's (unweighted) rho is
    built ONCE up front (K rho_component calls -- the same cost as a single
    rho_from_splat call), and every polish iteration after that is just a
    weighted sum of K precomputed (n_max**3, n_max**3) matrices plus one
    eigvalsh -- the same convex-refit idea fit3f's own weight_ls step already
    uses (see its docstring), extended with the psd_penalty term. The
    original histogram-loss weight-gradient (loss_and_grad3f's first K packed
    entries) is analytic and combined as-is.

    fit3f()'s own recipe is untouched -- this calls it unmodified and ADDS a
    weight-only polish stage on its output (no regression to fit3f()).
    lambda_psd=0 or psd_polish_iters=0 returns fit3f()'s output unchanged.
    """
    mix = fit3f(data, bins=bins, **fit3f_kwargs)
    if psd_polish_iters == 0 or lambda_psd == 0.0:
        return mix

    K = len(mix.w)
    # unit_comps[k]: rho_component_k with weight 1 (rho_component bakes w_k
    # in, so divide it back out) -- rho(w) = sum_k w[k] * unit_comps[k].
    unit_comps = [
        rho_component(mix, k, n_max_psd) / mix.w[k] for k in range(K)
    ]

    centers, targets = histogram_targets3(data, bins=bins)
    cvar = cell_var(centers)
    w = mix.w.copy()
    m1, m2 = np.zeros_like(w), np.zeros_like(w)
    eps = 1e-3
    for t in range(1, psd_polish_iters + 1):
        cur = SplatMixture3F(w, mix.mu, mix.ld, mix.lo)
        _, g_full = loss_and_grad3f(cur, centers, targets,
                                     lambda_neg=lambda_neg,
                                     lambda_sum=lambda_sum, cvar=cvar)
        g_loss_w = g_full[:K]  # weight block is _pack3f's first K entries

        total = sum(w[k] * unit_comps[k] for k in range(K))
        g_psd_w = np.empty(K)
        for k in range(K):
            pen_p = psd_penalty(total + eps * unit_comps[k])
            pen_m = psd_penalty(total - eps * unit_comps[k])
            g_psd_w[k] = (pen_p - pen_m) / (2 * eps)

        g = g_loss_w + lambda_psd * g_psd_w
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g ** 2
        w = w - psd_polish_lr * (m1 / (1 - 0.9 ** t)) / (
            np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8
        )

    return SplatMixture3F(w, mix.mu, mix.ld, mix.lo)


# ----------------------------------------------------------------------------
# Issue #8 follow-up: does giving the fringe stripes' SHAPE a few degrees of
# freedom (not just weight) let a PSD polish shed 3-mode negativity without
# collapsing fidelity? fit3f_psd (weight-only) measured that it cannot
# (experiments/08_positivity/penalty_then_project_3mode.py); full per-splat
# shape polish (28 params/splat) is FD-computationally infeasible. This
# section adds the middle ground the issue brief calls out: a HANDFUL of
# GLOBAL fringe-shape scalars, FD-polished jointly with the weights.

def identify_stripes(mixture, ld0, lo0, atol=1e-9):
    """Boolean mask (K,) marking `mixture`'s fringe-stripe components.

    matched_stripes() (see its docstring) gives every stripe splat the SAME
    covariance Cholesky factor (ld0, lo0) -- only each stripe's mean differs
    (a point on the ridge line). This checks each component's OWN (ld, lo)
    against that shared template, so it stays correct no matter how many
    weight_ls prune passes ran between construction and the mixture handed in
    (fit3f() runs two: one right after matched_stripes, one in its final
    cleanup step) -- pruning only drops rows or reweights, it never touches a
    surviving row's own (ld, lo).
    """
    ld_match = np.all(np.isclose(mixture.ld, ld0, atol=atol), axis=1)
    lo_match = np.all(np.isclose(mixture.lo, lo0, atol=atol), axis=1)
    return ld_match & lo_match


def apply_shape_knobs(mixture, is_stripe, direction, thin=0.03, base=0.5,
                      thin_mult=1.0, base_mult=1.0, center_scale=1.0):
    """Reparameterize `mixture`'s fringe-stripe components by 3 GLOBAL shape
    scalars, holding blob components (and all weights) fixed.

    matched_stripes() builds every stripe splat from the SAME
    `_probe_cov(direction, thin, base)` (variance `thin` along the ridge,
    `base` across it) with a mean on the ridge line (mus[i] = t_i *
    direction); `is_stripe` marks those rows (identify_stripes). This
    rescales that one shared covariance by (thin_mult, base_mult) and each
    stripe mean's distance along the ridge by center_scale -- the "3-6 global
    fringe-shape parameters" the issue brief asks for, not a full per-splat
    re-optimization. `thin`/`base` must match the values fit3f()/
    matched_stripes() actually used to build `mixture` (matched_stripes()
    always calls `_probe_cov(d, thin)`, i.e. base is ALWAYS its default 0.5
    unless matched_stripes() itself is changed -- kept as this function's
    default too).

    All three multipliers must be positive. fit3f_shape_psd parameterizes them
    in log-space so its finite-difference probes stay inside the SPD domain.

    at (thin_mult, base_mult, center_scale) == (1, 1, 1) this is a no-op
    (identity reparameterization): new_ld/new_lo reproduce (ld0, lo0) exactly
    and mu is unchanged.
    """
    mu = mixture.mu.copy()
    ld = mixture.ld.copy()
    lo = mixture.lo.copy()
    if thin <= 0 or base <= 0 or thin_mult <= 0 or base_mult <= 0 or center_scale <= 0:
        raise ValueError("shape-knob scales must be positive")
    if np.any(is_stripe):
        new_ld, new_lo = _cov_to_chol(
            _probe_cov(direction, thin * thin_mult, base * base_mult))
        ld[is_stripe] = new_ld
        lo[is_stripe] = new_lo
        mu[is_stripe] = mu[is_stripe] * center_scale
    return SplatMixture3F(mixture.w, mu, ld, lo)


def fit3f_shape_psd(data, lambda_psd=1.0, n_max_psd=8, shape_polish_iters=25,
                    shape_polish_lr=0.05, weight_polish_lr=0.02,
                    stripe_thin=0.03, lambda_neg=10.0, lambda_sum=1.0,
                    bins=24, fd_eps=1e-3, **fit3f_kwargs):
    """fit3f() followed by a JOINT {weights + 3 global fringe-shape knobs}
    finite-difference PSD polish (issue #8 follow-up to fit3f_psd's
    weight-only polish).

    fit3f_psd showed that killing negativity by weight alone collapses
    3-mode fidelity (0.75 -> ~0.4, all tried lambda_psd -- see its docstring
    and experiments/08_positivity/penalty_then_project_3mode.py). This tests
    whether the missing degree of freedom is SHAPE: apply_shape_knobs's 3
    scalars (thin_mult, base_mult, center_scale) rescale the ONE shared
    covariance/mean-line every fringe-stripe splat shares (identify_stripes
    picks them out of fit3f()'s own output; blob components are untouched).

    Both the weights AND the 3 knobs descend the SAME combined objective
    (histogram data loss + lambda_psd * psd_penalty), so this is a fair test
    of "can shape freedom keep the fit AND fix positivity", not just "can
    shape kill negativity". Weights use fit3f_psd's gradient (analytic data
    loss + the linear-in-weight FD psd trick: each component's unweighted rho
    is built once per iteration). The knobs use central-difference FD on BOTH
    terms -- FD psd via rebuilt stripe rho, FD data loss via loss3f on the
    shaped mixture. Fidelity is still re-measured on the ACTUAL polished
    mixture (FD gradients only approximate the descent direction).

    Cost: rebuilding a stripe splat's rho_component (the expensive step, ~1 s
    at n_max_psd=8) happens (1 + 2*3) * S times per iteration -- once for the
    current knobs (feeds the weight-FD, reused via the same linear trick) and
    twice per knob for its central difference (S = number of stripe splats).
    Blob components never change shape, so their unit-weight rho is built
    ONCE outside the loop. Even with S in the low teens this is tens of
    seconds PER ITERATION at n_max_psd=8 -- keep shape_polish_iters small
    (the default 25 is already minutes, not seconds) or use a coarser
    n_max_psd when only mechanics (not the reported falsification numbers)
    are being exercised.

    fit3f()'s own recipe is untouched -- this calls it unmodified and ADDS a
    polish stage on its output (no regression to fit3f()). lambda_psd=0 or
    shape_polish_iters=0 returns fit3f()'s output unchanged. Because the
    stripe identity is carried by the matched-filter template, the wrapped
    fit3f() nonlinear shape polish must remain disabled (`polish_iters=0`;
    the default); a nonzero value is rejected rather than silently disabling
    this stage.
    """
    if fit3f_kwargs.get("polish_iters", 0) != 0:
        raise ValueError("fit3f_shape_psd requires polish_iters=0")

    direction_box = {}

    def _capture(name, mix, *rest):
        if name == "stripes":
            direction_box["direction"] = rest[-1]

    mix = fit3f(data, bins=bins, stripe_thin=stripe_thin, callback=_capture,
               **fit3f_kwargs)
    if shape_polish_iters == 0 or lambda_psd == 0.0:
        return mix

    direction = direction_box["direction"]
    ld0, lo0 = _cov_to_chol(_probe_cov(direction, stripe_thin))
    is_stripe = identify_stripes(mix, ld0, lo0)
    stripe_idx = np.flatnonzero(is_stripe)
    blob_idx = np.flatnonzero(~is_stripe)
    K = len(mix.w)

    centers, targets = histogram_targets3(data, bins=bins)
    cvar = cell_var(centers)

    # blob components never change shape under knob updates -- unit-weight
    # rho built once, reused every iteration (mirrors fit3f_psd's unit_comps).
    blob_unit = {
        k: rho_component(mix, k, n_max_psd) / mix.w[k] for k in blob_idx
    }

    def shaped_mix(w, knobs):
        return apply_shape_knobs(
            SplatMixture3F(w, mix.mu, mix.ld, mix.lo), is_stripe, direction,
            thin=stripe_thin, thin_mult=knobs[0], base_mult=knobs[1],
            center_scale=knobs[2])

    def stripe_unit_comps(w, knobs):
        shaped = shaped_mix(w, knobs)
        return {
            k: rho_component(shaped, k, n_max_psd) / w[k] for k in stripe_idx
        }

    def blob_rho(w):
        dim = n_max_psd ** 3
        total = np.zeros((dim, dim), dtype=complex)
        for k in blob_idx:
            total = total + w[k] * blob_unit[k]
        return total

    w = mix.w.copy()
    shape_raw = np.zeros(3)
    knobs = np.exp(shape_raw)
    m1w, m2w = np.zeros_like(w), np.zeros_like(w)
    m1k, m2k = np.zeros_like(knobs), np.zeros_like(knobs)

    for t in range(1, shape_polish_iters + 1):
        # The weight gradient must be evaluated at the same shaped mixture
        # used by the PSD and knob gradients below.
        cur = shaped_mix(w, knobs)
        _, g_full = loss_and_grad3f(cur, centers, targets,
                                    lambda_neg=lambda_neg,
                                    lambda_sum=lambda_sum, cvar=cvar)
        g_loss_w = g_full[:K]

        s_unit = stripe_unit_comps(w, knobs)
        b_rho = blob_rho(w)
        s_rho = sum((w[k] * s_unit[k] for k in stripe_idx), np.zeros_like(b_rho))
        total = b_rho + s_rho

        g_psd_w = np.empty(K)
        for k in range(K):
            unit_k = blob_unit[k] if k in blob_unit else s_unit[k]
            pen_p = psd_penalty(total + fd_eps * unit_k)
            pen_m = psd_penalty(total - fd_eps * unit_k)
            g_psd_w[k] = (pen_p - pen_m) / (2 * fd_eps)

        g_psd_k = np.empty(3)
        g_loss_k = np.empty(3)
        for i in range(3):
            kp, km = knobs.copy(), knobs.copy()
            # Work in log-space: this keeps all scales positive and makes the
            # FD gradient a derivative with respect to shape_raw.
            kp[i] *= np.exp(fd_eps)
            km[i] *= np.exp(-fd_eps)
            s_p = stripe_unit_comps(w, kp)
            s_m = stripe_unit_comps(w, km)
            rho_p = b_rho + sum((w[k] * s_p[k] for k in stripe_idx), np.zeros_like(b_rho))
            rho_m = b_rho + sum((w[k] * s_m[k] for k in stripe_idx), np.zeros_like(b_rho))
            g_psd_k[i] = (psd_penalty(rho_p) - psd_penalty(rho_m)) / (2 * fd_eps)
            # data-loss FD on the knob. Without it the knobs chase POSITIVITY
            # alone and fidelity trivially collapses -- that would not test "can
            # shape freedom keep the histogram fit AND fix positivity", only
            # "can shape kill negativity". Mirror the weights, which get both.
            mix_p = shaped_mix(w, kp)
            mix_m = shaped_mix(w, km)
            lp = loss3f(mix_p, centers, targets, lambda_neg=lambda_neg,
                        lambda_sum=lambda_sum, cvar=cvar)
            lm = loss3f(mix_m, centers, targets, lambda_neg=lambda_neg,
                        lambda_sum=lambda_sum, cvar=cvar)
            g_loss_k[i] = (lp - lm) / (2 * fd_eps)

        gw = g_loss_w + lambda_psd * g_psd_w
        gk = g_loss_k + lambda_psd * g_psd_k

        m1w = 0.9 * m1w + 0.1 * gw
        m2w = 0.999 * m2w + 0.001 * gw ** 2
        w = w - weight_polish_lr * (m1w / (1 - 0.9 ** t)) / (
            np.sqrt(m2w / (1 - 0.999 ** t)) + 1e-8
        )

        m1k = 0.9 * m1k + 0.1 * gk
        m2k = 0.999 * m2k + 0.001 * gk ** 2
        shape_raw = shape_raw - shape_polish_lr * (m1k / (1 - 0.9 ** t)) / (
            np.sqrt(m2k / (1 - 0.999 ** t)) + 1e-8
        )
        knobs = np.exp(shape_raw)

    return shaped_mix(w, knobs)
