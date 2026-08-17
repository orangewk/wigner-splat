# The c=3 weak envelope bound (S4-Ew) — a self-contained summary

Date: 2026-08-17 / Author: mainline / status: **wip — summary, non-normative**

> **Status of the result.** Everything stated here is a **proof draft: cross-checked by multiple LLMs,
> internally reviewed at fixed commit SHAs, and awaiting independent external re-review.**
> The sole authoring location of the S4-program proof drafts (S4a/S4b/S4c) summarized here is the
> [FR document](2026-08-10-three-atom-block-frame-preparation--wip.md) §10 (v0.15, in Japanese);
> the predecessor kernels (QR5, the K2 family) are authored in their own predecessor documents (§8);
> in case of any discrepancy the FR document prevails. This summary introduces no new claims.

## 1. Background

Within the Gaussian border-rank closure program
([closure draft](2026-08-02-gaussian-border-rank-closure--wip.md), draft PR #178), Lemma N requires a
cancellation-aware exact frame for the span of colliding Gaussian atoms, subject to seven obligations
FR1–FR7 (FR document §4). For c=3 (three atoms), obligations FR1/FR2/FR4 and FR3(X)(L-d) were closed
earlier (frame constructions FR-S1′/S1″); the last open block was **FR6 — a uniform far-field envelope
bound** — together with FR5/FR7. This note summarizes the statement and proof architecture of the weak
envelope bound (S4-Ew) that closes it, in a form readable without the FR document's history and ledgers.

## 2. Setting

**Fock space.** `ℱ` is the Segal–Bargmann–Fock space of entire functions `f` with
`‖f‖² := (1/π)∫_ℂ |f(z)|²e^{−|z|²}dA(z) < ∞`; orthonormal basis `e_k = z^k/√k!`, reproducing kernel
`K(z,w) = e^{zw̄}`, hence `|f(z)| ≤ ‖f‖e^{|z|²/2}` for every `f ∈ ℱ`.

**Gaussian atoms.** `Φ(A,B)(z) := exp(Az²/2 + Bz)` (an element of `ℱ` whenever `|A| < 1`). Atom
parameters are confined to the compact class

  K_{δ,R} := {|A| ≤ 1−δ} × {|B| ≤ R}   (fixed 0 < δ < 1, R > 0).

The norm has the closed form `‖Φ(A,B)‖² = (1−|A|²)^{−1/2}exp[(|B|²+Re(AB̄²))/(1−|A|²)]`.

**Input (a collision cluster).** A sequence of three atoms `u_{j,m} = Φ(ξ_{j,m})` (`j = 1,2,3`,
`ξ_{j,m} ∈ K_{δ,R}`), `V_m := span{u_{1,m}, u_{2,m}, u_{3,m}}`, with `ξ_{j,m} → ξ*` for all `j`
(a single collision cluster). The collision scale is measured in the weighted metric
`d_w((A,B),(A′,B′)) := max(|A−A′|^{1/2}, |B−B′|)`, and `s̃_m := max_{i,j} d_w → 0` (in the original,
ungauged coordinates). The frame construction uses a common metaplectic gauge `U_m` moving a pivot atom
to the vacuum (an exact unitary preserving spans, norms and Gram matrices).

**Exact block tree.** Frame candidates are exact finite combinations `h_{ℓ,m} = Σ_j a_{ℓj,m}u_{j,m}`
carrying a rooted binary block tree: leaves are atoms, an internal node is an exact sum `H = X + Y`, and
the node envelope along a ray is `U_H(t) := max(log|X(te^{iθ})|, log|Y(te^{iθ})|)`. For c=3 the only
nontrivial shape (up to permutation) is "pair block + singleton" (2+1); its root envelope is written
`U_T`. The normalized frame is `v_{ℓ,m} := h_{ℓ,m}/‖h_{ℓ,m}‖_ℱ` with `r = dim V_m ≤ 3` elements
(construction: FR-S1′/S1″, accepted).

**The difficulty.** In a colliding family the norm of a combination can be far smaller than the norms of
its atoms (deep cancellation). The ratio `D_H := max(‖X‖,‖Y‖)/‖H‖` is expected to be unbounded — a
design note in FR document §10.8 records the *expectation* of blow-up at rate `s̃_m^{−2}` along a
second-difference configuration (the rate itself is an unproven design motivation; numerical
diagnostics exhibit configurations with `D_H ≈ 7×10⁵`). So summing
trivial per-atom bounds cannot give an m-uniform envelope for the *normalized* combinations; a mechanism
that preserves cancellation is required.

## 3. Main result

**Lemma (S4-Ew)** (FR document §10.8, Lemma EW; accepted at `b39216f`; per the status note above this
is a **proof draft**, not claimed as an established theorem): For the input above there
exist constants `C_w, C_lin > 0` and a threshold `m₀` such that for all `m ≥ m₀`, every frame index `ℓ`,
and every `z ∈ ℂ`,

  |(U_m^{−1}v_{ℓ,m})(z)| ≤ C_w · exp((1−δ/2)|z|²/2 + C_lin|z|).

The constants `C_w, C_lin` depend only on `(δ, R, ε_chain, C_T, C_RF)` (the uniform constants of §6) and
are independent of `m, ℓ, z, θ` and of all representation coefficients (SVD/Newton coefficients). The
threshold `m₀` may depend on the convergence speed of the input sequence (the target (E-w) only requires
its existence).

**What it means.** The trivial exponent is `(1−δ)|z|²/2 + R|z|` — but only *per atom*. The lemma
gives a uniform envelope for the *normalized combinations*, whose norms may have collapsed under
cancellation, at the cost of only `δ/2` in the quadratic coefficient. This closes FR6 (together with
FR5/FR7) in the program-internal c=3 FR ledger.

**Non-claims.** The polynomial-envelope form (E-d) (open, an obligation of general c), the quantified
completion of Lemma N itself, the closure theorem and Corollary C1, and general c (B2/S4, L2b/L3) — all
remain open on the closure-draft side.

## 4. Proof architecture

Fix a ray `z = te^{iθ}` and let `T := |z|`. The near-origin regime `T < 3` follows at once from the
reproducing-kernel bound (`e^{T²/2} = e^{(1−δ/2)T²/2}·e^{δT²/4}` and `δT²/4 ≤ (3δ/4)T`). The main case
is rank 3 with `T ≥ 3`, handled by a four-stage pipeline:

1. **Exit (W1+W2).** At `t = T`, convert `e^{U_T}` into Fock norms. The pair child needs the **strong**
   c=2 norming (quadratic coefficient `(1−δ)`, Lemma W2): a budget computation shows the weak form
   `(1−δ/2)` leaves no room to absorb the chain's quadratic cost `(δ/8)T²`, while the strong form does
   (`(1−δ)/2 + δ/8 = (1−3δ/4)/2 < (1−δ/2)/2`).
2. **Chain (W3).** Propagate the weighted function `G := e^{−U_T}H` inward along a unit-window
   segmentation `I_k = [a_k, a_k+1]` (descending from `a_1 = T−1`; overlaps `J_k` of length `ε_chain`;
   `N ≤ 2T+1` windows). Each one-window comparison is supplied by an accepted kernel (§5, M1/W3):
   uniform cost `C_T` on windows where the pair phases are *held* (kernel QR5), graded cost
   `exp(C_RF(1+Λ_{η,k}))` on *far* windows (kernel RF). The far costs sum to `(δ/8)T² + O(T)` by RF's
   global ledger.
3. **Terminal anchor (C0).** On the last window `I_N ⊂ [0,2]`:
   `max(‖X‖,‖Y‖)·‖G‖_{∞,I_N} ≤ C_anc·‖H‖`. The singleton child is zero-free and bounded below there.
   The accepted equivalent form `‖G‖_{∞,I_N} ≤ C_anc·D_H^{−1}` supplies the cancellation however large
   `D_H` may be (under the design-note expectation `D_H ~ s̃^{−2}` it would give
   `‖G‖_{∞,I_N} = O(s̃²)`).
4. **Composition (W4→EW).** Multiplying the three stages:
   `|H(Te^{iθ})| ≤ 2C₂C_anc·‖H‖·(1+T)²·e^{(1−3δ/4)T²/2+(R+C_ch)(T+1)}`; then `(1+T)² ≤ e^{2T}` and
   `(1−3δ/4) ≤ (1−δ/2)` yield the (S4-Ew) form. Rank 2 follows from W2 directly, rank 1 from the
   trivial singleton bound.

## 5. The lemma chain (statements)

Full proof drafts of all of the following are in FR document §10.8; each consumes previously accepted
inputs (the one-window QR5/RF inequalities, the coverage lemma, etc.) by citation without re-proving
them. Write
`E_{δ,R}(t) := exp((1−δ)t²/2 + Rt)`.

**W1 (Child-reserve interface, `a59768e`).** If each child of a binary node `H = X + Y` satisfies a
per-child strong bound `|X(z)| ≤ C_X P_X(t) E_{δ,R}(t)‖X‖` (with `P_X` a fixed-degree polynomial with
nonnegative coefficients), then `e^{U_H} ≤ C_res·P·E_{δ,R}·max(‖X‖,‖Y‖)` with `C_res = max(C_X,C_Y)`
and `P = P_X + P_Y`. A singleton `cΦ(ξ)` with `ξ ∈ K_{δ,R}` satisfies the bound with `C = 1, P = 1`
(using `‖Φ‖ ≥ |Φ(0)| = 1`).

**W2 (Pair norming, strong c=2 form, `a0fcd10`).** For distinct `ξ₁, ξ₂ ∈ K_{δ,R}`, `c₁c₂ ≠ 0`, and
`f = c₁Φ(ξ₁) + c₂Φ(ξ₂)`, for all `t ≥ 0`:

  |f(te^{iθ})| ≤ C₂(R)·(1+t)²·E_{δ,R}(t)·‖f‖_ℱ,
  C₂(R) = 1 + max{2(1+2R)(1+R), 2√2 + 2(1+R²)}.

The constant depends on `R` only — **not** on the collision scale or the pair separation. Proof
skeleton: bound the divided difference `ψ := (Φ(ξ₁)−Φ(ξ₂))/r` (`r = max(|ΔA|,|ΔB|)`) by a segment-path
integral representation (convexity of `K_{δ,R}`); extract a lower bound on the 0–2 jet of `ψ`
(`ψ₀ = 0, ψ₁ = ΔB/r, ψ₂ = (ΔA/r + (B₁+B₂)ΔB/r)/√2`) by a dichotomy; then eliminate the raw
coefficients of `f = (c₁+c₂)Φ(ξ₂) + (c₁r)ψ` through `‖f‖`. Even in deep collision the same `r` appears
both in the numerator and in the norming, so no scale-dependent factor survives into the statement.

**C0 (Terminal two-anchor, `f31cca0`).** For the root `H = X + Y` (`X` the pair block,
`Y = c₃Φ(ξ₃)` the singleton), `G := e^{−U_T}H`, and `I_N ⊂ [0,2]`:

  max(‖X‖,‖Y‖)·‖G‖_{∞,I_N} ≤ C_anc·‖H‖,   C_anc = max{6, (3/2)C_s}.

Proof skeleton: on `t ≤ 2` the singleton is zero-free with `|Y| ≥ c_Y‖Y‖` (closed-form norm upper bound
plus an exponent lower bound). Split on `A := ‖H‖` vs `B := ‖Y‖`: if `A ≥ B/2` use `|G| ≤ 2` and
`M ≤ 3A` directly; if `A < B/2` use the singleton-anchored bound `‖G‖ ≤ C_s A/B` against `M ≤ (3/2)B`.

**M1 (mode audit, `fd18e9d`).** A corollary of the accepted coverage lemma (S4b-COV, `c36d818`): the
public ray ledger consumes only weighted root records (QR5 on held windows / RF on far windows), exactly
one per non-terminal window (`k ∈ K_T = {1,…,N−1}`); the terminal window `I_N` carries no root record
and is reserved for C0. No new analytic content.

**W3 (Weighted chain, `4086ef9`).** For `m ≥ m₀` and `T ≥ 3`:

  ‖G‖_{∞,I₁} ≤ exp((δ/8)T² + C_ch(T+1))·‖G‖_{∞,I_N},
  C_ch = 10·log(1/ε_chain) + 2·log⁺C_T + 6·C_RF.

Iterate the one-window comparison `‖G‖_{∞,I_k} ≤ C_step,k·ε_chain^{−5}·‖G‖_{∞,I_{k+1}}` over
`N−1 ≤ 2(T+1)` windows and split the cost three ways: the `ε` factors are linear in `T`, held windows
uniform, far windows quadratic `(δ/8)T²` plus linear via RF's global ledger. The weight `U_T` is one
function on the whole ray, so no weight change occurs between records.

**W4 (Terminal-cancelled exit, `cb87eee`).** Composing W1/W2 (exit) × W3 (chain) × C0 (anchor):

  |H(Te^{iθ})| ≤ 2C₂(R)·C_anc·‖H‖·(1+T)²·exp((1−3δ/4)T²/2 + (R+C_ch)(T+1)).

The quadratic coefficient `(1−3δ/4)/2` beats the target `(1−δ/2)/2` by `δ/8`.

**EW-B (original-collision bridge, `b39216f`).** Re-instantiates the chain's witnesses (variation of the
pair phase difference `Λ_{η,k}`, etc.) in the original, ungauged coordinates: by definition of `s̃_m`,
`|ΔA| ≤ s̃_m²` and `|ΔB| ≤ s̃_m`, so RF's ledger applies with identical constants. Transferring through
the gauge (a metaplectic envelope composition) is *not* used — unitarity preserves norms but not
pointwise growth.

**EW (final, `b39216f`).** `F := U_m^{−1}v_{ℓ,m}` (`‖F‖ = 1`) is an exact combination of at most three
original atoms. A case split over effective rank (1/2/3) × `T ≥ 3` / `T < 3` yields (S4-Ew) with
`C_w = 2C₂(R)C_anc·e^L`, `C_lin = L + 2`, `L = R + C_ch`.

## 6. Constants

All constants assemble in closed form from `(δ,R)` and three uniform kernel constants:

| constant | source | value / dependency |
|---|---|---|
| `C₂(R)` | W2 | `1 + max{2(1+2R)(1+R), 2√2+2(1+R²)}` |
| `C_Φ, c_Y, C_s` | C0 | `C_Φ = [δ(2−δ)]^{−1/4}e^{R²/(2δ)}`, `c_Y = C_Φ^{−1}e^{−2(1−δ)−2R}`, `C_s = e²/c_Y` |
| `C_anc` | C0 | `max{6, (3/2)C_s}` |
| `ε_chain` | segmentation | `min(1/2, δ/[8(κ_chain+1)])` (from the route registry) |
| `C_T` | QR5 kernel (accepted; from a predecessor document outside the FR document) | uniform cost on held windows; normalized to `max(1,·)` on consumption |
| `C_RF` | Lemma RF (accepted; proved **inside** FR document §10.5.3) | graded cost constant on far windows (ledger included) |
| `C_ch` | W3 | `10log(1/ε_chain) + 2log⁺C_T + 6C_RF` |
| `C_w, C_lin` | EW | `2C₂C_anc·e^{R+C_ch}`, `R+C_ch+2` |

## 7. Verification status

- Every lemma passed the cadence: draft → independent LLM review at a fixed commit SHA (adversarial
  findings; blocking findings prevent acceptance until fixed) → acceptance. The SHAs are attached to
  each lemma in §5; the complete ledger is FR document §10.7/§11.
- Numerical diagnostics (**not evidence**): W2 was tested on 4×10³ random configurations (exact `‖f‖`
  via closed-form Gram matrices, including near-cancellation and collision scales `s ∈ [10⁻³,1]`) with
  no violation and minimum margin ×96; C0 on 3 parameter classes × 1500 configurations with no
  violation (margin ~1.9×10⁴ on a deep-cancellation configuration with `D_H ≈ 7×10⁵`). An independent
  recomputation at 70-digit precision also found no violation.
- Claim-surface consistency (the FR7 forbidden vocabulary, acceptance markings, version sync) is
  machine-monitored by the repo's [claim-surface tests](../tests/test_claim_surface_policy.py)
  (25 tests). These tests monitor the normative documents (the FR document and the closure draft);
  this summary itself is not among their targets.

**Open items:** independent external re-review of the entire c=3 FR arc, the quantified completion of
Lemma N itself, general c ((E-d), B2/S4, L2b/L3), and Corollary C1. This note claims none of them.

## 8. Where the full proofs live

| content | location |
|---|---|
| main result and all S4a proofs (W1–EW) | FR document §10.8 |
| exact specification of the target (E-w) | FR document §10.2 |
| segmentation, ledgers, route contracts | FR document §10.3–10.6 |
| RF kernel: interface / proof | FR document §10.5.2 (interface) / §10.5.3 (proof, internal to the FR document) |
| QR5 / K2-family kernels: proofs | predecessor documents (K2p1 §3.8.6 and others) — the FR document only cites and consumes the accepted results |
| coverage lemma (S4b-COV) | FR document §10.5.5 |
| acceptance ledger and version history | FR document §10.7 / §11 |
| position in the program (Lemma N, FR1–FR7) | closure draft §4.3; FR document §1–§4 |

Japanese version: [2026-08-17-fr-s4-selfcontained-summary--wip.md](2026-08-17-fr-s4-selfcontained-summary--wip.md)

*(The FR document and the closure draft are written in Japanese; this English summary is provided for
external readers. Terminology follows the FR document; where names differ, the FR document's usage
prevails.)*
