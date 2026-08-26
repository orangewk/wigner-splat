# Experiment 33 — negativity-budget sweep

Issue #140。packet 1は、後続sweepが消費するfixed-β difference forward interfaceだけを扱う。
定義・非物理性の境界・fail-closed評価規則は [`protocol.md`](protocol.md) を参照する。

このpacketはGKP quadrature値を読まず、optimizer、barrier、stage 1/2 resultを生成しない。

```powershell
python -m pytest tests\test_negativity_budget.py -q
```
