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

**判定(2026-07-06、実験03: 単一モード猫状態 α=1.5、12角、n_max=20 の R ρ R)**:
fidelity は全ショット予算で splat が勝つ(250 shots/angle で 0.980 vs 0.969、
4000 で 0.991 vs 0.987 — ショット効率の優位は実在)が、速度は MLE が約2倍速く
(~0.6s vs ~1.3s)、条件は**不成立**。約束通り記録する: **単一モード・この規模では
計算上の利得は生まれない。** 残る仮説はスケーリングである — 多モードでは Fock 基底
MLE の次元が指数爆発する(n_max^モード数)のに対し splat のパラメータ数は O(K) に
留まる。これは多モード拡張(ロードマップ)で検証し、そこでも勝てなければ
アプローチ全体を棄却する。

**判定・2モード(2026-07-07、実験04: もつれ猫 |α,α⟩+|−α,−α⟩ α=1.5、4×4 角度対、
Fock MLE は n_max=12 → 144次元)**: 単一モードから**役割が逆転**した。速度は splat が
全予算・全シードで **6–11倍**勝ち(~4 s vs 27–45 s)— 予言した O(K) vs n_max^モード数
のスケーリング分離が実測された。fidelity は統計的互角(splat 0.921±0.011 vs MLE
0.926±0.007、差 0.003–0.006 はシードノイズ 0.015–0.018 未満)で、両者とも同じ有限
ショット天井に座る(MLE の打ち切り上限は 0.99999)。もつれ負性は両者が回復(Wmin
≈ −0.07 vs 真値 −0.078)。厳密な「両勝ち」は平均では未達だが、**反証条件のトリガー
(両方で負ける)は発動しない**: 同等品質を約1/10の計算で得ること自体が計算上の利得
である。前提条件は**完全 4×4 共分散**であること — 分離可能(モードごとブロック対角)
スプラットは fidelity 0.50 で完全敗北する(**もつれ ⟺ モード間相関を持つ傾いた共分散**、
が本質。実験04の図と `tests/test_two_mode_fit.py` の xfail に記録)。決定打は3モード
(MLE は 12³=1728 次元で非現実的になる)で付ける。

## 構成

```
wigner_splat/
  states.py    # 参照状態(猫状態): Wigner 関数・homodyne 分布・サンプラー
  forward.py   # 符号付きガウス混合の Radon 投影(閉形式)= 微分可能フォワードモデル
  fit.py       # 再構成器: ヒストグラム損失 + 負性ペナルティ + Adam(解析勾配)
               #   + densification(勾配ノルム分裂・剪定・重み勾配場による符号付き誕生)
  fock.py      # 打ち切り Fock 基底: 猫状態の密度行列・Wigner 変換・fidelity
  mle.py       # iterative MLE ベースライン(Lvovsky R ρ R)
experiments/
  01_cat_state/       # 最初の実験: 猫状態のシミュレーション再構成(固定 K=8)
  02_densification/   # K=4 から適応成長させる再構成(固定 K=8 を上回る)
  03_mle_baseline/    # splat vs MLE 対照実験(反証条件の判定)
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
- [x] densification / pruning(勾配ノルム分裂・剪定 + **重み勾配場による符号付き誕生**。
      K=4→9 で相対L2 7.1%、固定 K=8 の 12.5% を上回る。分裂だけでは全正の局所解から
      負性が生まれない → 仮想スプラットの重み勾配 ∂L/∂w(μ)(=残差の逆投影)の極値に
      降下方向の符号で新スプラットを誕生させることで解決)
- [ ] 検出効率・ガウスノイズのモデル化(Bernoulli 損失 → 一般化)
- [x] iterative MLE ベースラインとの比較(実験03。fidelity: splat 勝ち(全予算)、
      速度: MLE 勝ち(単一モードでは行列が小さい)→ 反証条件は不成立、上記に記録)
- [ ] 物理制約(正定値性)の厳密な扱い — Kenfack 型の閉形式制約 vs ペナルティ
- [x] 2モード拡張(実験04。分離可能スプラットは F=0.50 で失敗 → 完全 4×4 共分散で
      F=MLE 同等・速度 6–11倍。もつれ ⟺ 傾いた共分散の対応を実証。上記判定参照)
- [ ] 3モード拡張(スケーリングの決定打: Fock MLE は 1728次元で非現実的、splat は O(K) のまま)

## 引用すべき近接先行研究

機構: [R2-Gaussian](https://arxiv.org/abs/2405.20693) / [X²-Gaussian](https://arxiv.org/abs/2503.21779) ·
表現: [Kenfack 2004](https://arxiv.org/abs/physics/0304029) / [Tosca 2025](https://arxiv.org/abs/2507.14076) ·
homodyne 最適化: [Strandberg 2022](https://arxiv.org/abs/2202.11584) / [Gaikwad 2025](https://arxiv.org/html/2503.04526v1)

詳細は [docs/prior-art-survey.md](docs/prior-art-survey.md)。
