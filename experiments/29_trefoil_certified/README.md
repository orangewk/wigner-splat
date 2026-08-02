# Experiment 29 — certified trefoil margins and the conic winding bound (issue #137 Gate T′ slice)

Pre-declaration, proofs, and falsification gates live in `derivation.md`
(committed before any implementation or run output existed). Its §8
claim table is the sole authoring location for epistemic status; this
README quotes it verbatim inside the generated block and restates
nothing by hand.

## What this experiment does

The subject is the exp25 trefoil target and the `K <= 2` pure-Gaussian
dictionary. What is claimed, and with what status, lives **only** in
`derivation.md` §8's claim table (rows W0–W5 for the derivation, N1–N5
for the run) — this README does not restate any of it. Structurally:
the memo derives margin formulas traced to exact rational enclosures
and a winding bound for the dictionary side, and the run establishes
the enclosures (E1), evaluates the certified radius (E2), referees the
margins on sound sample families (E3), checks the census structure
(E4), and cross-checks exp25's measured cells (E5), with blocking
falsification gates as declared in the memo §7.

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
- E1 exact enclosures (fractions; slop 1e-09 on transcendental steps): `s*` in [179174773/209715200, 89587411/104857600], `theta*` in [1.0243409, 1.0243415] (outward display); band contains `theta*`: True; core-disjoint rho cap 0.5464.
- E2 certified radius (lower bounds displayed rounded down): `eps29_cert` = 0.008482 at (rho, h) = (0.08, 0.0541) with margins (m, sigma) = (0.013985, 0.406288); certified fidelity bound (W5, upper bound displayed rounded up) = 0.999929.

  | rho | m_cert | sigma_cert |
  | --- | --- | --- |
  | 0.02 | 0.003496 | 0.731756 |
  | 0.04 | 0.006992 | 0.662826 |
  | 0.06 | 0.010489 | 0.563530 |
  | 0.08 | 0.013985 | 0.406288 |
  | 0.10 | 0.017481 | 0.000000 |
  | 0.12 | 0.020978 | 0.000000 |
  | 0.14 | 0.024474 | 0.000000 |
  | 0.16 | 0.027970 | 0.000000 |
  | 0.18 | 0.031467 | 0.000000 |
  | 0.20 | 0.034963 | 0.000000 |

- E3 sound margin referees (2105 polished zero points; clearance on the theta-certain complement, transversality on cloud-inside — membership backed by the §3 cloud-error certificate from the committed cloud's outward max residual 0.00000000000010, giving 0.000000001001 <= declared slack — and phase-normal probe families): violations 0. Cloud-complement grid margins are recorded as a heuristic diagnostic only.
- E4 census structure: 1 component(s), |windings| sorted [2, 3], linking offdiag []; cloud (declared loop-point stand-in) theta deviation from the enclosure 0.00000, min core distance 0.5464 >= gated threshold (floor - tol) 0.5365 (verdict from raw values).
- E5 `trefoil/gaussian/K=1`: measured best-found F = 0.244045 (displayed rounded up) vs certified bound 0.999929 — within: True (verdict from raw values).
- E5 `trefoil/gaussian/K=2`: measured best-found F = 0.646910 (displayed rounded up) vs certified bound 0.999929 — within: True (verdict from raw values).

Pre-declared verdicts (computed in run.py from the data):

- E1 exact enclosures established (F1 gate): **True**
- E2 certified radius positive (F2 gate): **True**
- E3 sound margin referees pass (F3 gate): **True**
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
