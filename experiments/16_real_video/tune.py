"""TRAIN-ONLY tuning runner for exp16 round 1 (issue #48 Phase 1).

Reproduces, from committed code, the exact tuning trajectory recorded in
out_tuning_round1.log (the PR #59 review asked for this): four stages,
each deterministic given seed 0, with the continuation stages resuming
the previous stage's state via fit_video(resume=...):

  tune 1  K=150, stage C (600, 0.02)
  tune 2  K=250, stage C (600, 0.02), (400, 0.006)
  tune 3  resume tune 2 + per-frame pose polish (80 it, lr rot 0.004 /
          trans 0.01) + stage C (600, 0.006), (400, 0.002)
          [joint pose lrs 0.005/0.01, logf lr 0.002]
  tune 4  resume tune 3 with the blur knob ON (s_blur init log 0.8,
          Adam lr 0.01) + stage C (500, 0.006), (300, 0.002)

This script NEVER touches the held-out frames: it loads train frames
only (run.load_train). PSNR aggregation is defined here once:
  PSNR_pool  = -10 log10( mean over frames of per-frame MSE )   [primary]
  PSNR_frame = per-frame values, printed as a table               [record]
Descriptive extra (diagnosis, not a gate): PSNR_pool excluding the
mid-window train frames where a close horse crosses the scene
(train positions 4-8 = original frames 5,6,7,8,9).

Outputs: out_tuning_round1.log (regenerated) and
tuning_residuals.png (per-frame PSNR bars + worst-frame residual maps
for the final tuned state).
"""
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "15_video_conf"))
sys.path.insert(0, str(HERE))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from jointfit import _cam, fit_pose, fit_video, psnr  # noqa: E402
from splatvid import render  # noqa: E402

# both experiment dirs ship a run.py; load THIS experiment's by path
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("run16", HERE / "run.py")
_run16 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_run16)
F0, K, SHAPE = _run16.F0, _run16.K, _run16.SHAPE
load_train, pixel_grid = _run16.load_train, _run16.pixel_grid

SUSPECT = (4, 5, 6, 7, 8)  # train positions of the close-crossing horse


def train_psnrs(st, poses, frames, U, V):
    f = float(np.exp(st["logf"]))
    mses = np.array([np.mean((render(st["mu"], st["s"], st["w"], st["b"],
                                     _cam(poses[i], f, SHAPE, U, V),
                                     s_blur=st["s_blur"]) - fr) ** 2)
                     for i, fr in enumerate(frames)])
    keep = [i for i in range(len(frames)) if i not in SUSPECT]
    return mses, psnr(float(mses.mean())), psnr(float(mses[keep].mean()))


def report(tag, st, poses, frames, U, V, wall):
    mses, pool, no_sus = train_psnrs(st, poses, frames, U, V)
    sb = (f", sigma_blur={np.exp(st['s_blur']):.2f}px"
          if st["s_blur"] is not None else "")
    print(f"{tag}: PSNR_pool={pool:.2f} dB  "
          f"PSNR_pool(excl. suspect frames)={no_sus:.2f} dB  "
          f"f={np.exp(st['logf']):.1f}{sb}  (wall {wall:.0f}s)")
    print("  per-frame PSNR: "
          + " ".join(f"{psnr(float(m)):.1f}" for m in mses), flush=True)
    return mses, pool


def main():
    frames = load_train()
    U, V = pixel_grid(SHAPE)

    t0 = time.perf_counter()
    st1, po1, _ = fit_video(frames, SHAPE, F0, K=150, seed=0,
                            final_schedule=((600, 0.02),))
    report("tune 1 (K=150)", st1, po1, frames, U, V,
           time.perf_counter() - t0)

    t0 = time.perf_counter()
    st2, po2, _ = fit_video(frames, SHAPE, F0, K=K, seed=0,
                            final_schedule=((600, 0.02), (400, 0.006)))
    report("tune 2 (K=250, stepped lr)", st2, po2, frames, U, V,
           time.perf_counter() - t0)

    t0 = time.perf_counter()
    for i in range(1, len(frames)):
        fit_pose(st2, po2, i, frames[i], SHAPE, U, V, 80, 0.004, 0.01)
    st3, po3, _ = fit_video(frames, SHAPE, F0, K=K, seed=0,
                            resume=(st2, po2),
                            final_schedule=((600, 0.006), (400, 0.002)),
                            lr_pose_r=0.005, lr_pose_c=0.01,
                            lr_glob=0.002)
    report("tune 3 (pose polish + continuation)", st3, po3, frames, U, V,
           time.perf_counter() - t0)

    t0 = time.perf_counter()
    st4, po4, _ = fit_video(frames, SHAPE, F0, K=K, seed=0, use_blur=True,
                            resume=(st3, po3),
                            final_schedule=((500, 0.006), (300, 0.002)),
                            lr_pose_r=0.005, lr_pose_c=0.01,
                            lr_glob=0.002, lr_blur=0.01)
    mses, pool = report("tune 4 (blur knob ON)", st4, po4, frames, U, V,
                        time.perf_counter() - t0)

    # diagnosis figure: per-frame PSNR bars + worst-frame residuals
    H, W = SHAPE
    f = float(np.exp(st4["logf"]))
    order = np.argsort(mses)[::-1][:3]
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(2, 1, 1)
    colors = ["tab:red" if i in SUSPECT else "tab:blue"
              for i in range(len(frames))]
    ax.bar(range(len(frames)), [psnr(float(m)) for m in mses],
           color=colors)
    ax.axhline(18.0, color="k", ls="--", lw=1)
    ax.set_xlabel("train frame position (red = close-crossing horse, "
                  "descriptive)")
    ax.set_ylabel("per-frame PSNR (dB)")
    ax.set_title("tune 4 final state: the declared floor (dashed) vs "
                 "per-frame PSNR")
    for j, i in enumerate(order):
        i = int(i)
        img = render(st4["mu"], st4["s"], st4["w"], st4["b"],
                     _cam(po4[i], f, SHAPE, U, V), s_blur=st4["s_blur"])
        axr = fig.add_subplot(2, 3, 4 + j)
        axr.imshow(np.abs(img - frames[i]).reshape(H, W), cmap="magma",
                   origin="upper")
        axr.set_title(f"|residual| frame pos {i} "
                      f"({psnr(float(mses[i])):.1f} dB)", fontsize=9)
        axr.set_xticks([]); axr.set_yticks([])
    fig.tight_layout()
    fig.savefig(HERE / "tuning_residuals.png", dpi=110)
    print(f"figure: {HERE / 'tuning_residuals.png'}")

    print("\nVERDICT: declared precondition is PSNR_pool >= 18 dB. "
          f"Final tuned value {pool:.2f} dB -> "
          + ("met." if pool >= 18.0 else
             "NOT met: DNF, held-out frames never loaded by this script "
             "(run.py enforces the same stop before evaluation)."))


if __name__ == "__main__":
    main()
