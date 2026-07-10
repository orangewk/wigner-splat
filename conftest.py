"""Pytest process defaults for numerical tests.

Pin BLAS/OpenMP thread counts to 1 for numerical reproducibility and to avoid
CPU oversubscription when several pytest processes run at once. setdefault lets
an explicit caller (e.g. experiments/06_three_mode/run.py) override.

NOTE: this is NOT a fix for the 2026-07-09 pytest hang. That hang was two
sessions running pytest on the same shared checkout; the fix is worktree
separation + the AGENTS.md no-double-launch rule, not this pin (the BLAS
oversubscription hypothesis did not reproduce).
"""

import os


for _name in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "BLIS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(_name, "1")
