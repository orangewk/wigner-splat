# Experiment 26 — Gaussian-group action on stellar zero links: derivation and pre-declared predictions

Status: issue #137 Gate T′, first slice. Opened in response to the 管理役
comment of 2026-07-31 on #137 (指摘 2: is the zero-link topology invariant
under the **full** Gaussian unitary group, or only under passive linear
optics?). This memo is written and committed **before** `run.py` results are
interpreted; the propositions below are the pre-declared predictions, and the
falsification conditions in §6 are fixed here. Measured numbers live only in
`gauss_invariance.json`; this memo contains none.

Headline (proved below, then measured): the answer to 指摘 2 splits.

- At any **fixed radius** the link is *not* a full-Gaussian invariant: an
  explicit Gaussian unitary removes the Hopf link of `|1,1>` from the unit
  sphere (G1/G2, with a clean threshold `lam* = sqrt(2) - 1`).
- What survives the full group is the link's germ **at infinity**: the
  multiplicity partition of the top homogeneous part of the stellar
  polynomial is invariant under every Gaussian unitary (G3), refining the
  Gaussian invariance of the stellar rank (the partition sums to the rank).

指摘 3 of the same comment (isotopy stability — lifting zero-**count**
stability to link-**type** stability inside a fidelity ball) is **not**
addressed in this experiment; it stays open as Gate T′ sub-goal (a).

## 1. Conventions

Stellar function conventions are those of
`experiments/24_hopf_stellar/derivation.md` §1 (referenced, not restated),
including the recorded building block `f_{T(lam)} = sqrt(1-lam^2) exp(lam w1
w2)` for the two-mode squeezed vacuum, `lam = tanh rho`.

**Finite-rank (P, A, b) form.** Every state of finite stellar rank has

```
f(w) = P(w) * exp( (1/2) w^T A w + b^T w ),
```

with `P` a polynomial of total degree `d`, `A` complex symmetric with
operator norm `< 1` (normalizability), `b in C^2`. The degree `d` is the
stellar rank in the sense of the stellar hierarchy; only the degree itself,
defined internally by this representation, is used below — no external
content is load-bearing. The **top form** `P_top` is the total-degree-`d`
homogeneous part of `P`; as a binary form it factors over `CP^1` into `d`
roots with multiplicities, and the sorted multiplicity list is the
**top-form partition** of the state (e.g. `w1 w2` -> `(1,1)`;
`w1^2` -> `(2)`; `w2^3` -> `(3)`).

**Gaussian group.** Displacements, passive `U(2)`, single-mode squeezers
`exp((zeta/2) a_i^dag2 - h.c.)`, and the two-mode squeezer
`exp(zeta a1^dag a2^dag - h.c.)`; "Gaussian unitary" means any finite
product. Zero sets never see global phases or positive constants.

**Toolkit.** `wigner_splat/gaussact.py` implements the *exact* action of
each factor on `(P, A, b)` data via the closed forms of Lemma C; validated
in `tests/test_gaussact.py` against an independent Taylor series in the flow
parameter and against truncated-Fock brute force (matrix exponentials).
Censuses reuse `wigner_splat/stellar2.py` unchanged.

## 2. Propositions (pre-declared predictions)

### 2.1 G1 (closed form of the squeezed `|1,1>`; proved)

For real `rho > 0`, `lam = tanh rho`:

```
f_{T(rho)|11>}(w) = sech^3(rho) * ( w1 w2 - sinh(rho) cosh(rho) ) * exp( lam w1 w2 ).
```

*Proof.* In the Bargmann representation `a_i^dag = w_i ·`, `a_i = d/dw_i`.
From the Bogoliubov relations `T a_1^dag T^dag = a_1^dag cosh - a_2 sinh`
(and 1<->2), `T|11> = (T a_1^dag T^dag)(T a_2^dag T^dag) T|00>`, with
`f_{T|00>} = sech * exp(lam w1 w2)` (recorded convention, exp24 §1; it also
follows from `(T a_i T^dag) T|00> = 0`, a first-order PDE pinning the
exponent). Apply the two operators:

```
(w2 cosh - sinh d1) e^{lam w1 w2} = w2 (cosh - lam sinh) e^{...} = w2 sech e^{...},
(w1 cosh - sinh d2) [ w2 e^{lam w1 w2} ] = [ (cosh - lam sinh) w1 w2 - sinh ] e^{...}
                                        = [ sech * w1 w2 - sinh ] e^{...},
```

using `cosh - tanh*sinh = sech`. Collecting constants gives the display. For
complex `zeta = rho e^{i theta}` the constant becomes
`e^{i theta} sinh cosh` and `lam -> e^{i theta} tanh rho` (phase covariance
`a_i -> e^{i theta_i} a_i`); the modulus, which is all §2.2 uses, is
unchanged. ∎

### 2.2 G2 (fixed-radius links are NOT full-Gaussian invariants; proved)

Write `c(lam) = sinh(rho)cosh(rho) = lam / (1 - lam^2)`. The zero set of
`f_{T(rho)|11>}` is exactly the smooth conic `{w1 w2 = c(lam)}` (the
exponential factor is nowhere zero). On `S3_rad`, AM–GM gives
`|w1 w2| <= rad^2/2` with equality only at `|w1| = |w2|`. Hence:

- **`c(lam) > rad^2/2`:** the link `L_rad(T|11>)` is **empty**.
- **`0 < c(lam) < rad^2/2`:** by 24/P4b (proved) the link is two circles
  with linking number `+1` — the positive Hopf link.

Since `L_rad(|11>)` is the Hopf link on *every* sphere (24/P1), component
count and linking matrix at any fixed radius are **not** invariant under the
full Gaussian unitary group; the invariance scope of 24/P2 (passive) is
sharp. At `rad = 1` the threshold `c = 1/2` is `lam^2 + 2 lam - 1 = 0`, i.e.

```
lam* = sqrt(2) - 1  (≈ 0.4142),   equivalently  sinh(2 rho*) = 1.
```

Restoration: for every fixed `rho`, all spheres with `rad^2 > 2 c(lam)`
carry the Hopf link again (same P4b application) — the lost topology
persists "at infinity", which motivates G3. ∎

### 2.3 G3 (top-form partition is a full-Gaussian invariant; proved modulo Lemmas A/B)

**Statement.** For every finite-rank state and every Gaussian unitary `G`,
the top-form partition of `G psi` equals that of `psi`. In particular the
partition refines the stellar rank (its sum), which is Gaussian-invariant.

**Lemma A (factorization; standard, sketch in §A).** Up to a global phase,
every two-mode Gaussian unitary factors as
`G = D(alpha) U_post S_1(zeta_1) S_2(zeta_2) U_pre` with `U`'s passive and
`S_i` single-mode squeezers (Bloch–Messiah / Euler decomposition of the
symplectic part, lifted factor-by-factor). Global phases do not move zeros.

**Lemma B (disentangled factor action; standard, numerically pinned).** On
Bargmann functions, with `s = e^{i theta} tanh rho`, `mu = sech rho`:

```
S(zeta):  f  ->  sqrt(mu) e^{(s/2) w_i^2} [ e^{-(sbar/2) d_i^2} f ](w with w_i -> mu w_i),
T(zeta):  f  ->  mu e^{Lam w1 w2} [ e^{-Lambar d1 d2} f ](mu w1, mu w2),
D(alpha): f  ->  e^{alpha^T w - |alpha|^2/2} f(w - conj alpha),
passive:  f  ->  f(U w).
```

These are the standard normal-ordered (disentangled) forms; they are pinned
numerically to machine precision in `tests/test_gaussact.py` against
truncated-Fock matrix exponentials. (The two-mode form is included because
the toolkit implements it; Lemma A makes it redundant for generality.)

**Lemma C (Gaussian-conjugated heat flow; proved here).** Let `S` be a
symmetric 2x2 matrix, and let `F_s = exp( (s/2) d^T S d ) [ P e^Q ]` with
`Q = (1/2) w^T A w + b^T w`. If `det(I - u S A) != 0` for `u in [0, s]`,
then `F_s = P_s e^{Q_s}` with

```
A_s = A (I - s S A)^{-1},        b_s = (I - s A S)^{-1} b,
P_s(w) = gamma_s * [ H_{Sigma_s} P ]( (I - s S A)^{-1} (w + s S b) ),
Sigma_s = s (I - s S A)^{-1} S     (symmetric),
gamma_s = det(I - s S A)^{-1/2} exp( (s/2) b^T (I - s S A)^{-1} S b ),
```

where `H_Sigma P = sum_k (1/k!) ((1/2) d^T Sigma d)^k P` is a finite sum
that **strictly lowers degree** beyond its leading term.

*Proof.* Write `F_s = P_s e^{Q_s}` and match `d/ds F = (1/2) d^T S d F`:

```
(1/2) d^T S d (P e^Q) = e^Q [ (1/2) d^T S d P + (grad P)^T S (A w + b)
                              + (P/2) ( (A w + b)^T S (A w + b) + Tr(S A) ) ].
```

The exponent must satisfy the matrix Riccati system `A' = A S A`,
`b' = A S b`, `c' = (1/2) b^T S b + (1/2) Tr(S A)`, solved by the displayed
`A_s`, `b_s` (differentiate and use the push-through identity
`(I - sSA)^{-1} S = S (I - sAS)^{-1}`); the trace term integrates to
`-(1/2) log det(I - sSA)`, giving the determinant prefactor. The polynomial
then satisfies the transport–heat equation

```
d/ds P_s = (1/2) d^T S d P_s + (grad P_s)^T S (A_s w + b_s).
```

Substituting `P_s(w) = R_s(N_s w + n_s)` with `N' = N S A_s`, `n' = N S b_s`,
`N_0 = I, n_0 = 0` removes the transport term; the solutions are
`N_s = (I - s S A)^{-1}` and `n_s = s (I - sSA)^{-1} S b` (differentiate;
for `n_s` use `d/ds [ A^{-1}(I - sAS)^{-1} ] = (I - sSA)^{-1} S (I - sAS)^{-1}`
when `A` is invertible, then drop `A^{-1}` from the final expression and
extend to singular `A` by continuity). The remaining equation is a pure heat
flow `d/ds R = (1/2) d^T (N S N^T) d R` whose accumulated covariance is
`Sigma_s = int_0^s N_u S N_u^T du = s (I - sSA)^{-1} S` (same antiderivative
identity). Uniqueness inside the finite-dimensional family {polynomial of
degree <= d times a Gaussian} — where the flow is a polynomial ODE system —
closes the argument. ∎

**Corollary (top-degree transport).** In Lemma C the heat part lowers
degree, and the substitution is affine with invertible linear part `N_s`,
so `(P_s)_top = P_top ∘ N_s`. Every Lemma B factor therefore transforms
`P_top` by a nonzero scalar and an invertible linear substitution:
the heat step by `N_s` (its domain condition holds because
`|s| = tanh rho < 1` and `||A|| < 1` for a normalizable input, so
`||u S A|| < 1` along the path for both `S = E_ii` and the cross matrix,
which have unit operator norm; each full unitary factor returns a
normalizable state, restoring `||A|| < 1` for the next factor); the `mu`
scaling and the passive substitution are linear and invertible; the
translation in `D(alpha)` fixes top forms; the exponential prefactors touch
only `(A, b)`. Hence `P_top` transforms under any Gaussian unitary by
`P_top -> const * P_top ∘ L`, `L in GL(2, C)`, and the root multiplicity
partition of the binary form on `CP^1` — a `PGL(2)`-invariant — is
preserved. **G3 follows, modulo Lemma A (standard, sketch) and Lemma B
(standard, numerically pinned).** ∎

Consistency check against G1/G2: for `|1,1>`, `P_top = w1 w2` has partition
`(1,1)` at every `lam`, and indeed the Hopf link always reappears at large
radius (G2 restoration) even after it leaves the unit sphere.

### 2.4 G4 (the large-radius link realizes the top-form pattern; sketch)

For radii large enough (state-dependent), the census link should realize
the top-form data: a **squarefree** top form (all multiplicities 1) has `d`
branches asymptotic to `d` distinct complex lines, so the large-radius link
should be `d` circles pairwise linking `+1`. Multiplicities `> 1` carry
extra Puiseux data *not* determined by the partition alone — the trefoil
family `t|20> + s|03>` has top form `∝ w2^3` (partition `(3)`) yet its
large-radius link is the `(3,2)` torus knot (one component), not three
fibers. For `d = 2` the dichotomy is concrete: partition `(1,1)` means the
affine conic is a hyperbola (two components, linking `+1` — the P4b pattern
after a linear change of frame, which is however not unitary in general, so
this case is *also* sketch outside the exact P4b frame); partition `(2)`
means a degenerate direction — a parabola (one component) or a parallel
line pair (two components, linking `0`) — and **never** a `+1`-linked pair.
**Status sketch**; E5 measures it.

### 2.5 G5 (Gaussian non-equivalence of `|2,0>` and `|1,1>`; corollary of G3)

`|2,0>` has top-form partition `(2)`, `|1,1>` has `(1,1)`; both have rank 2.
By G3 no Gaussian unitary maps one to the other, even though the rank
alone cannot distinguish them: **the partition strictly refines the rank as
a Gaussian invariant**. E6 probes this adversarially: a seeded multi-start
optimizer maximizes `F(G|20>, |11>)` (and the reverse) over the Gaussian
group; G3 forbids `F = 1` exactly, so a best-found value numerically
indistinguishable from 1 (threshold pre-declared in §5 E6) would falsify
the G3 lemma chain. The supremum over the (non-compact) group is not
claimed to stay away from 1 — only exact attainment is excluded; whatever
best-found value appears is recorded descriptively.

## 3. Position in the charter

- **指摘 2 answered** (this experiment): at fixed radius the invariance
  group of the link is passive only (G2 — so exp25's same-frame,
  same-radius comparisons were the right design); widening to the full
  Gaussian group trades the fixed sphere for the germ at infinity and keeps
  a strictly-finer-than-rank invariant (G3).
- **指摘 3 not addressed**: isotopy stability inside a fidelity ball
  remains Gate T′ sub-goal (a); nothing here uses or claims it.
- Dictionary-boundedness questions (Gate T′ (c)) are untouched: this
  experiment is about the *group*, not the dictionaries.

## 4. Claim table

One row per claim; empty cells would be visible. This table is the **sole
authoring location** for exp26 epistemic status; the README's generated
block quotes Basis and On-violation verbatim from here.

| ID | Statement | Basis | On violation |
| --- | --- | --- | --- |
| G1 | `f_{T(rho)|11>} = sech^3 (w1 w2 - sinh cosh) e^{lam w1 w2}` | proved here (§2.1) | tool alarm; halt all downstream cells |
| G2 | fixed-radius link of `T|11>`: Hopf iff `0 < c(lam) < rad^2/2`, empty above; threshold `lam* = sqrt(2)-1` at radius 1; not a full-Gaussian invariant | proved here (§2.2; uses 24/P1 and 24/P4b) | tool/proof alarm; halt E2/E3 interpretation |
| G3 | top-form multiplicity partition invariant under every Gaussian unitary | proved here modulo Lemma A (standard, sketch §A) and Lemma B (standard, numerically pinned in tests) | E4 mismatch: halt; diagnose the lemma chain before interpreting anything downstream of it |
| G4 | large-radius link realizes the top-form pattern (squarefree: d fibers pairwise `+1`; multiplicity: extra Puiseux data; `d=2` dichotomy) | sketch (§2.4) | recorded as evidence against the sketch (interesting either way); no halt |
| G5 | no Gaussian unitary connects `|2,0>` and `|1,1>`; E6 best-found `F` stays below `1 - 1e-6` | corollary of G3 | alarm: numerically contradicts the G3 chain; halt |

## 5. Experiment plan (E-series; all seeds and grids fixed here)

Censuses use `stellar2.census` defaults unless stated; census failures
propagate as **indeterminate** (`None`) verdict components, never passes
(exp25 discipline). Fock cross-checks use the exact `(P, A, b)` recursion
(no truncation beyond float roundoff for single coefficients).

- **E1 (machinery gate).** (a) G1 constant: for `lam in {0.3, 0.5}`, the
  toolkit's `squeeze2(|11>, atanh lam)` polynomial must satisfy
  `-(const / w1w2-coeff) = sinh cosh` to rel `1e-12`. (b) Transformer vs
  truncated-Fock brute force (cutoff 36, low block `m,n <= 8`): max rel
  diff `< 1e-6` for one seeded Gaussian (seed 100) on `|1,1>` and on the
  trefoil state. This is the **F1 gate** for everything downstream.
- **E2 (fixed-radius threshold scan; G2).** `T(lam)|11>` census on radius 1
  at `lam in {0.30, 0.35, 0.40, 0.43, 0.46, 0.50, 0.60}` (margin
  `|lam - lam*| >= 0.014` — no cell near the tangency). Predicted: 2
  components + linking `+1` for `lam <= 0.40`; 0 components for
  `lam >= 0.43`. Verdict computed per cell from `c(lam) vs 1/2`.
- **E3 (radius restoration; G2).** `lam = 0.5`, `rad*(lam) =
  sqrt(2 c(lam)) = sqrt(4/3)`: censuses at `0.9 rad*` (predicted empty) and
  `1.2 rad*` (predicted Hopf, 2 components lk `+1`).
- **E4 (orbit partition invariance; G3).** States `|1,1>`, `|2,0>`,
  trefoil `0.8|20> + 0.6|03>`; 8 seeded Gaussians each
  (`random_gauss_params(seed)`, seeds `100..107`, `200..207`, `300..307`
  respectively; `r_max = 0.6`, `alpha_max = 1.0`). Predicted: top-form
  partition unchanged — `(1,1)`, `(2)`, `(3)` — with clustering ambiguity
  margin `>= 1e-2` where applicable; any margin below `10x` tolerance is an
  indeterminate cell, not a pass.
- **E5 (links at infinity; G4 sketch).** For the first two Gaussians of
  each E4 family: censuses at radii `{2.5, 3.0}` with `n_eta = 120`,
  `n_xi = 128`; the two radii must agree on (component count, linking
  multiset), else the cell is indeterminate. Predicted patterns:
  `|1,1>`-images 2 components lk `+1`; `|2,0>`-images classified from the
  transformed polynomial (data-computed classifier: quadratic-part matrix
  is rank-1 by G3; if the residual linear term is parallel to the doubled
  direction — parallel-line type — predict 2 components lk `0`, with an
  interpretability guard: split constant `>= 1e-3` relative to max
  coefficient, else indeterminate; otherwise parabola type — predict 1
  component); trefoil-images 1 component (windings recorded descriptively
  only — frame-fixed caveat of 24/P2 applies verbatim).
- **E6 (adversarial G5 probe).** Maximize `F(G|20>, |11>)` and
  `F(G|11>, |20>)` over the 14-parameter factorized family (squeezing
  magnitudes and displacement radii mapped through `1.2 tanh` of raw
  optimizer coordinates; phases free). Seeded multi-start Nelder–Mead
  (numpy-only, exp25-style): 24 random starts + 8 structured starts
  (identity neighborhood, pure-squeeze directions), `FIT_SEED = 20260731`.
  Fidelity is exact per point (coefficient extraction from the transformer;
  unitarity of the transformer is separately tested). Alarm iff best-found
  `>= 1 - 1e-6`; otherwise the value is recorded descriptively (best-found,
  never a supremum — the group is non-compact and no upper bound on the
  supremum is claimed).

## 6. Falsification conditions (fixed before running)

- **F1 (tool gate):** if E1 fails, the transformer is falsified and no
  downstream cell is interpretable until diagnosed; `run.py` halts after
  writing the E1 record.
- **F2 (proved-claim gate):** any E2/E3 census disagreeing with G2's
  prediction is a tool/proof alarm; halt interpretation (G2 is proved — a
  stable disagreement means the tracker or the proof chain is broken and
  the log must say which).
- **F3 (lemma-chain gate):** any E4 partition change (with unambiguous
  clustering) contradicts G3; halt and diagnose Lemma A/B/C before
  interpreting anything else.
- **F4 (sketch class):** E5 outcomes against G4 are recorded as evidence
  against the sketch; no halt.
- **F5 (adversarial alarm):** E6 best-found `>= 1 - 1e-6` is treated as
  numerical evidence against the G3 chain (same halt as F3). A large but
  sub-threshold best-found value is *not* evidence for G3 — it is recorded
  descriptively only.
- **Scope:** two modes, pure states, no measured data; censuses numerically
  supported, not certified (exp24 limits verbatim); same-environment
  reproducibility contract (exp25 discipline: seeds fixed, environment
  recorded in the JSON, UTF-8 console); no novelty language pending Gate S′
  (§7).

## 7. Prior-art risk (survey pending; Gate S′ discipline)

"Link at infinity" of a plane algebraic curve is a standard object in
singularity theory, and the Gaussian invariance of the stellar rank is
established in the stellar-formalism literature already listed in
`docs/kepsilon-note/note.md` §9. It is entirely plausible that G3 (or a
stronger form) is known in one of those clusters; per `AGENTS.md`, no
primary source was re-read for this memo and none is cited with content
claims. Until Gate S′ closes, this experiment claims only its
self-contained derivations and measurements, and the words "new" or
"novel" appear nowhere.

## Appendix A. Lemma A sketch

The symplectic matrix of a two-mode Gaussian unitary, in complex form
`a -> E a + F a^dag + alpha`, satisfies `E E^dag - F F^dag = I` and
`E F^T = F E^T`. A singular-value decomposition `F = V Sigma_F W^T` with
the constraints forces `E = V Sigma_E W^dag` on matching singular bases
with `Sigma_E^2 - Sigma_F^2 = I`: passive rotations `V, W` around a
diagonal core `diag(cosh r_i, sinh r_i)`, i.e. single-mode squeezers —
the Euler / Bloch–Messiah normal form, with the displacement commuted to
the outside at the cost of changing `alpha`. The metaplectic lift of each
factor is the standard operator written in Lemma B; lifts compose up to a
global phase, which no zero set and no `|overlap|` sees. This is standard
linear algebra plus the metaplectic covering; it is recorded as a sketch
because the operator-level bookkeeping is not re-derived line-by-line here,
and Lemma B is instead pinned numerically in the tests.
