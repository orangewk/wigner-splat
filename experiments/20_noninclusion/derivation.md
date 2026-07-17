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
`A_{eta/(eta-sigma)}(cat)` of a pure non-Gaussian state. No Lemma-2
shortcut; `run.py` computes its spectrum directly (expected: a
thermal-like tail from the amplifier dilation, i.e. full rank — the
amplifier's Stinespring two-mode squeezer entangles every pure
non-vacuum input with the environment).

### Regime III: `eta' < eta - sigma`

`v < 0`: the residual factor is a formal **negative-variance** noise
and the pre-image is not a channel image of the cat at all. Whether
`chi_{rho'}` is PSD must be checked directly: `run.py` reconstructs
`rho'(eta')` in the Fock basis from its 4-Gaussian-term chi
(`rho' = (1/pi) int chi(lam) D(lam)^dagger d^2 lam`, Gauss–Hermite in
Re/Im lam against the closed-form displacement matrix elements) and
scans the minimum eigenvalue and the eigenvalue tail over an eta' grid.
Expected: PSD fails immediately below the boundary (noise subtraction
from a non-Gaussian mixed state), and nothing in the scan comes close
to rank 2.

## 3. What this buys

If the Regime-III scan shows PSD violation (or full rank wherever PSD
holds) across `(0, eta - sigma]`:

> For NO `eta'` in `(0, 1]` is the exp19 target expressible as
> `loss_eta'(rho')` with `rho'` of ANY finite rank — the regime-I/II
> exclusion is analytic (Lemmas 1–2), the regime-III / boundary
> exclusion is numerical on a grid.

Note the statement is stronger than the rank-2 question asked: Lemma 2
excludes every finite rank at once, and the numeric scan reports the
full spectrum, not a rank-2 test. The claim upgrade this licenses for
exp19 (decision rule case 2 on the issue) still requires the Route-B
corroboration: a best-approximation floor in `1 - F` that survives
cutoff growth, since the analytic statement concerns EXACT equality
while exp19's comparisons live at finite fidelity.

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
