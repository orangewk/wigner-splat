# handoff - Next session work order

1. Read `README.md` (all three falsification verdicts — the scaling ladder is the story),
   `docs/research-log.md`, `docs/three-mode-plan.md`.
2. Setup: `pip install numpy matplotlib pytest`; `python -m pytest tests/ -q -m "not slow"`
   (~51 passed expected; full suite adds slow integration runs incl. a 15-min MLE budget test).
3. FIRST TASK — collect experiment 06: at handoff time `experiments/06_three_mode/run.py`
   was executing in the background (a ~20-min official run: fit3f x 3 seeds + one 900 s
   512-dim MLE run + verdict figure). Check `experiments/06_three_mode/` for out_run.log /
   out/three_mode_verdict.png. If it completed: verify the printed verdict matches the README
   numbers, commit the artifacts, post the closing comment on issue #7 (table + scaling
   ladder + DNF analysis), and update the PR #5 body to cover the whole campaign (its
   current body stops at the two-mode verdict). If it did not complete, rerun it (~20 min).
4. Then, in order of value:
   - Issue #8 (positivity): the splat output is not a guaranteed physical state — now the
     main obstacle to paper-grade claims. Kenfack-type closed-form constraints vs penalty
     vs post-hoc projection onto the physical cone (in the truncated Fock basis, using the
     validated splat->rho path implicit in the fidelity formulas).
   - Issue #6 (entanglement-cost conjecture, refuted->refined): formalize R ~ m_1D(k) ~ k;
     a short note/preprint section is plausible.
   - Detector noise (efficiency eta, Gaussian dark noise) — one Gaussian convolution in the
     forward model, keeps closed forms; needed for any experimental-data claim.
   - 4 modes if a dramatic demo is wanted: MLE is fully DNF there; splat should stay ~30 s.

## Where the program stands (2026-07-07, end of session)

Scaling ladder, measured: 1 mode — MLE wins speed 2x (no gain). 2 modes — fidelity tie
(20-seed paired t, p=0.121), splat 7.4x faster. 3 modes — splat wins BOTH: F 0.756 vs
0.701-DNF, ~15 s vs 900+ s (MLE 512 dims, 0.72 s/iter, loglik plateaus while fidelity
creeps — 17.7k rows vs 262k params underdetermined; 2+ h extrapolated). Conclusion in
README: at >= 3 modes splat is practically the only full-tomography option.

Open PR #5 carries the whole two- and three-mode campaign (draft). Issues: #6 conjecture
(refuted->refined, exp05), #7 three-mode (verdict measured, exp06 official run pending
collection), #8 positivity (open), #9 tie (RESOLVED by exp07 — can be closed).

## Key findings ledger (chronological)

- Analytic gradients: 18x; histogram-noise overfitting past ~700 iters.
- Signed birth via weight-gradient field: split alone cannot create negativity.
- Entanglement <-> tilted covariance: separable splats fail at F=0.50; full 4x4 covariance
  is the representation of entanglement (~10 tilted vs ~80 axis-aligned components).
- Exp05: the cost ratio R tracks the fringe wavenumber k (slope 1.02), NOT the saturating
  entanglement entropy E = H2((1+sech(2a^2))/2) — naive conjecture refuted, refined to:
  entanglement decides WHETHER tilt is needed, k decides HOW MUCH it saves.
- Raw-fidelity acceptance criteria are cheatable by sub-Planck spikes (signed splats are a
  basis, not states); use relative-L2 or purity-aware criteria.
- Bin-average forward correction: density histograms estimate cell AVERAGES; comparing
  center values biases fringes down, worse with more shots; convolve model with bin box.
- Sparse-count regime (0.14 counts/cell): MSE loss minimum sits below the truth; nonlinear
  polish overfits; convex matched-filter weights are the honest estimator.
- MLE traps (regression-tested): R-operator orientation; probability conjugation; and at
  3 modes the underdetermined plateau (loglik flat while fidelity far from ceiling).

## Module map

states/2/3 (reference states) · forward/fit (1D) · forward2/fit2 (separable 2-mode,
recorded negative result) · forward2f/fit2f (full-cov 2-mode winner) · forward3f/fit3f
(full-cov 3-mode winner; bin-average correction lives here — consider backporting to 2-mode)
· fock (validated Fock tools, cat2/cat3) · mle/mle2/mle3 (R rho R baselines; mle3 returns
(rho, iters, converged) + time_budget_s) · data2/data3 (shared binning) · experiments/01-07
· docs/*-plan.md, research-log.md.
