# Experiment 23 — finite-energy GKP robust Bargmann zeros

This is Gate E for issue #71.  It evaluates the Theorem B′ premise for a
normalized, finite-energy square-lattice GKP logical-zero approximation, not
for the ideal (non-normalizable) GKP state.

**Discretization-bounded subject (configuration-specific; #71 management review).** The
JSON retains sampled and discretization-bounded columns: `N_robust_sampled` /
`N_robust_bounded` for `psi_trunc`, and their `N_robust_lifted_*`
counterparts for the untruncated finite-energy comb. The discretization-bounded count uses
the sampled circle minimum minus one sample-arc length times a coefficient-
norm upper bound on `sup |F'|`; it is therefore a lower bound for the true
circle minimum. The lifting threshold is `d(epsilon) + sqrt(fock_tail_upper_bound) +`
`lattice_envelope_amplitude_bound`. At
`delta=0.18` in the largest window, the discretization-bounded ideal-comb count remains
nonzero for `Delta=0.3, epsilon=1e-4` and `Delta=0.4, epsilon<=1e-3`;
`Delta=0.2` remains discretization-bounded only for `psi_trunc`.
For `Delta=0.2`, the tail norm is 0.074 at `n_max=160`, greater than
`d(1e-4)=0.010`; raising `n_max` through 260 does not yield a lifted zero,
while `polyroots` overflows around `n_max=320`. This implementation thus has
a numerical ceiling of roughly `n_max <= 300` for that lifting attempt.
The convention is `[q,p]=i`: the state is
`sum_s exp(-2*pi*Delta^2*s^2) D(s*sqrt(2*pi)) S(-log Delta)|0>`.
It scans `Delta={0.2,0.3,0.4}`, three windows around `sqrt(<n>)`,
`delta={0.18,0.30}`, and `epsilon={1e-2,1e-3,1e-4}`.

`robust_zero_results.json` contains the table and the symbolic Theorem B′
column `N_robust_bounded/C - B(R+delta)`.  It deliberately does not insert a guessed
value of Friedland's constant `C`.  Its scope is the restricted common-
squeezing, bounded-displacement dictionary `G_eq(a,B)`, not unrestricted
Gaussian rank.

Fock tails are bounded conservatively: for every displaced squeezed component
the explicitly resolved tail is supplemented by the exact
`<N(N-1)>/(n_ref(n_ref+1))` Markov remainder, then combined by triangle
inequality.  The compact lattice sum has its separately recorded Gaussian
envelope amplitude remainder.  `run.py` also asserts that every reported
`N_robust_bounded` is unchanged when `n_max` rises from 160 to 200, cross-checks roots by
a tiled argument-principle count (interior cells only; the annulus near
|z| = R is not covered by this cross-check), checks disk disjointness, and applies a
finite-window area-plus-boundary density sanity check.

Reproduce deterministically:

```powershell
& C:\dev\wigner-splat\.venv\Scripts\python.exe experiments\23_gkp_robust_zeros\run.py
```

The map colors robust zeros green and non-robust zeros red at the largest
window, `delta=0.18`, and `epsilon=1e-3`.
