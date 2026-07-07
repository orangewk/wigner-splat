# Two-mode extension plan (the decisive scaling test)

The falsification verdict at one mode (experiment 03, recorded in README):
splat wins fidelity, MLE wins speed. The surviving claim is SCALING — Fock
MLE dimension grows as n_max^modes while splat parameters stay O(K). Two
modes is the first point where that can be tested. If splat loses both
fidelity and speed here too, the README commits to abandoning the approach.

## Target state

Two-mode entangled cat |a,a> + parity |-a,-a| (real a, default a=1.5,
parity=+1). Conventions identical to states.py: vacuum marginal N(0, 1/2),
mode j measured at LO phase theta_j maps its alpha -> alpha e^{-i theta_j}.
Wavefunction: psi(x1,x2) = [psi_b(x1) psi_b(x2) + parity psi_{-b1}(x1)
psi_{-b2}(x2)] / sqrt(norm), b_j = a e^{-i theta_j}, built from
states.coherent_wavefunction. Norm: 2 (1 + parity e^{-4 a^2}).

## Data format (shared by everything)

    data = [((theta1, theta2), samples)]   # samples: float array (shots, 2)

Angle pairs: grid over [0, pi)^2, e.g. 4x4. Joint histograms: shared square
edges per axis (bins x bins), density=True, like fit.histogram_targets.

## Representation decision: separable splats

Each splat k is a PRODUCT of two 2D phase-space Gaussians (block-diagonal
4x4 covariance): params w (1), mu (4), s (2 per mode), phi (1 per mode) =
11 per splat. Rationale: the cat's cross term factorizes,

    e^{-sum} cos(k(p1+p2)) = e^{..}[cos(k p1)cos(k p2) - sin(k p1)sin(k p2)]

i.e. products of single-mode fringes, and each 1D fringe is approximable by
signed 1D Gaussians — so a MIXTURE of separable splats spans the needed
structure (mixture covariance is not component covariance). This reuses the
whole 1D machinery: the Radon projection onto (x_theta1, x_theta2) is a
product of two 1D Gaussians, so loss gradients, densification split, and
signed birth all lift from fit.py with per-mode bookkeeping. Restriction is
recorded: entangled Gaussian correlations inside ONE splat are not
representable; if the fit plateaus, that is the first suspect.

## Modules and owners

- wigner_splat/states2.py — TwoModeCat: wigner(x1,p1,x2,p2), joint
  homodyne_pdf(x1,x2,th1,th2), sample_homodyne(angle_pairs, shots, rng)
  (inverse-CDF per pair on a 2D grid is fine). MUST be validated against
  the product-Fock construction using the existing (1e-12-validated)
  fock.py: c_{mn} = kron of 1D cat coefficient pieces, joint pdf =
  |<x1,th1|<x2,th2| psi>|^2 via quadrature_vectors kron.
- wigner_splat/forward2.py + fit2.py — SplatMixture2 (radon2 = product of
  per-mode projected 1D Gaussians on the (x1,x2) bin grid), loss (2D
  histogram L2 + negativity + sum-to-1), analytic loss_and_grad
  (VECTORIZED over angle pairs from the start), adapt/birth lifted from
  fit.py (birth field on a coarse 4D grid is too big: use the pairwise
  marginal residual field or a random candidate set — owner decides,
  documents, and tests that a born splat decreases the loss).
- wigner_splat/mle2.py — product-Fock R rho R: quadrature vectors are
  krons of 1D vectors, keep only nonzero bins, same hardened stop
  condition as mle.py (likelihood decrease raises).
- wigner_splat/fidelity2.py — same-definition fidelity for both methods:
  Fock side <psi|rho|psi>; splat side (2 pi)^2 * integral W_fit W_true
  d^4z, closed form via per-mode 2D Gaussian overlaps (cat cross terms are
  Gaussians with complex means — take real parts at the end). Cross-check
  the two estimators against each other on states known in both forms.
- experiments/04_two_mode/run.py — the verdict table: fidelity AND
  wall-clock for splat vs MLE at >= 2 shot budgets, plus figures: 2D
  slices of the 4D Wigner ((p1,p2) at x1=x2=0 where the fringe lives, and
  (x1,p1) at x2=p2=0), true vs splat vs MLE side by side.

## Fairness rules (same spirit as exp 03)

- Both methods consume identical binned histograms.
- Splat timing includes the full fit; MLE timing includes projector build
  + iterations. Both single-threaded numpy in the same process.
- n_max chosen so the true cat is representable (a=1.5: mean n per mode
  2.25; n_max=12-14 per mode; document the truncation fidelity of the
  TRUE state as the MLE ceiling).
- Quote seed ranges, not single runs, for the splat side (issue #4).
