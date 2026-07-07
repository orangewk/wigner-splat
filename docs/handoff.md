# handoff - Next session work order

1. Read `README.md` (both falsification verdicts) and `docs/two-mode-plan.md`.
2. Setup: `pip install numpy matplotlib pytest`; `python -m pytest tests/ -q` → 40 passed, 1 xfailed
   (the xfail is a RECORDED negative result — separable splats cannot represent entanglement —
   do not "fix" it).
3. Main task: 3-mode extension — the decisive scaling point. Fock MLE needs a 12^3 = 1728-dim
   density matrix (R rho R becomes ~minutes-hours); full-covariance splats stay O(K) with
   6x6 Cholesky (21 cov params + 6 mu + 1 w = 28/splat). Extend states2 (three-mode cat
   |a,a,a> + parity |-a,-a,-a>, fringe cos(2 sqrt2 a (p1+p2+p3))), forward2f/fit2f
   (dimension-generic already in spirit — the overlap closed form is dimension-agnostic),
   mle3 only if tractable (it may simply time out: THAT is a result — record wall-clock).
4. Secondary tasks, either order:
   - More seeds at 2 modes to resolve the fidelity statistical tie (exp04: gap 0.003-0.006
     vs seed noise 0.015-0.018; ~20 seeds would decide).
   - Physical constraints (rho positivity) — the splat output is not guaranteed physical.
5. When quoting numbers: seed ranges, not single runs (issue #4).

## Where the program stands (2026-07-07)

Single mode (exp 03): splat wins fidelity, MLE wins speed 2x -> no computational gain at
one mode (recorded). Two modes (exp 04): ROLES FLIP — splat wins speed 6-11x (~4 s vs
27-45 s), fidelity statistical tie (0.921±0.011 vs 0.926±0.007), both at the same
finite-shot ceiling; falsification NOT triggered. The scaling hypothesis is confirmed in
direction; 3 modes makes it decisive.

Key scientific findings so far:
- Signed birth via the weight-gradient field (1D): split alone cannot create negativity.
- Entanglement <-> tilted covariance: separable (block-diagonal) splats fail at F=0.50
  (the fringe cos(2 sqrt2 a (p1+p2)) is constant along p1-p2 — needs ~80 axis-aligned
  splats vs ~10 tilted ones). Full 4x4 covariance is NOT an optimization, it is the
  representation of entanglement. Recorded as xfail with analysis in test_two_mode_fit.py.
- The MSE-histogram loss minimum caps fidelity at ~0.85 for separable splats but NOT for
  full covariance (hand-built F=0.99 mixture has lower loss than the blob solution).
- fit2f pipeline: blob envelope (variance-init, no true-state knowledge) -> convex
  matched-filter over a thin-stripe basis (fringe is LINEAR in stripe weights; one LS
  solve replaces unstable incremental births) -> Adam polish -> convex weight cleanup.
- MLE implementation traps (regression-tested): R operator orientation (transposed outer
  product silently stalls at F~0.35); probability conjugation (broke monotone ascent —
  the hardened stop condition caught it at iteration 11).

## Module map

states.py/states2.py (reference states) · forward.py/fit.py (1D splats, analytic grads,
adapt/birth) · forward2.py/fit2.py (separable 2-mode — kept as the recorded negative
result) · forward2f.py/fit2f.py (full-covariance 2-mode — the winner) · fock.py (validated
Fock tools + cat2) · mle.py/mle2.py (R rho R baselines) · data2.py (shared 2D binning) ·
experiments/01-04 (each README-linked) · docs/two-mode-plan.md (spec and fairness rules).
