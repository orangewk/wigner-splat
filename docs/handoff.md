# handoff - Next session work order

1. Read `README.md` (especially the falsification verdict) and `docs/prior-art-survey.md`.
2. Set up the environment: `pip install numpy matplotlib pytest`, then run `python -m pytest tests/ -q` and confirm 11 tests pass.
3. Main task: two-mode extension — the scaling hypothesis is now the ONLY remaining
   claim (see below). Extend forward.py to 4D phase space (two-mode splats, Radon
   projection along a chosen quadrature pair), states.py to a two-mode entangled cat
   (e.g. |a,a> + |-a,-a>), and compare against two-mode Fock MLE (n_max^2 dimension:
   400x400 density matrix at n_max=20). Acceptance: an experiments/04 run showing
   fidelity AND wall-clock for both methods; if splat loses both again, the README
   says we abandon the approach — do it.
4. Secondary: the splat fitter spends its time in a pure-Python loop over angles;
   before the two-mode comparison, vectorizing loss_and_grad over angles is fair game
   (MLE is already fully vectorized numpy).

## Done in previous sessions

- v0 scaffold: cat simulator, closed-form signed-splat Radon model, histogram fitter.
- Analytic gradients: loss_and_grad(), exp 01 ~29s -> ~1.6s, rel. L2 0.125.
  Overfits histogram shot noise past ~700 Adam iters; exp 01 stops at 680.
- Densification: adapt() (relative-median split thresholds; absolute ones fail near
  convergence) + signed BIRTH at the extremum of the weight-gradient field
  (birth_field(); split alone can never create negativity from an all-positive
  minimum). Exp 02: K=4 -> 9, rel. L2 0.071 vs 0.125 fixed-K=8.
- MLE baseline (this session): fock.py (truncated Fock tools, all conventions
  validated to 1e-12 against states.py closed forms) + mle.py (Lvovsky R rho R on
  the same binned histograms as the splat fitter). Exp 03 verdict, recorded in
  README: splat wins fidelity at every budget (0.980 vs 0.969 at 250 shots/angle
  — real shot-efficiency advantage), MLE wins speed ~2x at single-mode scale
  (n_max=20 matrices are tiny). Falsification condition NOT met -> single-mode
  brings no computational gain; the scaling claim must be tested at two modes.
  Implementation note: the R operator must be sum (f/p) |v><v| with |v>_i = <i|x_theta>
  — the transposed outer product is NOT the likelihood-ascent operator (it silently
  stalls at F ~ 0.35; there is a regression test).
