# Experiment 22 — K-curves for issue #100

`run.py` is a fit-free reanalysis of committed artifacts. It generates:

- `empirical_upper_bound.json`: the synthetic Route-B **family-constrained approximation curve**. Its fixed pre-loss operator rank is `R=2`; its x-axis `K={2,4,8}` is the number of Gaussian ket components per rank-2 column. It stores every `n_score={8,10,12} × K` best-fit point, highlights `n_score=12`, and records the corresponding empirical `R_epsilon <= 2` points. The generalized fidelity is for cropped/subnormalized matrices; it is still increasing with cutoff, so the infinite-cutoff limit is unresolved.
- `data_proxy.json`: held-out per-sample NLL by operator mixture rank `R` on the real GKP data, with `K=4` ket components fixed. It is a **data proxy** because true-state fidelity, and hence `K_epsilon`, is inaccessible on the data.
- `kcurves.png`: the two curves plus an explicitly empty **certified lower bound** panel reserved for Gate T.

Both JSON artifacts carry machine-readable rank primitive, fidelity convention, cutoff status, epistemic status, and the reserved certified-lower-bound slot. The script asserts the committed Route-B parameters (`eta=0.8`, `sigma=0.1`), every 3-cutoff × 3-K × 3-seed cell and seed uniqueness, ruling flag, GKP test-selected frontier, and both R4 confidence intervals. It refuses stale or differently configured inputs instead of silently drawing them.

Reproduce with the repository virtual environment:

```powershell
& C:\dev\wigner-splat\.venv\Scripts\python.exe experiments\22_kcurves\run.py
```

PR self-report: the figure separates a cutoff-scored synthetic family curve from a real-data rank proxy, and reserves (without computing) a certified lower-bound panel.
