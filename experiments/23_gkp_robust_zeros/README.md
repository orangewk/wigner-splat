# Experiment 23 — finite-energy GKP robust Bargmann zeros

This is Gate E for issue #71.  It evaluates the Theorem B′ premise for a
normalized, finite-energy square-lattice GKP logical-zero approximation, not
for the ideal (non-normalizable) GKP state.

**Certified subject (#71 exp23 merge review, point 1).** The state the
numbers certify is `psi_trunc`: the Fock-truncated (`n <= n_max`),
renormalized comb.  `psi_trunc` is itself a normalized pure state, so
Theorem B′ applies to it exactly.  The untruncated finite-energy comb is
within `sqrt(fock_tail_upper_bound)` of `psi_trunc` in amplitude (l2) norm —
0.074 at `Delta=0.2` — which **exceeds** `d(1e-4) = 0.010`; lifting the
bound to the untruncated comb by folding that amplitude into `d(epsilon)`
would drive `N_robust` to 0 at the current `n_max`.  The two statements
(exact bound for `psi_trunc`; l2 closeness to the comb) are therefore kept
separate and never combined into a single "certified for GKP" claim.

The convention is `[q,p]=i`: the state is
`sum_s exp(-2*pi*Delta^2*s^2) D(s*sqrt(2*pi)) S(-log Delta)|0>`.
It scans `Delta={0.2,0.3,0.4}`, three windows around `sqrt(<n>)`,
`delta={0.18,0.30}`, and `epsilon={1e-2,1e-3,1e-4}`.

`robust_zero_results.json` contains the table and the symbolic Theorem B′
column `N_robust/C - B(R+delta)`.  It deliberately does not insert a guessed
value of Friedland's constant `C`.  Its scope is the restricted common-
squeezing, bounded-displacement dictionary `G_eq(a,B)`, not unrestricted
Gaussian rank.

Fock tails are bounded conservatively: for every displaced squeezed component
the explicitly resolved tail is supplemented by the exact
`<N(N-1)>/(n_ref(n_ref+1))` Markov remainder, then combined by triangle
inequality.  The compact lattice sum has its separately recorded Gaussian
envelope amplitude remainder.  `run.py` also asserts that every reported
`N_robust` is unchanged when `n_max` rises from 160 to 200, cross-checks roots by
a tiled argument-principle count (interior cells only; the annulus near
|z| = R is not covered by this cross-check), checks disk disjointness, and applies a
finite-window area-plus-boundary density sanity check.

Reproduce deterministically:

```powershell
& C:\dev\wigner-splat\.venv\Scripts\python.exe experiments\23_gkp_robust_zeros\run.py
```

The map colors robust zeros green and non-robust zeros red at the largest
window, `delta=0.18`, and `epsilon=1e-3`.
