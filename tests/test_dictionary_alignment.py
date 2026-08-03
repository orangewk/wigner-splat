"""Referee tests for experiment 30 (dictionary alignment).

Independent re-proofs and pins for derivation.md's A1/A5 closed forms
and the E-series contracts. No epistemic status is asserted here beyond
what each test's own arithmetic establishes.
"""

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments" / "30_dictionary_alignment"))

import alignment  # noqa: E402
from wigner_splat import gaussact  # noqa: E402


def _random_symmetric(rng, norm_cap=0.9):
    M = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    A = (M + M.T) / 2.0
    s = np.linalg.norm(A, 2)
    return A * (norm_cap * rng.uniform(0.1, 1.0) / s)


def test_takagi_reconstructs_random_symmetric_matrices():
    rng = np.random.default_rng(7)
    for _ in range(50):
        A = _random_symmetric(rng)
        V, s = alignment.takagi(A)
        assert np.linalg.norm(V @ V.conj().T - np.eye(2)) < 1e-10
        assert np.linalg.norm(V @ np.diag(s) @ V.T - A) < 1e-10
        assert s[0] >= s[1] >= 0.0


def test_takagi_handles_degenerate_and_diagonal_cases():
    for A in (
        np.diag([0.5, 0.5]).astype(complex),
        np.diag([0.3, 0.0]).astype(complex),
        np.zeros((2, 2), dtype=complex),
        0.4 * np.exp(0.7j) * np.array([[0.0, 1.0], [1.0, 0.0]]),
    ):
        V, s = alignment.takagi(A)
        assert np.linalg.norm(V @ np.diag(s) @ V.T - A) < 1e-10


def test_alpha_b_maps_are_mutually_inverse_and_sandwiched():
    rng = np.random.default_rng(11)
    for _ in range(50):
        A = _random_symmetric(rng)
        alpha = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        b = alignment.b_from_alpha(A, alpha)
        back = alignment.alpha_from_b(A, b)
        assert np.linalg.norm(back - alpha) < 1e-10
        an = np.linalg.norm(A, 2)
        assert (1 - an) * np.linalg.norm(alpha) - 1e-12 <= np.linalg.norm(b)
        assert np.linalg.norm(b) <= (1 + an) * np.linalg.norm(alpha) + 1e-12


def test_recipe_state_matches_gaussact_chain():
    vac = gaussact.pq_state(np.array([[1.0 + 0j]]))
    for seed in (0, 3):
        params = gaussact.random_gauss_params(seed, r_max=0.6, alpha_max=0.8)
        chain = gaussact.gauss_unitary(vac, params)
        assert chain.P.shape == (1, 1)
        recipe = alignment.recipe_state(chain.A, chain.b)
        c1 = gaussact.fock_coeffs(chain, 22).ravel()
        c2 = gaussact.fock_coeffs(recipe, 22).ravel()
        c1 /= np.linalg.norm(c1)
        c2 /= np.linalg.norm(c2)
        ip = complex(np.vdot(c2, c1))
        assert abs(ip) > 0
        assert np.linalg.norm(c1 - (ip / abs(ip)) * c2) < 1e-9


def _independent_taylor(A, b, cutoff):
    """Independent Taylor recursion for exp(w^T A w / 2 + b^T w):
    (m+1) t_{m+1,n} = A11 t_{m-1,n} + A12 t_{m,n-1} + b1 t_{m,n} (and
    symmetrically in n), a different code path from gaussact's
    stellar2-based coefficient generator."""
    t = np.zeros((cutoff, cutoff), dtype=complex)
    t[0, 0] = 1.0
    for m in range(cutoff):
        for n in range(cutoff):
            if m == 0 and n == 0:
                continue
            if m > 0:
                acc = b[0] * t[m - 1, n]
                if m > 1:
                    acc += A[0, 0] * t[m - 2, n]
                if n > 0:
                    acc += A[0, 1] * t[m - 1, n - 1]
                t[m, n] = acc / m
            else:
                acc = b[1] * t[0, n - 1]
                if n > 1:
                    acc += A[1, 1] * t[0, n - 2]
                t[0, n] = acc / n
    root = np.sqrt([math.factorial(k) for k in range(cutoff)])
    return t * np.outer(root, root)


def test_gaussact_fock_coeffs_match_independent_recursion():
    rng = np.random.default_rng(23)
    for _ in range(5):
        A = _random_symmetric(rng, norm_cap=0.7)
        b = 0.5 * (rng.standard_normal(2) + 1j * rng.standard_normal(2))
        st = gaussact.pq_state(np.array([[1.0 + 0j]]), A, b)
        c1 = gaussact.fock_coeffs(st, 18)
        c2 = _independent_taylor(A, b, 18)
        assert np.max(np.abs(c1 - c2)) < 1e-9


def test_norm_closed_form_bracketed_by_partials():
    for s1, s2 in ((0.5, 0.7), (0.9, 0.3)):
        st = gaussact.pq_state(
            np.array([[1.0 + 0j]]), np.diag([s1, s2]).astype(complex)
        )
        c = gaussact.fock_coeffs(st, 60)
        t1 = np.abs(c[0::2, 0]) ** 2
        t2 = np.abs(c[0, 0::2]) ** 2
        p1, p2 = float(np.sum(t1)), float(np.sum(t2))
        u1 = p1 + alignment.mode_tail_bound(float(t1[-1]), s1)
        u2 = p2 + alignment.mode_tail_bound(float(t2[-1]), s2)
        closed = alignment.norm_sq_closed(s1, s2)
        # declared relative float slack (derivation.md §7 E2 note)
        assert p1 * p2 <= closed * (1.0 + 1e-12)
        assert closed <= u1 * u2 * (1.0 + 1e-12)


def test_one_mode_norm_series_identity_in_exact_arithmetic():
    """Re-proof of A1(iii)'s series sum on a rational sigma: the partial
    sums of C(2n,n) (sigma^2/4)^n approach (1-sigma^2)^{-1/2} from below,
    verified against the squared closed form in Fractions."""
    sigma_sq = Fraction(1, 4)  # sigma = 1/2
    target_sq = 1 / (1 - sigma_sq)  # closed form squared: 4/3
    partial = Fraction(0)
    for n in range(200):
        partial += Fraction(math.comb(2 * n, n), 4**n) * sigma_sq**n
        assert partial * partial <= target_sq
    assert target_sq - partial * partial < Fraction(1, 10**20)


def test_conversion_identities_and_outward_helpers():
    for k in range(1, 50):
        d2 = Fraction(k, 50)
        F = alignment.fidelity_of_delta_sq(d2)
        assert alignment.delta_sq_of_fidelity(F) == d2
        Fsq = d2**2
        assert alignment.fidelity_of_delta_sq(
            alignment.delta_sq_of_fidelity(Fsq)
        ) == Fsq
    exact = Fraction(1, 3)
    assert Fraction(alignment.float_down(exact)) <= exact
    assert Fraction(alignment.float_up(exact)) >= exact
    with pytest.raises(ValueError):
        alignment.delta_sq_of_fidelity(Fraction(1, 2))


def test_e3_rederivation_pins_one_committed_cell():
    """Rebuild trefoil/gaussian/K=2 from `best_params` alone and reproduce
    the committed best_fidelity through exp25's own estimator (Gram +
    pinv projection). Also pins the committed `coeffs_z` semantics: it is
    the census-stage z divided by each atom's raw Fock norm."""
    art = ROOT / "experiments" / "25_topological_kcurves" / "topological_kcurves.json"
    exp25 = json.loads(art.read_text(encoding="utf-8"))
    cutoff = int(exp25["cutoff"])
    cell = exp25["cells"]["trefoil/gaussian/K=2"]
    x = np.asarray(cell["best_params"], dtype=float).reshape(-1, 10)
    box = float(exp25["bounded_dictionary"]["quad_norm_max"])
    vecs, norms = [], []
    for row in x:
        A = np.array([
            [2 * (row[4] + 1j * row[5]), row[6] + 1j * row[7]],
            [row[6] + 1j * row[7], 2 * (row[8] + 1j * row[9])],
        ])
        assert np.linalg.norm(A, 2) <= box
        st = gaussact.pq_state(
            np.array([[1.0 + 0j]]), A,
            np.array([row[0] + 1j * row[1], row[2] + 1j * row[3]]),
        )
        v = gaussact.fock_coeffs(st, cutoff).ravel()
        norms.append(float(np.linalg.norm(v)))
        vecs.append(v / np.linalg.norm(v))
    vecs = np.array(vecs)
    t = np.zeros((cutoff, cutoff), dtype=complex)
    t[2, 0], t[0, 3] = 0.8, 0.6
    gram = np.conj(vecs) @ vecs.T
    h = np.conj(vecs) @ t.ravel()
    z = np.linalg.pinv(gram, rcond=1e-12, hermitian=True) @ h
    fre = float(np.real(np.conj(h) @ z))
    assert abs(fre - float(cell["best_fidelity"])) < 1e-6
    z_census = np.array([complex(re, im) for re, im in cell["coeffs_z"]])
    assert np.max(np.abs(z / np.array(norms) - z_census)) < 1e-6 * np.max(
        np.abs(z_census)
    )


def test_common_quadratic_factor_divides_out():
    """A3's division identity on data: a 2-term common-quadratic state's
    stellar function equals exp(common) * (coherent 2-term), checked
    pointwise on a w-grid."""
    A0 = np.array([[0.3, 0.1j], [0.1j, -0.2 + 0.1j]])
    b1 = np.array([0.4 + 0.2j, -0.1])
    b2 = np.array([-0.3, 0.5j])
    z1, z2 = 1.0 + 0.5j, -0.7
    f1 = gaussact.stellar_callable(gaussact.pq_state(np.array([[z1]]), A0, b1))
    f2 = gaussact.stellar_callable(gaussact.pq_state(np.array([[z2]]), A0, b2))
    rng = np.random.default_rng(5)
    w = rng.standard_normal((2, 40)) + 1j * rng.standard_normal((2, 40))
    total = f1(w[0], w[1]) + f2(w[0], w[1])
    quad = np.exp(
        0.5 * (A0[0, 0] * w[0] ** 2 + 2 * A0[0, 1] * w[0] * w[1]
               + A0[1, 1] * w[1] ** 2)
    )
    coh = z1 * np.exp(b1[0] * w[0] + b1[1] * w[1]) + z2 * np.exp(
        b2[0] * w[0] + b2[1] * w[1]
    )
    assert np.max(np.abs(total - quad * coh)) < 1e-9 * np.max(np.abs(total))


def test_claim_registry_parses_all_declared_ids():
    sys.path.insert(0, str(ROOT / "experiments" / "30_dictionary_alignment"))
    import summary_block

    reg = summary_block.load_claim_registry()
    assert set(reg) == set(summary_block.CLAIM_IDS)
    for row in reg.values():
        assert row["status"]
        assert row["basis"]


def test_committed_exp28_exp29_bounds_are_outward():
    """A5/E4 discipline cross-check: the committed fidelity bounds sit at
    or above the exact (1 - eps^2/2)^2 of their committed radii."""
    for art, radius_key in (
        ("28_isotopy_stability/isotopy_stability.json", "eps0_cert"),
        ("29_trefoil_certified/trefoil_certified.json", "eps29_cert"),
    ):
        d = json.loads((ROOT / "experiments" / art).read_text(encoding="utf-8"))
        eps = Fraction(d["E2"][radius_key])
        assert Fraction(d["E2"]["fidelity_bound"]) >= (1 - eps**2 / 2) ** 2
