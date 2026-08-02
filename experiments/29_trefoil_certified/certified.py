"""Experiment 29 certified evaluator (derivation.md §1, §3, §4, E1-E2).

Every constant is traced to exact rational enclosures (E1, `fractions`
arithmetic — no floats in the proofs) and combined by the monotone-factor
rules of derivation.md §3-§4. Transcendental steps (sin, cos, asin, sqrt,
exp) are evaluated in float and nudged outward by the declared SLOP, in
the direction that weakens the bound (lower bounds rounded down, upper
bounds rounded up), so every reported margin is safe up to SLOP-level
float error. No epistemic status is authored here (derivation.md §8 is
the sole authoring location).
"""

from __future__ import annotations

import math
from fractions import Fraction

# declared outward-rounding slop for transcendental float steps
SLOP = 1e-9

# exact squares of the target constants (derivation.md §1)
A_SQ = Fraction(8, 25)
B_SQ = Fraction(3, 50)


def _dn(x):
    """Round a float down by the declared slop (safe lower bound)."""
    return x - SLOP * max(1.0, abs(x))


def _up(x):
    """Round a float up by the declared slop (safe upper bound)."""
    return x + SLOP * max(1.0, abs(x))


# ---------------------------------------------------------------------------
# E1: exact rational enclosures
# ---------------------------------------------------------------------------

def sqrt_enclosure(square: Fraction, digits=8):
    """Rational [lo, hi] with lo^2 < square < hi^2, proven exactly."""
    scale = 10**digits
    lo_int = int(math.isqrt(square.numerator * scale * scale // square.denominator))
    lo = Fraction(lo_int, scale)
    hi = Fraction(lo_int + 2, scale)
    # exact proofs; widen if the float seed was off
    while lo * lo >= square:
        lo -= Fraction(1, scale)
    while hi * hi <= square:
        hi += Fraction(1, scale)
    assert lo * lo < square < hi * hi
    return lo, hi


A_LO, A_HI = sqrt_enclosure(A_SQ)
B_LO, B_HI = sqrt_enclosure(B_SQ)


def cubic_sign_bounds(s: Fraction):
    """Exact bounds on p(s) = b s^3 + a s^2 - a over the a, b enclosures.

    p is increasing in b and in a-multiplied terms with mixed signs, so
    bound term-wise: lower uses (b_lo, a_lo s^2, -a_hi), upper the flips.
    """
    lower = B_LO * s**3 + A_LO * s * s - A_HI
    upper = B_HI * s**3 + A_HI * s * s - A_LO
    return lower, upper


def s_star_enclosure(width=Fraction(1, 10**7)):
    """Certified bracket of the unique root s* in (0, 1) of the cubic
    (increasing there), by exact-sign bisection."""
    lo, hi = Fraction(1, 2), Fraction(99, 100)
    _, up0 = cubic_sign_bounds(lo)
    lo0, _ = cubic_sign_bounds(hi)
    assert up0 < 0 < lo0, "initial bracket failed its exact sign checks"
    while hi - lo > width:
        mid = (lo + hi) / 2
        low_b, up_b = cubic_sign_bounds(mid)
        if up_b < 0:
            lo = mid
        elif low_b > 0:
            hi = mid
        else:
            break  # sign indeterminate at this width; stop refining
    return lo, hi


def enclosures():
    """All E1 enclosures as floats with outward rounding, plus the exact
    fractions (stringified) for the artifact."""
    s_lo_f, s_hi_f = s_star_enclosure()
    th_lo = _dn(math.asin(float(s_lo_f)))
    th_hi = _up(math.asin(float(s_hi_f)))
    return {
        "a": (_dn(float(A_LO)), _up(float(A_HI))),
        "b": (_dn(float(B_LO)), _up(float(B_HI))),
        "s_star": (_dn(float(s_lo_f)), _up(float(s_hi_f))),
        "s_star_exact": (str(s_lo_f), str(s_hi_f)),
        "a_exact": (str(A_LO), str(A_HI)),
        "b_exact": (str(B_LO), str(B_HI)),
        "theta_star": (th_lo, th_hi),
    }


# ---------------------------------------------------------------------------
# W2: certified clearance (derivation.md §3)
# ---------------------------------------------------------------------------

# declared band B with rational endpoints (radians)
THETA_LO_B = 0.9
THETA_HI_B = 1.15


def band_check(enc):
    """Certified `theta* in B` via monotone sin: sin(theta_lo_B) < s*_lo
    and s*_hi < sin(theta_hi_B), with outward-rounded float sin."""
    return (
        _up(math.sin(THETA_LO_B)) < enc["s_star"][0]
        and enc["s_star"][1] < _dn(math.sin(THETA_HI_B))
    )


def w2_constants(enc):
    a_lo, a_hi = enc["a"]
    b_lo, b_hi = enc["b"]
    th_lo, th_hi = enc["theta_star"]
    # |g1| at the band endpoints, safely rounded down
    g1_at_lo = _dn(
        a_lo * _dn(math.cos(THETA_LO_B)) ** 2
        - b_hi * _up(math.sin(THETA_LO_B)) ** 3
    )
    g1_at_hi = _dn(
        b_lo * _dn(math.sin(THETA_HI_B)) ** 3
        - a_hi * _up(math.cos(THETA_HI_B)) ** 2
    )
    m_band = min(g1_at_lo, g1_at_hi)
    sc_lo_end = _dn(math.sin(THETA_LO_B) * math.cos(THETA_LO_B))
    sc_hi_end = _dn(math.sin(THETA_HI_B) * math.cos(THETA_HI_B))
    lam_b = min(sc_lo_end, sc_hi_end) * _dn(
        2.0 * a_lo + 3.0 * b_lo * _dn(math.sin(THETA_LO_B))
    )
    kap_b = _dn(
        4.0
        * a_lo
        * b_lo
        * _dn(math.cos(THETA_HI_B)) ** 2
        * _dn(math.sin(THETA_LO_B)) ** 3
    )
    # G lower bound: largest c* and s* on the theta* enclosure
    c_max = _up(math.cos(th_lo))
    s_max = _up(math.sin(th_hi))
    g_lower = _dn(math.sqrt(4.0 / (c_max * c_max) + 9.0 / (s_max * s_max)))
    return {
        "m_band": m_band,
        "lam_B": lam_b,
        "kap_B": kap_b,
        "G_lower": g_lower,
    }


def m_cert(rho, w2):
    pi_up = _up(math.pi)
    return min(
        w2["m_band"],
        w2["lam_B"] * rho / 2.0,
        _dn(math.sqrt(max(0.0, w2["kap_B"]))) * w2["G_lower"] * rho / (2.0 * pi_up),
    )


# ---------------------------------------------------------------------------
# W3: certified transversality (derivation.md §4)
# ---------------------------------------------------------------------------

def sigma_cert(rho, enc):
    a_lo, a_hi = enc["a"]
    b_lo, b_hi = enc["b"]
    th_lo, th_hi = enc["theta_star"]
    theta_minus = th_lo - rho
    theta_plus = th_hi + rho
    if theta_minus <= 0.0 or theta_plus >= math.pi / 2.0:
        return 0.0
    cos_plus = _dn(math.cos(theta_plus))
    sin_minus = _dn(math.sin(theta_minus))
    d2_min = _dn(
        4.0 * a_lo * a_lo * cos_plus * cos_plus
        + 9.0 * b_lo * b_lo * sin_minus**4
    )
    gbar_sq = _up(
        4.0 / (cos_plus * cos_plus) + 9.0 / (sin_minus * sin_minus)
    )
    lam_up = _up(a_hi + 1.5 * b_hi)
    cos_minus_sq_up = _up(math.cos(theta_minus)) ** 2
    m_f = rho * _up(
        math.sqrt(lam_up * lam_up + a_hi * b_hi * cos_minus_sq_up * gbar_sq)
    )
    e_max = _up(3.0 * m_f + a_hi * cos_minus_sq_up)
    return _dn(math.sqrt(max(0.0, d2_min - e_max * e_max)))


# ---------------------------------------------------------------------------
# E2: the certified radius (eps0_cert semantics of exp28 §3)
# ---------------------------------------------------------------------------

def c1(h):
    """exp28 S2 constant, rounded up (it sits in a denominator)."""
    return _up(math.sqrt(2.0) * math.exp((1.0 + h) ** 2 / 2.0) / h)


def rho_cap(enc):
    """W0 core-disjointness constraint: rho < min(theta*, pi/2 - theta*)."""
    th_lo, th_hi = enc["theta_star"]
    return min(th_lo, math.pi / 2.0 - th_hi)


def eps29_cert(rho_list, h_list, enc, w2):
    cap = rho_cap(enc)
    best = (0.0, None, None, None, None)
    rows = []
    for rho in rho_list:
        if rho >= cap:
            rows.append({"rho": rho, "admissible": False})
            continue
        m_r = m_cert(rho, w2)
        s_r = sigma_cert(rho, enc)
        rows.append(
            {"rho": rho, "admissible": True, "m_cert": m_r, "sigma_cert": s_r}
        )
        if m_r <= 0.0 or s_r <= 0.0:
            continue
        branch_a = m_r * _dn(math.exp(-0.5))
        for h in h_list:
            val = min(branch_a, s_r / c1(h))
            if val > best[0]:
                best = (val, rho, float(h), m_r, s_r)
    return best, rows


def fidelity_bound(eps):
    return (1.0 - eps * eps / 2.0) ** 2
