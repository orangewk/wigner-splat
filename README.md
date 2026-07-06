# wigner-splat

**Gaussian Splatting for Quantum State Tomography** — 符号付き異方性ガウス混合を
3DGS 流の微分可能最適化で homodyne 測定データにフィットし、Wigner 関数を再構成する。

親プログラム: [indirect-agent-lab / 3DGS × 量子論 ポジションペーパー](https://github.com/orangewk/indirect-agent-lab/blob/main/docs/research/2026-07-06-3dgs-quantum-program--position.md)(テーマA)

## 主張(2026-07-06 サーベイ通過後の定式化)

3DGS-for-Radon-tomography 機構([R2-Gaussian 2024](https://arxiv.org/abs/2405.20693)、
[X²-Gaussian 2025](https://arxiv.org/abs/2503.21779))と、符号付きガウス混合による
Wigner 負性表現([Kenfack et al. 2004](https://arxiv.org/abs/physics/0304029)、
[Tosca et al. 2025](https://arxiv.org/abs/2507.14076))という **2つの独立した先行系譜を、
実測 homodyne データからの逆問題として初めて統合する**。

対応関係:

| 3DGS | 本リポジトリ |
|---|---|
| カメラ姿勢 | homodyne 測定の局発位相 θ(位相空間の回転角) |
| レンダリング(投影) | Radon 変換(Wigner 関数の周辺分布 = 測定される quadrature 分布) |
| スプラット | 位相空間上の異方性ガウス成分 |
| 非負の不透明度 | **符号付き重み**(負スプラット = Wigner 負性 = 非古典性) |
| densification / pruning | 勾配ノルム駆動の成分分裂・剪定(TODO) |

固有の技術的困難(=貢献の中身): 負の重みを許しながら、物理的制約
(全確率 1、周辺分布の非負性、密度演算子の正定値性)を保つ最適化。

## 反証条件

同一ショット数で iterative MLE に fidelity・速度の両方で勝てないなら、
このアプローチは計算上の利得を生まないと結論し、その旨を記録する。

## 構成

```
wigner_splat/
  states.py    # 参照状態(猫状態): Wigner 関数・homodyne 分布・サンプラー
  forward.py   # 符号付きガウス混合の Radon 投影(閉形式)= 微分可能フォワードモデル
  fit.py       # v0 再構成器: ヒストグラム損失 + 負性ペナルティ + Adam(解析勾配)
experiments/
  01_cat_state/  # 最初の実験: 猫状態のシミュレーション再構成
tests/           # フォワードモデルと物理の整合性テスト
docs/
  prior-art-survey.md  # 先行研究サーベイ(2026-07-06)
```

## クイックスタート

```bash
pip install numpy matplotlib pytest
python -m pytest tests/ -q          # 物理整合性テスト
python experiments/01_cat_state/run.py   # データ生成 → 再構成 → 図の出力
```

## ロードマップ

- [x] 猫状態の homodyne シミュレーションデータ生成器(ショットノイズ込み)
- [x] 符号付きガウス混合の閉形式 Radon フォワードモデル
- [x] v0 フィッタ(固定 K、数値勾配+Adam、負性ペナルティ)
- [x] 猫状態(α=1.5)で Wigner 負性の回復を確認(min −0.194 vs 真値 −0.190、相対L2 13%)
- [x] 解析勾配化(閉形式チェインルール。実験 01 が ~29s → ~1.6s、相対L2 12.5%、負性回復を維持)
- [ ] densification / pruning(勾配ノルム駆動の分裂・剪定)
- [ ] 検出効率・ガウスノイズのモデル化(Bernoulli 損失 → 一般化)
- [ ] iterative MLE ベースラインとの比較(fidelity / ショット数効率 / 実行時間)
- [ ] 物理制約(正定値性)の厳密な扱い — Kenfack 型の閉形式制約 vs ペナルティ
- [ ] 多モード拡張

## 引用すべき近接先行研究

機構: [R2-Gaussian](https://arxiv.org/abs/2405.20693) / [X²-Gaussian](https://arxiv.org/abs/2503.21779) ·
表現: [Kenfack 2004](https://arxiv.org/abs/physics/0304029) / [Tosca 2025](https://arxiv.org/abs/2507.14076) ·
homodyne 最適化: [Strandberg 2022](https://arxiv.org/abs/2202.11584) / [Gaikwad 2025](https://arxiv.org/html/2503.04526v1)

詳細は [docs/prior-art-survey.md](docs/prior-art-survey.md)。
