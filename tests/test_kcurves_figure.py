"""Deterministic, torch-free rendering test for the issue #100 figure."""

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "22_kcurves"
sys.path.insert(0, str(EXP))
spec = importlib.util.spec_from_file_location("kcurves_run", EXP / "run.py")
assert spec is not None and spec.loader is not None
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)


def test_figure_bytes_are_deterministic(tmp_path):
    upper = run.extract_empirical_upper_bound(ROOT / "experiments/20_noninclusion/results_routeB.json")
    proxy = run.extract_data_proxy(
        ROOT / "experiments/18_gkp_saturation/results.json",
        ROOT / "experiments/14_gkp_rank/out_run.log",
    )
    output = tmp_path / "kcurves.png"
    run.make_figure(upper, proxy, output)
    first = output.read_bytes()
    run.make_figure(upper, proxy, output)
    assert output.read_bytes() == first
