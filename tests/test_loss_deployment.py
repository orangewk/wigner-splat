"""Checks for the issue #42 loss-model deployment across the remaining
reconstructors (bbdagM / purefock3 / splat) and the detector-noise sampler.

Per reconstructor, in order of independence:
  * eta = 1, extra = 0 reduces exactly to the existing pure path;
  * the closed-form lossy pdf matches an independent route (numerical
    convolution of the pure pdf, or the Fock-basis Kraus loss channel);
  * the analytic gradients match central differences with the loss on.
"""
import numpy as np
import pytest

from wigner_splat import bbdagM
from wigner_splat import purefock3
from wigner_splat.data3 import apply_detection_noise
from wigner_splat.fit3f import blob_span, cell_var, loss3f, loss_and_grad3f
from wigner_splat.fit3f import _pack3f, _unpack3f  # noqa: F401
from wigner_splat.fock import (
    hermite_psi, marginal_from_rho, quadrature_vectors,
)
from wigner_splat.forward3f import SplatMixture3F


# --------------------------------------------------------------- bbdagM ----


def _random_coherent(K, M, seed=20260716):
    rng = np.random.default_rng(seed)
    state = bbdagM.CoherentKetState(
        z=rng.normal(size=K) + 1j * rng.normal(size=K),
        alpha=rng.normal(size=(K, M)) + 1j * rng.normal(size=(K, M)),
    )
    data = [
        (rng.uniform(0.0, np.pi, M), rng.normal(scale=1.5, size=(25, M)))
        for _ in range(2)
    ]
    return state, data


def _random_coherent_mixed(R, K, M, seed=20260716):
    rng = np.random.default_rng(seed)
    state = bbdagM.MixedCoherentKetState(
        z=rng.normal(size=(R, K)) + 1j * rng.normal(size=(R, K)),
        alpha=rng.normal(size=(R, K, M)) + 1j * rng.normal(size=(R, K, M)),
    )
    data = [
        (rng.uniform(0.0, np.pi, M), rng.normal(scale=1.5, size=(25, M)))
        for _ in range(2)
    ]
    return state, data


def test_bbdagM_eta_one_delegates_to_pure():
    state, data = _random_coherent(K=2, M=2)
    assert bbdagM.nll_lossy(state, data, eta=1.0) == pytest.approx(
        bbdagM.nll(state, data), rel=1e-12
    )
    v0, g0 = bbdagM.nll_and_grad(state, data)
    v1, g1 = bbdagM.nll_and_grad_lossy(state, data, eta=1.0)
    assert v1 == pytest.approx(v0, rel=1e-12)
    assert np.allclose(g1, g0, rtol=1e-12)

    mixed, mdata = _random_coherent_mixed(R=2, K=2, M=2)
    assert bbdagM.nll_lossy_mixed(mixed, mdata, eta=1.0) == pytest.approx(
        bbdagM.nll_mixed(mixed, mdata), rel=1e-12
    )
    v0, g0 = bbdagM.nll_and_grad_mixed(mixed, mdata)
    v1, g1 = bbdagM.nll_and_grad_lossy_mixed(mixed, mdata, eta=1.0)
    assert v1 == pytest.approx(v0, rel=1e-12)
    assert np.allclose(g1, g0, rtol=1e-12)


@pytest.mark.parametrize("eta,extra", [(0.7, 0.0), (1.0, 0.05)])
def test_bbdagM_lossy_pdf_matches_numerical_convolution(eta, extra):
    state, _ = _random_coherent(K=2, M=1)
    theta = np.array([0.7])
    ys = np.linspace(-16, 16, 12001)
    p_pure = np.abs(state.psi_at(ys[:, None], theta)) ** 2 / state.norm_sq()
    sigma2 = (1.0 - eta) / 2.0 + extra
    xs = np.linspace(-4, 4, 41)
    kern = np.exp(-(xs[:, None] - np.sqrt(eta) * ys[None, :]) ** 2 / (2 * sigma2))
    kern /= np.sqrt(2 * np.pi * sigma2)
    p_num = np.trapezoid(kern * p_pure[None, :], ys, axis=1)
    p_cf = bbdagM.lossy_pdf(state, xs[:, None], theta, eta, extra)
    assert np.allclose(p_cf, p_num, rtol=1e-7, atol=1e-12)


def _loss_kraus_coeffs(n_max, eta):
    """c[n, k] = sqrt(C(n, k) eta^{n-k} (1-eta)^k), the damping amplitudes."""
    from math import comb
    c = np.zeros((n_max, n_max))
    for n in range(n_max):
        for k in range(n + 1):
            c[n, k] = np.sqrt(comb(n, k) * eta ** (n - k) * (1 - eta) ** k)
    return c


def _apply_loss_channel_1mode(rho, eta):
    """E_eta(rho) by truncated Kraus -- exact when rho is supported below
    n_max (A_k only moves population DOWN)."""
    n_max = len(rho)
    c = _loss_kraus_coeffs(n_max, eta)
    out = np.zeros_like(rho)
    for k in range(n_max):
        A = np.zeros((n_max, n_max))
        idx = np.arange(k, n_max)
        A[idx - k, idx] = c[idx, k]
        out += A @ rho @ A.conj().T
    return out


def test_bbdagM_mixed_lossy_pdf_matches_fock_loss_channel():
    """Rank-2 coherent mixture, M=1: Gaussian route vs Kraus algebra."""
    rng = np.random.default_rng(7)
    state = bbdagM.MixedCoherentKetState(
        z=rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)),
        alpha=0.9 * (rng.normal(size=(2, 2, 1)) + 1j * rng.normal(size=(2, 2, 1))),
    )
    n_max, eta = 40, 0.75
    from wigner_splat.fock import _coherent_coeffs

    def coherent_vec(a):
        v = _coherent_coeffs(abs(a), n_max).astype(complex)
        if a != 0:
            v *= (a / abs(a)) ** np.arange(n_max)
        return v

    rho = np.zeros((n_max, n_max), complex)
    for r in range(2):
        col = sum(state.z[r, c] * coherent_vec(state.alpha[r, c, 0])
                  for c in range(2))
        rho += np.outer(col, col.conj())
    rho /= state.norm_sq()
    rho_lossy = _apply_loss_channel_1mode(rho, eta)
    xs = np.linspace(-4, 4, 41)
    # NOTE the -th: the ket rotation alpha -> alpha e^{-i theta} and the
    # quadrature_vectors phase e^{-i n theta} sit on opposite sides of the
    # bracket, so the Fock-route marginal at -theta is the one that matches
    # (invisible for real states like the cats pinned elsewhere).
    for th in (0.0, 1.1):
        p_cf = bbdagM.lossy_pdf_mixed(state, xs[:, None], np.array([th]), eta)
        p_fock = marginal_from_rho(rho_lossy, xs, -th)
        assert np.allclose(p_cf, p_fock, rtol=1e-7, atol=1e-10)


@pytest.mark.parametrize("mixed", [False, True])
def test_bbdagM_lossy_grad_matches_central_difference(mixed):
    eta, extra = 0.75, 0.02
    if mixed:
        state, data = _random_coherent_mixed(R=2, K=2, M=2)
        value, g = bbdagM.nll_and_grad_lossy_mixed(state, data, eta, extra)
        v0 = bbdagM._pack_mixed(state)
        unpack = lambda v: bbdagM._unpack_mixed(v, 2, 2, 2)  # noqa: E731
        nll_fn = lambda st: bbdagM.nll_lossy_mixed(st, data, eta, extra)  # noqa: E731
    else:
        state, data = _random_coherent(K=2, M=2)
        value, g = bbdagM.nll_and_grad_lossy(state, data, eta, extra)
        v0 = bbdagM._pack(state)
        unpack = lambda v: bbdagM._unpack(v, 2, 2)  # noqa: E731
        nll_fn = lambda st: bbdagM.nll_lossy(st, data, eta, extra)  # noqa: E731
    assert value == pytest.approx(nll_fn(state), rel=1e-12)
    g_fd = np.zeros_like(v0)
    eps = 1e-5
    for i in range(len(v0)):
        vp = v0.copy(); vp[i] += eps
        vm = v0.copy(); vm[i] -= eps
        g_fd[i] = (nll_fn(unpack(vp)) - nll_fn(unpack(vm))) / (2 * eps)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g - g_fd) / scale) < 2e-7


def test_bbdagM_fit_lossy_smoke_known_eta():
    """fit_eta=False keeps eta pinned (the known-eta deployment)."""
    _, data = _random_coherent(K=2, M=1)
    st, eta = bbdagM.fit_bbdagM_lossy(data, K=2, M=1, eta0=0.8,
                                      fit_eta=False, iters=3)
    assert eta == pytest.approx(0.8, abs=1e-12)
    st, eta = bbdagM.fit_bbdagM_lossy_mixed(data, R=2, K=2, M=1, eta0=0.8,
                                            fit_eta=False, iters=3)
    assert eta == pytest.approx(0.8, abs=1e-12)


# ------------------------------------------------------------ purefock3 ----


def _random_psi(n_max, seed=3):
    rng = np.random.default_rng(seed)
    psi = rng.normal(size=(n_max,) * 3) + 1j * rng.normal(size=(n_max,) * 3)
    return psi / np.linalg.norm(psi)


def _random_data3(groups=2, samples=20, seed=5):
    rng = np.random.default_rng(seed)
    return [
        (rng.uniform(0.0, np.pi, 3), rng.normal(scale=1.3, size=(samples, 3)))
        for _ in range(groups)
    ]


def test_purefock3_eta_one_delegates_to_pure():
    psi = _random_psi(4)
    data = _random_data3()
    assert purefock3.lossy_nll_psi(psi, data, eta=1.0) == pytest.approx(
        purefock3.nll_psi(psi, data), rel=1e-12
    )
    v0, g0 = purefock3.nll_and_grad_psi(psi, data)
    v1, g1 = purefock3.lossy_nll_and_grad_psi(psi, data, eta=1.0)
    assert v1 == pytest.approx(v0, rel=1e-12)
    assert np.allclose(g1, g0, rtol=1e-12)


@pytest.mark.parametrize("eta,extra", [(0.7, 0.0), (0.9, 0.03), (1.0, 0.05)])
def test_purefock3_mode_matrices_match_numerical_convolution(eta, extra):
    """The Gauss-Hermite POVM matrix vs brute-force 1D integration."""
    n_max, theta = 5, 0.6
    sigma2 = (1.0 - eta) / 2.0 + extra
    xs = np.array([-2.3, 0.0, 0.4, 1.7])
    E = purefock3._lossy_mode_matrices(xs, theta, n_max, eta, sigma2)
    ys = np.linspace(-12, 12, 8001)
    psis = hermite_psi(ys, n_max)                          # (n, Y)
    ph = np.exp(-1j * theta * np.arange(n_max))
    for s, x in enumerate(xs):
        kern = np.exp(-(x - np.sqrt(eta) * ys) ** 2 / (2 * sigma2))
        kern /= np.sqrt(2 * np.pi * sigma2)
        Phi = np.trapezoid(
            psis[:, None, :] * psis[None, :, :] * kern[None, None, :], ys,
            axis=2,
        )
        E_num = np.conj(ph)[:, None] * Phi * ph[None, :]
        assert np.allclose(E[s], E_num, rtol=1e-8, atol=1e-12)


def test_purefock3_mode_matrices_match_kraus():
    """Independent route: the truncated Kraus sum (exact below n_max)."""
    n_max, eta, theta = 6, 0.7, 1.1
    sigma2 = (1.0 - eta) / 2.0
    xs = np.array([-1.5, 0.2, 2.0])
    E = purefock3._lossy_mode_matrices(xs, theta, n_max, eta, sigma2)
    c = _loss_kraus_coeffs(n_max, eta)
    v = quadrature_vectors(xs, theta, n_max)               # (S, n)
    E_kraus = np.zeros((len(xs), n_max, n_max), complex)
    for k in range(n_max):
        u = np.zeros((len(xs), n_max), complex)
        idx = np.arange(k, n_max)
        u[:, idx] = c[idx, k] * v[:, idx - k]
        E_kraus += np.conj(u)[:, :, None] * u[:, None, :]
    assert np.allclose(E, E_kraus, rtol=1e-9, atol=1e-12)


def test_purefock3_lossy_pdf_matches_kraus_channel_3mode():
    """Full 3-mode pdf vs applying the truncated Kraus channel to rho."""
    n_max, eta = 4, 0.75
    psi = _random_psi(n_max)
    # purefock3's amplitude is sum_n psi_n v_n (v unconjugated), so the
    # density matrix consistent with its pdf is rho_{mn} = conj(psi_m) psi_n.
    rho = np.outer(psi.ravel().conj(), psi.ravel())
    c = _loss_kraus_coeffs(n_max, eta)
    A1 = []
    for k in range(n_max):
        A = np.zeros((n_max, n_max))
        idx = np.arange(k, n_max)
        A[idx - k, idx] = c[idx, k]
        A1.append(A)
    I = np.eye(n_max)
    rho_l = np.zeros_like(rho)
    for mode in range(3):
        rho_l[...] = 0.0
        for A in A1:
            ops = [I, I, I]
            ops[mode] = A
            big = np.kron(np.kron(ops[0], ops[1]), ops[2])
            rho_l += big @ rho @ big.conj().T
        rho = rho_l.copy()
    theta = np.array([0.3, 1.2, 2.1])
    rng = np.random.default_rng(0)
    X = rng.normal(scale=1.2, size=(15, 3))
    v1, v2, v3 = purefock3._mode_vectors(X, theta, n_max)
    V = np.einsum("sm,sn,sq->smnq", v1, v2, v3).reshape(15, -1)
    p_kraus = np.real(np.einsum("sa,ab,sb->s", np.conj(V), rho, V))
    p_cf = purefock3.lossy_pdf_psi(psi, X, theta, eta)
    assert np.allclose(p_cf, p_kraus, rtol=1e-8, atol=1e-12)


def test_purefock3_lossy_grad_matches_central_difference():
    n_max, eta, extra = 3, 0.8, 0.02
    psi = _random_psi(n_max)
    data = _random_data3(groups=2, samples=12)
    value, g = purefock3.lossy_nll_and_grad_psi(psi, data, eta, extra,
                                                chunk=5)
    assert value == pytest.approx(
        purefock3.lossy_nll_psi(psi, data, eta, extra), rel=1e-12
    )
    v0 = purefock3._pack(psi)
    g_fd = np.zeros_like(v0)
    eps = 1e-6
    for i in range(len(v0)):
        vp = v0.copy(); vp[i] += eps
        vm = v0.copy(); vm[i] -= eps
        g_fd[i] = (
            purefock3.lossy_nll_psi(purefock3._unpack(vp, n_max), data, eta,
                                    extra)
            - purefock3.lossy_nll_psi(purefock3._unpack(vm, n_max), data, eta,
                                      extra)
        ) / (2 * eps)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g - g_fd) / scale) < 5e-6


# ----------------------------------------------------------------- splat ----


def _random_mixture(K=3, seed=11):
    rng = np.random.default_rng(seed)
    return SplatMixture3F(
        w=rng.normal(size=K),
        mu=rng.uniform(-1.5, 1.5, size=(K, 6)),
        ld=rng.uniform(-0.6, 0.1, size=(K, 6)),
        lo=0.2 * rng.normal(size=(K, 15)),
    )


def test_radon3_eta_one_is_identity():
    mix = _random_mixture()
    xs = np.linspace(-3, 3, 9)
    ref = mix.radon3(xs, xs, xs, 0.3, 1.1, 2.0, cell_var=0.01)
    out = mix.radon3(xs, xs, xs, 0.3, 1.1, 2.0, cell_var=0.01, eta=1.0,
                     extra_noise_var=0.0)
    assert np.array_equal(ref, out)


def test_radon3_lossy_equals_phase_space_loss_map():
    """The measurement-side map equals mu -> sqrt(eta) mu,
    Sigma -> eta Sigma + sigma2 I_6 applied to the mixture itself
    (U^T U = I), including the cross-covariance blocks."""
    mix = _random_mixture()
    eta, extra = 0.7, 0.04
    sigma2 = (1.0 - eta) / 2.0 + extra
    Sigma_l = eta * mix.Sigma() + sigma2 * np.eye(6)
    L = np.linalg.cholesky(Sigma_l)
    mapped = SplatMixture3F(
        w=mix.w,
        mu=np.sqrt(eta) * mix.mu,
        ld=np.log(np.diagonal(L, axis1=1, axis2=2)),
        lo=L[:, np.tril_indices(6, -1)[0], np.tril_indices(6, -1)[1]],
    )
    xs = np.linspace(-3, 3, 9)
    for th in ((0.0, 0.0, 0.0), (0.4, 1.3, 2.2)):
        out = mix.radon3(xs, xs, xs, *th, cell_var=0.01, eta=eta,
                         extra_noise_var=extra)
        ref = mapped.radon3(xs, xs, xs, *th, cell_var=0.01)
        assert np.allclose(out, ref, rtol=1e-10, atol=1e-14)


def test_radon3_lossy_matches_numerical_convolution():
    """Lossy radon3 vs brute-force 3D convolution of the pure density."""
    mix = _random_mixture(K=2, seed=3)
    eta, extra = 0.8, 0.02
    sigma2 = (1.0 - eta) / 2.0 + extra
    th = (0.5, 1.0, 1.9)
    ys = np.linspace(-8, 8, 161)
    h = ys[1] - ys[0]
    pure = mix.radon3(ys, ys, ys, *th, chunk=16)
    for x in ((-1.2, 0.3, 0.8), (0.0, 0.0, 0.0), (1.5, -0.7, 0.4)):
        k1, k2, k3 = (
            np.exp(-(x[m] - np.sqrt(eta) * ys) ** 2 / (2 * sigma2))
            / np.sqrt(2 * np.pi * sigma2)
            for m in range(3)
        )
        p_num = np.einsum("ijl,i,j,l->", pure, k1, k2, k3) * h ** 3
        p_cf = mix.radon3([x[0]], [x[1]], [x[2]], *th, eta=eta,
                          extra_noise_var=extra)[0, 0, 0]
        assert p_cf == pytest.approx(p_num, rel=1e-6, abs=1e-12)


def test_loss3f_grad_matches_central_difference_with_loss():
    rng = np.random.default_rng(2)
    mix = _random_mixture(K=2, seed=9)
    centers = np.linspace(-2.5, 2.5, 7)
    hist = rng.uniform(0.0, 0.02, size=(2, 7, 7, 7))
    targets = [((0.2, 0.9, 1.7), hist[0]), ((1.1, 0.0, 2.4), hist[1])]
    eta, extra = 0.75, 0.03
    val, g = loss_and_grad3f(mix, centers, targets, cvar=cell_var(centers),
                             eta=eta, extra_noise_var=extra)
    assert val == pytest.approx(
        loss3f(mix, centers, targets, cvar=cell_var(centers), eta=eta,
               extra_noise_var=extra), rel=1e-12
    )
    v0 = _pack3f(mix)
    K = len(mix.w)
    g_fd = np.zeros_like(v0)
    eps = 1e-6
    for i in range(len(v0)):
        vp = v0.copy(); vp[i] += eps
        vm = v0.copy(); vm[i] -= eps
        g_fd[i] = (
            loss3f(_unpack3f(vp, K), centers, targets,
                   cvar=cell_var(centers), eta=eta, extra_noise_var=extra)
            - loss3f(_unpack3f(vm, K), centers, targets,
                     cvar=cell_var(centers), eta=eta, extra_noise_var=extra)
        ) / (2 * eps)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g - g_fd) / scale) < 1e-5


def test_loss_params_validated_everywhere():
    mix = _random_mixture(K=1)
    xs = np.linspace(-1, 1, 3)
    psi = _random_psi(3)
    state, data = _random_coherent(K=1, M=1)
    for bad in (1.2, -0.1):
        with pytest.raises(ValueError):
            mix.radon3(xs, xs, xs, 0.0, 0.0, 0.0, eta=bad)
        with pytest.raises(ValueError):
            purefock3.lossy_pdf_psi(psi, np.zeros((2, 3)), np.zeros(3),
                                    eta=bad)
        with pytest.raises(ValueError):
            bbdagM.lossy_pdf(state, np.zeros((2, 1)), np.zeros(1), eta=bad)
        with pytest.raises(ValueError):
            apply_detection_noise(data, eta=bad)


def _tiny_cat_data(shots=150, seed=7):
    from wigner_splat.states3 import ThreeModeCat
    grid = [(0.0, 0.0, 0.0), (np.pi / 2, np.pi / 2, np.pi / 2),
            (0.3, 1.1, 2.0), (2.0, 0.3, 1.1)]
    return ThreeModeCat(1.5, +1).sample_homodyne(grid, shots, rng=seed)


def test_psd_wrappers_thread_noise_into_polish(monkeypatch):
    """Regression (PR-58 review P1): fit3f_psd / fit3f_shape_psd must pass
    eta / extra_noise_var into every polish-stage histogram-loss call, not
    only into the wrapped fit3f."""
    import wigner_splat.fit3f as f3
    eta, extra = 0.9, 0.01
    data = _tiny_cat_data()
    seen = {"grad": [], "loss": []}
    real_grad, real_loss = f3.loss_and_grad3f, f3.loss3f

    def spy_grad(*a, **kw):
        seen["grad"].append((kw.get("eta", 1.0),
                             kw.get("extra_noise_var", 0.0)))
        return real_grad(*a, **kw)

    def spy_loss(*a, **kw):
        seen["loss"].append((kw.get("eta", 1.0),
                             kw.get("extra_noise_var", 0.0)))
        return real_loss(*a, **kw)

    monkeypatch.setattr(f3, "loss_and_grad3f", spy_grad)
    monkeypatch.setattr(f3, "loss3f", spy_loss)

    seen["grad"].clear()
    f3.fit3f_psd(data, bins=8, n_max_psd=3, psd_polish_iters=1,
                 eta=eta, extra_noise_var=extra)
    assert seen["grad"], "psd polish never evaluated the histogram loss"
    assert all(v == (eta, extra) for v in seen["grad"])

    seen["grad"].clear()
    seen["loss"].clear()
    f3.fit3f_shape_psd(data, bins=8, n_max_psd=3, shape_polish_iters=1,
                       eta=eta, extra_noise_var=extra)
    assert seen["grad"] and seen["loss"]
    assert all(v == (eta, extra) for v in seen["grad"])
    assert all(v == (eta, extra) for v in seen["loss"])


def test_fit3f_rejects_eta_zero():
    """Regression (PR-58 review P2): the pre-loss state is unidentifiable
    at eta = 0 -- explicit ValueError instead of a divide-by-zero inf."""
    from wigner_splat.fit3f import fit3f
    data = _tiny_cat_data(shots=20)
    with pytest.raises(ValueError):
        fit3f(data, bins=8, eta=0.0)
    with pytest.raises(ValueError):
        blob_span(data, eta=0.0)


# --------------------------------------------------------------- sampler ----


def test_apply_detection_noise_identity_at_eta_one():
    data = _random_data3()
    out = apply_detection_noise(data, eta=1.0, extra_noise_var=0.0, rng=0)
    for (t0, x0), (t1, x1) in zip(data, out):
        assert np.array_equal(np.asarray(t0), np.asarray(t1))
        assert np.array_equal(np.asarray(x0, float), x1)


def test_apply_detection_noise_moments():
    """sqrt(eta) scaling of the mean and +sigma2 on the variance."""
    rng = np.random.default_rng(1)
    X = rng.normal(loc=2.0, scale=1.0, size=(200000, 3))
    eta, extra = 0.8, 0.1
    out = apply_detection_noise([(np.zeros(3), X)], eta, extra, rng=2)
    _, Y = out[0]
    sigma2 = (1.0 - eta) / 2.0 + extra
    assert np.allclose(Y.mean(axis=0), np.sqrt(eta) * 2.0, atol=0.01)
    assert np.allclose(Y.var(axis=0), eta * 1.0 + sigma2, atol=0.02)


def test_blob_span_inverts_the_loss_map():
    """Measured-variance samples map back to the pre-loss span."""
    rng = np.random.default_rng(4)
    span, eta, extra = 1.8, 0.7, 0.05
    sigma2 = (1.0 - eta) / 2.0 + extra
    signs = rng.choice([-1.0, 1.0], size=(120000, 3))
    X = signs * span + rng.normal(scale=np.sqrt(0.5), size=(120000, 3))
    Y = np.sqrt(eta) * X + rng.normal(scale=np.sqrt(sigma2),
                                      size=X.shape)
    est = blob_span([(np.zeros(3), Y)], eta=eta, extra_noise_var=extra)
    assert est == pytest.approx(span, abs=0.03)
