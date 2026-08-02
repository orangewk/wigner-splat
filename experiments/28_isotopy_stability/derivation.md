# Experiment 28 — link-type stability inside a fidelity ball: derivation and pre-declared claims

Status: **Hopf runner proposal, pending orange decision** — a proposed
slice 1 of issue #137 Gate T′ sub-goal (a), drafted 2026-08-02. Adoption
of Gate T′ (a) and the selection of research direction are NOT delegated
to the runner; implementation and runs start only on orange's separate
GO. This memo is written and committed **before** any implementation or
run output exists; the claims below are pre-declared, and the
falsification gates in §6 are fixed here. Measured numbers will live only in
`isotopy_stability.json`; this memo contains formulas and closed forms,
never evaluated run output.

Conventions are those of `experiments/24_hopf_stellar/derivation.md` §1
(stellar function `f_psi`, dictionaries, sphere `S3_r`, zero link
`L_r(psi)`), quoted by reference, not restated. The census sphere is
`r = 1` throughout; every claim in this memo is an `r = 1` statement
unless its row says otherwise.

Motivation. Exp24's P5 argued a fidelity gap by a tube/degree sketch and
管理役指摘2 (2026-07-31, issue #137) isolated the missing rung: stability
of the zero **count** does not by itself give stability of the link
**type** (isotopy). This memo closes that rung quantitatively: a norm
ball around a target with regular zero link on the sphere forces the
perturbed link to be ambient-isotopic to the target's, with explicit
constants, and evaluates the constants in closed form for `|1,1>`.
Combined with exp24 P3 (proved), this upgrades the P5-style gap for
`D_coh, K <= 2` against `|1,1>` from sketch to an explicit bound. No
novelty is claimed for any statement here (Gate S′ survey is open; the
stability toolbox — kernel bounds, Cauchy estimates, Ehresmann fibration,
isotopy extension — is standard); what is recorded is that the explicit
constants for these targets are now derived and testable in-repo.

## 1. Distance conventions

For unit vectors, `||psi - phi||^2 = 2(1 - Re<psi|phi>)`. Zeros of
stellar functions ignore global phase, so the working distance is the
phase-aligned norm distance

```
delta(psi, phi) = min_theta ||psi - e^{i theta} phi|| = sqrt(2(1 - sqrt(F))),
F = |<psi|phi>|^2.
```

All bounds below are stated in `delta`; the fidelity form is obtained by
inverting this monotone relation and is generated in code, not restated
by hand anywhere else.

## 2. Perturbation bounds (claims S1, S2)

**S1 (kernel sup bound; proved here).** For any states `psi, phi` and any
`w in C^2`,

```
|f_psi(w) - f_phi(w)| <= ||psi - phi|| * exp(|w|^2 / 2).
```

Proof: `f_psi(w) - f_phi(w) = sum_mn (c - d)_mn w1^m w2^n / sqrt(m! n!)`;
Cauchy–Schwarz against the square-summable weights `w1^m w2^n/sqrt(m!n!)`
whose squared sum is `exp(|w|^2)`. Equality holds when `psi - phi` is
proportional to the conjugated coherent kernel at `w`, so the constant is
sharp. ∎

**S2 (Cauchy derivative bound; proved here).** Let `Delta = f_psi - f_phi`
and `delta = ||psi - phi||`. For `|w0| <= 1` and any `h > 0`, the Cauchy
integral formula on the circle `|z - w0j| = h` in each coordinate gives

```
|d_j Delta(w0)| <= delta * exp((1 + h)^2 / 2) / h,      j = 1, 2,
```

since `|w|^2 <= (1 + h)^2` on those circles when `|w0| <= 1`. The real
differential of `Delta` as a map `R^4 -> R^2` at `w0` has operator norm
`sqrt(|d_1 Delta|^2 + |d_2 Delta|^2) <= delta * c1(h)` with

```
c1(h) = sqrt(2) * exp((1 + h)^2 / 2) / h.
```

`h` is a free parameter, optimized in code jointly with the tube radius
(§4); no value of `h` is fixed in this memo. ∎

## 3. The stability theorem (claim S3)

Target data. Let `T` be a unit state whose stellar function `f_T` has, on
`S3_1`, a **regular zero link**: `0` is a regular value of the restriction
`f_T|S3` (so `L_1(T)` is a smooth closed 1-manifold). Call a tube radius
`rho > 0` **admissible** when (i) `rho` is below the normal injectivity
radius of every component, so each closed geodesic tube of radius `rho`
around a component of `L_1(T)` in `S3_1` is an embedded closed solid
torus, (ii) the closed tubes are pairwise disjoint (their union is
`U_rho`), and (iii) both margins below are strictly positive. Define

```
m(rho)     = min over the closed set S3_1 \ int(U_rho) of |f_T|   (clearance),
sigma(rho) = min over U_rho of sigma_2( d(f_T|S3) )               (transversality),
```

`sigma_2` the smallest singular value of the real differential
`T_w S3 -> R^2`. Both minima run over compact sets, hence are attained;
for a regular target they are positive for all small enough `rho`, so
admissible radii exist.

**S3 (fidelity-ball link stability; proved here).** Let `g` be any unit
state with phase-aligned distance `delta(g, T) = delta`. If for some
admissible `rho` and some `h > 0`

```
(C0)  delta * e^{1/2}  <  m(rho)          and
(C1)  delta * c1(h)    <  sigma(rho),
```

then `Z(f_g) ∩ S3_1` is a smooth closed 1-manifold contained in `U_rho`
and the pair `(S3_1, Z(f_g) ∩ S3_1)` is ambient-isotopic to
`(S3_1, L_1(T))`. In particular component count and linking matrix —
ambient-isotopy invariants — coincide with the target's. Core windings
are frame-fixed quantities (exp24 P2), not isotopy invariants; they
transfer to the perturbed link only under the **additional hypothesis**
that `U_rho` is disjoint from both core circles `{w1 = 0} ∩ S3_1` and
`{w2 = 0} ∩ S3_1` — then every component stays disjoint from the cores
throughout the isotopy and its windings equal the isotopy-stable linking
numbers with them. That hypothesis fails for the `|1,1>` target itself,
whose link components ARE the core circles; no core-winding claim is
made for that target here (the linking matrix already distinguishes the
Hopf census, and none of S4–S5 uses windings).

Proof. Interpolate `f_t = f_T + t * Delta`, `t in [0, 1]`, `Delta = f_g -
f_T` after phase alignment (zeros of `f_g` and of the aligned function
agree). By S1, `|f_t - f_T| <= delta e^{1/2}` on `S3_1`, so (C0) forces
`Z(f_t) ∩ S3_1 ⊂ U_rho` for every `t`. By S2, `sigma_2(d(f_t|S3)) >=
sigma(rho) - delta c1(h) > 0` on `U_rho`, so `0` is a regular value of
every `f_t|S3` there. Hence

```
Z = { (t, w) in [0,1] x S3_1 : f_t(w) = 0 }
```

would be a compact 2-manifold with boundary over `t in {0, 1}` — and
Ehresmann's fibration theorem is stated for boundaryless proper
submersions, so the boundary case is not applied directly. Instead, use
the strictness of (C0) and (C1): both error bounds scale linearly with
`|t|` (the interpolation formula makes sense for every real `t`, with
`|f_t - f_T| <= |t| delta e^{1/2}` and the C^1 analogue), so there is a
`kappa > 0` such that (C0) and (C1) hold for the same `(rho, h)` and all
`t in (-kappa, 1 + kappa)`. Over that open interval

```
Z_open = { (t, w) in (-kappa, 1 + kappa) x S3_1 : f_t(w) = 0 }
```

is a smooth **boundaryless** 2-manifold, and the projection
`Z_open -> (-kappa, 1 + kappa)` is a submersion (surjectivity of
`d_w(f_t|S3)` lets any `dt`-component be lifted) and proper (the
preimage of a compact subinterval is a closed subset of a compact
product). Ehresmann's fibration theorem now applies; trivializing over
`[0, 1]` gives a smooth isotopy from `L_1(T)` to `Z(f_g) ∩ S3_1` inside
`U_rho`, and the isotopy extension theorem (textbook input, declared:
Hirsch, *Differential Topology*, ch. 8) upgrades it to an ambient
isotopy of `S3_1`. ∎

The resulting stability radius is

```
eps0(T) = sup over admissible rho and h > 0 of
          min( m(rho) * e^{-1/2},  sigma(rho) / c1(h) ),
```

a supremum (not claimed attained) over the admissible parameter set. Any
`delta < eps0(T)` lies below the min for some admissible `(rho, h)`, so
(C0) and (C1) hold for that pair and the link type is preserved.

Two distinct symbols, never interchanged:

- `eps0(T)` — the supremum above. A theoretical quantity; in general not
  computed exactly, and never reported as a number.
- `eps0_cert(T)` — the largest attained min over the **declared finite
  search grid** of admissible `(rho, h)` pairs, evaluated in `run.py`.
  Each admissible pair certifies its own min as a valid stability
  radius, so `eps0_cert(T) <= eps0(T) <=` (true breaking radius), and
  S3 directly guarantees: `delta < eps0_cert(T)` preserves the link
  type.

Every runnable statement in this experiment — the gates F2–F4, the E4
comparison, every JSON field — is stated in `eps0_cert`, never in
`eps0`.

## 4. Closed forms for the Hopf target (claim S4)

**S4 (margins of `|1,1>`; proved here).** `f = w1 w2`. On `S3_1` write
`|w1| = cos(theta)`, `|w2| = sin(theta)`. The geodesic distance from a
point to the core circle `{w2 = 0}` is `arcsin |w2|`, so the two tubes of
radius `rho` are `{|w2| <= sin rho}` and `{|w1| <= sin rho}`, disjoint
embedded solid tori for `rho < pi/4`. Then:

Every `rho < pi/4` is admissible for this target: the closed tubes are
embedded solid tori, disjoint exactly when `rho < pi/4`, and the margins
below are positive on `(0, pi/4)`.

- Clearance: on the closed complement of the open tubes,
  `sin rho <= |w2| <= cos rho`, and `|f| = |w1||w2| =
  sin(theta)cos(theta)` is minimized at the tube boundaries, so
  `m(rho) = sin(rho)cos(rho) = sin(2 rho)/2`.
- Transversality: for any unit covector `u in R^2`, the `C^2`-gradient of
  `Re(u* f)` is `(conj(u* w2), conj(u* w1))` with Euclidean norm `1`; its
  radial component at `w` is `2 Re(u* f(w))`, of magnitude `<= 2|f(w)|`.
  Restricted to `T_w S3` the covector therefore has norm
  `>= sqrt(1 - 4|f(w)|^2)`, giving the pointwise bound
  `sigma_2(d(f|S3))(w) >= sqrt(1 - sin^2(2 theta)) = |cos(2 theta)|`
  and hence `sigma(rho) >= cos(2 rho)` on both tubes. ∎

So for `|1,1>` the theorem's radius specializes to

```
eps0(|11>) >= sup over admissible rho < pi/4 and h > 0 of
              min( sin(2 rho) e^{-1/2} / 2,  cos(2 rho) h e^{-(1+h)^2/2} / sqrt(2) ),
```

a strictly positive explicit number (the right-hand side is a sup of a
continuous function on the open admissible set; `run.py` records
`eps0_cert(|11>)` on the declared `(rho, h)` grid per §3, never claiming
the sup is attained). Its value, the optimizing
`(rho, h)`, and the fidelity form are computed in `run.py` and recorded
in `isotopy_stability.json` only.

## 5. Consequence for the coherent dictionary (claim S5)

**S5 (explicit `D_coh, K<=2` gap at `|1,1>`; proved here, conditional
only on exp24 P3).** Every `K <= 2` coherent superposition has a zero
link on `S3_1` with no linked pair (exp24 P3, proved). The Hopf link has
a linked pair. Hence no `K <= 2` coherent state can lie within
phase-aligned distance `eps0(|11>)` of `|1,1>`:

```
sup over D_coh, K<=2 of F <= (1 - eps0(|11>)^2 / 2)^2,
```

the fidelity form of `delta >= eps0`. The runnable form substitutes
`eps0_cert(|11>) <= eps0(|11>)`, certifying the weaker bound
`F <= (1 - eps0_cert^2 / 2)^2`; only that certified form is evaluated
and recorded (E4). This is exp24 P5's conclusion with
an explicit constant and with the tube/degree sketch replaced by S3's
proof; P5's own row in exp24 §4 stays untouched until this memo passes
review (single-authoring-location discipline — the status change, if
accepted, is a follow-up edit there, not here).

Scope table for every claim above:

| ID | Modes | Sphere | Dictionary scope | What it quantifies over |
| --- | --- | --- | --- | --- |
| S1 | 2 | any `w` | none (any two states) | exact bound |
| S2 | 2 | `|w0| <= 1` | none | exact bound |
| S3 | 2 | `r = 1` | none (any perturbing state) | regular targets with margin data |
| S4 | 2 | `r = 1` | none | target `|1,1>` only |
| S5 | 2 | `r = 1` | `D_coh`, `K <= 2` | fidelity sup bound |

## 6. Numerical blocks and falsification gates

All verdict booleans are computed from data in `run.py` (AGENTS.md).
Grid standards and caps follow the exp24 census toolkit and are recorded
in diagnostics.

- **E1 (margin referee; one-sided contract).** Evaluate `|f_T|` on a
  declared grid of the closed tube complement, and `sigma_2(d(f_T|S3))`
  on a declared grid of `U_rho`, for `|1,1>`. A grid minimum over a
  subset can only sit **at or above** the true minimum, so the defect
  test is one-sided. Alarm `F1` (halt, tool defect): any grid sample
  strictly below its proved bound minus the declared numerical
  tolerance — `|f_T| < sin(2 rho)/2 - tol` at a sample outside the open
  tubes, or `sigma_2 < |cos(2 theta)| - tol` at any sample (either
  contradicts §4's proofs). The excess of the grid minima above the
  closed forms is recorded as a refinement diagnostic at the declared
  resolutions; it is expected, and is not an alarm.
- **E2 (constant evaluation).** Search admissible `(rho, h)` on a
  declared grid and record `eps0_cert(|11>)` (§3: the attained min for
  the best pair, a lower bound on `eps0(|11>)`), its fidelity form, and
  the certifying pair. The closed forms of §4 make each grid pair's min
  exactly evaluable, so this value is certified, unlike E5's. Alarm
  `F2`: `eps0_cert <= 0` or admissibility infeasible — record, halt
  interpretation (no physics conclusion).
- **E3 (tightness probe; measured, not predicted).** Pre-declared search
  contract with the constants fixed here. Probe directions `v`:
  - (i) coherent-kernel directions (S1's equality direction — the worst
    case of the C^0 bound) at the 8 declared sphere points
    `(w1, w2) = (e^{ia} cos(t0), e^{ib} sin(t0))` for
    `t0 in {pi/8, 3pi/8}` and `(a, b) in {0, pi/2}^2`;
  - (ii) 24 random perturbation directions: complex-Gaussian Fock
    coefficients at cutoff `12` per mode, seed `137028`, projected
    orthogonal to `T` and unit-normalized;
  - (iii) the best-found state of exp25's `|11>/D_coh/K=2` cell as an
    endpoint direction.
  Census change along a direction is **not assumed monotone** in
  `delta` — a link can break and re-form — so bisection alone is not a
  valid search. For each `v`, unit states `psi(s) = normalize(T + s v)`
  are scanned on the ascending declared lattice
  `delta in {0.02 k : k = 1, ..., 70}` (top of lattice `1.40 < sqrt 2`)
  against the standard exp24 census grid; `delta_break(v)` is the
  **first** census-changing lattice value, refined by bisection to
  absolute tolerance `1e-3` inside the single bracketing interval
  `[0.02(k-1), 0.02 k]`. This yields a lattice-resolution-limited,
  best-found **upper** bound on the breaking radius in that direction;
  it asserts nothing about un-probed `delta` values above
  `eps0_cert` (below `eps0_cert`, census constancy is S3's theorem —
  exactly what gate F3 tests). Recorded per direction: `delta_break`,
  the census at first change, the lattice index; plus the overall
  minimum and all ratios to `eps0_cert`. Same best-found discipline as
  exp25; no minimality claim.
  Gate `F3` (blocking): any probed state with `delta < eps0_cert` whose
  census differs from the Hopf link at census standards — theorem or
  census defect; halt all interpretation of this experiment and report
  before any further claim.
- **E4 (exp25 consistency).** Evaluate the certified fidelity bound
  `F <= (1 - eps0_cert^2 / 2)^2` — the exact inversion of
  `delta^2 = 2(1 - sqrt(F))` at `delta = eps0_cert` (well-defined since
  `eps0_cert <= sqrt(2)` for unit states; §5's runnable form) — and
  compare with the measured best-found fidelity of exp25's
  `|11>/D_coh/K=2` cell (read from `topological_kcurves.json`, never
  restated). Gate `F4` (blocking): measured best-found exceeds this
  certified bound — contradiction between a proof and a measurement;
  halt and report.
- **E5 (trefoil margins; numerically supported only).** Compute grid
  margins `m(rho)`, `sigma(rho)` for the exp25 trefoil target
  `0.8|20> + 0.6|03>` and record the induced `eps0_cert`-style value.
  Unlike E2, the margins themselves are grid evaluations without closed
  forms, so the result is **numerically supported only, not certified**
  (a grid minimum over-estimates the true margin, in the unsafe
  direction); the JSON field is named to say so. No dictionary gap is
  claimed for the trefoil here (that needs P6's winding bound, still
  sketch).

## 7. Claim table

One row per claim; empty cells would be visible. This table is the sole
authoring location for exp28 statuses.

| ID | Claim (headline) | Status | Basis |
| --- | --- | --- | --- |
| S1 | kernel sup bound with sharp constant | proved here | §2 |
| S2 | derivative bound `c1(h)` | proved here | §2 |
| S3 | margins + `(C0, C1)` imply ambient-isotopic zero link | proved here | §3 |
| S4 | `|11>` margins: `m = sin(2rho)/2`, `sigma >= cos(2rho)` | proved here | §4 |
| S5 | explicit `D_coh K<=2` fidelity gap at `|11>` | proved here (uses exp24 P3) | §5 |
| N1 | no grid sample below the proved closed-form bounds (one-sided referee) | numerical, E1 | run |
| N2 | `eps0_cert(|11>) > 0` evaluated, fidelity form recorded | numerical, E2 | run |
| N3 | no census change below `eps0_cert` in any probe; per-direction first-change `delta_break` and ratios recorded | numerical, E3 | run |
| N4 | certified S5 bound consistent with exp25 measured cell | numerical, E4 | run |
| N5 | trefoil margin estimate (numerically supported, not certified) | numerical, E5 | run |

Epistemic discipline: "proved here" means proved in this pre-declaration
memo and not yet independently reviewed; no certified-lower-bound
language is used anywhere until Gate T′ closes (issue #137 scope rule —
"certified" in E2/E4 qualifies only the internal `eps0_cert` semantics
of §3, not a Gate-T′-level certified-lower-bound claim). Exp24's claim
table is not edited by this experiment; any status promotion there (P5)
is a separate reviewed change. `eps0_cert` values are bounds from below
on `eps0`, itself a bound from below on the breaking radius — never
estimates of either.

Review record: the revisions of 2026-08-02 (min/inf and sup semantics,
admissible-`rho` definition, core-winding scope, E4 fidelity form,
`eps0`/`eps0_cert` separation, E1 one-sided contract, E3 constants and
non-monotonicity handling, and the boundaryless-extension step in S3's
Ehresmann argument) reflect findings of the report-only independent
re-reviews on PR #151, relayed and approved by orange. orange is the
decision authority for adoption, not the author of the findings;
per-finding attribution lives in the PR #151 thread.
