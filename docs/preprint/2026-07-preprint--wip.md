# Compact physical Gaussian-ket models for homodyne quantum-state tomography

**Author:** orange
**AI assistance:** drafting, implementation, and analysis were carried out with AI agents
(Claude, Codex); the author directed the research questions, reviewed every claim, and made
all editorial and protocol decisions. (Full statement in Acknowledgements.)

**Target:** Zenodo (concrete target; the generalist OSF Preprints server has been
closed to new submissions since 2025-08-25), short paper (6–10 pp).
**Status:** skeleton — prose slots marked `[...]`, numbers slot in from the committed
experiment logs at the end. Every claim carries its scope note inline; the claim
discipline *is* the selling point.

---

## Abstract (draft v1)

> Continuous-variable quantum-state tomography usually reconstructs a truncated
> Fock-basis density matrix. We study a compact alternative: finite mixtures of
> displaced, squeezed Gaussian kets whose ρ = BB† construction is positive
> semidefinite by construction, fitted by per-sample homodyne likelihood with
> closed-form gradients, and composed with physical loss and noise channels.
> On the public propagating-light GKP dataset of Konno *et al.* (Science 2024),
> a rank-4 model with 92 real parameters matches the empirical full-rank
> maximum-likelihood frontier (255 parameters) at confidence-interval
> resolution on held-out likelihood. On a synthetic thermal-noise target that
> we prove lies outside the model family — no detection efficiency and no
> finite rank reproduces it exactly — the channel-composed model fitted blind
> exceeds a full-rank MLE run under the pre-declared 900-second baseline
> budget, a verdict that holds across all five pre-declared seed and noise
> configurations. We do not claim a
> universally superior method: comparisons on real data reuse observations
> across splits, the strongest baseline is test-selected, and the blind result
> covers one target class. The contribution is a compact, physically
> constrained model family together with a fully falsification-first research
> record — negative results, superseded scorings, and pre-declared protocols
> are all preserved in the accompanying repository.

(v1 notes: ~180 words; each sentence maps to C1–C3 + the non-claim. The
headline says *a full-rank MLE under the pre-declared 900 s baseline budget* —
NOT "converged MLE" (exp21: converged 2/5) and NOT "equal wall-clock" (the
model side fits three initializations totaling ~1.4–2.0×10³ s per
configuration vs the MLE's 821–910 s; the budget asymmetry is disclosed in
§2.3/§3.3, review round 1).)

## 1. Introduction

- Origin: 3D Gaussian splatting ↔ homodyne tomography analogy (camera view = LO phase,
  splat = phase-space Gaussian, rendering = Radon projection). State explicitly: an
  origin story and an experimental representation, **not** a claim that CV-3DGS solves
  tomography.
- The two tracks and why the physical one became the main line:
  signed splats (expressive, fast, but non-PSD scores are not fidelities — the #8
  tension stated up front) → BB† Gaussian-ket mixtures (PSD by construction,
  closed-form per-sample likelihood, analytic gradients).
- Contribution list (each with its experiment tag and scope note):
  C1 honest scaling story (1/2/3 modes, exp05–11);
  C2 rank saturation + CI-resolution tie on real GKP data (exp12–14, 18);
  C3 blind out-of-family gate + analytic family boundary (exp19–21);
  C4 (speculative, one paragraph) splat count as a CV nonclassicality measure.
- Related work paragraph: R2-/X²-Gaussian (differentiable Radon), Kenfack/Tosca
  (Gaussian Wigner-negativity representations), Strandberg 2022 / Gaikwad 2025
  (physical homodyne optimization). Novelty boundary per docs/prior-art-survey.md:
  the *combination* question for splats; the BB† track does NOT inherit that claim.

## 2. Models and methods

### 2.1 Signed-splat Radon model (brief)
- Closed-form Radon projection of anisotropic signed Gaussians; birth/split/prune.
- Kept brief: it is the origin and the 1/2/3-mode comparison substrate.

### 2.2 Physical Gaussian-ket mixtures (main)
- ρ = BB†: mixtures of displaced squeezed kets; rank-R extension; per-sample homodyne
  NLL, closed-form gradients (issue #25 speedups: FD → analytic, 30–90×).
- Loss/noise channel composition: E_η ∘ ket mixture; thermal noise N_σ; the
  characteristic-function calculus (Lemma 1: N_σ∘E_η = E_η∘N_{σ/η}) — cite exp20
  derivation.md for the full proofs, state only what the paper needs.

### 2.3 Baselines and scoring
- Iterative RρR full-rank MLE at matched shot budgets; the MLE baseline runs under
  a pre-declared 900 s budget (NOT matched wall-clock: the model side fits three
  initializations of ~470–670 s each, 1.4–2.0×10³ s aggregate per configuration,
  and selects blind by train NLL — disclose the asymmetry and the 2/5 convergence
  rate wherever the comparison is cited).
- Generalized fidelity for subnormalized (cropped) matrices
  F = (Tr√(√ρσ√ρ) + √((1−Trρ)(1−Trσ)))² — why plain Uhlmann mis-scores cropped
  models (PR #64 round 2); used uniformly for exp19-class scoring.
- Held-out protocol: train/held-out splits, best-by-train-NLL selection rule
  (pre-declared), its known hazard (exp16) and where it bit mildly (exp21, σ=0.2).

## 3. Results

### 3.1 Synthetic scaling: an honest 1/2/3-mode story (C1)
- Table (from README): 1 mode — MLE faster; 2 modes — statistical tie at ~1/7.4
  compute (20 paired seeds); 3 modes — splat "wins" a score that is **not** a fidelity
  (non-PSD) while 512-dim MLE fails to converge in 900 s. Scope limits in the table
  itself, as in the README.

### 3.2 Real GKP data: rank saturation and the frontier tie (C2)
- Konno et al. Science 2024 public homodyne data (Dryad DOI).
- Loss-channel + rank-2 beats rank-1 at matched dof (exp13/14); rank curve saturates
  at R=4–5 with warm-start and matched-dof controls (exp18).
- Headline: rank-4, 92 real params ties the test-selected 255-param MLE frontier at
  CI resolution on both reshuffles (CIs [−0.00002,+0.00020], [−0.00017,+0.00003]
  nats/sample). Scope: splits reuse observations; opponent is test-selected; a tie at
  CI resolution is not preregistered confirmation.
- Figures: exp14 marginals; exp18 frontier plot.

### 3.3 The blind gate and the family boundary (C3)
- exp19: pre-declared full-rank thermal target; lossy rank-2 blind fit 0.923 (old
  metric) / 0.949 (generalized) vs converged MLE 0.898 with ~2.6×10⁵ params.
- exp20: Theorems (stated, proofs by pointer to the repo derivation): for **no**
  detection efficiency η′ ∈ (0,1] and **no finite rank** does the target factor
  through the loss channel — regime III via Q-function positivity vs Bargmann zeros;
  boundary point via infinite-rank amplifier kernel. The scan is corroboration, not
  the proof. Thin-boundary caveat: best-found approximations reach 1−F ≈ 1–2×10⁻³
  (upper bounds), so the blind gap is fit-/data-budget, not distance.
- exp21: 5 pre-declared configs (3 data seeds × σ_add range 4×): verdict holds 5/5
  (lossy 0.893–0.949 vs MLE 0.815–0.936). **Budget disclosure**: the MLE baseline
  runs under the pre-declared 900 s budget and converged on 2/5; the lossy side is
  three initializations (1.4–2.0×10³ s aggregate per configuration, sequential)
  selected blind by train NLL. Margins over unconverged baselines not guaranteed
  under longer optimization. Texture: no basin collapse in 15 fits; the exp16 selection hazard
  visible in mild non-verdict-affecting form; fitted η′ tracks σ_add as the exp20
  mechanism predicts.
- One new summary figure: exp19/20/21 combined (target, family boundary, sweep bars).

### 3.4 Negative results and hazards (kept, not buried)
- exp16 basin collapse + NLL-blindness (ΔF ≈ 0.45 at ΔNLL ≈ 2.5e-3).
- exp17 η non-identifiability on the train-NLL plateau ("fit するな、測るか固定しろ").
- Early exploratory experiments predate the pre-declaration discipline (recorded as
  such — mirrors the README falsification-first scoping).

## 4. Discussion

- What the record supports: compactness (92 vs 255 params at the frontier tie;
  ~110 vs ~2.6×10⁵ on the blind gate), channel-composed structure as the working
  mechanism (exp20 geometry: fitted η′ lands on the PSD boundary).
- C4 (one paragraph, flagged speculative): splat/ket count K as a CV analogue of
  stabilizer rank — "how many Gaussians is this state?" Links to issue #71; no
  results claimed.
- Limitations: one target class for the blind gate; exploratory reshuffles on real
  data; test-selected opponent; wall-clock-budget baselines.

## 5. Reproducibility

- Repository (MIT) + Zenodo archived release DOI 10.5281/zenodo.21387212.
  Experiment directories commit their scripts and available recorded outputs.
  The formal gates 16_exp11_seeds, 17_loss_control, 18_gkp_saturation,
  19_thermal_gate, 20_noninclusion, and 21_thermal_sweep additionally commit
  machine-readable results.json. The research log is the chronological record,
  including superseded scorings.

## Acknowledgements

- AI-assistance statement (per decision 2026-07-20): research direction, claim
  review, and all protocol decisions by the author; implementation, drafting, and
  analysis assistance by Claude (Anthropic) and Codex (OpenAI) agents; reviewer
  role by [Sol の表記をどうするか orange に確認] .
- Konno et al. / Dryad data attribution.

## References (seed list)

- Konno et al., Science 2024 (GKP data + Dryad DOI)
- R2-Gaussian (2405.20693), X²-Gaussian (2503.21779)
- Kenfack & Życzkowski (physics/0304029), Tosca et al. (2507.14076)
- Strandberg (2202.11584), Gaikwad et al. (2503.04526)
- Lütkenhaus & Barnett (Q-function zeros / depth argument, exp20 のメカニズム出典)
- Hudson's theorem / stabilizer-rank analogy anchors (C4 用、#71 から)
