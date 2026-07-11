"""Issue #8 benchmark figure: target-aligned physical existence result.

Renders historical reported values for the synthetic three-mode cat:

    signed splat (non-PSD overlap score) | PSD projection | BB^dagger fidelity

BB^dagger contains the target family and uses per-sample NLL; the signed splat
is a different representation trained with histogram L2. The figure therefore
shows an existence result, not a physicalization of the existing splat.
BB^dagger/projection raw logs and fit parameters were not retained. Phase B will
replace these hard-coded historical reports with a machine-readable artifact.
"""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "issue8_resolution.png"

# Historical reports for exp06 seed-42 data. Phase B replaces these constants
# with a machine-readable artifact and explicit evidence levels.
LABELS = [
    "signed splat\n(overlap score)",
    "splat\nPSD-projected",
    "BB†  K=4\n(target-aligned)",
    "BB†  K=8\n(target-aligned)",
]
F = [0.7562, 0.48, 0.9501, 0.9507]
PHYSICAL = [False, True, True, True]
WALL = [15.5, np.nan, 527, 1647]  # projection wall time was not retained
EVIDENCE_MARK = ["", "*", "*", "*"]
TRUE_F = 1.0


def main():
    fig, (ax, axw) = plt.subplots(1, 2, figsize=(11, 5.4), width_ratios=[3, 1.4])

    colors = ["#c0392b" if not p else "#27ae60" for p in PHYSICAL]
    hatch = ["////" if not p else None for p in PHYSICAL]
    x = np.arange(len(F))
    ax.bar(x, F, color=colors, edgecolor="black", hatch=hatch, width=0.62)
    for xi, f, mark in zip(x, F, EVIDENCE_MARK):
        ax.text(xi, f + 0.015, f"{f:.3f}{mark}", ha="center", va="bottom",
                fontsize=11, fontweight="bold")

    ax.axhline(TRUE_F, color="gray", ls=":", lw=1.0)
    ax.text(0.02, TRUE_F - 0.03, "true state F = 1", fontsize=8.5, color="gray")

    ax.set_xticks(x)
    ax.set_xticklabels(LABELS, fontsize=9.5)
    ax.set_ylabel("reported cat-target overlap / state fidelity", fontsize=11)
    ax.set_ylim(0, 1.08)
    ax.set_title("3-mode synthetic cat: target-aligned physical ansatz\n"
                 "attains high reported fidelity", fontsize=12, fontweight="bold")

    # physicality legend
    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(facecolor="#27ae60", edgecolor="black", label="physical (min eig ≥ 0)"),
        Patch(facecolor="#c0392b", edgecolor="black", hatch="////",
              label="non-PSD overlap score"),
    ], loc="lower left", fontsize=9, framealpha=0.95)

    # wall-clock panel (log scale) -- the honest cost caveat
    axw.bar(x, WALL, color=["#7f8c8d", "#7f8c8d", "#2980b9", "#2980b9"],
            edgecolor="black", width=0.62)
    axw.set_yscale("log")
    axw.set_xticks(x)
    axw.set_xticklabels(["splat", "proj", "K=4", "K=8"], fontsize=9)
    axw.set_ylabel("wall clock (s, log)", fontsize=10)
    axw.set_title("historical cost reports:\nFD optimizer is slow", fontsize=10)
    for xi, w, mark in zip(x, WALL, EVIDENCE_MARK):
        if np.isfinite(w):
            axw.text(xi, w * 1.15, f"{w:g}s{mark}",
                     ha="center", va="bottom", fontsize=8.5)
        else:
            axw.text(xi, 20, "not\nrecorded", ha="center", va="bottom", fontsize=8)

    fig.text(0.5, 0.012,
             "Existence result only: BB† contains the target family and uses "
             "per-sample NLL; signed splat uses histogram L2.\n"
             "This does not determine whether the existing splat's negative-eigenvalue "
             "components are necessary.  * historical report; raw BB†/projection "
             "log and fit parameters not retained.",
             ha="center", va="bottom", fontsize=7.5, color="#555", wrap=True)

    fig.tight_layout(rect=[0, 0.13, 1, 1])
    fig.savefig(OUT, dpi=140)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
