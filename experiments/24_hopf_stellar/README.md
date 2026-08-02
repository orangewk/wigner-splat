# Experiment 24 — stellar zero links on the phase-space 3-sphere

Exploratory side-track (no issue; conversational approval by orange,
2026-07-30; continued as issue #137). Two-mode extension of the K_ε note's
zero-counting idea: in two modes the stellar function's zeros meet the sphere
`|w1|^2 + |w2|^2 = 1` in a **link**. Component count and the pairwise linking
matrix are invariant under passive linear optics; per-component core windings
are **frame-fixed** diagnostics (defined against the state's own coordinate
cores, not passive invariants — see derivation P2, scope corrected during
PR #136 review). `|1,1>`'s zero link is literally two fibers of the Hopf
fibration (derivation P1), which is where this side-track started.

The propositions and all predictions were pre-declared in
[`derivation.md`](derivation.md) **before** the run.
`hopf_link_results.json` is the authoritative artifact: every verdict in it
is computed by comparing measured census data against the encoded prediction
(never a hard-coded string). The numbers below live in a block that `run.py`
generates from that JSON — the policy test
`tests/test_claim_surface_policy.py` fails if the block and the artifact
diverge.

## What ran

- **E1 tracker validation** (`|1,1>` under two census frame seeds,
  `|10>+|01>`, `|20>+|02>`) against the proved links; this is the F1 gate —
  on any mismatch the run halts before later sections are generated, and the
  same halt applies to E2 and E3.
- **E2 knot ladder**: `|30>+|03>` (three mutually linked circles) and
  `0.8|20>+0.6|03>` (the trefoil winding pair from derivation P6).
- **E3 dictionary probes**: TMSV odd cats (exact Hopf link at every
  squeezing, P4, with the closed-form fidelity checked against an
  independent Fock series), the smooth conic pair of a generic-phase TMSV
  cat (P4b signs), and a `cat (x) cat` state whose satellite-circle linking
  pattern is predicted geometrically in code.
- **E4 coherent fit ladder**: best multi-start Nelder–Mead fidelity to
  `|1,1>` over `K` coherent terms, with a zero census of each best state.

## Measured results (generated from the artifact)

<!-- generated-block: do not edit (written by run.py from hopf_link_results.json) -->
- E1 tracker validation against the proved links: **MATCH**.
- E2 knot ladder (three-chain linking, trefoil winding pair): **MATCH**.
- E3 dictionary probes: **MATCH** (TMSV odd-cat fidelities lam=0.3: F = 0.9919, lam=0.6: F = 0.8704, lam=0.9: F = 0.3439; closed form and Fock series agree per the recorded booleans).
- E4 coherent fit ladder (best-found, not certified suprema):

  | K | best fidelity | 1 - F | zero components | linked pair |
  | --- | --- | --- | --- | --- |
  | 1 | 0.135335 | 8.6e-01 | 0 | no |
  | 2 | 0.367879 | 6.3e-01 | 1 | no |
  | 3 | 0.592011 | 4.1e-01 | 1 | no |
  | 4 | 0.999766 | 2.3e-04 | 2 | yes |

  Observation (conjecture only): the K=1 / K=2 values sit within 2.5e-13 / 4.4e-12 of e^-2 / e^-1.
  Descriptive (no pre-declared criterion): first linked pair at K = 4; largest relative step lands at K = 4; the transition coincides with it.
<!-- generated-block: end -->

Interpretation beyond the block is deferred to the artifact: the block
carries the E1–E3 verdicts and a descriptive, criterion-free comparison of
the E4 ladder's first linked pair against its largest fidelity step; this
hand-written text intentionally repeats none of those outcomes.

## Scope limits

- The census is **numerically supported, not certified**: zero curves thinner
  than the grid are invisible, and completeness near the two excluded
  coordinate-core caps rests on a `|f|` floor heuristic recorded in the
  diagnostics. The linking integers themselves are exact crossing counts with
  consistency checks, given the traced curves.
- E4 fidelities are best-found under a fixed optimizer budget; the epistemic
  status of every derivation claim lives only in derivation.md §4's claim
  table — no certified-lower-bound language applies to this experiment's own
  census and E4 numbers.
- Two-mode, pure states, unit sphere; no measured data, no mixed states, no
  connection to the note's certified one-mode theorems is claimed, and
  novelty is unclaimed pending the derivation §7 survey (issue #137 Gate S′).

## Reproduce (same-environment determinism)

```bash
python experiments/24_hopf_stellar/run.py
python -m pytest tests/test_stellar2.py -q
```

Seeds are fixed and a rerun in the recording environment (see the
`environment` block in the JSON) regenerates the artifacts. **Cross-platform
bit-reproducibility is not claimed**: E1–E3 census topology is
integer-valued and has been stable across environments, but E4 multi-start
optimization can settle in different local optima under different
BLAS/libm builds (observed during PR #136 review on Windows), moving
best-found values at the third decimal and the satellite details of the
best state's census. That variation is within the "best-found, not
suprema" scope above. The runner pins its console stream to UTF-8, so
code-page consoles (e.g. CP932) no longer abort on the log's typography.

The toolkit lives in `wigner_splat/stellar2.py`; its proved-prediction tests
(`tests/test_stellar2.py`) pin the linking sign convention (standard Hopf
pair = +1) and re-derive every E1/E3 exact expectation independently of this
experiment's artifacts. `stellar_links_s3.png` shows stereographic
projections of six of the measured links; `coherent_fit_ladder.png` shows
the E4 ladder.
