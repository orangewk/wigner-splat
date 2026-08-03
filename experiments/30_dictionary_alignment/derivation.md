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

(Revised in the 2026-08-02 round-1 review: the first draft's ladder
display mixed atom sets with `K`-term classes; the two levels are now
typed explicitly, and every statement names its type.)

**Atom sets.** An *atom* is a normalized state whose stellar function
is `c exp((1/2) w^T A w + b^T w)` with `A = A^T`, `||A|| < 1` (§3
proves this is exactly the pure Gaussian states and that `||A|| < 1`
is forced). By the uniqueness lemma of §5 the data `(A, b)` is
determined by the state, so membership below is well-defined. Each of
the following is a **set of atoms**:

- **Atoms_coh(B)**: `A = 0`, `|b| <= B`. The union over all `B` is the
  atom set of exp24's `D_coh`.
- **Atoms_eq(A0, B)** (common-quadratic instance; the literal two-mode
  analogue of the note's `A(a, B)`): `A = A0` — one fixed matrix for
  the whole instance (`||A0|| <= a* < 1`), mirroring the note's "same a
  in modulus and angle" — and `|b| <= B`.
- **Atoms_b(s*)** (bounded, per-atom-varying quadratic; exp25's
  operational family): `||A|| <= s* < 1`, `A` and `b` otherwise free.
  exp25 ran `s* = 0.98` (its committed
  `bounded_dictionary.quad_norm_max`; its Fock-tail discipline is a
  truncation implementation detail, recorded but not a tier).
- **Atoms_G**: `||A|| < 1`, `b` free — the atom set of exp24's `D_G`
  (exp24's wording "no squeezing bound" means: no uniform `s* < 1`;
  individual physical atoms always have `||A|| < 1` by §3).

**K-term classes.** For an atom set `X` and a budget `K`, `S_K(X)` is
the set of normalized states proportional to `sum_{k<=K} z_k g_k` with
every `g_k in X`. `S_1(X)` is `X` itself (as states).

**A0 (ladder).**
(a) *Equality:* `Atoms_eq(0, B) = Atoms_coh(B)` — the common instance
at `A0 = 0` **is** the bounded coherent atom set (no properness is
claimed here or anywhere for this pair).
(b) *Atom-set inclusions:* for every `B <= B'`, `s* <= s*' < 1`, and
`A0` with `||A0|| <= s*`:

```
Atoms_coh(B) ⊆ Atoms_coh(B') ⊆ D_coh atoms ⊆ Atoms_G,
Atoms_eq(A0, B) ⊆ Atoms_b(s*) ⊆ Atoms_b(s*') ⊆ Atoms_G.
```

(c) *Class monotonicity:* `X ⊆ Y` implies `S_K(X) ⊆ S_K(Y)` for every
`K`.
Proof: (a) and (b) read off the definitions — each step only relaxes a
constraint. (c): a representation over `X` is a representation over
`Y`. ∎ Which of these inclusions are **proper** is a separate, typed
question answered in A4 (§5); nothing downstream of this section uses
properness.

The ladder mirrors the note §2.4 rows: `Atoms_eq` instances are the
two-mode sibling of row D2's dictionary; `Atoms_G` is the two-mode
sibling of the *family column* of row D1 (the unrestricted pure-Gaussian
superpositions); `Atoms_b` sits between and exists because exp25's
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
*(iii).* (Corrected in the 2026-08-02 round-1 review: the first draft
reduced (iii) to `b = 0` via "displacements are unitary", but removing
`b` needs an `alpha` with `b = alpha - A bar(alpha)`, and that map is
**not** surjective when `||A|| >= 1` — e.g. `A = diag(1, 0)` makes the
first component `alpha_1 - bar(alpha_1)`, purely imaginary, so
`b = (1, 0)` is unreachable. The direct argument below covers every
`b`.) Suppose `||A|| >= 1` and some normalizable state had stellar
function `f = exp((1/2) w^T A w + b^T w)`. Square-summable Fock
coefficients would place `f` in the Bargmann–Segal space
`HL^2(C^2, pi^{-2} e^{-|w|^2} dV)` with `int |f|^2 e^{-|w|^2} dV /
pi^2` equal to the squared Fock norm (Bargmann's isometry, imported as
a named classical fact; the K_ε note's §2 conventions live in the same
space). The space and its norm are invariant under the unitary
substitution `w -> U w` (a passive unitary on states, exp24 P2), so
with `U = bar(V)` from Takagi `A = V Sigma V^T` we may take
`A = Sigma = diag(sigma_1, sigma_2)`, `sigma_1 = ||A|| >= 1`, at the
price of replacing `b` by some `b'`. The integrand then factorizes
over the modes; writing `w_1 = x + i y`, `beta = Re b'_1`,
`gamma = -Im b'_1`, the mode-1 factor of `|f|^2 e^{-|w|^2}` is

```
exp( (sigma_1 - 1) x^2 + 2 beta x ) * exp( -(1 + sigma_1) y^2 + 2 gamma y ),
```

whose `x`-integral diverges for every `beta`: for `sigma_1 > 1` the
exponent grows, and for `sigma_1 = 1` it is `int exp(2 beta x) dx`,
infinite for every real `beta` (including `beta = 0`). The `y`-integral
and the whole mode-2 factor's integral are integrals of strictly
positive functions, hence positive (finite or not), so by Tonelli the
full integral diverges — contradicting membership in the Bargmann
space. Hence no normalizable state has that stellar function, for any
`b`. For `||A|| < 1` and `b = 0` the squared Fock norm is the product
of the one-mode series

```
sum_{n>=0} sigma^{2n} (2n)! / (4^n (n!)^2)  =  sum_n C(2n, n) (sigma^2/4)^n
                                            =  (1 - sigma^2)^{-1/2},
```

i.e. `prod_i (1 - sigma_i^2)^{-1/2}`, the closed form E2 referees
(each series converges since its terms are `~ sigma^{2n}/sqrt(pi n)`). ∎

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
class below**: `S_2(Atoms_b(s*))` for every `s* < 1` (in particular
exp25's `s* = 0.98` instance), `S_2(Atoms_eq(A0, B))` for every
instance, and every bounded or unbounded
coherent class. In the note's convention (`K_eps` with `F >= 1 - eps`),
for every `eps < 1 - (exp29's certified fidelity bound)` and every tier
`D` in the ladder: no `K <= 2` state from `D` sits in the fidelity
`eps`-ball of `T_tref` (the run's E4 records the outward-rounded
converted threshold; the exact-arithmetic conversion rule is A5).
(b) *Hopf target* `|1,1>`, `K <= 2`, coherent tiers: exp28 S5
certifies an upper bound on `sup F` over `D_coh` `K <= 2`; by
monotonicity it descends to `S_2(Atoms_coh(B))` for every `B`. ∎ (basis: exp29 W5 and
exp28 S3–S5 as black-box inputs; nothing here re-proves them.)

**A3 (common-quadratic division and the `|1,1>` gap at every common
instance).** Let `g` be a state of `S_K(Atoms_eq(A0, B))`
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
S3; a `S_2(Atoms_eq(A0, B))` state has no linked pair; hence every such
`g` has `delta >= ` that radius, and `sup F` over `S_2(Atoms_eq(A0, B))`
`K <= 2` obeys **the same certified fidelity bound as exp28's coherent
case — uniformly in `A0` and `B`**.

Contrast, recorded as part of the same claim: the *varying*-quadratic
tiers are **not** obstructed at `|1,1>`: exp24 P4's TMSV cats are
2-term states with `A_k = ± lambda * offdiag` (two *different*
quadratics), `F = 1 - lambda^4 -> 1`, and `||A_k|| = lambda` is
arbitrarily small — so for **every** `s* > 0`, `sup F` over `S_2(Atoms_b(s*))`
`K = 2` at `|1,1>` equals `1`. The dichotomy at `|1,1>` is therefore
**common vs varying quadratic**, not bounded vs unbounded: precisely
the two-mode mirror of the note's mechanism ("the common-squeezing
slice is immune — there the Gaussian factor divides out", note §5.4
discussion), reproduced here by topological rather than counting means.
At the trefoil target, by A2(a), even the unrestricted tier is
obstructed at `K <= 2`. ∎ (basis: exp24 P3–P4, exp28 S3–S5.)

## 5. Separations and non-transfer (claim A4)

(Rewritten in the 2026-08-02 round-1 review: the first draft asserted
atom-level strictness for "every inclusion in A0" — contradicting the
`Atoms_eq(0, B) = Atoms_coh(B)` equality — used an undefined bound
symbol in a witness, and offered a two-atom pair as an atom-level
witness. The claims below are typed, and each properness statement
carries a witness of its own type.)

**Uniqueness lemma (atom data is state-determined).** If two atoms
`c exp(q)` and `c' exp(q')` (`q, q'` quadratic-plus-linear exponents)
are the same state, their stellar functions agree up to a nonzero
constant, so `exp(q - q')` is a nonvanishing entire constant; then
`0 = d[exp(q - q')] = (dq - dq') exp(q - q')` forces `dq = dq'`
identically, hence `A = A'` and `b = b'`. Membership of a state in an
atom set of §2 is therefore well-defined. ∎

**A4.** (a) *Properness at the atom level (equivalently, of the
`S_1` classes).* With membership well-defined by the lemma: an atom
with `||A|| = (1 + s*)/2 in (s*, 1)` lies in `Atoms_G \ Atoms_b(s*)`;
an atom with `A != A0`, `||A|| <= s*`, `|b| <= B` lies in
`Atoms_b(s*) \ Atoms_eq(A0, B)`; an atom with `A != 0` lies outside
every coherent atom set; an atom with `|b| in (B, B']` separates the
`B`-graded sets. So every A0(b) inclusion between distinct constraint
tiers is proper at the atom level, while the A0(a) pair is an equality
and is claimed proper nowhere.
(b) *Properness at `K = 2`, common vs varying — the one class-level
properness this memo claims.* Fix any `s* in (0, 1)`, any `B >= 0`,
and any `A0` with `||A0|| <= s*`. exp24 P4's TMSV cat at squeezing
parameter `lambda = s*` is a 2-term superposition of atoms with
`A_k = ± lambda * offdiag` (`||A_k|| = lambda <= s*`, `b_k = 0`), so it
lies in `S_2(Atoms_b(s*))`; its zero link on `S3_1` contains a linked
pair (exp24 P4), while by A3 no state of `S_2(Atoms_eq(A0, B))` has
one. Hence `S_2(Atoms_eq(A0, B)) ⊊ S_2(Atoms_b(s*))` — properness of
the common tier inside the varying tier as *state classes*, not merely
as parametrizations. No other class-level properness is claimed
(whether e.g. `S_K(Atoms_b(s*))` exhausts `S_K(Atoms_G)` through
alternate representations is not needed by anything here and is left
open).
(c) *Direction of transfer.* Fidelity **upper** bounds descend the
ladder (monotonicity lemma); **constructions** (fidelity lower bounds /
optimizer cells) only ascend. exp25's measured cells are constructions
over `Atoms_b(0.98)` and so witness lower bounds for every class above,
none below. (d) *Convention bridge.* The note's `xi`-convention and
gaussact's `zeta`-convention squeezers differ by `xi = -zeta`; both
parametrize the same atom sets at any bound, and every set of §2 is
defined on `(A, b)` data only, so no statement in this memo depends on
the convention. (e) *No cross-mode identification.* The one-mode
`A(a, B)` and two-mode `Atoms_eq(A0, B)` are analogues by construction
of §3(ii); no theorem of the note is imported for two modes and no
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
  (membership in `Atoms_b(0.98)`). Descended-bound checks (A2): trefoil
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
| A0 | typed two-mode ladder: atom sets (`Atoms_coh`, `Atoms_eq`, `Atoms_b`, `Atoms_G`), their inclusions and the one equality, and `S_K` class monotonicity | proved here | §2 |
| A1 | Gaussian stellar normal form `c exp(w^T A w / 2 + b^T w)`, `\|\|A\|\| < 1` iff normalizable; Takagi/`tanh` translation and `b ↔ alpha` map (two-mode row-D2 analogue) | proved here | §3 |
| A2 | certified bounds descend: trefoil `K<=2` bound at every class below `D_G`'s; `\|11>` coherent bound at every `S_2(Atoms_coh(B))` | proved here (uses exp29 W5, exp28 S3–S5) | §4 |
| A3 | common-quadratic division: `S_2(Atoms_eq(A0, B))` has no linked pair; `\|11>` gap holds at every common instance with exp28's constant, while every `S_2(Atoms_b(s*))` reaches `F -> 1` there | proved here (uses exp24 P3–P4, exp28 S3–S5) | §4 |
| A4 | strict separations; transfer directions; convention bridge; no cross-mode identification | proved here | §5 |
| A5 | exact `delta`/`F`/`eps_note` conversions with outward evaluation discipline | proved here | §6 |
| N1 | E1 normal-form referee passes | numerical, E1 | run |
| N2 | E2 norm bracket holds | numerical, E2 | run |
| N3 | E3 membership, fidelity re-derivation, and descended bounds hold on committed cells | numerical, E3 | run |
| N4 | E4 exact conversions verified; converted thresholds recorded | numerical, E4 | run |
