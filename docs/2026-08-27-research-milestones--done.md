# 2026-08-27 — 研究マイルストーンと現在地

状態: **reader guide / recorded**

この文書は、研究全体の流れを短時間でつかむための案内である。
数値、判定、claim statusのauthoring locationではない。正確な値と適用範囲は、
各節からリンクしたartifact、claim table、charterを参照する。

## 一文での現在地

手法が動くことと、物理保証付きの低次元modelが実データで競争力を持つことは確認した。
現在は、signed表現の非物理な自由度が予測性能に本当に必要なのかを、
GKP held-out NLLで物理modelと直接比較する直前にいる。

## 到達したマイルストーン

### 1. signed splatの成立と多モードscaling

単一モードでは計算優位が出ず、二・三モードでFock-space MLEとの計算量分離が現れた。
一方、三モードで得た高いscoreとPSD物理性の間には強いtensionが残った。

- 経緯と判定: [`README.ja.md`](../README.ja.md) の「反証条件」と実験03–08
- 一次記録: [`docs/research-log.md`](research-log.md)
- 物理性の検査: [`experiments/08_positivity/`](../experiments/08_positivity/)

この段階で研究課題は「splatは速いか」だけでなく、
「速さやscoreが非物理性に支えられていないか」へ移った。

### 2. 構成的に物理なBB-dagger model

PSDを構成的に保証するBB-dagger表現へ移り、解析勾配、混合rank、loss channelを整備した。
GKP実データでは、rankとlossを含む物理modelが、より大きなMLE frontierと
held-out NLLの分解能内で競争できる地点まで到達した。

- 実データの戦歴: [`README.ja.md`](../README.ja.md) の実験12–18
- saturation artifact: [`experiments/18_gkp_saturation/results.json`](../experiments/18_gkp_saturation/results.json)
- model実装: [`wigner_splat/bbdagS.py`](../wigner_splat/bbdagS.py)

現時点で最も強い応用上の根拠は、物理性を守ることと予測性能が両立しうる、という点にある。

### 3. K-epsilon理論とtopological obstruction

K-epsilonをGaussian辞書での近似コストとして扱う理論ノートを公開し、
限定された二モードtargetと辞書について、stellar零点の位相的不一致から
定量的な近似障害へ接続するsliceを構築した。

- program charter: [issue #71](https://github.com/orangewk/wigner-splat/issues/71)
- topological charter: [issue #137](https://github.com/orangewk/wigner-splat/issues/137)
- link stability: [`experiments/28_isotopy_stability/`](../experiments/28_isotopy_stability/)
- trefoil slice: [`experiments/29_trefoil_certified/`](../experiments/29_trefoil_certified/)
- dictionary alignment: [`experiments/30_dictionary_alignment/`](../experiments/30_dictionary_alignment/)
- gate closure記録: [`docs/research-log.md`](research-log.md)

Gate T-primeとGate S-primeはcloseしたが、一般K、三モード以上、
公開ノート本体への二モード結果の統合、強いnovelty判定は完了していない。

### 4. 別の公開homodyne dataへの展開

Kawasaki pump-seriesで、raw data contract、restartable fit、review gate、
canonical result artifactまで一周させた。外部dataへ運べるpipelineは成立したが、
結果の読みはunit/phase conventionに敏感であり、一般的な性能優位としては扱わない。

- protocolと結果への入口: [`experiments/32_kawasaki_data/README.md`](../experiments/32_kawasaki_data/README.md)
- 数値の唯一の正本: [`experiments/32_kawasaki_data/pump_results.json`](../experiments/32_kawasaki_data/pump_results.json)
- publication PR: [PR #185](https://github.com/orangewk/wigner-splat/pull/185)

### 5. negativity-budget sweepの入口

物理なBB-daggerと自由なsigned表現の間を、固定beta差分modelで結ぶinterfaceを確定した。
betaは状態から同定する負性ではなく、外から与えるparameterization knobである。
rank/dofを揃えた物理側対照なしに、betaの効果を負性の証拠とは読まない。

- charterと事前判定: [issue #140](https://github.com/orangewk/wigner-splat/issues/140)
- interface契約: [`experiments/33_negativity_budget/protocol.md`](../experiments/33_negativity_budget/protocol.md)
- reviewed packet: [PR #187](https://github.com/orangewk/wigner-splat/pull/187)

Packet 1はpre-data-valuesであり、GKP値、fit、barrier係数、Stage 1/2の結果を含まない。
したがって、negativity-budgetについての科学的結論はまだ存在しない。

## 今ここからの本筋

### Packet 2 — fit可能なinterface

- fixed-beta modelの解析勾配
- train角度ごとのdense-grid positivity barrier
- componentの可変性とoptimizer lifecycleの契約
- finite-differenceから独立したgradient referee

このpacketでも実データの判定は行わない。

### Stage 1 — train-only粗探索

事前宣言したbeta gridで、train NLL、invalid率、barrier感度を見る。
test dataを見ずにbarrier係数とStage 2のbeta点を固定する。

### Stage 2 — 主要な研究判定

dofを揃えた物理側対照とheld-out NLLを比較し、次のどれかを記録する。

- signed自由度に予測価値が見つからない
- dof差では説明できない改善が見つかる
- 負densityによってmodel族が実用上破綻する

最良のsigned fitはFock基底でPSD射影し、物理状態へ戻したときに失われる予測性能も測る。
このStage 2が、次の大きな科学マイルストーンである。

## 並行線の位置づけ

- **K-epsilon一般化**: 理論programはopen。二モードの限定sliceを一般理論と混同しない。
- **Kawasaki follow-up**: scientific artifactはmainにある。公開導線のPR #186は未mergeだが、科学的blockerではない。
- **信頼度付き4DGS**: [issue #48](https://github.com/orangewk/wigner-splat/issues/48) は長期本線charter。
  現時点では量子側の証明書思想を輸出する計画であり、実証済み成果として扱わない。

## 研究判断

直近ではlineを増やすより、issue #140をStage 2まで通す価値が高い。
NULL、WIN、invalidのどの分岐でも、signed表現と物理modelの関係について
現在より強く、反証可能な結論が得られるためである。
