"""Incremental joint pose+splat fitting for real video (issue #48 Phase 1).

No COLMAP / no feature tracking in this environment, so poses come from
the same gradient machinery as everything else (MonoGS-style joint
optimization, reduced to our minimal renderer):

  stage A   fit splats + background on frame 0 alone (pose = gauge, fixed);
  stage B   for each next train frame: init its pose from the previous
            frame, optimize the POSE ALONE (splats frozen), then jointly
            refine splats + the poses inside a sliding window;
  stage C   final joint pass over all train frames (splats, background,
            all poses except frame 0, global log-focal, and -- when the
            blur knob is on -- the global s_blur).

Adam throughout; rotation moments live in the per-step identity chart
(standard small-angle approximation). Frame 0's pose is the gauge anchor;
global scale remains a gauge freedom (harmless for the Phase 1 metrics,
which are all image-space).
"""
import numpy as np

import splatvid
from splatvid import rot_exp


class _Adam:
    def __init__(self, shape, lr):
        self.m = np.zeros(shape)
        self.v = np.zeros(shape)
        self.t = 0
        self.lr = lr

    def step(self, g):
        self.t += 1
        self.m = 0.9 * self.m + 0.1 * g
        self.v = 0.999 * self.v + 0.001 * g ** 2
        return self.lr * (self.m / (1 - 0.9 ** self.t)) / (
            np.sqrt(self.v / (1 - 0.999 ** self.t)) + 1e-8)


def _cam(pose, f, shape, U, V):
    H, W = shape
    return {"R": pose[0], "c": pose[1], "f": f, "cx": (W - 1) / 2.0,
            "cy": (H - 1) / 2.0, "shape": shape, "U": U, "V": V}


def init_state(frame0, shape, f0, K, seed, z_range=(2.0, 10.0)):
    """Back-project K random pixels of frame 0 at random depths."""
    rng = np.random.default_rng(seed)
    H, W = shape
    us = rng.uniform(0, W - 1, K)
    vs = rng.uniform(0, H - 1, K)
    z = rng.uniform(*z_range, K)
    mu = np.column_stack([(us - (W - 1) / 2) / f0 * z,
                          (vs - (H - 1) / 2) / f0 * z, z])
    s = np.log(3.0 * z / f0)          # ~3 px footprints to start
    w = 0.05 * rng.standard_normal(K)
    b = float(np.median(frame0))
    return {"mu": mu, "s": s, "w": w, "b": b, "logf": float(np.log(f0)),
            "s_blur": None}


def fit_video(frames, shape, f0, K=150, seed=0, use_blur=False,
              iters_a=300, iters_pose=60, iters_win=60, window=5,
              final_schedule=((600, 0.02),), lr_splat=0.02,
              lr_pose_c=0.02, lr_pose_r=0.01, lr_glob=0.005,
              lr_blur=None, resume=None, renderer=None,
              opacity_init=None, log_every=None):
    """frames: (F, H*W) flattened train frames in order. Returns (state,
    poses, history).

    resume: optional (state, poses) from a previous fit_video call --
    stages A and B are skipped and only the stage-C final_schedule runs
    (the continuation path used by the committed tuning trajectory;
    Adam moments restart fresh, as in the original runs).

    renderer: module providing render/render_and_grad (default splatvid;
    pass composite for the round-2 alpha-compositing model, which adds a
    per-splat opacity logit "o" to the state, initialized at
    opacity_init).
    """
    rd = splatvid if renderer is None else renderer
    F = len(frames)
    H, W = shape
    vs, us = np.meshgrid(np.arange(H, dtype=float),
                         np.arange(W, dtype=float), indexing="ij")
    U, V = us.ravel(), vs.ravel()
    if resume is None:
        st = init_state(frames[0], shape, f0, K, seed)
        if opacity_init is not None:
            st["o"] = np.full(K, float(opacity_init))
        poses = [(np.eye(3), np.zeros(3))]
    else:
        st = dict(resume[0])
        poses = [(R.copy(), c.copy()) for R, c in resume[1]]
        assert len(poses) == F
    history = {"stage": [], "loss": []}

    def cams(f_idx):
        f = float(np.exp(st["logf"]))
        return _cam(poses[f_idx], f, shape, U, V)

    def joint_pass(idxs, n_iter, opt_pose, opt_glob, tag, lr=None):
        keys = ("mu", "s", "w", "b") + (("o",) if "o" in st else ())
        ad = {k: _Adam(np.shape(st[k]), lr or lr_splat) for k in keys}
        if opt_glob:
            ad["logf"] = _Adam((), lr_glob)
            if st["s_blur"] is not None:
                ad["s_blur"] = _Adam((), lr_blur if lr_blur is not None
                                     else lr_glob)
        pad = {i: (_Adam(3, lr_pose_r), _Adam(3, lr_pose_c))
               for i in idxs if i != 0 and opt_pose}
        for it in range(n_iter):
            g = {k: np.zeros(np.shape(st[k])) for k in ad}
            loss = 0.0
            for i in idxs:
                extra = {"o": st["o"]} if "o" in st else {}
                L, _, gf = rd.render_and_grad(st["mu"], st["s"], st["w"],
                                              st["b"], cams(i), frames[i],
                                              s_blur=st["s_blur"], **extra)
                loss += L / len(idxs)
                for k in ad:
                    g[k] += np.asarray(gf[k]) / len(idxs)
                if i in pad:
                    aR, ac = pad[i]
                    R, c = poses[i]
                    poses[i] = (rot_exp(-aR.step(gf["rot"])) @ R,
                                c - ac.step(gf["c"]))
            for k in ad:
                st[k] = st[k] - ad[k].step(g[k])
            history["stage"].append(tag)
            history["loss"].append(loss)
            if log_every and (it + 1) % log_every == 0:
                print(f"    [{tag}] iter {it + 1}/{n_iter} "
                      f"loss={loss:.4e}", flush=True)

    if resume is None:
        # stage A: frame 0 alone, pose fixed
        joint_pass([0], iters_a, opt_pose=False, opt_glob=False, tag="A")

        # stage B: incremental frames
        for f_idx in range(1, F):
            poses.append((poses[-1][0].copy(), poses[-1][1].copy()))
            fit_pose(st, poses, f_idx, frames[f_idx], shape, U, V,
                     iters_pose, lr_pose_r, lr_pose_c, renderer=rd)
            lo = max(0, f_idx - window + 1)
            joint_pass(list(range(lo, f_idx + 1)), iters_win,
                       opt_pose=True, opt_glob=False, tag=f"B{f_idx}")

    # stage C: global joint passes (optionally with stepped-down lr)
    if use_blur and st["s_blur"] is None:
        st["s_blur"] = float(np.log(0.8))
    for ci, (n_iter, lr) in enumerate(final_schedule):
        joint_pass(list(range(F)), n_iter, opt_pose=True, opt_glob=True,
                   tag=f"C{ci}", lr=lr)
    return st, poses, history


def fit_pose(st, poses, f_idx, frame, shape, U, V, n_iter,
             lr_pose_r=0.01, lr_pose_c=0.02, renderer=None):
    """Optimize ONE frame's pose with the splats frozen (also used for
    held-out frames at evaluation time, per the declared protocol)."""
    rd = splatvid if renderer is None else renderer
    aR, ac = _Adam(3, lr_pose_r), _Adam(3, lr_pose_c)
    f = float(np.exp(st["logf"]))
    extra = {"o": st["o"]} if "o" in st else {}
    for _ in range(n_iter):
        R, c = poses[f_idx]
        cam = _cam((R, c), f, shape, U, V)
        _, _, g = rd.render_and_grad(st["mu"], st["s"], st["w"], st["b"],
                                     cam, frame, s_blur=st["s_blur"],
                                     **extra)
        poses[f_idx] = (rot_exp(-aR.step(g["rot"])) @ R,
                        c - ac.step(g["c"]))


def psnr(mse):
    return -10.0 * np.log10(max(mse, 1e-12))
