"""Full-covariance two-mode reconstructor: fit a signed full-cov splat mixture
to binned joint homodyne data. The faithful 3DGS densification loop lifted to
4D phase space, with the Cholesky covariance of forward2f.

Loss (identical to fit2, for a fair head-to-head with the separable fitter and
the MLE baseline):

    Loss = sum_{th1,th2} mean( (model - hist)^2 )            (2D histogram L2)
         + lambda_neg * sum mean( min(model, 0)^2 )          (marginals >= 0)
         + lambda_sum * (sum_k w_k - 1)^2                     (total probability)

The forward model (forward2f.radon2) is a correlated 2D Gaussian per splat, so
the loss gradient is closed-form. For a 2D Gaussian N(x; m, C):

    dN/dm = N P d,           dN/dC = (N/2)(P d d^T P - P),   P = C^{-1}, d = x-m.

Chain to the splat: dL/dmu_k = sum_pairs U dL/dm,
dL/dSigma_k = sum_pairs U (dL/dC) U^T, and Sigma = L L^T gives
dL/dL = 2 sym(dL/dSigma) L (lower triangle only; the diagonal is scaled by
exp(ld) because L[i,i] = exp(ld_i)). Vectorized over angle pairs; the
per-splat, per-cell 2D-Gaussian moment sums are contracted with einsum.

Densification is the REAL 3DGS split now that it is meaningful: split a splat
along the principal eigenvector of its 4D covariance (fit2 could only split
within one mode's 2D plane). Signed birth uses a weight-gradient field with a
DICTIONARY of anisotropic probes -- the closed-form dL/dw of a hypothetical
new splat with each candidate covariance at each 4D location -- so a probe
elongated along the residual's correlation ridge resonates with the entangled
fringe that an isotropic probe smears over (root cause (c) in the separable
falsification). A born splat inherits the resonant probe's covariance, so full
covariance then lets Adam stretch it along the ridge. Adam-moment inheritance
(children inherit the parent's moments) follows the fit.py policy.
"""

import numpy as np

from .data2 import histogram_targets2
from .forward2f import SplatMixture2F, _U, build_L, _TRIL_I, _TRIL_J, _DIAG


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

    The (P, B, B, K) tensor of per-cell 2D-Gaussian values N is built once; all
    parameter gradients are contractions of it. See the module docstring for the
    closed forms. Central-difference tested to rtol 1e-5.
    """
    K = len(mixture.w)
    B = len(centers)
    w = mixture.w

    th = np.array([a for a, _ in targets])                # (P, 2)
    hist = np.array([h for _, h in targets])              # (P, B, B)
    th1, th2 = th[:, 0], th[:, 1]
    P = len(th)

    # projection U (P, 4, 2)
    U = np.zeros((P, 4, 2))
    U[:, 0, 0], U[:, 1, 0] = np.cos(th1), np.sin(th1)
    U[:, 2, 1], U[:, 3, 1] = np.cos(th2), np.sin(th2)

    L = mixture.L()                                       # (K, 4, 4)
    Sigma = L @ L.transpose(0, 2, 1)                      # (K, 4, 4)

    m = np.einsum("par,ka->pkr", U, mixture.mu)           # (P, K, 2)
    C = np.einsum("par,kab,pbs->pkrs", U, Sigma, U)       # (P, K, 2, 2)
    Prec = np.linalg.inv(C)                               # (P, K, 2, 2)
    detC = np.linalg.det(C)                               # (P, K)
    P00, P01, P11 = Prec[..., 0, 0], Prec[..., 0, 1], Prec[..., 1, 1]

    d1 = centers[None, :, None] - m[:, None, :, 0]        # (P, B, K)
    d2 = centers[None, :, None] - m[:, None, :, 1]        # (P, B, K)
    quad = (
        P00[:, None, None, :] * d1[:, :, None, :] ** 2
        + 2 * P01[:, None, None, :] * d1[:, :, None, :] * d2[:, None, :, :]
        + P11[:, None, None, :] * d2[:, None, :, :] ** 2
    )                                                     # (P, B, B, K)
    Nker = np.exp(-quad / 2) / (2 * np.pi * np.sqrt(detC)[:, None, None, :])

    model = np.einsum("pijk,k->pij", Nker, w)             # (P, B, B)
    resid = model - hist
    neg = np.minimum(model, 0.0)
    total = np.sum(np.mean(resid ** 2, axis=(1, 2))) + lambda_neg * np.sum(
        np.mean(neg ** 2, axis=(1, 2))
    )
    r = (2.0 / (B * B)) * (resid + lambda_neg * neg)      # (P, B, B) = dL/dmodel

    rN = r[..., None] * Nker                              # (P, B, B, K)
    rNi = rN.sum(axis=2)                                  # (P, B, K) summed over j
    rNj = rN.sum(axis=1)                                  # (P, B, K) summed over i

    A = rNi.sum(axis=1)                                   # (P, K)
    Sd1 = np.einsum("pik,pik->pk", d1, rNi)
    Sd11 = np.einsum("pik,pik->pk", d1 ** 2, rNi)
    Sd2 = np.einsum("pjk,pjk->pk", d2, rNj)
    Sd22 = np.einsum("pjk,pjk->pk", d2 ** 2, rNj)
    Sd12 = np.einsum("pik,pjk,pijk->pk", d1, d2, rN)

    # weight gradient
    gw = A.sum(axis=0)                                    # (K,)

    # projected-mean gradient gm (P, K, 2) = w (P d) contracted with rN
    gm0 = w * (P00 * Sd1 + P01 * Sd2)
    gm1 = w * (P01 * Sd1 + P11 * Sd2)
    gm = np.stack([gm0, gm1], axis=-1)                    # (P, K, 2)

    # projected-cov gradient gC (P, K, 2, 2) = w/2 (M - P A)
    M00 = P00 ** 2 * Sd11 + 2 * P00 * P01 * Sd12 + P01 ** 2 * Sd22
    M01 = P00 * P01 * Sd11 + (P00 * P11 + P01 ** 2) * Sd12 + P01 * P11 * Sd22
    M11 = P01 ** 2 * Sd11 + 2 * P01 * P11 * Sd12 + P11 ** 2 * Sd22
    gC00 = 0.5 * w * (M00 - P00 * A)
    gC01 = 0.5 * w * (M01 - P01 * A)
    gC11 = 0.5 * w * (M11 - P11 * A)
    gC = np.empty((P, K, 2, 2))
    gC[..., 0, 0] = gC00
    gC[..., 0, 1] = gC01
    gC[..., 1, 0] = gC01
    gC[..., 1, 1] = gC11

    # chain projection -> splat params
    gmu = np.einsum("par,pkr->ka", U, gm)                 # (K, 4)
    gSigma = np.einsum("par,pkrs,pbs->kab", U, gC, U)     # (K, 4, 4)

    # chain Sigma = L L^T -> L (gSigma symmetric already): dL/dL = 2 gSigma L
    gL = 2 * np.einsum("kab,kbc->kac", gSigma, L)         # (K, 4, 4)
    gld = gL[:, _DIAG, _DIAG] * np.exp(mixture.ld)        # (K, 4)
    glo = gL[:, _TRIL_I, _TRIL_J]                          # (K, 6)

    wsum = w.sum() - 1.0
    total += lambda_sum * wsum ** 2
    gw = gw + 2 * lambda_sum * wsum
    return total, np.concatenate([gw, gmu.ravel(), gld.ravel(), glo.ravel()])


def _principal_axis(Sigma_k):
    """Unit eigenvector of the largest eigenvalue and its sqrt-eigenvalue."""
    vals, vecs = np.linalg.eigh(Sigma_k)
    i = int(np.argmax(vals))
    return vecs[:, i], np.sqrt(max(vals[i], 1e-12))


def adapt2f(mixture, m1, m2, gnorm, K_max, prune_weight=5e-3, split_rel=2.0,
            split_factor=1.6, split_offset=0.6):
    """One densification/pruning step (the real 3DGS split in 4D).

    Prunes |w| < prune_weight. Splits splats whose accumulated 4D positional
    gradient norm exceeds split_rel * median into two half-weight children,
    offset by split_offset * sqrt(lambda_max) along the PRINCIPAL EIGENVECTOR
    of the 4D covariance (fit2 could only split inside one mode's plane; a
    full-cov splat's dominant axis can lie along an entangled direction). The
    covariance is shrunk along that axis by split_factor via a rank-1 Cholesky
    downdate approximation (scale the eigen-component). Adam moments follow the
    same row selection and children inherit the parent's moments (fit.adapt
    policy). Returns (mixture, m1, m2).
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
            # shrink covariance along `axis`: Sigma' = Sigma - c axis axis^T
            c = (1.0 - 1.0 / split_factor ** 2) * sig ** 2
            Sig_new = Sigma[row] - c * np.outer(axis, axis)
            Sig_new = Sig_new + 1e-9 * np.eye(4)
            Ln = np.linalg.cholesky(Sig_new)
            new.ld[row] = np.log(np.diag(Ln))
            new.lo[row] = Ln[_TRIL_I, _TRIL_J]
        new.w[child] *= 0.5
    return new, m1n, m2n


def _probe_dictionary(scale=0.5, elong=3.0):
    """Covariances for the birth probes: one isotropic + several anisotropic
    ones elongated along the generic two-mode correlation directions (pairwise
    sums/differences of the two modes' quadratures). No knowledge of the true
    state: these are the natural anisotropy axes of ANY two-mode Gaussian
    correlation; the residual picks which one resonates. Returns list of (4,4)."""
    base = scale ** 2
    dirs = [
        np.array([0.0, 1.0, 0.0, -1.0]),   # p1 - p2
        np.array([0.0, 1.0, 0.0, 1.0]),    # p1 + p2
        np.array([1.0, 0.0, -1.0, 0.0]),   # x1 - x2
        np.array([1.0, 0.0, 1.0, 0.0]),    # x1 + x2
    ]
    probes = [base * np.eye(4)]
    for v in dirs:
        v = v / np.linalg.norm(v)
        probes.append(base * (np.eye(4) + (elong ** 2 - 1.0) * np.outer(v, v)))
    return probes


def birth_field2f(mixture, centers, targets, candidates, Sigma_probe,
                  lambda_neg=10.0, chunk=2048, _Ds=None):
    """dL/dw for a probe splat with covariance Sigma_probe at each 4D candidate.

    candidates: (G, 4) as (x1, p1, x2, p2). The probe's projected covariance
    C = U^T Sigma_probe U is the same for every candidate at a given angle, so
    only the projected mean depends on the location. The weight gradient is the
    current residual back-projected through the probe's (correlated) kernel --
    closed form. Where it is large and positive the model needs NEGATIVE mass
    (and vice versa), so the field both places and signs newborn splats. Pass a
    precomputed _Ds (list of (th1, th2, dL/dmodel)) to reuse the residual across
    probes. Returns (G,)."""
    if _Ds is None:
        B = len(centers)
        _Ds = []
        for (th1, th2), hist in targets:
            model = mixture.radon2(centers, centers, th1, th2)
            D = (2.0 / (B * B)) * ((model - hist) + lambda_neg * np.minimum(model, 0.0))
            _Ds.append((th1, th2, D))
    field = np.zeros(len(candidates))
    for lo in range(0, len(candidates), chunk):
        cand = candidates[lo : lo + chunk]                # (g, 4)
        acc = np.zeros(len(cand))
        for th1, th2, D in _Ds:
            U = _U(th1, th2)
            C = U.T @ Sigma_probe @ U                     # (2, 2)
            Prec = np.linalg.inv(C)
            det = np.linalg.det(C)
            mp = cand @ U                                 # (g, 2)
            d1 = centers[None, :] - mp[:, 0:1]            # (g, B)
            d2 = centers[None, :] - mp[:, 1:2]            # (g, B)
            # correlated 2D gaussian kernel gk[g, i, j]
            q = (
                Prec[0, 0] * d1[:, :, None] ** 2
                + 2 * Prec[0, 1] * d1[:, :, None] * d2[:, None, :]
                + Prec[1, 1] * d2[:, None, :] ** 2
            )
            gk = np.exp(-q / 2) / (2 * np.pi * np.sqrt(det))
            acc += np.einsum("gij,ij->g", gk, D)
        field[lo : lo + chunk] = acc
    return field


def _birth_batch(field, candidates, n_birth, spread):
    """Greedy top-|field| picks, suppressing radius `spread` around each pick."""
    fa = np.abs(field).copy()
    chosen = []
    for _ in range(n_birth):
        j = int(np.argmax(fa))
        if fa[j] <= 0.0:
            break
        chosen.append(j)
        fa[np.linalg.norm(candidates - candidates[j], axis=1) < spread] = 0.0
    return chosen


def _append_splat(v, K, w0, mu0, Sigma0):
    """Append one splat (weight w0, mean mu0, covariance Sigma0) to packed v."""
    m = _unpack2f(v, K)
    L0 = np.linalg.cholesky(Sigma0 + 1e-9 * np.eye(4))
    return _pack2f(SplatMixture2F(
        np.append(m.w, w0),
        np.vstack([m.mu, mu0]),
        np.vstack([m.ld, np.log(np.diag(L0))]),
        np.vstack([m.lo, L0[_TRIL_I, _TRIL_J]]),
    ))


def _append_zero(v, K):
    """Append one all-zero moment row (matches _append_splat's layout)."""
    m = _unpack2f(v, K)
    return _pack2f(SplatMixture2F(
        np.append(m.w, 0.0),
        np.vstack([m.mu, np.zeros((1, 4))]),
        np.vstack([m.ld, np.zeros((1, 4))]),
        np.vstack([m.lo, np.zeros((1, 6))]),
    ))


def fit2f(data, K=4, iters=700, lr=0.05, seed=0, bins=40, callback=None,
          birth_start=200, birth_every=50, birth_until=None, K_max=14,
          densify_every=100, prune_weight=5e-3, birth_weight=0.05,
          birth_grid=7, birth_scale=0.5, birth_elong=3.0, lambda_neg=10.0,
          lambda_sum=1.0, n_birth=4, birth_spread=1.2, init_blobs=True):
    """Adam on the analytic full-cov loss gradient, with staged densification.

    Stage 1 (t < birth_start): fit the positive envelope (the two coherent
    blobs) to a loss plateau -- from init_blobs the mixture starts as a small
    set of positive splats. Stage 2 (birth_start <= t <= birth_until, default
    0.85 iters): every birth_every steps, up to n_birth signed splats are born
    at the extrema of the anisotropic-probe weight-gradient field, each
    inheriting the resonant probe's covariance and the descent sign; every
    densify_every steps adapt2f prunes/splits. By Stage 2 the residual field IS
    the fringe (the blobs are fit), so births land on it. K grows to K_max.
    Returns the fitted mixture.
    """
    centers, targets = histogram_targets2(data, bins=bins)
    if birth_until is None:
        birth_until = int(0.85 * iters)

    if init_blobs:
        # generic positive-envelope init: place blobs on the measured
        # (x1, x2) correlation, isotropic; NOT the true blob centers.
        span = centers[-1] * 0.55
        mus = np.array([[span, 0.0, span, 0.0], [-span, 0.0, -span, 0.0],
                        [span, 0.0, -span, 0.0], [-span, 0.0, span, 0.0]])[:K]
        mix = SplatMixture2F(
            w=np.full(K, 1.0 / K), mu=mus,
            ld=np.full((K, 4), np.log(0.8)), lo=np.zeros((K, 6)),
        )
    else:
        mix = SplatMixture2F.random_init(K, rng=seed)

    v = _pack2f(mix)
    m1, m2 = np.zeros_like(v), np.zeros_like(v)

    xg = np.linspace(centers[0], centers[-1], birth_grid)
    G = np.meshgrid(xg, xg, xg, xg, indexing="ij")
    candidates = np.stack([g.ravel() for g in G], axis=1)
    probes = _probe_dictionary(scale=birth_scale, elong=birth_elong)

    gnorm = np.zeros(K)
    for t in range(1, iters + 1):
        cur, grad = loss_and_grad2f(
            _unpack2f(v, K), centers, targets,
            lambda_neg=lambda_neg, lambda_sum=lambda_sum,
        )
        gnorm += np.linalg.norm(grad[K : 5 * K].reshape(K, 4), axis=1)
        m1 = 0.9 * m1 + 0.1 * grad
        m2 = 0.999 * m2 + 0.001 * grad ** 2
        step = lr * (m1 / (1 - 0.9 ** t)) / (np.sqrt(m2 / (1 - 0.999 ** t)) + 1e-8)
        v -= step

        do_split = densify_every and t % densify_every == 0 and t <= birth_until
        do_birth = (t >= birth_start and birth_every and t % birth_every == 0
                    and t <= birth_until)
        if do_split:
            mix_t, m1, m2 = adapt2f(
                _unpack2f(v, K), m1, m2, gnorm / densify_every,
                K_max=K_max, prune_weight=prune_weight,
            )
            K = len(mix_t.w)
            v = _pack2f(mix_t)
            gnorm = np.zeros(K)
        if do_birth and K < K_max:
            mix_t = _unpack2f(v, K)
            # residual field shared across probes; per-probe field, best |resp|
            Ds = None
            best = None
            for Sp in probes:
                if Ds is None:
                    B = len(centers)
                    Ds = []
                    for (th1, th2), hist in targets:
                        model = mix_t.radon2(centers, centers, th1, th2)
                        D = (2.0 / (B * B)) * (
                            (model - hist) + lambda_neg * np.minimum(model, 0.0)
                        )
                        Ds.append((th1, th2, D))
                fld = birth_field2f(mix_t, centers, targets, candidates, Sp, _Ds=Ds)
                if best is None or np.abs(fld).max() > np.abs(best[0]).max():
                    best = (fld, Sp)
            field, Sprobe = best
            room = K_max - K
            idx = _birth_batch(field, candidates, min(n_birth, room), birth_spread)
            for i in idx:
                v = _append_splat(
                    v, K, -np.sign(field[i]) * birth_weight, candidates[i], Sprobe
                )
                m1 = _append_zero(m1, K)
                m2 = _append_zero(m2, K)
                K += 1
            gnorm = np.zeros(K)
        if callback and t % 50 == 0:
            callback(t, loss2f(_unpack2f(v, K), centers, targets), K)
    return _unpack2f(v, K)
