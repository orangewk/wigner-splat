# handoff - Next session work order

1. Read `README.md` and `docs/prior-art-survey.md` to recover context.
2. Set up the environment: `pip install numpy matplotlib pytest`, then run `python -m pytest tests/ -q` and confirm 4 tests pass.
3. Main task: replace the numerical central-difference gradients in `wigner_splat/fit.py` with closed-form analytic gradients.
   The forward model in `forward.py` (`radon()`) is a closed-form Gaussian projection, so its gradients can be derived directly.
   Acceptance: `experiments/01_cat_state/run.py` reaches results at least as good as v0, with recovered negativity and relative L2 <= 0.13, while running much faster than the numerical-gradient implementation.
4. Next task: design densification / pruning driven by gradient norms. See the roadmap in `README.md`.
