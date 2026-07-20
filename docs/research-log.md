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

**Tried.** Seeded the repository from an earlier exploratory spike: a fixed-K
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

## 2026-07-11 — Target-aligned rho=BB† achieves high fidelity on the synthetic benchmark

Waves: constructively-physical reparameterization (dream #1). Instead of placing
signed Gaussians in phase space (forward.py, no PSD guarantee), build a STATE and
derive its marginals. The resulting pure state is rank-1 PSD by construction.
Modules: bbdag.py (1-mode displaced-squeezed kets; finite-grid normalization) and
bbdagM.py (multimode coherent-product kets; closed-form norm via the coherent
overlap <a|b> = exp(-|a|^2/2 - |b|^2/2 + a* b)). oracle de-risked the
displaced-squeezed wavefunction + LO-phase rotation (alpha->alpha e^{-i theta},
xi->xi e^{-2 i theta}); it reduces to states.coherent_wavefunction at xi=0 (diff 0).

Historical reported observations:
- 1-mode gate (prototype): cat recovered at F=0.9999 with K=2 (a cat IS two
  coherent kets). Machinery validated.
- 3-mode exp06 data (27 triples x 2000 shots):
    signed splat (generic, ~15 s): target Wigner-overlap score
      0.756 / 0.741 / 0.624 (seeds 42/1/2), non-PSD.
    splat PSD-projected: reported state fidelity 0.48.
    BB† K=4 (physical, ~300-530 s): exact state fidelity
      0.9501 / 0.9434 / 0.9332 (seeds 42/1/2).
    BB† K=8: reported exact state fidelity 0.9507 (seed 42).
- Reported seed-42 training observations were NLL(fit)=3.9108 and
  NLL(true state)=3.9153. Their ordering says only that the reported fit assigned
  higher likelihood to those training samples than the true-state parameters did.
  It neither proves a global ML optimum nor defines a fidelity ceiling.
- The exp06 signed-splat baseline has a committed raw log. The BB†, PSD-projection,
  and NLL reports do not have retained raw stdout logs or fit parameters, so those
  historical values cannot yet be independently recalculated from repository artifacts.

Learned / scope: this is a benchmark-level existence result. A constructively
physical ansatz that contains the target family achieved high reported fidelity
on this synthetic cat benchmark. It is not a physicalization of the existing
signed-splat fit: the representation differs, and BB† optimizes per-sample NLL
while the splat optimizes histogram L2. The result therefore does not determine
whether the existing splat's negative-eigenvalue components are necessary for
its fitted overlap score. Open follow-ups: evidence-bundle capture, matched-objective
and held-out comparisons, out-of-family targets (squeezed cat, unequal amplitudes,
mixed cat, loss channel), analytic gradients, and multimode squeeze. Figure:
experiments/08_positivity/issue8_resolution.png.

## 2026-07-12 — Issue #6 entanglement-cost: one theorem + a sharp open problem

Turned experiment 05's empirical law R = K_axis/K_tilted ~ k (re-measured: log-log
slope 1.02, corr 0.956; m_1D common-width fit 1.70 k + 2.27, linear) into precise
statements (docs/2026-07-12-entanglement-cost-theory-note.md), oracle-de-risked.
- THEOREM: common-width translated real Gaussians need Theta(k) atoms to approximate
  cos(kp)e^{-p^2} (lower Omega(k) via Schoenberg total positivity / variation-diminishing:
  n translates -> <= n-1 sign changes, target oscillates Omega(k) times; upper O(k) by
  construction). This covers exactly the measured m_1D.
- THEOREM: K_tilted = O(k) by the rotate-to-(p1+p2)-and-elongate construction.
- OPEN (crux): K_axis = Omega(m_1D^2) -> R = Omega(k). Rank fails (function is rank-2
  separable u_c u_c - u_s u_s); sign-matrix fails ((-1)^{i+j} is rank-1). Needs a
  product-Gaussian-dictionary sparsity bound, not tensor rank. Also open: width-free
  m_1D = Omega(k) (adaptive widths defeat total positivity; empirically still linear).
- Reading: entanglement decides WHETHER a tilt is needed (separable F=0.50, saturates
  with E); interference scale k = sub-Planck fineness decides HOW MUCH it saves (R~k).
  Stellar rank (cat = infinite) is NOT the right complexity measure here; k is.

## 2026-07-12 (later) — C2 timebox: conjecture re-scoped (bounded atomic norm) + Ω(m_1D) upgraded

Timeboxed attempt on the C2 crux (K_axis = Ω(m_1D²)). A Sol/gpt-5.5 probe proposed a
counterexample: common-width product Gaussians with equal x/y width are ISOTROPIC
(rotation invariant), so a diagonal construction resolves the rotated fringe
e^{-u^2-v^2}cos(sqrt2 k u) in 1D → O(m_1D). VERIFIED NUMERICALLY
(experiments/08_positivity/c2_isotropic_escape.py) that this escape needs
EXPONENTIAL weights: bounded-coeff (|c|<=50) diagonal-isotropic never reaches
rel-L2<=0.14 for k=4,6,8; near-fits have max|c|=5.5e5 / 5.7e8 / 3.8e9. A narrow
isotropic atom (bounded weights) is narrow in v too → must tile 2D → back to m^2.
Outcome: (a) C2 as originally stated (unconstrained coefficients) is FALSE — fixed
by adding a BOUNDED-ATOMIC-NORM hypothesis (the regime exp05's spike-proof
criterion measures). (b) The slice lower bound is upgraded to theorem-grade
K_axis = Ω(m_1D) (common width) via even/odd orthogonality:
||(I-P_U)F||^2 = ||(I-P_U)C||^2||C||^2 + ||(I-P_U)S||^2||S||^2. (c) Ω(m_1D^2) at
bounded norm stays open. Note corrected accordingly; pivoting to track A next.

## 2026-07-13 — Track A step 1: analytic BB-dagger gradients (issue #25 resolved)

Tried: replace the finite-difference NLL gradient in fit_bbdagM (the priority
bottleneck named by the science recommendations: FD made 3-mode BB-dagger fits
cost 300-1600 s vs splat's 15 s) with the exact closed-form gradient. Both
pieces are Gaussian-overlap calculus: (a) Z = z^dag G z with G the
coherent-overlap Gram matrix, so dZ/d(z, alpha) differentiates log<a|b> =
-|a|^2/2 - |b|^2/2 + conj(a)b; (b) the sample term differentiates
log|psi|^2 through the coherent wavefunction, d log f/d(Re beta, Im beta) =
(sqrt2(x - sqrt2 Re beta) - i Im beta, i(sqrt2 x - Re beta)), pulled back
through the LO rotation beta = alpha e^{-i theta}. FD path retained as the
independent reference (fit_bbdagM(gradient="fd")).

Happened (exp06 data, 27 triples x 2000 shots, K=4 iters=200, committed raw
log experiments/08_positivity/out_bbdag_3mode_analytic.log, source commit
12ba509):
- verification: analytic vs central-diff max relative error 8e-10 / 7e-9 /
  2e-8 at (K,M) = (1,1)/(3,2)/(4,3), pinned in tests; same-init analytic and
  FD Adam trajectories land on the same state (rtol 1e-4).
- seed 42 K=4: F=0.9501 wall=10.6-16.6 s across container reruns --
  reproduces the historical FD report (0.9501, 527 s) to 4 decimals at
  32-50x speed; training NLL 3.9108 also matches the historical report.
- seed 42 K=8: F=0.9507 wall=17.6-28.0 s (FD: 0.9507, 1647 s -- 59-94x).
- seeds 1/2 K=4: F=0.9593 / 0.9566 (FD reports were 0.9434 / 0.9332) -- the
  exact gradient removes FD truncation noise (eps=1e-5) and lands higher; the
  seed-42 agreement shows this is the same optimum basin, not a different
  algorithm.
- provenance: the four analytic runs replace the historical_report_only
  BB-dagger primaries in the issue-8 registry with committed_raw_log records
  (figure regenerated). After PR-35 review, the evidence was made PORTABLE:
  the fitted parameters and optimizer trace are committed
  (experiments/08_positivity/evidence/bbdag_analytic_fits.json, from a
  clean-tree run at the recorded source commit), and a regression test pins
  that they recompute the registry fidelities; raw samples regenerate
  deterministically from the recorded data seeds. The acceptance criteria of
  issue #25 (central-diff match, O(10 s)-scale 3-mode fit, evidence-backed
  reproduction of the reported fidelities) are met with durable artifacts.

Learned: "physical AND fast" now holds in a single method -- the BB-dagger
reconstructor sits at the splat's timescale (K=4: 10.6-16.6 s, K=8:
17.6-28.0 s across container reruns, vs the splat's ~15 s) while keeping
PSD by construction, at F 0.95-0.96 vs the splat's non-physical 0.62-0.76
overlap score on the same data. The iteration-cost argument was exactly the
splat analytic-gradient story replayed (PR #1: 29 s -> 1.6 s): one closed-form
pass replaces 2 x 2K(M+1) NLL evaluations per step. This unblocks the rest of
track A: matched-objective / fair-baseline comparisons (#27) and out-of-family
targets (#28) now cost seconds per run instead of tens of minutes.

## 2026-07-13 (later) — Track A step 2: the fair baseline decomposes the BB-dagger win (issue #27)

Tried: the missing control for the exp06/exp08 comparison. Full-rank R rho R
(512-dim, F 0.676 DNF at 900 s) loses to BB-dagger K=4 (F ~0.95, 10 s), but
that comparison confounds the REPRESENTATION (coherent-product kets) with the
CONSTRAINT (rank-1, few parameters). New module purefock3.py: a GENERIC pure
Fock ket (n_max=8, 512 complex parameters), trained with the SAME per-sample
NLL, SAME Adam, SAME analytic-gradient discipline (gradient pinned vs central
differences at ~1e-8, tests). Also the held-out split issue #27 asked for:
train 1600 / test 400 shots per triple; per-sample NLL reported on both splits
for each method AND the true state. Experiment 09 (committed raw log), seeds
42/1/2.

Happened (means over 3 seeds; full table in experiments/09_fair_baseline/out_run.log):
- fidelity: purefock 0.979 (0.975-0.983; truncation ceiling 0.993) vs
  BB-dagger 0.959 (0.952-0.968). The GENERIC constrained fit is HIGHER.
- compute: BB-dagger 13.8 s vs purefock 155.6 s (~11x).
- held-out NLL: BB-dagger 3.9191 (at or slightly below the true state's
  3.9231 -- generalization at the noise floor; the small sub-true readings are
  within shared-test-set fluctuation) vs purefock 3.9329 (clearly above true:
  512 free parameters overfit). On TRAIN, BB-dagger undercuts the true state
  by MORE (~-0.0044 vs purefock's ~-0.0014) yet still generalizes at the true
  level, while purefock's smaller train undercut costs it ~+0.010 on test --
  the generic fit loses far more generalization per unit of train-likelihood
  gain.

Learned / verdict on the falsification condition (per axis -- the strict
conjunctive trigger "generic matches BB-dagger at <= compute" does not fire
because of the ~11x compute, but the axes SPLIT and must be reported as such):
- fidelity axis: PUREFOCK wins (0.979 vs 0.959) -- most of the fidelity gap
  over full-rank MLE (0.68 -> 0.98) comes from the pure-state CONSTRAINT plus
  per-sample gradient ML, not from the coherent ansatz. An ansatz fidelity
  advantage must NOT be claimed.
- compute axis: BB-dagger wins (13.8 s vs 155.6 s, ~11x), with ~32x fewer
  real parameters (32 vs 1024).
- held-out likelihood axis: BB-dagger wins (test NLL 3.9191 ~= true 3.9231 vs
  purefock 3.9329).
"Physical, fast, and generalizing" survives; "highest-fidelity" does not.
Also notable: R rho R's 0.676 was partly the ALGORITHM (fixed-point on binned
data), since the same 512-dim space under sample-level gradient ML reaches
0.98.

## 2026-07-13 (later) — Track A step 3: out-of-family targets + rank>1 BB-dagger (issue #28)

Tried: take the coherent rank-1 ansatz out of its family in two orthogonal
directions (new module states3x.py, sampling through the SAME grid sampler as
ThreeModeCat, now factored as states3.sample_homodyne_pdf3):
- MIXEDNESS: LossyThreeModeCat -- the cat after a per-mode pure-loss channel
  (transmissivity eta=0.8), via E(|a><b|) = <b|a>^{1-eta} |sqrt(eta)a><sqrt(eta)b|;
  rank 2, cross fringe damped by e^{-6 a^2 (1-eta)} (~0.067 at alpha=1.5).
  Tests pin: eta=1 reduces to ThreeModeCat, pdf normalized/nonnegative, and
  the lossy cat is EXACTLY a rank-2 BB-dagger state on its own coherent span.
- KET SHAPE: SqueezedThreeModeCat -- per-mode squeeze r=0.4 on the cat's kets;
  still pure, but squeezed kets are outside the coherent dictionary at any
  finite K. Fidelity via exact per-mode quadrature overlaps.
Plus the rank-R mixed extension itself (bbdagM.MixedCoherentKetState,
rho = sum_r |psi_r><psi_r| / Z), analytic NLL gradient (FD-pinned in tests),
and an EXACT Uhlmann fidelity on coherent-product spans (Loewdin
orthonormalization of the joint ket Gram -- no Fock truncation). Experiment 10
(committed raw log), data seed 42.

Happened:
- lossy cat: rank-1 plateaus at Uhlmann F 0.521-0.531 (K=2 vs K=4 barely
  differ -- capacity is not the bottleneck, rank is); rank-2 recovers
  F=0.9947 (K=2, 16 s) with better NLL (3.9062 vs 3.9101). The rank
  extension, not more kets, is what the mixed target demands -- exactly the
  predicted failure mode and fix.
- squeezed cat: coherent-K sweep F = 0.787 / 0.807 / 0.823 (K=2/4/8) --
  graceful but SLOW improvement; the constraint-matched generic control
  (purefock3) reaches F=0.961 on the same data (174 s). The coherent
  dictionary is inefficient for squeezed kets, as expected.

Learned / status (superseded 2026-07-13 later: experiment 11 below decides
the ruling): PARTIAL COMPLETION -- the issue-#28 falsification condition
compares BB-dagger against the SPLAT and MLE reconstructors on each
out-of-family target, and neither side has a pipeline for these targets yet,
so the condition is UNDECIDED (not "does not fire"). What IS established as
supporting evidence: the rank-2 extension recovers its enlarged family (lossy
cat: 0.53 -> 0.9947; an independent in-span bound puts the best rank-1 at
0.5336, matching the measured 0.5307 plateau), and out-of-family fidelity
improves monotonically with K. The squeezed-cat gap (0.82 vs the generic
control's 0.96) marks the next representation step: MULTIMODE
SQUEEZED-PRODUCT kets (the 1-mode machinery already exists in bbdag.py). The
rank-2 result opens the decoherence path (dreams #5: time-resolved tomography
of a decohering cat is now representable). Remaining scope for the actual
ruling: splat and full-rank-MLE sides of the 3-way comparison on these new
targets, more seeds, non-equal-amplitude targets (in-family, low priority),
and the squeezed-product ansatz.

## 2026-07-13 (later) — Track A step 4: squeezed-product ansatz + issue #28 scoped family-adaptability ruling (experiment 11)

Tried, part 1 — the representation upgrade exp10 pointed to: MULTIMODE
SQUEEZED-PRODUCT kets (bbdagS.py), |psi> = sum_c z_c prod_m D(alpha) S(xi) |0>,
with a fully closed-form analytic NLL gradient. The machinery is Gaussian
calculus end to end: pair overlaps <g_c|g_d> are complex Gaussian integrals
(A, B, C from the two kets' q, x0, p0), and every d log f/d(parameter) is a
degree-<=2 polynomial in x, so the norm gradient reduces to the overlap moment
ratios R1 = B/(2A), R2 = R1^2 + 1/(2A) — no quadrature anywhere. The xi = 0
phase singularity of (r, phi) is removed by nu = xi sinh|xi|/|xi|. Reduces
exactly to bbdagM at xi = 0; gradient pinned vs central differences (2e-7
with FD eps 1e-5, incl. through xi = 0 and both LO-rotation chains); the exact
squeezed cat scores F = 1 in closed form.

Happened, part 1 (exp10 squeezed-cat data, r=0.4, seed 42): K=4 reaches
F = 0.9695-0.9702 in ~20-40 s — above the generic Fock control (0.9611,
~150 s) and far above coherent K=8 (0.8228). Honesty note: K=2 (the exact
family size) is init-sensitive — init seeds 1/2 fall into bad local minima
(F ~ 0.00, 0.15) at 200 iters and seed 0 needs 400 iters to reach 0.9702;
K=4's redundancy makes the landscape benign. Overparameterize.

Tried, part 2 — the three-way scoring the ruling needs:
- splat side: closed-form target overlaps in forward3f. The lossy cat keeps
  the exact cat Wigner form (amplitude sqrt(eta) a, fringe damped by
  e^{-6a^2(1-eta)}); the squeezed cat maps symplectically onto the pure cat
  at amplitude a e^r via D(a)S(r)|0> = S(r)D(a e^r)|0>, so both reuse the
  validated Gaussian-overlap core. lossy_cat3_purity = the mixed target's
  perfect-score ceiling (0.5023 at eta=0.8, alpha=1.5).
- MLE side: fock.lossy_cat3_fock (truncated rank-2 target, trace 0.9983 at
  n_max=8) and a quadrature-projected squeezed-cat Fock ket (retention
  0.9944); Uhlmann / pure fidelity vs the mle3 reconstruction.

Happened, part 2 — experiment 11 (committed raw log; data seed 42, exp06
budget, mle3 at 900 s):

  lossy cat (eta=0.8, mixed; perfect overlap score = purity 0.5023):
    bbdag rank2 K=2   Uhlmann F 0.9947   21 s
    splat fit3f       overlap 0.4960     20 s  (98.7% of the purity ceiling)
    mle3 full-rank    Uhlmann F 0.9554   901 s DNF (431 iters)
    purefock rank-1   Uhlmann F 0.5169   186 s (wrong-rank control; in-span
                                                rank-1 ceiling is 0.5336)
  squeezed cat (r=0.4, pure):
    bbdag squeezed K=4  exact F 0.9700   54 s
    splat fit3f         overlap 1.7674   20 s  (see below)
    mle3 full-rank      exact F 0.7132   901 s DNF (462 iters)
    purefock rank-1     exact F 0.9611   183 s

RULING (issue #28, scoped per PR-36 review): the Boolean ruling compares
LIKE metrics only — BB-dagger vs MLE state fidelity — because the splat
overlap score is not commensurable (its perfect value is the target PURITY
0.5023 on the mixed target, and it is unbounded for a non-PSD fit); the
splat score is a separate axis. On the fidelity axis BB-dagger does not
lose on either target in THIS RUN (single data seed 42, single init seed;
squeezed-target margin over the purefock control is only +0.0089), so the
falsification condition does not fire. With its two extensions BB-dagger
attains the highest physical fidelity IN THIS RUN on both targets at
21-54 s, while full-rank MLE is DNF at 900 s on both.
[MULTI-SEED UPDATE, exp16 2026-07-16 (issue #39): replicated over 3 data
x 3 init seeds with the optional MLE arm. The squeezed rankings hold on
every seed (bbdagS K=4 0.9688-0.9761 > purefock 0.9610-0.9694 > MLE
0.68-0.72) but the margin over purefock is descriptive only (n=3
sign-consistent, cannot reach significance). The lossy verdict is
INIT-FRAGILE: rank-2 collapses to F ~ 0.52 on 3/9 inits at dNLL ~ 1e-4,
and best-by-train-NLL selection lands F = 0.9524 on data seed 1 — BELOW
the MLE's 0.9580 there — so "does not lose" fails on 1/3 data seeds
under an honest selection rule. See the exp16 entry.]

SCOPE CORRECTION (PR-36 review, accepted): both targets are out-of-family
only relative to the ORIGINAL rank-1 coherent ansatz — for the extensions
actually fitted here they are exactly IN-family (the lossy cat is rank-2
coherent by construction; the squeezed cat is a squeezed-product ket by
construction). What experiment 11 therefore establishes is the FAMILY'S
ADAPTABILITY: identify the failure direction, extend the ansatz to cover
it, win the like-metric comparison. It does NOT yet establish blind
generalization to targets outside the extended family. That gate needs a
held-out target no finite-rank ket mixture contains — e.g. a thermal-noise
lossy cat (full-rank rho; its per-mode Gaussian-convolution pdf is exactly
the detector-noise machinery already on the roadmap) — recorded as the
remaining gate before any "generalizing method" claim.

Bonus finding — the splat score of 1.7674 (> 1) on the PURE squeezed target
is a certificate of non-physicality: tr(rho sigma) <= 1 for any physical
sigma against a pure rho, so a score above 1 is only reachable by a non-PSD
reconstruction. The issue-#8 tension, previously inferred via Fock
projection, here shows up directly in the headline score. (On the lossy
target the splat score 0.4960 vs ceiling 0.5023 shows the splat DOES
reconstruct the damped-fringe Wigner well — the pathology is target- and
fit-dependent, not universal.)

Learned: Track A's three steps are all implemented and ruled AS SCOPED —
#25 (analytic gradients), #27 (fair-baseline decomposition), #28
(original-family out-of-family question + family adaptability; the
extended-family blind-generalization gate remains open, see the scope
correction above). The BB-dagger family now covers mixedness and squeezed
ket shape with closed-form gradients throughout, and the program's honest
headline is: "a physical, fast reconstructor family whose extensions
recover their enlarged families; fidelity leadership belongs to constraint
+ gradient ML, not to any particular ansatz; the signed-splat
representation remains the fast screener whose scores must be read as
overlap scores, not fidelities." Remaining (recorded): the held-out
full-rank target (thermal-noise lossy cat = detector-noise machinery),
multi-seed replication of exp11, and the mixed+squeezed combined ansatz
(rank-R over squeezed kets); then the public-data hunt (2026-07-13
position doc).

## 2026-07-14 — First real data: Furusawa-group GKP states (experiment 12, issue #41)

Tried: the program's first non-synthetic data. orange downloaded the Dryad
dataset of Konno et al., Science 383, 289 (2024) (propagating-light GKP
states; doi:10.5061/dryad.t76hdr86j, CC0) -- raw homodyne quadrature values
at six LO phases (0/+-30/+-60/-90 deg, ~20k shots each; found by the
public-data survey, docs/2026-07-14-public-data-survey--recorded.md, as the
ONLY confirmed open raw-homodyne dataset). Redistributed under
experiments/12_gkp_data/data/ with the original Dryad README. Convention
check from the data itself: 0-deg peak spacing ~1.69 ~ sqrt(pi) matches the
repo's vacuum-variance-1/2 units (no rescaling); a phase-INDEPENDENT mean
offset ~ -0.26 across 150 deg of LO phase is instrumental, not a coherent
displacement (which would rotate) -- fitted as-is, no subtraction.

Happened (exp12, committed log + marginal-overlay figure; held-out 20%):
- mle (R rho R, n_max=25, the paper's own method class): held-out
  per-sample NLL 1.6299, sub-second fit, marginals visually excellent.
- bbdagS pure squeezed-product (K=4/6, analytic gradients, ~30-40 s):
  held-out NLL 1.7670/1.7819 -- LOSES decisively. The overlay shows the
  signature failure: over-deep interference dips and over-tall peaks. A
  PURE state cannot wash out fringe contrast; the real (lossy) GKP state
  is MIXED. More kets do not help (K=6 is worse than K=4 on held-out --
  overfitting within the wrong manifold).

Learned -- first real-data verdict, recorded as promised: on real data the
current physical reconstructor loses to the textbook full-rank MLE at one
mode, because the deficit is RANK (mixedness) and detection efficiency, not
ket shape. This is precisely the gap the already-filed extensions target:
rank-R x squeezed ansatz (issue #40) and the efficiency/noise forward model
(issue #42) now have a concrete real-data benchmark (beat NLL 1.6299 on
this dataset while staying constructively physical and O(K)-parametric).
Note the scale caveat: at ONE mode the MLE matrix is tiny (25x25) and
sub-second -- the program's scaling argument is untouched; what real data
tests is physics fidelity of the forward model, and mixedness is the first
missing piece. GKP itself is the dreams-#7 native-fit target: the fitted
squeezes (r ~ 0.4-1.0) confirm the ansatz reaches for the comb structure.

CORRECTION (2026-07-14, owner review of PR #37): the claim "more kets do
not help -- K=6 overfits within the wrong manifold" was wrong. K=6 was
worse than K=4 on TRAIN NLL too, which a nested family cannot be at a
well-optimized solution -- that is an optimization failure, not
overfitting. The exp13 multi-seed retest (best-of-3 by train) confirms:
pure K=6 still trains worse than pure K=4 (1.75386 vs 1.74336), so at this
budget OPTIMIZATION, not the family, is the limit, and no overfitting
claim is supported either way.

## 2026-07-14 — GKP rematch: exploratory loss-model reanalysis (experiment 13, issue #42 partial)

(This entry replaces a first version whose protocol the owner review of
PR #37 correctly rejected: it selected K on the test set, attributed the
eta effect across unequal configs, compared parameter counts against one
arbitrary MLE cutoff, and reused the exp12 split for every decision. The
post-review protocol was declared before the rerun, but only after the
dataset and first-run results had been inspected; this is therefore an
exploratory reanalysis, not preregistered confirmation. It fixes the primary
config at lossy K=4, selects init seeds {0,1,2} by TRAIN NLL with convergence
flags, uses same-K same-budget eta ablations, and reports an n_max dof
frontier. Its best MLE point is selected on test data and its paired bootstrap
intervals are conditional on that selection. Split seed 1 reshuffles the same
observations as a sensitivity check, not as an independent holdout.)

Tried: bbdagS gained a detection-efficiency forward model: the measured
pdf is the pure ansatz pdf convolved with the loss Gaussian (variance
(1-eta)/2 + optional electronic noise), which is EXACTLY the homodyne
marginal of loss_eta(|psi><psi|/Z) -- PSD by construction, closed form
throughout (the pair-overlap Gaussians get tilted: A -> A + eta/(2 s^2),
B -> B + (sqrt(eta)/s^2) x; the d log f polynomial trick then gives the
analytic gradient via tilted moment ratios). eta is fitted jointly (logit
+ scalar central difference), with range validation. Pinned by 12 tests,
including exact agreement with the Fock-basis loss channel (a fully
independent route) and eta recovery on synthetic lossy-cat samples.

Happened (exp13 committed log, overlay + NLL-dof frontier figures;
held-out per-sample NLL within each split):
- Same-K eta ablation, primary split: K=4 pure 1.75542 -> lossy 1.63304
  (97.5% of the gap to the empirical MLE frontier best 1.62984); K=6 98.2%;
  alternate-split reshuffle 97.8%. Adding one physical parameter accounts
  for most of the observed improvement in every like-for-like comparison;
  fitted eta is stable at 0.638-0.643 across K, seeds, and splits.
- Headline "matches full-rank MLE on real data": DESCRIPTIVE LOSS for these
  fitted models. The empirical, test-selected best MLE stays below lossy
  K=4 on both reshuffles. Conditional paired-bootstrap intervals are
  [+0.0022, +0.0041] on the primary split and [+0.0016, +0.0034] on the
  alternate split, both above zero. These intervals condition on the
  fitted models and test-selected n_max; they do not account for model
  selection and therefore do not establish confirmatory significance.
- Parameter efficiency has an observed Pareto comparison (the "1/17"
  framing was wrong -- the MLE frontier is flat above n_max ~ 8, dof 63):
  at comparable dof, lossy K=4 (23 dof) has NLL 1.63304 versus MLE n_max=6
  (35 dof) at 1.63534. The frontier figure shows the red points below the
  observed MLE curve in their dof band.
- exp12 correction confirmed (see the corrected exp12 entry): pure K=6
  still TRAINS worse than K=4 under best-of-3 seeds, an optimization
  artifact, not overfitting.

Learned: the same-K ablations support mixedness-by-loss as a useful
working diagnosis, with 97.5-98.2% observed gap closure across primary and
alternate reshuffles. They are a repeated-split sensitivity result, not
independent confirmation, because both partitions reuse the same
observations. The honest current summary is that a 23-dof constructively
physical model with one loss parameter has an observed Pareto relation at
comparable dof and sits 0.002-0.004 nats behind the empirical, test-selected
MLE frontier for these fits. The residual's physical cause is not identified:
optimization, finite-K or pure-state capacity, and misspecification of a
single Gaussian loss channel remain open alternatives. Issue #40 tests
rank-R x squeezed as one hypothesis rather than receiving a confirmed rank
diagnosis. #42 itself stays OPEN: this is the bbdagS vertical slice; the
issue's full scope (known-eta deployment across bbdagM / purefock3 / splat +
controlled comparisons) remains.

## 2026-07-14 — Rank freedom on real data: exploratory rank-hypothesis test (experiment 14, issue #40)

Tried: exp13 left a descriptive residual (+0.002..+0.004 nats vs the
test-selected MLE frontier) with its cause explicitly unidentified --
optimization, ket capacity, and loss-channel misspecification all open.
Exp14 tests the RANK hypothesis: bbdagS gained MixedSqueezedKetState
(rho = B B^dagger over R independent squeezed-ket columns, composed with
the #42 loss channel; PSD by construction, closed form, analytic
gradients = the rank-1 pair-density machinery summed over columns).
Pinned by 10 tests including an exact rank-2 B B^dagger factorization of
the lossy cat against the Fock-basis loss channel. Same exploratory
framing as exp13 (dataset and prior results already inspected; split
seeds 0/1 are the same reshuffles; MLE opponent is the test-selected
frontier best; bootstrap intervals are conditional on the fitted models).
Primary config pre-fixed at lossy R=2 K=4 against a same-schedule rank-1
baseline; R=3 K=4 as a never-test-selected saturation probe.

Happened (committed log, overlay + frontier figures; held-out per-sample
NLL, conditional paired-bootstrap 95% CIs):
- The R2K4 parameterization adds descriptive predictive capacity on both
  reshuffles: CI(R=2 - rank1) = [-0.00296, -0.00143] primary and
  [-0.00283, -0.00124] alternate. ATTRIBUTION CAVEAT (owner review of
  PR #44): this comparison changes the ket primitive count (4 -> 8), the
  dof (23 -> 46), and the compute per iteration together with the rank,
  so whether the gain comes from physical rank or from the accompanying
  ket/parameter capacity is UNRESOLVED here -- the matched-dof control
  (R=1,K=8 = 47 dof vs R=2,K=4 = 46 dof, control_k8.py) addresses it
  below.
- The frontier gap SHRANK but REMAINS for these fits: CI(R=2 - best MLE)
  = [+0.00055, +0.00149] primary (point +0.00100, down from exp13's
  +0.00320) and [+0.00002, +0.00093] alternate (point +0.00048 --
  borderline at CI resolution). Recorded as another descriptive loss,
  the third on real data, now by half a millinat.
- The Pareto band WIDENED: R=2 (46 dof) 1.63084 and R=3 (69 dof) 1.63009
  sit below the observed MLE curve in their dof bands (n_max=6/35 dof
  1.63534, n_max=8/63 dof 1.63036); on the alternate reshuffle R=2 at
  46 dof (1.62770) is below the MLE curve until ~99 dof. Train NLL
  improves monotonically R=1 -> 2 -> 3 (1.62938, 1.62761, 1.62688) at
  the same optimizer schedule -- but capacity and compute grow with R,
  so the supported statement is only that the train objective had not
  plateaued under this R/K schedule, not that "rank is unsaturated".
- eta-rank identifiability drifted as pre-declared: fitted eta 0.643 ->
  0.701 -> 0.875 for R=1/2/3. Rank absorbs mixedness that the loss knob
  no longer must carry; fitted eta is a model parameter here, NOT a
  calibrated detection efficiency.

CONTROL RESULT (control_k8.py, committed log; run after the amendment
above): the matched-dof comparison the review asked for -- R=1,K=8
(47 dof) vs R=2,K=4 (46 dof), identical schedule, both reshuffles. The
nested under-optimization check PASSED (R1K8 best-of-3 train NLL 1.62882
/ 1.62952 is below the R1K4 floor 1.62938 / 1.63019, so K=8 was not the
exp13-style optimization casualty). At matched dof the rank
parameterization wins held-out on both reshuffles: test NLL 1.63084 vs
1.63216 (primary) and 1.62770 vs 1.62936 (alternate), conditional paired
CI(R2K4 - R1K8) = [-0.00194, -0.00067] and [-0.00230, -0.00100]. A
consistent side observation: the pure-column R1K8 fit keeps eta pinned
at 0.640 (all mixedness must go through the loss knob) while R2K4 sits
at 0.70. Reading, per the pre-declared branches: capacity-matched
DESCRIPTIVE support for the rank hypothesis -- the exp14 gain is not
attributable to ket/parameter capacity alone. Still exploratory (same
reshuffles, conditional intervals); "physical rank identified" remains
too strong, but "capacity alone explains it" is now descriptively
disfavored.

Learned (amended per the PR #44 owner review, which flagged the original
rank attribution as confounded): the R2K4 extension improved descriptive
predictive performance on both reshuffles, cutting ~2/3 of exp13's
residual on the primary one -- but whether that gain comes from physical
rank or from the accompanying increase in ket/parameter capacity was
initially unresolved; the matched-dof control above then made the
capacity-only explanation descriptively DISFAVORED, while still not
identifying physical rank (same-data reshuffles, conditional
intervals). The remaining half-millinat stays unexplained (deeper rank,
non-Gaussian noise, optimization all open). The program's honest
position after three real-data rounds: constructively physical
BB-dagger extensions now trace the MLE's NLL-dof frontier from below
through dof ~69 and lose the asymptote by ~0.0005-0.0010 nats on these
reshuffles; each round's deficit produced a concrete next hypothesis,
though no round has yet identified its residual's cause. #40 stays open
(deeper R, warm starts, K interplay); #42's known-eta deployment across
the other reconstructors is unchanged.

## 2026-07-15 — Outreach demo: the birth field, exported to plain image fitting (demos/birthfield_image, #46 idea 4)

(Entry rewritten twice under the PR #49 review: round one caught an
Adam-moment inconsistency at growth events, an attribution confound, an
untested sign invariant, and asset/state mismatches; round two caught an
UNPAIRED aggregation that overstated the ablation effect and an
over-broad "placement dominates" attribution. Numbers below are from the
corrected rerun with paired aggregation.)

Tried: the first deliverable of the applications track (#46) -- a
self-contained demo (core fitter numpy-only) restating exp02's
densification lesson on an audience-friendly target: the cat Wigner
function fitted AS AN IMAGE by signed 2D Gaussian splats. Growth rules
under a shared budget: split (parent-sign-preserving baseline; invariant
tested directly on split_one) vs birth-field placement, plus the ablation
isolating ONLY the newborn's initial weight: signed / forced positive /
zero.

Happened (committed log, 3 seeds per mode; HEADLINE at the fixed shared
budget of 1000 updates, all modes at K = 10; 4000-iter numbers kept as a
one-off auxiliary record; the GIF is a fixed-seed illustration, not
comparison evidence):
- Honesty corrections: (a) "split can never obtain negatives" is wrong
  for this objective -- the optimizer drags weights through zero; split
  runs end with 11-19 negatives; what holds is that splitting itself
  preserves sign. (b) The first run's ratios (up to 25496x) carried an
  Adam bookkeeping artifact (moments zero-padded while the
  bias-correction clock reset); fixed by resetting both together.
  (c) The second run's "zero-init ~10x better" was an UNPAIRED-median
  artifact; paired per-seed ratios tell the honest story.
- HEADLINE: per-seed paired split/birth loss ratios at 1000 updates =
  767x / 18x / 493x (declared bar 10x -- passed on every seed).
  Auxiliary final ratios 52-85x.
- Ablation, paired per seed: birth_pos/birth median 0.99x at 1000
  (1.46x final), birth_zero/birth median 0.84x at 1000 (0.53x final).
  So SIGN INJECTION IS NOT A MAIN FACTOR (forced-positive matches
  signed; zero-init is comparable-to-better on these seeds). What the
  data support: the COMPOSITE birth rule (placement + initial scale +
  generation method) beats this split baseline. Placement-ALONE
  attribution would need a separate scale/position ablation, not run.

Learned: three of this demo's own narratives died under review-driven
measurement (never-negative, the inflated ratios, the sign-injection
story), and the survivor is still a strong, simple recommendation for
the 3DGS audience: spawning new Gaussians at the closed-form
birth-field argmax -- with the sign left to the optimizer -- beats
gradient-norm splitting by 1-3 orders of magnitude at a matched budget
on this signed target. The applications-track template in both senses:
small and self-contained, with claims cut to exactly what paired
measurements support.

## 2026-07-16 — Application mainline declared + Phase 0 gate: confidence certificate for few-view 3D (experiment 15, issue #48)

Owner decision: issue #48 is the applications-track MAINLINE, re-scoped
to "6-second video (or few images) -> confidence-annotated 4DGS", with
the staged gates kept (static 3DGS + confidence must pass Gates A/B
before the dynamic extension). The quantum core line (#42 remainder,
#40 follow-up, #39) continues in parallel — this track is the outward
face, not a replacement.

Phase 0 setup (all declared on the issue before running): no
GPU/torch/gsplat in the environment, so a numpy-only minimal renderer —
isotropic signed 3D Gaussians, ADDITIVE emission imaging (no occlusion,
no alpha compositing), pinhole projection with paraxial footprints
(sigma_img = f sigma / z). The physics that survives the simplification
is the monocular size-distance degeneracy, broken only by parallax.
Synthetic scene of 10 signed splats, "6 seconds" = 24 frames with total
baseline 0.8 at depth ~6 (parallax ~0.13 rad), pixel noise 0.02,
inverse crime accepted deliberately (the question is
information-vs-error, not model mismatch). Gate A: covered-region
Spearman between the certificate and the TRUE density error >= 0.3 on
all 3 seeds.

Round 1 — FAILED, recorded (out_round1.log): the pure-geometry score
(lambda_min of a unit probe splat's Gauss-Newton information; sees
camera geometry only, never pixels) landed at rho = -0.101 / +0.096 /
-0.200. The all-points correlation was NEGATIVE: true error
concentrates on structure in the well-covered center (fit
imperfection), while information-starved empty regions are cheap to
get right. A score decoupled from model amplitude measures "where you
COULD be wrong", not "where you ARE wrong".

Round 2 — PASSED (out_run.log; score re-declared on the issue before
running, same gate numbers): delta-method predicted uncertainty
sigma_pred(x)^2 = J_rho(x)^T (H + eps I)^{-1} J_rho(x), H = the fitted
model's Gauss-Newton matrix over all frames, eps = 1e-9 tr(H)/P fixed
in advance. Sees the video (through the fit) and the model — never the
truth. Covered-region Spearman = +0.909 / +0.863 / +0.763 (bar 0.3,
every seed). Auxiliaries: all-points +0.910 / +0.919 / +0.798,
model-support-restricted +0.827 / +0.823 / +0.415; the round-1 score
kept for comparison stays near zero.

Controls (added per the PR #54 review — sigma_pred contains J_rho, so
it could track fitted amplitude/support rather than information): on
the same seeds and masks, |rho_fit| reaches covered Spearman +0.889 /
+0.835 / +0.911, ||J_rho|| (the H = I score) +0.851 / +0.619 / +0.903,
diagonal-H +0.796 / +0.533 / +0.812. sigma_pred leads on seeds 0/1 and
on the support mask there, but on seed 2 the plain fitted-amplitude
control BEATS it on both masks — no consistent uplift.

Learned (narrowed under review): what these data support is that THIS
fitted-model-dependent score passed the declared toy Phase 0 gate;
attributing the gain to information propagated through H^{-1} is NOT
supported — simple amplitude/support tracking explains most of the
correlation, and beats the certificate outright on one seed. What
survives of the causal story is round 1's negative half: information
ALONE (never coupled to the model) certifies nothing here. Whether the
H^{-1} propagation adds anything beyond amplitude tracking becomes a
declared gate candidate for Phase 1, where occlusion and model mismatch
should separate the two. Scope: additive-emission inverse-crime
synthetic Phase 0 only; nothing here claims occlusion handling or
real-video performance. Pins: tests/test_gauss3d.py (9 tests — FD
gradients, probe/Jacobian brute-force matches, parallax raises
lambda_min, predicted sigma falls with baseline).
## 2026-07-16 — Multi-seed replication of experiment 11 (experiment 16, issue #39)

(Numbering note: this experiment lives in experiments/16_exp11_seeds.
It ran as "exp15" before the parallel application line's experiment 15
(15_video_conf, issue #48) merged first, and was renumbered; the
committed raw log headers still print exp15 and are left untouched.)

Tried: exp11's ruling rested on a single run (data seed 42, init seed 0),
and its squeezed-target margin over the generic control was only +0.0089.
Exp15 reran the seed-sensitive fits over data seeds {42, 1, 2} x init
seeds {0, 1, 2} with the exp11 configs unchanged (45 fits), plus the
issue's optional MLE arm (deterministic given the data, so data-seed axis
only: 6 runs at the exp11 MLE config). Declared before the run: init
selection is best TRAIN NLL per data seed (never fidelity); the K=2
success threshold is F >= 0.9; and the n=3 paired design bottoms out at a
sign-test p = 0.125, so it CANNOT certify significance — any consistent
sign stays descriptive by construction.

Happened (committed logs + results json):
- All four exp11 single values (0.9947 / 0.5169 / 0.9700 / 0.9611) fall
  inside their measured 9-cell ranges.
- SQUEEZED target replicates robustly: bbdagS K=4 spans F 0.9688-0.9761
  over all 9 cells (spread ~0.007), purefock 0.9610-0.9694, MLE
  {0.7157, 0.7007, 0.6767}. The bbdagS-vs-purefock margin is
  sign-consistent — paired best-by-NLL diffs +0.0089/+0.0043/+0.0108,
  9/9 cells positive — but per the pre-declared rule this is a
  DESCRIPTIVE advantage only; the honest exp11 rewrite is "BB-dagger and
  the generic control are statistically indistinguishable on the squeezed
  target at this design (consistent-sign ~+0.004..+0.011), while both
  beat the MLE by ~0.25-0.30."
- LOSSY target: the verdict is INIT-FRAGILE. The rank-2 coherent fit
  collapses to F ~ 0.52-0.55 (the rank-deficient mode) on 3/9 inits
  while the train NLL moves by only ~1e-4..3e-3 nats; best-by-NLL per
  data seed = {0.9947, 0.9524, 0.9948} against a stable MLE
  {0.9550, 0.9580, 0.9580}. On data seed 1 the NLL-selected BB-dagger
  fit (0.9524) sits BELOW the MLE (0.9580) even though an F = 0.9947
  init exists at dNLL ~ 1e-4: the training objective cannot see a
  0.4-fidelity difference at this budget. exp11's "does not lose"
  therefore survives 2/3 data seeds and FAILS on the third under the
  declared selection rule.
- K=2 vs K=4 init sensitivity (issue item 3): K=2 fails 2/9 (F 0.7754
  and 0.8414, both at init seed 1); K=4 passes 9/9. The catastrophic
  K=2 failures recorded in the exp11 entry (F ~ 0.00/0.15) were at a
  200-iter schedule; at the 400-iter schedule used here the failure mode
  is milder — consistent with an optimization-schedule artifact on top
  of a genuinely worse K=2 landscape. Overparameterizing in K remains
  the cheap, effective fix.

Learned: seed noise was the right thing to fear, but it lives in a
different place than the issue guessed. The squeezed-target rankings are
seed-robust and the +0.0089 margin replicates in sign — it just cannot
be certified at n=3, so it is downgraded to descriptive per the
acceptance criteria. The genuinely fragile number is the LOSSY-target
0.9947: the rank-2 landscape has a collapse mode that the likelihood is
nearly blind to (dNLL ~ 1e-4 vs dF ~ 0.4), so single-init headline
fidelities on mixed targets should be read as "best observed", not
"typical". Follow-up recorded, not opened as an issue yet: a
selection-robust practice for mixed-target BB-dagger fits (more inits,
or a fidelity-blind diagnostic such as the fitted state's own purity /
column Gram rank) would close the gap between best-observed and
NLL-selected.
## 2026-07-16 — Loss model deployed across all reconstructors + the noise control (experiment 17, issue #42 full scope)

(Numbering note: this experiment lives in experiments/17_loss_control.
It ran as "exp16" before the parallel application line's experiment 15
(15_video_conf, issue #48) merged first and shifted the quantum-line
numbering; the committed raw log headers still print exp16 and are
left untouched.)

Tried: the remaining #42 scope — take the exp13 loss forward model
(measured pdf = pure pdf convolved per mode with N(0, sigma2),
sigma2 = (1 - eta)/2 + electronic noise) out of bbdagS and into every
other reconstructor, each by the route its representation makes natural:
  * bbdagM (coherent, rank-1 and rank-R): DELEGATION. A coherent ket is
    the xi = 0 slice of the squeezed ansatz, so the lossy pdf / NLL /
    analytic gradient are the bbdagS pair machinery evaluated at xi = 0
    with the xi gradient block dropped — exact, nothing re-derived.
    Known-eta and jointly-fitted-eta modes both exposed.
  * purefock3: per-mode inefficient-homodyne POVM matrices
    Phi[n,n'](x) = int psi_n(y) psi_n'(y) N(x - sqrt(eta) y; sigma2) dy
    by a Gauss-Hermite rule that is EXACT (polynomial x Gaussian
    integrand), so electronic noise is supported with no truncation
    error; a truncated-Kraus route serves as the independent test
    cross-check at sigma_el = 0. p = psi^dag (E1 x E2 x E3) psi / Z via
    three sequential mode contractions; known-eta fitter.
  * splat (forward3f / fit3f): the measurement map on the projected
    Gaussians, m -> sqrt(eta) m, C -> eta C + sigma2 I — and because the
    projection columns are orthonormal (U^T U = I), this equals the
    PHASE-SPACE loss map mu -> sqrt(eta) mu, Sigma -> eta Sigma +
    sigma2 I_6 on the mixture itself. The fitted splat therefore
    estimates the PRE-loss Wigner function and every pure-target overlap
    score applies unchanged. Threaded through all fit3f stages including
    the blob_span variance inversion.
  * data3.apply_detection_noise: detector-side noisy sampler for ANY
    target's ideal samples.
Pinned by 22 new tests (eta = 1 exact reduction everywhere; agreement
with numerical convolution AND the Fock/Kraus channel on independent
routes; FD gradient checks with the loss on; parameter validation); the
full suite passes at 181. A latent convention subtlety surfaced:
purefock3's amplitude (sum psi_n v_n, unconjugated) and
fock.marginal_from_rho are mutually CONJUGATE phase conventions —
invisible for real-coefficient states (every state pinned before now),
visible for random complex ones; documented where the tests hit it.

Happened (experiment 17, pre-declared ignore/known/fitted control on a
pure cat3 with known detector noise eta = 0.8, sigma_el^2 = 0.02, 27
triples x 1000 shots, single data seed, descriptive):
    bbdagM K=2   ignore 0.6188 | known 0.8246 | fitted 0.5085 (eta -> 0.56)
    purefock3    ignore 0.8925 | known 0.9727
    splat        ignore 0.4364 | known 0.5009   (overlap-score axis)
Ignoring the detector costs every reconstructor and the known-eta
correction recovers most of it (purefock3 to 0.9727 against the ~0.993
truncation ceiling). The surprise is the FITTED arm: jointly fitted eta
landed at 0.5635 with F = 0.5085 — worse than ignoring the noise.

Diagnostic (diagnose_eta.py, committed log; discriminator declared
before running: start sensitivity vs identifiability): refits from
eta0 = 0.6 AND 0.79, three inits each, ALL land on one train-NLL plateau
(3.96110-3.96112, with the known-eta reference at 3.96109) while fitted
eta scatters 0.56-0.77 and fidelity scatters 0.06-0.80. The likelihood
at this budget is flat to ~1e-5 nats along a (state, eta) direction
across fits whose fidelity differs by 0.74: a genuine IDENTIFIABILITY
failure, not under-optimization. Known eta pins the model to the right
member of the plateau — that is what the calibration knob is for.

Learned: the known-eta deployment holds across every representation with
the closed-form discipline intact (the only integral anywhere is an
exact finite Gauss-Hermite rule). And "fit eta jointly" is not a free
lunch: it was safe on the GKP data (exp13: ~60k single-mode samples,
fitted eta stable at 0.638-0.643 across seeds and splits) and is UNSAFE
on a 27k-sample three-mode cat, where eta is unidentifiable and fidelity
collapses silently while the NLL moves by 1e-5. This is the same
budget-blindness exp16 (the exp11 multi-seed replication, issue #39)
exposed on the init axis, seen here on the eta
axis: at small budgets the training objective cannot see directions
fidelity cares about. Practical rule going forward: calibrate eta when a
calibration exists; fit it only with enough per-mode data; read fitted
eta as a model parameter (exp14's pre-declared stance) always. #42's
full scope (bbdagM / purefock3 / splat deployment + known-vs-fitted
control) is complete; #38's thermal-noise held-out target shares this
Gaussian-convolution machinery as designed.

## 2026-07-16 — Rank saturation on the GKP data: the frontier gap closes (experiment 18, issue #40)

(Numbering note: this experiment lives in experiments/18_gkp_saturation.
It ran as "exp17" before the quantum-line renumbering triggered by the
application line's experiment 15; the committed raw log header still
prints exp17 and is left untouched.)

Tried: exp14 left three threads open -- the rank curve had not plateaued
at R=3, warm starts were untested, and the rank-vs-K interplay had only
the 46/47-dof control point -- with the frontier deficit at half a
millinat. Exp18 runs the pre-declared saturation protocol: cold R=4
(both reshuffles) and R=5 (primary), a warm-start chain R3 -> 4 -> 5
(grow the best parent by one small-weight column;
fit_bbdagS_lossy_mixed gained an init= hook for it), a matched ~70-dof
K-interplay pair (R3K4 = 69 dof vs R2K6 = 70 dof), and the MLE frontier
rerun per split. Same exploratory standing caveats as exp13/14/17 (same
reshuffles, test-selected MLE opponent, conditional intervals). The R=3
refits reproduced exp14's committed numbers exactly (train 1.62688
primary), pinning cross-run reproducibility on this machine.

Happened (committed log, results json, frontier figure; conditional
paired bootstrap 95% CIs):
- SATURATION (decision check 1): best-by-train deltas delta(4) =
  +0.00016 < the declared 0.0002 flatness threshold; delta(5) = +0.00000
  exactly. Held-out follows: R3 1.63009, R4 1.62993, R5 1.62995
  (primary). The rank curve saturates at R = 4-5 under this schedule.
- FRONTIER (decision check 2): CI(R4 - test-selected best MLE) =
  [-0.00002, +0.00020] (point +0.00009) on the primary reshuffle and
  [-0.00017, +0.00003] (point -0.00007) on the alternate. Both straddle
  zero: per the pre-declared branches the fits TIE the empirical MLE
  frontier at CI resolution -- the first real-data round without a
  descriptive loss, after three straight losses (exp12/13/14). The
  physical model does it at 92 real dof against the MLE frontier best's
  255, and the tie is with a test-selected oracle opponent.
- OPTIMIZATION (decision check 3): warm R=4 beats the cold best by only
  0.00003 train nats (< the declared 0.0001), so the cold schedule is
  adequate at R=4 and under-optimization is descriptively disfavored as
  the residual's cause. The warm chain's endpoint (warm R=5, train
  1.62663, test 1.62990) is consistent with the same plateau.
- K INTERPLAY (decision check 4): at matched ~70 dof the rank split wins
  held-out: CI(R3K4 - R2K6) = [-0.00098, -0.00018]. Together with
  exp14's 46-dof control, a dof spent on rank beats a dof spent on ket
  count at both probed frontier points.
- ETA DRIFT (decision check 5, pre-declared): fitted eta climbs 0.87 ->
  0.94 -> 0.92 for R = 3/4/5 and reaches 0.9948 on the warm R=5 chain:
  as rank grows the loss knob is squeezed out entirely, and the model
  converges toward a pure rank mixture. Fitted eta remains a model
  parameter, not a calibrated efficiency.

Learned: the exp13 residual is now fully walked down -- loss modeling
closed 98% of the pure-model gap (exp13), rank-2 cut the remainder by
two thirds (exp14), and rank-4 closes the rest to a statistical tie
with the empirical MLE frontier on both reshuffles (this run), with
matched-dof controls attributing each step to rank rather than
capacity, and warm starts ruling out under-optimization at the end
point. The honest headline after four real-data rounds: a
constructively physical rank-4 x squeezed x loss model with 92 real
parameters ties the test-selected full-rank MLE frontier on the Konno
et al. GKP dataset at CI resolution, on the same exploratory reshuffles
every prior round used. What it does NOT say: no independent holdout
exists (the splits reuse the same observations), the opponent is
test-selected (favoring the MLE), and "ties" is a CI statement, not
preregistered confirmation. #40's saturation question is answered
(R = 4-5, schedule-adequate); the natural next step on this dataset is
an INDEPTH preregistered confirmation only if a fresh dataset or a
held-out session becomes available (#41 scope).

## 2026-07-16 — The blind-generalization gate: thermal-noise lossy cat (experiment 19, issue #38)

(Numbering note: experiments 15-18 were taken by the time this ran
(15_video_conf #48, 16_exp11_seeds #39, 17_loss_control #42,
18_gkp_saturation #40); this one lives in experiments/19_thermal_gate.)

Tried: the gate exp11's scope correction demanded before any
"generalizing method" claim -- a held-out target NO finite-rank ket
mixture contains. Target: the lossy cat followed by per-mode classical
Gaussian displacement noise (states3x.ThermalLossyThreeModeCat; eta=0.8,
sigma_add=0.1 variance per quadrature; purity 0.2882 -- genuinely full
rank). Machinery, all pinned by tests on independent routes
(tests/test_thermal_target.py): closed-form pdf via the issue-#42 pair
machinery at eta=1 on the target side; a numerically exact Fock-route
construction (fock.gaussian_noise_channel_3mode: Gauss-Laguerre radial x
exact-harmonic angular displacement quadrature, cross-checked against
the pdf convolution); a width-scaled closed-form splat overlap
(forward3f.overlap_vs_thermal_lossy_cat3). Rank-R fidelity ceilings from
the target spectrum (max over rank-R sigma of F = sum of the top R
eigenvalues): R1 0.3786, R2 0.7501, R4 0.8181, R8 0.9521 (stable at
n_max=10). Protocol pre-declared: fixed blind lineup (exp11/exp14
extensions, nobody told sigma_add), init seeds {0,1,2} best-by-train
(an exp11-protocol upgrade justified by exp16's likelihood-blindness
finding), and the issue's falsification condition: best fixed-family F
short of its own rank ceiling by > 0.05 AND below the MLE fires
"in-family adaptation only".

Happened (committed log, single data seed 42):
    bbdagM R2K2        F = 0.6481   (86% of its rank-2 ceiling 0.7501)
    bbdagS K4          F = 0.3696   (rank-1 ceiling 0.3786: NEAR CEILING)
    purefock3          F = 0.3710   (ditto -- the generic control too)
    bbdagS lossy R2K4  F = 0.9234   eta fitted blind -> 0.3593
    mle3 (full rank)   F = 0.8976   (converged, 900 s budget)
    splat overlap 0.2861 vs perfect 0.2882 (99.3%; separate non-PSD axis)

SCORING CORRECTION (documented, superseded log kept): the first run
scored the channel-composed model by projecting its PRE-loss kets at
n_max=8 -- but the blind fit drove eta to 0.36, which scales pre-loss
amplitudes by 1/sqrt(eta) and overflowed the cutoff (projection trace
0.53, F 0.4256; out_run_prescoringfix.log). The declared fix
(rescore_and_addendum.py, out_followup.log) projects the pre-loss kets
at n_max=16, applies the truncated Kraus channel there, and cuts the
output back to the n_max=8 scoring block (trace 0.977). The main log
was regenerated with the corrected pipeline; the deterministic fits
reproduced exactly. A second correction in the same pass: the
channel-composed model is FULL RANK (a CPTP output), so the rank-2
ceiling never bounded it -- its ceiling is the truncated trace 0.9922.
A third correction (PR-61 review): the TARGET had the same disease --
the displacement channel scatters population in both directions, so
building it from an n_max=8 lossy cat loses the contributions that
scatter back into the scoring block from above.
fock.thermal_lossy_cat3_fock now builds at n_build=16 and crops to the
scoring block (regression pinned at the experiment amplitude:
n_build 16 vs 20 agree to 5e-6 while build-at-8 differs by > 1e-4),
and the run was regenerated once more; every value moved by ~1e-3
upward and no comparison flipped (superseded logs kept:
out_run_prescoringfix.log, out_run_pretargetfix.log).

RULING: the pre-declared falsification condition does NOT fire: the
channel-composed member of the fixed family, fitted blind, landed ABOVE
the converged full-rank MLE (0.9234 vs 0.8976) with ~110 real
parameters against the MLE's ~2.6e5. FAMILY-BOUNDARY NOTE (PR-61
review, accepted): the target lies outside every finite-rank ket
mixture -- the boundary the exp11 gate was worded against -- but the
winning model is loss_eta(B B^dagger), itself a FULL-RANK family with a
free eta, and whether the target lies outside (or merely near) THAT
family is not established. What this run records is therefore BLIND
HELD-OUT PERFORMANCE on one synthetic full-rank target, not proven
out-of-family generalization.
The texture is the informative part:
  1. The PURE-DETECTION ket mixtures track their rank ceilings almost
     exactly (rank-1 models sit 0.008-0.009 below theirs; rank-2
     coherent at 86%). Their limitation on a full-rank target is rank
     CAPACITY, not fit quality. [Exploratory addendum, outside the
     declared lineup and labeled as such: a blind bbdagM rank-8 reaches
     F 0.8759 = 92% of its 0.9521 ceiling -- capacity keeps being the
     binding constraint as R grows.]
  2. The mechanism behind the blind held-out performance is CHANNEL
     COMPOSITION:
     loss_eta(B B^dagger) is full rank with O(K) parameters, and the
     blind fit spent its eta knob (0.36, far from the physical 0.8) to
     buy the Gaussian width the ket mixture cannot express -- fitted
     eta as a model parameter, exactly the exp14/exp17 stance. The
     eta-(state) flat direction that made joint fitting UNSAFE for
     calibration in exp17 is here doing useful work: the flat family
     contains a good approximant of the target (which lies outside
     every finite-rank ket mixture; whether it also lies outside the
     channel-composed family is the unresolved non-inclusion question
     recorded below).

Learned: the gate as originally worded (a target no finite-rank ket
mixture contains) is met, and on it the pure-detection ket mixtures
behave exactly as their spectra predict -- rank capacity, not fit
quality, binds them. But the family had already outgrown that boundary:
its channel-composed member is full rank, and it delivered blind
held-out fidelity above the converged full-rank MLE. The honest record
is therefore NOT "out-of-family generalization achieved" (the target
may lie inside or near the channel-composed family; unresolved
[ADDENDUM 2026-07-18, exp20 / issue #63: resolved -- strictly OUTSIDE,
for every eta' and every finite rank; the claim moves up one notch in
the exp20 entry below]) but
"one recorded instance of blind held-out performance above a converged
full-rank MLE on a synthetic full-rank target". Single data seed, one
target class, fidelity in an n_max=8 truncation (conservative for the
model: its own post-channel trace is 0.977), MLE at the exp06-era
900 s budget. The README's wording moves accordingly -- one notch, no
further. Follow-ups recorded, not opened: a sigma_add / seed sweep;
a non-inclusion test (is N_sigma(E_eta(cat)) exactly representable as
loss_eta' of a rank-2 squeezed mixture?) that would settle the family
boundary; and a theory note on WHY channel composition approximates
Gaussian-noise states this well.

## 2026-07-16 (later) — Phase 1 on real video, round 1: precondition DNF (experiment 16 = 16_real_video, issue #48)

(Numbering note: "experiment 16" collided across the two parallel
lines; this one lives in experiments/16_real_video, distinct from the
quantum line's experiments/16_exp11_seeds below/above.)

Real data arrived from the owner: a 10 s hand-held walking video of a
(stationary — verified by strip-shift analysis) carousel. Extracted a
6 s / 24-frame window with provenance; held-out frames 4/10/16/22 and
all gates declared on the issue BEFORE implementation.

Built for it (all FD-pinned): the exp15 renderer extended with a global
background, the eta-style blur knob composed in CLOSED FORM
(si^2 = a^2 + sigma_b^2 with the mass-preserving amplitude factor
a^2/si^2 — a Gaussian blurred by a Gaussian is a Gaussian, exp13's
one-knob philosophy exported to graphics), and analytic camera-pose
gradients (translation dL/dc = -sum g_mu by symmetry; rotation
dL/dd = sum p x gp), driving a MonoGS-style incremental joint
pose+splat fit — no COLMAP exists in this environment.

Happened: the declared precondition (train PSNR >= 18 dB, defined as
PSNR of the pooled per-frame MSE) was NOT reached. Train-only tuning
trajectory (reproducible from committed code via tune.py, which — like
the hard stop now enforced in run.py before load_holdout() — never
loads the held-out frames): K=150 17.24 dB; K=250 + stepped lr 17.68;
+ pose polish and 1000 more iterations 17.82; + blur knob 17.85
(sigma_blur -> 0.60 px, +0.03 dB only). Recorded as DNF per the
declaration; Gate B/B2/ablation were NOT evaluated, and the held-out
frames were never touched — the protocol survives intact for round 2.

Working diagnosis (narrowed under the PR #59 review — a diagnosis, not
an established cause): per-frame PSNR is weakest on the mid-window
frames where a close horse crosses the scene, which is where an
additive no-occlusion renderer must pay — it cannot dim what is behind
an occluder, so foreground and background compete for the same pixels.
Occlusion is the LEADING candidate for the ceiling, but capacity was
not exhausted (K 150 -> 250 still bought +0.44 dB), so the claim stays
a working hypothesis that round 2's sorted alpha compositing will
test: if occlusion is the ceiling, compositing should clear the floor
at comparable K; if it does not, the diagnosis was wrong and that gets
recorded too.

Learned: the declared-precondition discipline did its job — it stopped
us from grading a certificate on a fit that fails for a plausibly
structural reason, which would have produced uninterpretable gate
numbers. The blur knob's honest non-result also matters: at 96x54 the
downsampling already dominates whatever motion blur the walk produced,
so the knob had nothing to absorb (sigma_blur ~ half a pixel). Round 2
= sorted alpha compositing in the renderer (the falsification path
named in the declaration), then the SAME untouched protocol.

## 2026-07-16 (night) — Phase 1 round 2: precondition met, Gate B falsified (experiment 16 = 16_real_video, issue #48)

Round 2 replaced the additive renderer with sorted alpha compositing
(composite.py: a_k = alpha_k A_k G_k, T_k = prod(1 - a_j), background
composited last; analytic gradients throughout incl.
dI/da_k = c_k T_k - S_k/(1-a_k); five pins in tests/test_composite.py
including the occlusion test and the small-alpha additive limit with
effective weights (c-b)alpha). Protocol and gates were re-declared on
the issue BEFORE running; identical continuation budgets for the
blur-on/off branches from a shared checkpoint per seed.

Result 1 — the round-1 diagnosis was CONFIRMED: at the same K=250 and
comparable budgets where the additive renderer asymptoted at 17.85 dB,
compositing cleared the declared floor on all three seeds (train PSNR
18.08 / 18.16 / 18.21 dB, blur-on primary). Occlusion was the round-1
ceiling. Precondition met; the held-out frames were opened for the
first time in this experiment.

Result 2 — Gate B FAILED, decisively and identically on every seed:
pooled held-out Spearman(sigma_pred, |residual|) = +0.029 / +0.026 /
+0.026 against the declared bar 0.3. Gate B2 also failed: the
row-norm control ||J|| beats the certificate on every seed (+0.256 /
+0.274 / +0.281 — itself below the bar), and the raw-amplitude control
is negative. The blur ablation missed its bar too (held-out MSE
ratios on/off = 1.007 / 1.008 / 0.996; sigma_blur 0.33-0.47 px — same
story as round 1, at 96x54 the downsampling dominates).

Per the pre-declared falsification: "the certificate does not survive
occlusion + model mismatch on real video — back to the renderer, not
the score." Recorded as such. The figure (heldout_certificate.png)
says why in one glance: the held-out residual concentrates on
high-frequency structure — poles, horse silhouettes, edges — that 250
isotropic Gaussians at 18 dB simply cannot represent, while sigma_pred
is a smooth field of splat-footprint blobs. At this fit quality the
residual is BIAS-dominated (model mismatch), and the delta-method
certificate quantifies VARIANCE (parameter uncertainty propagated
through H^{-1}). They are different quantities, and on a
bias-dominated residual a variance certificate has nothing to
correlate with. Phase 0 never saw this because the inverse-crime
synthetic had zero model mismatch — bias ~ 0, variance was the whole
residual. That is precisely the gap Phase 1 existed to expose, and it
did.

Learned: (1) occlusion diagnosis confirmed — compositing is worth
+0.35 dB at equal capacity and is now the baseline renderer; (2) the
Phase 0 certificate, as built, does NOT transfer to real video, and
the honest statement is sharp: a variance-only certificate cannot
rank residuals wherever bias dominates, i.e. anywhere short of a
near-perfect fit; (3) even the support-tracking control tops out at
+0.28 — the residual field here is mostly unexplained structure, not
anything any per-pixel score derived from this model can see. Any
round 3 must either close the bias gap (anisotropic splats / higher K
/ higher resolution until variance is a visible fraction of the
residual) or change what is being certified (a certificate that
models bias, not just variance) — and either way the gates get
re-declared on the issue before running. No post-hoc rescoping of
this round: it failed as declared.

## 2026-07-18 — The non-inclusion test: exp19's target is strictly outside the channel-composed family (experiment 20, issue #63)

Tried: the boundary question the PR-61 review left open -- is the
thermal-noise lossy cat N_sigma(E_eta(cat)) exactly representable as
loss_eta'(rho') with rho' a rank-2 (or ANY finite-rank) squeezed ket
mixture? Protocol pre-declared on the issue: an analytic Route A
(characteristic-function calculus) as primary, a numerical Route B
(direct best-approximation, fidelity axis) as corroboration, and a
three-branch decision rule fixing what each outcome does to exp19's
claim wording.

Route A (experiments/20_noninclusion/derivation.md + run.py): both
channels act on chi(lam) by argument rescale x Gaussian multiplication,
so E_eta' is injective and the pre-image at each eta' is UNIQUE:
chi'(mu) = chi_cat(k mu) e^{-c|mu|^2}, k^2 = eta/eta',
c = (eta' - eta + 2 sigma)/(2 eta'). The interval splits at
eta'_crit = eta - sigma = 0.70:
  * eta' > 0.70: the pre-image decomposes as a POSITIVE-variance
    Gaussian-displacement-noise composition (N_{sigma/eta'} after loss
    for eta' > eta; N_v after a quantum-limited amplifier for
    eta - sigma < eta' <= eta), and a displacement-orthogonality lemma
    makes any such output FULL RANK. Analytic exclusion of every
    finite rank at once.
  * eta' < 0.70 [STRENGTHENED after the PR-64 review, which correctly
    flagged that a grid scan cannot exclude a continuum and a finite
    cutoff cannot exclude "any finite rank"]: excluded ANALYTICALLY on
    the whole subinterval (Theorem 1): the pre-image's Husimi function
    is a rescaled s-ordered quasidistribution W_s of the CAT with
    s > -1 exactly when eta' < eta - sigma; if the pre-image were PSD
    then W_s >= 0, so its Gaussian smoothing Q_cat would be strictly
    positive -- but Q_cat has closed-form Bargmann zeros
    (cosh(conj(beta) alpha) = 0). Contradiction (the
    Lutkenhaus-Barnett depth-1 mechanism, self-contained).
  * eta' = 0.70 exactly (amplifier output, a valid state): infinite
    rank ANALYTICALLY (Theorem 2): the Husimi identity's Bargmann-
    kernel continuation carries a factor e^{t u conj(v)} with
    t = 1 - 1/G != 0, whose kernel rank is infinite; a rank-R state
    would cap it at R.
    The exclusion is therefore analytic on ALL of (0, 1]. The scan
    (run.py) is CORROBORATION and visualization: PSD violation at
    every regime-III grid point (min eigenvalue -4.9e-3 at eta' = 0.69
    growing to -4.4e+2 at eta' = 0.10, against a 1e-16 numerical
    floor, stable under node doubling and cutoff raise), PSD with a
    full-rank tail (3rd eigenvalue 5e-2) at the boundary, and the same
    structure in a 3-mode confirmation scan (per-term Kronecker
    factorization). Accuracy pinned by 8 tests
    (tests/test_noninclusion.py) against independent references in
    every regime: Lemma-1 remap onto gaussian_noise_channel_1mode,
    regime-I remap onto thermal_lossy_cat3_fock, and truncated-Kraus
    forward recovery of the target from the regime-III pre-image.

Route B (routeB.py): a first run silently deviated from the issue's
declared parameters (HS objective, cutoffs {12,16,20}, K {2,4}); the
PR-64 review flagged it and the run was REDONE per declaration --
direct FIDELITY objective, scoring cutoffs {8,10,12}, K {2,4,8}, 3
inits spanning the regime boundary (the superseded log is kept as
out_routeB_hsobj.log; its numbers agree at the same order). The ONE
declared deviation stands: the issue sketched the 3-MODE fit, whose FD
cost is out of reach; the run is the ONE-MODE problem, with exp19's
own blind 3-mode residual standing in as the 3-mode data point. A
labeled free-Fock-ket superset arm (eta' free) removes the
parametrization confound.
A round-2 review finding corrected the metric itself: the cropped
matrices are SUBNORMALIZED, and the plain Uhlmann formula let the
crop's trace deficit leak into the residual (identical crops scored
(Tr rho)^2 < 1 -- at n = 8 that penalty alone, 0.0051, exceeded the
then-reported best residual, so the objective was not even optimizing
agreement). All Route B scoring now uses the generalized fidelity for
subnormalized states, F = (Tr sqrt(sqrt(rho) sigma sqrt(rho)) +
sqrt((1 - Tr rho)(1 - Tr sigma)))^2, which returns exactly 1 for
identical crops; target traces are quoted per cutoff (superseded log
kept as out_routeB_plainuhlmann.log).
Result: best-found 1 - F = 0.0014 / 0.0020 / 0.0022 at cutoffs
8/10/12, K-saturated at K = 4-8, pre-loss tail mass monitored small
(no cutoff abuse); the superset arm lands at the same order (0.0063).
EPISTEMIC STATUS (per the review): local-optimization residuals are
UPPER bounds on the family's true distance -- heuristic corroboration
of the analytic exclusion, not a proven floor; the case-2 obstruction
rests on Route A's theorems alone. And the fitted eta' converges to
0.65-0.67 from every init: the optimizer walks to the PSD boundary of
Route A's regime map and parks where the pre-image's negativity is
smallest -- the two routes agree not just on the verdict but on the
geometry.

Ruling (decision rule case 2 fires): the target admits NO finite-rank
pre-image for ANY eta' in (0, 1] -- analytic on the whole interval
(Lemmas 1-2, Theorems 1-2), numerically corroborated on the grid --
so it is STRICTLY OUTSIDE the channel-composed family, and
exp19's record upgrades exactly one notch: "one recorded instance of
blind held-out performance on a genuinely OUT-OF-FAMILY full-rank
target, above a converged full-rank MLE" (single data seed, one target
class; universal claims stay barred). The honest counterweight is that
the boundary is THIN: the family approximates the target to
1 - F ~ 2e-3 (best-found, an upper bound on its true distance), so
exp19's blind gap (1 - F = 0.077) is dominated by fit
and data budget, not by the family boundary. Both faces go into the
READMEs.

Learned: the eta-(state) flat direction now has its full arc written
in one algebra (derivation.md section 4): the SAME curve of
(eta', state) pairs that makes joint calibration unidentifiable
(exp17) lets a blind fit slide toward Gaussian-noise surrogates
(exp19), and its endpoint -- the PSD boundary at eta' = eta - sigma --
is exactly where Route B's optimizer settles. Non-inclusion is proven,
yet the family tracks the excluded target to ~2e-3: "outside the
family" and "far from the family" are different claims, and only the
first is established. Follow-up recorded, not opened: the sigma_add /
seed sweep (unchanged from exp19); a possible representation-theory
note on WHICH mixed states loss_eta'(finite-rank) can reach exactly
(the scan machinery generalizes beyond this target).

## 2026-07-18 — Experiment 20 / issue #48 Round 3, Phase 0–2

(Numbering note: "experiment 20" collided across the two parallel
lines again; this line's lives in experiments/20_real_video_gpu,
distinct from the quantum line's experiments/20_noninclusion above.)

Owner/decisions: orange approved the GPU migration plan and Phase 2 execution; Codex session `019f6d8a` selected the version pins and executed the environment, data-boundary, and train-only COLMAP checks on branch `feat/issue-48-round3-gpu`.

Environment: RTX 5070 (sm_120, 12 GB), driver 576.88, Python 3.10.11, PyTorch 2.11.0+cu128, CUDA Toolkit 12.8.93, MSVC 19.44, and gsplat commit `77ab983f`. The Windows build exposed two upstream/toolchain edges: PyTorch decoded UTF-8 Japanese MSVC output as OEM CP932 during its ABI probe, and `Cameras.cuh` called host-only `std::isfinite` from device code on NVCC 12.8. The build uses PyTorch's ABI-check bypass after an independent compiler-version check and a recorded one-line `::isfinite` patch. Compiling every new backend was needlessly large; rebuilding only the standard RGB 3DGS feature set succeeded. A real RTX 5070 rasterization forward, backward, and Adam step were finite.

Data boundary: the supplied file is 20,130,116 bytes, H.264, 1920x1080@30 fps, 10.2667 s, SHA-256 `4483e898...f7b9e`. This differs from the old provenance text's 12 MB / HEVC metadata, but direct comparison against the committed 24 downscaled frames confirmed it is the same capture. Positions 4/10/16/22 live under `heldout-sealed`; only the other 20 filenames occur in the COLMAP database.

COLMAP finding: the planned 4.1.0 official CUDA asset is built with CUDA 13.2. Driver 576.88 cannot initialize it. No driver upgrade was attempted. Official release 4.0.4 is CUDA 12.9 with `all-major` architectures and ran GPU SIFT/matching successfully. Train-only sequential matching produced 69/69 verified pairs and 58,159 inliers. The mapper used its standard automatic initialization-constraint relaxation, then formed one model with 20/20 registered images, 4,567 points, mean track length 4.484, and mean reprojection error 0.695 px. Ordered camera steps are continuous (median 0.532, max 1.130 in arbitrary COLMAP units). Phase 2 passes without exposing held-out data to reconstruction.

Protocol-record correction: the local plan was approved before execution, but its promised Issue #48 publication was omitted before Phase 2. This is recorded as a process failure, not backdated. The unchanged protocol was published as a late hard lock before any gsplat training, PSNR tuning, held-out registration, or Gate B evaluation: issue comment `5008571914`.

## 2026-07-18 — Experiment 20 / issue #48 Round 3(a), final

The fixed full-resolution gsplat recipe cleared the 25 dB hard stop on all
three train-only fits: 26.961 / 27.071 / 27.021 dB with 551,891 / 557,226 /
545,356 splats. A 512-probe Rademacher estimator then built each train-only
per-splat 6x6 `[mean, log-scale]` Fisher in 6.7–7.5 minutes at <0.70 GiB peak
VRAM. Held-out remained sealed through this point.

After the hard stop, all four held-out poses were registered against a copy of
the frozen train reconstruction using GPU SIFT/matching and COLMAP
`image_registrator`. No BA, triangulation, or splat update ran. The 20 train
poses, camera intrinsics, and all 4,567 point XYZ coordinates remained fixed;
the 24-frame trajectory was continuous (step median 0.499, max 0.589).

Gate B PASSED on every fit seed: pooled full-resolution RGB-L2
Spearman(block-Fisher sigma, held-out residual) = +0.33433 / +0.33237 /
+0.33510 against the fixed 0.3 bar. Gate B2 FAILED on every seed. The H=I
`||J||` control scored +0.40247 / +0.39836 / +0.40093 and diagonal-Fisher
scored +0.37832 / +0.36601 / +0.37780; rendered amplitude was near zero and
slightly negative. Float32 outer-product accumulation produced tiny numerical
negative eigenvalues, so the pre-score amendment projected only negative 6x6
eigenvalues to zero before adding the unchanged damping. The relative
Frobenius correction was 0.62e-9–1.98e-9 and does not drive the result.

Honest reading: closing the fit-quality gap changed the round-2 result in an
important way — model-derived predictive sensitivity now correlates with real
held-out error above the preregistered bar. But the block covariance does not
beat simpler support/sensitivity controls, so this round establishes useful
error localization, not a block-Fisher-specific mechanism. Machine-readable
result: `experiments/20_real_video_gpu/phase5_gate_b_result.json`; certificate:
`experiments/20_real_video_gpu/heldout_certificate.png`; Issue result comment
`5011709434`.

## 2026-07-19 — Robustness sweep of the thermal gate: the blind verdict holds on all five configurations (experiment 21, issue #67)

Tried: the preprint prerequisite. exp19's headline (the channel-composed
model beating the converged full-rank MLE blind) was a single data
seed, and exp16 had demonstrated that this very fit family can be
init-fragile enough to flip verdicts on the pure-cat target, with the
train likelihood blind to the collapse. Pre-declared protocol (issue
#67): data seeds {42, 1, 2} at sigma_add = 0.1 plus sigma_add
{0.05, 0.2} at seed 42 (five configs, exp19 conventions), lossy R2K4
x init seeds {0,1,2} best-by-train-NLL vs mle3 (900 s), scored with
the generalized fidelity for subnormalized matrices (the PR-64
round-2 metric) through the exp19 wide-intermediate pipeline.
Pre-declared reading: any config with representative lossy F < F_mle
adds an exp16-style fragility note; all five holding permits "robust
across 3 data seeds and a 4x sigma_add range" (one target class,
exploratory -- unchanged).

Happened (committed log, results.json):

    config            lossy rep    F_mle    verdict     eta' (rep)
    seed 42, 0.10      0.9490     0.8980    holds        0.359
    seed  1, 0.10      0.9435     0.9023    holds        0.359
    seed  2, 0.10      0.9435     0.9032    holds        0.362
    seed 42, 0.05      0.9490     0.9362    holds        0.442
    seed 42, 0.20      0.8929     0.8147    holds        0.297

Verdict holds on 5/5. (The 42/0.10 row is exp19 reproduced under the
generalized-fidelity metric: the lossy row rises 0.9234 -> 0.9490 --
the plain-Uhlmann convention had been penalizing exactly the winning
row's trace deficit, as predicted in the PR-64 discussion -- while
the trace-1 MLE row barely moves, 0.8976 -> 0.8980.)

Texture worth recording honestly:
  1. NO exp16-style basin collapse anywhere: 15 fits, per-config F
     spreads 0.024-0.041 (exp16's collapse was dF ~ 0.45). The
     thermal target appears to regularize the fit landscape relative
     to the pure lossy cat.
  2. The NLL-blindness itself is still visible in mild form: on the
     sigma_add = 0.20 config, best-by-train-NLL selects the WORST of
     the three inits (F 0.8929 vs 0.9243/0.9253 available; dNLL
     0.0026 vs dF 0.032). The declared selection rule was honored and
     the verdict is unaffected (margin over MLE 0.078), but the
     selection hazard exp16 documented has not disappeared -- it is
     just too small here to bite.
  3. eta' tracks sigma_add monotonically (0.442 / ~0.36 / 0.297 for
     sigma_add 0.05 / 0.10 / 0.20): the flat-direction mechanism the
     exp20 derivation formalized (spend eta' to buy Gaussian width),
     behaving as predicted across the noise range.
  4. MLE convergence within the 900 s budget is config-dependent
     (converged on 2 of 5); the sweep inherits exp19's budget
     convention unchanged.

Learned: the pre-declared reading's favorable branch fires -- the
exp19 blind verdict is robust across 3 data seeds and a 4x sigma_add
range on this target class, and the wording in both READMEs moves
accordingly (still one target class, still exploratory, still no
universal claims). The preprint (issue #69) can now cite exp21 for
robustness and exp16 for the selection hazard that exp21 shows in
mild, non-verdict-affecting form.

## 2026-07-19 — Experiment 20 / issue #48 Round 4, fresh replication

Owner/decisions: orange approved and hard-locked the protocol in Issue #48
comment 5013626313; Codex session 019f6d8a implemented and executed the GPU
evaluation without refitting the three frozen Round 3 checkpoints.

Four previously unused frames from the end of the same capture (source indices
216/244/272/300, 7.20–10.00 s) were losslessly extracted and sealed. COLMAP
registered all 4/4 against a copy of the frozen train model. Existing train
poses, camera intrinsics, and point XYZ remained fixed; no BA, triangulation, or
splat update ran. The new interval is temporal extrapolation within one
registerable trajectory, not an independent-scene replication.

Gate B replicated on all fit seeds:
Spearman(block-Fisher sigma, fresh RGB-L2 residual) =
0.36905 / 0.33663 / 0.37550 against the fixed 0.3 bar. Unlike Round 3,
block Fisher strictly beat amplitude (-0.155 / -0.182 / -0.116), H=I J-norm
(0.196 / 0.215 / 0.245), and diagonal Fisher
(0.319 / 0.295 / 0.345) on every seed.

Gate B2 nevertheless failed on every seed because the shared three-fit-seed
ensemble sigma scored 0.57534 / 0.56690 / 0.54286, above block Fisher in all
three comparisons. The hard-locked reading therefore applies: at this
operating point the H^-1 certificate does not beat brute-force repetition.
This is a result about the declared 3-seed ensemble, not all possible ensemble
sizes or independent scenes.

The descriptive damping sweep was monotone on all seeds:
1e-4: 0.299 / 0.285 / 0.317; primary 1e-6:
0.369 / 0.337 / 0.376; 1e-8: 0.422 / 0.383 / 0.434.
It shows material regularization sensitivity but does not alter the primary
verdict. Fresh pooled RGB MSE was 0.03186 / 0.03315 / 0.02852, much higher
than Round 3's opened views, consistent with the intended extrapolation stress.
Machine-readable result: experiments/20_real_video_gpu/phase6_round4_result.json;
certificate: experiments/20_real_video_gpu/round4_certificate.png.

## 2026-07-19 — Experiment 20 / issue #48 Round 5, public-scene DNF

Owner/decisions: orange approved hard lock comment 5014598454. Codex session
019f6d8a executed the GPU-side pipeline. Official Tanks and Temples Truck and
Train image-set archives were pinned by URL, byte length, and SHA-256; their
251/301 frames yielded declared strides 10/12 and native 1920x1080 splits.
CC BY 4.0 attribution (the license page's Copyright section) and the same
page's conflicting License Grant restrictions (non-commercial research only,
no third-party redistribution) are both recorded without being resolved.

The prerequisite failed before fitting. The video-oriented sequential matcher
registered Truck 11/20 and Train 3/20. Before any fit or held-out access,
operational correction comment 5014845453 fixed CUDA exhaustive matching for
the globally spaced image set while preserving both failures. It improved
Truck to 15/20 but Train produced 2/20; neither met the explicit 20/20
completion condition.

Both scenes are DNF. No gsplat, pooled-train-PSNR decision, Fisher, held-out
registration, Gate B/B2, or ensemble decomposition ran. This result does not
replicate or reject Gate B; the locked 24-frame global stride failed to supply
the complete SfM prerequisite. Further rescue tuning was barred as post-hoc
protocol exploration. Machine-readable result:
experiments/20_real_video_gpu/phase7_round5_result.json; certificate:
experiments/20_real_video_gpu/round5_dnf_certificate.png.

## 2026-07-20 — Experiment 20 / issue #48 Round 6, SfM pass then fit DNF

Owner/decisions: orange approved hard lock comment 5017827938 and gave the GPU
GO after execution handoff 5018136279. Codex session 019f6d8a ran the fixed
contiguous central windows: Truck source 113–136 and Train 138–161, with
positions 4/10/16/22 sealed.

CUDA exhaustive COLMAP registered 20/20 train images for both scenes on the
first attempt (Truck 10,537 points / 0.648 px mean reprojection error; Train
8,934 / 0.719 px). No parameter rescue or window movement occurred. This
repairs the exact prerequisite that stopped Round 5 and supports its diagnosis:
the global-stride selection, not GPU availability, broke SfM connectivity.

The next hard stop failed. With the unchanged 4000-step gsplat recipe, seed 0
ended at pooled train PSNR 24.305 dB for Truck and 22.180 dB for Train, both
below the declared 25 dB floor. Truck descriptively peaked at 24.969 dB at step
2999, but selecting that checkpoint would change the fixed decision point after
seeing the trajectory, so step 3999 remains authoritative.

One failed seed is sufficient for scene DNF. Seeds 1/2, production Fisher,
held-out registration, Gate B/B2, and ensemble decomposition were not run;
held-out images were not accessed by COLMAP, fit, or evaluation. Round 6 thus
neither replicates nor rejects Gate B. Machine-readable result:
experiments/20_real_video_gpu/phase8_round6_result.json; certificate:
experiments/20_real_video_gpu/round6_dnf_certificate.png.

## 2026-07-20 — Experiment 22 / issue #89, signed-splat expression demos

Owner/decisions: orange approved the demo line and later fixed the acceptance
contract to a public, pretrained, visually beautiful, high-detail 3DGS with no
additional training. Codex session 019f6d8a selected the public material,
implemented the GPU path, rendered the effects, and performed visual QA. This
is expression work, not a confirmatory gate or a continuation of issue #48's
scientific claim.

The final input is steam studio / 3D SCAN STUDIO iris's CC0 cactus model:
Nikon Z7II, 8256x5504, 427 photos, Postshot 25k steps, 1,935,120 splats, and
SH degree 3. The 456,689,798-byte PLY hash is
`0d747af95e3e9d55837a1e3aa6a4ed7dc6222866e0ba8cda928e211f7e8888c1`.
No GPU training ran.

The production renderer uses gsplat CUDA with the trained position, opacity,
anisotropic scale, WXYZ quaternion, and SH degree-3 coefficients. It renders
three time-varying signed operations: a moving 3D eraser sphere, a dark beam
filled with negative Gaussians, and a translated negative copy that annihilates
the cactus at contact. The CPU fixed-footprint renderer remains a fallback but
is not used for the high-fidelity result.

Three CC0-derived videos are committed at 960x960, 12 fps, 96 frames, and
8 seconds. They passed ffprobe, 1/4/7-second visual QA, and an additional final
frame check for complete annihilation while retaining the pot. Six targeted
tests passed. Exact recipes and hashes are in
`experiments/22_signed_splat_demo/demo_result.json`.

This supersedes the earlier garden/provenance conclusion. The ambiguous
cakewalk garden asset is not used, and the contract is satisfied by continuing
the public-data search rather than switching to a self-captured MOV.
