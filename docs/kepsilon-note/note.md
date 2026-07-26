# Certified lower bounds and measured K–ε curves for approximate Gaussian rank

**Status: T2 draft (issue #71). Not yet reviewed as a whole; statements passed T0/T1 review (2 independent reviewers × 2 rounds), proofs of §3–§5 written out below, §7 numbers pending Gate E.**

Working note for the theory companion to the preprint
[doi:10.5281/zenodo.21457049](https://doi.org/10.5281/zenodo.21457049).
Vocabulary and gate history: issue #71.

---

## 1. Introduction

How well can a continuous-variable quantum state be described by finitely
many Gaussians? The exact and approximate *Gaussian rank* of a pure state —
the minimum number of pure-Gaussian components in a superposition — has
recently been defined and developed by Hahn, Takagi, Ferrini and Yamasaki
[HTFY, arXiv:2404.07115] (χ and its approximate version χ_δ, Gaussian
extent ξ), with the fidelity-ball ε-relaxation template established for the
stellar rank by Hahn, Garnier, Ferrini, Ferraro and Chabaud
[arXiv:2410.23721] and lower-bound techniques for the *coherent-state* rank
initiated by Cottier and Chabaud [arXiv:2604.00766]. **We claim no novelty
for the definitions**; this note adopts them and contributes three things
the cited line does not currently contain:

1. **Certified lower bounds from Bargmann zeros for bounded
   common-squeezing dictionaries** (§5), by a technique different from the
   low-rank-approximation route of [Cottier–Chabaud]: robust zeros of the
   target's Bargmann function survive fidelity-ball perturbation (Rouché)
   and are counted against an exponential-sum zero budget. The restriction
   to a bounded dictionary is **forced, not cosmetic**: we exhibit
   counterexample families showing that no disk-zero argument can bound the
   unrestricted rank (§5.4).
2. **An inequivalence theorem** (§6): the thermal lossy cat state of the
   preprint's experiment 20 has approximate Gaussian rank ≤ 2 for every ε,
   yet *no finite-rank pre-loss operator representation at any efficiency*
   (exact statement below). Gaussian-superposition compressibility and
   pre-loss operator-rank compressibility are inequivalent notions, and the
   same state separates them.
3. **Measured K–ε-type curves on public data and synthetic gates** (§7):
   the cutoff-scored family-constrained approximation curve and the
   real-data rank proxy of experiment 22, and (Gate E, pending) a
   numerically certified robust-zero census for finite-energy GKP states.

Throughout, three epistemic labels are used and never mixed: **certified**
(theorem-backed), **empirical** (best-found by optimization; an upper
bound on what is achievable), **proxy** (measured quantity standing in for
an inaccessible one, stated with its model assumptions).

## 2. Definitions

### 2.1 Gaussian rank and its fidelity-ball relaxation (adopted)

Fix a finite mode number M. For a normalized pure state |ψ⟩,

> χ_G(|ψ⟩) := min{ K : |ψ⟩ ∝ Σ_{k=1}^{K} c_k |G_k⟩, |G_k⟩ pure Gaussian },

with χ_G(|ψ⟩) := ∞ when no finite decomposition exists; the value set is
ℕ_{≥1} ∪ {∞} [HTFY's χ]. For a density operator ρ, using generalized
ensembles (a measure μ on a standard Borel space with a measurable field of
pure states, ρ = ∫ |ψ_i⟩⟨ψ_i| dμ(i)):

> χ_G(ρ) := inf over decompositions of [ ess sup_i χ_G(|ψ_i⟩) ],

the essential supremum taken with respect to the completed measure. Because
the objective is integer-valued, the outer infimum is attained (Lemma A1′).
Convex mixing is free by design; this matches the classical-simulability
anchor (mixtures of Gaussians are the classical backdrop against which
components are counted).

With F the **squared Uhlmann fidelity** F(ρ,σ) = (Tr √(√ρ σ √ρ))²
(pure–pure case |⟨ψ|φ⟩|²), the approximate rank is

> **K_ε^{G,F}(ρ) := min{ χ_G(σ) : F(ρ,σ) ≥ 1−ε }**, ε ∈ [0,1],

monotone non-increasing in ε, K_0 = χ_G. This is the fidelity-ball
template of [arXiv:2410.23721, Def. 7] applied to χ_G; on pure states it is
interconvertible with χ_δ of [HTFY] via ‖ψ−ψ′‖² = 2(1−Re⟨ψ|ψ′⟩)
(Appendix C).

### 2.2 The bounded common-squeezing dictionary (the certified results' quantity)

The certified lower bounds of §5 concern the following *restricted*
dictionary. Fix a complex squeezing parameter a, |a| ≤ a* < 1 — common in
**modulus and angle** — and a displacement budget B:

> G_eq(a,B) := { states whose Bargmann function is
> F(z) = e^{a z²/2} Σ_{k=1}^{K} c_k e^{b_k z}, |b_k| ≤ B }.

χ_{G_eq(a,B)} and K_ε^{G_eq(a,B),F} are defined verbatim as above with
components restricted to this family (mixed case: restricted ess-sup roof).
**Physical translation** (operator ordering D(α)S(ξ)|0⟩, ξ = r e^{iφ},
S(ξ) = exp[(ξ* â² − ξ â†²)/2]): a = −e^{iφ} tanh r and b = α − a α*, an
invertible real-linear map at fixed a with
(1−|a|)|α| ≤ |b| ≤ (1+|a|)|α| and α = (b + a b*)/(1−|a|²). So at fixed a,
a displacement bound and a B-bound are equivalent, and with
⟨n⟩ = |α|² + sinh²r the dictionary is energy-bounded; **neither equivalence
is uniform as |a| → 1**, which is why a* < 1 is part of the definition.

Since K_ε^{G,F} ≤ K_ε^{G_eq(a,B),F}, lower bounds on the restricted
quantity do **not** transfer to the unrestricted one. §5.4 shows this is
intrinsic to any zero-counting argument, not a defect of ours.

### 2.3 The subordinate contrast quantity R_ε

For the inequivalence theorem only, define the **pre-loss operator rank**

> R_ε(ρ) := min{ R : ∃ η′ ∈ (0,1], ∃ ρ′ ⪰ 0 with rank(ρ′) ≤ R and
> F(loss_{η′}(ρ′), ρ) ≥ 1−ε }.

R_ε is a repository-specific contrast quantity with no counterpart in the
cited literature. **It is subordinate by charter**: the note's claims are
made for χ_G / K_ε; R_ε appears only to exhibit their inequivalence, and no
monotonicity is claimed for it (loss cannot be "pulled back" through the
monotonicity of §3; the inequality only runs forward).

### 2.4 Declaration table (single source of truth for "which quantity, which state")

Every theorem, table and figure in this note cites one row of this table.
Rows are also targets of the build-time claim checker (§7.4): any number a
prose sentence attributes to a row must match the artifact JSON it names.

| ID | Quantity | State it certifies | Dictionary / family | Source of numbers |
|----|----------|--------------------|---------------------|-------------------|
| D1 | K_ε^{G,F} (unrestricted) | any ρ | all pure-Gaussian superpositions, roof | definitions only; no lower bounds claimed (impossible by §5.4a) |
| D2 | K_ε^{G_eq(a,B),F} (restricted) | pure targets of §5; ψ_trunc of Gate E | common complex a (\|a\| ≤ a* < 1), \|b_k\| ≤ B | Theorem B′ + exp23 `N_robust` |
| D3 | K_ε^{G_eq(a,B),F} lifted to the untruncated finite-energy comb | ideal finite-energy GKP comb | as D2, threshold d(ε)+‖tail‖ | exp23 `N_robust_lifted` (computed column; per-configuration) |
| D4 | R_ε (pre-loss operator rank; subordinate) | thermal lossy cat ρ_T | loss ∘ finite-rank | exp20 theorems (R_0 = ∞, certified); Route B series (empirical) |
| D5 | family-constrained approximation curve | thermal lossy cat ρ_T | rank-2 BB† + loss, K kets/column | exp22 JSON (empirical; cutoff-conditioned) |
| D6 | held-out NLL rank proxy | measured GKP data (true state unknown) | operator mixture rank R, K=4 kets | exp22 JSON (proxy) |

## 3. Consistency and monotonicity (certified)

**Lemma A1′.** χ_G is well-defined with values in ℕ_{≥1} ∪ {∞}; the sets
{ψ : χ_G(ψ) ≤ K} are universally measurable; for every ρ the outer infimum
in the roof is attained; K_ε^{G,F} is non-increasing in ε with
K_0^{G,F} = χ_G.

*Proof sketch (full version in Appendix A).* Measurability: {χ_G ≤ K} is
the projection of a Borel set in the (K-tuple of Gaussian parameters ×
coefficients) parameterization, hence analytic, hence universally
measurable; the ess sup is taken in the completed measure. Attainment: the
roof objective takes values in a discrete set; if no decomposition achieved
the value m := inf, every decomposition would have value ≥ m+1,
contradicting inf = m. K_0 = χ_G follows from F(ρ,σ) = 1 ⟺ ρ = σ. ∎

**Theorem A′ (Gaussian-channel monotonicity).** For every Gaussian channel
Λ (including loss and classical Gaussian noise), every state ρ, and every
ε ∈ [0,1]:

> K_ε^{G,F}(Λρ) ≤ K_ε^{G,F}(ρ), and χ_G(Λρ) ≤ χ_G(ρ).

*Proof.* (i) Rank part. Let σ achieve χ_G(σ) = m with decomposition
{μ, ψ_i}, ess sup χ_G(ψ_i) ≤ m (attained by Lemma A1′). Stinespring-dilate
Λ = Tr_E [U_G (· ⊗ |0⟩⟨0|_E) U_G†] with U_G Gaussian (for a mixed Gaussian
environment, purify with a further Gaussian ancilla). Resolve the
environment in the coherent-state POVM: for each i and β ∈ ℂ^{M_E},

  M_β ψ_i := ⟨β|_E U_G (|ψ_i⟩ ⊗ |0⟩_E)

is (unnormalized) a superposition of at most χ_G(ψ_i) ≤ m pure Gaussian
kets, because U_G maps Gaussian products to Gaussians and ⟨β| projections
of Gaussians are Gaussian. The joint measure dν(i,β) = dμ(i) p(dβ|i), with
zero-norm branches discarded and states renormalized (the weight absorbed
into ν), is a generalized ensemble for Λσ. Hence χ_G(Λσ) ≤ m.
(ii) ε part. If F(ρ,σ) ≥ 1−ε then F(Λρ, Λσ) ≥ F(ρ,σ) ≥ 1−ε by CPTP
monotonicity of the Uhlmann fidelity; combine with (i). ∎

The same proof restricted to G_eq(a,B) requires the channel to preserve the
dictionary and is **not** claimed; monotonicity is a statement about the
unrestricted quantities.

## 4. Zero counting for the dictionary (certified)

**Lemma P1 (multiplicity).** A nonzero exponential sum
g(z) = Σ_{k=1}^{K} c_k e^{b_k z} with distinct b_k and c_k ≠ 0 has zeros of
multiplicity at most K−1.

*Proof.* g^{(j)}(z₀) = Σ_k c_k b_k^j e^{b_k z₀}; if all derivatives up to
order K−1 vanish, the Vandermonde matrix (b_k^j) annihilates the nonzero
vector (c_k e^{b_k z₀}) — contradiction. ∎

**Lemma B1′-eq (disk zero count).** Let f ≢ 0 have the dictionary form
f(z) = e^{a z²/2} Σ_{k=1}^{K} c_k e^{b_k z} with |b_k| ≤ B (repeated
exponents merged, so the reduced order is ≤ K). Then for every disk
D̄(z₀,R), counting multiplicity:

> N(D̄(z₀,R); f) ≤ C·(K + B·R), with C an absolute constant.

*Proof.* e^{a z²/2} is zero-free, so N(f) = N(g) for the exponential sum g.
Apply the disk zero bound for exponential polynomials
[O. Friedland, arXiv:2606.24823, Lemma B.1]: a nonzero exponential sum of
order m with σ = max_k |μ_k| has at most C(m + σr) zeros (with
multiplicity) in any closed disk of radius r. Here m ≤ K, σ ≤ B. ∎

Because [arXiv:2606.24823] is a recent preprint, Appendix B re-derives its
Lemma 3.2 (disk growth: sup_{D(z₀,R)}|q| ≤ e^{2Rσ}(CR/r)^{m−1}
sup_{D(z₀,r)}|q|, by reducing rays z = z₀ + sθ to the classical interval
Turán inequality — the exponents θμ_k satisfy |Re(θμ_k)| ≤ σ) and its
Lemma B.1 (Blaschke: N zeros in D(z₀,r) force a factor θ^N, θ < 1 absolute,
against the disk growth at outer radius 8r). The only external input then
remaining is the classical interval Turán inequality itself. Both reviewer
audits (issue #71, T1 round 2) independently verified this chain.

## 5. Robust-zero lower bounds (certified, restricted dictionary)

### 5.1 Fidelity-to-Bargmann bridge

Convention: for normalized |ψ⟩, the Bargmann function
F_ψ(z) = e^{−|z|²/2}-normalized coherent overlap satisfies
|F_ψ(z)| ≤ e^{|z|²/2}, and the evaluation functional has norm e^{|z|²/2}.
If F(ψ,φ) ≥ 1−ε, choose the global phase of φ so ⟨ψ|φ⟩ ≥ 0; then
‖ψ−φ‖² = 2−2|⟨ψ|φ⟩| ≤ 2−2√(1−ε) =: d(ε)², and for all z

> |F_ψ(z) − F_φ(z)| ≤ e^{|z|²/2} d(ε).

The phase change multiplies all dictionary coefficients by one phase and
changes neither the component count nor the zeros.

### 5.2 Robust zeros

Let z_1, …, z_J be **distinct** zeros of F_ψ in D(0,R), with
multiplicities m_j, such that the closed disks D̄(z_j,δ) are pairwise
disjoint, and each is **(δ,ε)-robust**:

> min_{|z−z_j|=δ} |F_ψ(z)| > e^{(|z_j|+δ)²/2} d(ε).

Define **N_robust(ψ; R,δ,ε) := Σ_j m_j**.

### 5.3 Theorem B′

**Theorem B′.** Let |ψ⟩ be a normalized pure state and let |φ⟩ satisfy
F(ψ,φ) ≥ 1−ε with χ_{G_eq(a,B)}(φ) ≤ K. Then

> **K ≥ N_robust(ψ; R,δ,ε)/C − B(R+δ)**,

with C the absolute constant of Lemma B1′-eq.
*Mixed version* (pure target): if σ is mixed with F(ψ,σ) = ⟨ψ|σ|ψ⟩ ≥ 1−ε
and some generalized-ensemble decomposition has χ_{G_eq(a,B)}(φ_i) ≤ K for
μ-almost every i (equivalently the restricted roof is ≤ K, which is
attained by Lemma A1′), then the same bound holds.

*Proof.* By §5.1 the perturbation on each circle |z−z_j| = δ is strictly
below min |F_ψ| there; Rouché gives F_φ exactly m_j zeros (with
multiplicity) in D(z_j,δ). The disks are disjoint and contained in
D(0,R+δ), so F_φ has ≥ Σ m_j = N_robust zeros there; Lemma B1′-eq bounds
that count by C(K + B(R+δ)). Rearranged. Mixed case: since
∫ |⟨ψ|φ_i⟩|² dμ ≥ 1−ε, the set {i : |⟨ψ|φ_i⟩|² ≥ 1−ε} has positive
measure — otherwise the average would be strictly below 1−ε — and it meets
the full-measure set where the rank condition holds; pick a member and
apply the pure case. ∎

### 5.4 Why the restriction is forced (impossibility remarks)

**(a) No unrestricted disk-zero bound.** The even-cat family
|α⟩+|−α⟩ (K = 2, a = 0, b = ±α) has ~2Rα/π zeros in D(0,R). As α → ∞ the
zero count in a fixed disk is unbounded at fixed K. Hence no function of
(K, R) alone bounds disk zeros, and no lower bound on the unrestricted
χ_G can be extracted from zeros in a disk: the displacement budget B must
appear. (This is also why our certified quantity is K_ε^{G_eq(a,B),F};
cf. §2.2.)

**(b) The common-squeezing restriction and the plateau.** With two distinct
squeezings the family e^{a z²/2} − 1 (K = 2) has ~|a|R²/π zeros in D(0,R)
(a double zero at the origin — note Lemma P1 does not apply across distinct
squeezings). More generally a 2-component sum with squeezing gap Δa and
displacement gap Δb has ≤ c(|Δa|R² + |Δb|R) zeros, and this is sharp in
form. So for *general* bounded-squeezing dictionaries the adversary budget
acquires an area term (K−1)·O(a*R²), and the lower bound for area-density
targets saturates at K ≥ 1 + Ω(1/a*) instead of growing with R. We record
this as a calibrated **conjecture** (statement in Appendix D), not a
theorem; the certified results of this note are the common-squeezing case.

**(c) Selectivity.** For the cat target itself the bound is vacuous
(its own zeros are line-density and absorbed by the B(R+δ) term) — correct,
since cats *are* rank 2. The bound has content precisely for targets with
**area-density robust zeros**, the GKP class being the natural candidate
(§7.2). The scaling limit is honest: as a* → 1 or B → ∞ the technique
loses all power.

## 6. Inequivalence of the two compressibilities (certified + empirical)

Target: the thermal lossy cat of experiment 20,
ρ_T = N_σ(E_η(|cat⟩⟨cat|)), η = 0.8, σ = 0.1 (per-quadrature added
variance), α = 1.5, parity +1.

**Theorem C′ (inequivalence).**
(C′1, certified) R_0(ρ_T) = ∞: for **no** η′ ∈ (0,1] does ρ_T admit a
finite-rank pre-loss representation. [Experiment 20, derivation.md,
Lemmas 1–2 and Theorems 1–2: regimes I/II by full-rankness of noise
outputs, the boundary η′ = η−σ by an analytic-kernel linear-independence
argument, regime III by the Bargmann-zero vs Q-positivity obstruction.]
(C′2, certified) χ_G(ρ_T) ≤ 2, hence K_ε^{G,F}(ρ_T) ≤ 2 for all ε:
|cat⟩ has χ_G ≤ 2 and both N_σ and E_η are Gaussian channels; apply
Theorem A′.
(C′3, empirical) R_ε ≤ 2 already at ε = 3.44×10⁻³ / 2.37×10⁻³ / 2.17×10⁻³
(Route B, n_score = 12; the three values are the best-found 1−F at
K = 2/4/8 ket components per rank-2 column; the series over cutoffs
n_score ∈ {8,10,12} is still increasing, so these are cutoff-conditioned
empirical values, not limits).

**Reading.** One and the same state has Gaussian-superposition rank 2 and
pre-loss operator rank ∞: Gaussian classical noise makes operator rank
explode while leaving χ_G untouched (the continuous-ensemble roof absorbs
it). The two compressibility notions are inequivalent, and neither implies
the other's smallness. This recovers, in sharpened form, what experiment 20
actually proved — and corrects an earlier conflation of the two quantities
in this repository's working notes (issue #71, C′3 correction).

## 7. Measured curves (empirical / proxy) and the GKP census (Gate E)

### 7.1 Experiment 22 artifacts

From committed results only (no new fits): the **family-constrained
approximation curve** (synthetic thermal-cat target; rank-2 BB† + loss
family, K ket components per column; all n_score series; labels and
machine-readable `rank_primitive`, `fidelity_convention`, `cutoff_status`,
`epistemic_status` in the JSONs) and the **real-data rank proxy** (held-out
per-sample NLL vs operator mixture rank R = 1..5 on the public GKP homodyne
dataset; true-state fidelity — hence K_ε — is inaccessible on measured
data, and the proxy is labeled as such). The certified-lower-bound panel is
reserved and unpopulated pending Gate E. Figures: experiments/22_kcurves/.

### 7.2 Gate E: robust-zero census for finite-energy GKP

For finite-energy GKP states (square lattice, envelope Δ ∈ {0.2, 0.3, 0.4},
⟨n⟩ ≈ 12.0 / 5.1 / 2.4) the zeros of the Bargmann function in energy
windows R ≲ √⟨n⟩ are located and tested against the robustness threshold of
§5.2, with explicit truncation-tail bounds
(experiments/23_gkp_robust_zeros). Two certification levels, per the
declaration table:

- **D2 (ψ_trunc):** N_robust = 12 / 8 / 4 at the largest windows
  (ε = 10⁻⁴) — the area-density scaling N_robust ~ ⟨n⟩ is measured, with
  all three points nonzero. The bound K ≥ N_robust/C − B(R+δ) certifies
  the renormalized truncated states exactly.
- **D3 (untruncated comb, lifted threshold d(ε)+‖tail‖):** the
  Δ = 0.3 and Δ = 0.4 configurations certify the ideal finite-energy comb
  directly (nonzero N_robust_lifted at ε ≤ 10⁻⁴ and ε ≤ 10⁻³
  respectively); Δ = 0.2 does not lift at the current truncation
  (‖tail‖ = 0.074 > d(10⁻⁴) = 0.010, not repairable below the
  polynomial-root numerical ceiling n_max ≲ 300 of this implementation)
  and remains a ψ_trunc statement.

Robustness activates only for ε ≲ 10⁻³ (at ε = 10⁻² no zero is robust in
any configuration): certified content requires high-fidelity approximation
demands. [EXACT LIFTED VALUES MACHINE-CHECKED AGAINST exp23 JSON — §7.4]

### 7.3½ Claim checker (build gate)

A build script (docs/kepsilon-note/check_claims.py, to be added with the
final draft) verifies every number this note attributes to an artifact —
including numbers asserted inside prose metadata fields such as
`certified_subject` — against the committed JSONs of exp20/22/23. The
lesson behind it: three same-shaped failures (routeB's hardcoded verdict
print, the K-axis conflation, the blanket ψ_trunc declaration) all came
from prose carrying claims that no computation backed. Prose that makes a
claim gets that claim checked.

### 7.3 Quoting policy for Route B numbers

Cutoff series always quoted alongside (8/10/12); headline = largest
scored cutoff; the phrase "cutoff-stable" is not used (the series still
increases); the compressed range "1–2×10⁻³" is deprecated repository-wide.

## 8. Discussion

The world-model question that motivates this repository — *is the world
describable by Gaussian splats?* — here takes a sharpened, answerable form.
The definitions are the community's (χ, χ_δ, r*_ε); what this note adds is
a certified way to say **no at a rate** for bounded dictionaries
(area-density robust zeros defeat line-density zero budgets), an
inequivalence showing that "how many Gaussians" and "what operator rank
before loss" are different questions with opposite answers on the same
state, and measured curves that keep the theory attached to data. The
technique's limits are part of the result: it dies at unbounded
displacement, saturates for general squeezing (plateau conjecture), and is
selective — vacuous exactly on states that *are* Gaussian-compressible.

Open next steps, in charter order: Gate E census (→ §7.2 numbers), the
plateau conjecture, the dynamics program K_ε(t) (issue #97 direction 2),
and the relation between the zero-counting route and the
low-rank-approximation route of [Cottier–Chabaud] — the two see different
obstructions and might compose.

---

## Appendix A. Proof of Lemma A1′

**A.1 Setup.** Fix M modes. Pure Gaussian states form a finite-dimensional
real-analytic manifold 𝒢 (parameterized by covariance/mean or, per mode
pair, by (a, b) with |a| < 1 in the Bargmann form). For K ∈ ℕ let

  S_K := { |ψ⟩ ∈ ℋ, ‖ψ‖ = 1 : |ψ⟩ ∝ Σ_{k=1}^{K} c_k |G_k⟩, |G_k⟩ ∈ 𝒢 }.

**A.2 Measurability.** The map Φ_K : 𝒢^K × ℂ^K → ℋ,
Φ_K(G_1..G_K, c) = Σ c_k |G_k⟩, is continuous (Gaussian states depend
continuously on parameters in norm; finite sums preserve continuity). S_K
is the image of the Borel set {‖Φ_K‖ ≠ 0} under normalization composed
with Φ_K, i.e. an analytic subset of the unit sphere of ℋ (continuous
image of a Polish space). Analytic sets are universally measurable, so
{ψ : χ_G(ψ) ≤ K} = S_K (mod phase) is universally measurable, and
χ_G(·) = min{K : ψ ∈ S_K} (with min ∅ = ∞) is a universally measurable
function into ℕ_{≥1} ∪ {∞}. For a generalized ensemble (standard Borel
index space, measurable pure-state field) the composition i ↦ χ_G(ψ_i) is
measurable for the completed measure, and ess sup_i χ_G(ψ_i) is
well-defined.

**A.3 Attainment of the outer infimum.** The roof objective takes values
in the discrete set ℕ_{≥1} ∪ {∞}. Let m := inf over decompositions of the
ess sup. If m = ∞ there is nothing to attain. If m < ∞, some decomposition
has ess sup < m + 1, i.e. ≤ m, i.e. = m by definition of the infimum.
(The ensemble set is nonempty: the spectral decomposition is a countable
generalized ensemble.)

**A.4 Monotonicity in ε and K_0 = χ_G.** The feasible set
{σ : F(ρ,σ) ≥ 1−ε} grows with ε, so the min is non-increasing. At ε = 0,
F(ρ,σ) = 1 ⟺ ρ = σ for density operators, so K_0^{G,F}(ρ) = χ_G(ρ). ∎

## Appendix B. Re-derivation of the disk zero bound

Following [Friedland, arXiv:2606.24823, Lemma 3.2 and Lemma B.1]; both
steps were independently audited in the T1 round-2 reviews (issue #71).
The only external input is the classical interval Turán inequality:

**Input (interval Turán).** For a nonzero exponential sum
q(t) = Σ_{k=1}^{m} a_k e^{μ_k t} restricted to a real interval I of length
L, and a subinterval J ⊂ I,

  sup_I |q| ≤ e^{L·max_k|Re μ_k|} (c L / |J|)^{m−1} sup_J |q|,

with c an absolute constant. [Classical; also subsumed by the
Turán–Nazarov inequality, Friedland–Yomdin arXiv:1107.0039, Thm 1.1.]

**B.1 Disk growth (Friedland Lemma 3.2).** For q as above, z₀ ∈ ℂ,
0 < r ≤ R, σ := max_k |μ_k|:

  sup_{D(z₀,R)} |q| ≤ e^{2Rσ} (C R/r)^{m−1} sup_{D(z₀,r)} |q|.

*Derivation.* Let z* realize the outer sup and w* the point of D(z₀,r)
where |q| is largest on the segment ray through z* — parameterize the line
through z₀ and z* as z = z₀ + sθ with |θ| = 1, s ∈ [−R, R]. On this line
Q(s) := q(z₀ + sθ) is an exponential sum with exponents θμ_k, and
|Re(θμ_k)| ≤ |μ_k| ≤ σ. Apply interval Turán with I of length 2R and
J = the sub-segment of length 2r inside D(z₀,r): sup on I (hence at z*)
is ≤ e^{2Rσ}(cR/r)^{m−1} times the sup on J, which is ≤ the sup on
D(z₀,r). ∎

**B.2 Blaschke step (Friedland Lemma B.1).** Suppose q has N zeros
(with multiplicity) in D̄(z₀,r), q ≢ 0. Write q = B_N · h on D(z₀,8r)
where B_N is the product of the N Möbius factors vanishing at the zeros
(normalized for the disk of radius 8r) and h is zero-free there. Each
Möbius factor has modulus ≤ θ < 1 (an absolute constant) on D̄(z₀,r) and
= 1 on ∂D(z₀,8r), so

  sup_{D(z₀,r)} |q| ≤ θ^N sup_{D(z₀,8r)} |q|
                   ≤ θ^N e^{16 r σ} (8C)^{m−1} sup_{D(z₀,r)} |q|,

using B.1 at radii (8r, r). Dividing by the (nonzero) sup and taking
logarithms: N log(1/θ) ≤ 16 r σ + (m−1) log(8C), i.e.

  **N ≤ C′ (m + σ r)** with C′ absolute. ∎

## Appendix C. Interconversion with χ_δ of HTFY on pure states

HTFY define χ_δ(|ψ⟩) = inf{ χ(|ψ′⟩) : ‖ψ − ψ′‖ < δ } (vector-norm ball).
For normalized ψ, ψ′ with optimally aligned phases,
‖ψ−ψ′‖² = 2(1 − |⟨ψ|ψ′⟩|) and F = |⟨ψ|ψ′⟩|², so a fidelity ball
F ≥ 1−ε equals a norm ball of radius d(ε) = √(2−2√(1−ε)):

  K_ε^{G,F}(|ψ⟩⟨ψ| restricted to pure approximants) = χ_{d(ε)}(|ψ⟩),

up to the open/closed ball convention. Two caveats keep this from being an
identity of the full quantities: (i) our K_ε permits **mixed** approximants
σ, which can only lower the min (on pure targets, if a mixed σ with roof
value K satisfies ⟨ψ|σ|ψ⟩ ≥ 1−ε, the averaging argument of Theorem B′
produces a pure member with the same K and fidelity, so the two agree on
pure targets); (ii) HTFY's χ counts superpositions only, matching our
pure-state χ_G. On mixed targets the quantities differ by construction
(roof vs no natural χ_δ analogue), and no identification is claimed.

## Appendix D. The plateau conjecture for general bounded-squeezing dictionaries

**Calibrating examples (certified).** (i) e^{a z²/2} − 1 (two components
with squeezing gap a) has ≈ |a|R²/π zeros in D(0,R), including a double
zero at 0. (ii) More generally, for two components with parameter gaps
(Δa, Δb), zeros solve Δa·z²/2 + Δb·z ∈ iπ(2ℤ+1); counting lattice points
of spacing 2π hit by a degree-2 polynomial image of the disk gives
N ≤ c(|Δa| R² + |Δb| R), sharp in form. Any general-dictionary zero bound
must therefore carry an area term a* R².

**Conjecture D.** For f = Σ_{k=1}^{K} c_k e^{a_k z²/2 + b_k z + d_k} with
|a_k| ≤ a* < 1, |b_k| ≤ B, f ≢ 0, in minimal representation:

  N(D̄(z₀,R); f) ≤ C (K − 1)(1 + a* R² + B R).

**Consequence if true.** For an area-density target
(N_robust ~ ρ₀ R², ρ₀ ≤ 1/π) the Theorem-B′-style bound saturates:
K ≥ 1 + ρ₀/(C a*) as R → ∞ — a plateau inversely proportional to the
squeezing budget, instead of unbounded growth. The certified results of
this note are the a-common slice, where the area term cancels exactly
(§4); the conjecture marks where the technique's power ends, not where the
states become easy.

**Status.** Statement calibrated by the examples above (T1, issue #71);
proof route sketched via the order-K linear ODE with polynomial
coefficients satisfied by f (Wronskian = (Π_k f_k)·Q with deg Q ≤
K(K−1)/2) and disconjugacy on disks avoiding Q's zeros; the naive complex
Chebyshev shortcut is false (W[1, e^{μz}] never vanishes while e^{μz}−1
has ~Rμ/π disk zeros), so coefficient bounds must enter. Left open.

## References

Primary-source verification status per repository policy: [pdf] = read in
PDF/HTML by this project; [stmt] = the specific cited statement was
transcribed and checked; remaining items to re-verify at final draft.

1. K. Hahn, R. Takagi, G. Ferrini, H. Yamasaki, *Classical simulation and
   quantum resource theory of non-Gaussian optics*, arXiv:2404.07115;
   Quantum 9, 1881 (2025). [pdf][stmt: χ, χ_δ, ξ definitions; convex-roof
   mixed extension; monotonicity under Gaussian unitaries/measurements]
2. K. Hahn, A. Garnier, G. Ferrini, A. Ferraro, U. Chabaud, *Assessing
   non-Gaussian quantum state conversion with the stellar rank*,
   arXiv:2410.23721; Quantum 10, 2095 (2026). [pdf][stmt: Def. 7 r*_ε;
   Thm 1 monotonicity; convex-roof mixed stellar rank]
3. F. Cottier, U. Chabaud, *Lower Bounds on Coherent State Rank*,
   arXiv:2604.00766 (2026). [pdf-abstract][stmt: ε-approximate coherent
   state rank; low-rank-approximation and permanent-complexity lower
   bounds; single-mode characterization] — full-text re-read scheduled at
   final draft (technique comparison in §8).
4. O. Friedland, *A Disk-Growth Remez Principle and a Modular Proof of the
   Measurable Turán-Nazarov Inequality*, arXiv:2606.24823 (2026).
   [stmt: Lemma 3.2, Lemma B.1 — audited by two independent reviews;
   re-derived in Appendix B]
5. O. Friedland, Y. Yomdin, *An observation on Turán-Nazarov inequality*,
   arXiv:1107.0039. [pdf][stmt: Thm 1.1 interval Turán–Nazarov]
6. M. Motamedi et al., *The stellar decomposition of Gaussian quantum
   states*, arXiv:2504.10455. [stmt: Bargmann parameter table, cross-check
   of a = −e^{iφ}tanh r, b = α − aα*]
7. Experiment 20 derivation note (this repository,
   experiments/20_noninclusion/derivation.md): Lemmas 1–2, Theorems 1–2.
   [in-repo, PR-64-reviewed]
8. Experiments 22–23 artifacts (this repository): exp22 curves JSON,
   exp23 robust-zero census JSON. [in-repo, reviewed]
9. Preprint: W. Kawashima, *Compact physical Gaussian-ket models for
   homodyne quantum-state tomography* (2026), doi:10.5281/zenodo.21457049.
   [v2 planned with this note; erratum for the Route B quoting]
