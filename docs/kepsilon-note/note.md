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

### 7.2 Gate E: robust-zero census for finite-energy GKP (pending)

For finite-energy GKP states (square lattice, envelope Δ), the robust-zero
count in the energy window R ≲ √⟨n⟩ is computed numerically with explicit
truncation-tail bounds (experiments/23_gkp_robust_zeros, in progress).
Candidate statement to be instantiated: for a GKP state of mean photon
number ⟨n⟩ and a dictionary G_eq(a,B),

> K_ε^{G_eq(a,B),F} ≥ N_robust(R,δ,ε)/C − B(R+δ), R ~ √⟨n⟩,

with N_robust read from the census table. Until that table exists, "the
bound has content for GKP" is a **candidate application, not a theorem**
(T1 review, fix 5). [NUMBERS PENDING GATE E]

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

## Appendix A. Proof of Lemma A1′ [TO WRITE IN FULL — sketch in §3 verified at T1]

## Appendix B. Re-derivation of the disk zero bound [TO WRITE — chain verified by both T1 reviewers; external input reduced to classical interval Turán]

## Appendix C. Interconversion with χ_δ of HTFY on pure states [SHORT]

## Appendix D. The plateau conjecture for general bounded-squeezing dictionaries [STATEMENT + counterexample calibration from T1]

## References [TO COMPILE — all primary-source verified per repository policy: HTFY 2404.07115; Hahn et al. 2410.23721; Cottier–Chabaud 2604.00766; Friedland 2606.24823; Motamedi et al. 2504.10455 (Bargmann parameter table); classical Turán; exp20 derivation; exp22 artifacts]
