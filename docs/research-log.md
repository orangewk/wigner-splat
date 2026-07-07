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
