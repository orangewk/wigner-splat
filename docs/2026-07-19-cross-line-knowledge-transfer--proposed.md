# 両線の知見移転ノート — 量子コア線 ⇄ 応用線(4DGS 証明書)

日付: 2026-07-19 / 状態: proposed(未採択の候補棚卸し)
きっかけ: 応用線 round 3(a) のマイルストーン到達(exp20 =
`20_real_video_gpu`、Gate B 初合格・Gate B2 不合格、issue #48 comment
5011709434)を機に、量子コア線の直近マイルストーン(#39 exp16 =
`16_exp11_seeds`、#42 exp17 = `17_loss_control`、#40 exp18 =
`18_gkp_saturation`)と突き合わせ、双方向の移転可能性を orange の依頼で
棚卸しした。

適用ルール: ここに書くのは「候補」であり、どれかを実行する場合は該当
issue で gate ごと事前宣言してから。この文書自体は何も宣言しない。

⚠️ 出典の状態: exp20 の実装・結果(Gate B/B2 数値、乱択 Fisher、
checkpoints)は**未マージの draft PR #66 のブランチ上にのみ存在**し、
本文書の時点で main には入っていない。exp20 への言及はすべて「draft
PR #66 上の未マージ成果」への参照である。

---

## 0. 両線に共通する観測(一般化は限定つき)

- 量子 exp16(#39): lossy 標的の rank-2 fit に崩壊 basin が存在し、
  崩壊解と高忠実度解の差は ΔF ≈ 0.448–0.476 に対し ΔNLL ≈
  2.48e-3–3.35e-3 nats(`16_exp11_seeds/results.json`)。さらに data
  seed 1 では、NLL 選択された F = 0.9524 の解に対し F = 0.9947 の解が
  ΔNLL ~ 1e-4 の近同値に存在し、宣言済み選択規則が良い方を選べなかった
  (この 1e-4 は崩壊ペアの数値ではなく、選択の近同値ペアの数値)。
- 量子 exp17(#42): fitted-η が train-NLL 平坦域(3.96110–3.96112)上で
  η 0.56–0.77・F 0.06–0.80 に散る — この設計で η は識別不能。
- 応用 exp16→exp20: 18 dB 作業点では held-out 残差と証明書の相関が
  +0.03、25 dB 超の作業点(モデル・解像度・容量・パイプラインを変えた
  operating-point 比較)では +0.33。

これら三例のメカニズムは同一ではない: 一つ目は離れた basin 間の
multimodality、二つ目は局所的な識別 ridge、三つ目は作業点の移動であり、
三例目から train loss の平坦方向を測ったわけでもない。現時点で主張して
よい共通構造は **「スカラーの fit objective(NLL / PSNR)単独では下流
品質を決め切れない」** まで。H / Fisher / GN 解析はこのうち **選択済みの
解の周りの局所的な**識別性・感度を診断する道具であり(GGN/Laplace の
局所線形化の射程: Immer et al., PMLR 2021,
https://proceedings.mlr.press/v130/immer21a.html; 単一 mode Gaussian
近似の限界: Yu et al., PMLR 2024,
https://proceedings.mlr.press/v238/yu24a.html)、離れた basin・モデル
バイアス・multimodality を直接検出するものではない。exp17 の η ridge は
局所診断の射程内の候補、exp16 #39 の崩壊 basin は射程外(multi-start 等
の大域的手当てが引き続き必要)。

## 1. 量子 → 応用(応用線のブラッシュアップ候補)

1. **ニュイサンスは「fit するな、測るか固定しろ」— 仮説として検証**。
   exp17 の実証は「η はこの設計の尤度で識別不能で、joint fit は ignore
   より悪化し得る」。応用線の blur knob ablation 失敗(on ≥ off が 2/3
   seed)が同型の識別不能によるものかは**未検証の仮説**。GPU ラウンドで
   blur / appearance を再導入するなら、`diagnose_eta.py` 方式の識別可能
   性診断(複数スタート → loss 平坦性の確認)を先に宣言して仮説ごと
   検証する。
2. **選択規則の事前宣言と init-fragility 検査**(exp16 #39)。
   best-by-train-loss の選択規則を宣言し、seed 間の解のばらつき自体を
   診断量にする。ΔNLL ~ 1e-4 の近同値解ペアの存在は、選択規則単独では
   足りないことの実例。
3. **容量の飽和スイープ**(exp18 #40 の R=4–5 特定手順)。splat 数 /
   densification 予算を「宣言済み飽和点」で選ぶ手順に移植可能。
4. **アンサンブル分散を対照に加える — 探索と確認を分離**。既存の 3
   fit-seed checkpoint(draft PR #66 のローカル成果物、未コミット)と
   既開封の held-out で計算するアンサンブル分散比較は**探索的解析に
   限られる**(同じ held-out は既に Gate B/B2 に使用済み)。確認的な
   round 4 / Gate B2 に載せる場合は、issue #48 の carry-forward
   どおり fresh sealed data または明示的に独立な評価単位を使い、3 seed
   からの分散推定法(不偏化・画素単位の定義)も事前固定する。
5. (PR #66 クロスチェックで指摘済みの再掲)単一スカラー damping への
   σ_pred の感度スイープも round 4 の設計材料。

## 2. 応用 → 量子(ViceVersa)

1. **証明書機構の逆輸入 — 位相空間の局所 predictive variance(候補)**。
   σ_pred² = JᵀH⁻¹J は、画素を (x,p) に読み替えれば Wigner 再構成の
   **選択 mode 周りの局所 Laplace/GGN 型 predictive variance の候補**に
   なる。量子線のパラメータ数は小さい(K≤6, R≤5)ので乱択不要・厳密な
   H が組める。ただしこれは離れた basin の崩壊・モデルバイアス・
   multimodality を直接検出しない(§0)。「崩壊モード = H の平坦方向」
   は**未実証の仮説**であり、実験項目としては (a) 既知の崩壊モード・η
   ridge と H 固有方向の対応の確認、(b) synthetic での coverage /
   calibration 検証、(c) 局所 variance とバイアス・mode 間分散の分離、
   を先に置く。W(0,0) の負値については「有意性判定」ではなく
   **「校正対象の候補」**(calibration が通った範囲でのみ誤差バーとして
   意味を持つ)として扱う。
2. **バイアス/分散の適用条件 — 予言(検証予定の仮説)**。round 2→3 の
   教訓は「分散型証明書はバイアスが小さい作業点でのみ残差と相関した」。
   これを量子側に写した予想: purefock3(0.9727、truncation 天井 ~0.993
   近傍)や bbdagS には効く見込み、splat 再構成(overlap ~0.50)は
   バイアス支配で効かない見込み — いずれも**未検証**で、検証時は該当
   issue で宣言してから。
3. **対照群規律(B2 型)**。量子側で不確かさを主張する際も、|W| 振幅・
   ‖J‖ 級の安価な対照との比較を宣言に含める。応用線は「洗練された
   証明書が単純対照に勝てない」を 2 回経験済み(Phase 0 の控えめ化、
   round 3 の B2 不合格)。同じ罠の予防。
4. **乱択 matrix-free Fisher(draft PR #66 の Phase 4b)**。現行の量子
   実験には不要(厳密 H が組める)が、将来パラメータが増えた場合に
   備え、unbiased Rademacher 推定器 + tiny-exact-gate 検証パターンの
   実装が draft PR #66 のブランチ上に存在する(マージまでは未マージ
   成果としての参照)。

## 3. 実行順の推奨(宣言は各 issue で)

- 応用線 round 4: アンサンブル分散対照(fresh sealed data / 独立評価
  単位 + 分散推定法の事前固定)+ ノブ識別可能性診断 + damping 感度を
  宣言に含める。
- 量子線 次イシュー候補: 厳密 H による Wigner 局所誤差バーの構築と、
  §2.1 の (a)(b)(c) による射程の検証(W(0,0) は校正対象の候補)。

出典: docs/research-log.md の各エントリ(exp16=16_exp11_seeds,
exp17=17_loss_control, exp18=18_gkp_saturation, 応用線 exp15/16)、
`16_exp11_seeds/results.json`、issue #48 comments 5011474178 /
5011709434、PR #59(マージ済み)/ PR #66(draft・未マージ)。
