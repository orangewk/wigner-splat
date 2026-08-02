# Experiment 29 — certified margins for the trefoil target and the conic winding bound: derivation and pre-declared claims

Status: issue #137 Gate T′ slice, adopted under orange's blanket approval of
2026-08-02 (recorded in this session's #137 thread). This memo is written
and committed **before** any implementation or run output exists; the
claims below are pre-declared and the falsification gates in §7 are fixed
here. Measured and certified-evaluated numbers live only in
`trefoil_certified.json`; this memo contains exact definitions and
formulas, never evaluated run output.

Conventions are those of `experiments/24_hopf_stellar/derivation.md` §1
and `experiments/28_isotopy_stability/derivation.md` §1–§3 (stellar
functions, dictionaries, sphere `S3_1`, phase-aligned distance `delta`,
margins `(m, sigma)`, the `eps0`/`eps0_cert` semantics, the Cauchy
constant `c1(h)`), quoted by reference. Census sphere `r = 1` throughout.

Goal. Exp28 certified a stability radius for `|1,1>` because its margins
have closed forms. This memo does the same for the exp25 **trefoil
target** and proves the conic winding bound (the statement of exp24's
P6), which together yield a certified fidelity gap **one dictionary level
above** the `|1,1>`/`D_coh` gap: no `K <= 2` superposition from the
unbounded pure-Gaussian dictionary `D_G` can approach the trefoil target
beyond an explicit fidelity bound. No novelty is claimed anywhere (Gate
S′ is open; zero sets of two-term weighted-homogeneous polynomials and
their torus-knot links are classical singularity-theory material, and the
winding-bound argument is an elementary Bezout/argument-principle
exercise).

## 1. Target and exact constants

```
T = 0.8 |2,0> + 0.6 |0,3>,      f_T(w) = a w1^2 + b w2^3,
a = 0.8 / sqrt(2!),  a^2 = 8/25,        b = 0.6 / sqrt(3!),  b^2 = 3/50.
```

`a, b > 0` with exactly rational squares, so certified rational
enclosures of every constant below follow from exact integer
comparisons (E1). On `S3_1` write `|w1| = c = cos(theta)`,
`|w2| = s = sin(theta)`, `alpha = arg w1`, `beta = arg w2`, and

```
g1(theta) = a c^2 - b s^3,
phi       = 2 alpha - 3 beta   (mod 2 pi),
|f_T|^2   = g1^2 + 4 a b c^2 s^3 cos^2(phi / 2)
          = (a c^2 - b s^3)^2 + 4 a b c^2 s^3 cos^2(phi / 2).
```

**W1 (structure of the zero link — status: §8 table).** `g1` is strictly
decreasing on `(0, pi/2)` (`g1' = -s c (2a + 3 b s) < 0`), from `a > 0`
to `-b < 0`, so `a c^2 = b s^3` has a unique root `theta* = arcsin(s*)`,
where `s*` is the unique root in `(0, 1)` of the cubic

```
b s^3 + a s^2 - a = 0.
```

The zero set `L_1(T) = {theta = theta*, phi = pi}`: on the flat torus
`{theta = theta*}` the condition `2 alpha - 3 beta ≡ pi (mod 2 pi)` is a
single closed curve (`gcd(2, 3) = 1`), parametrized by
`(alpha, beta) = (alpha0 + 3u, beta0 + 2u)`, `u in [0, 2 pi]`. Hence
`L_1(T)` is **one component with core windings `(m1, m2) = (3, 2)`** (a
`(2,3)` torus knot; the trefoil), and it is **disjoint from both core
circles**, with geodesic distances `theta*` to `{w2 = 0}` and
`pi/2 - theta*` to `{w1 = 0}` (exp28 §4's distance formulas).
Regularity: on `L_1(T)`, `|d f_T|^2 = 4 a^2 c^2 + 9 b^2 s^4 > 0` and
transversality follows from W3's bound below being positive at
`rho -> 0`. ∎

## 2. Metric-neighborhood form of the exp28 stability theorem

**W0 (metric-neighborhood stability theorem; standalone statement —
status: §8 table).** Let `T` be a unit state whose `f_T` has `0` as
a regular value of `f_T|S3_1`, let `U` be any closed subset of `S3_1`
containing `L_1(T)` in its interior, and define

```
m     = min over the closed set S3_1 \ int(U) of |f_T|,
sigma = min over U of sigma_2( d(f_T|S3) ),
```

both assumed positive. Let `g` be a unit state with phase-aligned
distance `delta` to `T` satisfying, for some `h > 0`,

```
(C0)  delta e^{1/2} < m        and        (C1)  delta c1(h) < sigma.
```

Then `Z(f_g) ∩ S3_1` is a smooth closed 1-manifold contained in `U`,
and `(S3_1, Z(f_g) ∩ S3_1)` is ambient-isotopic to `(S3_1, L_1(T))`
through an isotopy whose zero-set track stays inside `U`. If moreover
`U` is disjoint from the two core circles, every component stays
disjoint from the cores throughout, so core windings transfer as the
isotopy-stable linking numbers with the cores. **No tube or normal-
injectivity structure on `U` is assumed.**

Proof (self-contained; the same chain as exp28 §3, reproduced so that
this statement does not depend on exp28's admissibility wording).
Interpolate `f_t = f_T + t Delta`, `Delta = f_g - f_T` after phase
alignment. Exp28 S1 gives `|f_t - f_T| <= |t| delta e^{1/2}` on the
sphere and exp28 S2 gives the C^1 analogue with constant `c1(h)`; both
scale linearly in `|t|`. Strictness of (C0)/(C1) therefore yields
`kappa > 0` such that for all `t in (-kappa, 1 + kappa)`: every zero of
`f_t|S3` lies in `U` (else `|f_T| >= m` at that point, contradicting
(C0)-with-slack), and `sigma_2(d(f_t|S3)) >= sigma - (1 + kappa) delta
c1(h) > 0` on `U`. Hence

```
Z_open = { (t, w) in (-kappa, 1 + kappa) x S3_1 : f_t(w) = 0 }
```

is a smooth boundaryless 2-manifold (regular-value theorem at each
`t`, jointly smooth in `(t, w)`), and the projection to
`(-kappa, 1 + kappa)` is a submersion (surjectivity of `d_w(f_t|S3)`
lifts any `dt`-component) and proper (preimages of compact
subintervals are closed subsets of compact products). Ehresmann's
fibration theorem trivializes it over `[0, 1]`, giving a smooth isotopy
from `L_1(T) = Z_0` to `Z(f_g) ∩ S3_1 = Z_1` with every intermediate
zero set inside `U`; the isotopy extension theorem (textbook input,
declared: Hirsch, *Differential Topology*, ch. 8) upgrades it to an
ambient isotopy of `S3_1`. Nothing in this chain references a tubular
structure of `U`. If `U ∩ (cores) = ∅`, the track stays off the cores,
each `Z_t` component's linking numbers with the cores are constant in
`t`, and for components disjoint from the cores these equal the core
windings (exp24 §1). ∎

For this experiment `U = U_rho := {p : dist(p, L_1(T)) <= rho}` with
the **declared constraint**

```
rho < min(theta*, pi/2 - theta*),
```

which is certified from the E1 enclosure of `theta*` and implies
`U_rho ∩ (cores) = ∅` since `dist >= |theta - theta*|`. Exp28's file is
not edited by this memo.

## 3. Certified clearance

Fix a declared band `B = [theta_lo, theta_hi]` with rational endpoints
and the certified check `theta* in B` (E1 sign checks). Define, with all
maxima/minima taken via monotone factors on the stated intervals (each
evaluable on the E1 enclosures with outward rounding):

```
m_band   = min(|g1(theta_lo)|, |g1(theta_hi)|)          (g1 monotone),
lam_B    = [min of s c over the endpoints of B] * (2a + 3 b sin(theta_lo)),
kap_B    = 4 a b cos(theta_hi)^2 sin(theta_lo)^3,
G        = sqrt( 4 / cos(theta*)^2 + 9 / sin(theta*)^2 )   (lower-bounded
           on the enclosure of theta*).
```

**W2 (certified clearance — status: §8 table).** For every `rho > 0`,

```
m_cert(rho) = min( m_band,  lam_B * rho / 2,  sqrt(kap_B) * G * rho / (2 pi) )
```

satisfies `|f_T(p)| >= m_cert(rho)` for every `p` with
`dist(p, L_1(T)) >= rho`.

Proof. If `theta(p) not in B`: `|f_T| >= |g1| >= m_band` by monotonicity.
If `theta(p) in B`: the point `q = (theta*, alpha(p), beta(p))` and the
flat-torus distance from `(alpha, beta)` to the line `{phi ≡ pi}` give

```
dist(p, L_1(T)) <= |theta - theta*| + |psi| / G,     psi := phi - pi in [-pi, pi],
```

(the theta-segment is a geodesic of length `|Delta theta|`; on the torus
`{theta = theta*}` with metric `c*^2 d alpha^2 + s*^2 d beta^2` the
distance to the zero level of the linear functional `psi` is
`|psi| / |grad psi|` with `|grad psi| = G`; intrinsic torus distance
upper-bounds ambient distance). So `dist >= rho` forces
`max(|Delta theta|, |psi|/G) >= rho/2`. In the first case the mean value
theorem on `B` (where `|g1'| >= lam_B`, using `s c` minimized at the
endpoints of `B` since `s c` is unimodal with maximum at `pi/4`, and
`2a + 3bs` increasing) gives `|f_T| >= |g1| >= lam_B rho / 2`. In the
second, `sin(|psi|/2) >= |psi| / pi` on `|psi| <= pi` and
`4 a b c^2 s^3 >= kap_B` on `B` give
`|f_T| >= sqrt(kap_B) |psi| / pi >= sqrt(kap_B) G rho / (2 pi)`; if
`G rho / 2 > pi` this case is vacuous and the bound only loosens. ∎

**Corollary (cloud-error certificate; added in the 2026-08-02 Sol audit
round to close the residual-to-distance gap in E3's membership).** If
`|f_T(q)| <= r0 < m_band` then `theta(q) in B` (outside `B`,
`|f_T| >= m_band`), hence `|theta(q) - theta*| <= r0 / lam_B` (MVT on
`B`) and `|psi(q)| <= pi r0 / sqrt(kap_B)` (the phase term alone is
below `|f_T|`), and W2's distance decomposition gives

```
dist(q, L_1(T)) <= r0 * ( 1/lam_B + pi / (sqrt(kap_B) G) ).
```

The run evaluates an outward-safe maximum residual over the **actual
committed cloud** (high-precision Decimal at exactly normalized points)
and feeds that value — not the filter threshold — into this bound,
recording both in the artifact. ∎

**Lemma (float-distance budget; added in the round-5 re-audit to tie
the certificate points to the distance selector).** For `x in [0, 1]`
and `eps in [0, 1]`,

```
arccos( x (1 - eps) ) <= arccos(x) + sqrt(3 eps).
```

Proof: with `d = arccos(x)` and `delta = sqrt(3 eps)`, `cos(d + delta)
<= cos d cos delta` (both angles in `[0, pi]`) and `cos delta <= 1 -
3 eps/2 + 3 eps^2/8 <= 1 - eps`, so `cos(d + delta) <= x (1 - eps)`;
monotonicity of `cos` gives the claim. ∎

Consequently, when the selector computes `acos(p . c)` on float rows
`p` (sphere samples) and `c` (the once-normalized cloud, the **same
array** whose exact normalizations carry the residual certificate), the
true geodesic distance to the certified point exceeds the computed one
by at most `dist_budget := sqrt(3 eps_tot)`, where `eps_tot` is a
declared relative budget covering the unit-norm defects of `p` and `c`
(a few ulps each) and the float dot/acos rounding — the run declares
`eps_tot = 1e-14`, giving `dist_budget < 2e-7`, and gates the
cloud-inside family on

```
cloud_err + dist_budget <= tol_cloud        (tol_cloud declared),
```

with the selector using `rho - tol_cloud`. Membership then follows:
`dist(p_hat, L) <= acos(p . c) + dist_budget + cloud_err <= rho`. ∎

## 4. Certified transversality

Let `E(w) = w1 d1 f_T + w2 d2 f_T = 2 a w1^2 + 3 b w2^3 = 3 f_T - a w1^2`
(the Euler field pairing). As in exp28 §4, for any unit covector `u` the
`C^2`-gradient of `Re(u* f_T)` has squared norm
`|d f_T|^2 = 4 a^2 c^2 + 9 b^2 s^4` (u-independent) and radial component
`Re(u* E)`, of magnitude `<= |E|`. Hence pointwise

```
sigma_2( d(f_T|S3) ) >= sqrt( |d f_T|^2 - |E|^2 )        whenever positive.
```

**W3 (certified transversality on `U_rho` — status: §8 table).** With
`theta^- = arcsin(s_lo) - rho`, `theta^+ = arcsin(s_hi) + rho` from the
E1 enclosure `s* in [s_lo, s_hi]` (every point of `U_rho` has
`|theta - theta*| <= rho` since `theta` is 1-Lipschitz), define

```
D2_min(rho)  = 4 a^2 cos(theta^+)^2 + 9 b^2 sin(theta^-)^4,
Gbar(rho)^2  = 4 / cos(theta^+)^2 + 9 / sin(theta^-)^2,
lam_up       = a + (3/2) b                     (from s c <= 1/2, s <= 1),
M_f(rho)     = rho * sqrt( lam_up^2 + a b cos(theta^-)^2 Gbar(rho)^2 ),
E_max(rho)   = 3 M_f(rho) + a cos(theta^-)^2,
sigma_cert(rho) = sqrt( max(0, D2_min(rho) - E_max(rho)^2) ).
```

(Correction, 2026-08-02 second review round: the first draft carried an
extra `/4` inside `M_f`'s square root. It does not survive the algebra —
`4 a b c^2 s^3 sin^2(psi/2) <= 4 a b c^2 s^3 * psi^2/4 = a b c^2 s^3
psi^2` — so the factor cancels exactly. The finding is algebraic; a
numerical witness offered alongside it was later withdrawn by the
reviewer (wrong phase origin), and probes of `U_0.10` did not violate
the old value — which was therefore accidentally true, but not proved
by the old chain. The formula above and the implementation carry the
corrected coefficient.)

Then `sigma_2 >= sigma_cert(rho)` on `U_rho`. Proof: `|d f_T|^2 >=
D2_min` by the monotonicity of `c^2` (decreasing) and `s^4` (increasing);
`|f_T| <= M_f(rho)` on `U_rho` from `|g1| <= lam_up * rho` (MVT with the
global bounds `s c <= 1/2`, `s <= 1`) and
`|psi| <= Gbar(rho) * rho` (`psi` is Lipschitz with constant
`|grad psi| <= Gbar(rho)` on the theta-band of `U_rho`, and `psi = 0` on
the zero curve), with `sin^2(psi/2) <= psi^2/4`; hence
`|E| <= 3 |f_T| + a c^2 <= E_max(rho)`. ∎

## 5. The conic winding bound (the statement of exp24's P6)

**W4 (conic winding bound — status: §8 table).** Standing hypotheses, stated in full: `f_g = z1
e^{q1} + z2 e^{q2}` with `z1 z2 != 0` (a vanishing coefficient reduces
to `K <= 1`), `q1, q2` holomorphic affine quadratics in `(w1, w2)`
(exp24 §1's `D_G`; pure-state terms, any displacement and squeezing,
no boundedness assumed), zero link on some `S3_r` nonempty, and the
component `gamma` under consideration avoids the two coordinate core
circles and the singular points of its level set (the census convention
of exp24 §1; on-core or through-singularity components carry no winding
claim). All degenerations of the level sets — `Q` affine-linear, `Q`
constant, reducible conics including line pairs and double lines — are
covered by the case split below. Conclusion: `|m1| <= 2` and
`|m2| <= 2`.

Proof. `K = 1` is vacuous (`f = z e^q` has no zeros). For `K = 2`,
`f_g = 0` iff `Q(w) := q2(w) - q1(w)` lies in the countable level set
`{log(-z1/z2) + 2 pi i n}`, so every component lies on one affine level
`V_c = {Q = c}` with `Q` affine quadratic.

Case (i): `Q` affine linear (or a level is a line pair / double line
after degeneration). Each irreducible piece is an affine complex line;
`w1` restricted to a line is affine of degree `<= 1`, and the argument
below gives `|m1| <= 1`.

Case (ii): `V_c` an irreducible affine conic. Its projective closure
`Vbar` in `CP^2` is an irreducible curve of degree 2, hence rational:
the normalization is `nu : CP^1 -> Vbar`, injective away from the
finitely many preimages of `Sing(Vbar)`. If `w1` is constant on `V_c`,
then `gamma` avoiding `{w1 = 0}` forces that constant nonzero and
`m1 = 0`. Otherwise `w1 ∘ nu : CP^1 -> CP^1` is a nonconstant rational
map whose degree `d1` equals the intersection number of `Vbar` with a
generic line `{w1 = t}`, so `d1 <= 2` by Bezout (the closure of an
affine curve never contains the line at infinity).

`gamma` avoids `Sing(V_c)` and the cores, so it lifts to an **embedded**
closed loop `gamma~` in `CP^1` avoiding the zeros and poles of
`w1 ∘ nu`. An embedded loop in `CP^1` separates it into two disks (Jordan);
let `D` be one of them. By the argument principle for the meromorphic
function `w1 ∘ nu` on `D`,

```
m1 = winding of arg w1 along gamma
   = (zeros of w1∘nu in D) - (poles of w1∘nu in D)   counted with multiplicity,
```

and both counts are bounded by `deg(w1 ∘ nu) = d1 <= 2`, so
`|m1| <= 2`. The same argument with `w2` gives `|m2| <= 2`. ∎

(Orientation bookkeeping: reversing the choice of disk or of `gamma`'s
orientation flips the sign only. Nothing in exp24's §4 table is edited
by this memo; promoting P6's status there is a separate step after this
memo passes review, per the one-authoring-location rule.)

## 6. The certified gap one dictionary level up

Let `eps29_cert` be the best certified value of
`min( m_cert(rho) e^{-1/2}, sigma_cert(rho) / c1(h) )` over the declared
`(rho, h)` grid, with `rho` restricted by W0's core-disjointness
constraint (E2). The `eps0`/`eps0_cert` semantics of exp28 §3 apply
verbatim: `eps29_cert` lower-bounds the supremum, which lower-bounds the
true breaking radius, and every runnable statement uses `eps29_cert`.

**W5 (certified `D_G, K <= 2` gap at the trefoil — status: §8 table;
uses W0–W4).** For every `K <= 2`
superposition `g` from `D_G` (unit-normalized, phase-aligned),

```
delta(g, T) >= eps29_cert,   equivalently   F(g, T) <= (1 - eps29_cert^2 / 2)^2.
```

Proof. Suppose `delta(g, T) < eps29_cert`. By exp28 S3 with W0's metric
neighborhood (margins W2, W3; conditions C0, C1 hold for the certifying
pair), `Z(f_g) ∩ S3_1` is a smooth closed 1-manifold ambient-isotopic to
`L_1(T)`, contained in `U_rho` with `U_rho` disjoint from the cores; in
particular it is **nonempty** (excluding `K = 1` and zero-free `K = 2`
configurations) and consists of one component `gamma_g`. The isotopy
keeps `gamma_g` disjoint from the cores, so its core windings equal its
linking numbers with the cores, which are isotopy-invariant and equal
the target's: `(m1, m2) = (3, 2)` up to overall orientation. Smoothness
plus (C1)-transversality on `U_rho` force `d f_g != 0` on the zero set
there, so `gamma_g` avoids the singular points of its level set, and it
avoids the cores; W4 then gives `|m1| <= 2` — contradicting `|m1| = 3`.
∎

Scope table:

| ID | Modes | Sphere | Quantifies over |
| --- | --- | --- | --- |
| W0 | 2 | `r = 1` | regular targets, metric neighborhoods |
| W1 | 2 | `r = 1` | this target only |
| W2, W3 | 2 | `r = 1` | this target only |
| W4 | 2 | every `r` | `D_G`, `K <= 2`; components off cores and singular points |
| W5 | 2 | `r = 1` | `D_G`, `K <= 2` |

## 7. Numerical blocks and falsification gates

Verdict booleans are computed from data in `run.py`; grid standards
follow exp24/25. "Certified evaluation" means: every constant traced to
the E1 rational enclosures and combined by the monotone-factor rules of
§3–§4, with a declared outward-rounding slop recorded in the JSON.

- **E1 (exact enclosures).** Prove rational enclosures for `a, b` (by
  exact integer squaring against `a^2 = 8/25`, `b^2 = 3/50`), for `s*`
  (sign checks of `b s^3 + a s^2 - a` at declared rational points using
  the `a, b` enclosures, in exact `fractions` arithmetic), hence for
  `theta*`, `G`, and the band membership `theta* in B`. Gate `F1`
  (halt, defect): any sign check fails or an enclosure is empty.
- **E2 (certified evaluation).** Evaluate `m_cert(rho)`,
  `sigma_cert(rho)` on the declared `rho` list (respecting W0's
  constraint) and `eps29_cert` over the `(rho, h)` grid; record the
  certifying pair and the W5 fidelity bound. Gate `F2` (halt
  interpretation): `eps29_cert <= 0` or no admissible `rho`.
- **E3 (margin referees; revised in the 2026-08-02 second review round —
  the first draft's cloud-complement referee was not one-sided, because
  cloud distance upper-bounds nothing: it over-estimates the true
  distance to the link, so `d_cloud >= rho` does not certify complement
  membership).** Two **sound** referees gate F3, plus one recorded
  diagnostic:
  - (a) clearance, sound subset: every sphere sample with
    `|theta - theta*| >= rho` certainly lies outside `int(U_rho)`
    (`dist >= |Delta theta|`); check `|f_T| >= m_cert(rho) - tol` there.
  - (b) transversality, sound subsets: (i) samples within computed
    cloud distance `rho - tol_cloud` of the **once-normalized** polished
    zero cloud certainly lie in `U_rho`, **provided** the full §3 chain
    is established first: the residual certificate is evaluated on the
    exact normalizations of the same normalized array the distance
    selector uses, and the gate is `cloud_err + dist_budget <=
    tol_cloud` with the float-distance budget of §3's lemma (round-5
    revision: `tol_cloud = 1e-6`, `eps_tot = 1e-14`; all recorded in
    the artifact); (ii) targeted phase-normal samples on the
    `theta*` torus with `|Delta theta| + |psi| / G_lower <= rho`
    (membership by W2's distance decomposition, with `G_lower <= G`
    only loosening it). Check `sigma_2 >= sigma_cert(rho) - tol` on
    both families.
  - (c) diagnostic, not a gate: the exp28-E5-style cloud-complement grid
    margins are recorded for comparison only (their complement
    membership is heuristic).
  Gate `F3` (blocking halt) on any violation in (a) or (b).
- **E4 (structure referee; stand-in declared explicitly in the
  2026-08-02 second review round).** Census of `T` on the standard grid
  must show one component with `|windings| = {3, 2}` and no linked pair
  (matching W1). Coordinate checks use the **polished zero cloud as the
  declared stand-in** for traced loop points (the census exposes loop
  coordinates only stereographically): every cloud point must satisfy
  both `theta` inside the E1 enclosure of `theta*` up to the declared
  tolerance, and `min(theta, pi/2 - theta) >=
  min(theta*_lo, pi/2 - theta*_hi) - tol` (cores-disjointness, the
  declared quantity). Gate `F4` (blocking halt) on mismatch.
- **E5 (exp25 consistency).** The measured best-found fidelities of
  exp25's `trefoil/gaussian/K=1` and `trefoil/gaussian/K=2` cells (read
  from `topological_kcurves.json`, never restated) must satisfy
  `F <= (1 - eps29_cert^2/2)^2`. Gate `F5` (blocking halt): a proof-vs-
  measurement contradiction.

## 8. Claim table

One row per claim; empty cells would be visible. This table is the sole
authoring location for exp29 statuses.

| ID | Claim (headline) | Status | Basis |
| --- | --- | --- | --- |
| W0 | exp28 S3 holds for metric neighborhoods; winding transfer off cores | proved here | §2 |
| W1 | trefoil zero link = one `(3,2)`-winding curve at `theta*`, off both cores | proved here | §1 |
| W2 | certified clearance `m_cert(rho)` | proved here | §3 |
| W3 | certified transversality `sigma_cert(rho)` | proved here | §4 |
| W4 | conic winding bound `|m1|,|m2| <= 2` for `D_G K<=2` (exp24 P6 statement) | proved here | §5 |
| W5 | certified `D_G K<=2` fidelity gap at the trefoil | proved here (uses exp28 S3) | §6 |
| N1 | exact rational enclosures established | numerical, E1 | run |
| N2 | `eps29_cert > 0` evaluated, fidelity bound recorded | numerical, E2 | run |
| N3 | sound margin referees pass (theta-complement clearance; cloud-inside and phase-normal transversality) | numerical, E3 | run |
| N4 | target census matches W1, cores-disjoint | numerical, E4 | run |
| N5 | exp25 trefoil cells within the certified bound | numerical, E5 | run |

Epistemic discipline: "proved here" means proved in this pre-declaration
memo and not yet independently reviewed; "certified" refers to the
`eps0_cert` semantics of exp28 §3 (a machine-evaluable lower bound
traced to exact enclosures), not to the certified-lower-bound language
of the K_ε note, which stays unavailable until Gate T′ closes (issue
#137 scope rule). Exp24's claim table is not edited by this experiment;
promoting P6 there is a separate reviewed change. `eps29_cert` is a
bound from below on the breaking radius, never an estimate of it. All
`D_G` statements quantify over the unbounded exp24 dictionary — which
contains exp25's operational `D_G^b` — so W5 also bounds every
`D_G^b` cell (dictionary alignment beyond this containment stays Gate
T′ (c)).
