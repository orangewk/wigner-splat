# Experiment 24 — stellar zero links on the phase-space 3-sphere

Exploratory side-track (no issue; conversational approval by orange,
2026-07-30). Two-mode extension of the K_ε note's zero-counting idea: in two
modes the stellar function's zeros meet the sphere
`|w1|^2 + |w2|^2 = 1` in a **link**, and the link type — component count, core
windings, pairwise linking numbers — is invariant under passive linear optics
and can separate Gaussian dictionaries at fixed term budget `K`. The
propositions and all predictions were pre-declared in
[`derivation.md`](derivation.md) **before** the run; `|1,1>`'s zero link is
literally two fibers of the Hopf fibration (derivation P1), which is where
this side-track started.

`hopf_link_results.json` is the authoritative artifact: every verdict in it is
computed by comparing measured census data against the encoded prediction
(never a hard-coded string), and the numbers quoted below are citations of
that file.

## What ran (all four sections passed their pre-declared checks)

- **E1 tracker validation.** `|1,1>` (two frame seeds), `|10>+|01>`,
  `|20>+|02>` reproduce the proved links exactly — for `|1,1>`: two
  components, windings `(1, ·)`/`(·, 1)`, linking `+1`. Verdict
  `e1_tracker_validated: true` (this is the F1 gate; a failure here would
  have halted interpretation).
- **E2 knot ladder.** `|30>+|03>`: three mutually `+1`-linked circles.
  `0.8|20>+0.6|03>`: a single component with winding pair `(3, 2)` — the
  trefoil signature that P6 argues is out of reach for Gaussian `K=2`.
- **E3 dictionary probes.** TMSV odd cats at `lam = 0.3 / 0.6 / 0.9` carry
  the **exact** Hopf link at every squeezing (P4) with fidelity to `|1,1>`
  equal to `1 - lam^4` (closed form and independent Fock series agree to
  1e-10, recorded per lam). The generic-phase TMSV cat's smooth conic pair
  shows windings `(+1,-1)/(-1,+1)` and linking `+1` exactly as P4b proves.
  The `cat (x) cat` state at `t = 3.5` shows six components whose full
  linking pattern matches the in-code geometric prediction
  (satellite-line intersection points inside/outside the ball).
- **E4 coherent fit ladder (numeric; best-found, not certified suprema).**
  Best multi-start Nelder–Mead fidelity to `|1,1>` over `K` coherent terms:

  | K | best fidelity | 1 - F | zero components | linked pair |
  | --- | --- | --- | --- | --- |
  | 1 | 0.135335 | 8.6e-1 | 0 | – |
  | 2 | 0.367879 | 6.3e-1 | 1 | no (P3 proves impossible) |
  | 3 | 0.592011 | 4.1e-1 | 1 | no (Q1: open cell, measured) |
  | 4 | 0.999766 | 2.3e-4 | 2 | **yes — the Hopf link appears** |

  The three-orders-of-magnitude fidelity jump coincides with the appearance
  of the linked pair. Observation (not preregistered, conjecture only): the
  K=1 and K=2 values agree with `e^-2` and `e^-1` to the shown digits.

## Scope limits

- The census is **numerically supported, not certified**: zero curves thinner
  than the grid are invisible, and completeness near the two excluded
  coordinate-core caps rests on a `|f|` floor heuristic recorded in the
  diagnostics. The linking integers themselves are exact crossing counts with
  consistency checks, given the traced curves.
- E4 fidelities are best-found under a fixed optimizer budget
  (`fit_seed = 20260730`); K=3 especially is an upper-bound-free numeric
  observation, and derivation P5/P6 remain sketches — no certified
  lower-bound language applies anywhere in this experiment.
- Everything is two-mode, pure-state, unit-sphere; no measured data, no mixed
  states, no connection to the note's certified one-mode theorems is claimed,
  and novelty is unclaimed pending the derivation §7 survey.

## Reproduce deterministically

```bash
python experiments/24_hopf_stellar/run.py
python -m pytest tests/test_stellar2.py -q
```

The toolkit lives in `wigner_splat/stellar2.py`; its proved-prediction tests
(`tests/test_stellar2.py`) pin the linking sign convention (standard Hopf
pair = +1) and re-derive every E1/E3 exact expectation independently of this
experiment's artifacts.

`stellar_links_s3.png` shows stereographic projections of six of the measured
links (the trefoil is visibly a trefoil); `coherent_fit_ladder.png` shows the
E4 table as a curve.
