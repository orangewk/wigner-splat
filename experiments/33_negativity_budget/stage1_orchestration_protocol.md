# 負性予算 sweep Stage 1 cell identity / orchestration packet

状態: **canonical cell registry / pre-data-values**

Issue: #140

依存: Stage 1 candidate setup。runnerとbarrier selectorは本packetのcell identityを参照する。

本packetはStage 1のsource、reshuffle、beta、init seedを一つのimmutable cell identityへ束ね、
train-only setupをcanonical順で構築する。GKP値の読取り、実data digest、fit実行、artifact、
checkpoint、held-out評価、Stage 2選択、科学的判定は扱わない。

## 1. authoring locationとcell registry

Stage 1 cell identity、全cell集合、順序、barrier-selection view、split algorithmは本文書を唯一の
authoring locationとする。

| 項目 | 固定値 / 意味 |
| --- | --- |
| dataset id | `dryad:10.5061/dryad.t76hdr86j:gkp-six-phase-npy` |
| phase順 | `0, 30, 60, -30, -60, -90` degrees |
| reshuffle seed | `0, 1` |
| beta | `0, 0.02, 0.05, 0.1, 0.2, 0.4` |
| init seed | `0, 1, 2` |
| canonical順 | reshuffle-major、beta-major、init-seed-major |

全registryは `2 * 6 * 3 = 36` cellである。`Stage1CellIdentity`はdataset id、reshuffle seed、
beta、init seedを保持し、宣言集合外の値を拒否する。source固有情報をgenericな
`Stage1CandidateSetup`へ追加しない。

## 2. train-only split

callerが渡すsourceは宣言phase順の6 groupで、各groupはphase scalarと有限実数の1次元sample
vectorを持つ。実ファイルを開くloaderは本packetに置かない。

各reshuffleについて `numpy.random.Generator(numpy.random.PCG64(seed))` を一つ作り、phase順に
各groupの `permutation(N)` を呼ぶ。先頭 `int(0.8 * N)` indexだけをtrainとする。これは現行
NumPyでexp18の `default_rng(seed)` splitと一致しつつ、bit generatorをPCG64へ明示する。
test indexとtest sampleは返さず、`Stage1CandidateSetup`へ渡さない。後続artifactは実行環境と
split index digestを記録するが、本packetは実dataを読まずdigestを計算しない。

## 3. cell constructionとbinding

`prepare_stage1_cells(source_groups)` はreshuffleごとにtrain groupを一度導出し、canonicalな
36 identityそれぞれについて既存 `prepare_stage1_candidate(train, beta, init_seed)` を呼ぶ。
各cellはidentityと専有setupを保持し、identityのbeta/init seedとsetupが一致しなければ拒否する。

runnerはsetup単体でなくcellを受け、runへcell identityを保持する。barrier assessmentも同じ
identityを保持し、run側identityとの不一致を拒否する。lambda間では同一cell/setup objectを
再利用する。これによりfactoryが付与したsource/reshuffle/beta/init seedを下流で別runへ
差し替える誤結合をartifact定義前に塞ぐ。

本packetは実data contentを読まないため、外部から直接組み立てたcellのsemantic dataset idが
setup内容を真正に表すことまでは証明しない。実data runでは`prepare_stage1_cells`だけをcell構築
入口とし、後続artifact packetがsource file digestとsplit index digestを記録・再検証する。

## 4. barrier-selection view

`barrier_selection_cells(cells)` はcanonical 36-cell registryだけを受理し、beta `0`を除いた
`2 * 5 * 3 = 30` cellを元の順序で返す。beta `0`は物理controlでbarrier係数選択には使わない。
global lambdaはこの30 cellすべてでadmissibleでなければならない。

## 5. gates

1. identity registryが36 cellで重複なくcanonical順、barrier viewがbeta-positive 30 cellである。
2. six-phase順、real finite 1-D sample、declared identity domainをfail closedで検証する。
3. splitが明示PCG64、seed 0/1、phase順の逐次permutation、80% floorで独立計算と一致する。
4. setupへtrainだけを渡し、cell/result interfaceにtest dataを持たない。
5. cellとsetupのbeta/init seed、runとassessmentのcell identityの不一致を拒否する。
6. resultへ実data digest、artifact、checkpoint、held-out metric、Stage 2、科学的verdictを持たない。

## 6. 実装前に確認した一次資料

- NumPy random compatibility policyは同じBitGenerator、seed、呼出し列、build、環境でのstream
  compatibilityを境界とし、個別BitGeneratorの方が強い保証を持つとする。
  <https://numpy.org/doc/2.0/reference/random/compatibility.html>
- NumPy PCG64は固定seedに同じrandom integer streamを保証する。
  <https://numpy.org/doc/stable/reference/random/bit_generators/pcg64.html>
- MLflow Datasetはsource、digest、schema/profileを分離してrun inputへ結び付ける。本packetも
  semantic source identityを先に固定し、content digestは実行artifactへ残す。
  <https://mlflow.org/docs/latest/api_reference/python_api/mlflow.data.html>
- DVCはversioned fileをcontent-addressed hashで識別する。本projectへ依存は追加せず、
  同じsource/digest分離だけを後続artifact設計へ採る。
  <https://dvc.org/blog/dvc-vs-rclone/>
- W3C PROVはentity、activity、agentとその関係をprovenance modelの中心に置く。本packetでは
  dataset/cellをentity、後続runをactivityとして結び付ける最小fieldだけを実装する。
  <https://www.w3.org/TR/prov-overview/>
