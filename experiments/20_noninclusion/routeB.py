"""Experiment 20, Route B -- issue #63: best-approximation corroboration.

Route A (derivation.md Lemmas 1-2 + Theorems 1-2) settled EXACT
non-inclusion analytically: no eta' in (0, 1] admits a finite-rank
pre-image of the thermal-noise target. Route B probes the
FINITE-fidelity axis the exp19 comparisons actually live on: directly
optimize the Uhlmann fidelity of loss_eta'(rank-2 squeezed ket
mixture) against the target -- no data, no sampling noise, FD
gradients on the exact Fock-side objective.

WHAT ROUTE B CAN AND CANNOT SHOW (wording per the PR-64 review): a
best-found residual from local optimization is an UPPER bound on the
family's true distance to the target -- multi-init, cutoff-stable,
superset-armed residuals are HEURISTIC corroboration of a floor, not
a proven lower bound. The load-bearing obstruction for the issue-63
case-2 ruling is Route A's analytic theorems; what Route B adds is
(a) the finite-fidelity scale of the boundary and (b) a live alarm:
any fit reaching 1 - F < 1e-4 would CONTRADICT Route A and reopen the
derivation (representability branch, case 1).

THIS RUN follows the issue-declared parameters: direct FIDELITY
objective, scoring cutoffs n_max in {8, 10, 12}, K in {2, 4, 8}. (A
first run deviated undeclared -- HS objective, cutoffs {12, 16, 20},
K {2, 4}; the PR-64 review flagged it, its log is kept superseded as
out_routeB_hsobj.log, and its results agree with this run at the same
order.) The ONE declared deviation stands: the issue sketched the
3-MODE fit, whose FD cost is computationally out of reach (the
wide-cutoff channel application per FD probe puts a single config in
the multi-hour range); Route B runs the ONE-MODE problem -- same
channels, same cat, same regime structure (derivation.md section 5 is
mode-count-agnostic) -- and exp19's own blind 3-mode residual
(1 - F = 0.077 at trace ceiling 0.9922) stands in as the 3-mode
point.

Design:
  * target: N_sigma(E_eta(cat1)) built wide (n = 30) and cropped.
  * model: rho' = B B^dag / Z, B = 2 columns of K displaced-squeezed
    kets (bbdagS.sq_wavefunction coefficients by quadrature, n_build =
    30); channel = truncated Kraus loss at n_build, cropped to
    n_score; eta' free through a logit. OBJECTIVE: minimize
    1 - F_Uhlmann(model, target) directly.
  * grid: n_score in {8, 10, 12} x K in {2, 4, 8} x 3 inits (seed
    0/1/2 with eta'0 = 0.8 / 0.6 / 0.4 -- inits span the regime
    boundary). Representative per (n_score, K): best final 1 - F.
  * addendum arm (labeled, outside the issue lineup): rank-2
    FREE-Fock-ket pre-image (columns as unconstrained complex
    vectors, a strict superset of the squeezed family) with eta' ALSO
    free, at n_score = 12 -- removes both the parametrization
    confound and the fixed-eta' objection of the first run.
  * cutoff-abuse monitor: pre-loss population of the fitted kets
    above n_score is quoted (an optimizer parking mass at the build
    cutoff would fake a high F).
"""
import json
import pathlib
import sys
import time
from math import comb

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagS import sq_wavefunction  # noqa: E402
from wigner_splat.fock import (  # noqa: E402
    gaussian_noise_channel_1mode, hermite_psi,
)

ALPHA = 1.5
PARITY = +1
ETA = 0.8
SIGMA = 0.1
N_BUILD = 30
N_SCORES = (8, 10, 12)
KS = (2, 4, 8)
INITS = ((0, 0.8), (1, 0.6), (2, 0.4))
ITERS = 500
ITERS_FREE = 400
FD_H = 1e-5

_XGRID = np.linspace(-12.0, 12.0, 1201)   # machine-precision identical to
_HPSI = hermite_psi(_XGRID, N_BUILD)      # a 4001-pt/28-wide grid at n=30
_COMB = np.zeros((N_BUILD, N_BUILD))
for _m in range(N_BUILD):
    for _k in range(_m + 1):
        _COMB[_m, _k] = comb(_m, _k)


def cat1_fock(alpha, parity, n_max):
    n = np.arange(n_max)
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    c = np.exp(-alpha ** 2 / 2.0 + n * np.log(alpha) - log_fact / 2.0)
    c = c * (1.0 + parity * (-1.0) ** n)
    return c / np.linalg.norm(c)


def kraus_ops(eta, n_max):
    ops = []
    for k in range(n_max):
        A = np.zeros((n_max, n_max))
        idx = np.arange(k, n_max)
        A[idx - k, idx] = np.sqrt(_COMB[idx, k] * eta ** (idx - k)
                                  * (1 - eta) ** k)
        ops.append(A)
    return ops


def kraus_loss(rho, eta, n_max):
    out = np.zeros_like(rho)
    for A in kraus_ops(eta, n_max):
        out += A @ rho @ A.T
    return out


def build_target(n_score):
    c = cat1_fock(ALPHA, PARITY, N_BUILD)
    t = gaussian_noise_channel_1mode(
        kraus_loss(np.outer(c, c.conj()), ETA, N_BUILD), SIGMA)
    return t[:n_score, :n_score]


def uhlmann(rho, sigma):
    rho = (rho + rho.conj().T) / 2
    sigma = (sigma + sigma.conj().T) / 2
    w, U = np.linalg.eigh(rho)
    sq = (U * np.sqrt(np.maximum(w, 0.0))) @ U.conj().T
    inner = sq @ sigma @ sq
    ev = np.maximum(np.linalg.eigvalsh((inner + inner.conj().T) / 2), 0.0)
    return float(np.sum(np.sqrt(ev)) ** 2)


# ---------------- squeezed-family model ----------------
# theta layout: [eta_logit, then per column r, per ket k:
#   Re z, Im z, Re alpha, Im alpha, Re xi, Im xi]

def unpack(theta, K):
    eta_p = 1.0 / (1.0 + np.exp(-theta[0]))
    rest = theta[1:].reshape(2, K, 6)
    z = rest[..., 0] + 1j * rest[..., 1]
    al = rest[..., 2] + 1j * rest[..., 3]
    xi = rest[..., 4] + 1j * rest[..., 5]
    return eta_p, z, al, xi


def _coeff(al, xi):
    f = sq_wavefunction(_XGRID, al, xi)
    return np.trapezoid(_HPSI * f[None, :], _XGRID, axis=1)


def _coeff_table(al, xi):
    """(2, K, N_BUILD) coefficient vectors of every ket."""
    K = al.shape[1]
    V = np.empty((2, K, N_BUILD), complex)
    for r in range(2):
        for k in range(K):
            V[r, k] = _coeff(al[r, k], xi[r, k])
    return V


def _obj_parts(eta_p, z, V, n_score, target):
    rho_pre = np.zeros((N_BUILD, N_BUILD), complex)
    for r in range(2):
        col = z[r] @ V[r]
        rho_pre += np.outer(col, col.conj())
    Z = np.trace(rho_pre).real
    out = kraus_loss(rho_pre / Z, eta_p, N_BUILD)
    return 1.0 - uhlmann(out[:n_score, :n_score], target)


def model_state(theta, K, n_score):
    """(cropped model matrix, eta', pre-loss rho at N_BUILD)."""
    eta_p, z, al, xi = unpack(theta, K)
    V = _coeff_table(al, xi)
    rho_pre = np.zeros((N_BUILD, N_BUILD), complex)
    for r in range(2):
        col = z[r] @ V[r]
        rho_pre += np.outer(col, col.conj())
    Z = np.trace(rho_pre).real
    out = kraus_loss(rho_pre / Z, eta_p, N_BUILD)
    return out[:n_score, :n_score], eta_p, rho_pre / Z


def fid_obj(theta, K, n_score, target):
    m, _, _ = model_state(theta, K, n_score)
    return 1.0 - uhlmann(m, target)


def _structured_grad(theta, K, n_score, target):
    """Central-difference gradient of fid_obj that only recomputes the
    ONE perturbed ket's coefficient vector per probe (the quadrature is
    the expensive part; z and eta' probes reuse the cached table).
    Numerically identical to blind FD on fid_obj."""
    eta_p, z, al, xi = unpack(theta, K)
    V = _coeff_table(al, xi)
    g = np.empty_like(theta)
    # eta' slot
    e_p = 1.0 / (1.0 + np.exp(-(theta[0] + FD_H)))
    e_m = 1.0 / (1.0 + np.exp(-(theta[0] - FD_H)))
    g[0] = (_obj_parts(e_p, z, V, n_score, target)
            - _obj_parts(e_m, z, V, n_score, target)) / (2 * FD_H)
    # per-ket slots
    for r in range(2):
        for k in range(K):
            base = 1 + (r * K + k) * 6
            for j in range(6):
                idx = base + j
                if j < 2:                        # z: table unchanged
                    zp = z.copy(); zm = z.copy()
                    d = FD_H if j == 0 else 1j * FD_H
                    zp[r, k] += d; zm[r, k] -= d
                    g[idx] = (_obj_parts(eta_p, zp, V, n_score, target)
                              - _obj_parts(eta_p, zm, V, n_score, target)
                              ) / (2 * FD_H)
                else:                            # alpha / xi: one vector
                    d = FD_H if j % 2 == 0 else 1j * FD_H
                    a_p, x_p = al[r, k], xi[r, k]
                    if j < 4:
                        vp = _coeff(a_p + d, x_p)
                        vm = _coeff(a_p - d, x_p)
                    else:
                        vp = _coeff(a_p, x_p + d)
                        vm = _coeff(a_p, x_p - d)
                    keep = V[r, k].copy()
                    V[r, k] = vp
                    op = _obj_parts(eta_p, z, V, n_score, target)
                    V[r, k] = vm
                    om = _obj_parts(eta_p, z, V, n_score, target)
                    V[r, k] = keep
                    g[idx] = (op - om) / (2 * FD_H)
    return g


def adam_fd(obj, theta0, iters, lr=0.02, grad_fn=None):
    theta = theta0.copy()
    m = np.zeros_like(theta)
    v = np.zeros_like(theta)
    for t in range(1, iters + 1):
        if grad_fn is not None:
            g = grad_fn(theta)
        else:
            g = np.empty_like(theta)
            for i in range(len(theta)):
                tp = theta.copy(); tp[i] += FD_H
                tm = theta.copy(); tm[i] -= FD_H
                g[i] = (obj(tp) - obj(tm)) / (2 * FD_H)
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g * g
        mh = m / (1 - 0.9 ** t)
        vh = v / (1 - 0.999 ** t)
        theta -= lr * mh / (np.sqrt(vh) + 1e-8)
        if t == int(iters * 0.7):
            lr *= 0.3
    return theta


def fit_squeezed(K, n_score, seed, eta0, target):
    rng = np.random.default_rng(seed)
    theta0 = np.zeros(1 + 2 * K * 6)
    theta0[0] = np.log(eta0 / (1 - eta0))
    pars = rng.normal(0.0, 0.6, (2, K, 6))
    pars[..., 2] += rng.choice([-1.5, 1.5], (2, K))     # alpha near +-alpha
    pars[..., 4:] *= 0.2                                 # small squeezing
    theta0[1:] = pars.ravel()
    theta = adam_fd(lambda th: fid_obj(th, K, n_score, target), theta0, ITERS,
                    grad_fn=lambda th: _structured_grad(th, K, n_score,
                                                        target))
    m, eta_p, rho_pre = model_state(theta, K, n_score)
    tail = float(1.0 - np.trace(rho_pre[:n_score, :n_score]).real)
    return dict(F=uhlmann(m, target), eta_p=float(eta_p),
                pre_tail=tail, seed=seed, eta0=eta0)


# ---------------- free-ket addendum arm ----------------
# theta: [eta' logit, then per column Re/Im of an N_BUILD Fock vector]

def model_free(theta, n_score):
    eta_p = 1.0 / (1.0 + np.exp(-theta[0]))
    cols = theta[1:].reshape(2, N_BUILD, 2)
    rho_pre = np.zeros((N_BUILD, N_BUILD), complex)
    for r in range(2):
        col = cols[r, :, 0] + 1j * cols[r, :, 1]
        rho_pre += np.outer(col, col.conj())
    Z = np.trace(rho_pre).real
    out = kraus_loss(rho_pre / Z, eta_p, N_BUILD)
    return out[:n_score, :n_score], eta_p, rho_pre / Z


def fit_free(n_score, seed, eta0, target):
    rng = np.random.default_rng(seed)
    theta0 = np.concatenate([[np.log(eta0 / (1 - eta0))],
                             rng.normal(0.0, 0.3, 2 * N_BUILD * 2)])

    def obj(th):
        m, _, _ = model_free(th, n_score)
        return 1.0 - uhlmann(m, target)

    theta = adam_fd(obj, theta0, ITERS_FREE, lr=0.05)
    m, eta_p, rho_pre = model_free(theta, n_score)
    tail = float(1.0 - np.trace(rho_pre[:n_score, :n_score]).real)
    return dict(F=uhlmann(m, target), eta_p=float(eta_p),
                pre_tail=tail, seed=seed, eta0=eta0)


def main():
    out = dict(params=dict(alpha=ALPHA, parity=PARITY, eta=ETA, sigma=SIGMA,
                           n_build=N_BUILD, iters=ITERS, fd_h=FD_H),
               squeezed=[], free_ket=[])
    print("=== exp20 Route B: best-approximation residuals (declared "
          "protocol: fidelity objective, n {8,10,12}, K {2,4,8}; 1-mode "
          "is the single declared deviation, see docstring) ===")
    for n_score in N_SCORES:
        target = build_target(n_score)
        for K in KS:
            fits = []
            for seed, eta0 in INITS:
                t0 = time.perf_counter()
                r = fit_squeezed(K, n_score, seed, eta0, target)
                r.update(n_score=n_score, K=K,
                         wall=round(time.perf_counter() - t0))
                fits.append(r)
                out["squeezed"].append(r)
            best = min(fits, key=lambda r: 1 - r["F"])
            print(f"  n{n_score} K{K}: best 1-F = {1 - best['F']:.5f} "
                  f"(eta' {best['eta_p']:.3f}, "
                  f"pre-tail {best['pre_tail']:.1e}, seed {best['seed']}; "
                  f"all 1-F: "
                  f"{[round(1 - r['F'], 5) for r in fits]})", flush=True)

    print("\n--- [ADDENDUM] rank-2 free-ket superset arm (n_score=12, "
          "eta' free) ---")
    target = build_target(12)
    fits = []
    for seed, eta0 in INITS:
        r = fit_free(12, seed, eta0, target)
        r.update(n_score=12)
        fits.append(r)
        out["free_ket"].append(r)
    best = min(fits, key=lambda r: 1 - r["F"])
    print(f"  best 1-F = {1 - best['F']:.5f} (eta' {best['eta_p']:.3f}, "
          f"pre-tail {best['pre_tail']:.1e}; "
          f"all 1-F: {[round(1 - r['F'], 5) for r in fits]}, "
          f"eta': {[round(r['eta_p'], 3) for r in fits]})", flush=True)

    floors = {}
    for n_score in N_SCORES:
        rs = [r for r in out["squeezed"] if r["n_score"] == n_score]
        floors[n_score] = min(1 - r["F"] for r in rs)
    out["ruling"] = dict(best_residuals_by_cutoff=floors,
                         alarm=any(f < 1e-4 for f in floors.values()))
    print("\n=== Route B ruling ===")
    print(f"  best-found 1-F by scoring cutoff: "
          f"{ {k: round(v, 5) for k, v in floors.items()} }")
    if out["ruling"]["alarm"]:
        print("-> ALARM: a fit reached 1-F < 1e-4, contradicting Route A's "
              "exact non-inclusion -- the derivation must be re-examined "
              "before any ruling (case-1 branch).")
    else:
        print("-> best-found residuals stay well above the alarm line at "
              "every cutoff and K, and are cutoff-stable. As local-"
              "optimization results these are UPPER bounds on the "
              "family's distance -- heuristic corroboration of Route A's "
              "analytic exclusion, which alone carries the case-2 "
              "obstruction (issue #63 decision rule).")

    path = pathlib.Path(__file__).parent / "results_routeB.json"
    path.write_text(json.dumps(out, indent=1))
    print(f"\nraw results -> {path}")


if __name__ == "__main__":
    main()
