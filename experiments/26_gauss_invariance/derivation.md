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
- What survives the full group is the **multiplicity partition of the top
  homogeneous part of the stellar polynomial**: it is invariant under every
  Gaussian unitary (G3), refining the Gaussian invariance of the stellar
  rank (the partition sums to the rank). The partition is a strictly
  coarser datum than the link at large radius — multiplicities hide Puiseux
  data (§2.4) — so no invariance of the "link at infinity" itself is
  claimed; that reading is exactly the G4 sketch. *(Corrected during the
  PR #138 Sol audit: an earlier draft of this bullet said the link's "germ
  at infinity" survives, which overstates G3 and contradicts G4's own
  self-limitation.)*

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
carry the Hopf link again (same P4b application) — for this family the lost
topology persists at large radius, which motivates G3. ∎

### 2.3 G3 (top-form partition is a full-Gaussian invariant; proved modulo Lemmas A/B)

**Statement.** For every finite-rank state and every Gaussian unitary `G`,
the top-form partition of `G psi` equals that of `psi`. In particular the
partition refines the stellar rank (its sum), which is Gaussian-invariant.

**Lemma A (factorization; precise statement and proof in Appendix A).** Up
to a global phase, every two-mode Gaussian unitary factors as
`G = D(alpha) U_post S_1(r_1) S_2(r_2) U_pre` with `U`'s passive and `S_i`
single-mode squeezers with real `r_i >= 0` (Bloch–Messiah / Euler normal
form; the appendix handles degenerate singular values and `F = 0`, and the
operator-level phase is fixed by irreducibility). Global phases do not move
zeros. *(Upgraded from a sketch during the PR #138 Sol audit.)*

**Lemma B (disentangled factor action; standard, numerically pinned).** On
Bargmann functions, with `s = e^{i theta} tanh rho`, `mu = sech rho`:

```
S(zeta):  f  ->  sqrt(mu) e^{(s/2) w_i^2} [ e^{-(sbar/2) d_i^2} f ](w with w_i -> mu w_i),
T(zeta):  f  ->  mu e^{Lam w1 w2} [ e^{-Lambar d1 d2} f ](mu w1, mu w2),
D(alpha): f  ->  e^{alpha^T w - |alpha|^2/2} f(w - conj alpha),
passive:  f  ->  f(U w).
```

These are the standard normal-ordered (disentangled) forms. The
displacement and passive rows are proved by elementary arguments, and the
single-mode squeezer row is **proved on the finite-rank class** — the only
class G3 quantifies over — in Appendix B; all rows are additionally pinned
numerically to machine precision in `tests/test_gaussact.py` against
truncated-Fock matrix exponentials. (The two-mode form is included because
the toolkit implements it; Lemma A makes it redundant for the G3 proof
chain, so its analytic status is carried by the numerical pin plus the
independent G1 cross-check only.) *(Upgraded from "standard, numerically
pinned" during the PR #138 Sol audit.)*

**Lemma C (Gaussian-conjugated heat flow; proved here).** Let `S` be a
symmetric 2x2 matrix, and let `F_s = exp( (s/2) d^T S d ) [ P e^Q ]` with
`Q = (1/2) w^T A w + b^T w`, `s` complex. The flow parameter runs along the
straight segment `u = t s`, `t in [0, 1]`; if `det(I - t s S A) != 0` for
every `t in [0, 1]`, then `F_s = P_s e^{Q_s}` with

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
`||t s S A|| <= |s| ||A|| < 1` for every `t in [0, 1]` — both `S = E_ii`
and the cross matrix have unit operator norm, so `det(I - t s S A) != 0`
on the whole segment; each full unitary factor returns a normalizable
state, restoring `||A|| < 1` for the next factor); the `mu`
scaling and the passive substitution are linear and invertible; the
translation in `D(alpha)` fixes top forms; the exponential prefactors touch
only `(A, b)`. Hence `P_top` transforms under any Gaussian unitary by
`P_top -> const * P_top ∘ L`, `L in GL(2, C)`, and the root multiplicity
partition of the binary form on `CP^1` — a `PGL(2)`-invariant — is
preserved. **G3 follows from Lemmas A–C: A and B are proved in the
appendices (B on the finite-rank class, the only class G3 quantifies
over), and both are additionally pinned numerically in the tests.** ∎

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
a Gaussian invariant**. E6 is a **descriptive stress probe** of this
corollary: a seeded multi-start optimizer maximizes `F(G|20>, |11>)` (and
the reverse) over a magnitude-capped factorized subset of the group (§5
E6 — not the full non-compact group). G3/G5 exclude only the **exact**
attainment `F = 1`; since the supremum over the group is not claimed to
stay away from 1 and the searched family is capped, **no finite
best-found value can either support or refute G3** — whatever appears is
recorded descriptively, with no falsification gate attached. *(Corrected
during the PR #138 Sol audit: the original text declared a near-1
best-found value to be a numerical falsification of the G3 chain, which
is logically wrong for exactly the reasons just stated.)*

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
| G3 | top-form multiplicity partition invariant under every Gaussian unitary | proved here (§2.3 with Lemma C; Lemma A proved in Appendix A; Lemma B proved on the finite-rank class in Appendix B and pinned in tests) — status upgraded in the PR #138 Sol audit | E4 mismatch: halt; diagnose the lemma chain before interpreting anything downstream of it |
| G4 | large-radius link realizes the top-form pattern (squarefree: d fibers pairwise `+1`; multiplicity: extra Puiseux data; `d=2` dichotomy) | sketch (§2.4) | recorded as evidence against the sketch (interesting either way); no halt |
| G5 | no Gaussian unitary connects `|2,0>` and `|1,1>` | corollary of G3 | not experimentally testable here: E6 is a descriptive stress probe over a capped family and can neither support nor refute G3 (F5 gate removed in the PR #138 Sol audit) |

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
- **E6 (descriptive stress probe of G5).** Maximize `F(G|20>, |11>)` and
  `F(G|11>, |20>)` over the 14-parameter **magnitude-capped factorized
  family** (squeezing magnitudes and displacement radii mapped through
  `1.2 tanh` of raw optimizer coordinates, so magnitudes stay below 1.2;
  phases free). This family is a capped subset of the Gaussian group, NOT
  the full non-compact group, and every surface reports it as such.
  Seeded multi-start Nelder–Mead (numpy-only, exp25-style): 24 random
  starts + 8 structured starts (identity neighborhood, pure-squeeze
  directions), `FIT_SEED = 20260731`. Fidelity is exact per point
  (coefficient extraction from the transformer; unitarity of the
  transformer is separately tested). The best-found value is recorded
  descriptively only; **no falsification gate attaches** — see F5.
  *(Corrected during the PR #138 Sol audit: the original cell declared an
  alarm at best-found `>= 1 - 1e-6` treated as numerical evidence against
  G3; that alarm cannot falsify G3, which excludes exact attainment only,
  and the searched family is capped besides.)*

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
- **F5 (withdrawn during the PR #138 Sol audit):** as originally declared,
  E6 best-found `>= 1 - 1e-6` was to be treated as numerical evidence
  against the G3 chain, with a halt. That declaration was a logic error:
  G3/G5 exclude only the **exact** attainment `F = 1`, the supremum over
  the non-compact group is not claimed to stay below 1, and E6 searches a
  magnitude-capped family besides — so no finite best-found value can
  falsify (or support) G3. E6 therefore carries **no gate and no halt**;
  its value is recorded descriptively only. The original declaration is
  preserved here as the record of what was corrected.
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

## Appendix A. Lemma A: precise statement and proof

*(Rewritten during the PR #138 Sol audit; the earlier sketch did not treat
degenerate singular values, `F = 0`, or the operator-level phase.)*

**Statement.** Let `G` be a two-mode Gaussian unitary, i.e. a unitary with

```
G^dag a_i G = sum_j ( E_ij a_j + F_ij a_j^dag ) + alpha_i,      i = 1, 2,
```

where preservation of the commutation relations forces
`E E^dag - F F^dag = I` and `E F^T = F E^T` (both 2x2 identities). Then
there exist `V, W in U(2)`, `r_1, r_2 >= 0`, `beta in C^2`, `phi in R` with

```
G = e^{i phi} D(beta) U_V S_1(r_1) S_2(r_2) U_W,
```

`U_V, U_W` the passive unitaries with Bogoliubov matrices `V, W` (Appendix
B.2), `S_i(r) = exp((r/2)(a_i^dag2 - a_i^2))`. No nondegeneracy of the
squeezing spectrum is assumed, and `F = 0` (passive `G`) is the case
`r_1 = r_2 = 0`.

**Imported classical facts** (finite-dimensional linear algebra /
representation theory; used as named theorems, not re-derived):
(i) the Autonne–Takagi factorization — every complex **symmetric** matrix
`Lam` can be written `Lam = U_T T U_T^T` with `U_T` unitary and
`T = diag(t_1, t_2)` its singular values, with **no** nondegeneracy
hypothesis; (ii) irreducibility of the two-mode Fock (Weyl)
representation.

**Proof.**

1. *`E` is invertible*: `E E^dag = I + F F^dag >= I`, so all singular
   values of `E` are `>= 1`.
2. *`Lam := E^{-1} F` is symmetric with `||Lam|| < 1`*: symmetry — from
   `E F^T = F E^T`, `F^T = E^{-1} F E^T`, hence
   `Lam^T = F^T E^{-T} = E^{-1} F = Lam`. Norm — substituting `F = E Lam`
   into `E E^dag - F F^dag = I` gives `E (I - Lam Lam^dag) E^dag = I`, so
   `I - Lam Lam^dag = E^{-1} E^{-dag} > 0`, i.e. `||Lam|| < 1`.
3. *Takagi and the squeezing parameters*: write `Lam = U_T T U_T^T` (fact
   (i)); `t_1, t_2 in [0, 1)` by step 2. Set `r_i := artanh(t_i) >= 0`,
   `C := diag(cosh r_i)`, `S_h := diag(sinh r_i)`, so `T = C^{-1} S_h`.
4. *Construction of `V, W`*: take `W := U_T^dag` and `V := E U_T C^{-1}`.
   Then, composing Bogoliubov maps (apply `U_W`, then the squeezers, then
   `U_V`: `a -> W a`, then `a_i -> cosh(r_i) a_i + sinh(r_i) a_i^dag`,
   then `a -> V a`), the candidate `G' := U_V S_1 S_2 U_W` has Bogoliubov
   pair `(E', F') = (V C W, V S_h conj(W))`. Check the three identities:
   - `V` is unitary: step 2 gives `E^{-1}E^{-dag} = I - Lam Lam^dag`, and
     `Lam Lam^dag = U_T T U_T^T conj(U_T) T U_T^dag = U_T T^2 U_T^dag`
     (using `U_T^T conj(U_T) = I`), so `E^{-1}E^{-dag} = U_T C^{-2}
     U_T^dag` and `V V^dag = E U_T C^{-2} U_T^dag E^dag = E (E^{-1}
     E^{-dag}) E^dag = I`.
   - `E' = V C W = E U_T C^{-1} C U_T^dag = E`.
   - `F' = V S_h conj(W) = E U_T C^{-1} S_h U_T^T = E U_T T U_T^T
     = E Lam = F` (using `conj(W) = conj(U_T^dag) = U_T^T`).
5. *Displacement and phase*: `H := G (U_V S_1 S_2 U_W)^{-1}` now satisfies
   `H^dag a_i H = a_i + gamma_i` for some `gamma in C^2` (the linear parts
   cancel by step 4). Then `H D(gamma')^{-1}` for the matching
   displacement commutes with every `a_i` and (taking adjoints of the
   relation) every `a_i^dag`, hence with all Weyl operators; by fact (ii)
   it is a scalar, and unitarity makes it a phase `e^{i phi}`. Absorb the
   inversion into `beta`. ∎

## Appendix B. Lemma B: factor actions on Bargmann space

*(Added during the PR #138 Sol audit; previously only the numerical pin.)*

### B.1 Displacement (elementary, all Bargmann elements)

`[alpha a^dag, -conj(alpha) a] = |alpha|^2` is central, so the BCH series
terminates exactly: `D(alpha) = e^{-|alpha|^2/2} e^{alpha a^dag}
e^{-conj(alpha) a}`. In Bargmann representation `e^{alpha a^dag}` is
multiplication by `e^{alpha w}`, and `e^{-conj(alpha) a} =
e^{-conj(alpha) d/dw}` acts on every **entire** `f` as the translation
`f(w - conj(alpha))` — Taylor's theorem for entire functions, no growth
hypothesis needed. This is the Lemma B displacement row. ∎

### B.2 Passive rotations (elementary)

For `V in U(2)` define `(Gamma_V f)(w) := f(V w)`. The Bargmann inner
product `∫ conj(f) g e^{-|w|^2} dV(w)` is invariant under the variable
change `w -> V^dag w` (unimodular, `|w|^2`-preserving), so `Gamma_V` is
unitary. Chain rule gives `Gamma_V^{-1} a_i Gamma_V = sum_j V_ji a_j` and
the adjoint relation for `a_i^dag`: `Gamma_V` implements a passive
Bogoliubov pair `(E, F) = (V-transposed bookkeeping, 0)`, and every
passive pair arises this way up to the Appendix A phase argument. The
`V`-versus-`V^T` labeling is the bookkeeping caveat recorded in the
toolkit docstrings; no G3 step depends on it. ∎

### B.3 Single-mode squeezer (proved on the finite-rank class)

**Claim** (mode 1; mode 2 identical): for `zeta = rho e^{i theta}`,
`s = e^{i theta} tanh(rho)`, `mu = sech(rho)`, and every finite-rank
`f = P e^Q` with `||A|| < 1`,

```
e^{(zeta/2) a^dag2 - (conj(zeta)/2) a^2} f
   = sqrt(mu) e^{(s/2) w_1^2} [ e^{-(conj(s)/2) d_1^2} f ](mu w_1, w_2).
```

**Step 1 — the SU(1,1) matrix identity.** With `k_+ = [[0,1],[0,0]]`,
`k_- = [[0,0],[-1,0]]`, `k_0 = diag(1/2,-1/2)` (the defining rep of the
`K_+ = a^dag2/2, K_- = a^2/2, K_0 = (a^dag a + 1/2)/2` commutation
relations `[k_0, k_pm] = pm k_pm`, `[k_+, k_-] = -2 k_0`), direct 2x2
multiplication gives

```
e^{zeta k_+ - conj(zeta) k_-}            = [[cosh rho,            e^{i theta} sinh rho],
                                            [e^{-i theta} sinh rho, cosh rho          ]],
e^{s k_+} mu^{2 k_0} e^{-conj(s) k_-}    = [[mu + |s|^2/mu, s/mu],
                                            [conj(s)/mu,    1/mu]],
```

and the two agree entrywise (`mu + |s|^2/mu = (1 + sinh^2)/cosh = cosh`,
`s/mu = e^{i theta} sinh`, `1/mu = cosh`). So the disentangling holds
exactly in the defining representation.

**Step 2 — transfer to Fock space.** Finite Fock-support vectors are
analytic vectors for the quadratic generator `X = zeta K_+ -
conj(zeta) K_-` (Nelson's analytic-vector theorem for quadratic
Hamiltonians; imported classical fact), so `X` generates a unitary
one-parameter group and the su(1,1) relations exponentiate to a unitary
representation of the universal cover along continuous paths from the
identity. Both sides of the claim are the lifts, along the same path
`t in [0, 1] -> (s(t), mu(t)) = (e^{i theta} tanh(t rho), sech(t rho))`,
of the same SU(1,1) path (Step 1); lifts through the (double) cover along
a fixed continuous path from the identity are unique, so the operators
agree up to a `t`-independent phase fixed to `+1` at `t = 0`. On the
finite-rank class the right-hand side is exactly the toolkit's factor
action (heat step, scaling, quadratic prefactor — the domain condition
`||t s S A|| < 1` of Lemma C holds on the whole path), which is where G3
uses it. ∎

Tier note: B.3 imports two named classical facts (Nelson's theorem;
uniqueness of continuous lifts). Independently of B.3, the identical
formulas are pinned to machine precision against truncated-Fock matrix
exponentials in `tests/test_gaussact.py`, and the two-mode squeezer's
analogous form — not needed for the G3 chain after Lemma A — carries the
numerical pin plus the independent G1 cross-check only.
