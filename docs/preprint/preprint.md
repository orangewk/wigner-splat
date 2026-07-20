---
title: "Compact physical Gaussian-ket models for homodyne quantum-state tomography"
author: "Wataru Kawashima (ORCID: 0009-0002-7713-5547)"
date: "July 2026 — draft v1 (not yet submitted)"
abstract: |
  Continuous-variable quantum-state tomography usually reconstructs a
  truncated Fock-basis density matrix. We study a compact alternative:
  finite mixtures of displaced, squeezed Gaussian kets whose
  $\rho = BB^{\dagger}$ construction is positive semidefinite by
  construction, fitted by per-sample homodyne likelihood with closed-form
  gradients, and composed with physical loss and noise channels. On the
  public propagating-light GKP dataset of Konno *et al.* (Science 2024), a
  rank-4 model with 92 real parameters matches the empirical full-rank
  maximum-likelihood frontier (255 parameters) at confidence-interval
  resolution on held-out likelihood. On a synthetic thermal-noise target
  that we prove lies outside the model family --- no detection efficiency
  and no finite rank reproduces it exactly --- the channel-composed model
  fitted blind exceeds a full-rank MLE run under the pre-declared
  900-second baseline budget, a verdict that holds across all five
  pre-declared seed and noise configurations. We do not claim a universally
  superior method: comparisons on real data reuse observations across
  splits, the strongest baseline is test-selected, and the blind result
  covers one target class. The contribution is a compact, physically
  constrained model family together with a fully falsification-first
  research record --- negative results, superseded scorings, and
  pre-declared protocols are all preserved in the accompanying repository.
geometry: margin=2.7cm
fontsize: 10pt
numbersections: true
---

# Introduction

This project began with an analogy. In computer-vision 3D Gaussian
splatting, a scene is represented as a mixture of anisotropic Gaussians and
rendered by projection; in homodyne tomography, a quantum state's Wigner
function is observed through one-dimensional projections --- Radon
transforms --- indexed by the local-oscillator phase. A camera view
corresponds to a homodyne phase, a splat to a phase-space Gaussian,
rendering to a Radon projection. We state up front what the analogy is and
is not: it is the origin of the project and an experimental representation
choice, not a claim that computer-vision splatting solves quantum
tomography.

Two model tracks came out of it. The first, *signed* anisotropic Gaussian
mixtures fitted to quadrature marginals through a closed-form
differentiable Radon forward model, is expressive and fast --- signed
weights can represent Wigner negativity --- but a signed mixture is not
guaranteed to be a quantum state, and the resulting overlap scores are not
physically bounded and are not fidelities; on one out-of-family target the
recorded score exceeds unity (§3.4). The second track responds to that
tension: finite mixtures of displaced, squeezed Gaussian kets assembled as
$\rho = BB^{\dagger}$, which is positive semidefinite by construction,
admits a closed-form per-sample homodyne likelihood with analytic
gradients, and composes with physical loss and noise channels. The
physical track is the main subject of this paper.

Our contributions are deliberately scoped:

- **C1** --- an honest scaling comparison of the signed-splat track against
  full-rank maximum-likelihood estimation on one, two, and three synthetic
  modes, including the non-PSD failure that motivates the physical track
  (§3.1).
- **C2** --- on the public GKP homodyne dataset of Konno *et al.*, a
  rank-saturation analysis showing a 92-parameter physical model tying the
  empirical full-rank MLE frontier at confidence-interval resolution on
  held-out likelihood (§3.2).
- **C3** --- a pre-declared blind gate on a synthetic thermal-noise target,
  together with an analytic proof that the target lies outside the model
  family for every assumed efficiency and every finite rank, and a
  five-configuration robustness sweep (§3.3).
- **C4** --- a one-paragraph speculative discussion: the number of Gaussian
  components needed by a state as a possible continuous-variable analogue
  of stabilizer rank (§4).

Prior work bounds the novelty claims, and the closest precedents concern
the physical track itself. Gaussian-superposition representations are an
established lineage: the stellar representation of Chabaud, Markham, and
Grosshans stratifies non-Gaussian states by the zeros of their Bargmann
functions; Marshall and Anand simulate quantum optics by finite
coherent-state decompositions; and variational Gaussian-wavepacket
superpositions go back to Heller's frozen Gaussians in chemical physics.
On the inverse-problem side, structured and model-based homodyne
tomography is likewise established: Ohliger *et al.* formulated low-rank
continuous-variable tomography, Tiunov *et al.* demonstrated that a
physically constrained generative model beats generic MLE at small sample
sizes on experimental homodyne data, and Fedotova *et al.* pursue
Fock-truncation-free reconstruction at high amplitude. Against this
background we do not claim a new Gaussian-state representation: the
surviving contribution is algorithmic and empirical --- a differentiable,
closed-form-likelihood Gaussian-ket estimator with physical channel
composition, evaluated under pre-declared falsification protocols. For the
signed-splat track the anchors are differentiable Gaussian Radon
tomography (R2-Gaussian, X²-Gaussian) and Gaussian representations of
Wigner negativity (Kenfack and Życzkowski; Tosca *et al.*), and the
narrow open question is their combination on measured homodyne data;
physical-model homodyne optimizers (Strandberg; Gaikwad *et al.*) are
adjacent to both tracks. The repository's prior-art survey records these
boundaries in detail.

# Models and methods

## Signed-splat Radon model

A state's Wigner function is modeled as a signed mixture of anisotropic
Gaussians; the Radon projection of each component is Gaussian and
closed-form, so quadrature histograms are differentiable in all mixture
parameters. Gradient-driven birth, splitting, and pruning adapt the
mixture size during fitting. We keep this section brief: in this paper the
signed-splat model serves as the origin story and as one arm of the §3.1
scaling comparison, and its central limitation --- signed mixtures need
not be positive semidefinite, so overlap scores are not fidelities --- is
exactly what the physical track removes.

## Physical Gaussian-ket mixtures

The physical model represents $B$ as a $K$-component mixture of displaced,
squeezed product kets and sets $\rho = BB^{\dagger}/\mathrm{Tr}(BB^{\dagger})$:
positive semidefinite by construction, with the trace normalized
explicitly; a rank-$R$ extension takes $R$ such columns. The homodyne
likelihood of a quadrature sample at a given phase is closed-form in the
mixture parameters, with analytic gradients for the ket and mixture
parameters (replacing an earlier finite-difference implementation, a
30--90× wall-clock improvement that made the multi-start protocols of §3.3
affordable); when the loss transmissivity $\eta'$ is itself fitted, its
derivative is taken by a scalar finite difference. Mixed states are
reached by composing the ket mixture with a physical loss channel of
transmissivity $\eta'$; the composed likelihood remains closed-form. The
implementation also supports a *fixed* additive-noise variance, but the
blind protocols of §3.3 deliberately do not use it: the fitted family is
the loss-composed ket mixture alone, while the target contains additive
thermal noise that this family provably cannot represent exactly --- that
mismatch is the point of the gate. The characteristic-function calculus
behind the composition --- including the commutation of loss and noise
channels used throughout §3.3 --- is developed in the repository's
derivation document, and we state here only the facts the results depend
on.

## Baselines and scoring

The full-rank baseline is iterative $R\rho R$ maximum-likelihood
estimation at a matched shot budget. Where wall-clock budgets matter
(§3.3), the MLE runs under a pre-declared 900-second budget; the model
side fits three initializations of roughly 470--670 s each ---
$1.4$--$2.0\times10^{3}$ s aggregate per configuration --- and selects blind by
training likelihood. This asymmetry, and the fact that the MLE met its
convergence criterion on only two of five sweep configurations, is
disclosed wherever the comparison is cited.

Fidelity to a known synthetic target is scored with a generalized fidelity
for subnormalized matrices,
$F = \left(\mathrm{Tr}\sqrt{\sqrt{\rho}\,\sigma\sqrt{\rho}} +
\sqrt{(1-\mathrm{Tr}\,\rho)(1-\mathrm{Tr}\,\sigma)}\right)^{2}$,
which reduces to the Uhlmann fidelity at unit trace. The generalization
matters because scored operators are crops of larger-cutoff computations:
for an identical pair $\rho = \sigma$ of common trace $t < 1$, plain
squared Uhlmann fidelity returns $t^{2} < 1$ --- its residual conflates
crop loss with genuine disagreement --- while the generalized form returns
exactly 1. (The artifact was caught during review of the non-inclusion
study.) All §3.3-class scores use the generalized form uniformly.

Held-out evaluation uses train/held-out splits with the selection rule
declared before scoring. The known hazards of this design --- a training
likelihood nearly blind to large fidelity differences, and
non-identifiable nuisance parameters --- are documented negative results
in this record (§3.4), and the blind protocols are shaped around them.

# Results

## Synthetic scaling: an honest one/two/three-mode story (C1)

The signed-splat track was compared against iterative $R\rho R$
maximum-likelihood estimation on simulated cat states at matched shot
budgets. The outcome is deliberately reported as a scaling story rather
than a win. At one mode the splat reaches a slightly higher score but the
MLE is about twice as fast, so there is no computational advantage at that
scale. At two modes, reconstruction fidelity is statistically
indistinguishable across 20 paired seeds while the splat uses roughly
1/7.4 of the measured compute; the caveat is structural, since the result
requires full cross-mode covariance and separable splats fail. At three
modes a signed-splat run reached a higher Wigner-overlap score in about
15 s while the 512-dimensional MLE did not converge within 900 s --- but
the reconstruction is not positive semidefinite there, so this score is
not a state fidelity and we do not report it as a physical-tomography win.
That tension is what motivated the physical track.

## Real GKP data: rank saturation and the frontier tie (C2)

On the public propagating-light GKP homodyne dataset of Konno *et al.*
(Science 2024; Dryad doi:10.5061/dryad.t76hdr86j), a pure Gaussian-ket
model initially lost clearly to full-rank MLE on held-out likelihood ---
a recorded negative result. Composing the model with a physical loss
channel and moving to a rank-two squeezed-ket mixture improved held-out
likelihood and, in a matched-degrees-of-freedom control, outperformed a
rank-one model of comparable capacity.

A rank-saturation study then walked the remaining frontier gap down. The
held-out rank curve saturates at $R = 4$--$5$; warm starts make material
under-optimization unlikely under the tested schedule, and
matched-degrees-of-freedom controls at two frontier points attribute each
gain to rank rather than raw parameter count. At rank 4 --- 92 real
parameters --- the physical model ties the empirical MLE frontier at
confidence-interval resolution on both data reshuffles: conditional 95%
intervals of $[-0.00002, +0.00020]$ and $[-0.00017, +0.00003]$ nats per
held-out sample against the test-selected frontier best at 255
parameters. Three scope limits apply and are not footnotes: the reshuffled
splits reuse the same observations, the MLE opponent is selected on test
performance, and a tie at confidence-interval resolution is not a
preregistered confirmation.

![Measured GKP homodyne marginals and physical-model
reconstructions.](../../experiments/14_gkp_rank/gkp_rank_marginals.png){width=85%}

![Held-out NLL versus degrees of freedom for physical models and MLE,
ranks 1 through 5.](../../experiments/18_gkp_saturation/gkp_saturation_frontier.png){width=85%}

## The blind gate and the family boundary (C3)

The strongest single result is a pre-declared, held-out gate on a
synthetic target chosen to be hostile: a lossy cat state with added
thermal noise, which is full-rank and --- as proven below --- outside the
model family. Fitted blind (all modeling decisions declared before
scoring), the loss-composed rank-2 model reached generalized fidelity
0.949 against 0.898 for a full-rank MLE run under the pre-declared
900-second baseline budget, with roughly 110 versus $\sim 2.6\times10^{5}$ real
parameters. The pure-detection ket mixtures, by contrast, were
capacity-limited: the rank-1 models landed within 2--3% of their
rank-capacity ceiling (0.370--0.371 against 0.379), while the rank-2
mixture reached 0.648, about 86% of its 0.750 ceiling. The loss channel
thus buys structured full-rank expressivity with very few parameters,
rather than generic fitting capacity.

A non-inclusion analysis then settled what "out-of-family" means here. For
**no** assumed detection efficiency $\eta' \in (0, 1]$ and **no** finite
rank does the target factor as a loss-channel image of a finite-rank
state: for $\eta'$ below $\eta - \sigma$ the required pre-image is not a
positive operator at all --- positivity of the pre-image would force an
$s$-ordered quasidistribution of the *cat state itself* to be nonnegative,
and Gaussian smoothing of that nonnegative function would make the cat's
Husimi function strictly positive, contradicting its exact (Bargmann)
zeros, an adaptation of the phase-space argument of Lütkenhaus and
Barnett; exactly at the boundary the pre-image is an amplified cat whose
kernel has no finite-rank factorization; above the boundary the pre-image
is a valid but full-rank state. Proofs are in the repository derivation; a
validated numerical scan corroborates the theorems but is not the
argument. The boundary is thin, however: direct best-approximation fits
approach the target to $1$--$2\times10^{-3}$ in $1 - F$ (cutoff-stable best-found
values, hence upper bounds on the true distance), with best-found fitted
$\eta'$ values of 0.648--0.661 across ranks --- pressed against the
positivity boundary (Fig. 3a). The blind gap of $\sim 0.05$ is therefore a
fit- and data-budget effect, not the family boundary itself.

Finally, a robustness sweep repeated the blind comparison across three
data seeds and a fourfold range of noise strength. The pre-declared
verdict holds on all five configurations, with representative lossy
fidelities 0.893--0.949 against MLE 0.815--0.936 (Fig. 3b). Budget
disclosure: the MLE baseline runs under the pre-declared 900 s budget and
met its convergence criterion on two of the five configurations; the
model side fits three initializations ($1.4$--$2.0\times10^{3}$ s aggregate per
configuration, sequential) and selects blind by training likelihood.
Margins over the unconverged baselines are not guaranteed to survive
longer MLE optimization. Three observations worth recording: no
initialization-basin collapse occurred in any of the fifteen fits; the
known selection hazard (§3.4) did appear in mild form --- at the highest
noise level the likelihood-selected initialization was the worst of three
in fidelity, without affecting the verdict; and the fitted $\eta'$
tracked the injected noise monotonically, exactly the flat-direction
mechanism the non-inclusion derivation predicts.

![The blind gate and its family boundary. (a) The detection-efficiency
axis with the excluding theorem for each regime; markers show
best-approximation fits pressing against the positivity boundary. (b) The
five-configuration robustness sweep; hatching marks MLE runs that did not
meet their convergence criterion within the 900 s
budget.](summary_figure.png){width=95%}

## Negative results and hazards (kept, not buried)

Two failure modes documented earlier in the record bound how far
§3.3-style results can be trusted, and we state them as first-class
findings. First, multi-seed refits of a lossy-target model exhibited a
collapse basin: solutions differing by $\Delta F \approx 0.45$ in fidelity
were separated by only $\approx 2.5\times10^{-3}$ nats per sample in
training likelihood, and in one case a pre-declared selection rule picked
a solution 0.04 worse in fidelity than a near-equivalent alternative at
$\Delta\mathrm{NLL} \sim 10^{-4}$ nats per sample. Training likelihood can
be almost blind to fidelity-relevant structure; every blind protocol above
therefore pre-declares its selection rule, and the robustness sweep
additionally records all per-initialization fidelities (the
single-configuration gate retains only its selected fit --- a limitation
the sweep remedies). Second, jointly fitting the detection efficiency
$\eta$ with the state is non-identifiable in this design: fitted $\eta$
scattered over 0.56--0.77 along a training-NLL plateau of width
$\sim10^{-5}$ nats per sample while fidelity varied from 0.06 to 0.80.
Nuisance channel parameters must be measured or fixed, not fitted. Third,
the signed-splat score is directly non-physical in the worst case: on a
squeezed out-of-family target its recorded overlap score reached
$1.7674 > 1$ --- impossible for a physical state scored against a pure
target --- which is why §3.1 declines to report splat scores as
fidelities. The earliest experiments in the repository predate the
pre-declaration discipline and are recorded as exploratory.

# Discussion

What the record supports is compactness under physical constraints. On
real data, 92 parameters tie a 255-parameter empirical frontier at
confidence-interval resolution; on the synthetic gate, roughly 110
parameters exceed a $\sim 2.6\times10^{5}$-parameter baseline under the disclosed
budget conventions. The controls isolate a mechanistic reading under the
tested protocols: rank buys what parameter count alone does not (§3.2's
matched-degrees-of-freedom controls), and channel composition buys
structured full-rank expressivity that pure-detection mixtures lack
(§3.3's ceiling analysis). The non-inclusion geometry sharpens this:
best-approximation fits press against the positivity boundary of the
channel parameter, with best-found fitted $\eta'$ of 0.648--0.661 across
ranks --- the family is exploiting the boundary the theorems draw.

One speculative direction seems worth naming (C4). The number of Gaussian
components a state requires --- in either track --- behaves like a
resource count: cat states need few, and the rank/component saturation
points found on real data (§3.2) are small. Hudson's theorem (pure states
with nonnegative Wigner functions are Gaussian) anchors the intuition that
non-Gaussianity is the resource being counted, suggesting a
continuous-variable analogue of stabilizer rank: "how many Gaussians is
this state," as a nonclassicality measure grounded in fitting practice.
Any precise version must be distinguished from existing hierarchies: it is
not the stellar rank of Chabaud *et al.* (a cat state has infinite stellar
rank --- its Bargmann function has infinitely many zeros --- yet needs
only two Gaussian kets here), and it is not identical to coherent-state
decomposition rank (components here carry independent squeezing). Whether
"Gaussian count" differs meaningfully from those hierarchies, and its
basis dependence, robustness to loss, and relation to negativity measures,
is exactly what would need to be established. We flag this as speculation:
no result in this paper establishes it.

The limitations bound the claims. The blind gate covers one target class;
the real-data analyses reuse observations across reshuffled splits and
face a test-selected opponent; the wall-clock baselines are budget
conventions, not converged optima; and nothing here is a universality
claim about tomography methods.

# Reproducibility

The repository (MIT license) and its archived Zenodo release
(doi:10.5281/zenodo.21387212) contain the complete record. Experiment
directories commit their scripts and available recorded outputs; the
formal gates 16_exp11_seeds, 17_loss_control, 18_gkp_saturation,
19_thermal_gate, 20_noninclusion, and 21_thermal_sweep additionally
commit machine-readable results.json files, and the summary figure
regenerates from committed machine-readable result files (the sweep's
results.json and the non-inclusion study's results_routeB.json) with
assertions that fail if the plotted verdict diverges from the data. The
research log preserves the chronological record, including superseded
scorings and the negative results of §3.4. The public GKP dataset is
included with its source attribution.

# Acknowledgements {-}

Research direction, claim review, and all protocol decisions are by the
author, who maintains the accompanying repository under the handle
*orangewk*. Implementation, drafting, analysis, and internal-review
assistance were provided by AI agents: Claude (Anthropic) and Codex
(OpenAI). The GKP homodyne dataset is by Konno *et al.*, redistributed
with attribution from the Dryad archive (doi:10.5061/dryad.t76hdr86j);
we thank the authors for making it public.

# References {-}

1. S. Konno *et al.*, "Logical states for fault-tolerant quantum
   computation with propagating light," Science **383**, 289 (2024). Data:
   Dryad, doi:10.5061/dryad.t76hdr86j.
2. R. Zha *et al.*, "R²-Gaussian: Rectifying radiative Gaussian splatting
   for tomographic reconstruction," NeurIPS 2024; arXiv:2405.20693.
3. W. Yu *et al.*, "X²-Gaussian: 4D radiative Gaussian splatting for
   continuous-time tomographic reconstruction," arXiv:2503.21779.
4. A. Kenfack and K. Życzkowski, "Negativity of the Wigner function as an
   indicator of non-classicality," J. Opt. B **6**, 396 (2004);
   arXiv:physics/0304029.
5. J. Tosca, F. Carnazza, L. Giacomelli, and C. Ciuti, "Variational
   multi-Gaussian phase-space dynamics via automatic differentiation,"
   arXiv:2507.14076 (2025).
6. I. Strandberg, "Simple, reliable, and noise-resilient continuous-variable
   quantum state tomography with convex optimization," Phys. Rev. Applied
   **18**, 044041 (2022); arXiv:2202.11584.
7. A. Gaikwad, M. S. Torres, S. Ahmed, and A. F. Kockum, "Gradient-descent
   methods for fast quantum state tomography," Quantum Sci. Technol.
   **10**, 045055 (2025); arXiv:2503.04526.
8. U. Chabaud, D. Markham, and F. Grosshans, "Stellar representation of
   non-Gaussian quantum states," Phys. Rev. Lett. **124**, 063605 (2020);
   arXiv:1907.11009.
9. J. Marshall and N. Anand, "Simulation of quantum optics by coherent
   state decomposition," Optica Quantum **1**, 78 (2023); arXiv:2305.17099.
10. E. S. Tiunov, V. V. Tiunova, A. E. Ulanov, A. I. Lvovsky, and
    A. K. Fedorov, "Experimental quantum homodyne tomography via machine
    learning," Optica **7**, 448 (2020).
11. M. Ohliger, V. Nesme, D. Gross, Y.-K. Liu, and J. Eisert,
    "Continuous-variable quantum compressed sensing," arXiv:1111.0853.
12. E. Fedotova, N. Kuznetsov, E. Tiunov, A. E. Ulanov, and A. I. Lvovsky,
    "Continuous-variable quantum tomography of high-amplitude states,"
    Phys. Rev. A **108**, 042430 (2023); arXiv:2212.07406.
13. E. J. Heller, "Frozen Gaussians: A very simple semiclassical
    approximation," J. Chem. Phys. **75**, 2923 (1981).
14. N. Lütkenhaus and S. M. Barnett, "Nonclassical effects in phase
    space," Phys. Rev. A **51**, 3340 (1995).
15. R. L. Hudson, "When is the Wigner quasi-probability density
    non-negative?" Rep. Math. Phys. **6**, 249 (1974).

*Repository:* <https://github.com/orangewk/wigner-splat> --- prior-art
survey, research log, derivations, and all experiment protocols.
