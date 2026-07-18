# Experiment 20 — the non-inclusion test (issue #63): derivation note

Question (pre-declared on the issue): does there exist an efficiency
`eta' in (0, 1]` and a rank-2 squeezed-product ket mixture
`rho' = B'B'^dagger / Z` such that

```
loss_eta'(rho')  =  N_sigma(E_eta(rho_cat))        (exactly)
```

for the exp19 target (`alpha = 1.5`, `parity = +1`, `eta = 0.8`,
`sigma_add = 0.1` added variance per quadrature)? Secondary: if not for
rank 2, for **any** finite rank.

This note fixes conventions, derives the unique pre-image for every
`eta'`, and splits `(0, 1]` into a regime where non-inclusion is
**analytic** and a boundary regime where it is settled **numerically**
(`run.py` in this directory). Everything is one-mode until the final
section; the three-mode port is a per-mode bookkeeping change.

## 1. Conventions

Symmetric characteristic function `chi_rho(lam) = Tr[rho D(lam)]`,
`lam in C`, with `D` the displacement operator. In these units the
vacuum has `chi = exp(-|lam|^2 / 2)`, i.e. variance 1/2 per quadrature,
and a symmetric Gaussian state with variance `V` per quadrature has
`chi = exp(-V |lam|^2)`.

The two channels of interest act on `chi` by argument rescale times
Gaussian multiplication:

- **Loss** `E_eta`:  `chi(lam) -> chi(sqrt(eta) lam) * exp(-(1-eta) |lam|^2 / 2)`.
  (Vacuum fixed point checks the convention.)
- **Classical Gaussian displacement noise** `N_v` (random displacement,
  added variance `v` per quadrature):  `chi(lam) -> chi(lam) * exp(-v |lam|^2)`.
- **Quantum-limited amplifier** `A_G` (gain `G >= 1`):
  `chi(lam) -> chi(sqrt(G) lam) * exp(-(G-1) |lam|^2 / 2)`.

The exp19 target is `T = N_{sigma}(E_eta(cat))` with `sigma = 0.1`:

```
chi_T(lam) = chi_cat(sqrt(eta) lam) * exp(-[(1-eta)/2 + sigma] |lam|^2).
```

Two standard lemmas used below:

**Lemma 1 (commutation).** `N_sigma . E_eta = E_eta . N_{sigma/eta}`.
*Proof*: compose the chi actions; the Gaussian exponents match iff the
inner noise is `sigma/eta`. (One line each way.)

**Lemma 2 (noise output is full rank).** For `v > 0` and any state
`rho`, `N_v(rho)` has trivial kernel (full rank).
*Proof*: suppose `<psi| N_v(rho) |psi> = 0`. Writing
`N_v(rho) = integral p(beta) D(beta) rho D(beta)^dagger d^2 beta` with a
strictly positive Gaussian `p`, every eigenvector `phi` of `rho` (with
eigenvalue `> 0`) must satisfy `<psi| D(beta) |phi> = 0` for almost
every `beta`. But `beta -> <psi|D(beta)|phi>` is continuous with
L^2 norm `pi <psi|psi><phi|phi> > 0` by the displacement orthogonality
relations — contradiction. (The same argument runs verbatim with
multi-mode displacements.)

## 2. The unique pre-image, for every eta'

`E_eta'` is injective on trace-class operators (its chi action is
invertible pointwise), so IF the target is in the family, the pre-loss
state is unique:

```
chi_{rho'}(mu) = chi_T(mu / sqrt(eta')) * exp(+(1-eta') |mu|^2 / (2 eta'))
              = chi_cat(k mu) * exp(-c |mu|^2),
k^2 = eta / eta',        c = (eta' - eta + 2 sigma) / (2 eta').
```

Decay is never the issue: each Gaussian term of `chi_cat` decays like
`exp(-k^2 |mu|^2 / 2)` (up to displacement phases), so the total decay
rate is `k^2/2 + c = 1/2 + sigma/eta' > 1/2` — faster than vacuum for
every `eta'`. The binding question is whether `chi_{rho'}` is the
characteristic function of a **positive semidefinite** operator, and if
so, of one with **rank <= 2**.

### Regime I: `eta' > eta` (less loss than physical)

Split off a loss channel at `k^2 = eta/eta' < 1`:

```
rho' = N_{sigma/eta'} ( E_{eta/eta'} (cat) ),
```

(the residual Gaussian exponent after the loss factor is
`c - (1-k^2)/2 = sigma/eta' > 0`). Valid state for every such `eta'`,
but by Lemma 2 it is FULL RANK. A rank-2 mixture — or any finite-rank
state — cannot equal it. **Excluded analytically.**

### Regime II: `eta - sigma < eta' <= eta`

Now `k >= 1`; split off an amplifier at `G = eta/eta' >= 1`:

```
rho' = N_v ( A_G (cat) ),      v = (eta' - eta + sigma) / eta' > 0.
```

Again a valid state, again full rank by Lemma 2. **Excluded
analytically.**

### Boundary: `eta' = eta - sigma` (= 0.7 for the exp19 numbers)

`v = 0`: the pre-image is exactly the quantum-limited amplifier output
`A_G(cat)`, `G = eta/(eta - sigma)` — a valid state, so PSD offers no
contradiction. Finite rank is excluded by the analytic-kernel argument
of Theorem 2 below. (The first draft of this note left the boundary to
a finite-cutoff spectrum computation; the PR-64 review correctly
flagged that as insufficient for an "any finite rank" claim, and this
section was strengthened to a proof.)

**Theorem 2 (boundary: infinite rank).** `A_G(cat)` with `G > 1` has
no finite-rank representation.
*Proof.* Write the Husimi function through chi (Section 1):
`Q_{rho'}(beta) = (1/G) Q_cat(beta/sqrt(G))`, since at the boundary
`w := (c + 1/2)/k^2 = 1/2` exactly (see Theorem 1 below for `w`). The
Bargmann kernel `B(u, conj(v)) = e^{(|u|^2+|v|^2)/2} <v|rho'|u>` is
entire in `(u, conj(v))` and is determined by its diagonal, which the
Husimi identity fixes as

```
B(beta, conj(beta)) = (1/G) e^{|beta|^2 (1 - 1/G)}
                      F(conj(beta)/sqrt(G)) conj(F(conj(beta)/sqrt(G))),
```

with `F` the cat's (entire) Bargmann function. Its unique entire
continuation is `B(u, cv) = (1/G) e^{u cv (1 - 1/G)} F(cv/sqrt(G))
Ftil(u/sqrt(G))` (`Ftil(u) = conj(F(conj(u)))`, entire). If `rho'` had
rank `R < infinity`, `B` would be a sum of `R` products
`G_r(u) conj(G_r(conj(cv)))` and the functions `u -> B(u, cv_j)` could
span at most `R` dimensions. But for `t = 1 - 1/G != 0` the functions
`u -> e^{t u cv_j} F...(u)` for distinct `cv_j` are linearly
independent (divide out the nonzero entire factor; distinct
exponentials are independent). Contradiction. QED

### Regime III: `eta' < eta - sigma`

`v < 0`: the residual factor is a formal **negative-variance** noise
and the pre-image is not a channel image of the cat at all. Here PSD
itself fails, on the WHOLE subinterval, analytically:

**Theorem 1 (regime III: no PSD pre-image).** For every
`eta' < eta - sigma` there is no PSD trace-class operator with the
pre-image characteristic function.
*Proof.* Suppose `rho'` is such an operator. Its Husimi function is
`Q_{rho'}(beta) = (1/pi^2) int chi_{rho'}(lam) e^{-|lam|^2/2}
e^{beta conj(lam) - conj(beta) lam} d^2 lam`. Substituting
`mu = k lam` turns this into a rescaled s-ordered quasidistribution of
the CAT itself:

```
Q_{rho'}(beta) = (1/k^2) W_s(cat)(beta/k),
s = -2w,   w = (c + 1/2)/k^2 = (2 eta' - eta + 2 sigma) / (2 eta),
```

and `w < 1/2` (i.e. `s > -1`) **exactly** characterizes
`eta' < eta - sigma`. PSD of `rho'` forces `Q_{rho'} >= 0`, hence
`W_s(cat) >= 0` everywhere. But then the cat's Husimi function, which
is the further Gaussian smoothing `Q_cat = W_s * Gauss_{(s+1)/2}` with
a strictly positive kernel, would be strictly positive everywhere —
while `Q_cat` has EXPLICIT zeros: the even cat's Bargmann function
`F(cb) ~ cosh(cb alpha)` vanishes at `cb = i pi (2j+1) / (2 alpha)`.
Contradiction. QED
(This is the nonclassical-depth-1 mechanism of Lutkenhaus & Barnett,
PRA 51, 3340 (1995), instantiated with the cat's closed-form Bargmann
zeros so the argument is self-contained.)

`run.py` CORROBORATES Theorem 1 on a grid: it reconstructs
`rho'(eta')` in the Fock basis from its 4-Gaussian-term chi
(`rho' = (1/pi) int chi(lam) D(lam)^dagger d^2 lam`, Gauss–Hermite in
Re/Im lam against the closed-form displacement matrix elements) and
reports minimum eigenvalues and eigenvalue tails; the scan also
visualizes HOW the violation grows away from the boundary. The
conclusions do not rest on the grid.

## 3. What this buys

> For NO `eta'` in `(0, 1]` is the exp19 target expressible as
> `loss_eta'(rho')` with `rho'` of ANY finite rank — regime I/II by
> Lemmas 1–2, regime III by Theorem 1, the boundary point by
> Theorem 2. The exclusion is analytic on the whole interval; the
> run.py scan is numerical corroboration.

Note the statement is stronger than the rank-2 question asked: every
finite rank is excluded at once. The claim movement this licenses for
exp19 (decision rule case 2 on the issue) also asks for Route-B
corroboration on the finite-fidelity axis, since the analytic
statement concerns EXACT equality while exp19's comparisons live at
finite fidelity. Route B (routeB.py) supplies best-approximation
residuals: by nature these are UPPER bounds on the family's distance
to the target obtained by local optimization — heuristic
corroboration, not a proven lower bound (wording per the PR-64
review).

## 4. The eta-flat direction (exp17's hazard = exp19's asset)

The same algebra explains the pairing recorded in exp17/exp19. Along
the curve `eta'(s), rho'(s) = N_{sigma(s)}(E_{k^2(s)}(cat))` traced in
Section 2, the DATA distribution `loss_eta'(rho')` is constant while
`eta'` moves across an interval of width `O(sigma)` — an exactly flat
likelihood direction whenever the model family contains Gaussian-noise
surrogates for loss. Small budgets cannot resolve `eta'` along it
(exp17: joint fitting is identifiability-unsafe), and precisely the
same freedom lets a blind fit slide along the curve to soak up noise
the ket mixture cannot express (exp19: eta fitted 0.8 -> 0.36). One
flat direction, two faces.

## 5. Three modes

The target and family apply the channels PER MODE, and the 3-mode cat's
chi is a sum of 4 terms, each a PRODUCT over modes of 1-mode
Gaussian-with-phase factors (it is a superposition of two product
coherent states). Every step above — Lemma 1, the pre-image formula,
the regime splits — acts mode-by-mode on these factors, and Lemma 2's
orthogonality argument runs verbatim with 3-mode displacements. So the
regime-I/II analytic exclusion ports unchanged, and the regime-III
Fock reconstruction factorizes: each chi term contributes a Kronecker
product of three 1-mode operators, each computed by the same 2D
quadrature (`run.py` does the 3-mode reconstruction this way,
cross-checked against the 1-mode scan).
