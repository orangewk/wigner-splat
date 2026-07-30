# Experiment 25 — topological K–ε curves (issue #137, Gate M)

Measures the [issue #137](https://github.com/orangewk/wigner-splat/issues/137)
Gate M question: per cell (target, dictionary, K), the best-found `1 - F`
**and** the zero-link topology of the best state. Predictions PA–PE and
alarms were pre-declared in [`plan.md`](plan.md) and committed before any
output was interpreted. `topological_kcurves.json` is the authoritative
artifact; verdicts in it are computed from measured data, with census
failures propagating as indeterminate (`None`), never as passes. The numbers
below live in a block that `run.py` generates from that JSON, checked by
`tests/test_claim_surface_policy.py`.

## Result surfaces and epistemic status

Measured outcomes — the per-ladder curves, first-transition Ks, the
descriptive coincidence report including its tally, and the pre-declared
verdict values — live only in the generated block below and in the JSON;
this hand-written text intentionally repeats none of them
(one-authoring-location policy, checked mechanically by the policy tests).

The epistemic status of each pre-declared check is likewise not authored
here: `plan.md`'s claim table is its **sole** authoring location, and the
generated block quotes every check's basis and violation clause verbatim
from that table (mechanism added in review round 3, after a hand-restated
status drifted across surfaces in round 2). The cliff-vs-transition
comparison has no pre-declared criterion and is reported descriptively
only; whether to pre-register one is deferred to #137. Ladders whose
transition K sits above a census failure are excluded from the tally as
indeterminate — the generated line says so when it happens.

## Measured results (generated from the artifact)

<!-- generated-block: do not edit (written by run.py from topological_kcurves.json) -->
**|1,1>** — per-K best-found `1 - F` (linked pair flagged):

  | dictionary | K | 1 - F | linked pair |
  | --- | --- | --- | --- |
  | coherent | 1 | 8.647e-01 | no |
  | coherent | 2 | 6.321e-01 | no |
  | coherent | 3 | 4.080e-01 | no |
  | coherent | 4 | 1.600e-04 | yes |
  | gaussian | 1 | 7.500e-01 | no |
  | gaussian | 2 | 1.322e-04 | yes |
  | gaussian | 3 | 2.348e-05 | yes |
  | gaussian | 4 | 1.393e-05 | yes |

  - coherent: first linked pair at K = 4; the ladder's largest relative step lands at K = 4 (x2550.4), which coincides with the transition. Descriptive only — no cliff criterion was pre-declared.
  - gaussian: first linked pair at K = 2; the ladder's largest relative step lands at K = 2 (x5672.6), which coincides with the transition. Descriptive only — no cliff criterion was pre-declared.

**0.8|20>+0.6|03> (trefoil)** — per-K best-found `1 - F` ((3,2) winding flagged):

  | dictionary | K | 1 - F | (3,2) winding |
  | --- | --- | --- | --- |
  | coherent | 1 | 8.268e-01 | no |
  | coherent | 2 | 6.353e-01 | no |
  | coherent | 3 | 3.600e-01 | no |
  | coherent | 4 | 2.428e-01 | no |
  | coherent | 5 | 3.698e-03 | yes |
  | coherent | 6 | 9.601e-04 | yes |
  | gaussian | 1 | 7.560e-01 | no |
  | gaussian | 2 | 3.531e-01 | no |
  | gaussian | 3 | 6.041e-02 | yes |
  | gaussian | 4 | 8.314e-03 | yes |
  | gaussian | 5 | 4.782e-03 | yes |
  | gaussian | 6 | 3.255e-03 | yes |

  - coherent: first (3,2) winding at K = 5; the ladder's largest relative step lands at K = 5 (x65.7), which coincides with the transition. Descriptive only — no cliff criterion was pre-declared.
  - gaussian: first (3,2) winding at K = 3; the ladder's largest relative step lands at K = 4 (x7.3), which does NOT coincide with the transition. Descriptive only — no cliff criterion was pre-declared.

Tally (descriptive, no pre-declared criterion): transition and largest relative step coincide in 3 of 4 scored ladders; differing: trefoil/gaussian.

Pre-declared verdicts (computed; None = blocked by census failure):

- PA `|11>`/Gaussian/K=2 reaches the target with the Hopf link: **True**
- PB no coherent K<=2 linked pair: **True**
- PC Gaussian K=2 max |winding| <= 2: **True**
- PE trefoil/Gaussian/K=6 best-found fidelity: **0.9967**
- Cross-check vs exp24's closed-form machinery: max |dF| = 7.4e-05 (consistent: True)
- Census failures: none

Epistemic status — quoted verbatim from plan.md's claim table, its sole authoring location:

- PA — basis: "24/P4 proved (family contains `F = 1 - lam^4`)"; on violation: "optimizer defect, recorded; not a physics result"
- PB — basis: "24/P3 proved"; on violation: "tool/proof alarm; halt interpretation of that cell"
- PC — basis: "24/P6 sketch"; on violation: "recorded as evidence against the P6 sketch (interesting either way); no halt"
- PD — basis: "24/Q1"; on violation: "n/a"
- PE — basis: "24-memo construction, soft"; on violation: "optimizer budget noted, no alarm"
<!-- generated-block: end -->

## Scope limits

- All fidelities are **best-found** under a fixed multi-start Nelder–Mead
  budget (`fit_seed` in the JSON); nothing here is a certified supremum or
  lower bound, and the trefoil/Gaussian tail is still drifting at optimizer
  resolution.
- Core windings (including the `(3,2)` signature) are **frame-fixed**
  quantities read in the target's own coordinate frame — not passive
  invariants (see exp24 derivation P2, scope corrected in review). Target
  and approximant are always compared in that one common frame, which
  fidelity respects since both dictionaries are closed under passive
  transformations.
- The bounded dictionary is operational: quadratic operator norm < 0.98
  **and** truncated tail mass < 1e-8 at cutoff 36; the tail budget is the
  binding constraint (effective squeezing singular value near 0.56), in the
  same spirit as, but not equivalent to, the K_ε note's §2.2 dictionary.
- Censuses are numerically supported, not certified (exp24 README limits
  apply verbatim). Two-mode, pure states, unit sphere; no measured data.

## Reproduce (same-environment determinism)

```bash
python experiments/25_topological_kcurves/run.py
```

Seeds are fixed; a rerun in the recording environment (the JSON's
`environment` block) regenerates the artifacts — the figure-color rerun of
this experiment reproduced the JSON byte-identically. Cross-platform
bit-reproducibility is **not** claimed: best-found optima can differ across
BLAS/libm builds (see exp24 README). The census toolkit and its tests live
in `wigner_splat/stellar2.py` / `tests/test_stellar2.py`.
