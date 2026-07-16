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
    splitting itself preserves the parent's sign (tested directly), so
    split-only runs must grow negatives by that slow route.
  * headline bar: at the SAME iteration and splat budget, the composite
    birth rule reaches >= 10x lower loss than the split baseline, mid-run
    (iter 1000) and final, across seeds. If not, the narrative is
    unsupported and recorded as such.
  * ATTRIBUTION ablation (review item 2): the birth rule changes
    placement, initial scale, AND initial sign at once vs split. Variants
    differing only in the newborn's initial weight -- signed / forced
    positive / zero -- isolate the sign-injection component. Whatever the
    ablation shows is reported as measured; the narrative claims only
    what the variants support.
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
    for mode in ("split", "birth", "birth_pos", "birth_zero"):
        for seed in SEEDS:
            t0 = time.perf_counter()
            hist = fit(target, EXTENT, mode, K0=K0, K_max=K_MAX,
                       iters=ITERS, grow_every=GROW_EVERY, seed=seed,
                       snapshot_every=80)
            wall = time.perf_counter() - t0
            wfin = hist["final"][0]["w"]
            print(f"  {mode:10s} seed={seed}: loss@1000={hist['loss'][1000]:.3e}"
                  f"  final={hist['loss'][-1]:.3e}  K={len(wfin)}  "
                  f"negatives={int(np.sum(wfin < 0))}  wall={wall:.0f}s",
                  flush=True)
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
    axes[0].set_title("loss: split vs birth variants (3 seeds)")
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
    print("\n=== verdicts vs declared expectations (docstring) ===")
    print(f"1. composite rule: loss ratio split/birth at iter 1000 "
          f"{[f'{g:.0f}x' for g in gaps_mid]}, final "
          f"{[f'{g:.0f}x' for g in gaps_fin]}")
    if min(gaps_mid) >= 10 and min(gaps_fin) >= 10:
        print("   -> the composite birth rule beats this split baseline by "
              ">=10x on every seed, mid-run and final.")
    else:
        print("   -> NOT SUPPORTED at the declared 10x bar on at least one "
              "seed -- recorded; do not publish the narrative.")
    print("   note: split runs DO end with negative weights (the optimizer "
          "drags weights through zero); splitting itself never flips a "
          "sign (tested directly).")
    print("2. attribution ablation (same placement and scale; only the "
          "newborn's initial weight differs):")
    for stage, idx in (("iter 1000", 1000), ("final", -1)):
        med = {m: float(np.median([results[(m, sd)]["loss"][idx]
                                   for sd in SEEDS]))
               for m in ("birth", "birth_pos", "birth_zero")}
        print(f"   {stage}: median loss birth {med['birth']:.3e}, "
              f"birth_pos {med['birth_pos']:.3e}, "
              f"birth_zero {med['birth_zero']:.3e}  "
              f"(pos/signed {med['birth_pos'] / med['birth']:.1f}x, "
              f"zero/signed {med['birth_zero'] / med['birth']:.1f}x)")
    med_f = {m: float(np.median([results[(m, sd)]["loss"][-1]
                                 for sd in SEEDS]))
             for m in ("birth", "birth_pos", "birth_zero")}
    if med_f["birth_pos"] >= 3.0 * med_f["birth"]:
        print("   -> sign injection carries a real share of the gain "
              "(forced-positive newborns are >=3x worse).")
    else:
        print("   -> PLACEMENT dominates: newborns recover from a wrong or "
              "zero initial sign quickly (a newborn's weight sits at zero "
              "scale, so the optimizer flips it cheaply -- unlike a grown "
              "splat's). The narrative must credit the birth LOCATION, "
              "not the sign injection.")


if __name__ == "__main__":
    main()
