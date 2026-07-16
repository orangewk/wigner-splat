"""Birth-field demo: fit the cat-state Wigner function as a plain image.

Produces the outreach assets for #46 idea 4:
  * birthfield_demo.gif  -- 5-panel animation of the BIRTH run (target,
    reconstruction, signed splat map, birth field, loss curve);
  * comparison.png       -- split-only vs birth loss curves (3 seeds each)
    and the final images side by side;
  * out_run.log          -- the committed numbers.

The target is this repository's own object of study: the Wigner function
of the cat state |alpha> + |-alpha| (alpha = 2), whose interference
fringes are NEGATIVE regions -- the structure that split/clone
densification cannot inject directly, because a split preserves its
parent's sign (exp02 lesson, restated precisely below).

Declared expectation (corrected after a first exploratory run -- the
naive "split can NEVER obtain negatives" reading is wrong for this
objective, because gradient descent can drag a weight through zero):
splitting preserves each splat's sign, so split-only runs must grow their
negatives by the slow weight-through-zero route, visible as long plateaus
in the loss; the birth field injects the right sign at the right place
directly. The measurable claim: at the SAME iteration and splat budget,
birth reaches >= 10x lower loss than split-only, both mid-run (iter 1000)
and at the end, across seeds. If split-only keeps up, the demo narrative
is unsupported and is recorded as such.
"""
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse  # noqa: E402
from PIL import Image  # noqa: E402

from birthfield2d import fit  # noqa: E402
from wigner_splat.fock import cat_fock, wigner_from_rho  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ALPHA = 2.0
EXTENT = 4.0
GRID = 96
SEEDS = (0, 1, 2)
ITERS = 4000
GROW_EVERY = 150
K0, K_MAX = 4, 40


def cat_wigner_image():
    rho = np.outer(*(2 * [cat_fock(ALPHA, +1, n_max=30)]))
    xs = np.linspace(-EXTENT, EXTENT, GRID)
    W = wigner_from_rho(rho, xs[None, :], xs[:, None])
    return W / np.max(np.abs(W)), xs


def draw_splats(ax, params, extent):
    for k in range(len(params["w"])):
        sig1, sig2 = np.exp(params["s"][k]) * 2.0  # 2-sigma outline
        color = "tab:blue" if params["w"][k] >= 0 else "tab:red"
        ax.add_patch(Ellipse(params["mu"][k], 2 * sig1, 2 * sig2,
                             angle=np.degrees(params["phi"][k]),
                             fill=False, color=color,
                             lw=1.0 + 2.0 * min(1, abs(params["w"][k]))))
    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect("equal")


def make_gif(target, hist, path):
    frames = []
    losses = hist["loss"]
    for it, params, image, B in hist["snapshots"]:
        fig, axes = plt.subplots(1, 5, figsize=(16, 3.4))
        for ax, img, title in [(axes[0], target, "target (cat Wigner)"),
                               (axes[1], image, f"reconstruction  it={it}")]:
            ax.imshow(img, cmap="RdBu_r", vmin=-1, vmax=1, origin="lower",
                      extent=[-EXTENT, EXTENT, -EXTENT, EXTENT])
            ax.set_title(title, fontsize=10)
            ax.set_xticks([]); ax.set_yticks([])
        draw_splats(axes[2], params, EXTENT)
        neg = int(np.sum(params["w"] < 0))
        axes[2].set_title(f"splats: {len(params['w'])} "
                          f"(negative: {neg})", fontsize=10)
        axes[2].set_xticks([]); axes[2].set_yticks([])
        vB = np.max(np.abs(B)) + 1e-12
        axes[3].imshow(B, cmap="PiYG", vmin=-vB, vmax=vB, origin="lower",
                       extent=[-EXTENT, EXTENT, -EXTENT, EXTENT])
        axes[3].set_title("birth field  dL/dw(mu)", fontsize=10)
        axes[3].set_xticks([]); axes[3].set_yticks([])
        axes[4].semilogy(losses[:it], color="k", lw=1.2)
        for ev_it, kind, _, _ in hist["events"]:
            if ev_it <= it and kind == "birth":
                axes[4].axvline(ev_it, color="tab:red", alpha=0.25, lw=0.8)
        axes[4].set_xlim(0, ITERS)
        axes[4].set_title("loss (red lines: births)", fontsize=10)
        fig.tight_layout()
        fig.canvas.draw()
        frames.append(Image.fromarray(
            np.asarray(fig.canvas.buffer_rgba())[..., :3]))
        plt.close(fig)
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=140, loop=0)


def main():
    target, _ = cat_wigner_image()
    print("=== birth-field demo: cat Wigner as an image target ===")
    print(f"target: alpha={ALPHA} even cat, {GRID}x{GRID}, "
          f"negative fraction {np.mean(target < -0.02):.2f}")

    results = {}
    for mode in ("split", "birth"):
        for seed in SEEDS:
            t0 = time.perf_counter()
            hist = fit(target, EXTENT, mode, K0=K0, K_max=K_MAX,
                       iters=ITERS, grow_every=GROW_EVERY, seed=seed,
                       snapshot_every=80)
            wall = time.perf_counter() - t0
            wfin = hist["final"][0]["w"]
            print(f"  {mode:5s} seed={seed}: final loss={hist['loss'][-1]:.5f}  "
                  f"K={len(wfin)}  negatives={int(np.sum(wfin < 0))}  "
                  f"wall={wall:.0f}s", flush=True)
            results[(mode, seed)] = hist

    # comparison figure
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.6))
    for mode, color in (("split", "tab:blue"), ("birth", "tab:red")):
        for seed in SEEDS:
            axes[0].semilogy(results[(mode, seed)]["loss"], color=color,
                             alpha=0.6, lw=1.2,
                             label=mode if seed == SEEDS[0] else None)
    axes[0].legend(); axes[0].set_title("loss: split-only vs birth (3 seeds)")
    axes[0].set_xlabel("iteration")
    best = {m: min(SEEDS, key=lambda sd: results[(m, sd)]["loss"][-1])
            for m in ("split", "birth")}
    panels = [(target, "target"),
              (results[("split", best["split"])]["final"][1],
               f"split-only best (loss "
               f"{results[('split', best['split'])]['loss'][-1]:.1e})"),
              (results[("birth", best["birth"])]["final"][1],
               f"birth best (loss "
               f"{results[('birth', best['birth'])]['loss'][-1]:.1e})")]
    for ax, (img, title) in zip(axes[1:], panels):
        ax.imshow(img, cmap="RdBu_r", vmin=-1, vmax=1, origin="lower")
        ax.set_title(title, fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(HERE / "comparison.png", dpi=100)

    make_gif(target, results[("birth", best["birth"])],
             HERE / "birthfield_demo.gif")
    print(f"  assets: {HERE / 'birthfield_demo.gif'}, "
          f"{HERE / 'comparison.png'}")

    gaps_mid = [results[("split", sd)]["loss"][1000]
                / results[("birth", sd)]["loss"][1000] for sd in SEEDS]
    gaps_fin = [results[("split", sd)]["loss"][-1]
                / results[("birth", sd)]["loss"][-1] for sd in SEEDS]
    print("\n=== verdict vs declared expectation (docstring) ===")
    print(f"loss ratio split/birth at iter 1000 per seed: "
          f"{[f'{g:.0f}x' for g in gaps_mid]}")
    print(f"loss ratio split/birth at the end per seed:   "
          f"{[f'{g:.0f}x' for g in gaps_fin]}")
    print("note: split-only runs DO end with negative weights -- gradient "
          "descent drags weights through zero -- but that route is slow "
          "(the plateaus in the blue curves); splitting itself never flips "
          "a sign.")
    if min(gaps_mid) >= 10 and min(gaps_fin) >= 10:
        print("-> CONFIRMED: at matched iteration and splat budget the "
              "birth field beats split-only by >=10x on every seed, "
              "mid-run and final, by injecting signed splats where the "
              "residual demands them.")
    else:
        print("-> NOT SUPPORTED at the declared 10x bar on at least one "
              "seed -- recorded; do not publish the narrative.")


if __name__ == "__main__":
    main()
