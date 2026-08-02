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
- E2 certified radius (grid per JSON `declared`): `eps0_cert(|11>)` = 0.109964 at (rho, h) = (0.1859, 0.6185); certified fidelity bound (S5 runnable form) = 0.987944.
- E1 one-sided referee (481 thetas x 4^2 phases, tol 1e-09): clearance violations 0, sigma violations 0; min clearance excess over the closed form 0.001 (refinement diagnostic, not an alarm).
- E3 first-change probe (ascending lattice per JSON `declared`; first census change per direction, bisected in the bracketing interval; census signature = isotopy-invariant content only, components + |linking|):

  | family | directions | broke | min delta_break | min ratio to eps0_cert | census failures |
  | --- | --- | --- | --- | --- | --- |
  | kernel | 8 | 8 | 0.2000 | 1.82 | 0 |
  | random | 24 | 24 | 0.2381 | 2.17 | 0 |
  | exp25_endpoint | 1 | 1 | 0.7444 | 6.77 | 0 |

  Overall min delta_break: 0.2000 (best-found upper bounds within the probed families; no minimality claim).
- E4 exp25 consistency: measured best-found F of `t11/coherent/K=2` = 0.367879 vs certified bound 0.987944.
- E5 trefoil grid margins (2105 polished zero points; grid minima over-estimate true margins, so these are numerically supported only, NOT certified):

  | rho | m_grid | sigma_grid |
  | --- | --- | --- |
  | 0.05 | 0.0480 | 0.7548 |
  | 0.10 | 0.0853 | 0.7090 |
  | 0.15 | 0.1163 | 0.6535 |
  | 0.20 | 0.1426 | 0.5890 |
  | 0.25 | 0.1724 | 0.5163 |
  | 0.30 | 0.1919 | 0.4365 |
  | 0.35 | 0.2104 | 0.3657 |
  | 0.40 | 0.2264 | 0.2834 |
  | 0.45 | 0.2376 | 0.1877 |
  | 0.50 | 0.2435 | 0.1079 |

  Induced eps0-style grid estimate (not certified): 0.070518 at (rho, h) = (0.15, 0.4181).

Pre-declared verdicts (computed in run.py from the data):

- E2 certified radius positive (F2 gate): **True**
- E1 no grid sample below a proved bound (F1 gate): **True**
- E3 reference census is the Hopf link: **True**
- E3 no census change below eps0_cert (F3 gate): **True**
- E4 exp25 measured cell within the certified bound (F4 gate): **True**
- E5 trefoil margins recorded: **True**

Epistemic status — quoted verbatim from derivation.md §7, its sole authoring location:

- S1 — status: "proved here"; basis: "§2"
- S2 — status: "proved here"; basis: "§2"
- S3 — status: "proved here"; basis: "§3"
- S4 — status: "proved here"; basis: "§4"
- S5 — status: "proved here (uses exp24 P3)"; basis: "§5"
- N1 — status: "numerical, E1"; basis: "run"
- N2 — status: "numerical, E2"; basis: "run"
- N3 — status: "numerical, E3"; basis: "run"
- N4 — status: "numerical, E4"; basis: "run"
- N5 — status: "numerical, E5"; basis: "run"
<!-- generated-block: end -->
