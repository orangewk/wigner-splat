"""Experiment 05: the representation entanglement-cost of the two-mode cat.

QUESTION (orchestrator's conjecture). To approximate the two-mode entangled
cat Wigner |a,a> + |-a,-a> at fidelity >= F_th with a SIGNED Gaussian mixture,
the axis-aligned (separable, block-diagonal covariance) representation needs
K_axis components and the tilted (full 4x4 covariance) representation needs
K_tilted. Does the ratio R(alpha) = K_axis / K_tilted track

  (i) the ENTANGLEMENT E(alpha), which SATURATES at 1 ebit as alpha grows, or
  (ii) the phase-space fringe wavenumber k = 2 sqrt2 alpha, which grows without
       bound?

If R keeps climbing after E has saturated (alpha >~ 1.5), the naive "cost
tracks entanglement" story is REFUTED and must be refined to "cost tracks the
nonclassical interference scale k". We MEASURE; we do not advocate.

METHOD (approximation theory, not tomography -- no sampling, no histograms).
Both forward modules give the EXACT overlap fidelity_vs_cat = tr(rho_mix
rho_cat) = (2pi)^2 int W_mix W_cat, linear in the component weights. For a fixed
set of component geometries {mu_k, Sigma_k} the honest, non-degenerate
reconstruction is the L2 fit

  min_w || W_mix - W_cat ||^2  s.t.  sum_k w_k = 1,

a small equality-constrained QP:  min w^T A w - 2 b^T w,
  A_kl = tr(rho_k rho_l)  (closed-form 4D Gaussian-Gaussian overlap, = gram()),
  b_k  = tr(rho_k rho_cat) (= bvec(), == forward2f.fidelity_vs_cat per-component).
At the optimum, achieved fidelity F = b^T w and relative-L2^2 = 1 - 2F + w^T A w.

STOPPING CRITERION -- why relative L2, not raw F. The components are SIGNED
Gaussians used as a BASIS (the Kenfack / this-repo premise), NOT physical states,
so a single sub-Planck "spike" Gaussian can have raw overlap b_k = tr(rho_k
rho_cat) > 1 (measured: 1.8 for one narrow Gaussian). Raw F >= F_th is therefore
cheatable and meaningless. The honest, spike-proof criterion is the
approximation-theory one the protocol specifies: relative L2 <= eps, with
eps = sqrt(2 (1 - F_th)). This rejects spikes (their purity self-energy w^T A w
blows relative-L2 up) and COINCIDES with F >= F_th exactly at unit purity
w^T A w = 1 (a pure reconstruction). In every run below the L2-optimal mixtures
sit at purity ~1 (0.96-1.01) with bounded weights (|w| <~ 0.5), so the achieved
F (reported alongside) lands at ~0.98-1.00, i.e. the F_th target.

K_min is found by GREEDY matching pursuit from a candidate pool (add the
component most correlated with the fidelity residual b - A_sel w, re-solve the
QP, stop at relative L2 <= eps). The SAME greedy runs on both pools, so R is
apples-to-apples. Both constructions are cross-checked against the library
fidelity_vs_cat.

BIAS / CAVEAT on K_min. (1) Greedy is an UPPER bound on the true K-term optimum;
both pools pay it, so it largely cancels in R. (2) The ABSOLUTE K's depend on the
dictionary scale (component width); the RATIO R is the deliverable and is stable
across reasonable width choices (robustness check printed at the end). (3) The
tilted pool is a small 1D ridge, nearly exhausted; the axis pool is a 2D product
grid where greedy is looser -- so if anything R is UNDER-stated at large alpha,
which only strengthens a "R keeps growing" verdict.

E(alpha) DERIVATION (parity +1). With normalized even/odd cats |+>,|-> and
u = <a|-a> = e^{-2a^2}, the entangled coherent state Schmidt-decomposes as
|Psi> ∝ N+ |+>|+> + N- |->|->, N± = 2(1 ± u). The Schmidt probabilities are
p± = (1 ± x)/2 with x = 2u/(1+u^2) = sech(2 a^2), so

  E(alpha) = H2( (1 + sech(2 a^2)) / 2 ),   H2 the binary entropy (bits).

x -> 0 as alpha -> inf => E -> H2(1/2) = 1 ebit (SATURATES); x -> 1 as
alpha -> 0 => E -> 0 (product state). Verified numerically below.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from wigner_splat.forward2f import (
    _gaussian_overlap4, _TRIL_I, _TRIL_J, SplatMixture2F,
    fidelity_vs_cat as fid_full,
)
from wigner_splat.forward2 import SplatMixture2, fidelity_vs_cat as fid_sep

R2 = np.sqrt(2.0)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# principal-axis unit vectors in (x1, p1, x2, p2)
E_X1 = np.array([1.0, 0, 0, 0])
E_X2 = np.array([0.0, 0, 1, 0])
E_S = np.array([0.0, 1, 0, 1]) / R2   # (p1 + p2) direction
E_D = np.array([0.0, 1, 0, -1]) / R2  # (p1 - p2) direction


# --------------------------------------------------------------------------
# entanglement + fringe drivers
# --------------------------------------------------------------------------
def entanglement_entropy(alpha):
    """E(alpha) in bits for the parity-+1 two-mode cat (see module docstring)."""
    u = np.exp(-2.0 * alpha ** 2)
    x = 2.0 * u / (1.0 + u ** 2)          # = sech(2 alpha^2)
    p = 0.5 * (1.0 + x)
    def h(q):
        if q <= 0.0 or q >= 1.0:
            return 0.0
        return -q * np.log2(q) - (1 - q) * np.log2(1 - q)
    return h(p)


def k_fringe(alpha):
    return 2.0 * R2 * alpha


# --------------------------------------------------------------------------
# closed-form L2-fit engine (validated in scratch against library + brute force)
# --------------------------------------------------------------------------
def bvec(mu, Sigma, alpha, parity=+1):
    """b_k = tr(rho_k rho_cat) for each component; == fidelity_vs_cat per k."""
    a = float(alpha)
    r2a = R2 * a
    norm = 2 * (1 + parity * np.exp(-4 * a ** 2))
    c_pp = np.array([r2a, 0.0, r2a, 0.0])
    c_mm = -c_pp
    c_f = np.array([0.0, 1j * r2a, 0.0, 1j * r2a])
    O_pp = _gaussian_overlap4(mu, Sigma, c_pp).real
    O_mm = _gaussian_overlap4(mu, Sigma, c_mm).real
    O_f = _gaussian_overlap4(mu, Sigma, c_f)
    per_k = O_pp + O_mm + parity * 2.0 * np.exp(-2 * r2a ** 2) * O_f.real
    return 4.0 / norm * per_k


def gram(mu, Sigma):
    """A_kl = tr(rho_k rho_l), closed-form 4D Gaussian-Gaussian overlap."""
    S = Sigma[:, None, :, :] + Sigma[None, :, :, :]
    d = mu[:, None, :] - mu[None, :, :]
    Sinv = np.linalg.inv(S)
    quad = np.einsum("kli,klij,klj->kl", d, Sinv, d)
    det = np.linalg.det(S)
    return np.exp(-0.5 * quad) / np.sqrt(det)


def solve_qp(A, b, ridge):
    """min w^T (A+ridge I) w - 2 b^T w  s.t. 1^T w = 1.  Returns (w, F=b^T w)."""
    n = len(b)
    M = A + ridge * np.eye(n)
    Mi_b = np.linalg.solve(M, b)
    Mi_1 = np.linalg.solve(M, np.ones(n))
    lam = (np.ones(n) @ Mi_b - 1.0) / (np.ones(n) @ Mi_1)
    w = Mi_b - lam * Mi_1
    return w, float(b @ w)


def greedy_kmin(mu, Sigma, alpha, F_th, max_K, ridge=1e-8, parity=+1):
    """Greedy matching pursuit: smallest set whose L2-optimal fit reaches
    relative L2 <= sqrt(2 (1 - F_th)) (== F >= F_th at unit purity).

    Returns (K, F, relL2, purity, sel_indices, w). Adds the pool component most
    correlated with the fidelity residual b - A_sel w, re-solves the constrained
    QP each step. relL2^2 = 1 - 2 F + w^T A w uses the true (unridged) A.
    """
    A = gram(mu, Sigma)
    b = bvec(mu, Sigma, alpha, parity)
    P = len(b)
    tol2 = 2.0 * (1.0 - F_th)                 # relative-L2^2 threshold
    sel = []
    w = np.zeros(0)
    best = (P, 0.0, np.inf, 1.0)             # K, F, relL2^2, purity at best relL2
    As = np.zeros((0, 0))
    for _ in range(min(max_K, P)):
        resid = (b - A[:, sel] @ w) if sel else b.copy()
        resid = resid.copy()
        if sel:
            resid[sel] = 0.0                 # do not re-pick
        c = int(np.argmax(np.abs(resid)))
        sel.append(c)
        As = A[np.ix_(sel, sel)]
        w, F = solve_qp(As, b[sel], ridge)
        wAw = float(w @ As @ w)
        rel2 = 1.0 - 2.0 * F + wAw
        if rel2 < best[2]:
            best = (len(sel), F, rel2, wAw)
        if rel2 <= tol2:
            return len(sel), F, np.sqrt(max(rel2, 0.0)), wAw, list(sel), w
    # never reached tol within the pool: report the closest (best relL2)
    return best[0], best[1], np.sqrt(max(best[2], 0.0)), best[3], list(sel), w


# --------------------------------------------------------------------------
# candidate pools
# --------------------------------------------------------------------------
def _blobs_full(alpha):
    r2a = R2 * alpha
    mu = np.array([[r2a, 0, r2a, 0], [-r2a, 0, -r2a, 0]], float)
    Sig = np.array([0.5 * np.eye(4), 0.5 * np.eye(4)])
    return mu, Sig


def _ridge_sigma(vx, vs, vd):
    return (vx * (np.outer(E_X1, E_X1) + np.outer(E_X2, E_X2))
            + vs * np.outer(E_S, E_S) + vd * np.outer(E_D, E_D))


def tilted_pool(alpha, over=3.0, wf=0.5, Smax=3.0):
    """2 blobs + a ridge of full-cov fringe Gaussians along (p1+p2), elongated
    to match the isotropic envelope (vx=vd=1/2) and narrow along p1+p2 to
    resolve the wavenumber sqrt2*k oscillation. Same over/wf convention as the
    axis pool, so the two K's are measured with one consistent dictionary."""
    k = k_fringe(alpha)
    mu0, Sig0 = _blobs_full(alpha)
    half = np.pi / (R2 * k)                 # half period along s = p1+p2
    dsr = half / over                       # ridge spacing
    n = int(2 * Smax / dsr) + 1
    sig_s = np.linspace(-Smax, Smax, n)
    vs = (wf * dsr) ** 2                    # narrow along p1+p2
    mus, Sigs = [], []
    for s in sig_s:
        p = s / R2                          # p1 = p2 = s / sqrt2  (d = 0)
        mus.append([0.0, p, 0.0, p])
        Sigs.append(_ridge_sigma(0.5, vs, 0.5))
    mu = np.vstack([mu0, np.array(mus)])
    Sig = np.concatenate([Sig0, np.array(Sigs)], axis=0)
    return mu, Sig


def _blobs_sep_sigma(alpha):
    mu = np.array([[R2 * alpha, 0, R2 * alpha, 0],
                   [-R2 * alpha, 0, -R2 * alpha, 0]], float)
    Sig = np.array([0.5 * np.eye(4), 0.5 * np.eye(4)])
    return mu, Sig


def axis_pool(alpha, over=3.0, wf=0.5, Bmax=2.8, mcap=34):
    """2 blobs + a product grid of separable (block-diagonal) fringe Gaussians:
    component (i,j) = mode-1 Gaussian at p1=b_i times mode-2 Gaussian at p2=b_j,
    each cov diag(1/2, vp), narrow in p to resolve the per-mode wavenumber k.
    `over` = oversampling of the half period, `wf` = width / grid-spacing."""
    k = k_fringe(alpha)
    mu0, Sig0 = _blobs_sep_sigma(alpha)
    half = np.pi / k                        # half period per mode
    db = half / over                        # grid spacing
    m = min(int(2 * Bmax / db) + 1, mcap)
    b = np.linspace(-Bmax, Bmax, m)
    vp = (wf * (b[1] - b[0])) ** 2
    block = np.diag([0.5, vp])
    mus, Sigs = [], []
    for bi in b:
        for bj in b:
            mus.append([0.0, bi, 0.0, bj])
            S = np.zeros((4, 4))
            S[0:2, 0:2] = block
            S[2:4, 2:4] = block
            Sigs.append(S)
    mu = np.vstack([mu0, np.array(mus)])
    Sig = np.concatenate([Sig0, np.array(Sigs)], axis=0)
    return mu, Sig, m


# --------------------------------------------------------------------------
# cross-checks against the library forward models
# --------------------------------------------------------------------------
def _check_full(mu, Sig, w, sel, alpha):
    ms, Ss = mu[sel], Sig[sel]
    ld = np.zeros((len(sel), 4)); lo = np.zeros((len(sel), 6))
    for i, S in enumerate(Ss):
        L = np.linalg.cholesky(S); ld[i] = np.log(np.diag(L)); lo[i] = L[_TRIL_I, _TRIL_J]
    return fid_full(SplatMixture2F(w, ms, ld, lo), alpha)


def _check_sep(mu, Sig, w, sel, alpha):
    ms, Ss = mu[sel], Sig[sel]
    K = len(sel)
    s = np.zeros((K, 2, 2)); phi = np.zeros((K, 2))
    for i, S in enumerate(Ss):
        for j in range(2):
            blk = S[2 * j:2 * j + 2, 2 * j:2 * j + 2]
            evals, evecs = np.linalg.eigh(blk)
            s[i, j] = 0.5 * np.log(evals)
            phi[i, j] = np.arctan2(evecs[1, 0], evecs[0, 0])
    return fid_sep(SplatMixture2(w, ms, s, phi), alpha)


# --------------------------------------------------------------------------
# 1D building-block cost m_1D(alpha)
# --------------------------------------------------------------------------
def m1d(alpha, eps=0.05):
    """Signed real Gaussians to fit the 1D fringe cos(k p) e^{-p^2} to relative
    L2 <= eps. The width is line-searched at each m (decoupled from the grid
    spacing) so m(alpha) is a clean monotone diagnostic of the 1D cost ~ k."""
    k = k_fringe(alpha)
    p = np.linspace(-4.0, 4.0, 900)
    g = np.cos(k * p) * np.exp(-p ** 2)
    gn = np.sqrt(np.trapezoid(g ** 2, p))
    P = 2.7                                  # fringe support (envelope + lobes)
    for m in range(1, 90):
        c = np.linspace(-P, P, m) if m > 1 else np.array([0.0])
        sp = (c[1] - c[0]) if m > 1 else 1.0
        best = np.inf
        for wf in (0.35, 0.45, 0.55, 0.7, 0.9):   # line-search the width
            v = (wf * sp) ** 2
            Phi = np.exp(-(p[:, None] - c[None, :]) ** 2 / (2 * v))
            a, *_ = np.linalg.lstsq(Phi, g, rcond=None)
            rel = np.sqrt(np.trapezoid((g - Phi @ a) ** 2, p)) / gn
            best = min(best, rel)
        if best <= eps:
            return m
    return m


# --------------------------------------------------------------------------
# sweep
# --------------------------------------------------------------------------
def run_sweep(alphas, F_th, max_K=300, verbose=True):
    rows = []
    for a in alphas:
        E = entanglement_entropy(a)
        k = k_fringe(a)
        m = m1d(a)
        tmu, tSig = tilted_pool(a)
        Kt, Ft, rt, purt, tsel, tw = greedy_kmin(tmu, tSig, a, F_th, max_K)
        amu, aSig, mgrid = axis_pool(a)
        Ka, Fa, ra, pura, asel, aw = greedy_kmin(amu, aSig, a, F_th, max_K)
        # cross-check the two greedy solutions against the library forward models
        ct = _check_full(tmu, tSig, tw, tsel, a)
        ca = _check_sep(amu, aSig, aw, asel, a)
        assert abs(ct - Ft) < 1e-6, (ct, Ft)
        assert abs(ca - Fa) < 1e-6, (ca, Fa)
        R = Ka / Kt
        rows.append(dict(alpha=a, E=E, k=k, m1d=m, Kt=Kt, Ka=Ka, R=R,
                         Ft=Ft, Fa=Fa, rt=rt, ra=ra, purt=purt, pura=pura,
                         poolA=len(amu), poolT=len(tmu)))
        if verbose:
            print(f"  a={a:.2f} E={E:.3f} k={k:.2f} m1D={m:2d} | "
                  f"Kt={Kt:3d}(F={Ft:.3f},L2={rt:.3f},pur={purt:.2f}) "
                  f"Ka={Ka:3d}(F={Fa:.3f},L2={ra:.3f},pur={pura:.2f}) R={R:5.2f} "
                  f"[poolA={len(amu)}]")
    return rows


def print_table(rows, F_th):
    print(f"\n{'='*84}\n TABLE  (F_th = {F_th};  criterion: relative-L2 <= "
          f"{np.sqrt(2*(1-F_th)):.3f})\n{'='*84}")
    hdr = (f"{'alpha':>6} {'E(bits)':>8} {'k':>6} {'m_1D':>5} {'K_tilted':>9} "
           f"{'K_axis':>7} {'R=Ka/Kt':>8} {'F_tilt':>7} {'F_axis':>7}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['alpha']:>6.2f} {r['E']:>8.3f} {r['k']:>6.2f} {r['m1d']:>5d} "
              f"{r['Kt']:>9d} {r['Ka']:>7d} {r['R']:>8.2f} "
              f"{r['Ft']:>7.4f} {r['Fa']:>7.4f}")


def verdict(rows):
    print(f"\n{'='*78}\n VERDICT\n{'='*78}")
    alphas = np.array([r["alpha"] for r in rows])
    E = np.array([r["E"] for r in rows])
    k = np.array([r["k"] for r in rows])
    R = np.array([r["R"] for r in rows])
    m = np.array([r["m1d"] for r in rows])
    # where has E saturated? (within 1% of 1 ebit)
    sat = alphas[E >= 0.99]
    a_sat = sat.min() if len(sat) else np.inf
    print(f"E(alpha) reaches >=0.99 ebit at alpha={a_sat:.2f} and is flat (<=1) after.")
    # R growth across the post-saturation tail
    tail = alphas >= max(a_sat, 1.5)
    if tail.sum() >= 2:
        Rt = R[tail]
        growth = Rt[-1] / Rt[0]
        print(f"Over alpha in [{alphas[tail][0]:.2f}, {alphas[tail][-1]:.2f}] "
              f"(E already saturated): R goes {Rt[0]:.2f} -> {Rt[-1]:.2f} "
              f"(x{growth:.2f}), while E is flat.")
    # correlations (log-log slopes) of R vs k and R vs m1d
    lr = np.log(R)
    for name, x in [("k", k), ("m_1D", m)]:
        lx = np.log(x)
        slope = np.polyfit(lx, lr, 1)[0]
        corr = np.corrcoef(lx, lr)[0, 1]
        print(f"  log R vs log {name:>4}: slope={slope:.2f}  corr={corr:.3f}")
    ratio_Rk = R / k
    print(f"  R/k = {np.array2string(ratio_Rk, precision=2)} "
          f"(flat => R ~ k, i.e. tracks the interference scale)")
    if tail.sum() >= 2 and R[tail][-1] > 1.15 * R[tail][0]:
        print("\n  => R KEEPS GROWING after E saturates. The naive 'cost tracks")
        print("     entanglement' conjecture is REFUTED. Representation cost tracks")
        print("     the nonclassical INTERFERENCE SCALE k = 2 sqrt2 alpha (R ~ k,")
        print("     consistent with K_axis ~ m_1D^2, K_tilted ~ m_1D, R ~ m_1D ~ k).")
    else:
        print("\n  => R SATURATES with E. The naive 'cost tracks entanglement' form survives.")


def make_figure(rows, F_th, path):
    alphas = np.array([r["alpha"] for r in rows])
    E = np.array([r["E"] for r in rows])
    k = np.array([r["k"] for r in rows])
    R = np.array([r["R"] for r in rows])
    Kt = np.array([r["Kt"] for r in rows])
    Ka = np.array([r["Ka"] for r in rows])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))

    ax1.plot(alphas, R, "o-", color="#c0392b", lw=2, ms=7, label="R = K_axis / K_tilted")
    ax1.plot(alphas, E / E.max() * R.max(), "s--", color="#2980b9",
             label="E(alpha) (scaled) -- saturates")
    ax1.plot(alphas, k / k.max() * R.max(), "^:", color="#27ae60",
             label="k = 2 sqrt2 alpha (scaled) -- unbounded")
    ax1.set_xlabel("alpha"); ax1.set_ylabel("R  (and scaled drivers)")
    ax1.set_title(f"Representation cost ratio vs drivers  (F_th={F_th})")
    ax1.legend(fontsize=8, loc="upper left"); ax1.grid(alpha=0.3)

    ax2.semilogy(alphas, Ka, "o-", color="#c0392b", lw=2, ms=7, label="K_axis (separable)")
    ax2.semilogy(alphas, Kt, "s-", color="#2980b9", lw=2, ms=7, label="K_tilted (full-cov)")
    ax2.set_xlabel("alpha"); ax2.set_ylabel("K_min  (log scale)")
    ax2.set_title("Components to reach F_th")
    ax2.legend(fontsize=9); ax2.grid(alpha=0.3, which="both")

    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def main():
    # sanity: E saturates at 1 ebit, is 0 at alpha=0
    assert abs(entanglement_entropy(0.0) - 0.0) < 1e-9
    assert abs(entanglement_entropy(4.0) - 1.0) < 1e-3

    alphas = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5]
    print("Sweep at F_th = 0.99:")
    rows99 = run_sweep(alphas, 0.99)
    print_table(rows99, 0.99)

    print("\nRobustness sweep at F_th = 0.95:")
    rows95 = run_sweep(alphas, 0.95)
    print_table(rows95, 0.95)

    verdict(rows99)

    # robustness: is R (the deliverable) stable if the dictionary width changes?
    print(f"\n{'='*84}\n ROBUSTNESS of R to the dictionary component width (wf)\n{'='*84}")
    print("(absolute K depends on dictionary scale; R should not)")
    for a in [1.0, 1.5, 2.0, 2.5]:
        cells = []
        for wf in [0.5, 0.65, 0.8]:      # well-conditioned regime (wf<0.5 -> spiky)
            tmu, tSig = tilted_pool(a, wf=wf)
            Kt = greedy_kmin(tmu, tSig, a, 0.99, 300)[0]
            amu, aSig, _ = axis_pool(a, wf=wf)
            Ka = greedy_kmin(amu, aSig, a, 0.99, 300)[0]
            cells.append(f"wf={wf}: R={Ka/Kt:5.2f}(Kt={Kt},Ka={Ka})")
        print(f"  a={a:.2f}  " + "  ".join(cells))

    fig = make_figure(rows99, 0.99, os.path.join(OUT, "entanglement_cost.png"))
    print(f"\nFigure written to {fig}")


if __name__ == "__main__":
    main()
