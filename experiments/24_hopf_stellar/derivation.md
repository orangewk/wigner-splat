# Experiment 24 — stellar zero links on the phase-space 3-sphere: derivation and pre-declared predictions

Status: exploratory side-track (no issue; approved conversationally by orange
on 2026-07-30 with an explicitly light scope). This memo is written and
committed **before** `run.py` results are interpreted; the propositions below
are the pre-declared predictions, and the falsification conditions in §6 are
fixed here. Measured numbers live only in `hopf_link_results.json`; this memo
contains none.

Motivation. The K_ε theory note (`docs/kepsilon-note/note.md`) certifies
one-mode lower bounds on approximate rank over its **restricted** bounded
common-squeezing dictionary (note §2.2, row D2) by **counting** robust zeros
of a state's stellar function; for the unrestricted quantity (row D1) the
note claims no disk-zero bound. In two modes the zero set of the stellar
function is a complex curve; its intersection with a phase-space 3-sphere is a
closed 1-dimensional curve system — a **link**. Links carry more than a count:
components can wind and be mutually linked, the simplest nontrivial case being
the Hopf link (the fibers of the Hopf fibration `S^3 -> S^2`). This memo asks
whether that topology is (a) computable, (b) partially invariant under
passive linear optics (see P2 for the exact scope — component count and
linking are; core windings are not), and (c) an obstruction **candidate**
against the specific dictionaries fixed in §1 (`D_coh`, `D_G`) at fixed term
budget `K` — a **restricted-dictionary topological K–ε obstruction program**,
the 2-mode sibling of the note's restricted-dictionary zero counting. No
bound on unrestricted Gaussian rank (or on the unrestricted `K_ε` of the
note's row D1) is claimed anywhere in this memo. One mode counts zeros; two
modes can also link them.

## 1. Conventions

Stellar function of `|psi> = sum c_mn |m,n>`:

```
f_psi(w1, w2) = sum_mn c_mn w1^m w2^n / sqrt(m! n!),        entire on C^2,
<gamma1, gamma2 | psi> = exp(-(|gamma1|^2+|gamma2|^2)/2) f_psi(conj gamma1, conj gamma2).
```

Zeros of the Husimi function correspond to zeros of `f_psi`. Building blocks
(all equalities up to stated constants, which never move zeros):

- Two-mode coherent `|g1, g2>`: `f = exp(g1 w1 + g2 w2) * exp(-(|g1|^2+|g2|^2)/2)`.
- Two-mode squeezed vacuum `T(lam)`, `lam = tanh r in (-1, 1)`:
  `f = sqrt(1-lam^2) * exp(lam w1 w2)`.
- **Coherent dictionary** `D_coh`: stellar terms `z * exp(linear in w)`.
- **Pure-Gaussian dictionary** `D_G`: stellar terms `z * exp(affine quadratic in w)`
  (displaced squeezed two-mode pure states; `D_coh` is the linear-exponent
  subfamily). A `K`-term state is `f = sum_{k<=K} z_k exp(q_k(w))`. Pure-state
  superpositions only; no mixed states anywhere in this experiment.

These dictionaries are fixed per-experiment families in the spirit of the
note's restricted-dictionary approach; all results below are per-dictionary,
per-`K` statements. `D_G` as defined here carries **no** squeezing bound, so
it is not the note's §2.2 bounded common-squeezing dictionary, and no
equivalence is claimed (dictionary alignment is a Gate T′ design item,
issue #137).

Sphere `S3_r = {|w1|^2 + |w2|^2 = r^2}`; the census sphere is `r = 1` unless
stated. The **zero link** is `L_r(psi) = f_psi^{-1}(0) ∩ S3_r`. Each component
is oriented by the **boundary orientation** induced from the complex
orientation of the analytic curve piece inside the ball (outward-normal-first
convention). Recorded quantities:

- number of components;
- per-component **core windings** `(m1, m2)` = winding of `arg w1` / `arg w2`
  along the component (equal to the linking numbers with the two core great
  circles `{w1=0} ∩ S3`, `{w2=0} ∩ S3` when the component avoids them).
  These are **frame-fixed** quantities: they reference the state's own
  coordinate cores and are not passive invariants (P2);
- the pairwise **linking matrix** of the components.

The overall sign convention (ambient `S^3` orientation) is fixed once in code;
only relative signs across states are claim-bearing.

## 2. Propositions (pre-declared predictions)

**P1 (Hopf link of |1,1>; proved).** `f_{|11>} = w1 w2`. The zero set is the
union of the two transverse complex lines `{w1=0}` and `{w2=0}`; on every
`S3_r` this is two great circles. Their linking number is `+1`: the two disks
they bound inside the ball (the line pieces) meet exactly at the origin,
transversally, and complex submanifolds intersect positively, so the boundary
linking number equals `+1`. `L_r(|11>)` is the positive Hopf link for every
`r > 0` — literally two fibers of the Hopf fibration.

**P2 (passive invariance — corrected scope; proved as a variable-change
statement).** A linear unitary substitution `w -> U w`, `U in U(2)`, sends
stellar functions to stellar functions of passively transformed states (beam
splitters and phase shifters; the `U`-versus-`U^T` bookkeeping between state
and substitution is not used anywhere below). It fixes every `S3_r` and maps
zero sets diffeomorphically to zero sets, preserving complex orientations.
Hence **component count and the pairwise linking matrix** are invariant under
passive linear optics. **Core windings are NOT**: they are linking numbers
with the *fixed* coordinate cores, which a generic `U` moves — e.g.
`f = w1 + w2` has winding `(1, 1)` but a 50:50 beam splitter carries it to
`sqrt(2) w1`, whose zero circle is the core `{w1 = 0}` itself, windings
`(·, 1)`. Windings are invariant only under per-mode phase rotations and are
swapped by mode exchange. They remain well-defined *per state in its own
frame* — the census's internal random frame is transported back before
windings are read off — and every use below (the trefoil family in P6, the
E-series checks) compares target and approximant **in one common frame**,
which fidelity comparisons respect since both dictionaries are closed under
passive transformations. *(Corrected during PR #136 review: the original
draft wrongly listed core windings among the passive invariants.)*
Displacements and squeezers act affinely/nonlinearly on `w` and do **not**
fix the spheres; no invariance is claimed for them.

**P3 (coherent K<=2 states cannot link; proved).** Let
`f = z1 exp(l1) + z2 exp(l2)` with `l1, l2` affine linear, `z1 z2 != 0`. Then
`f = 0` iff `l(w) := l2(w) - l1(w) = log(-z1/z2) + 2 pi i n`, `n in Z`: the
zero set is a countable family of **parallel affine complex lines**. A complex
line meets a round `S3_r` in one round circle or not at all, so every
component sits on its own level `{l = c_n}`. For components on distinct levels
`c != c'`, the linking number is the winding of `arg(l(w) - c')` along the
curve in `{l = c}` — the winding of the nonzero constant `c - c'` — which is
`0`. (`K = 1` and degenerate cases have no zeros at all.) **Corollary:** no
`K <= 2` superposition from `D_coh` has a linked pair in its zero link, on any
sphere.

**P4 (TMSV odd cat carries the exact Hopf link at every squeezing; proved).**
`|C(lam)> ∝ T(lam) - T(-lam)` has `f ∝ sinh(lam w1 w2)`, zero set
`{w1 w2 = i pi n / lam}`. On the unit sphere `|w1 w2| <= 1/2 < pi/lam` for all
`lam in (0,1)`, so only `n = 0` contributes:

```
L_1(C(lam)) = {w1 w2 = 0} ∩ S3  =  L_1(|11>)   exactly, for every lam.
```

Fidelity to the target, from `<11|T(lam)> = sqrt(1-lam^2) lam` and
`<T(lam)|T(mu)> = sqrt((1-lam^2)(1-mu^2)) / (1 - lam mu)`:

```
||T(lam) - T(-lam)||^2 = 2 - 2 (1-lam^2)/(1+lam^2) = 4 lam^2 / (1+lam^2),
F(C(lam), |11>) = [4 lam^2 (1-lam^2)] / [4 lam^2/(1+lam^2)] = 1 - lam^4.
```

So `D_G` reaches `|11>` at `K = 2` (as `lam -> 0`) with the target's zero
topology **held exactly along the whole path**. Together with P3 this
separates the dictionaries at `K = 2`: squeezing is what buys the link.

**P4b (smooth conic pairs are Hopf-linked; proved at the homology level).**
For `0 < |c| < r^2/2` the smooth conic `{w1 w2 = c}` meets `S3_r` in two
circles `gamma_+` (large `|w1|`) and `gamma_-` (small `|w1|`), the boundary of
an annulus in the ball. With boundary orientations, core windings are
`(+1, -1)` for `gamma_+` and `(-1, +1)` for `gamma_-`, and
`lk(gamma_+, gamma_-) = +1`: `gamma_-` lies in the solid torus
`{|w1| <= r/sqrt2}` homologous to `+[core_1]`, `gamma_+` in the complementary
solid torus homologous to `+[core_2]`, and `lk(core_1, core_2) = +1`;
meridional corrections bound disks disjoint from the other curve and
contribute `0`. Such pairs appear for generic-phase TMSV cats
`T(lam) - e^{i phi} T(-lam)` whose zero levels miss `0`.

**P5 (topological fidelity gap: coherent K<=2 versus |1,1>; sketch).**
Bargmann reproducing-kernel bound: `|f_psi(w) - f_phi(w)| <= ||psi - phi|| *
exp(|w|^2/2)`. If coherent `K <= 2` states approached `|11>` in norm, their
stellar functions would converge uniformly on the closed unit ball to
`w1 w2`; inside disjoint solid-torus tubes around the two Hopf circles of
`L_{1/2}(|11>)`, the argument principle on transverse disks then forces zero
curves carrying winding `1` around each tube core, and two such curves in
complementary Hopf tubes have linking `+1` — contradicting P3. Hence there is
an `eps0 > 0` with `sup F <= 1 - eps0` over `K <= 2` coherent superpositions.
The tube/degree step is standard but not written out, and no explicit `eps0`
is computed here: **status sketch**, with numerical support delegated to E4.

**P6 (conic winding bound; the trefoil needs more than Gaussian K=2; sketch).**
For a `K = 2` state from `D_G`, the same reduction as P3 makes the zero set a
level family `{Q = c_n}` of one affine quadratic `Q`. Each component lies on
an affine conic, and its winding around a core circle equals the positive
count of intersections of the analytic piece it bounds with that core line —
at most the Bezout number `deg Q * deg(line) = 2`. So every component of a
Gaussian `K = 2` zero link has `|m1| <= 2` and `|m2| <= 2`, on every sphere.
The **trefoil family** `f = t w1^2/sqrt2 + s w2^3/sqrt6` (states
`t|20> + s|03>`, `ts != 0`) has, on every sphere, a single zero component
with winding pair `(m1, m2) = (3, 2)` up to convention (from the
weighted-homogeneous monodromy `w1^2 ∝ w2^3`; the curve meets a core only at
the origin, which is off-sphere). Winding `3 > 2` is topologically
inaccessible to Gaussian `K = 2`, predicting (via a P5-style stability step,
also not written out) a fidelity gap **one dictionary level above** the |11>
obstruction: `|11>` separates `D_coh` from `D_G` at `K = 2`; the trefoil
family separates `D_G` at `K = 2` from larger budgets. **Status sketch.**

**R1 (three-chain remark; conditional sketch).** `|30> + |03>` has three
mutually `+1`-linked great circles (three lines, pairwise transverse at the
origin). For Gaussian `K = 2`, cross-level linking sums to zero over a level
(P3 argument with `Q`), so three pairwise `+1` components would need a level
carrying `>= 3` components. Whether a conic level can meet `S^3` in three or
more circles is not settled here; the census records component counts per
family, and the remark stays conditional on that observed premise.

**Q1 (open; measured, not predicted).** Coherent `K = 3` against `|11>`:
`f = 1 + a exp(u.w) + b exp(v.w)` with `u` not parallel to `v` is no longer a
level family of one function, and none of the arguments above apply. E4
records the best-found fidelity and the zero census of the optimized state.
No prediction is declared; whatever appears is recorded.

## 3. Why this connects to the K–ε program

The note's one-mode robust-zero bound (its Theorem B′) certifies approximate
rank **over the restricted bounded common-squeezing dictionary** (note §2.2,
row D2) from zeros that **survive an ε-ball**; it does not bound the
unrestricted quantity (note row D1). Linking is the topological form of that
robustness: a linked pair cannot be unlinked by any perturbation that keeps
the curves disjoint — the link can only die by zeros colliding or leaving the
sphere, which is exactly the event a K–ε curve tracks. The ladder is:

| modes | zero set on sphere | invariant | certificate style |
| --- | --- | --- | --- |
| 1 | points in the disk | count | note §4–5 (certified there for the restricted bounded common-squeezing dictionary only; unrestricted: no disk-zero bound, note row D1) |
| 2 | link in `S^3` | count + windings + linking matrix | this memo (P3/P5/P6: proved/sketch) |
| n>=3 | real (2n-3)-dimensional manifolds in `S^{2n-1}` (Milnor links; for n=3, 3-manifolds in `S^5` — dimension corrected 2026-08-02 to match the #137 Gate L correction, an earlier draft said "surfaces") | not touched here | open |

## 4. Claim table

One row per claim; empty cells would be visible.

| ID | Claim (headline) | Modes | Dictionary / family | Sphere scope | Status |
| --- | --- | --- | --- | --- | --- |
| P1 | `L_r(|11>)` = positive Hopf link | 2 | target state | every `r` | proved here |
| P2 | component count + linking matrix passive-invariant; core windings frame-fixed, NOT passive-invariant | 2 | any state | every `r` | proved here (scope corrected in review) |
| P3 | coherent `K<=2`: parallel lines, no linked pair | 2 | `D_coh`, `K<=2` | every `r` | proved here |
| P4 | TMSV odd cat: exact Hopf link, `F = 1 - lam^4` | 2 | `D_G`, `K=2` | `r = 1` (link claim), fidelity global | proved here |
| P4b | smooth conic pair: windings `(±1,∓1)`, `lk = +1` | 2 | conic zero families | `|c| < r^2/2` | proved here (homology level) |
| P5 | fidelity gap `D_coh, K<=2` vs `|11>` | 2 | `D_coh`, `K<=2` | ball `r<=1` argument | sketch + E4 numeric |
| P6 | conic winding `<=2`; trefoil blocked for `D_G, K=2` | 2 | `D_G`, `K=2` | every `r` | sketch |
| R1 | three-chain blocked for `D_G, K=2` | 2 | `D_G`, `K=2` | every `r` | conditional sketch |
| Q1 | coherent `K=3` vs `|11>` behavior | 2 | `D_coh`, `K=3` | `r = 1` | open, measured only |

## 5. Experiment plan (E-series)

All censuses run through one code path (`wigner_splat/stellar2.py`): a seeded
generic `U(2)` frame rotation (P2 makes this harmless and it moves curves off
coordinate degeneracies), phase-winding zero-face detection on a Hopf-angle
grid, curve tracing, canonical boundary orientation from the local complex
tangent, core windings, and a signed linking matrix from projected crossing
counts. The census is **numerically supported, not certified**: curves thinner
than the grid are invisible, and completeness near the excluded coordinate
cores is checked only by a `|f|` floor heuristic (same epistemic tier as the
note's sampled columns).

- **E1 validation:** `|10>+|01>`, `|11>`, `|20>+|02>` against P1/P2 exact
  predictions, including a second census under a different frame seed.
- **E2 knot ladder:** `|30>+|03>` (three-chain), `0.8|20>+0.6|03>` (trefoil
  windings `(3,2)` up to convention).
- **E3 dictionary probes:** TMSV odd cats `lam in {0.3, 0.6, 0.9}` (P4: exact
  Hopf census and `F = 1 - lam^4` against an independent Fock-truncation
  fidelity); a generic-phase TMSV cat with `|c_0| < 1/2` (P4b signs); a
  `cat ⊗ cat` coherent `K = 4` state large enough that satellite circles
  enter the sphere, with the cross-family linking pattern predicted
  geometrically in code (line intersection points inside/outside the ball).
- **E4 coherent fit ladder:** for `K = 1..4`, maximize fidelity to `|11>`
  over `D_coh` parameters (linear coefficients solved exactly through the
  Gram matrix; nonlinear parameters by seeded multi-start Nelder–Mead), then
  census the best state per `K`. Records the numeric shape of the P5 gap and
  the open Q1 cell.

## 6. Falsification conditions (fixed before running)

- **F1 (tool):** if any E1/E2/E3 census disagrees with a **proved** row of §4
  (component count, winding multiset, or linking matrix, up to the one global
  sign convention), the tracker is falsified and no downstream cell is
  interpretable until the disagreement is diagnosed in the log.
- **F2 (theory alarm):** a linked pair in any E4 `K <= 2` coherent census
  contradicts P3, which is proved; such an outcome is recorded as a tool or
  proof defect, never as a discovery.
- **F3 (sketch risk):** P5/P6 are sketches; E4 numbers can weaken them but a
  small measured gap does not certify them. No certified-lower-bound language
  may be attached to any E4 number.
- **Scope:** nothing here touches measured data, mixed states, or the note's
  certified one-mode theorems; no novelty is claimed pending a prior-art
  survey (§7).

## 7. Prior-art risk (survey pending)

Links of plane-curve singularities (torus knots from `w1^p + w2^q`) are
classical singularity theory; knotted vortex/zero lines are an established
topic in structured-light optics; stellar-rank robustness is established in
the references already recorded in `docs/kepsilon-note/note.md` §9. Per
`AGENTS.md`, none of these are cited here with specific content claims — no
primary source was re-read for this memo. Before any novelty language is used
for "linking as a restricted-dictionary K–ε obstruction", a Gate-S-style
survey must check at minimum: singularity-link literature, optical
vortex-knot literature, and
the stellar-formalism cluster. Until then this experiment claims only its
self-contained derivations and measurements.
