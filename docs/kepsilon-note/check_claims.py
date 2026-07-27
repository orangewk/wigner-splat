"""Build gate for the K_epsilon note: verify a declared list of the numbers
the note attributes to committed artifacts — including numbers asserted
inside prose metadata fields — against the artifact JSONs themselves.
Coverage is the checks coded below, not literally every number in the note
(energies, delta values outside pinned checks, and physical parameters are
spot-checked only).

Principle (issue #71, 2026-07-26): prose that makes a claim gets that claim
checked. Three same-shaped failures motivated this gate: routeB's hardcoded
verdict print, the exp22 K-axis conflation, and the blanket psi_trunc
declaration that under-reported exp23's lifted results.

Run:  python docs/kepsilon-note/check_claims.py   (exit 0 = coded checks pass)
"""
from __future__ import annotations

import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
NOTE = pathlib.Path(__file__).resolve().parent / "note.md"

FAILURES: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        FAILURES.append(f"{label}: {detail}")


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    note = NOTE.read_text(encoding="utf-8")

    # --- exp20 Route B (section 6, C'3): the three quoted 1-F values must be
    # the best-F squeezed rows at the largest scoring cutoff, and the series
    # must still be increasing (so "cutoff-stable" stays banned).
    rb = load("experiments/20_noninclusion/results_routeB.json")
    rows = rb["squeezed"]
    n_top = max(r["n_score"] for r in rows)
    quoted = {2: 3.44e-3, 4: 2.37e-3, 8: 2.17e-3}
    for K, q in quoted.items():
        best = max((r for r in rows if r["K"] == K and r["n_score"] == n_top),
                   key=lambda r: r["F"])
        check(f"C'3 K={K}", math.isclose(1 - best["F"], q, rel_tol=5e-3),
              f"note quotes {q}, artifact has {1-best['F']:.3e}")
        series = [max((r for r in rows if r["K"] == K and r["n_score"] == n),
                      key=lambda r: r["F"]) for n in sorted({r["n_score"] for r in rows})]
        vals = [1 - r["F"] for r in series]
        check(f"C'3 K={K} trend", vals == sorted(vals),
              f"series not increasing: {vals}")
    check("no cutoff-stable wording", "cutoff-stable" not in note.replace(
        '"cutoff-stable" is not used', ""), "banned phrase present")

    # --- exp23 (section 7.2): psi_trunc N_robust values and the per-config
    # lifted certification split, INCLUDING the prose claims in the JSON.
    rz = load("experiments/23_gkp_robust_zeros/robust_zero_results.json")
    by_delta = {c["envelope_width_Delta"]: c for c in rz["configurations"]}
    # note claims: N_robust = 12 / 8 / 4 at largest windows, eps=1e-4,
    # delta=0.18 pinned (Sol: max over delta let a dropped condition pass).
    for delta, want in [(0.2, 12), (0.3, 8), (0.4, 4)]:
        got = max(r["N_robust_bounded"] for r in by_delta[delta]["rows"]
                  if r["epsilon"] == 1e-4 and r["delta"] == 0.18)
        check(f"7.2 D2 Delta={delta}", got == want,
              f"note claims N_robust={want} at delta=0.18, artifact max={got}")
    # note claims: lifted certifies ideal comb for 0.3 (eps<=1e-4) and 0.4
    # (eps<=1e-3); 0.2 does not lift.
    def lifted_eps(delta: float) -> set[float]:
        return {r["epsilon"] for r in by_delta[delta]["rows"]
                if r.get("N_robust_lifted_bounded", 0) > 0 and r["delta"] == 0.18}
    check("7.2 D3 Delta=0.2", lifted_eps(0.2) == set(),
          f"note claims no lift, artifact lifts at {lifted_eps(0.2)}")
    check("7.2 D3 Delta=0.3", lifted_eps(0.3) == {1e-4},
          f"artifact lifts at {lifted_eps(0.3)}")
    check("7.2 D3 Delta=0.4", lifted_eps(0.4) == {1e-3, 1e-4},
          f"artifact lifts at {lifted_eps(0.4)}")
    # artifact-interpretation policy (issue #71, 2026-07-27): artifacts must
    # not carry conclusion prose at all; enforced here in addition to the
    # repo test suite.
    raw23 = json.dumps(rz)
    for banned in ("\"claim\"", "\"description\"", "\"interpretation\""):
        check(f"exp23 no-conclusion-prose {banned}", banned not in raw23,
              "conclusion-prose field present in artifact")

    # --- exp22 (section 7.1): labels and rank primitives still declared.
    up = load("experiments/22_kcurves/empirical_upper_bound.json")
    check("7.1 upper label", up["label"] == "family-constrained approximation curve",
          f"label is {up['label']!r}")
    check("7.1 upper rank_primitive", "rank_primitive" in up, "missing key")
    px = load("experiments/22_kcurves/data_proxy.json")
    check("7.1 proxy axis", all("R" in p for p in px["points"]),
          "proxy points no longer keyed by operator rank R")

    # --- self-application (management proposal, 2026-07-26): status prose and
    # internal references are claims too.
    for banned in ("pending", "TO WRITE", "TODO", "to be added"):
        check(f"stale-status phrase '{banned}'", banned not in note,
              "present in note body — rephrase or resolve")
    headings = set()
    for m in re.finditer(r"^#{2,3}\s+(?:Appendix\s+([A-Z])|(\d+(?:\.\d+)?))[.\s]",
                         note, re.M):
        headings.add(m.group(1) or m.group(2))
    for m in re.finditer(r"§(\d+(?:\.\d+)?)", note):
        ref = m.group(1)
        check(f"internal ref §{ref}",
              ref in headings or ref.split(".")[0] in headings,
              "no such heading")

    if FAILURES:
        print("CLAIM CHECK FAILED:")
        for f in FAILURES:
            print("  -", f)
        return 1
    print("coded claim checks pass (coverage: the checks above, not every number)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
