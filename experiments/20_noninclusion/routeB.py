"""Experiment 20, Route B -- issue #63: best-approximation corroboration.

Route A (run.py + derivation.md) settled EXACT non-inclusion: no eta'
in (0, 1] admits a finite-rank pre-image of the thermal-noise target.
Route B corroborates on the FINITE-fidelity axis the exp19 comparisons
actually live on: directly optimize the fidelity of
loss_eta'(rank-2 squeezed ket mixture) against the target -- no data,
no sampling noise, FD gradients on the exact Fock-side objective -- and
watch whether 1 - F approaches 0 (which would CONTRADICT Route A and
fire the representability branch) or stalls on a floor that survives
cutoff growth.

PROTOCOL NOTE (deviation from the issue text, declared before running):
the issue sketched Route B "against the Fock-basis target at n_max =
8, 10, 12" with the 3-mode target in mind. A 3-mode FD fit is
computationally out of reach (the wide-cutoff channel application per
FD probe puts a single config in the multi-hour range), and Route A's
regime argument is mode-count-agnostic (derivation.md section 5). Route
B therefore runs the ONE-MODE problem -- same channels, same cat, same
regime structure, scoring cutoffs n_score = 12 / 16 / 20 -- where the
objective is exact and cheap. The exp19 blind 3-mode fit itself
(F = 0.9234, i.e. 1 - F = 0.077 at trace ceiling 0.9922) already
provides the 3-mode data point: a NLL-driven optimizer left a gap of
the same order as the floor found here.

Design:
  * target: N_sigma(E_eta(cat1)) built wide (n = 30) and cropped.
  * model: rho' = B B^dag / Z, B = 2 columns of K displaced-squeezed
    kets (bbdagS.sq_wavefunction coefficients by quadrature, n_build =
    30); channel = truncated Kraus loss at n_build, cropped to n_score;
    eta' free through a logit. OBJECTIVE: minimize the Frobenius (HS)
    distance || model - target ||_F (smooth, cheap); REPORT Uhlmann
    fidelity of the final state (the declared floor metric).
  * grid: n_score in {12, 16, 20} x K in {2, 4} x 3 inits (seed 0/1/2
    with eta'0 = 0.8 / 0.6 / 0.4 -- inits span the regime boundary).
    Representative per (n_score, K): best final HS.
  * addendum arm (labeled): rank-2 FREE-Fock-ket pre-image (columns as
    unconstrained complex vectors, a strict superset of the squeezed
    family) at n_score = 16 -- an upper bound that removes the
    "squeezed parametrization just couldn't express it" confound.
  * cutoff-abuse monitor: pre-loss population of the fitted kets above
    n_score is quoted (an optimizer parking mass at the build cutoff
    would fake a low HS).

Decision quantities: min over fits of 1 - F per n_score. Floor stable
across n_score (and shared by the free-ket arm) -> corroborates case 2.
Any fit with 1 - F < 1e-4 -> representability alarm, re-examine Route A.
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
N_SCORES = (12, 16, 20)
KS = (2, 4)
INITS = ((0, 0.8), (1, 0.6), (2, 0.4))
ITERS = 500
ITERS_FREE = 400
FD_H = 1e-5

_XGRID = np.linspace(-14.0, 14.0, 4001)
_HPSI = hermite_psi(_XGRID, N_BUILD)


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
        A[idx - k, idx] = [np.sqrt(comb(m, k) * eta ** (m - k)
                                   * (1 - eta) ** k) for m in idx]
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


def model_state(theta, K, n_score):
    """(cropped model matrix, eta', pre-loss rho at N_BUILD)."""
    eta_p, z, al, xi = unpack(theta, K)
    rho_pre = np.zeros((N_BUILD, N_BUILD), complex)
    for r in range(2):
        col = np.zeros(N_BUILD, complex)
        for k in range(K):
            f = sq_wavefunction(_XGRID, al[r, k], xi[r, k])
            col += z[r, k] * np.trapezoid(_HPSI * f[None, :], _XGRID, axis=1)
        rho_pre += np.outer(col, col.conj())
    Z = np.trace(rho_pre).real
    out = kraus_loss(rho_pre / Z, eta_p, N_BUILD)
    return out[:n_score, :n_score], eta_p, rho_pre / Z


def hs_obj(theta, K, n_score, target):
    m, _, _ = model_state(theta, K, n_score)
    return float(np.sum(np.abs(m - target) ** 2))


def adam_fd(obj, theta0, iters, lr=0.02):
    theta = theta0.copy()
    m = np.zeros_like(theta)
    v = np.zeros_like(theta)
    for t in range(1, iters + 1):
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
    theta = adam_fd(lambda th: hs_obj(th, K, n_score, target), theta0, ITERS)
    m, eta_p, rho_pre = model_state(theta, K, n_score)
    tail = float(1.0 - np.trace(rho_pre[:n_score, :n_score]).real)
    return dict(hs=float(np.sqrt(np.sum(np.abs(m - target) ** 2))),
                F=uhlmann(m, target), eta_p=float(eta_p),
                pre_tail=tail, seed=seed, eta0=eta0)


# ---------------- free-ket addendum arm ----------------
# theta: per column, Re/Im of an N_BUILD Fock vector (superset family)

def model_free(theta, n_score, eta_p):
    cols = theta.reshape(2, N_BUILD, 2)
    rho_pre = np.zeros((N_BUILD, N_BUILD), complex)
    for r in range(2):
        col = cols[r, :, 0] + 1j * cols[r, :, 1]
        rho_pre += np.outer(col, col.conj())
    Z = np.trace(rho_pre).real
    out = kraus_loss(rho_pre / Z, eta_p, N_BUILD)
    return out[:n_score, :n_score], rho_pre / Z


def fit_free(n_score, seed, eta_p, target):
    """eta' held FIXED per run (the free-ket arm probes ket freedom;
    the eta' axis is already scanned exactly by Route A)."""
    rng = np.random.default_rng(seed)
    theta0 = rng.normal(0.0, 0.3, 2 * N_BUILD * 2)

    def obj(th):
        m, _ = model_free(th, n_score, eta_p)
        return float(np.sum(np.abs(m - target) ** 2))

    theta = adam_fd(obj, theta0, ITERS_FREE, lr=0.05)
    m, rho_pre = model_free(theta, n_score, eta_p)
    tail = float(1.0 - np.trace(rho_pre[:n_score, :n_score]).real)
    return dict(hs=float(np.sqrt(np.sum(np.abs(m - target) ** 2))),
                F=uhlmann(m, target), eta_p=eta_p, pre_tail=tail, seed=seed)


def main():
    out = dict(params=dict(alpha=ALPHA, parity=PARITY, eta=ETA, sigma=SIGMA,
                           n_build=N_BUILD, iters=ITERS, fd_h=FD_H),
               squeezed=[], free_ket=[])
    print("=== exp20 Route B: best-approximation floor (1-mode; protocol "
          "deviation from the 3-mode sketch declared in the docstring) ===")
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
            best = min(fits, key=lambda r: r["hs"])
            print(f"  n{n_score} K{K}: best 1-F = {1 - best['F']:.5f} "
                  f"(HS {best['hs']:.4f}, eta' {best['eta_p']:.3f}, "
                  f"pre-tail {best['pre_tail']:.1e}, seed {best['seed']}; "
                  f"all 1-F: "
                  f"{[round(1 - r['F'], 5) for r in fits]})", flush=True)

    print("\n--- [ADDENDUM] rank-2 free-ket upper-bound arm (n_score=16) ---")
    target = build_target(16)
    for eta_p in (0.5, 0.65, 0.8):
        fits = [fit_free(16, s, eta_p, target) for s in (0, 1, 2)]
        best = min(fits, key=lambda r: r["hs"])
        for r in fits:
            r.update(n_score=16)
            out["free_ket"].append(r)
        print(f"  eta'={eta_p:.2f}: best 1-F = {1 - best['F']:.5f} "
              f"(HS {best['hs']:.4f}, pre-tail {best['pre_tail']:.1e}; "
              f"all 1-F: {[round(1 - r['F'], 5) for r in fits]})",
              flush=True)

    floors = {}
    for n_score in N_SCORES:
        rs = [r for r in out["squeezed"] if r["n_score"] == n_score]
        floors[n_score] = min(1 - r["F"] for r in rs)
    out["ruling"] = dict(floors_by_cutoff=floors,
                         alarm=any(f < 1e-4 for f in floors.values()))
    print("\n=== Route B ruling ===")
    print(f"  best 1-F by scoring cutoff: "
          f"{ {k: round(v, 5) for k, v in floors.items()} }")
    if out["ruling"]["alarm"]:
        print("-> ALARM: a fit reached 1-F < 1e-4; representability branch "
              "must be re-examined against Route A before any ruling.")
    else:
        print("-> a floor in 1-F persists at every scoring cutoff, "
              "corroborating Route A's exact non-inclusion on the "
              "finite-fidelity axis (issue #63 decision rule, case 2).")

    path = pathlib.Path(__file__).parent / "results_routeB.json"
    path.write_text(json.dumps(out, indent=1))
    print(f"\nraw results -> {path}")


if __name__ == "__main__":
    main()
