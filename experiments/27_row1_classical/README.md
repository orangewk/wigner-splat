# Experiment 27 — issue #126 closure

This page is the canonical scientific-status surface for experiment 27 as of
2026-09-03.  The decision owner is orange; the implementation and run files are
historical evidence, not acceptance surfaces.  In particular,
[`RUN_REPORT.md`](RUN_REPORT.md) records machine execution and internal gates,
and the recovery wording in PR #171 does not override the decisions below.

## Closure table

The table is the sole authoring location for the current dispositions.  Scope
qualifiers stay in their row rather than being summarized elsewhere.

| ID | Object | Evidence | Disposition | Scope qualifier |
| --- | --- | --- | --- | --- |
| E27-D0 | Issue #126 / row 1 programme | [orange-authorized 2026-09-03 routing record](https://github.com/orangewk/wigner-splat/issues/126#issuecomment-5521760656) | **decision: close as an incomplete pilot when this reviewed packet merges** | Until that merge, the GitHub issue remains open. Closing it records the end of this attempt; it is not acceptance or completion of the proposed programme. |
| E27-P1 | PR #171 statement that the run met its completion conditions | [PR #171](https://github.com/orangewk/wigner-splat/pull/171) and the [2026-08-01 audit](../../docs/2026-08-01-sebastian-drift-audit--done.md) F1 | **superseded as a scientific-acceptance statement** | PR #171 remains the provenance record for recovering the historical files; its execution summary is not an acceptance decision. |
| E27-E1 | System A execution | [`results.json`](results.json), [`pytest_results.json`](pytest_results.json), and [`RUN_REPORT.md`](RUN_REPORT.md) | **recorded as reproducible execution evidence** | The committed run covers A1–A3 and the parabolic gate only. |
| E27-V1 | Quantum-path validation | [`results.json`](results.json) `parabolic_gate` and `A1.parameters.quantum_method`; [2026-08-01 audit](../../docs/2026-08-01-sebastian-drift-audit--done.md) F1 | **WKB implementation-consistency evidence only** | The gate and A1 share `radial_uniform_WKB_logistic_connection`; no independent quantum solver validates A1 on the screened-Coulomb target. |
| E27-R1 | Reported `R_obs` values | [`results.json`](results.json) `A1.points` | **not accepted as a research claim** | The values depend on the unvalidated A1 WKB route; numerical convergence and an exact-parabola self-check do not supply the missing solver independence. |
| E27-K1 | “Nature pays `K > 1`” for this row | [`BRIEF.md`](BRIEF.md) scope and [`results.json`](results.json) `scope_flags` | **not demonstrated** | Systems B and C and the Wigner/rank/witness outputs were not run; the rate layer alone is not a state certificate. |
| E27-N1 | Negative result for the row-1 hypothesis | E27-R1 and E27-K1 | **not obtained** | The hypothesis was not tested by an accepted independent quantum route, so this closure is incompleteness rather than a negative scientific result. |

## Reopening contract

Any renewed attempt starts in a new issue.  Before reading a replacement
`R_obs`, it must pre-register a quantum route that shares no action-integral or
logistic-connection call target with the A1 radial-WKB route.  The record must
pin each route's entry point, transitive call target, and code digest; a
canonical input digest must bind both routes and the classical calculation to
the same physical target and initial ensemble.  A reviewer independent of the
implementation must inspect those identities and the numerical comparison at
an exact SHA before `R_obs` can be considered for acceptance.  This is a
provenance test of computational independence, not another method-name string
comparison (see [audit §8, item 4](../../docs/2026-08-01-sebastian-drift-audit--done.md)).

The files in this directory remain historical evidence for this attempt rather
than being silently promoted into that new attempt.
