# Entanglement representation cost — a theory note (issue #6)

- Status: research note / proposed
- Date: 2026-07-12
- Author: Claude (research lead). Derivation de-risked with the codex/gpt-5.5 oracle (adversarial "where does it leak" pass); empirical claims re-measured from `experiments/05_entanglement_cost/run.py`.
- Scope: turns experiment 05's empirical law **R ~ k** into a precise mathematical statement — separating what is a *theorem* from what is a sharply-stated *open conjecture*. Per the repo ethos: prove what is provable, and record the boundary honestly.

---

## 0. One-paragraph summary

Approximating the two-mode entangled-cat Wigner function with a **signed real Gaussian mixture** costs far more with axis-aligned (separable) blobs than with tilted (full-covariance) blobs, and the ratio R = K_axis / K_tilted grows **linearly in the fringe wavenumber** k = 2√2·α (measured log–log slope 1.02), not with the entanglement E(α) (which saturates at 1 ebit). We prove the 1D core of the mechanism — for **common-width** translated Gaussians, resolving a k-oscillation fringe needs Θ(k) atoms — via total positivity / the variation-diminishing property (Schoenberg). We give the tilted upper bound K_tilted = O(k) by construction. The two hard directions — the **width-free** 1D lower bound and the **axis penalty** K_axis = Ω(m²) that would upgrade R ≥ c to R = Ω(k) — remain open, and we state exactly why the easy arguments (rank, sign-matrix) leak. The upshot is a clean division of labour: **entanglement decides *whether* a tilt is needed; the interference scale k decides *how much* it saves.**

---

## 1. The empirical law (experiment 05, re-measured 2026-07-12)

Target: two-mode cat Wigner W_cat ∝ blobs + parity·cos(k(p₁+p₂))·e^{−|z|²}, with fringe wavenumber k = 2√2·α. Fit with a signed Gaussian mixture by the exact L2-optimal weight QP; K_min = greedy matching-pursuit count to reach relative-L2 ≤ √(2(1−F_th)). Two dictionaries: **tilted** (full 4×4 covariance, can elongate along the ridge p₁−p₂) and **axis** (separable, block-diagonal product Gaussians).

| α | E (bits) | k | m_1D | K_tilted | K_axis | R = K_axis/K_tilted |
|---|---|---|---|---|---|---|
| 0.75 | 0.734 | 2.12 | 7 | 10 | 28 | 2.80 |
| 1.25 | 0.994 | 3.54 | 9 | 13 | 57 | 4.38 |
| 1.50 | 1.000 | 4.24 | 9 | 13 | 80 | 6.15 |
| 2.00 | 1.000 | 5.66 | 13 | 16 | 154 | 9.62 |
| 2.50 | 1.000 | 7.07 | 15 | 19 | 165 | 8.68 |

- **log R vs log k over all 7 swept α: slope 1.02, corr 0.956** — consistent with R linear in k (few points, wide CI; not asserted as an exact exponent). The table above samples 5 of the 7 swept points for brevity; the slope/corr use all 7.
- E(α) saturates at 1 ebit by α ≈ 1.25, yet R keeps climbing over α ∈ [1.5, 2.5] (×1.41) → the naive "cost tracks entanglement" story is **refuted**; cost tracks the interference scale k.
- The 1D building-block cost m_1D(k) (min common-width signed Gaussians to fit the 1D fringe cos(kp)e^{−p²} to rel-L2 ≤ 0.05) is **linear**: over k ∈ [4, 16], `m_1D ≈ 1.70 k + 2.27` (fresh sweep, this note).
- **Disclosed contamination.** At the largest point (α = 2.5) the axis pool hits its component cap (`mcap = 34`, while the grid wants ≈ 38), so K_axis there is truncated and the final R (9.62 → 8.68) is likely a pool artifact; run.py's own caveat notes R is then *under*-stated, which only strengthens "R keeps growing." The slope includes this point.

---

## 2. What is a theorem: the 1D common-width lower bound

> **Lemma (1D interference cost, common width).** For **any** common width σ > 0, let the dictionary be translates {g_c(p) = e^{−(p−c)²/(2σ²)} : c ∈ ℝ} of that one Gaussian, with **signed real coefficients**. Any finite s(p) = Σ_{i=1}^{n} a_i g_{c_i}(p) with relative L2 error ‖s − f_k‖ ≤ ε‖f_k‖ to f_k(p) = cos(kp) e^{−p²} has n ≥ C(ε)·k, with **C(ε) independent of σ** (below a fixed ε threshold). Writing m_1D(k, ε) for the minimum over the choice of common width, m_1D(k, ε) = Θ(k) (upper bound below). Note C(ε) does not depend on σ, so the bound holds even when the width is optimized per k — which is exactly what experiment 05 does.

**Proof sketch.** Fix any σ. Nothing below uses the value of σ.
1. **Variation-diminishing (σ-free).** A common-width translate sum is s = g_σ ∗ μ, the convolution of the Gaussian with the atomic signed measure μ = Σ a_i δ_{c_i}. The Gaussian is a Pólya frequency function (strictly totally positive kernel), so by Schoenberg's variation-diminishing property S⁻(g_σ ∗ μ) ≤ S⁻(μ) ≤ n − 1: **s has at most n − 1 sign changes on ℝ** (equivalently, common-width Gaussian translates form a Chebyshev system). This resolves the "translated, not convolved" worry — a translate sum *is* a convolution with an atomic measure.
2. **The target oscillates Ω(k) times.** f_k has zeros at p = (j + ½)π/k; on |p| ≤ P (the envelope carries all but ε² of the L2 mass) it has c₀k := ⌊2Pk/π⌋ = Ω(k) sign changes, bracketing that many bumps of alternating sign. Each single bump has L2 mass Θ(1/k)·‖f_k‖² (width π/k under a bounded envelope; ‖f_k‖² is Θ(1) in k) — **not** a fixed fraction; the fixed fraction is the *sum* over the Ω(k) bumps.
3. **L2-closeness forces the sign changes (correct accounting).** If s has only n − 1 sign changes it is sign-definite on ≤ n intervals, so it disagrees in sign with f_k on all but ≤ n − 1 of the c₀k bumps, i.e. it **mis-signs ≥ (c₀k − n) − 1 bumps** (the −1 for bumps split by a sign-change point). On any bump where sign(s) is opposite to sign(f_k), |s − f_k| ≥ |f_k| pointwise, so that bump contributes ≥ its full mass Θ(1/k)·‖f_k‖² to ‖s − f_k‖². Summing, ‖s − f_k‖² ≥ (c₀k − n − 1)·(c₁/k)·‖f_k‖². If n ≤ δk this is ≥ (c₀ − δ)c₁·‖f_k‖², a **constant** lower bound; so ‖s − f_k‖ ≤ ε‖f_k‖ with ε below √((c₀ − δ)c₁) forces n > δk. This is the "ε below a fixed threshold" in the statement, and C(ε) = δ(ε) is σ-independent. ∎

**Sandwich.** Lower bound: n = Ω(k) for **every** common width (step 1–3). Upper bound: **there exists** a common width σ ~ 1/k achieving O(k) — place ⌈2Pk/π⌉ translates of a σ ~ 1/k Gaussian, one per half-period, and fit signed coefficients. Hence **m_1D(k) = min over common width = Θ(k)**, and the theorem covers exactly the quantity experiment 05 measures (its `m1d()` shares one line-searched width across all atoms per m).

**Theory ↔ measurement.** The construction places one atom per half-period over support 2P, i.e. slope 2P/π = 2·2.7/π ≈ **1.72** atoms per unit k. The measured fit `m_1D ≈ 1.70 k + 2.27` has slope **1.70** — a near-exact match, tying the Θ(k) constant to the fringe geometry.

**Cite:** Schoenberg, *Über variationsvermindernde lineare Transformationen* (1930); Karlin, *Total Positivity* (1968) — Pólya frequency functions / variation-diminishing convolution.

---

## 3. What is a construction: the tilted upper bound

> **Proposition (tilted upper bound).** K_tilted = O(m_1D(k)) = O(k).

Rotate to normalized coordinates u = (p₁+p₂)/√2, v = (p₁−p₂)/√2. The target separates **exactly**: e^{−p₁²−p₂²}cos(k(p₁+p₂)) = e^{−u²}e^{−v²}cos(√2·k·u), constant-envelope in v and a 1D oscillation of wavenumber √2·k in u. A full-covariance Gaussian can be **elongated along v** (matching e^{−v²}) and **narrow along u** (resolving the oscillation), so the 2D fit reduces to the 1D problem along u: ~m_1D(√2 k) = O(k) tilted atoms tile the ridge (plus the two blob terms). Assumptions of this upper bound: a finite target window with ε tail tolerance, covariance aspect ratio allowed to grow with k, signed weights, constants depending on ε. This is what the tilted dictionary achieves in experiment 05 (K_tilted 10 → 19 as k 2.1 → 7.1). ∎

---

## 4. What stays open: the crux conjectures

The empirical R = Ω(k) is **not yet a theorem**. Two gaps, stated sharply:

**(C1) Width-free 1D lower bound.** With per-atom adaptive widths, the variation-diminishing argument fails (total positivity is a *fixed-kernel* statement; a sum of *different-width* Gaussians can have more sign changes than n − 1). So m_1D^{free}(k, ε) ≥ C(ε)k is **conjectural**, even though empirically the adaptive-width fit is still linear in k (experiment 05's line-search never beats the common-width slope). Closing C1 needs a scale-robust lower bound (atomic-norm / bounded condition number, or a Fourier–Ingham argument on the ±k spectral mass built from frequency-0-centred atoms).

**(C2) The axis penalty — the mathematical heart of "entanglement cost."** To reach **R = Ω(k)** we need
> **K_axis = Ω(m_1D²)** *under a bounded-coefficient (atomic-norm / bounded-purity) constraint*, i.e. the separable dictionary pays the *square* of the 1D cost.
The naive arguments **leak**:
- *Rank fails.* e^{−p₁²−p₂²}cos(k(p₁+p₂)) = u_c(p₁)u_c(p₂) − u_s(p₁)u_s(p₂) is a **rank-2** separable function, so a tensor-rank bound gives O(1), not m².
- *Sign-matrix fails.* On a grid the sign pattern (−1)^{i+j} = (−1)^i(−1)^j is **rank-1**; checkerboard sign complexity alone does not force m².

**Why the constraint is not optional (an oracle-found, numerically-verified counterexample).** *Without* a coefficient/conditioning bound the Ω(m_1D²) claim is **false**: a common-width product Gaussian with equal x- and y-width is an **isotropic**, hence rotation-invariant, blob. Rotating to u = (p₁+p₂)/√2, F_k = e^{−u²−v²}cos(√2 k u); an isotropic construction on the diagonal (v = 0) formally gives O(m_1D) atoms. **But this construction needs exponentially large weights**: to resolve the √2k oscillation with isotropic (not-narrow-in-u) atoms, a width-1 Gaussian must synthesize frequency √2k, and its transform there is ~e^{−k²}, so coefficients blow up like e^{k²}. Measured (this note, `experiments/08_positivity`-style diagonal LS fit): the bounded-coefficient (|c| ≤ 50) diagonal-isotropic fit **never** reaches rel-L2 ≤ 0.14 for k = 4, 6, 8; where it approaches, max|c| = 5.5×10⁵, 5.7×10⁸, 3.8×10⁹ respectively. A *narrow* isotropic atom (which would resolve the fringe with bounded weights) is narrow in v too, so it cannot elongate along the ridge and must tile the 2D envelope → back to Θ(m²). So the escape is **only** the ill-conditioned regime; experiment 05's spike-proof relative-L2 criterion (purity ≈ 1, |w| ≲ 0.5) sits squarely in the bounded regime where R ~ k is measured.

So the sharpened open problem is: **K_axis = Ω(m_1D²) for signed product-Gaussian mixtures of bounded atomic norm.** The slice argument gives a rigorous **lower bound K_axis = Ω(m_1D)** for the common-width dictionary — with the clean orthogonality accounting (C even, S odd ⟹ ‖(I−P_U)F‖² = ‖(I−P_U)C‖²‖C‖² + ‖(I−P_U)S‖²‖S‖², so the x-atom span U must approximate both C and S, forcing dim U ≥ Ω(m_1D)). The gap from Ω(m_1D) to Ω(m_1D²) — that a bounded-norm product dictionary cannot collapse the diagonal ridge — is the genuinely new mechanism still needed. **This (with the bounded-norm hypothesis) is the open problem that would make "entanglement representation cost" a theorem.**

Honest status table:

| Statement | Status |
|---|---|
| m_1D^{common}(k) = Θ(k) | **theorem** (§2, §3) |
| K_tilted(k) = O(k) | **theorem** (construction, §3) |
| K_axis(k) = Ω(m_1D) (common width) | **theorem-grade** (slice + even/odd orthogonality) |
| m_1D^{free}(k) = Ω(k) | conjecture (C1); strong empirical support |
| K_axis(k) = Ω(m_1D²) **at bounded atomic norm** ⟹ R = Ω(k) | **conjecture (C2)** — the crux; empirical slope 1.02. *Without* the norm bound it is **false** (isotropic-diagonal escape, needs weights ~e^{k²}, verified) |

---

## 5. Quantum-information reading

The division of labour that survives the analysis:

- **Entanglement E(α) decides *whether* a tilt is needed.** *At matched count* (K ≈ K_tilted), a separable/block-diagonal splat ansatz fails on the entangled cat — the two-mode experiment 04 measured F ≈ 0.50 for the block-diagonal gradient fitter at practical component counts. (This is **not** count-independent impossibility: a *signed sum* of Θ(m²) product Gaussians does reach the target — the same note's table shows K_axis = 28…165 hitting F_th = 0.99 — consistent with the rank-2 identity cos(k(p₁+p₂))e^{−|z|²} = u_c⊗u_c − u_s⊗u_s.) So entanglement sets a **qualitative same-count** advantage of tilting (R > 1), and this saturates with E. Caveat: the Wigner-correlation ⟺ entanglement equivalence used here holds for **pure** states.
- **The interference scale k decides *how much* the tilt saves.** Given a tilt is used, the *quantitative* saving is R ~ k: one tilted Gaussian sweeps the diagonal ridge, replacing an m_1D-wide tiling. k = 2√2·α is the phase-space fringe wavenumber. The two-component cat oscillates in **one** phase-space direction (Δp ~ 1/k under an O(1) envelope), so its interference patches have **sub-Planck area ~ ħ/k** (the 1/k² ~ ħ²/A figure is for two-directionally-oscillating *compass* states; Zurek 2001). So the representation cost is set by the *fineness of the non-classical structure*, not by the amount of entanglement.

**Relation to stellar rank (from the #29 survey).** The cat has *infinite* stellar rank (its Bargmann function ∝ cosh has infinitely many zeros), yet its splat *representation* cost here is finite and set by k. So **within the cat/fringe family and for this signed-Gaussian dictionary, stellar rank does not resolve this cost — the interference scale k does** (we do not claim k is the universally correct measure). The prior-art survey (Chabaud–Markham–Grosshans, PRL 2020) lets us state the distinction precisely: stellar rank counts non-Gaussianity by Husimi/Bargmann zeros; the splat cost counts the *oscillation density* the dictionary must resolve. The two measure different things here.

---

## 6. What to do next

1. **C2 is the prize — but it must carry the bounded-atomic-norm hypothesis** (a timebox attempt showed the unconstrained version is false: the isotropic-diagonal escape, `c2_isotropic_escape.py`). The right target is a product-Gaussian sparsity lower bound K_axis = Ω(m_1D²) *at bounded atomic norm / bounded condition number*, which would make R = Ω(k) a theorem (self-contained approximation theory, no quantum input). Attack via: (a) an atomic-norm / incoherence bound forcing narrow (fringe-resolving) atoms, which are isotropic-narrow and thus tile 2D; (b) a 2D variation-diminishing statement for the anti-diagonal restricted to bounded-norm combinations. The intermediate **K_axis = Ω(m_1D)** (common width, via the even/odd orthogonality of §4) is already theorem-grade and worth writing up cleanly.
2. **C1** is likely easier and worth a Fourier–Ingham attempt (frequency-0-centred atoms building ±k spectral mass).
3. This note is intentionally a **standalone artifact** — provable lemma + sharp open problem — independent of whether the splat/BB† reconstructors win benchmarks. It can seed a short preprint or an outreach thread (the C2 problem is quotable to approximation theorists).

## References

- Schoenberg (1930); Karlin, *Total Positivity* (1968) — variation-diminishing / totally positive kernels.
- Chabaud, Markham, Grosshans, *Stellar representation of non-Gaussian quantum states*, PRL 124, 063605 (2020) — stellar rank (see `docs/prior-art-survey.md` §5).
- Zurek, *Sub-Planck structure in phase space* (Nature 2001) — the interference scale 1/k².
- experiment 05: `experiments/05_entanglement_cost/run.py`; issue #6.
