# Experiment 33 — fixed-negativity-budget interface

状態: **packet 1 / pre-data-values**

Issue: #140

本packetは、負性予算sweepが下流で消費するforward interfaceだけを固定する。
GKP quadrature値、exp18 result値、optimizer、barrier係数、stage 1/2のfit・判定は扱わない。

## 1. authoring location

固定β差分modelの意味と評価境界は本文書を唯一のauthoring locationとする。
`fixed_beta.py` はこの定義を実装し、専用testは別計算で検査する。

## 2. fixed-β difference model

`rho_B` と `rho_C` を、それぞれ内部traceが1のPSDな
`MixedSqueezedKetState` modelとする。数式上は `0 <= beta < 1/2` とし、
pre-normalizationの正・負massを `1-beta` と `beta` に固定する。報告modelは

`rho_beta = ((1-beta) rho_B - beta rho_C) / (1-2 beta)`

である。したがってtraceは1だが、`beta > 0`ではPSDも測定密度の非負性も保証しない。
`beta` はこの差分構成のpre-normalization負mass比であり、Fock射影後の負固有値絶対値和や
Wigner負体積とは別の量である。

本packetが数値計算として対応する範囲は `0 <= beta <= 0.49` とする。この範囲では
分母 `1-2 beta >= 0.02`、係数は `c_+ <= 25.5`、`c_- <= 24.5` である。
stage 1の宣言済みgridは0.4までとし、invalid率のkneeを挟む必要がある場合だけ
stage 2が `(0.4, 0.49]` を使える。これは0.5の特異点から離す数値条件の契約であり、
データが許す負性の物理的上限を0.4へ事前固定しない。

`c_+(beta) = (1-beta)/(1-2 beta)`、`c_-(beta) = beta/(1-2 beta)` とする。
`beta_1 < beta_2`、任意のtrace-one PSD成分 `S` に対し、
`d = c_+(beta_2)-c_+(beta_1) = c_-(beta_2)-c_-(beta_1) > 0` と置けば、

`rho_B2 = (c_+(beta_1) rho_B1 + d S) / c_+(beta_2)`

`rho_C2 = (c_-(beta_1) rho_C1 + d S) / c_-(beta_2)`

は同じ報告modelを `beta_2` で表す。`beta_1=0`では負成分の項を0とする。
したがってrankを増やせるinterfaceでは、小さいbetaのmodel classを大きいbetaのclassが含む。

| claim | scope / interpretation |
| --- | --- |
| `beta` | 差分構成へ外から与えるknob。fitされた状態から同定する量ではない |
| class inclusion | 正・負成分のmixture rankを必要分だけ増やせる場合。固定rank予算では成立しないことがある |
| 実験での性能差 | beta単独の物理的負性の証拠にしない。rank/dofを明記し、dofを揃えた物理側対照と比較する |

同じloss channel parameter `eta` を両成分へ適用してから線形結合する。
`beta=0`では負成分を構築せず、既存のpositive modelとparameterizationごと同一にする。

## 3. fail-closed evaluation boundary

- 各measurement groupはreal finiteな数値配列 `X` shape `(N, M)`、
  `theta` shape `(M,)`、`N >= 1` とし、不一致はdensity評価前に入力エラーとして拒否する。
- loss parameterはreal finite scalar `0 <= eta <= 1`、`extra_noise_var >= 0` とし、
  bool、非scalar、complex、非finite、domain外をdensity評価前にparameter errorとして拒否する。
- 各PSD成分は既存`lossy_pdf_mixed`で評価する。その後のsigned線形結合は
  clip・floor・renormalizeしない。
- held-out sampleの1点でもdensityが非finiteまたは0以下なら、そのfitはinvalidとし
  NLLを返さない。
- 正の全sampleに対してだけ、per-sample `-log(p)` とそのmeanを返す。
- dense-grid barrierとそのgradientはpacket 2で追加する。packet 1のmodelを変更せず消費する。

## 4. packet 1 gates

1. `beta=0`のdensityは既存`lossy_pdf_mixed`と一致する。NLLは全densityが
   `1e-300`以上なら既存`nll_lossy_mixed`と一致し、floorがbindingする領域では
   旧実装がfloorを使う一方、strict NLLは真の正densityを使うか0なら拒否する。
2. 対応域上端`beta=0.49`を含め、各成分densityが正規化されている場合は
   signed densityも積分1になる。
3. 負densityを観測可能な形で保持し、strict NLLが拒否する。
4. beta domain、成分shape、mode不一致、非finite norm、非real/nonfinite観測、
   不正loss parameterをfail closedで拒否する。
5. rankを増やした構成で `class(beta_1)` の同じdensityを `class(beta_2)` が再現する。
