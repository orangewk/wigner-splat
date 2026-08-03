# Experiment 30 — dictionary alignment: two-mode bounded and common-squeezing tiers, and certified-gap transfer (issue #137 Gate T′ sub-goal (c))

Status: adopted under orange's GO of 2026-08-02 (following the blanket
approval recorded on issue #137; the exp29 slice and the exp24 P6
promotion are merged prerequisites). This memo is written and committed
**before** any implementation or run output exists; the claims below are
pre-declared and the falsification gates in §8 are fixed here. Evaluated
numbers will live only in `dictionary_alignment.json` and the README
block generated from it; this memo contains formulas and closed forms,
never evaluated run output. Epistemic status lives **only** in §9's
claim table.

## 0. Scope and non-claims

This slice aligns the **definitions** of the repo's two-mode
dictionaries (exp24 §1: `D_coh`, `D_G`; exp25's operational bounded
family) with the K_ε note's restricted bounded common-squeezing
dictionary (`docs/kepsilon-note/note.md` §2.2, declaration rows D1–D2),
and transfers the repo's certified two-mode fidelity gaps down the
resulting inclusion ladder. Explicit non-claims, fixed here:

- Nothing here extends the note's **one-mode** certified theorems
  (Theorem B′ and rows D2–D3) to two modes; the note's multimode
  extension (its §8) stays open and untouched. The transfer results
  below rest on the repo's own two-mode topological chain (exp24 P3/P6,
  exp28 S3–S5, exp29 W4–W5), not on zero counting.
- No claim is made about the note's row D1 (one-mode unrestricted
  quantity), and no equivalence between one-mode and two-mode
  quantities is claimed anywhere.
- No novelty claims (Gate S′ survey remains open). The Gaussian normal
  form of §3 is standard material; what is recorded is the precise
  in-repo statement, its proof at the level the transfer needs, and its
  machine referee.
- Program-level "certified lower bound" language for the K–ε program
  remains withheld until orange closes Gate T′; this memo states
  slice-local theorems only.
- Pure states only; no mixed-state, ess-sup-roof, or channel statement
  of any kind.

## 1. Conventions

Reused by reference, not restated: exp24 §1 (stellar function `f_psi`,
dictionaries `D_coh` and `D_G`, spheres `S3_r`, zero link `L_r`),
exp26's `(P, A, b)` stellar data (`wigner_splat/gaussact.py`:
`f(w) = P(w) exp((1/2) w^T A w + b^T w)`, `A` complex symmetric 2x2,
`b in C^2`), exp28 §1's phase-aligned distance
`delta(psi, phi) = sqrt(2 (1 - sqrt(F)))`, and the note §2.1–2.2
(quantities `chi_G`, `K_eps^{G,F}`, the one-mode dictionary
`A(a, B)`).

Norms: `||A||` is the spectral (operator 2-)norm; `|b|`, `|alpha|` are
Euclidean norms on `C^2`. `bar(x)` is complex conjugation, applied
entrywise to vectors and matrices.

Squeezing-operator sign conventions differ between the note
(`S(xi) = exp[(xi* a^2 - xi a^dag^2)/2]`, giving one-mode
`a = -e^{i phi} tanh r`) and gaussact
(`exp[(zeta/2) a^dag^2 - (zeta*/2) a^2]`, giving `s = e^{i theta} tanh
rho`). The two conventions differ by `xi = -zeta` and produce the same
**set** of atoms at any given squeezing bound; every definition below is
stated on the `(A, b)` data itself, so it is convention-independent
(recorded again as part of A4).

## 2. The two-mode dictionary ladder (claim A0)

All tiers are sets of **normalized** pure two-mode states (statehood up
to global phase); `K`-term superpositions from a tier are states
proportional to `sum_{k<=K} z_k g_k` with atoms `g_k` in the tier.
Atom = state whose stellar function is `c exp((1/2) w^T A w + b^T w)`
with `A = A^T`, `||A|| < 1` (§3 proves this is exactly the pure
Gaussian states and that `||A|| < 1` is forced).

- **T_coh(B)** (bounded coherent): atoms with `A = 0`, `|b| <= B`.
  exp24's `D_coh` is the union over all `B` (no bound).
- **T_eq(A0, B)** (common-quadratic instance; the literal two-mode
  analogue of the note's `A(a, B)`): one fixed `A0` (`||A0|| <= a* <
  1`) shared by **every** atom of the instance — the full matrix is
  common, mirroring the note's "same a in modulus and angle" — and
  `|b_k| <= B`.
- **T_b(s*)** (bounded, per-atom-varying quadratic; exp25's operational
  family): atoms with `||A_k|| <= s* < 1`, `A_k` free per atom, `b_k`
  free. exp25 ran this tier with `s* = 0.98` (its committed
  `bounded_dictionary.quad_norm_max`; its Fock-tail discipline is a
  truncation implementation detail, recorded but not a tier).
- **D_G** (unrestricted; exp24 §1): atoms with any `||A|| < 1`, any
  `b`. (exp24's wording "no squeezing bound" means: no bound `s* < 1`
  imposed uniformly; individual physical atoms always have `||A|| < 1`
  by §3.)

**A0 (ladder).** For every `K`, every `B`, every `A0` with
`||A0|| <= s*`, and every `s* < 1`, the `K`-term superposition classes
nest:

```
T_coh(B)  ⊂  T_eq(0, B)-superpositions = bounded-coherent superpositions,
T_eq(A0, B)  ⊂  T_b(s*)  ⊂  D_G          (atom sets, hence K-term classes),
D_coh  ⊂  D_G.
```

Proof: immediate from the definitions — each inclusion only relaxes
constraints (`A_k = A0` fixed ⟹ `||A_k|| <= s*`; bounded ⟹
unbounded). `T_eq(0, B)` atoms are exactly `T_coh(B)` atoms. ∎

The tier table mirrors the note §2.4 rows: `T_eq` is the two-mode
sibling of row D2's dictionary; `D_G` is the two-mode sibling of the
*family column* of row D1 (the unrestricted pure-Gaussian
superpositions); `T_b` is strictly between and exists because exp25's
optimizer needed a compact search box. No quantity-level identification
with the note's one-mode rows is implied (non-claims, §0).

## 3. The Gaussian stellar normal form (claim A1)

**A1 (normal form, physical translation, and normalizability).**
(i) A normalized pure two-mode state is a pure Gaussian state (an
element of the metaplectic + displacement orbit of the vacuum,
equivalently `D(alpha) U_p S_1(r_1) S_2(r_2) |0>` by Bloch–Messiah)
**iff** its stellar function is

```
f_G(w) = c exp( (1/2) w^T A w + b^T w ),      A = A^T,  ||A|| < 1,
```

with `c != 0` (fixed up to global phase by normalization).
(ii) The parameters translate: the singular values of `A` are
`tanh r_1, tanh r_2` (the Bloch–Messiah squeezing parameters), and at
fixed `A` the displacement `alpha` and the linear coefficient `b`
determine each other by the invertible conjugate-linear pair

```
b = alpha - A bar(alpha),        alpha = (I - A bar(A))^{-1} (b + A bar(b)),
(1 - ||A||) |alpha|  <=  |b|  <=  (1 + ||A||) |alpha|.
```

(iii) If `||A|| >= 1` the function `exp((1/2) w^T A w + b^T w)` is not
the stellar function of any normalizable state.

Proof. *(i) construction direction.* `S_1 S_2 |0>` has stellar function
`prod_i (1 - |s_i|^2)^{1/4} exp((s_i / 2) w_i^2)` (single-mode squeezed
vacua; gaussact's `squeeze1` closed form, pinned in
`tests/test_gaussact.py`), i.e. `A = diag(s_1, s_2)`, `|s_i| = tanh r_i
< 1`. A passive `U` acts by the substitution `w -> U w` (exp24 P2,
gaussact `passive`), sending `A -> U^T A U` — same singular values —
and `b -> U^T b`. A displacement `D(alpha)` acts by gaussact's
`displace` closed form: `A` unchanged, `b -> b + alpha - A bar(alpha)`
(from `b = 0`: exactly (ii)'s map). All three factors keep the
polynomial part constant, so every pure Gaussian state has the stated
form with `||A|| < 1`.
*(i) converse.* Given `A = A^T` with `||A|| < 1`: by Autonne–Takagi,
`A = V Sigma V^T` with `V` unitary and `Sigma = diag(sigma_1, sigma_2)`,
`0 <= sigma_i = ||A||-ordered singular values < 1`. Take `r_i = artanh
sigma_i`, the passive substitution `U = V^T`, and the displacement
`alpha` of (ii); composing the three factors above produces a pure
Gaussian state with exactly the data `(A, b)`. Uniqueness of the state
up to phase: the stellar function determines the state (Fock
coefficients are its Taylor coefficients).
*(ii).* The map `alpha -> alpha - A bar(alpha)` has the stated inverse:
conjugating `b = alpha - A bar(alpha)` gives `bar(b) = bar(alpha) -
bar(A) alpha`, so `b + A bar(b) = (I - A bar(A)) alpha`, and
`||A bar(A)|| <= ||A||^2 < 1` makes `I - A bar(A)` invertible. The
sandwich follows from `|A bar(alpha)| <= ||A|| |alpha|` and the
triangle inequality. (This is verbatim the two-mode form of the note
§2.2's one-mode translation `b = alpha - a alpha*`,
`alpha = (b + a b*)/(1 - |a|^2)`; with `<n> = |alpha|^2 + sum_i
sinh^2 r_i` the instance is energy-bounded at fixed `(A0, B)`, and
neither equivalence is uniform as `||A|| -> 1` — same caveat, same
reason `a* < 1` is part of the definition.)
*(iii).* Displacements are unitary, so it suffices to rule out
`b = 0`. Passive substitutions preserve the Bargmann/Fock norm (they
implement passive unitaries on states — exp24 P2; exactness pinned in
exp26's tests), so by Takagi reduce to `A = diag(sigma_1, sigma_2)`,
`sigma_1 = ||A|| >= 1`. The squared Fock norm of
`exp((sigma/2) w^2)` in one mode is

```
sum_{n>=0} sigma^{2n} (2n)! / (4^n (n!)^2)  =  sum_n C(2n, n) (sigma^2/4)^n
                                            =  (1 - sigma^2)^{-1/2}
```

for `sigma < 1`, and the series **diverges** for `sigma >= 1` (its
terms are `C(2n,n) 4^{-n} sigma^{2n} ~ sigma^{2n} / sqrt(pi n)`).
The two-mode diagonal case is the product of the two one-mode series,
so it diverges whenever `sigma_1 >= 1`, and there is no normalizable
state with that stellar function. For `||A|| < 1` the same product
`prod_i (1 - sigma_i^2)^{-1/2}` is the finite squared norm of the
undisplaced atom (used by E2). ∎

## 4. Certified-gap transfer (claims A2, A3)

**Monotonicity lemma.** If `D ⊆ D'` (as `K`-term superposition
classes for a fixed target `T` and budget `K`), then
`sup_{g in D} F(g, T) <= sup_{g in D'} F(g, T)`. Proof: a supremum over
a subset. ∎

**A2 (descended certified bounds).**
(a) *Trefoil target* `T_tref` (exp25/exp29's `0.8|20> + 0.6|03>`), `K
<= 2`: exp29 W5 certifies an upper bound on `sup F` over `D_G` `K <= 2`
superpositions (its certified constant; value in exp29's artifact, not
restated here). By A0 + monotonicity, the **same bound holds over every
tier below `D_G`**: every `T_b(s*)` (`s* < 1`, in particular exp25's
`s* = 0.98` instance), every `T_eq(A0, B)`, every bounded or unbounded
coherent class. In the note's convention (`K_eps` with `F >= 1 - eps`),
for every `eps < 1 - (exp29's certified fidelity bound)` and every tier
`D` in the ladder: no `K <= 2` state from `D` sits in the fidelity
`eps`-ball of `T_tref` (the run's E4 records the outward-rounded
converted threshold; the exact-arithmetic conversion rule is A5).
(b) *Hopf target* `|1,1>`, `K <= 2`, coherent tiers: exp28 S5
certifies an upper bound on `sup F` over `D_coh` `K <= 2`; by
monotonicity it descends to every `T_coh(B)`. ∎ (basis: exp29 W5 and
exp28 S3–S5 as black-box inputs; nothing here re-proves them.)

**A3 (common-quadratic division and the `|1,1>` gap at every common
instance).** Let `g` be a `K`-term superposition from `T_eq(A0, B)`
(any fixed `A0`, `||A0|| < 1`; the bound `B` plays no role in this
claim). Its stellar function is

```
f_g(w) = sum_{k<=K} z_k c_k exp((1/2) w^T A0 w + b_k^T w)
       = exp((1/2) w^T A0 w) * sum_{k<=K} z_k c_k exp(b_k^T w),
```

and the common Gaussian factor never vanishes, so `Z(f_g)` equals the
zero set of the **coherent-type** function `sum z_k c_k exp(b_k^T w)`.
By exp24 P3, for `K <= 2` this zero set is a family of parallel affine
complex lines with no linked pair, on every sphere. Consequently the
exp28 S5 argument applies verbatim to the common tier: any unit `g`
with `delta(g, |11>) < ` exp28's certified stability radius would have
zero link ambient-isotopic to the Hopf link (a linked pair) by exp28
S3; a `T_eq(A0, B)` `K <= 2` state has no linked pair; hence every such
`g` has `delta >= ` that radius, and `sup F` over `T_eq(A0, B)`
`K <= 2` obeys **the same certified fidelity bound as exp28's coherent
case — uniformly in `A0` and `B`**.

Contrast, recorded as part of the same claim: the *varying*-quadratic
tiers are **not** obstructed at `|1,1>`: exp24 P4's TMSV cats are
2-term states with `A_k = ± lambda * offdiag` (two *different*
quadratics), `F = 1 - lambda^4 -> 1`, and `||A_k|| = lambda` is
arbitrarily small — so for **every** `s* > 0`, `sup F` over `T_b(s*)`
`K = 2` at `|1,1>` equals `1`. The dichotomy at `|1,1>` is therefore
**common vs varying quadratic**, not bounded vs unbounded: precisely
the two-mode mirror of the note's mechanism ("the common-squeezing
slice is immune — there the Gaussian factor divides out", note §5.4
discussion), reproduced here by topological rather than counting means.
At the trefoil target, by A2(a), even the unrestricted tier is
obstructed at `K <= 2`. ∎ (basis: exp24 P3–P4, exp28 S3–S5.)

## 5. Separations and non-transfer (claim A4)

**A4.** (a) *Strictness.* Every inclusion in A0 is strict at the atom
level: an atom with `||A|| in (tanh S, 1)` witnesses `T_b(tanh S) ⊊
D_G`; two atoms with different quadratics witness that a `T_b` pair
lies in no single `T_eq(A0, ·)` instance; any atom with `A != 0`
witnesses `T_coh ⊊` gaussian tiers. (b) *Direction of transfer.*
Fidelity **upper** bounds descend the ladder (monotonicity lemma);
**constructions** (fidelity lower bounds / optimizer cells) only
ascend. exp25's measured cells are constructions in `T_b(0.98)` and so
witness lower bounds for every tier above it, none below. (c)
*Convention bridge.* The note's `xi`-convention and gaussact's
`zeta`-convention squeezers differ by `xi = -zeta`; both parametrize
the same atom sets at any bound, and every tier of §2 is defined on
`(A, b)` data only, so no statement in this memo depends on the
convention. (d) *No cross-mode identification.* The one-mode
`A(a, B)` and two-mode `T_eq(A0, B)` are analogues by construction of
§3(ii); no theorem of the note is imported for two modes and no
two-mode result is claimed to bear on the note's one-mode rows. ∎

## 6. Exact ε-convention conversion (claim A5)

**A5.** With `F = |<psi|phi>|^2`, `delta = sqrt(2 (1 - sqrt(F)))`
(exp28 §1), the maps below are exact, mutually inverse where stated,
and monotone:

```
F(delta)   = (1 - delta^2 / 2)^2          for delta in [0, sqrt(2)]  (decreasing),
delta(F)   = sqrt(2 (1 - sqrt(F)))        for F in [0, 1]            (decreasing),
eps_note(delta*) = 1 - (1 - delta*^2 / 2)^2                          (increasing),
```

so a certified stability radius `delta*` (exp28's or exp29's constant)
converts to the note-convention statement "for every `eps <
eps_note(delta*)`, no admissible `K`-budget state reaches `F >= 1 -
eps`". Proof: `delta^2 = 2(1 - sqrt(F))` ⟺ `sqrt(F) = 1 - delta^2/2`
(both sides in `[0,1]` for `delta <= sqrt(2)`), square; monotonicity by
inspection; the `eps_note` form is `1 - F(delta*)`. Evaluation
discipline (binding for the run and any restated number): thresholds of
the "for all `eps < ...`" form are rounded **down** (a smaller
threshold weakens the claim), fidelity upper bounds are rounded **up**;
exact arithmetic in `fractions.Fraction` on the committed binary values
of the input constants, with `math.nextafter` outward float conversion
(the exp29 `fidelity_bound` pattern). This memo restates no evaluated
constant; the run records them. ∎

## 7. Experiment plan (E-series; constants declared here)

Artifacts: `dictionary_alignment.json` written by `run.py`; README
block generated by `summary_block.py` from the JSON (one authoring
location, policy-tested like exp28/29). Referee tests in
`tests/test_dictionary_alignment.py`.

Declared constants: `SEEDS = range(64)`, `R_MAX = 0.8`,
`ALPHA_MAX = 1.0`, `CUTOFF_E1 = 30`, `TOL_E1 = 1e-9`,
`SIGMAS_E2 = (0.1, 0.3, 0.5, 0.7, 0.9, 0.95)` (all ordered pairs),
`CUTOFF_E2 = 80`, `TOL_E3_F = 1e-6`, `EPS_GRID_E4 = {k/50 : k = 1..49}`.

- **E1 (normal-form referee; gates F1).** For each seed: draw random
  Gaussian-unitary factor data (`gaussact.random_gauss_params(seed,
  r_max = R_MAX, alpha_max = ALPHA_MAX)`), apply the factor chain to
  the vacuum via gaussact, and check: the polynomial part stays degree
  0; `A` is symmetric with `||A|| < 1`. Then **rebuild** the state a
  second way through A1's constructive recipe — Takagi of the chain's
  `A`, `r_i = artanh sigma_i`, passive `V^T`, displacement `alpha =
  (I - A bar(A))^{-1}(b + A bar(b))` — and check the two states agree
  up to global phase in Fock coefficients at `CUTOFF_E1` within
  `TOL_E1`; check `b = alpha - A bar(alpha)` reproduces the chain's `b`
  within `TOL_E1`; check the A1(ii) sandwich inequalities.
- **E2 (norm closed form; gates F2).** For each `(sigma_1, sigma_2)`
  pair from `SIGMAS_E2`: partial Fock norm of the undisplaced diagonal
  atom at `CUTOFF_E2`, plus the certified geometric tail bound
  `t_N <= |c_N|^2 sigma^2 / (1 - sigma^2)` per mode (the term ratio
  `(2n+1)/(2n+2) sigma^2 < sigma^2` makes the tail dominated by a
  geometric series), must bracket the closed form
  `prod_i (1 - sigma_i^2)^{-1/2}`: closed form in
  `[partial, partial + tail]`. (Implementation note, 2026-08-02, after
  the first run halted at F2: the comparisons are float-valued, and on
  fully-converged small-sigma pairs the bracket endpoints coincide with
  the closed form to machine precision, flipping direction by 1–2 ulp —
  observed `<= 4.5e-16` relative, both sides. The comparisons therefore
  carry a declared relative slack `E2_REL_SLACK = 1e-12` on each side:
  four orders above the observed float noise, and far below any genuine
  closed-form defect this referee is meant to catch, which would enter
  at percent scale or worse.)
- **E3 (committed-cell membership and descended bounds; gates F3).**
  From exp25's committed artifact: for every gaussian cell, rebuild
  each atom's `(A_k, b_k)` from `best_params` by exp25's own
  parametrization (`A = [[2 q11, q12], [q12, 2 q22]]`, `b = (l1,
  l2)` — `run.py::terms_from_params`), recompute the cell's fidelity
  independently through gaussact Fock coefficients at exp25's committed
  cutoff and check agreement with the committed `best_fidelity` within
  `TOL_E3_F` (this pins the parametrization reading); check
  `||A_k|| <= ` the committed `bounded_dictionary.quad_norm_max`
  (membership in `T_b(0.98)`). Descended-bound checks (A2): trefoil
  gaussian and coherent `K <= 2` cells against exp29's committed
  fidelity bound; `t11` coherent `K <= 2` cells against exp28's
  committed fidelity bound. Recorded as a diagnostic, **not** a gate:
  `t11/gaussian/K=2`'s measured `F` (A3's contrast predicts it can
  approach 1; no bound is claimed there).
- **E4 (exact conversions; gates F4).** In `Fraction` arithmetic:
  round-trip identities `F(delta(F)) = F` on `EPS_GRID_E4` (implementation
  note, added 2026-08-02 before any implementation ran: this leg runs on
  the exact rational squares `(k/50)^2` as the `F` values, so both legs
  stay in exact arithmetic — the square root of a non-square rational
  has no exact representation, and an enclosure-based round trip would
  verify only the enclosure) and `delta(F(delta)) = delta` on the
  grid read as rational `delta^2` values; then the outward-rounded
  note-convention thresholds `eps_note` for exp28's and exp29's
  committed radii per A5's evaluation discipline, recorded in the
  artifact (rounded down) next to the committed fidelity bounds
  (rounded up).

Verdicts are computed in `run.py` from the data (never hand-written);
halt discipline as in exp28/29: a firing gate stops downstream
sections, artifacts are written before the halt.

## 8. Falsification gates (blocking; fixed before implementation)

- **F1**: any E1 referee violation — the normal form or the A1
  translation is defective as implemented; halt, diagnose §3 against
  gaussact before interpreting anything.
- **F2**: E2 bracket violation — A1(iii)'s norm closed form is wrong
  or the tail bound is unsound; halt.
- **F3**: any committed gaussian cell fails membership or fidelity
  re-derivation, or any covered cell violates a descended bound — the
  A0/A2 chain or a committed artifact is defective; halt (a descended-
  bound violation would also be evidence against the exp28/29 inputs
  and must be reported upstream, never absorbed).
- **F4**: any exact conversion identity fails — A5 is defective; halt.

## 9. Claim table

One row per claim; empty cells would be visible. This table is the sole
authoring location for exp30 epistemic status.

| ID | Claim (headline) | Status | Basis |
| --- | --- | --- | --- |
| A0 | two-mode tier definitions; inclusion ladder `T_coh ⊂ T_eq ⊂ T_b ⊂ D_G` (as stated per-K) | proved here | §2 |
| A1 | Gaussian stellar normal form `c exp(w^T A w / 2 + b^T w)`, `\|\|A\|\| < 1` iff normalizable; Takagi/`tanh` translation and `b ↔ alpha` map (two-mode row-D2 analogue) | proved here | §3 |
| A2 | certified bounds descend: trefoil `K<=2` bound at every tier below `D_G`; `\|11>` coherent bound at every `T_coh(B)` | proved here (uses exp29 W5, exp28 S3–S5) | §4 |
| A3 | common-quadratic division: `T_eq(A0, B)` `K<=2` has no linked pair; `\|11>` gap holds at every common instance with exp28's constant, while every `T_b(s*)` reaches `F -> 1` there | proved here (uses exp24 P3–P4, exp28 S3–S5) | §4 |
| A4 | strict separations; transfer directions; convention bridge; no cross-mode identification | proved here | §5 |
| A5 | exact `delta`/`F`/`eps_note` conversions with outward evaluation discipline | proved here | §6 |
| N1 | E1 normal-form referee passes | numerical, E1 | run |
| N2 | E2 norm bracket holds | numerical, E2 | run |
| N3 | E3 membership, fidelity re-derivation, and descended bounds hold on committed cells | numerical, E3 | run |
| N4 | E4 exact conversions verified; converted thresholds recorded | numerical, E4 | run |
