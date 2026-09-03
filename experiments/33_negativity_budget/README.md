# Experiment 33 — negativity-budget sweep

Issue #140。

- Packet 1 forward model: [`protocol.md`](protocol.md) / [`fixed_beta.py`](fixed_beta.py)
- Packet 2 density Jacobian・grid barrier: [`packet2_protocol.md`](packet2_protocol.md) / [`packet2.py`](packet2.py)
- Stage 1 candidate setup: [`stage1_setup_protocol.md`](stage1_setup_protocol.md) / [`stage1_setup.py`](stage1_setup.py)
- Stage 1 train objective: [`stage1_objective_protocol.md`](stage1_objective_protocol.md) / [`stage1_objective.py`](stage1_objective.py)
- Stage 1 Adam step: [`stage1_adam_step_protocol.md`](stage1_adam_step_protocol.md) / [`stage1_adam_step.py`](stage1_adam_step.py)
- Stage 1 candidate runner: [`stage1_runner_protocol.md`](stage1_runner_protocol.md) / [`stage1_runner.py`](stage1_runner.py)
- Stage 1 barrier selection: [`stage1_barrier_selection_protocol.md`](stage1_barrier_selection_protocol.md) / [`stage1_barrier_selection.py`](stage1_barrier_selection.py)
- gates: [`../../tests/test_negativity_budget.py`](../../tests/test_negativity_budget.py) / [`../../tests/test_negativity_budget_packet2.py`](../../tests/test_negativity_budget_packet2.py) / [`../../tests/test_negativity_budget_stage1_setup.py`](../../tests/test_negativity_budget_stage1_setup.py) / [`../../tests/test_negativity_budget_stage1_objective.py`](../../tests/test_negativity_budget_stage1_objective.py) / [`../../tests/test_negativity_budget_stage1_adam_step.py`](../../tests/test_negativity_budget_stage1_adam_step.py) / [`../../tests/test_negativity_budget_stage1_runner.py`](../../tests/test_negativity_budget_stage1_runner.py) / [`../../tests/test_negativity_budget_stage1_barrier_selection.py`](../../tests/test_negativity_budget_stage1_barrier_selection.py)

各packetのscopeとresult境界は対応するprotocolだけを正本とし、このREADMEは入口だけを置く。

```powershell
python -m pytest -p no:cacheprovider tests\test_negativity_budget.py tests\test_negativity_budget_packet2.py tests\test_negativity_budget_stage1_setup.py tests\test_negativity_budget_stage1_objective.py tests\test_negativity_budget_stage1_adam_step.py tests\test_negativity_budget_stage1_runner.py tests\test_negativity_budget_stage1_barrier_selection.py -q
```
