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

### 3.1 Synthetic scaling: an honest one/two/three-mode story (C1)

The signed-splat track was compared against iterative RρR maximum-likelihood
estimation on simulated cat states at matched shot budgets. The outcome is
deliberately reported as a scaling story rather than a win. At one mode the
splat reaches a slightly higher score but the MLE is about twice as fast, so
there is no computational advantage at that scale. At two modes,
reconstruction fidelity is statistically indistinguishable across 20 paired
seeds while the splat uses roughly 1/7.4 of the measured compute; the caveat
is structural, since the result requires full cross-mode covariance and
separable splats fail. At three modes a signed-splat run reached a higher
Wigner-overlap score in about 15 s while the 512-dimensional MLE did not
converge within 900 s — but the reconstruction is not positive semidefinite
there, so this score is not a state fidelity and we do not report it as a
physical-tomography win. That tension is what motivated the physical track.

### 3.2 Real GKP data: rank saturation and the frontier tie (C2)

On the public propagating-light GKP homodyne dataset of Konno *et al.*
(Science 2024; Dryad doi:10.5061/dryad.t76hdr86j), a pure Gaussian-ket model
initially lost clearly to full-rank MLE on held-out likelihood — a recorded
negative result. Composing the model with a physical loss channel and moving
to a rank-two squeezed-ket mixture improved held-out likelihood and, in a
matched-degrees-of-freedom control, outperformed a rank-one model of
comparable capacity.

A rank-saturation study then walked the remaining frontier gap down. The
held-out rank curve saturates at R = 4–5; warm starts make material
under-optimization unlikely under the tested schedule, and matched-degrees-of-freedom
controls at two frontier points attribute each gain to rank rather than raw
parameter count. At rank 4 — 92 real parameters — the physical model ties
the empirical MLE frontier at confidence-interval resolution on both data
reshuffles: conditional 95% intervals of [−0.00002, +0.00020] and
[−0.00017, +0.00003] nats per held-out sample against the test-selected
frontier best at 255 parameters. Three scope limits apply and are not
footnotes: the reshuffled splits reuse the same observations, the MLE
opponent is selected on test performance, and a tie at confidence-interval
resolution is not a preregistered confirmation. (Figures: measured-marginal
reconstructions and the held-out NLL-vs-dof frontier, from experiments 14
and 18.)

### 3.3 The blind gate and the family boundary (C3)

The strongest single result is a pre-declared, held-out gate on a synthetic
target chosen to be hostile: a lossy cat state with added thermal noise,
which is full-rank and — as proven below — outside the model family. Fitted
blind (all modeling decisions declared before scoring), the loss-composed
rank-2 model reached generalized fidelity 0.949 against 0.898 for a
full-rank MLE run under the pre-declared 900-second baseline budget, with
roughly 110 versus ~2.6×10⁵ real parameters. The pure-detection ket
mixtures, by contrast, were capacity-limited: the rank-1 models landed
within 2–3% of their rank-capacity ceiling (0.370–0.371 against 0.379),
while the rank-2 mixture reached 0.648, about 86% of its 0.750 ceiling.
The loss channel thus buys structured full-rank expressivity with very few
parameters, rather than generic fitting capacity.

A non-inclusion analysis then settled what "out-of-family" means here. For
**no** assumed detection efficiency η′ ∈ (0, 1] and **no** finite rank does
the target factor as a loss-channel image of a finite-rank state: for
η′ below η − σ the required pre-image is not a positive operator at all:
positivity of the pre-image would force an s-ordered quasidistribution of
the *cat state itself* to be nonnegative, and Gaussian smoothing of that
nonnegative function would make the cat's Husimi function strictly
positive — contradicting its exact (Bargmann) zeros;
exactly at the boundary the pre-image is an amplified cat whose kernel has
no finite-rank factorization; above the boundary the pre-image is a valid
but full-rank state. Proofs are in the repository derivation; a validated
numerical scan corroborates the theorems but is not the argument. The
boundary is thin, however: direct best-approximation fits approach the
target to 1–2×10⁻³ in 1 − F (cutoff-stable best-found values, hence upper
bounds on the true distance), with best-found fitted η′ values of
0.648–0.661 across ranks — pressed against the positivity boundary
(Fig. summary, panel a). The blind gap of ~0.05 is therefore a fit- and data-budget
effect, not the family boundary itself.

Finally, a robustness sweep repeated the blind comparison across three data
seeds and a fourfold range of noise strength. The pre-declared verdict holds
on all five configurations, with representative lossy fidelities 0.893–0.949
against MLE 0.815–0.936 (Fig. summary, panel b). Budget disclosure: the MLE
baseline runs under the pre-declared 900 s budget and met its convergence
criterion on two of the five configurations; the model side fits three
initializations (1.4–2.0×10³ s aggregate per configuration, sequential) and
selects blind by training likelihood. Margins over the unconverged baselines
are not guaranteed to survive longer MLE optimization. Three observations
worth recording: no initialization-basin collapse occurred in any of the
fifteen fits; the known selection hazard (§3.4) did appear in mild form — at
the highest noise level the likelihood-selected initialization was the worst
of three in fidelity, without affecting the verdict; and the fitted η′
tracked the injected noise monotonically, exactly the flat-direction
mechanism the non-inclusion derivation predicts.

### 3.4 Negative results and hazards (kept, not buried)

Two failure modes documented earlier in the record bound how far §3.3-style
results can be trusted, and we state them as first-class findings. First,
multi-seed refits of a lossy-target model exhibited a collapse basin:
solutions differing by ΔF ≈ 0.45 in fidelity were separated by only
≈ 2.5×10⁻³ nats per sample in training likelihood, and in one case a
pre-declared selection rule picked a solution 0.04 worse in fidelity than a
near-equivalent alternative at ΔNLL ~ 10⁻⁴ nats per sample. Training
likelihood can be almost blind to fidelity-relevant structure; every blind
protocol above therefore pre-declares its selection rule, and the
robustness sweep additionally records all per-initialization fidelities
(the single-configuration gate retains only its selected fit — a
limitation the sweep remedies).
Second, jointly fitting the detection efficiency η with the state is
non-identifiable in this design: fitted η scattered over 0.56–0.77 along a
training-NLL plateau of width ~10⁻⁵ nats per sample while fidelity varied
from 0.06 to 0.80. Nuisance channel parameters must be measured or fixed, not fitted.
The earliest experiments in the repository predate the pre-declaration
discipline and are recorded as exploratory.

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
  review, and all protocol decisions by the author; implementation, drafting,
  analysis, and internal-review assistance by Claude (Anthropic) and Codex
  (OpenAI) agents.
- Konno et al. / Dryad data attribution.

## References (seed list)

- Konno et al., Science 2024 (GKP data + Dryad DOI)
- R2-Gaussian (2405.20693), X²-Gaussian (2503.21779)
- Kenfack & Życzkowski (physics/0304029), Tosca et al. (2507.14076)
- Strandberg (2202.11584), Gaikwad et al. (2503.04526)
- Lütkenhaus & Barnett (Q-function zeros / depth argument, exp20 のメカニズム出典)
- Hudson's theorem / stabilizer-rank analogy anchors (C4 用、#71 から)
