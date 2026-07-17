# wigner-splat

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21387212.svg)](https://doi.org/10.5281/zenodo.21387212)

**Constructively physical Gaussian representations for continuous-variable quantum-state tomography.**

`wigner-splat` is a reproducible research prototype for fitting homodyne
measurements without making a truncated Fock density matrix the primary model.
It began from a Gaussian-splatting view of the Radon projections of a Wigner
function, and now also contains constructively physical $\rho = BB^\dagger$
models with closed-form homodyne likelihoods and analytic gradients.

> **Research status.** This is preliminary research software, not a claim of a
> universally superior tomography method. The repository preserves negative
> results, scope limits, and the exact experiments behind every headline below.
> The complete chronological research narrative is available in
> [Japanese](README.ja.md).

## What is being explored

Homodyne tomography observes one-dimensional quadrature marginals at local
oscillator phases. The project investigates two related but distinct
representations:

1. **Signed anisotropic Gaussian mixtures ("splats").** A closed-form,
   differentiable Radon forward model fits Wigner-function marginals. Signed
   weights can express Wigner negativity, and gradient-driven birth, splitting,
   and pruning adapt the mixture.
2. **Physical Gaussian-ket mixtures.** Finite mixtures of displaced and squeezed
   product kets are fitted by per-sample likelihood. Their $BB^\dagger$
   construction guarantees a positive-semidefinite density operator; loss and
   finite-rank extensions model mixed states.

The 3D Gaussian-splatting analogy is useful because a camera view corresponds to
a homodyne phase, splatting corresponds to a phase-space Gaussian primitive, and
rendering corresponds to a Radon projection. It is an origin and an experimental
representation—not a claim that computer-vision 3DGS itself solves quantum
tomography.

## Evidence at a glance

### Synthetic multimode tests

The signed-splat track was tested against iterative $R\rho R$ maximum
likelihood estimation (MLE) on simulated cat states at matched shot budgets.

| Setting | Observed result | Scope limit |
| --- | --- | --- |
| 1 mode | Splat has slightly higher score, but MLE is about 2x faster. | No computational advantage at this scale. |
| 2 modes | Fidelity is statistically indistinguishable across 20 paired seeds; splat uses about 1/7.4 of the measured compute. | Requires full cross-mode covariance; separable splats fail. |
| 3 modes | A signed-splat run reached a higher Wigner-overlap score in about 15 s while the 512-dimensional MLE run did not converge within 900 s. | This score is not state fidelity when the reconstruction is non-PSD. It is not a physical-tomography win. |

The physical $BB^\dagger$ track resolves the PSD issue by construction. Its
early synthetic high-fidelity results were **in-family existence results**, and
a fair Fock-ket comparison showed that its main demonstrated advantage is
compactness and speed, not a general fidelity advantage. A held-out full-rank
gate (experiment 19) later recorded **blind held-out performance above a
converged full-rank MLE**: on a thermal-noise lossy cat that no finite-rank
ket mixture contains, the loss-channel-composed rank-2 model reached fidelity
0.923 against the MLE's 0.898 with roughly 110 real parameters — while the
pure-detection ket mixtures landed almost exactly on their rank-capacity
ceilings. A non-inclusion analysis (experiment 20) then settled the family
boundary: for **no** efficiency does the target admit a finite-rank pre-image
(analytic for most of the parameter range, a validated numerical scan for the
rest), so the target is **strictly outside the winning family** and the exp19
record is one instance of blind performance on a genuinely out-of-family
target. The boundary is thin, however: a direct best-approximation study
found the family approaches the target to about 1 − F ≈ 5 × 10⁻³ (one-mode
floor, stable under cutoff growth), so exp19's larger blind gap is a fit- and
data-budget effect, not the family boundary. Single seed and a single target
class; universal claims remain unwarranted. See the
[research log](docs/research-log.md) and [prior-art survey](docs/prior-art-survey.md)
for the evidence and comparisons.

### Public homodyne data: GKP states

On the public propagating-light GKP homodyne dataset from Konno *et al.*
(Science 2024; [Dryad DOI](https://doi.org/10.5061/dryad.t76hdr86j)), a pure
physical model initially lost clearly to full-rank MLE. Adding a physical loss
channel and rank-two squeezed-ket model improved held-out likelihood and, in a
matched-degree-of-freedom control, outperformed a rank-one model of comparable
capacity.

A rank-saturation study (experiment 18) then walked the remaining gap down:
the rank curve saturates at R = 4–5, warm starts rule out under-optimization,
and matched-degree-of-freedom controls at two frontier points attribute each
gain to rank rather than parameter count. At rank 4 (92 real parameters) the
physical model **ties the empirical MLE frontier at confidence-interval
resolution on both reshuffles** (conditional 95% CIs [−0.00002, +0.00020] and
[−0.00017, +0.00003] nats per held-out sample against the test-selected
frontier best at 255 parameters). Earlier rounds' recorded losses
(experiments 12–14) stand in the log. These analyses remain exploratory—the
splits reuse the same observations, the MLE opponent is test-selected, and a
tie at CI resolution is not preregistered confirmation.

<p align="center">
  <img src="experiments/14_gkp_rank/gkp_rank_marginals.png" width="78%" alt="Measured GKP homodyne marginals and reconstructions" />
</p>

<p align="center">
  <img src="experiments/18_gkp_saturation/gkp_saturation_frontier.png" width="78%" alt="Held-out NLL versus degrees of freedom for physical models and MLE, ranks 1 through 5" />
</p>

The figures and their full protocols are in
[`experiments/14_gkp_rank`](experiments/14_gkp_rank) /
[`experiments/18_gkp_saturation`](experiments/18_gkp_saturation) and the dated
research-log entries
([exp14](docs/research-log.md#2026-07-14--rank-freedom-on-real-data-exploratory-rank-hypothesis-test-experiment-14-issue-40),
[exp18](docs/research-log.md#2026-07-16--rank-saturation-on-the-gkp-data-the-frontier-gap-closes-experiment-18-issue-40)).

## Reproduce

The repository is intentionally lightweight. For the core synthetic experiment:

```bash
pip install numpy matplotlib pytest
python -m pytest tests/ -q
python experiments/01_cat_state/run.py
```

Experiment directories contain their own scripts, committed output logs, and
where applicable the generated figures. The public GKP dataset is included with
its source README and attribution under `experiments/12_gkp_data/data/`.

## Repository map

```text
wigner_splat/   forward models, fitters, physical Gaussian-ket models, and MLE baselines
experiments/    reproducible synthetic and public-data experiments
tests/          numerical and physical-consistency tests
docs/           research log, surveys, and reproducibility notes
```

## Prior work and novelty boundary

This project builds on, rather than replaces, several lines of work:

- 3DGS-style differentiable Radon tomography:
  [R2-Gaussian](https://arxiv.org/abs/2405.20693) and
  [X²-Gaussian](https://arxiv.org/abs/2503.21779)
- Gaussian representations of Wigner negativity:
  [Kenfack *et al.* (2004)](https://arxiv.org/abs/physics/0304029) and
  [Tosca *et al.* (2025)](https://arxiv.org/abs/2507.14076)
- Homodyne tomography and physical optimization:
  [Strandberg (2022)](https://arxiv.org/abs/2202.11584) and
  [Gaikwad *et al.* (2025)](https://arxiv.org/html/2503.04526v1)

The narrow signed-splat research question is whether those two first lines can
be combined as an inverse problem on measured homodyne data. The physical
Gaussian-ket track has a different prior-art boundary and should not inherit that
novelty claim. The [prior-art survey](docs/prior-art-survey.md) records both
boundaries and their remaining risks.

## Citation and license

If this software or its research record is useful, please cite it using
[`CITATION.cff`](CITATION.cff). The exact archived `v0.1.0` release is
[DOI: 10.5281/zenodo.21387212](https://doi.org/10.5281/zenodo.21387212).
The [concept DOI](https://doi.org/10.5281/zenodo.21387211) always resolves to
the latest archived version and is not the citation for this fixed release.
The code is released under the [MIT License](LICENSE).

Small support for compute and agent time will be welcome once a sponsorship link
is configured; citations and careful technical feedback are already valuable.
