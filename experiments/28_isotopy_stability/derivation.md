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

is a compact smooth 2-manifold with boundary only over `t in {0, 1}`,
and the projection `Z -> [0,1]` is a proper submersion (surjectivity of
`d_w(f_t|S3)` lets any `dt`-component be lifted). By the Ehresmann
fibration argument this is a product cobordism, giving a smooth isotopy
from `L_1(T)` to `Z(f_g) ∩ S3_1` inside `U_rho`; the isotopy extension
theorem (textbook input, declared: Hirsch, *Differential Topology*,
ch. 8) upgrades it to an ambient isotopy of `S3_1`. ∎

The resulting stability radius is

```
eps0(T) = sup over admissible rho and h > 0 of
          min( m(rho) * e^{-1/2},  sigma(rho) / c1(h) ),
```

a supremum (not claimed attained) over the admissible parameter set. Any
`delta < eps0(T)` lies below the min for some admissible `(rho, h)`, so
(C0) and (C1) hold for that pair and the link type is preserved. Every
admissible pair certifies its own min value as a valid stability radius;
`run.py` records the best certified value found, which lower-bounds
`eps0`, itself a lower bound on the true breaking radius — never an
estimate of it.

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
continuous function on the open admissible set; `run.py` records the
best certified value on a declared search grid, never claiming the sup
is attained). Its value, the optimizing
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

the fidelity form of `delta >= eps0`. This is exp24 P5's conclusion with
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

- **E1 (margin referee).** Evaluate `m(rho)` and the `sigma` lower bound
  for `|1,1>` on a declared grid over `S3_1` and compare with §4's closed
  forms. Alarm `F1`: relative mismatch beyond declared tolerance — halt,
  tool defect (closed forms are proved; a mismatch means code is wrong).
- **E2 (constant evaluation).** Search admissible `(rho, h)` on a
  declared grid and record the best certified stability radius (the
  attained min for the best pair — a lower bound on `eps0(|11>)`, per
  §3), its fidelity form, and the certifying pair. Alarm `F2`: best
  certified value `<= 0` or admissibility infeasible — record, halt
  interpretation (no physics conclusion).
- **E3 (tightness probe; measured, not predicted).** Pre-declared search
  contract. Probe directions `v`, fixed here: (i) the coherent-kernel
  direction at declared sphere points (S1's equality direction — the
  worst case of the C^0 bound), (ii) Fock-truncated random perturbations
  at a declared cutoff with a fixed seed recorded in `run.py`, (iii) the
  best-found state of exp25's `|11>/D_coh/K=2` cell as an endpoint
  direction. For each `v`, unit states `psi(s) = normalize(T + s v)` are
  scanned by bisection on the phase-aligned `delta` (declared tolerance
  and budget, recorded in diagnostics) against the standard exp24 census
  grid; `delta_break(v)` is the smallest census-changing `delta` that
  bisection finds in that direction. Recorded: per-direction
  `delta_break`, their minimum, and ratios to `eps0`. All are best-found
  **upper** bounds on the true breaking radius within the probed
  families — no minimality claim, same best-found discipline as exp25.
  Gate `F3` (blocking): any probed state with `delta < eps0` whose
  census differs from the Hopf link at census standards — theorem or
  census defect; halt all interpretation of this experiment and report
  before any further claim.
- **E4 (exp25 consistency).** Evaluate the S5 fidelity bound
  `F <= (1 - eps0^2 / 2)^2` — the exact inversion of
  `delta^2 = 2(1 - sqrt(F))` at `delta = eps0` (well-defined since
  `eps0 <= sqrt(2)` for unit states) — and compare with the measured
  best-found fidelity of exp25's `|11>/D_coh/K=2` cell (read from
  `topological_kcurves.json`, never restated). Gate `F4` (blocking):
  measured best-found exceeds the S5 bound — contradiction between a
  proof and a measurement; halt and report.
- **E5 (trefoil margins; numerically supported only).** Compute grid
  margins `m(rho)`, `sigma(rho)` for the exp25 trefoil target
  `0.8|20> + 0.6|03>` and record the induced `eps0` estimate. No closed
  form is claimed; status stays numerically supported, and no dictionary
  gap is claimed for the trefoil here (that needs P6's winding bound,
  still sketch).

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
| N1 | closed forms match grid margins | numerical, E1 | run |
| N2 | `eps0(|11>) > 0` evaluated, fidelity form recorded | numerical, E2 | run |
| N3 | no census change below `eps0` in any probe; per-family best-found `delta_break` and ratios recorded | numerical, E3 | run |
| N4 | S5 bound consistent with exp25 measured cell | numerical, E4 | run |
| N5 | trefoil `eps0` estimate | numerical, E5 | run |

Epistemic discipline: "proved here" means proved in this pre-declaration
memo and not yet independently reviewed; no certified-lower-bound
language is used anywhere until Gate T′ closes (issue #137 scope rule).
Exp24's claim table is not edited by this experiment; any status
promotion there (P5) is a separate reviewed change. `eps0` values are
bounds from below on the breaking radius, never estimates of it.
