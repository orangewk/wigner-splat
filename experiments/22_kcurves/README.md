# Experiment 22 — K-curves for issue #100

`run.py` is a fit-free reanalysis of committed artifacts. It generates:

- `empirical_upper_bound.json`: Route B at the largest scoring cutoff (`n_score=12`). A fitted K-component state attains each point, so it is an **empirical upper bound** (`K_epsilon <= K`), not a certified lower bound.
- `data_proxy.json`: held-out per-sample NLL by mixture rank on the real GKP data. It is a **data proxy** because true-state fidelity, and hence `K_epsilon`, is inaccessible on the data.
- `kcurves.png`: the two curves plus an explicitly empty **certified lower bound** panel reserved for Gate T.

The script asserts the committed Route-B parameters (`eta=0.8`, `sigma=0.1`), cutoff, ruling flag, GKP test-selected frontier, and both R4 confidence intervals. It refuses stale or differently configured inputs instead of silently drawing them.

Reproduce with the repository virtual environment:

```powershell
& C:\dev\wigner-splat\.venv\Scripts\python.exe experiments\22_kcurves\run.py
```

PR self-report: this change uses only the labels **empirical upper bound**, **data proxy**, and the reserved **certified lower bound** panel; it makes no claim beyond those scopes.
