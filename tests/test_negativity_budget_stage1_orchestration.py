"""Synthetic gates for the canonical Stage 1 cell registry."""

from __future__ import annotations

from dataclasses import fields, replace
from importlib import import_module

import numpy as np
import pytest


orchestration = import_module(
    "experiments.33_negativity_budget.stage1_orchestration"
)
stage1_setup = import_module(
    "experiments.33_negativity_budget.stage1_setup"
)


def _source_groups(sample_count=10):
    return [
        (
            np.deg2rad(degrees),
            np.linspace(-2.0, 2.0, sample_count) + group_index / 10.0,
        )
        for group_index, degrees in enumerate(
            orchestration.MEASUREMENT_DEGREES
        )
    ]


def _independent_train(source, reshuffle_seed, generator_factory):
    generator = generator_factory(reshuffle_seed)
    return tuple(
        samples[
            generator.permutation(len(samples))[
                : int(orchestration.TRAIN_FRACTION * len(samples))
            ]
        ]
        for _theta, samples in source
    )


def test_declared_cell_registries_have_exact_membership_and_order():
    identities = orchestration.stage1_cell_identities()
    expected = tuple(
        (
            orchestration.DATASET_ID,
            reshuffle_seed,
            beta,
            init_seed,
        )
        for reshuffle_seed in (0, 1)
        for beta in (0.0, 0.02, 0.05, 0.1, 0.2, 0.4)
        for init_seed in (0, 1, 2)
    )
    observed = tuple(
        (
            identity.dataset_id,
            identity.reshuffle_seed,
            identity.beta,
            identity.init_seed,
        )
        for identity in identities
    )
    assert observed == expected
    assert len(identities) == len(set(identities)) == 36

    barrier = orchestration.barrier_selection_identities()
    assert len(barrier) == 30
    assert barrier == tuple(identity for identity in identities if identity.beta)


def test_prepare_cells_matches_independent_pcg64_train_split():
    source = _source_groups()
    assert orchestration.BIT_GENERATOR is np.random.PCG64
    cells = orchestration.prepare_stage1_cells(source)
    assert tuple(cell.identity for cell in cells) == (
        orchestration.stage1_cell_identities()
    )
    assert len({id(cell.setup) for cell in cells}) == 36

    for reshuffle_seed in orchestration.RESHUFFLE_SEEDS:
        expected_pcg64 = _independent_train(
            source,
            reshuffle_seed,
            lambda seed: np.random.Generator(np.random.PCG64(seed)),
        )
        expected_exp18 = _independent_train(
            source, reshuffle_seed, np.random.default_rng
        )
        for pcg64, exp18 in zip(expected_pcg64, expected_exp18, strict=True):
            np.testing.assert_array_equal(pcg64, exp18)
        representative = next(
            cell
            for cell in cells
            if cell.identity.reshuffle_seed == reshuffle_seed
            and cell.identity.beta == 0.0
            and cell.identity.init_seed == 0
        )
        for group_index, expected in enumerate(expected_exp18):
            np.testing.assert_array_equal(
                representative.setup.train_groups[group_index][1][:, 0],
                expected,
            )

    source[0][1][:] = 999.0
    assert not np.all(cells[0].setup.train_groups[0][1] == 999.0)


def test_barrier_view_requires_complete_canonical_registry():
    cells = orchestration.prepare_stage1_cells(_source_groups())
    barrier = orchestration.barrier_selection_cells(cells)
    assert len(barrier) == 30
    assert tuple(cell.identity for cell in barrier) == (
        orchestration.barrier_selection_identities()
    )
    assert all(cell.identity.beta > 0.0 for cell in barrier)

    with pytest.raises(ValueError, match="declared Stage 1 registry"):
        orchestration.barrier_selection_cells(cells[:-1])
    with pytest.raises(ValueError, match="declared Stage 1 registry"):
        orchestration.barrier_selection_cells(tuple(reversed(cells)))
    with pytest.raises(TypeError, match="Stage1CandidateCell"):
        orchestration.barrier_selection_cells([object()])

    duplicate_setup = list(cells)
    first = cells[0]
    matching_other_reshuffle = next(
        cell
        for cell in cells
        if cell.identity.reshuffle_seed == 1
        and cell.identity.beta == first.identity.beta
        and cell.identity.init_seed == first.identity.init_seed
    )
    other_index = next(
        index
        for index, cell in enumerate(cells)
        if cell is matching_other_reshuffle
    )
    duplicate_setup[other_index] = replace(
        matching_other_reshuffle, setup=first.setup
    )
    with pytest.raises(ValueError, match="distinct setup"):
        orchestration.barrier_selection_cells(duplicate_setup)


def test_identity_and_cell_mismatches_fail_closed():
    identity = orchestration.Stage1CellIdentity(
        orchestration.DATASET_ID, 0, 0.1, 1
    )
    setup = stage1_setup.prepare_stage1_candidate(
        [(np.array([0.0]), np.array([[-1.0], [0.0], [1.0]]))],
        beta=0.1,
        seed=1,
    )
    cell = orchestration.Stage1CandidateCell(identity, setup)
    assert cell.identity is identity
    assert cell.setup is setup

    for changes in (
        {"dataset_id": "other"},
        {"dataset_id": object()},
        {"reshuffle_seed": 2},
        {"beta": 0.3},
        {"init_seed": 3},
    ):
        with pytest.raises(ValueError):
            replace(identity, **changes)
    with pytest.raises(ValueError, match="beta differs"):
        orchestration.Stage1CandidateCell(
            identity,
            stage1_setup.prepare_stage1_candidate(
                [(np.array([0.0]), np.array([[-1.0], [0.0], [1.0]]))],
                beta=0.2,
                seed=1,
            ),
        )
    with pytest.raises(ValueError, match="init seed differs"):
        orchestration.Stage1CandidateCell(
            identity,
            stage1_setup.prepare_stage1_candidate(
                [(np.array([0.0]), np.array([[-1.0], [0.0], [1.0]]))],
                beta=0.1,
                seed=0,
            ),
        )


@pytest.mark.parametrize(
    "mutate",
    [
        lambda groups: groups.pop(),
        lambda groups: groups.__setitem__(
            0, (np.deg2rad(30), groups[0][1])
        ),
        lambda groups: groups.__setitem__(0, (groups[0][0], np.array([1.0]))),
        lambda groups: groups.__setitem__(
            0, (groups[0][0], np.full(10, np.nan))
        ),
        lambda groups: groups.__setitem__(
            0, (groups[0][0], np.full(10, True))
        ),
    ],
)
def test_source_boundary_rejects_invalid_groups(mutate):
    groups = _source_groups()
    mutate(groups)
    with pytest.raises(ValueError):
        orchestration.prepare_stage1_cells(groups)


def test_cell_interfaces_do_not_expose_test_or_artifact_data():
    forbidden = {
        "test",
        "test_data",
        "test_indices",
        "test_nll",
        "artifact",
        "checkpoint",
        "stage2_beta",
        "scientific_verdict",
    }
    assert {field.name for field in fields(
        orchestration.Stage1CellIdentity
    )}.isdisjoint(forbidden)
    assert {field.name for field in fields(
        orchestration.Stage1CandidateCell
    )}.isdisjoint(forbidden)
