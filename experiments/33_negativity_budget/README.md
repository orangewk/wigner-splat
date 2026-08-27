# Experiment 33 — negativity-budget sweep

Issue #140。

- Packet 1 forward model: [`protocol.md`](protocol.md) / [`fixed_beta.py`](fixed_beta.py)
- Packet 2 density Jacobian・grid barrier: [`packet2_protocol.md`](packet2_protocol.md) / [`packet2.py`](packet2.py)
- Stage 1 candidate setup: [`stage1_setup_protocol.md`](stage1_setup_protocol.md) / [`stage1_setup.py`](stage1_setup.py)
- Stage 1 train objective: [`stage1_objective_protocol.md`](stage1_objective_protocol.md) / [`stage1_objective.py`](stage1_objective.py)
- gates: [`../../tests/test_negativity_budget.py`](../../tests/test_negativity_budget.py) / [`../../tests/test_negativity_budget_packet2.py`](../../tests/test_negativity_budget_packet2.py) / [`../../tests/test_negativity_budget_stage1_setup.py`](../../tests/test_negativity_budget_stage1_setup.py) / [`../../tests/test_negativity_budget_stage1_objective.py`](../../tests/test_negativity_budget_stage1_objective.py)

各packetはGKP quadrature値を読まず、optimizerやstage 1/2 resultを生成しない。

```powershell
python -m pytest tests\test_negativity_budget.py tests\test_negativity_budget_packet2.py tests\test_negativity_budget_stage1_setup.py tests\test_negativity_budget_stage1_objective.py -q
```
