# handoff - Next session work order

1. Read `README.md` and `docs/prior-art-survey.md` to recover context.
2. Set up the environment: `pip install numpy matplotlib pytest`, then run `python -m pytest tests/ -q` and confirm 8 tests pass.
3. Main task: iterative MLE baseline for the falsification test in `README.md`.
   Implement Lvovsky-style iterative MLE (R rho R algorithm) in a Fock basis truncated
   at n_max ~ 20, on the same binned homodyne data, and compare against the splat fitter
   on: fidelity to the true cat state, shot-number efficiency, and wall-clock time.
   Acceptance: an `experiments/03_mle_baseline/run.py` that prints a side-by-side table
   for at least 2 shot budgets. Record the outcome honestly either way — losing the
   comparison triggers the falsification condition in the README.
4. Next task: physical constraints (positive semidefinite density operator) — penalty vs
   Kenfack-type closed-form constraints.

## Done in previous sessions

- v0 scaffold: cat-state simulator, closed-form signed-splat Radon forward model,
  histogram-loss fitter with Adam, experiment 01 recovering negativity (rel. L2 13%).
- Analytic gradients: `loss_and_grad()` (closed-form chain rule), verified against
  central differences. Experiment 01: ~29s -> ~1.6s, rel. L2 0.125. Note: past ~700
  Adam iterations the fit overfits histogram shot noise; exp 01 stops at 680.
- Densification/pruning (this session): `adapt()` prunes |w| < threshold and splits
  splats whose accumulated positional-gradient norm exceeds split_rel * median
  (absolute 3DGS-style thresholds fail near convergence; relative ones keep working).
  KEY FINDING: split/clone alone cannot create negativity — from an all-positive K=4
  local minimum, two positive children never make a negative fringe (2/3 seeds failed,
  L2 ~ 1.0). Fixed by signed BIRTH: the weight gradient dL/dw(mu) of a hypothetical
  splat at mu is the residual back-projected through the splat kernel (closed form,
  `birth_field()`); a splat born at its extremum with the descent sign seeds negative
  structure. Experiment 02: K=4 -> 9 (2 negative weights), rel. L2 0.071 vs 0.125 for
  fixed K=8, negativity -0.191 vs true -0.190, all 5 test seeds in [0.05, 0.09].
