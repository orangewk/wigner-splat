# Experiment 26 — Gaussian-group action on stellar zero links (issue #137, Gate T′ slice 1)

Measures whether the zero-link topology of experiments 24/25 survives the
**full** Gaussian unitary group or only passive linear optics — 指摘 2 of the
管理役 comment of 2026-07-31 on
[issue #137](https://github.com/orangewk/wigner-splat/issues/137).
Everything pre-declared lives in [`derivation.md`](derivation.md): the
propositions, the E-series grids/seeds/thresholds (§5), and the falsification
gates F1–F5 (§6), all committed before any run output was interpreted.

`gauss_invariance.json` is the authoritative artifact: every verdict in it is
computed from measured data, and census failures propagate as indeterminate
(`None`), never as passes. The numbers below live in a block that `run.py`
generates from that JSON, checked by `tests/test_claim_surface_policy.py`.

## Result surfaces and epistemic status

Measured outcomes — the E1 gate reading, the E2/E3 threshold cells, the E4
partition cells, the E5 large-radius comparisons, the E6 best-found values,
and every verdict — live only in the generated block below and in the JSON;
this hand-written text intentionally repeats none of them
(one-authoring-location policy, checked mechanically by the policy tests).

The epistemic status of each claim is likewise not authored here: the claim
table in `derivation.md` §4 is its **sole** authoring location, and the
generated block quotes every claim's basis and on-violation cell verbatim
from that table (same mechanism as experiment 25, added there in review).

## What runs (pointers only)

- **E1** machinery gate for the exact `(P, A, b)` transformer
  (`wigner_splat/gaussact.py`) — the F1 gate for everything downstream.
- **E2/E3** fixed-radius census scans of the squeezed `|1,1>` family against
  the pre-declared threshold and restoration cells of `derivation.md` §5.
- **E4** top-form partition of seeded Gaussian orbits of `|1,1>`, `|2,0>`,
  and the trefoil state `0.8|20> + 0.6|03>`.
- **E5** large-radius censuses of the first two orbit images per family,
  with a data-computed curve classifier for the `|2,0>` images.
- **E6** descriptive multi-start stress probe of Gaussian connectivity of
  `|2,0>` and `|1,1>`, over a magnitude-capped factorized family (no
  falsification gate — see derivation.md F5 as corrected in the Sol audit).

## Measured results (generated from the artifact)

<!-- generated-block: do not edit (written by run.py from gauss_invariance.json) -->
- E1 transformer gate (F1): **MATCH** (truncated-Fock brute force at cutoff 36, max rel diff on the low block — `|1,1>`: 4.55e-15, trefoil: 4.60e-15).
- E2 fixed-radius scan (squeeze2 of `|1,1>`, radius 1.0; prediction computed per cell from c(lam) vs rad^2/2):

  | lam | c(lam) | predicted | measured comps | linking | cell |
  | --- | --- | --- | --- | --- | --- |
  | 0.30 | 0.3297 | 2 comps, lk [1] | 2 | [1] | True |
  | 0.35 | 0.3989 | 2 comps, lk [1] | 2 | [1] | True |
  | 0.40 | 0.4762 | 2 comps, lk [1] | 2 | [1] | True |
  | 0.43 | 0.5275 | 0 comps, lk [] | 0 | [] | True |
  | 0.46 | 0.5835 | 0 comps, lk [] | 0 | [] | True |
  | 0.50 | 0.6667 | 0 comps, lk [] | 0 | [] | True |
  | 0.60 | 0.9375 | 0 comps, lk [] | 0 | [] | True |

- E3 radius 1.0392 (0.9 x rad*): predicted 0 comps, lk []; measured 0 comps, lk [] — True.
- E3 radius 1.3856 (1.2 x rad*): predicted 2 comps, lk [1]; measured 2 comps, lk [1] — True.
- E4 top-form partitions of seeded Gaussian orbits (clustering tol 0.001, indeterminate below margin 0.01):

  | state | partitions (8 seeds) | min margin | cells |
  | --- | --- | --- | --- |
  | t11 | (1,1) x8 | 9.887e-01 | True |
  | t20 | (2) x8 | inf | True |
  | trefoil | (3) x8 | inf | True |

- E5 large-radius censuses (radii 2.5 / 3.0; a cell is indeterminate unless both radii agree on components and linking):

  | state/seed | type | radii agree | comps 2.5/3.0 | lk 2.5/3.0 | sketch-consistent |
  | --- | --- | --- | --- | --- | --- |
  | t11/100 | - | True | 2 / 2 | [1] / [1] | True |
  | t11/101 | - | True | 2 / 2 | [1] / [1] | True |
  | t20/200 | parallel_lines | True | 2 / 2 | [0] / [0] | True |
  | t20/201 | parallel_lines | True | 2 / 2 | [0] / [0] | True |
  | trefoil/300 | - | True | 1 / 1 | [] / [] | True |
  | trefoil/301 | - | True | 1 / 1 | [] / [] | True |

- E6 descriptive stress probe over the magnitude-capped factorized family (cap 1.2, 32 NM starts per direction; best-found only — no gate attaches, and per derivation.md F5 the value can neither support nor refute G3): max F(G`|2,0>`, `|1,1>`) = 0.500000; max F(G`|1,1>`, `|2,0>`) = 0.500000.

Pre-declared verdicts (computed; INDETERMINATE = census failure or ambiguous clustering, never a pass):

- E1 transformer validated (F1 gate): **True**
- E2 fixed-radius cells match the G2 prediction: **True**
- E3 restoration cells match the G2 prediction: **True**
- E4 top-form partition unchanged across all orbit cells (G3): **True**
- E5 determinate cells all consistent with the G4-predicted patterns (F4: no halt either way): **True**
- E5 cell tally: consistent 6, inconsistent 0, indeterminate 0
- E6 best-found F (descriptive stress probe, capped family; no gate — F5 withdrawn in the PR #138 Sol audit): G`|2,0>` -> `|1,1>`: 0.500000; G`|1,1>` -> `|2,0>`: 0.500000
- Census failures: none

Epistemic status — quoted verbatim from derivation.md §4, its sole authoring location:

- G1 — basis: "proved here (§2.1)"; on violation: "tool alarm; halt all downstream cells"
- G2 — basis: "proved here (§2.2; uses 24/P1 and 24/P4b)"; on violation: "tool/proof alarm; halt E2/E3 interpretation"
- G3 — basis: "proved here (§2.3 with Lemma C; Lemma A proved in Appendix A; Lemma B proved on the finite-rank class in Appendix B and pinned in tests) — status upgraded in the PR #138 Sol audit"; on violation: "E4 mismatch: halt; diagnose the lemma chain before interpreting anything downstream of it"
- G4 — basis: "sketch (§2.4)"; on violation: "recorded as evidence against the sketch (interesting either way); no halt"
- G5 — basis: "corollary of G3"; on violation: "not experimentally testable here: E6 is a descriptive stress probe over a capped family and can neither support nor refute G3 (F5 gate removed in the PR #138 Sol audit)"
<!-- generated-block: end -->

## Scope limits

- E6 values are **best-found** under a fixed multi-start Nelder–Mead budget
  (`fit_seed` in the JSON) over a **magnitude-capped factorized family**
  (caps recorded in the JSON) — not the full non-compact Gaussian group.
  Nothing is a supremum, no upper bound on the group supremum is claimed,
  and per derivation.md F5 (corrected in the Sol audit) the E6 value can
  neither support nor refute G3.
- Censuses are numerically supported, not certified (exp24 README limits
  apply verbatim); grid and cap diagnostics are recorded per census in the
  JSON.
- Core windings are **frame-fixed** diagnostics (exp24 derivation P2 scope
  caveat applies verbatim); E5 records trefoil-image windings descriptively
  in that sense only.
- Two modes, pure states, no measured data; novelty is unclaimed pending the
  Gate S′ survey (`derivation.md` §7).

## Reproduce (same-environment determinism)

```bash
python experiments/26_gauss_invariance/run.py
python -m pytest tests/test_gaussact.py tests/test_claim_surface_policy.py -q
```

Seeds are fixed; a rerun in the recording environment (the JSON's
`environment` block) regenerates `gauss_invariance.json` byte-identically
(verified at authoring time). Cross-platform bit-reproducibility is **not**
claimed: best-found optima can differ across BLAS/libm builds (see the
exp24/25 READMEs). The transformer toolkit and its independent referees live
in `wigner_splat/gaussact.py` / `tests/test_gaussact.py`; censuses reuse
`wigner_splat/stellar2.py` unchanged. `gauss_links.png` shows four
stereographic panels of measured links, titled from census data.
