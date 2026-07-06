# handoff - Next session work order

1. Read `README.md` and `docs/prior-art-survey.md` to recover context.
2. Set up the environment: `pip install numpy matplotlib pytest`, then run `python -m pytest tests/ -q` and confirm 5 tests pass.
3. Main task: gradient-norm-driven densification / pruning (see the roadmap in `README.md`).
   `fit.loss_and_grad()` already returns per-parameter analytic gradients, so per-splat
   gradient norms are available for free; split splats with large positional gradient
   norms, prune splats whose |w_k| stays negligible.
   Acceptance: starting from a smaller K (e.g. 4), the fitter reaches the fixed-K=8
   quality of experiment 01 (relative L2 <= 0.13 with recovered negativity) or better.
4. Next task: iterative MLE baseline for the fidelity / shot-efficiency / runtime comparison.

## Done in previous sessions

- v0 scaffold: cat-state simulator, closed-form signed-splat Radon forward model,
  histogram-loss fitter with Adam, experiment 01 recovering negativity (rel. L2 13%).
- Analytic gradients (this session): replaced central differences in `wigner_splat/fit.py`
  with `loss_and_grad()` (closed-form chain rule through projected mean/variance),
  verified against central differences in `tests/test_forward.py`. Experiment 01 runs
  ~29s -> ~1.6s with relative L2 0.125 and recovered negativity (min -0.197 vs true -0.190).
  Note: past ~700 Adam iterations the fit overfits histogram shot noise and the
  Wigner-grid L2 degrades; experiment 01 stops at 680 (inside the 640-700 plateau).
