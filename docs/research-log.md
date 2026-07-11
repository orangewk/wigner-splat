# Research log — wigner-splat

A dated, chronological record of the program: signed anisotropic Gaussian
mixtures ("splats") fit differentiably to homodyne data to reconstruct Wigner
functions, benchmarked against iterative maximum-likelihood (MLE) tomography.
The organizing question is the README's falsification condition: *can the splat
approach beat iterative MLE on both fidelity and speed at equal shot counts?*
Every milestone below records what was tried, what happened (with the real
numbers from commits, tests, and experiment outputs), and what was learned.

Numbers are quoted as recorded in the sources; single-environment values vary at
the ~epsilon level between machines (issue #4), so seed ranges are preferred
where available.

---

## 2026-07-06 — v0 scaffold (fixed K, numerical gradients)

**Tried.** Seeded the repository from the indirect-agent-lab spike: a fixed-K
signed Gaussian mixture, a closed-form Radon (quadrature-marginal) forward model,
an Adam fitter with numerical gradients, and a negativity penalty. Target: the
single-mode cat state |α⟩ + |−α⟩ at α = 1.5.

**Happened.** The fitter recovered the Wigner negativity that marks
non-classicality: minimum W = −0.194 vs the true −0.190, relative L2 error ≈ 13%
on the Wigner grid.

**Learned.** The signed-splat representation can carry Wigner negativity at all,
and the closed-form Radon projection is a usable differentiable forward model.
This is the baseline every later improvement is measured against.

---

## 2026-07-06 — Analytic (closed-form) gradients

**Tried.** Replaced numerical gradients with a closed-form chain rule through
each splat's projected mean `m_k = μ_k · u` and projected variance
`var_k = e^{2 s1} cos²(φ − θ) + e^{2 s2} sin²(φ − θ)`. `loss_and_grad()`
computes the full parameter gradient in one vectorized pass per angle; `fit()`
runs Adam on it. Verified against central differences (rtol 1e-5).

**Happened.** Experiment 01 wall time dropped from ~29 s to ~1.6 s (~18×) with
relative L2 improving 0.131 → 0.125 and negativity preserved (min −0.197 vs true
−0.190). The iteration count was fixed at 680 after an **overfitting finding**:
past ~700 iterations the fit begins tracking histogram shot noise and the
Wigner-grid L2 *degrades*; 640–700 iterations is a plateau.

**Learned.** The forward model being closed form makes exact gradients cheap, and
the histogram-MSE objective has a finite useful horizon — beyond it the optimizer
fits sampling noise rather than the state. This early-stopping window recurs as a
theme (the histogram loss is a proxy, not the fidelity).

---

## 2026-07-06 — Densification / pruning with signed birth

**Tried.** Grow the mixture from a small K instead of fixing capacity up front:
- `adapt()`: prune splats with |w| below threshold; split splats whose
  accumulated positional-gradient norm exceeds a multiple of the *median*
  (absolute 3DGS-style thresholds fail near convergence, where all gradient norms
  shrink together). Children take half the parent weight, offset along the major
  axis; Adam moments follow the same row bookkeeping.
- `birth_field()`: the weight gradient ∂L/∂w(μ) of a hypothetical splat at μ —
  the residual back-projected through the splat kernel, in closed form like the
  rest of the model. Each densify event births one splat at the field extremum,
  with the descent sign, when capacity remains.

**Happened.** Experiment 02 (same data as 01, K = 4 → 9, ending with 2 negative
weights): relative L2 0.071 vs 0.125 for fixed K = 8; negativity −0.191 vs true
−0.190; **all 5 tested seeds** land at L2 0.05–0.09, versus roughly 1-in-3
success without birth.

**Learned — split-cannot-create-negativity.** Splitting or cloning alone cannot
recover negativity from an all-positive local minimum: two positive children
never sum to a negative fringe (2 of 3 seeds stalled at L2 ≈ 1.0 without birth).
Negativity has to be *born* with an explicitly negative weight, placed where the
residual back-projection says it reduces the loss. This is the first structural
lesson about signed representations and reappears, magnified, at two modes.

---

## 2026-07-06 — Single-mode falsification verdict (experiment 03)

**Tried.** Built the fair MLE comparison the README's falsification condition
demands:
- `fock.py`: truncated Fock-basis tools (cat density matrix, quadrature vectors
  ⟨n|x_θ⟩, displaced-parity Wigner transform, pure-state fidelity, and a
  Wigner-overlap fidelity for states that exist only as Wigner functions, i.e.
  the splat mixture). Conventions validated to ~1e-12 against `states.py`.
- `mle.py`: Lvovsky-style R ρ R iteration on the *same* binned histograms the
  splat fitter consumes.
- `experiments/03_mle_baseline/run.py`: side-by-side fidelity / wall-clock /
  negativity over 250, 1000, 4000 shots per angle, α = 1.5, 12 angles,
  n_max = 20.

**Implementation trap (regression-tested).** The R operator must be
`sum (f/p) |v⟩⟨v|` with `|v⟩_i = ⟨i|x_θ⟩`; the transposed outer product silently
*stalls at F ≈ 0.35* instead of ascending the likelihood.

**Happened.** Splat wins fidelity at every budget (250 shots/angle: 0.980 vs
0.969 — a real shot-efficiency advantage; 4000: 0.991 vs 0.987). MLE wins speed
by ~2× at single-mode scale, where the n_max = 20 matrices are tiny (~0.6 s MLE
vs ~1.3 s splat).

**Learned / verdict.** The falsification condition (win *both*) is **not met at
one mode** — and, as promised, this is recorded as no computational gain at
single-mode scale. The surviving hypothesis is **scaling**: the Fock MLE
dimension grows as n_max^modes while the splat parameter count stays O(K). The
first place to test that is two modes.

---

## 2026-07-07 — Two-mode campaign

Spec and fairness rules in `docs/two-mode-plan.md`. Target state: the entangled
two-mode cat |α, α⟩ + |−α, −α⟩ at α = 1.5, parity +1. Both methods consume
identical binned 2D histograms (`data2.histogram_targets2`, 40 bins), on a 4×4
grid of LO-phase pairs over [0, π)². Fidelity uses the same definition on both
sides, tr(ρ_recon ρ_cat).

### Wave 1 — reference state + vectorized gradients

**Tried.** `states2.py` `TwoModeCat`: closed-form 4D Wigner, joint homodyne pdf,
conditional inverse-CDF sampler. Also vectorized the single-mode
`loss_and_grad` over the angle axis for timing fairness against the fully
vectorized MLE baselines.

**Happened / closed form.** The single-mode fringe cos(2√2 α p) lifts to the
**entangled fringe cos(2√2 α (p1 + p2))**. Validated: 2D Radon identity to
~1e-16, product-Fock cross-check to ~1e-12, purity integral, negativity present.
The vectorized gradient is 3.4× faster per call and matches the looped reference
to rtol 1e-12. 18 tests green.

**Learned.** The entangled fringe lives along the p1 + p2 direction and is
*constant* along p1 − p2 — the geometric fact that drives every result below.
Because cos(k(p1+p2)) factorizes per mode, the plan initially bet that a mixture
of *separable* (per-mode-product) splats could span it.

### Wave 2, part 1 — two-mode MLE baseline (product Fock, 144-dim)

**Tried.** `mle2.py`: R ρ R with Kronecker-product quadrature vectors over the
nonzero bins of the shared 2D histograms, same hardened stop condition as
`mle.py`. `fock.py` gained `cat2_fock` and `cat2_truncation_fidelity`. At α = 1.5,
n_max = 12 per mode, the truncation ceiling (the best fidelity any n_max = 12 MLE
can reach) is **0.999991**; the density matrix is 12² = 144-dimensional.

**Implementation traps (regression-tested).** Two traps guard this baseline: (a)
the single-mode R-operator orientation above (transposed outer product stalls at
F ≈ 0.35); (b) a **probability-conjugation bug** in the two-mode probability
computation broke monotone likelihood ascent — the hardened stop condition
*caught it at iteration 11* rather than letting it "converge" to a wrong fixed
point.

**Happened.** Recovery fidelity 0.9236 at 4×4 angle pairs × 3000 shots, n_max =
12, 646 iterations, ~55 s. First scaling data point: two-mode MLE wall time ~55 s
vs 0.5–0.9 s at one mode — a ~60–100× jump at matched shot budgets.

**Learned.** The MLE side reconstructs the entangled state faithfully from this
data, so **the data determine the state** — any failure on the splat side is a
representation/optimization limitation, not missing information. And the MLE cost
is already climbing steeply with mode count, exactly as the scaling hypothesis
predicts.

### Wave 2, part 2 — separable splats fail (F = 0.50, negative result)

**Tried.** `forward2.py` `SplatMixture2`: separable (block-diagonal 4×4
covariance) splats, 11 parameters each — product `radon2`, `wigner4`, and a
closed-form `fidelity_vs_cat` (the 4D overlap factorizes into per-mode 2D
Gaussian overlaps; the fringe factors are Gaussians with imaginary means).
`fit2.py`: analytic vectorized gradients, `adapt2`, a 4D birth field, and `fit2`
with densification.

**Happened.** The separable reconstructor recovers the two coherent blobs but
**not** the entangled fringe: fit fidelity **0.50** (the classical two-blob
overlap), while the MLE recovers 0.92 from the *same* data. Recorded as a
`strict=False` xfail in `tests/test_two_mode_fit.py` with the full analysis.
Tested exhaustively before recording: shots up to 2e5, angles up to 6×6, K up to
120, batched fringe-seeded birth, λ_neg from 0 to 10 — every setting settles in
the classical basin.

**Learned — three root causes** (the core of the negative result):
1. **The loss minimum itself caps fidelity.** The fringe is a ~2%-RMS
   joint-correlation signal; histogram-MSE overfits it, and the loss *minimum*
   sits at fidelity ≈ 0.80–0.85. A hand-built fidelity-0.997 mixture *degrades*
   to ≈ 0.85 under the loss, so no optimizer can exceed ~0.9 with this objective.
2. **Block-diagonal splats cannot tilt.** cos(k(p1+p2)) is constant along the
   p1 − p2 ridge; a separable splat cannot elongate along it, so ~80
   axis-aligned splats would be needed just to tile the fringe.
3. **Residual birth chases the blobs.** From random init the birth field is
   dominated by the strong blob residual, never the weak fringe, so the fit lands
   in the classical two-blob basin (fidelity ≈ 0.5, no negativity).

This kills the *separable simplification*, not the method: full anisotropic
covariance — the actual 3DGS analog — is the next and last candidate.

### Wave 3 — full-covariance splats win (the decisive positive result)

**Tried.** `forward2f.py` `SplatMixture2F`: a full 4×4 Cholesky covariance per
splat (15 covariance params; correlated projected covariance C = Uᵀ Σ U, the
cross term the separable model lacked), `wigner4`, and a dimension-agnostic
closed-form fidelity (Gaussian overlap with complex means; validated to 1e-12
against brute force, against |⟨00|cat⟩|², and against `forward2` on
block-diagonal mixtures). `fit2f.py`: analytic vectorized gradients (central-diff
to 3.7e-12), a principal-eigenvector split (the real 3DGS split), an anisotropic
birth field, and a **staged driver**:
blob envelope (variance-initialized, no true-state knowledge) → **convex
matched-filter over a thin-stripe basis** → Adam polish → convex weight cleanup.

**The matched-filter idea.** The fringe is *linear* in the weights of a
thin-stripe basis aligned to the p1 + p2 direction, so a single least-squares
solve recovers the signed fringe weights, replacing the unstable incremental
births that failed in the separable model. `matched_stripes` recovers the fringe
direction ±(p1 + p2)/√2 directly from the data residual.

**Key diagnostic.** The separable root cause "loss minimum caps fidelity at
~0.85" **does not hold** for full covariance: a hand-built fidelity-0.99 mixture
has *lower* loss than the blob solution at every budget. Both methods instead hit
the same finite-shot-noise ceiling. The ceiling was a property of the *separable*
representation, not the loss in general.

**Happened.** Acceptance (4×4 angle pairs × 3000 shots, rng = 42, verified
independently by the orchestrator): fidelity **0.9328 vs MLE 0.9236**, wall
**3.9 s vs 55.1 s (~12×)**, Wigner negativity −0.075 recovered, using **225 splat
parameters vs a 144×144 density matrix**. Seed sweep mean 0.923 (range
0.90–0.95). Suite: 40 passed, 1 xfailed. The tilted covariance means the fringe
needs ~10 splats instead of ~80.

**Learned — entanglement ⟺ tilted covariance.** Full 4×4 covariance is **not an
optimization convenience, it is the representation of entanglement**: one tilted
signed Gaussian stretches along the p1 − p2 ridge that a block-diagonal splat
cannot reach. Mode-cross correlation in the covariance is the splat-space image
of entanglement.

### Wave 4 — experiment 04, the official verdict table

`experiments/04_two_mode/run.py` runs both reconstructors on identical binned
data, 2 budgets × 3 seeds (42, 0, 7), with a two-mode displaced-parity
Wigner-slice helper validated against the `states2` closed form to 3e-8, and a
4-panel figure. The MLE-side histogram build is timed inside the block so both
wall-clock numbers include identical binning work.

**Official numbers (means over seeds 42 / 0 / 7):**

| budget (shots/pair) | F_splat | t_splat | F_mle | t_mle |
|---|---|---|---|---|
| 1000 | 0.9193 | 4.3 s | 0.9225 | 45.4 s |
| 3000 | 0.9205 | 4.1 s | 0.9264 | 26.5 s |

Aggregate: splat 0.921 ± 0.011 vs MLE 0.926 ± 0.007. The MLE truncation upper
bound (n_max = 12) is 0.99999. Both methods recover the entangled negativity
(Wmin ≈ −0.07 vs true −0.078).

**Verdict / roles-flip reading.** Compared with single mode, **the roles flip**:
- **Speed:** splat wins at every budget and every seed by **6–11×** (~4 s vs
  27–45 s) — the O(K) vs n_max^modes scaling separation the README predicted,
  now measured.
- **Fidelity:** a statistical tie. The gap (0.003–0.006) is *below* the seed
  noise (0.015–0.018); both methods sit at the same finite-shot ceiling.

The strict "win both on the mean" bar is **not** cleared (fidelity is a tie, not
a win), but the falsification trigger — *lose both* — is **not** activated.
Obtaining equal-quality reconstructions at ~1/10 the compute is itself the
computational gain the program was looking for. The precondition is full 4×4
covariance; separable splats fail outright at F = 0.50 (recorded xfail). The
decisive point remains 3 modes, where the Fock MLE reaches 12³ = 1728 dimensions
and should become impractical while the splat stays O(K).

---

## Open questions (as of 2026-07-07)

1. **Representation entanglement-cost conjecture.** Define
   R(α) = K_axis / K_tilted, the ratio of axis-aligned to tilted signed
   Gaussians needed to approximate the two-mode cat Wigner at *fixed* fidelity.
   At α = 1.5 the measured point is ≈ 8× (~80 axis-aligned vs ~10 tilted). Two
   candidate drivers: (a) the entanglement entropy of the state, which
   *saturates* with α; (b) the fringe wavenumber 2√2 α, which *grows* with α.
   Their α-dependence differs, so sweeping R(α) vs α distinguishes them —
   currently being swept by another agent; experiment 05 will decide. Why it
   matters: R(α) would be a *geometric complexity measure of entanglement*
   expressed in splat count.
2. **3-mode decisive test.** Fock MLE at 12³ = 1728 dimensions becomes
   impractical (R ρ R at minutes–hours); full-covariance splats stay O(K) with a
   6×6 Cholesky (21 covariance + 6 mean + 1 weight = 28 params/splat). If
   tractable at all, an MLE timeout is itself a recordable result (log
   wall-clock). Acceptance sketch in `docs/handoff.md` item 3.
3. **Density-operator positivity.** The splat Wigner is *not* guaranteed to be a
   physical state (ρ ⪰ 0). Options: Kenfack-type closed-form constraints vs a
   penalty term vs post-hoc projection. Needed before quoting paper-grade
   numbers.
4. **Fidelity statistical tie.** The exp-04 gap (0.003–0.006) is buried under
   seed noise (0.015–0.018); ~20 seeds would resolve whether MLE holds a real
   (if tiny) fidelity edge. Cheap on the splat side (~4 s/run), expensive on the
   MLE side (~30–60 s/run).
5. **Detector-noise modeling.** Current data are ideal-detector homodyne
   samples. Generalize the forward model to detection efficiency and Gaussian
   noise (Bernoulli loss → generalized), which the roadmap flags as unfinished.

## 2026-07-07 (later) — Experiment 05: the entanglement-cost conjecture, refuted and refined

Tried: measure R(alpha) = K_axis / K_tilted (minimal signed-Gaussian components,
axis-aligned vs tilted, to reach F_th = 0.99 against the exact two-mode cat Wigner)
across alpha in [0.75, 2.5], with a spike-proof relative-L2 criterion (raw fidelity
is cheatable by sub-Planck spikes: signed splats are a basis, not states), greedy
matching pursuit over validated closed-form Gram/overlap matrices, dictionary-width
robustness checks.

Happened: entanglement entropy E(alpha) = H2((1 + sech(2 alpha^2))/2) saturates at
1 ebit by alpha ~ 1.25, but R keeps climbing across the saturated tail (6.15 at 1.5
-> 8.68-9.62 at 2.0-2.5). log R vs log k has slope 1.02 (corr 0.956), k = 2 sqrt2
alpha; K_axis grows 28 -> 165 while K_tilted grows 10 -> 19. Same trend at F_th = 0.95.

Learned: the NAIVE conjecture ("representation cost ratio tracks entanglement") is
REFUTED — R tracks the nonclassical interference scale k, which grows without bound,
not the 1-ebit-saturating entanglement. Refined statement: tilt buys the
factorization saving m^2 -> m on the fringe, so R ~ m_1D(k) ~ k. Entanglement decides
WHETHER tilted components are needed at all (the qualitative separable failure);
the interference scale decides HOW MUCH they save (the quantitative ratio).
Recorded in issue #6.

## 2026-07-07 (evening) — Three-mode campaign: the first both-axes win

Waves: reference state (states3: fringe cos(2 sqrt2 a (p1+p2+p3)), prefactor
exactly 2, ceilings 0.9932/0.9996/0.99999 at n_max 8/10/12) -> full-covariance
fitter fit3f (6x6 Cholesky, 28 params/splat, ridge DETECTED from data) + MLE
tractability (mle3, 512 dims).

Happened (official budget: 27 triples x 2000 shots, bins=24, 0.14 counts/cell):
- splat: F 0.756/0.741/0.624 over seeds 42/1/2, negativity recovered on every
  seed, wall ~15 s single-threaded.
- MLE: 0.715 s/iter clean; 900 s budget -> 935 iters, F 0.701, converged=False
  (DNF). Loglik plateaus in ~40 iters while fidelity creeps at 6e-5/iter:
  17.7k measurement rows vs 262k density-matrix parameters (underdetermined).
  Honest extrapolation: 2+ hours to approach the 0.993 ceiling, if the ML
  fixed point of this dataset even sits there. n_max=10 costs x2.8.
- Two findings: (1) bin-average forward correction — density histograms are
  CELL-AVERAGE estimators; comparing model center values attenuates the fringe
  as a bias that grows with shots; radon3 convolves with the bin box
  (+width^2/12). (2) At 0.14 counts/cell the MSE loss minimum sits below the
  truth; nonlinear polish overfits; the convex matched filter is the honest
  estimator (polish off by default).
- Experiment 07 (20 seeds, two modes): paired t(19)=+1.62, p=0.121 — the
  fidelity tie is CONFIRMED; splat matches MLE at 7.4x less compute.

Learned: the scaling ladder is now measured end to end — 1 mode: MLE wins
speed 2x; 2 modes: tie at 7.4x less compute; 3 modes: splat wins BOTH
(F 0.756 vs 0.701-DNF, 15 s vs 900+ s). At >= 3 modes the splat reconstructor
is, practically, the only full-tomography option. Experiment 06 formalizes
this as the official run (in flight at the time of writing; its printed
verdict and figure land in experiments/06_three_mode/).

## 2026-07-11 — Issue #8 resolved (this benchmark): rho=BB† physical fit beats the splat

Waves: constructively-physical reparameterization (dream #1). Instead of placing
signed Gaussians in phase space (forward.py, no PSD guarantee), build a STATE and
derive its marginals. Pure ansatz |psi> = sum_c z_c prod_m D(alpha_c^m) S(xi_c^m)|0>,
p_theta(x) = |psi_theta(x)|^2 / Z -> physical (rank-1 PSD) by construction, and
|.|^2/Z needs no nonnegativity/sum penalty. Modules: bbdag.py (1-mode, squeeze),
bbdagM.py (multimode coherent-product kets, all quantities closed form via the
coherent overlap <a|b> = exp(-|a|^2/2 - |b|^2/2 + a* b)). oracle de-risked the
displaced-squeezed wavefunction + LO-phase rotation (alpha->alpha e^{-i theta},
xi->xi e^{-2 i theta}); it reduces to states.coherent_wavefunction at xi=0 (diff 0).

Happened:
- 1-mode gate (prototype): cat recovered at F=0.9999 with K=2 (a cat IS two
  coherent kets). Machinery validated.
- 3-mode decider, exp06 seed-42 data (27 triples x 2000 shots), SAME metric
  F = tr(rho_recon rho_cat3) = (2pi)^3 int W W as forward3f.fidelity_vs_cat3:
    signed splat (generic, ~15 s):   F 0.756 / 0.741 / 0.624 (seeds 42/1/2), UNphysical.
    splat PSD-projected:             F 0.48, physical but degraded.
    BB† K=4 (physical, ~300-530 s):  F 0.9501 / 0.9434 / 0.9332 (seeds 42/1/2).
    BB† K=8:                         F 0.9507 (seed 42).
- Diagnostic: NLL(fit)=3.9108 < NLL(true)=3.9153 on seed-42 data -> the fit sits
  at/below the finite-data ML optimum; F~0.95 is the DATA-LIMITED ceiling (ML
  overfits sampling noise slightly below the truth), and the splat's 0.756 sits
  below that ceiling.

Learned (scoped per oracle fairness review): FOR THIS 3-mode cat benchmark,
physicality is NOT the fidelity bottleneck -- a physical, cat-family-capable ML
ansatz reaches the finite-data fidelity ceiling ~0.95 on the identical metric,
so the signed splat's non-PSD negativity was NOT necessary for high fidelity
here. Honest scope: (a) the BB† ansatz CONTAINS the target family (two coherent
product kets), so this is target-aligned physical ML vs generic unphysical splat,
not generic-vs-generic; (b) "negativity was noise-fitting" is NOT yet claimable
(splat optimizes histogram-L2, not likelihood) -- needs a train/test held-out
comparison; (c) the FD optimizer is far slower than the splat (300-1600 s vs 15 s).
Open follow-ups to firm the claim: out-of-ansatz-family target (squeezed cat,
unequal amplitudes, mixed cat, loss channel), train/test split, analytic
gradients, and multimode squeeze. Figure: experiments/08_positivity/issue8_resolution.png.
