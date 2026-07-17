"""Experiment 20 -- issue #63: the non-inclusion test, Route A numerics.

Does ANY eta' in (0, 1] admit a finite-rank pre-image rho' with
loss_eta'(rho') = N_sigma(E_eta(cat)) (the exp19 target)? The derivation
note (derivation.md, same directory) shows the pre-image is UNIQUE for
every eta' and splits (0, 1] into:

  Regime I/II  (eta' > eta - sigma):  pre-image = a positive-variance
      Gaussian-displacement-noise composition -> FULL RANK analytically
      (Lemma 2, displacement orthogonality). This script CORROBORATES
      the lemma numerically (eigenvalue tails at sample points, checked
      against the independent channel machinery in wigner_splat.fock).
  Boundary     (eta' = eta - sigma):  pre-image = quantum-limited
      amplifier output A_G(cat) -- no lemma; the spectrum is computed.
  Regime III   (eta' < eta - sigma):  the pre-image carries a formal
      negative-variance residue; whether it is even PSD is the open
      part. This script SETTLES it on a grid: reconstruct rho'(eta') in
      the Fock basis from its closed-form characteristic function and
      scan min eigenvalue + eigenvalue tail.

Reconstruction route: chi_{rho'}(lam) = chi_cat(k lam) e^{-c |lam|^2}
with k^2 = eta/eta', c = (eta' - eta + 2 sigma)/(2 eta') is a sum of 4
coherent-pair terms (the cat is a 2-coherent superposition), and
rho' = (1/pi) int chi(lam) D(lam)^dagger d^2lam is evaluated by
Gauss-Hermite quadrature rescaled to the integrand's dominant Gaussian
(total decay rate 1/2 + sigma/eta' on the chi side plus 1/2 from the
displacement kernel -- see derivation.md section 2). The 3-mode
pre-image factorizes per chi term into a Kronecker product of identical
1-mode operators, so the scan runs in full 3-mode form as well.

Accuracy is pinned by tests/test_noninclusion.py against independent
references: at eta' = eta the pre-image must equal N_{sigma/eta}(cat)
(Lemma 1), in regime I it must equal thermal_lossy_cat3_fock with
remapped parameters, and applying truncated-Kraus loss to the
reconstruction must recover the target.

DECISION QUANTITIES (issue #63 decision rule):
  * regime III: min eigenvalue << -numerical noise on the whole grid
    -> no PSD pre-image -> combined with the regime-I/II lemma, NO
    finite-rank pre-image exists for ANY eta' (case-2 branch, pending
    Route B corroboration).
  * any eta' with a PSD pre-image of rank <= 2 -> representable
    (case-1 branch).

Scan design: 1-mode fine grid eta' in [0.10, 1.00] step 0.02 at
n_max = 30 (n_max = 40 stability spot checks at the smallest eta',
where the amplified cat k*alpha = alpha*sqrt(eta/eta') needs the most
headroom), plus a fine boundary strip [0.60, 0.72] step 0.01. 3-mode
confirmation grid eta' in {0.40 ... 1.00} step 0.05 at n_max = 12 per
mode. Parameters frozen to the exp19 target: alpha = 1.5, parity = +1,
eta = 0.8, sigma_add = 0.1.
"""
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fock import _genlaguerre, displacement_matrix  # noqa: E402

ALPHA = 1.5
PARITY = +1
ETA = 0.8
SIGMA = 0.1
N_1MODE = 30
N_1MODE_CHECK = 40
N_3MODE = 12
GH_NODES = 80

ETA_GRID_1M = np.round(np.concatenate([
    np.arange(0.10, 1.0001, 0.02),
    np.arange(0.60, 0.7201, 0.01),
]), 4)
ETA_GRID_1M = np.unique(ETA_GRID_1M)
ETA_GRID_3M = np.round(np.arange(0.40, 1.0001, 0.05), 4)


# ---------------- closed-form chi pieces (coherent pairs) ----------------

def coh_pair_chi(beta, gam, lam):
    """Tr[|beta><gam| D(lam)] = <gam|D(lam)|beta> for coherent beta, gam.

    From D(lam)|beta> = e^{(lam conj(beta) - conj(lam) beta)/2} |beta+lam>
    and <gam|mu> = exp(-|gam|^2/2 - |mu|^2/2 + conj(gam) mu).
    """
    mu = beta + lam
    return np.exp((lam * np.conj(beta) - np.conj(lam) * beta) / 2.0
                  - np.abs(gam) ** 2 / 2.0 - np.abs(mu) ** 2 / 2.0
                  + np.conj(gam) * mu)


def cat_terms_1mode(alpha, parity):
    """[(beta, gam, coef)] with rho_cat = sum coef |beta><gam| (1 mode)."""
    n2 = 2.0 * (1.0 + parity * np.exp(-2.0 * alpha ** 2))
    a = complex(alpha)
    return [(a, a, 1.0 / n2), (-a, -a, 1.0 / n2),
            (a, -a, parity / n2), (-a, a, parity / n2)]


def cat_terms_3mode(alpha, parity):
    """Per-term data for the 3-mode cat |a,a,a> + parity |-a,-a,-a>.

    Each term is coef * |b>< g| ^{tensor 3} with the SAME 1-mode pair in
    every mode, so the pre-image assembles as coef * kron(O, O, O).
    """
    n2 = 2.0 * (1.0 + parity * np.exp(-6.0 * alpha ** 2))
    a = complex(alpha)
    return [(a, a, 1.0 / n2), (-a, -a, 1.0 / n2),
            (a, -a, parity / n2), (-a, a, parity / n2)]


def preimage_consts(eta_p, eta=ETA, sigma=SIGMA):
    """k (argument scale) and c (Gaussian residue) of the pre-image chi."""
    k = np.sqrt(eta / eta_p)
    c = (eta_p - eta + 2.0 * sigma) / (2.0 * eta_p)
    return k, c


# ---------------- chi -> Fock by rescaled Gauss-Hermite ----------------

def _gh_lambda_grid(a_scale, n_nodes):
    """2D nodes lam and weights w with int f d^2lam = sum w f(lam),
    Gauss-Hermite rescaled so the weight matches e^{-a_scale |lam|^2}."""
    t, wt = np.polynomial.hermite.hermgauss(n_nodes)
    s = np.sqrt(a_scale)
    x = t / s
    wx = wt * np.exp(t ** 2) / s          # compensated 1D weights
    lam = x[:, None] + 1j * x[None, :]
    w = wx[:, None] * wx[None, :]
    return lam.ravel(), w.ravel()


def displacement_batch(betas, n_max):
    """D[g, m, n] = <m|D(beta_g)|n> for a 1D array of betas.

    Same Laguerre closed form as fock.displacement_matrix (which stays
    the tested scalar reference), vectorized over the quadrature grid --
    the scan calls this once per eta' instead of G times.
    """
    betas = np.asarray(betas, complex).ravel()
    y = np.abs(betas) ** 2
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    env = np.exp(-y / 2.0)
    D = np.zeros((len(betas), n_max, n_max), complex)
    for d in range(n_max):
        L = _genlaguerre(n_max - d, d, y)              # (n_max - d, G)
        bd = betas ** d
        bdc = (-np.conj(betas)) ** d
        for n in range(n_max - d):
            m = n + d
            amp = np.exp((log_fact[n] - log_fact[m]) / 2.0)
            D[:, m, n] = amp * bd * env * L[n]
            if d > 0:
                D[:, n, m] = amp * bdc * env * L[n]
    return D


def preimage_ops(eta_p, n_max, terms, n_nodes=GH_NODES,
                 eta=ETA, sigma=SIGMA):
    """One (n_max, n_max) operator per coherent-pair term:
    O = (1/pi) int <gam|D(k lam)|beta> e^{-c|lam|^2} D(lam)^dag d^2lam.

    Dominant Gaussian decay of the integrand is (k^2/2 + c) from the chi
    side + 1/2 from D^dagger's envelope, which fixes the quadrature
    rescale; the displacement tensor is shared across the terms.
    """
    k, c = preimage_consts(eta_p, eta, sigma)
    a_scale = k ** 2 / 2.0 + c + 0.5
    lam, w = _gh_lambda_grid(a_scale, n_nodes)
    Dc = displacement_batch(lam, n_max).conj()         # (G, m, n) of conj(D)
    ops = []
    for beta, gam, _ in terms:
        chi = coh_pair_chi(beta, gam, k * lam) * np.exp(-c * np.abs(lam) ** 2)
        ops.append(np.tensordot(w * chi, Dc, axes=(0, 0)).T / np.pi)
    return ops


def preimage_1mode(eta_p, n_max, n_nodes=GH_NODES, alpha=ALPHA,
                   parity=PARITY, eta=ETA, sigma=SIGMA):
    """rho'(eta') for the 1-mode model problem."""
    terms = cat_terms_1mode(alpha, parity)
    ops = preimage_ops(eta_p, n_max, terms, n_nodes, eta, sigma)
    rho = np.zeros((n_max, n_max), complex)
    for (_, _, coef), op in zip(terms, ops):
        rho += coef * op
    return rho


def preimage_3mode(eta_p, n_max, n_nodes=GH_NODES, alpha=ALPHA,
                   parity=PARITY, eta=ETA, sigma=SIGMA):
    """rho'(eta') for the actual 3-mode exp19 target, via the per-term
    Kronecker factorization (flat (n^3, n^3))."""
    terms = cat_terms_3mode(alpha, parity)
    ops = preimage_ops(eta_p, n_max, terms, n_nodes, eta, sigma)
    rho = np.zeros((n_max ** 3, n_max ** 3), complex)
    for (_, _, coef), op in zip(terms, ops):
        rho += coef * np.kron(np.kron(op, op), op)
    return rho


# ---------------- diagnostics ----------------

def spectrum_report(rho):
    herm = float(np.max(np.abs(rho - rho.conj().T)))
    ev = np.sort(np.linalg.eigvalsh((rho + rho.conj().T) / 2.0))[::-1]
    return dict(
        trace=float(np.sum(ev)),
        herm_resid=herm,
        min_eig=float(ev[-1]),
        top4=[float(v) for v in ev[:4]],
        lam3=float(ev[2]),          # rank-2 residual: 3rd eigenvalue
        neg_mass=float(np.sum(np.abs(ev[ev < 0.0]))),
    )


def main():
    out = dict(params=dict(alpha=ALPHA, parity=PARITY, eta=ETA, sigma=SIGMA,
                           n_1mode=N_1MODE, n_3mode=N_3MODE,
                           gh_nodes=GH_NODES),
               scan_1mode=[], scan_3mode=[], stability=[])
    print("=== exp20: issue #63 -- non-inclusion test, Route A numerics ===")
    print(f"target alpha={ALPHA} parity={PARITY:+d} eta={ETA} "
          f"sigma_add={SIGMA}; boundary eta'-crit = eta - sigma = "
          f"{ETA - SIGMA:.2f}")
    print(f"\n--- 1-mode scan (n_max={N_1MODE}, GH {GH_NODES}^2) ---")
    print("  eta'    trace     min_eig     lam3       regime")
    for eta_p in ETA_GRID_1M:
        rho = preimage_1mode(float(eta_p), N_1MODE)
        rep = spectrum_report(rho)
        rep["eta_p"] = float(eta_p)
        regime = ("III (v<0)" if eta_p < ETA - SIGMA - 1e-12 else
                  "boundary" if abs(eta_p - (ETA - SIGMA)) < 1e-12 else
                  "II" if eta_p <= ETA else "I")
        rep["regime"] = regime
        out["scan_1mode"].append(rep)
        print(f"  {eta_p:.2f}   {rep['trace']:+.5f}  {rep['min_eig']:+.2e}"
              f"  {rep['lam3']:.2e}   {regime}", flush=True)

    print(f"\n--- n_max={N_1MODE_CHECK} stability spot checks ---")
    for eta_p in (0.10, 0.20, 0.40, 0.69):
        rho = preimage_1mode(eta_p, N_1MODE_CHECK)
        rep = spectrum_report(rho)
        rep["eta_p"] = eta_p
        out["stability"].append(rep)
        base = next(r for r in out["scan_1mode"]
                    if abs(r["eta_p"] - eta_p) < 1e-9)
        print(f"  eta'={eta_p:.2f}: min_eig {rep['min_eig']:+.3e} "
              f"(n{N_1MODE}: {base['min_eig']:+.3e}), trace "
              f"{rep['trace']:+.5f}", flush=True)

    print(f"\n--- 3-mode confirmation scan (n_max={N_3MODE}/mode) ---")
    print("  eta'    trace     min_eig     lam3       regime")
    for eta_p in ETA_GRID_3M:
        rho = preimage_3mode(float(eta_p), N_3MODE)
        rep = spectrum_report(rho)
        rep["eta_p"] = float(eta_p)
        regime = ("III (v<0)" if eta_p < ETA - SIGMA - 1e-12 else
                  "II" if eta_p <= ETA else "I")
        rep["regime"] = regime
        out["scan_3mode"].append(rep)
        print(f"  {eta_p:.2f}   {rep['trace']:+.5f}  {rep['min_eig']:+.2e}"
              f"  {rep['lam3']:.2e}   {regime}", flush=True)

    # ---------------- ruling (decision quantities, issue #63) -----------
    noise = 10.0 ** -8          # PSD violations must clear this by orders
    r3 = [r for r in out["scan_1mode"] if r["regime"].startswith("III")]
    r12 = [r for r in out["scan_1mode"]
           if r["regime"] in ("I", "II", "boundary")]
    worst_neg = min(r["min_eig"] for r in r3)
    all_neg = all(r["min_eig"] < -noise for r in r3)
    min_lam3 = min(r["lam3"] for r in r12 if r["min_eig"] > -noise)
    r3_3m = [r for r in out["scan_3mode"] if r["regime"].startswith("III")]
    all_neg_3m = all(r["min_eig"] < -noise for r in r3_3m)
    out["ruling"] = dict(regimeIII_all_nonPSD_1mode=all_neg,
                         regimeIII_worst_min_eig=worst_neg,
                         regimeIII_all_nonPSD_3mode=all_neg_3m,
                         regimeI_II_min_lam3=min_lam3)
    print("\n=== Route A ruling ===")
    print(f"  regime III (eta' < {ETA - SIGMA:.2f}): PSD fails at every "
          f"grid point (1-mode): {all_neg}; worst min_eig {worst_neg:+.3e}")
    print(f"  regime III 3-mode confirmation: {all_neg_3m}")
    print(f"  regime I/II PSD points: smallest 3rd eigenvalue "
          f"{min_lam3:.3e} (rank-2 would need ~0; full-rank tail as "
          f"Lemma 2 predicts)")
    if all_neg and all_neg_3m:
        print("-> NO eta' in (0, 1] admits a PSD finite-rank pre-image on "
              "the scanned grid: regime I/II excluded analytically "
              "(derivation.md Lemmas 1-2), regime III excluded by this "
              "scan. Pending Route B corroboration (issue #63 decision "
              "rule, case-2 branch).")
    else:
        print("-> scan found PSD candidates in regime III or a rank-2-"
              "compatible tail; the representability branch (case 1) "
              "must be examined before any ruling.")

    path = pathlib.Path(__file__).parent / "results.json"
    path.write_text(json.dumps(out, indent=1))
    print(f"\nraw results -> {path}")


if __name__ == "__main__":
    main()
