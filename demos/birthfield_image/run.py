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

Declared expectations (corrected after a first exploratory run and the
PR #49 review):
  * the naive "split can NEVER obtain negatives" reading is wrong for
    this objective -- gradient descent can drag a weight through zero;
    what holds (and is tested directly) is that splitting itself
    preserves the parent's sign.
  * HEADLINE (fixed shared budget, per the re-review): the comparison
    BENCH runs every mode x seed to exactly 1000 updates (all modes at
    K = 10); the composite birth growth rule must reach >= 10x lower loss
    than the split baseline on every seed (paired, same seed). A 4000-
    update sweep exists only behind --full (one-off auxiliary; the
    committed record of it lives in the research log). The GIF comes from
    a separate PRE-FIXED run (mode 'birth', seed GIF_SEED) to 4000
    updates -- a completion illustration, never comparison evidence.
  * ATTRIBUTION ablation, PAIRED: variants differing only in the
    newborn's initial weight -- signed / forced positive / zero --
    isolate ONLY the sign-injection component (placement, initial scale,
    and generation method remain shared with 'birth' but different from
    'split'). Aggregation is per-seed paired ratios with their median --
    NOT medians of separate pools. The supported conclusion shape is
    therefore "sign injection is/is not a main factor" and "the COMPOSITE
    birth rule beats this split baseline"; placement-only claims would
    need a separate scale/position ablation and are NOT made here.
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
ITERS_BENCH = 1000   # the shared comparison budget (all modes at K=10)
ITERS_FULL = 4000    # --full auxiliary sweep / the fixed GIF run
GIF_SEED = 0         # pre-fixed BEFORE running; never selected post hoc
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
        axes[4].set_xlim(0, len(losses))
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

    full = "--full" in sys.argv
    iters = ITERS_FULL if full else ITERS_BENCH
    print(f"bench budget: {iters} updates per run"
          + (" (--full auxiliary sweep)" if full else ""))
    results = {}
    for mode in ("split", "birth", "birth_pos", "birth_zero"):
        for seed in SEEDS:
            t0 = time.perf_counter()
            hist = fit(target, EXTENT, mode, K0=K0, K_max=K_MAX,
                       iters=iters, grow_every=GROW_EVERY, seed=seed,
                       snapshot_every=10 ** 9)
            wall = time.perf_counter() - t0
            wfin = hist["final"][0]["w"]
            print(f"  {mode:10s} seed={seed}: loss@end={hist['loss'][-1]:.3e}"
                  f"  K={len(wfin)}  negatives={int(np.sum(wfin < 0))}  "
                  f"wall={wall:.0f}s", flush=True)
            results[(mode, seed)] = hist

    # comparison figure
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.6))
    for mode, color in (("split", "tab:blue"), ("birth", "tab:red"),
                        ("birth_pos", "tab:orange"),
                        ("birth_zero", "tab:green")):
        for seed in SEEDS:
            axes[0].semilogy(results[(mode, seed)]["loss"], color=color,
                             alpha=0.6, lw=1.2,
                             label=mode if seed == SEEDS[0] else None)
    axes[0].legend(fontsize=8)
    axes[0].set_title(f"loss to the shared budget ({iters} updates, 3 seeds)")
    axes[0].set_xlabel("iteration")
    panels = [(target, "target"),
              (results[("split", GIF_SEED)]["final"][1],
               f"split, seed {GIF_SEED} (loss "
               f"{results[('split', GIF_SEED)]['loss'][-1]:.1e})"),
              (results[("birth", GIF_SEED)]["final"][1],
               f"birth, seed {GIF_SEED} (loss "
               f"{results[('birth', GIF_SEED)]['loss'][-1]:.1e})")]
    for ax, (img, title) in zip(axes[1:], panels):
        ax.imshow(img, cmap="RdBu_r", vmin=-1, vmax=1, origin="lower")
        ax.set_title(title, fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(HERE / "comparison.png", dpi=100)

    print(f"  GIF run: mode=birth seed={GIF_SEED} (pre-fixed), "
          f"{ITERS_FULL} updates -- illustration only", flush=True)
    gif_hist = fit(target, EXTENT, "birth", K0=K0, K_max=K_MAX,
                   iters=ITERS_FULL, grow_every=GROW_EVERY, seed=GIF_SEED,
                   snapshot_every=80)
    make_gif(target, gif_hist, HERE / "birthfield_demo.gif")
    print(f"  assets: {HERE / 'birthfield_demo.gif'}, "
          f"{HERE / 'comparison.png'}")

    print("\n=== verdicts vs declared expectations (docstring) ===")
    gaps_1k = [results[("split", sd)]["loss"][-1]
               / results[("birth", sd)]["loss"][-1] for sd in SEEDS]
    print(f"1. HEADLINE, fixed shared budget of {iters} updates, per-seed "
          "PAIRED split/birth loss ratios: "
          f"{[f'{g:.0f}x' for g in gaps_1k]}")
    if min(gaps_1k) >= 10:
        print("   -> the composite birth growth rule beats this split "
              "baseline by >=10x on every seed at the shared budget.")
    else:
        print("   -> NOT SUPPORTED at the declared 10x bar on at least one "
              "seed -- recorded; do not publish the narrative.")
    print("   note: split runs acquire negative weights over long runs "
          "(the optimizer can drag a weight through zero); splitting "
          "itself never flips a sign (tested directly).")
    print("2. attribution ablation, PAIRED per seed (only the newborn's "
          "initial weight differs; placement/scale/method shared with "
          "'birth'):")
    for variant in ("birth_pos", "birth_zero"):
        ratios = [results[(variant, sd)]["loss"][-1]
                  / results[("birth", sd)]["loss"][-1] for sd in SEEDS]
        print(f"   at {iters} updates: {variant}/birth per seed "
              f"{[f'{r:.3f}' for r in ratios]}  "
              f"paired median {np.median(ratios):.3f}x")
    pos_1k = np.median([results[("birth_pos", sd)]["loss"][-1]
                        / results[("birth", sd)]["loss"][-1]
                        for sd in SEEDS])
    if pos_1k >= 3.0:
        print("   -> sign injection carries a real share of the gain "
              "(forced-positive newborns >=3x worse, paired median).")
    else:
        print("   -> sign injection is NOT a main factor: forced-positive "
              "and zero-init newborns land within small factors of signed "
              "ones (paired medians above). What these data support: the "
              "COMPOSITE birth rule (placement + initial scale + "
              "generation method) beats this split baseline; attributing "
              "the gain to placement ALONE would need a separate "
              "scale/position ablation, not run here.")


if __name__ == "__main__":
    main()
