# Experiment 23 — finite-energy GKP robust Bargmann zeros

This is Gate E for issue #71.  It evaluates the Theorem B′ premise for a
normalized, finite-energy square-lattice GKP logical-zero approximation, not
for the ideal (non-normalizable) GKP state.

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
`<N(N-1)>/((n_ref+1)(n_ref+2))` Markov remainder, then combined by triangle
inequality.  The compact lattice sum has its separately recorded Gaussian
envelope amplitude remainder.  `run.py` also asserts that every reported
`N_robust` is unchanged when `n_max` rises from 160 to 200, validates roots by
a tiled argument-principle count, checks disk disjointness, and applies a
finite-window area-plus-boundary density sanity check.

Reproduce deterministically:

```powershell
& C:\dev\wigner-splat\.venv\Scripts\python.exe experiments\23_gkp_robust_zeros\run.py
```

The map colors robust zeros green and non-robust zeros red at the largest
window, `delta=0.18`, and `epsilon=1e-3`.
