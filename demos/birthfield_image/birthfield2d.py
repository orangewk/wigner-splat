"""Signed 2D Gaussian splat image fitting with birth-field densification.

A self-contained demo module (issue #46 idea 4) exporting the repo's exp02
lesson to plain image fitting: splitting/cloning existing splats can never
flip a weight's sign, so the subtractive (negative) structure a target
needs must be BORN -- and the right place and sign are given in closed form
by the "birth field", the loss gradient with respect to the weight of a
hypothetical new splat at position mu:

    B(mu) = dL/dw|_{w=0, splat at mu} = (2/N) sum_p r(p) exp(-|p-mu|^2/(2 sigma_b^2))

i.e. the residual r = I - T smoothed by the probe kernel. Descent wants a
new splat where |B| peaks, with weight sign = -sign(B).

Everything is analytic (gradients pinned against central differences in
tests/test_birthfield2d.py); no dependency beyond numpy.

Splat parameterization (matches the repo's phase-space splats): position
mu, log-scales s1 s2, orientation phi, SIGNED weight w; kernel amplitude
G(p) = exp(-q/2), q = e^{-2 s1} u^2 + e^{-2 s2} v^2, (u, v) = R(phi)^T (p - mu).
"""
import numpy as np


def render_and_grad(mu, s, phi, w, X, Y, target):
    """MSE loss, rendered image, and analytic gradients for all K splats.

    mu (K,2), s (K,2) log-scales, phi (K,), w (K,) signed; X, Y flattened
    grid (N,); target (N,). Returns (loss, image, grads dict).
    """
    K = len(w)
    dx = X[None, :] - mu[:, 0][:, None]
    dy = Y[None, :] - mu[:, 1][:, None]
    c0, s0 = np.cos(phi)[:, None], np.sin(phi)[:, None]
    u = c0 * dx + s0 * dy
    v = -s0 * dx + c0 * dy
    e1 = np.exp(-2.0 * s[:, 0])[:, None]
    e2 = np.exp(-2.0 * s[:, 1])[:, None]
    G = np.exp(-0.5 * (e1 * u ** 2 + e2 * v ** 2))
    image = w @ G
    r = image - target
    N = len(X)
    loss = float(np.mean(r ** 2))

    r2 = (2.0 / N) * r
    g_w = G @ r2
    common = w[:, None] * G * (-0.5)
    base = common * r2[None, :]
    dq_mux = -2.0 * (e1 * u * c0 - e2 * v * s0)
    dq_muy = -2.0 * (e1 * u * s0 + e2 * v * c0)
    g_mu = np.stack([np.sum(base * dq_mux, axis=1),
                     np.sum(base * dq_muy, axis=1)], axis=1)
    g_s = np.stack([np.sum(base * (-2.0 * e1 * u ** 2), axis=1),
                    np.sum(base * (-2.0 * e2 * v ** 2), axis=1)], axis=1)
    g_phi = np.sum(base * (2.0 * u * v * (e1 - e2)), axis=1)
    return loss, image, {"mu": g_mu, "s": g_s, "phi": g_phi, "w": g_w}


def birth_field(residual_img, sigma_px):
    """dL/dw of a hypothetical unit splat at each pixel: (2/N) * (r * probe).

    Separable correlation of the residual image (H, W) with the UNNORMALIZED
    Gaussian kernel exp(-t^2 / (2 sigma^2)) -- numpy only, no scipy.
    """
    H, W = residual_img.shape
    half = int(np.ceil(6 * sigma_px))  # 6 sigma: truncation < 1e-8 relative
    t = np.arange(-half, half + 1, dtype=float)
    k = np.exp(-t ** 2 / (2.0 * sigma_px ** 2))
    pad_r = np.pad(residual_img, ((0, 0), (half, half)), mode="constant")
    rows = np.stack([np.convolve(row, k, mode="valid") for row in pad_r])
    pad_c = np.pad(rows, ((half, half), (0, 0)), mode="constant")
    out = np.stack([np.convolve(col, k, mode="valid") for col in pad_c.T]).T
    return (2.0 / residual_img.size) * out


def _adam_state(shapes):
    return {k: (np.zeros(sh), np.zeros(sh)) for k, sh in shapes.items()}


def fit(target_img, extent, mode, K0=4, K_max=40, iters=4000, grow_every=150,
        lr=0.03, sigma_b_px=3.0, seed=0, snapshot_every=50):
    """Fit target_img (H, W) over [-extent, extent]^2. mode: 'birth'|'split'.

    Returns a history dict: loss (per iter), snapshots (iter, params, image),
    events (iter, kind, position), final params.
    """
    H, W = target_img.shape
    xs = np.linspace(-extent, extent, W)
    ys = np.linspace(-extent, extent, H)
    Xg, Yg = np.meshgrid(xs, ys)
    X, Y = Xg.ravel(), Yg.ravel()
    T = target_img.ravel()
    px = 2.0 * extent / W

    rng = np.random.default_rng(seed)
    mu = rng.uniform(-extent / 2, extent / 2, (K0, 2))
    s = np.full((K0, 2), np.log(extent / 3.0))
    phi = rng.uniform(0, np.pi, K0)
    w = np.full(K0, 0.3)  # positive start: negativity must be born
    m = _adam_state({"mu": mu.shape, "s": s.shape,
                     "phi": phi.shape, "w": w.shape})
    acc_gmu = np.zeros(K0)

    history = {"loss": [], "snapshots": [], "events": [], "shape": (H, W)}
    t_adam = 0
    for it in range(1, iters + 1):
        loss, image, g = render_and_grad(mu, s, phi, w, X, Y, T)
        history["loss"].append(loss)
        acc_gmu += np.linalg.norm(g["mu"], axis=1)
        t_adam += 1
        params = {"mu": mu, "s": s, "phi": phi, "w": w}
        for key in params:
            m1, m2 = m[key]
            m1[:] = 0.9 * m1 + 0.1 * g[key]
            m2[:] = 0.999 * m2 + 0.001 * g[key] ** 2
            step = lr * (m1 / (1 - 0.9 ** t_adam)) / (
                np.sqrt(m2 / (1 - 0.999 ** t_adam)) + 1e-8)
            params[key] -= step

        if it % snapshot_every == 0 or it == 1:
            B = birth_field((image - T).reshape(H, W), sigma_b_px)
            history["snapshots"].append(
                (it, {k: v.copy() for k, v in params.items()},
                 image.reshape(H, W).copy(), B))

        if it % grow_every == 0 and len(w) < K_max:
            if mode == "birth":
                B = birth_field((image - T).reshape(H, W), sigma_b_px)
                idx = np.unravel_index(np.argmax(np.abs(B)), B.shape)
                pos = np.array([xs[idx[1]], ys[idx[0]]])
                sign = -np.sign(B[idx])
                mu = np.vstack([mu, pos])
                s = np.vstack([s, np.full(2, np.log(sigma_b_px * px))])
                phi = np.append(phi, 0.0)
                w = np.append(w, sign * 0.05)
                history["events"].append((it, "birth", pos, float(sign)))
            else:  # split: the exp02-style baseline (no new sign possible)
                k = int(np.argmax(acc_gmu))
                major = int(np.argmax(s[k]))
                d = (np.array([np.cos(phi[k]), np.sin(phi[k])]) if major == 0
                     else np.array([-np.sin(phi[k]), np.cos(phi[k])]))
                off = 0.6 * np.exp(s[k, major]) * d
                mu = np.vstack([mu, mu[k] + off])
                mu[k] = mu[k] - off
                s = np.vstack([s, s[k]])
                s[k, major] -= np.log(1.6)
                s[-1, major] -= np.log(1.6)
                phi = np.append(phi, phi[k])
                w[k] *= 0.5
                w = np.append(w, w[k])
                history["events"].append((it, "split", mu[k].copy(), 0.0))
            grown = {"mu": mu, "s": s, "phi": phi, "w": w}
            for key in m:  # extend Adam moments for the new row
                m1, m2 = m[key]
                pad = [(0, grown[key].shape[0] - m1.shape[0])] + \
                      [(0, 0)] * (m1.ndim - 1)
                m[key] = (np.pad(m1, pad), np.pad(m2, pad))
            acc_gmu = np.zeros(len(w))
            t_adam = 0  # re-bias-correct after the parameter-space change

    loss, image, _ = render_and_grad(mu, s, phi, w, X, Y, T)
    history["loss"].append(loss)
    history["final"] = ({"mu": mu, "s": s, "phi": phi, "w": w},
                        image.reshape(H, W))
    return history
