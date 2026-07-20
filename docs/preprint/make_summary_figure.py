"""Summary figure for the preprint (#69): the exp19/20/21 story in two panels.

Panel (a): the exp20 family boundary on the detection-efficiency axis
    eta' in (0, 1] -- regime I/II/boundary/III with the theorem that
    excludes each, plus the Route-B best-fit eta' (which lands just
    inside regime III, at the PSD boundary the fits push against).
Panel (b): the exp21 robustness sweep -- representative lossy fidelity
    vs the 900 s-budget MLE on all five pre-declared configurations
    (hatched MLE bars: convergence criterion not met within budget).

Numbers are read from committed results.json files; regime constants
match experiments/20_noninclusion (ETA = 0.8, SIGMA = 0.1).
"""

import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent / "summary_figure.png"

# Route B fitted eta' (experiments/20_noninclusion/results_routeB.json):
# per rank K, the best-F squeezed-family fit at the largest scoring cutoff.
routeB = json.loads(
    (ROOT / "experiments/20_noninclusion/results_routeB.json").read_text()
)

# exp20 constants, from the committed result data (single source of truth)
ETA = routeB["params"]["eta"]
SIGMA = routeB["params"]["sigma"]
ETA_CRIT = ETA - SIGMA  # 0.70
rows = routeB["squeezed"]
n_max = max(r["n_score"] for r in rows)
routeB_etas = [
    max(
        (r for r in rows if r["K"] == K and r["n_score"] == n_max),
        key=lambda r: r["F"],
    )["eta_p"]
    for K in sorted({r["K"] for r in rows})
]

# exp21 sweep (experiments/21_thermal_sweep/results.json)
sweep = json.loads(
    (ROOT / "experiments/21_thermal_sweep/results.json").read_text()
)
configs = sweep["configs"]

# The panel-(b) title states the verdict -- derive it from the data so a
# regenerated figure cannot silently keep a stale claim.
ruling = sweep["ruling"]
assert ruling["holds"] == ruling["total"] == len(configs) == 5, ruling
assert all(c["verdict_lossy_ge_mle"] for c in configs), "verdict flag flipped"

fig, (ax_a, ax_b) = plt.subplots(
    2, 1, figsize=(7.2, 5.4), gridspec_kw={"height_ratios": [1.0, 1.6]}
)

# ---------------------------------------------------------------- panel (a)
REGIONS = [
    (0.0, ETA_CRIT, "#d9e8f5", "III: no PSD pre-image\n(Thm. 1)"),
    (ETA_CRIT, ETA, "#f5e3d0", "II\n(Lemma 2)"),
    (ETA, 1.0, "#e5f0dc", "I: full rank\n(Lemma 2)"),
]
XMIN = 0.0  # full theorem domain (0, 1]
for x0, x1, color, label in REGIONS:
    ax_a.axvspan(x0, x1, color=color)
    ax_a.text(
        (max(x0, XMIN) + x1) / 2, 0.72, label,
        ha="center", va="center", fontsize=8.5,
    )

ax_a.axvline(ETA_CRIT, color="#8a4a10", lw=1.6)
ax_a.annotate(
    "boundary $\\eta' = \\eta - \\sigma$:\nno finite rank (Thm. 2)",
    xy=(ETA_CRIT, 0.32),
    xytext=(0.30, 0.32),
    fontsize=8.5,
    ha="center",
    va="center",
    arrowprops=dict(arrowstyle="->", lw=0.9, shrinkA=8),
)
ax_a.axvline(ETA, color="#5b6b3a", lw=1.0, ls=":")
ax_a.text(ETA + 0.008, 0.94, "$\\eta = 0.8$", ha="left", va="top", fontsize=8)

for e in routeB_etas:
    ax_a.plot([e], [0.10], marker="v", color="#20456b", ms=7, clip_on=False)
ax_a.text(
    min(routeB_etas) - 0.015,
    0.10,
    "best-approximation fits\n(Route B, free $\\eta'$)",
    ha="right",
    va="center",
    fontsize=8,
    color="#20456b",
)

ax_a.set_xlim(0.0, 1.0)
ax_a.set_ylim(0, 1)
ax_a.set_yticks([])
ax_a.set_xlabel("assumed detection efficiency $\\eta'$", fontsize=9)
ax_a.set_title(
    "(a)  exp20: outside the loss-composed family for every $\\eta'$, "
    "every finite rank",
    fontsize=9.5,
    loc="left",
)

# ---------------------------------------------------------------- panel (b)
labels = [
    f"seed {c['data_seed']}\n$\\sigma_{{add}}$ = {c['sigma_add']:.2f}"
    for c in configs
]
lossy = [c["F_lossy"] for c in configs]
mle = [c["F_mle"] for c in configs]
conv = [c["mle_converged"] for c in configs]

x = range(len(configs))
w = 0.38
ax_b.bar(
    [i - w / 2 for i in x],
    lossy,
    width=w,
    color="#20456b",
)
for i, (m, cv) in enumerate(zip(mle, conv)):
    ax_b.bar(
        i + w / 2,
        m,
        width=w,
        color="#b0653a",
        hatch="" if cv else "///",
        edgecolor="white" if cv else "#7a3d1a",
        label=None,
    )
legend_handles = [
    Patch(color="#20456b", label="loss-composed rank-2 (blind selection)"),
    Patch(color="#b0653a", label="full-rank MLE (900 s budget)"),
    Patch(
        facecolor="#b0653a",
        hatch="///",
        edgecolor="#7a3d1a",
        label="MLE: not converged within budget",
    ),
]

for i, (l, m) in enumerate(zip(lossy, mle)):
    ax_b.annotate(
        f"+{l - m:.3f}",
        xy=(i, max(l, m) + 0.012),
        ha="center",
        fontsize=8,
    )

ax_b.set_xticks(list(x))
ax_b.set_xticklabels(labels, fontsize=8)
ax_b.set_ylim(0.75, 1.0)
ax_b.set_ylabel("generalized fidelity to target", fontsize=9)
ax_b.legend(handles=legend_handles, fontsize=7.5, loc="lower left", framealpha=0.95)
ax_b.set_title(
    "(b)  exp21: the blind verdict holds on all five pre-declared "
    "configurations",
    fontsize=9.5,
    loc="left",
)

fig.tight_layout()
fig.savefig(OUT, dpi=200)
print(f"wrote {OUT}")
