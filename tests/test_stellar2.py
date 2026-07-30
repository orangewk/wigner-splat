"""Tests for wigner_splat/stellar2.py against the proved rows of
experiments/24_hopf_stellar/derivation.md (P1-P4b) plus tool calibration.

These are the F1 falsification gates of the derivation memo: each assertion
below is a *proved* prediction, so a failure here means the tracker (or a
proof) is broken, and experiment 24 results are not interpretable.
"""

import math

import numpy as np
import pytest

from wigner_splat.stellar2 import (
    TraceError,
    census,
    coherent_term,
    fock_stellar,
    gaussian_sum_stellar,
    linking_number,
    tmsv_term,
    _pick_pole,
    _stereographic,
)


def _circle4(fn, n=200):
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)
    return np.stack(fn(t), axis=1)


def test_linking_calibration():
    """Pins the global sign convention: standard positively oriented Hopf
    pair (e^{it}, 0), (0, e^{is}) measures +1, from several poles."""
    c1 = _circle4(lambda t: (np.cos(t), np.sin(t), 0 * t, 0 * t))
    c2 = _circle4(lambda t: (0 * t, 0 * t, np.cos(t), np.sin(t)))
    rng = np.random.default_rng(7)
    seen = set()
    checked = 0
    for k in range(20):
        p = rng.normal(size=4)
        p /= np.linalg.norm(p)
        d = min(
            np.min(np.linalg.norm(c1 - p, axis=1)),
            np.min(np.linalg.norm(c2 - p, axis=1)),
        )
        if d < 0.3:
            continue
        seen.add(linking_number(_stereographic(c1, p), _stereographic(c2, p), seed=k))
        checked += 1
    assert checked >= 5
    assert seen == {1}


def test_linking_unlinked_circles():
    t = np.linspace(0, 2 * math.pi, 150, endpoint=False)
    a = np.stack([np.cos(t), np.sin(t), 0 * t], axis=1)
    b = np.stack([np.cos(t) + 3.0, np.sin(t), 0 * t + 0.5], axis=1)
    assert linking_number(a, b, seed=0) == 0


def test_fock_stellar_values():
    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    f = fock_stellar(c)
    w1 = np.array([0.3 + 0.1j, -0.2j])
    w2 = np.array([0.5 - 0.4j, 0.7])
    assert np.allclose(f(w1, w2), w1 * w2)

    # TMSV stellar function equals its Fock series
    lam = 0.55
    cutoff = 40
    c = np.zeros((cutoff, cutoff), dtype=complex)
    for n in range(cutoff):
        c[n, n] = math.sqrt(1 - lam**2) * lam**n
    series = fock_stellar(c)
    closed = gaussian_sum_stellar([tmsv_term(lam)])
    assert np.allclose(series(w1, w2), closed(w1, w2))


def _winding_set(res):
    return {tuple(w) for w in (c["windings"] for c in res["components"])}


def test_census_11_is_hopf_link_and_frame_invariant():
    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    f = fock_stellar(c)
    results = [
        census(f, n_eta=60, n_xi=64, frame_seed=seed) for seed in (0, 100)
    ]
    for res in results:
        assert len(res["components"]) == 2
        assert _winding_set(res) == {(1, None), (None, 1)}
        assert res["linking_matrix"][0][1] == 1
        assert res["diagnostics"]["caps_clear"]


def test_census_superposition_single_fiber():
    c = np.zeros((2, 2), dtype=complex)
    c[1, 0] = 1.0
    c[0, 1] = 1.0
    res = census(fock_stellar(c), n_eta=60, n_xi=64)
    assert len(res["components"]) == 1
    assert res["components"][0]["windings"] == [1, 1]


def test_census_2002_hopf_pair():
    c = np.zeros((3, 3), dtype=complex)
    c[2, 0] = 1.0
    c[0, 2] = 1.0
    res = census(fock_stellar(c), n_eta=60, n_xi=64)
    assert len(res["components"]) == 2
    assert res["linking_matrix"][0][1] == 1  # same sign as the |11> link


def test_census_trefoil_windings():
    c = np.zeros((3, 4), dtype=complex)
    c[2, 0] = 0.8
    c[0, 3] = 0.6
    res = census(fock_stellar(c), n_eta=72, n_xi=80)
    assert len(res["components"]) == 1
    assert sorted(res["components"][0]["windings"]) == [2, 3]


def test_census_3003_three_chain():
    c = np.zeros((4, 4), dtype=complex)
    c[3, 0] = 1.0
    c[0, 3] = 1.0
    res = census(fock_stellar(c), n_eta=72, n_xi=80)
    assert len(res["components"]) == 3
    lk = np.array(res["linking_matrix"])
    assert np.all(lk[np.triu_indices(3, k=1)] == 1)


def test_tmsv_odd_cat_exact_hopf_link_and_fidelity():
    lam = 0.6
    f = gaussian_sum_stellar([tmsv_term(lam), tmsv_term(-lam, z=-1.0)])
    res = census(f, n_eta=60, n_xi=64)
    assert len(res["components"]) == 2
    assert _winding_set(res) == {(1, None), (None, 1)}
    assert res["linking_matrix"][0][1] == 1

    # independent Fock-truncation check of F(C(lam), |11>) = 1 - lam^4
    n = np.arange(1, 80, 2)  # odd cat keeps odd |n,n>
    coeffs = lam**n
    fid = coeffs[0] ** 2 / np.sum(coeffs**2)
    assert math.isclose(fid, 1 - lam**4, rel_tol=1e-12)


def test_generic_tmsv_cat_conic_pair_signs():
    """P4b: smooth conic pair, windings (+1,-1)/(-1,+1), linking +1."""
    lam = 0.85
    f = gaussian_sum_stellar(
        [tmsv_term(lam), tmsv_term(-lam, z=-np.exp(0.35j))]
    )
    res = census(f, n_eta=72, n_xi=80)
    assert len(res["components"]) == 2
    assert _winding_set(res) == {(-1, 1), (1, -1)}
    assert res["linking_matrix"][0][1] == 1


def test_coherent_cat_parallel_lines_unlinked():
    """P3: coherent K=2 zero circles are pairwise unlinked."""
    g = 4.0 / math.sqrt(2)
    f = gaussian_sum_stellar(
        [coherent_term(g, g), coherent_term(-g, -g, z=-1.0)]
    )
    res = census(f, n_eta=72, n_xi=80)
    assert len(res["components"]) == 3
    lk = np.array(res["linking_matrix"])
    assert np.all(lk == 0)


def test_gaussian_stellar_rejects_bad_input():
    with pytest.raises(ValueError):
        gaussian_sum_stellar([])
    with pytest.raises(ValueError):
        tmsv_term(1.0)


def test_pick_pole_avoids_curves():
    t = np.linspace(0, 2 * math.pi, 64, endpoint=False)
    c1 = _circle4(lambda t: (np.cos(t), np.sin(t), 0 * t, 0 * t), n=64)
    pole = _pick_pole([c1], seed=0)
    assert np.min(np.linalg.norm(c1 - pole, axis=1)) > 0.1
