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

- **log R vs log k: slope 1.02, corr 0.956** → R grows linearly in k.
- E(α) saturates at 1 ebit by α ≈ 1.25, yet R keeps climbing over α ∈ [1.5, 2.5] (×1.41) → the naive "cost tracks entanglement" story is **refuted**; cost tracks the interference scale k.
- The 1D building-block cost m_1D(k) (min common-width signed Gaussians to fit the 1D fringe cos(kp)e^{−p²} to rel-L2 ≤ 0.05) is **linear**: over k ∈ [4, 16], `m_1D ≈ 1.70 k + 2.27` (fresh sweep, this note).

---

## 2. What is a theorem: the 1D common-width lower bound

> **Lemma (1D interference cost, common width).** Fix a width σ > 0 and let the dictionary be translated real Gaussians {g_c(p) = e^{−(p−c)²/(2σ²)} : c ∈ ℝ} with **signed real coefficients**. Any finite signed combination s(p) = Σ_{i=1}^{n} a_i g_{c_i}(p) that approximates f_k(p) = cos(kp) e^{−p²} to relative L2 error ≤ ε (ε below a fixed threshold) has n = Ω(k). Equivalently m_1D^{σ}(k, ε) ≥ C(ε)·k.

**Proof sketch (rigorous for common width).**
1. **Variation-diminishing.** The Gaussian is a strictly totally positive kernel; by Schoenberg's variation-diminishing property, a linear combination of n translates of a fixed-width Gaussian changes sign at most n − 1 times. Hence s has at most n − 1 sign changes (zeros with sign change) on ℝ.
2. **The target oscillates Ω(k) times.** f_k has zeros at p = (j + ½)π/k; on its effective support |p| ≤ P (where the envelope carries all but ε² of the L2 mass) it has ⌊2P k/π⌋ = Ω(k) sign changes, each bracketing a bump of definite sign whose L2 mass is a fixed fraction of ‖f_k‖².
3. **L2-closeness forces the sign changes.** On any maximal interval where s keeps a constant sign but f_k completes a full bump of the opposite average sign, ‖s − f_k‖²_{that interval} is bounded below by a fixed fraction of that bump's mass. If s has only n − 1 sign changes it is sign-definite on n intervals and thus "misses" ≥ (Ω(k) − n) bumps, so ε²‖f_k‖² = ‖s − f_k‖² ≥ (Ω(k) − n)·(bump mass). For ε small enough this forces n ≥ C(ε)·k. ∎

**Sandwich.** The matching upper bound m_1D^{σ}(k) = O(k) is immediate by construction (place ~2Pk/π narrow Gaussians of width σ ~ 1/k along the support, one per half-period). Hence **m_1D^{σ}(k) = Θ(k)** for common width — matching the measured `1.70 k + 2.27`. The measured m_1D in experiment 05 *is* a common-width quantity (one width is line-searched per m, shared by all atoms), so the theorem covers exactly the quantity plotted.

**Cite:** Schoenberg, *Über variationsvermindernde lineare Transformationen* (1930) and total-positivity theory (Karlin, *Total Positivity*, 1968); the Gaussian-translate kernel's strict total positivity.

---

## 3. What is a construction: the tilted upper bound

> **Proposition (tilted upper bound).** K_tilted = O(m_1D(k)) = O(k).

Rotate to (u, v) = (p₁+p₂, p₁−p₂). The fringe cos(k u /√2·√2)… is constant in v and a 1D oscillation in u. A full-covariance Gaussian can be **elongated along v** (matching the envelope) and **narrow along u** (resolving the oscillation), so the 2D problem factorizes into the 1D problem along u: ~m_1D(k) tilted atoms tile the ridge. This is a one-sided (upper) bound and is what the tilted dictionary achieves in experiment 05 (K_tilted 10 → 19 as k 2.1 → 7.1). ∎

---

## 4. What stays open: the crux conjectures

The empirical R = Ω(k) is **not yet a theorem**. Two gaps, stated sharply:

**(C1) Width-free 1D lower bound.** With per-atom adaptive widths, the variation-diminishing argument fails (total positivity is a *fixed-kernel* statement; a sum of *different-width* Gaussians can have more sign changes than n − 1). So m_1D^{free}(k, ε) ≥ C(ε)k is **conjectural**, even though empirically the adaptive-width fit is still linear in k (experiment 05's line-search never beats the common-width slope). Closing C1 needs a scale-robust lower bound (atomic-norm / bounded condition number, or a Fourier–Ingham argument on the ±k spectral mass built from frequency-0-centred atoms).

**(C2) The axis penalty — the mathematical heart of "entanglement cost."** To upgrade R ≥ c (a constant separation, reachable) to **R = Ω(k)** we need
> **K_axis = Ω(m_1D²)**, i.e. the separable dictionary pays the *square* of the 1D cost.
This is where the naive arguments **leak** (oracle-confirmed):
- *Rank fails.* e^{−p₁²−p₂²}cos(k(p₁+p₂)) = u_c(p₁)u_c(p₂) − u_s(p₁)u_s(p₂) is a **rank-2** separable function, so a tensor-rank bound gives O(1), not m².
- *Sign-matrix fails.* On a grid the sign pattern (−1)^{i+j} = (−1)^i(−1)^j is **rank-1**; checkerboard sign complexity alone does not force m².
A slice argument gives only K_axis = Ω(m_1D) (evaluate along one mode). The Ω(m_1D²) lower bound — the statement that a product-Gaussian dictionary *cannot* exploit the diagonal ridge and must tile the full 2D grid — requires a genuinely new lower-bound mechanism (product-dictionary sparsity, not tensor rank). **This is the open problem that would make "entanglement representation cost" a theorem.**

Honest status table:

| Statement | Status |
|---|---|
| m_1D^{common}(k) = Θ(k) | **theorem** (§2, §3) |
| K_tilted(k) = O(k) | **theorem** (construction, §3) |
| m_1D^{free}(k) = Ω(k) | conjecture (C1); strong empirical support |
| K_axis(k) = Ω(m_1D²) ⟹ R = Ω(k) | **conjecture (C2)** — the crux; empirical slope 1.02 |

---

## 5. Quantum-information reading

The division of labour that survives the analysis:

- **Entanglement E(α) decides *whether* a tilt is needed.** A separable (product) Wigner ansatz fails *qualitatively* on the entangled cat — the two-mode experiment measured F = 0.50 for block-diagonal splats regardless of count, because the cross-mode ridge cannot be represented by any product of per-mode Gaussians at leading order. This is a 0/1 fact set by entanglement, and it saturates with E.
- **The interference scale k decides *how much* the tilt saves.** Given that a tilt is needed, the *quantitative* saving is the ratio R ~ k: one tilted Gaussian sweeps the whole diagonal ridge, replacing an m_1D-wide tiling per mode. k = 2√2·α is the phase-space fringe wavenumber, i.e. the inverse of the **sub-Planck** interference scale (area ~ 1/k² ≪ ħ; Zurek). So the representation cost is set by the *fineness of the non-classical structure*, not by the amount of entanglement.

**Relation to stellar rank (from the #29 survey).** The single-mode cat has *infinite* stellar rank, yet its *representation* cost here is finite and set by k. So stellar rank is **not** the right complexity measure for this cost — the interference scale k is. This is a clean distinction the prior-art survey (Chabaud–Markham–Grosshans, PRL 2020) lets us state precisely: stellar rank counts non-Gaussianity by Husimi zeros; the splat cost counts the *oscillation density* the signed-Gaussian dictionary must resolve. The two coincide for low-rank core states but diverge for cats.

---

## 6. What to do next

1. **C2 is the prize.** A product-Gaussian-dictionary sparsity lower bound K_axis = Ω(m_1D²) would make R = Ω(k) a theorem and is a self-contained approximation-theory problem (no quantum input). Attack via: (a) a 2D variation-diminishing / total-positivity statement for product kernels along the anti-diagonal; (b) an incoherence/atomic-norm bound on the separable dictionary restricted to the ridge.
2. **C1** is likely easier and worth a Fourier–Ingham attempt (frequency-0-centred atoms building ±k spectral mass).
3. This note is intentionally a **standalone artifact** — provable lemma + sharp open problem — independent of whether the splat/BB† reconstructors win benchmarks. It can seed a short preprint or an outreach thread (the C2 problem is quotable to approximation theorists).

## References

- Schoenberg (1930); Karlin, *Total Positivity* (1968) — variation-diminishing / totally positive kernels.
- Chabaud, Markham, Grosshans, *Stellar representation of non-Gaussian quantum states*, PRL 124, 063605 (2020) — stellar rank (see `docs/prior-art-survey.md` §5).
- Zurek, *Sub-Planck structure in phase space* (Nature 2001) — the interference scale 1/k².
- experiment 05: `experiments/05_entanglement_cost/run.py`; issue #6.
