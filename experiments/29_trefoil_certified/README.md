# Experiment 29 — certified trefoil margins and the conic winding bound (issue #137 Gate T′ slice)

Pre-declaration, proofs, and falsification gates live in `derivation.md`
(committed before any implementation or run output existed). Its §8
claim table is the sole authoring location for epistemic status; this
README quotes it verbatim inside the generated block and restates
nothing by hand.

## What this experiment does

`derivation.md` proves certified (exact-enclosure-traceable) clearance
and transversality margins for the exp25 trefoil target, whose zero
link is a single `(3,2)`-winding curve disjoint from both coordinate
cores (W1), and proves the conic winding bound for `K <= 2`
pure-Gaussian superpositions (W4 — the statement of exp24's P6).
Together with exp28's stability theorem in metric-neighborhood form
(W0), these yield a certified fidelity gap for `D_G, K <= 2` at the
trefoil (W5). The run establishes the exact enclosures (E1), evaluates
the certified radius (E2), referees the certified margins one-sidedly
against grid estimates (E3), checks the census structure (E4), and
cross-checks exp25's measured cells (E5).

## Result surfaces and epistemic status

Evaluated numbers live only in `trefoil_certified.json`, written by
`run.py`; the block below is generated from that JSON by
`summary_block.py` and checked by `tests/test_claim_surface_policy.py`.
Referee tests live in `tests/test_trefoil_certified.py`.

## Reproduce

```
python experiments/29_trefoil_certified/run.py
python -m pytest tests/test_trefoil_certified.py tests/test_claim_surface_policy.py -q
```

Same-environment reproduction contract as exp24/25 (environment
recorded in the JSON).

## Results

<!-- generated-block: do not edit (written by run.py from trefoil_certified.json) -->
- E1 exact enclosures (fractions; slop 1e-09 on transcendental steps): `s*` in [179174773/209715200, 89587411/104857600], `theta*` in [1.024341, 1.024341]; band contains `theta*`: True; core-disjoint rho cap 0.5465.
- E2 certified radius: `eps29_cert` = 0.012724 at (rho, h) = (0.12, 0.3240) with margins (m, sigma) = (0.020978, 0.134361); certified fidelity bound (W5) = 0.999838.

  | rho | m_cert | sigma_cert |
  | --- | --- | --- |
  | 0.02 | 0.003496 | 0.738394 |
  | 0.04 | 0.006993 | 0.684549 |
  | 0.06 | 0.010489 | 0.615717 |
  | 0.08 | 0.013985 | 0.524764 |
  | 0.10 | 0.017482 | 0.394628 |
  | 0.12 | 0.020978 | 0.134361 |
  | 0.14 | 0.024475 | 0.000000 |
  | 0.16 | 0.027971 | 0.000000 |
  | 0.18 | 0.031467 | 0.000000 |
  | 0.20 | 0.034964 | 0.000000 |

- E3 one-sided referee vs grid margins (2105 polished zero points; certified values must sit at or below grid estimates): violations 0.
- E4 census structure: 1 component(s), |windings| sorted [2, 3], linking offdiag []; cloud theta deviation from the enclosure 0.00000.
- E5 `trefoil/gaussian/K=1`: measured best-found F = 0.244044 vs certified bound 0.999838 — within: True.
- E5 `trefoil/gaussian/K=2`: measured best-found F = 0.646909 vs certified bound 0.999838 — within: True.

Pre-declared verdicts (computed in run.py from the data):

- E1 exact enclosures established (F1 gate): **True**
- E2 certified radius positive (F2 gate): **True**
- E3 certified margins below grid margins (F3 gate): **True**
- E4 census matches the W1 structure (F4 gate): **True**
- E5 exp25 trefoil cells within the certified bound (F5 gate): **True**

Epistemic status — quoted verbatim from derivation.md §8, its sole authoring location:

- W0 — status: "proved here"; basis: "§2"
- W1 — status: "proved here"; basis: "§1"
- W2 — status: "proved here"; basis: "§3"
- W3 — status: "proved here"; basis: "§4"
- W4 — status: "proved here"; basis: "§5"
- W5 — status: "proved here (uses exp28 S3)"; basis: "§6"
- N1 — status: "numerical, E1"; basis: "run"
- N2 — status: "numerical, E2"; basis: "run"
- N3 — status: "numerical, E3"; basis: "run"
- N4 — status: "numerical, E4"; basis: "run"
- N5 — status: "numerical, E5"; basis: "run"
<!-- generated-block: end -->
