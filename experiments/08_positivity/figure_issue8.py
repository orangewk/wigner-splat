"""Issue #8 resolution figure: physical fidelity vs the unphysical splat.

Renders the decisive three-mode comparison on the IDENTICAL fidelity functional
F = tr(rho_recon rho_cat3) = (2 pi)^3 integral W_recon W_cat3:

    signed splat (unphysical)  |  splat PSD-projected  |  BB^dagger (physical)

with the finite-data ML ceiling (~0.95) and the true-state F=1 as references.
Numbers are the measured results (experiments/08_positivity/bbdag_3mode.py and
exp06 seed 42). Scope printed on the figure per the oracle fairness review:
resolved FOR THIS cat benchmark; BB^dagger ansatz contains the target family;
the FD optimizer is slow (500-1600 s vs the splat's ~15 s).
"""
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "issue8_resolution.png"

# measured results (tr(rho rho_cat3) metric, exp06 seed 42 data)
LABELS = ["signed splat\n(generic)", "splat\nPSD-projected", "BB†  K=4\n(physical)", "BB†  K=8\n(physical)"]
F = [0.756, 0.48, 0.9501, 0.9507]
PHYSICAL = [False, True, True, True]
WALL = [15, 15, 527, 1647]  # s
ML_CEILING = 0.95
TRUE_F = 1.0


def main():
    fig, (ax, axw) = plt.subplots(1, 2, figsize=(11, 5.2), width_ratios=[3, 1.4])

    colors = ["#c0392b" if not p else "#27ae60" for p in PHYSICAL]
    hatch = ["////" if not p else None for p in PHYSICAL]
    x = np.arange(len(F))
    bars = ax.bar(x, F, color=colors, edgecolor="black", hatch=hatch, width=0.62)
    for xi, f in zip(x, F):
        ax.text(xi, f + 0.015, f"{f:.3f}", ha="center", va="bottom",
                fontsize=11, fontweight="bold")

    ax.axhline(ML_CEILING, color="#2c3e50", ls="--", lw=1.3)
    ax.text(1.5, ML_CEILING - 0.05, "finite-data ML ceiling ~0.95",
            ha="center", va="top", fontsize=9, color="#2c3e50")
    ax.axhline(TRUE_F, color="gray", ls=":", lw=1.0)
    ax.text(0.02, TRUE_F - 0.03, "true state F = 1", fontsize=8.5, color="gray")

    ax.set_xticks(x)
    ax.set_xticklabels(LABELS, fontsize=9.5)
    ax.set_ylabel(r"fidelity  $F=\mathrm{tr}(\rho_{\rm recon}\,\rho_{\rm cat3})$", fontsize=11)
    ax.set_ylim(0, 1.08)
    ax.set_title("Issue #8 — 3-mode cat: physical reconstruction beats the\n"
                 "unphysical splat on the SAME metric", fontsize=12, fontweight="bold")

    # physicality legend
    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(facecolor="#27ae60", edgecolor="black", label="physical (min eig ≥ 0)"),
        Patch(facecolor="#c0392b", edgecolor="black", hatch="////",
              label="UNphysical (min eig < 0)"),
    ], loc="lower left", fontsize=9, framealpha=0.95)

    # wall-clock panel (log scale) -- the honest cost caveat
    axw.bar(x, WALL, color=["#7f8c8d", "#7f8c8d", "#2980b9", "#2980b9"],
            edgecolor="black", width=0.62)
    axw.set_yscale("log")
    axw.set_xticks(x)
    axw.set_xticklabels(["splat", "proj", "K=4", "K=8"], fontsize=9)
    axw.set_ylabel("wall clock (s, log)", fontsize=10)
    axw.set_title("cost caveat:\nFD optimizer is slow", fontsize=10)
    for xi, w in zip(x, WALL):
        axw.text(xi, w * 1.15, f"{w}s", ha="center", va="bottom", fontsize=8.5)

    fig.text(0.5, 0.005,
             "Scope (oracle fairness review): resolved FOR THIS cat benchmark. "
             "BB† ansatz contains the target family; analytic gradients + "
             "out-of-family targets are the open follow-ups.",
             ha="center", fontsize=8, color="#555", wrap=True)

    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(OUT, dpi=140)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
