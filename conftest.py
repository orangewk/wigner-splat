"""Pytest process defaults for numerical tests.

Keep BLAS/OpenMP-backed libraries from oversubscribing CPU threads when pytest
runs overlap on Windows. Use setdefault so an explicit caller setting wins.
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
