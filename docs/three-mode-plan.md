# Three-mode plan — the decisive scaling point (issue #7)

Two modes flipped the roles (exp 04: fidelity tie, splat 6-11x faster). Three
modes is where Fock MLE becomes impractical (n_max^3 dims) while full-covariance
splats stay O(K) at 28 params/splat. If MLE simply cannot finish, THAT is the
result — measure it honestly rather than crippling either side.

## Target state

|a,a,a> + parity |-a,-a,-a>, real a (default 1.5), parity +1. Fringe lifts to
cos(2 sqrt2 a (p1+p2+p3)) (same derivation pattern as states2; cross term is a
product of per-mode central Gaussians x phase). Norm: 2(1 + parity e^{-6 a^2}).

## Data format

    data = [((th1, th2, th3), samples (shots, 3))]

Angle triples: 3x3x3 grid over [0, pi)^3 (27 triples). Shots: 2000/triple
(54k total). Shared binning data3.histogram_targets3(bins=24) -> centers (24,),
targets [((th), hist (24,24,24))]. density=True. Keep only nonzero cells on the
MLE side (<= ~1500/triple).

## Budgets and honesty rules

- Splat (forward3f/fit3f): full 6x6 Cholesky, generalize forward2f/fit2f. The
  ridge direction for the matched-stripe stage must be DETECTED from data
  correlations (generic candidate axes incl. (p1+p2+p3)/sqrt3), not hardcoded.
  Loss pass memory: 27 triples x 24^3 cells x K — chunk over triples.
- MLE (mle3): product Fock, n_max chosen by memory/ceiling tradeoff (compute
  cat3_truncation_fidelity exactly; n_max=8 -> 512 dims, ceiling likely ~0.99+;
  document). V matrix (M x n_max^3) complex; M ~ 40k rows -> ~0.3 GB at 512 dims
  (acceptable), per-iteration cost O(M N^2) — measure it FIRST, then either run
  to convergence or to a 30-minute wall budget, whichever first; report fidelity
  reached, iterations, and time-per-iteration with an honest extrapolation to
  convergence. A DNF (did not finish) verdict requires the measured per-iter
  cost and the convergence-trajectory extrapolation, not just a timeout.
- Fidelity: Fock side <psi|rho|psi> with cat3_fock (kron of 1D pieces); splat
  side closed-form Gaussian overlap (the forward2f overlap formula is
  dimension-agnostic — lift it, validate vs brute force on a coarse 6D grid and
  vs |<000|cat3>|^2 exactly).
- Same-data rule: both consume histogram_targets3 output.
- Quote seed ranges (>= 3 data seeds for the splat side; MLE per-seed only if
  budget allows — document).

## Experiment 06

experiments/06_three_mode/run.py: per-seed table (F, wall, Wmin on the
(p1,p2) plane at p3=0, x=0 — fringe visible there as cos(k(p1+p2))), verdict
block (splat must win BOTH; falsification = lose BOTH), figure: true vs splat
vs MLE (if it produced anything) Wigner slices + K_axis... no — reuse the
exp04 figure pattern. Include the MLE cost story (dims 144 -> 512/1728,
time/iter, total) as a printed scaling table alongside exp03/exp04 numbers.
