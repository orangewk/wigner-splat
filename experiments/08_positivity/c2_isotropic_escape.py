"""Issue #6 / C2: is the isotropic-diagonal "escape" a real counterexample?

An oracle review proposed that K_axis = Omega(m_1D^2) is FALSE because a
common-width product Gaussian with equal x/y width is ISOTROPIC (rotation
invariant); placed on the diagonal v=0 it resolves the rotated fringe
F_k = e^{-u^2-v^2}cos(sqrt2 k u) in 1D, giving O(m_1D) atoms.

This script checks whether that escape survives a BOUNDED-COEFFICIENT constraint
(the regime experiment 05 actually measures via its spike-proof relative-L2
criterion). Result: it does NOT. With |c| <= 50 the diagonal-isotropic fit never
reaches rel-L2 <= 0.14; where it approaches, the weights blow up like ~e^{k^2}
(max|c| = 1e5..1e9). So the escape is only the ill-conditioned regime, and the
Omega(m_1D^2) axis penalty (C2) stands once bounded atomic norm is imposed.
"""
import numpy as np


def diagonal_isotropic_fit(k, s, n, L=3.5, N=140):
    """Least-squares fit of F_k by n isotropic width-s Gaussians on the diagonal.

    Returns (relative_L2, max_abs_coefficient).
    """
    xs = np.linspace(-L, L, N)
    X, Y = np.meshgrid(xs, xs)
    F = np.exp(-X ** 2 - Y ** 2) * np.cos(k * (X + Y))
    Fn = np.sqrt(np.mean(F ** 2))
    P = 2.7 / np.sqrt(2)                      # diagonal span (u-support / sqrt2)
    a = np.linspace(-P, P, n)
    Phi = np.stack(
        [np.exp(-((X - ai) ** 2 + (Y - ai) ** 2) / (2 * s ** 2)) for ai in a],
        axis=0,
    ).reshape(n, -1).T
    c, *_ = np.linalg.lstsq(Phi, F.ravel(), rcond=None)
    rel = np.sqrt(np.mean((Phi @ c - F.ravel()) ** 2)) / Fn
    return rel, float(np.max(np.abs(c)))


def main():
    widths = [0.15, 0.25, 0.4, 0.6, 0.9, 1.2]
    counts = [8, 12, 16, 20, 30, 45, 60]
    coeff_cap = 50.0
    for k in (4.0, 6.0, 8.0):
        print(f"--- k={k:g}  (1D needs ~{1.7 * k + 2.3:.0f} atoms) ---")
        best = None
        for s in widths:
            for n in counts:
                rel, cmax = diagonal_isotropic_fit(k, s, n)
                if rel <= 0.14 and cmax <= coeff_cap and (best is None or n < best[0]):
                    best = (n, s, rel, cmax)
        print(f"  bounded-coeff (|c|<={coeff_cap:g}) diagonal reaches rel<=0.14 at: {best}")
        for s in (0.25, 0.6, 1.2):
            rel, cmax = diagonal_isotropic_fit(k, s, 60)
            print(f"    s={s:g}: n=60 -> rel={rel:.3f}  max|c|={cmax:.1e}")


if __name__ == "__main__":
    main()
