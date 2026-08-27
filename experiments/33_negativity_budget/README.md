# Experiment 33 — negativity-budget sweep

Issue #140。

- Packet 1 forward model: [`protocol.md`](protocol.md) / [`fixed_beta.py`](fixed_beta.py)
- Packet 2 density Jacobian・grid barrier: [`packet2_protocol.md`](packet2_protocol.md) / [`packet2.py`](packet2.py)
- gates: [`../../tests/test_negativity_budget.py`](../../tests/test_negativity_budget.py) / [`../../tests/test_negativity_budget_packet2.py`](../../tests/test_negativity_budget_packet2.py)

両packetともGKP quadrature値を読まず、optimizerやstage 1/2 resultを生成しない。

```powershell
python -m pytest tests\test_negativity_budget.py tests\test_negativity_budget_packet2.py -q
```
