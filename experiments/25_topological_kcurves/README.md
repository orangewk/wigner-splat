# Experiment 25 — topological K–ε curves (issue #137, Gate M)

Measures the [issue #137](https://github.com/orangewk/wigner-splat/issues/137)
Gate M question: per cell (target, dictionary, K), the best-found `1 - F`
**and** the zero-link topology of the best state, testing whether the jumps
of the K–ε curve coincide with topology transitions in the census.
Predictions PA–PE and alarms were pre-declared in [`plan.md`](plan.md) and
committed before any output was interpreted.
`topological_kcurves.json` is the authoritative artifact; every verdict in it
is computed from measured data, and the numbers below cite it.

## Result: every fidelity cliff sits on a topology transition

- **`|1,1>` (Hopf-link target).** Coherent dictionary: `1 - F` crawls
  0.86 → 0.63 → 0.41 over `K = 1..3`, then drops to 1.6e-4 at `K = 4` —
  exactly where the census first shows a linked pair. Gaussian dictionary:
  the same drop happens already at `K = 2` (1.3e-4, Hopf link in the census),
  as P4 proves it must (PA verdict true). First-linked-K: coherent 4,
  Gaussian 2.
- **Trefoil target `0.8|20> + 0.6|03>`.** Coherent: the cliff is at `K = 5`
  (0.24 → 3.7e-3) and that is precisely where the `(3,2)` winding first
  appears; Gaussian: the cliff is at `K = 3` (0.35 → 6.0e-2, then 8.3e-3 /
  4.8e-3 / 3.3e-3), again coinciding with the first `(3,2)` census. At
  `K = 2` the Gaussian best state instead fakes progress with a linked pair
  of winding-1 circles — consistent with P6's conic winding bound
  (`max |winding| <= 2` holds in every Gaussian `K = 2` cell; PC true).
- **Alarms clean.** No coherent `K <= 2` census shows a linked pair
  (PB true, as P3 proves); no census failed; the `|11>`/coherent ladder
  agrees with exp24's independent closed-form machinery to 7.4e-5
  (`crosscheck_exp24_e4_consistent`).
- **PE.** The explicit squeezed construction pushes the trefoil /
  Gaussian / `K = 6` cell to `F = 0.9967`.

So within this experiment's scope, the expensive part of the approximation
is topological in all four ladders: the curve does not fall until the state
can afford the target's zero-link invariant, and the dictionary that buys
the invariant earlier (squeezing for the Hopf link at `K = 2`; the `(3,2)`
winding at `K = 3`) gets the earlier cliff.

## Scope limits

- All fidelities are **best-found** under a fixed multi-start Nelder–Mead
  budget (`fit_seed` in the JSON); they are upper bounds on `1 - F` only in
  the trivial direction, and nothing here is a certified supremum or lower
  bound. The trefoil/Gaussian tail `K = 4..6` in particular is still
  drifting at optimizer resolution.
- The bounded dictionary is operational: quadratic operator norm < 0.98
  **and** truncated tail mass < 1e-8 at cutoff 36. The tail budget is the
  binding constraint — it caps the effective squeezing singular value near
  0.56 — so these are bounded-squeezing dictionaries in the same spirit as,
  but not equivalent to, the K_ε note's §2.2 dictionary.
- Censuses are numerically supported, not certified (exp24 README's limits
  apply verbatim). Two-mode, pure states, unit sphere; no measured data.

## Reproduce deterministically

```bash
python experiments/25_topological_kcurves/run.py
```

Seeds are fixed; the census toolkit and its tests live in
`wigner_splat/stellar2.py` / `tests/test_stellar2.py`.
