# Experiment 28 — link-type stability inside a fidelity ball (issue #137 Gate T′ sub-goal (a), slice 1)

Pre-declaration, claims, proofs, and falsification gates live in
`derivation.md` (committed before any implementation or run output
existed). Its §7 claim table is the sole authoring location for epistemic
status; this README quotes it verbatim inside the generated block and
restates nothing by hand.

## What this experiment does

`derivation.md` proves a quantitative stability theorem (S3): a state
close enough to a regular-zero-link target in phase-aligned norm distance
has an ambient-isotopic zero link on the census sphere, with the
admissibility conditions and margins defined there. For the `|1,1>`
target the margins have closed forms (S4), which makes the certified
radius `eps0_cert` exactly evaluable (E2) and one-side-refereeable on a
grid (E1). E3 probes tightness along pre-declared direction families,
E4 cross-checks the certified fidelity bound against exp25's measured
`|11>/D_coh/K=2` cell, and E5 records grid-only (not certified) margins
for the exp25 trefoil target.

## Result surfaces and epistemic status

Measured numbers live only in `isotopy_stability.json`, written by
`run.py`; the block below is generated from that JSON by
`summary_block.py` and checked by `tests/test_claim_surface_policy.py`.
Referee tests for the toolkit live in `tests/test_isotopy_stability.py`.

## Reproduce

```
python experiments/28_isotopy_stability/run.py
python -m pytest tests/test_isotopy_stability.py tests/test_claim_surface_policy.py -q
```

Same-environment reproduction contract as exp24/25 (environment recorded
in the JSON).

## Results

<!-- generated-block: do not edit (written by run.py from isotopy_stability.json) -->
<!-- generated-block: end -->
