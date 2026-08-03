# Experiment 30 — dictionary alignment: two-mode tiers and certified-gap transfer (issue #137 Gate T′ sub-goal (c))

Pre-declaration, proofs, and falsification gates live in `derivation.md`
(committed before any implementation or run output existed). Its §9
claim table is the sole authoring location for epistemic status; this
README quotes it verbatim inside the generated block and restates
nothing by hand.

## What this experiment does

The subject is the alignment between the repo's two-mode dictionaries
(exp24 §1, exp25's operational bounded family) and the K_ε note's
restricted bounded common-squeezing dictionary (note §2.2, rows D1–D2).
What is claimed, and with what status, lives **only** in
`derivation.md` §9's claim table (rows A0–A5 for the derivation, N1–N4
for the run) — this README does not restate any of it. Structurally:
the memo defines the two-mode tier ladder, proves the Gaussian stellar
normal form with its physical translation, transfers the repo's
certified fidelity gaps down the ladder, proves the common-quadratic
division dichotomy, and fixes exact ε-convention conversions; the run
referees the normal form on seeded Gaussian-unitary chains (E1), the
norm closed form (E2), the committed exp25 cells' membership and
re-derivation with the descended bounds (E3), and the exact conversion
identities with the note-convention thresholds (E4), with blocking
falsification gates as declared in the memo §8.

## Result surfaces and epistemic status

Evaluated numbers live only in `dictionary_alignment.json`, written by
`run.py`; the block below is generated from that JSON by
`summary_block.py` and checked by `tests/test_claim_surface_policy.py`.
Referee tests live in `tests/test_dictionary_alignment.py`.

## Reproduce

```
python experiments/30_dictionary_alignment/run.py
python -m pytest tests/test_dictionary_alignment.py tests/test_claim_surface_policy.py -q
```

Same-environment reproduction contract as exp24/25/28/29 (environment
recorded in the JSON).

## Results

<!-- generated-block: do not edit (written by run.py from dictionary_alignment.json) -->
- E1 normal-form referee (64 seeded Gaussian-unitary chains vs the A1 recipe): polynomial part stayed degree 0 on all; max ||A|| = 0.880554 < 1; max phase-aligned Fock mismatch (upper display) 0.000000000001; max b-map residual 0.000000000001; sandwich violations 0.
- E2 norm closed form vs bracketed partial sums (36 sigma pairs, cutoff 80): bracket failures 0; max relative bracket width (upper display) 0.00950795.
- E3 committed exp25 cells (10 rebuilt from `best_params`): max fidelity re-derivation gap (upper display) 0.00000001; max atom ||A|| 0.7072 <= committed box 0.98: True; descended-bound violations 0 (verdict from raw values). Diagnostic only (no bound claimed, A3 contrast): `t11/gaussian/K=2` measured F = 0.999868.
- E4 exact conversions: identity failures 0 on the declared grid; committed-bound outwardness re-verified: True. Note-convention thresholds (rounded DOWN; 'for all eps below'): trefoil/K<=2 eps < 0.000071 (from exp29's radius, fidelity bound 0.999929 rounded up); |11>/coherent and common-quadratic K<=2 eps < 0.012055 (from exp28's radius, fidelity bound 0.987945 rounded up).

Pre-declared verdicts (computed in run.py from the data):

- E1 normal-form referee passes (F1 gate): **True**
- E2 norm bracket holds (F2 gate): **True**
- E3 membership + re-derivation + descended bounds (F3 gate): **True**
- E4 exact conversions verified (F4 gate): **True**

Epistemic status — quoted verbatim from derivation.md §9, its sole authoring location:

- A0 — status: "proved here"; basis: "§2"
- A1 — status: "proved here"; basis: "§3"
- A2 — status: "proved here (uses exp29 W5, exp28 S3–S5)"; basis: "§4"
- A3 — status: "proved here (uses exp24 P3–P4, exp28 S3–S5)"; basis: "§4"
- A4 — status: "proved here"; basis: "§5"
- A5 — status: "proved here"; basis: "§6"
- N1 — status: "numerical, E1"; basis: "run"
- N2 — status: "numerical, E2"; basis: "run"
- N3 — status: "numerical, E3"; basis: "run"
- N4 — status: "numerical, E4"; basis: "run"
<!-- generated-block: end -->
