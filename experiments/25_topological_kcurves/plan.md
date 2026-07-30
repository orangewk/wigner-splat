# Experiment 25 — topological K–ε curves (issue #137, Gate M): pre-declaration

Written and committed before interpreting any run output. Builds on the
proved/sketched propositions of `experiments/24_hopf_stellar/derivation.md`
(P1–P6, R1, Q1); measured numbers live only in `topological_kcurves.json`.

## Question

For each cell (target, dictionary, K), how close can a K-term superposition
get to the target (best-found `1 - F`), and what is the zero-link topology of
the best state found? The claim candidate this measures — not proves — is
that **topology transitions in the census coincide with the jumps of the
K–ε curve**, i.e. the expensive part of the approximation is topological.

## Cells

- Targets (unit-normalized Fock superpositions):
  - `|11>` — zero link = positive Hopf link (24/P1).
  - `trefoil` = `0.8|20> + 0.6|03>` — single zero component of winding
    `(3, 2)` (24/P6 family).
- Dictionaries (stellar-exponent classes of `wigner_splat/stellar2.py`
  Gaussian-sum terms):
  - `D_coh`: affine-linear exponents (two-mode coherent terms).
  - `D_G^b`: full affine-quadratic exponents — displaced/squeezed including
    cross-mode squeezing. Boundedness is enforced operationally: quadratic
    operator norm < 0.98 and truncated Fock tail mass < 1e-8 at cutoff 36,
    else the parameter point is rejected. This parallels the K_ε note's
    bounded-dictionary discipline; no equivalence with its one-mode
    common-squeezing dictionary is claimed.
- `K = 1..4` for `|11>`, `K = 1..6` for the trefoil.

## Method

Per term, Fock coefficients by the Taylor recursion
(`gaussian_term_fock_coeffs`, tested against three closed forms); per cell,
the best superposition coefficients are the exact Gram solution (pseudo-
inverse) in the truncated space, and the nonlinear parameters run seeded
multi-start Nelder–Mead (structured seeds: TMSV cats for `|11>`/`D_G^b`, the
explicit 6-term squeezed construction for the trefoil, coherent grids;
greedy warm starts from the `K-1` cell; fixed `fit_seed`). The best state of
every cell gets a zero census with the exp24 toolkit and grid.

## Pre-declared predictions and alarms

| ID | Statement | Basis | On violation |
| --- | --- | --- | --- |
| PA | `|11>` / `D_G^b` / `K=2` reaches `F >= 0.999` and its census is the Hopf link | 24/P4 proved (family contains `F = 1 - lam^4`) | optimizer defect, recorded; not a physics result |
| PB | every `D_coh` `K<=2` census has no linked pair | 24/P3 proved | tool/proof alarm; halt interpretation of that cell |
| PC | every `D_G^b` `K=2` census has max abs winding `<= 2`; in particular the trefoil cell has no `(3,2)` component | 24/P6 sketch | recorded as evidence against the P6 sketch (interesting either way); no halt |
| PD | trefoil curves for both dictionaries at `K>=3`, and `|11>`/`D_coh`/`K=3`: open cells, measured only | 24/Q1 | n/a |
| PE | trefoil / `D_G^b` / `K=6` should sit near `F ~ 1` (explicit construction exists) | 24-memo construction, soft | optimizer budget noted, no alarm |

Epistemic status: all fidelities are best-found under a fixed optimizer
budget, never suprema; censuses are numerically supported (grid and cap
limits recorded in diagnostics); no certified-lower-bound language anywhere.
Verdict booleans are computed from data in `run.py`.
