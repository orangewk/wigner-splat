"""Public exp27 entry point with recorded SSM provenance."""

from __future__ import annotations

import importlib.util
from pathlib import Path


BASE_PATH = Path(__file__).with_name("_run_final_base.py")
SPEC = importlib.util.spec_from_file_location("exp27_final_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load exp27 final runner")
FINAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FINAL)
CORE = FINAL.BASE


_compute_debye_length = CORE.compute_debye_length


def compute_debye_length() -> dict:
    result = _compute_debye_length()
    result["source"] = {
        "model": "B16-GS98",
        "paper_url": "https://arxiv.org/abs/1611.09867",
        "composition_table": "Table_1_GS98_abundances",
        "central_mass_fraction_table": "Table_4_B16-GS98_Yc_Zc",
        "density_input_type": "declared_run_input",
    }
    return result


def main() -> None:
    CORE.compute_debye_length = compute_debye_length
    FINAL.main()


if __name__ == "__main__":
    main()
