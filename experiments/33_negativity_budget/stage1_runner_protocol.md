# 負性予算 sweep Stage 1 candidate runner packet

状態: **single-candidate runner contract / pre-data-values**

Issue: #140

依存: Stage 1 candidate setup、train objective、Adam step。

本packetは一つのsetupと一つのbarrier係数を固定scheduleで走らせ、最後にcommit済みの
optimizer stateと停止理由を返す。barrier係数の候補・選択規則、beta/seed sweep、artifact
schema、GKP値、test評価、Stage 1の科学的結果は扱わない。

## 1. authoring location とschedule

単一candidate runの初期state、iteration数、停止status、集計interfaceは本文書を唯一の
authoring locationとする。一回の更新は `stage1_adam_step_protocol.md` を参照し、再定義しない。

| 項目 | 固定値 / 意味 |
| --- | --- |
| eta初期値 | exp18と同じ `0.8`。同じ式でlogitへ変換 |
| moments / iteration | state-plus-logit長のzero moments、完了済みiteration `0` |
| schedule | `100` accepted Adam steps。Issue #140のStage 1短縮schedule |
| early stopping / best iterate | なし。成功時は100回目にcommitしたstateを返す |

objectiveが減少しなくてもrunnerは停止しない。feasibility判定とmoment commitは一回更新の
契約に従い、runnerはその判定を上書きしない。

## 2. initial boundary

`run_stage1_candidate(setup, barrier_weight)` は `Stage1Objective` を構築し、初期stateの
value-only objectiveを一度評価してから更新loopへ入る。setup型、barrier係数、初期density、
初期objectiveの不正は実験candidateの結果ではなく呼出し・実装契約の破損なのでstatusへ丸めず
例外を伝播する。

test dataを受け取る引数は設けない。setupが保持するtrain groupsとtrain由来gridだけを使う。

## 3. declared numerical stops

| status | 正確な意味 |
| --- | --- |
| `completed` | 100回のAdam stepをacceptしcommitした |
| `no_feasible_step` | 次のAdam updateで17候補すべてstrict objectiveの定義域外だった |
| `eta_gradient_unavailable` | objectiveのeta-logit有限差分refereeがgradientを受理しなかった |
| `nonfinite_update` | current objective/gradientまたはAdam moment/updateがnonfiniteになった |
| `unsupported_gradient` | current stateが解析gradientの実装対応域外だった |

これらはoptimizer runの停止理由であり、held-out評価の `invalid` 判定ではない。予期しない
`ValueError`、`TypeError`、内部整合性の `RuntimeError` はstatusへ変換せず伝播し、bugを
candidate失敗へ偽装しない。

## 4. result interface

`Stage1CandidateRun` はstatus、最後にcommit済みのimmutable Adam state、initial/terminal
objective evaluation、accepted stepだけのbacktrack集計、accepted stepで使った最小eta
finite-difference stepを返す。完了iteration数はstateの `iteration` を唯一の正本とし、別fieldへ
複製しない。evaluation scalarはfinite、barrierは非負、etaはstateと一致することをresult境界で
検査する。

停止したstepの未commit moment、候補parameter、例外messageは返さない。barrier weight、beta、
seedは入力setup/objective側の正本を後続orchestratorが参照し、本resultへ重複記録しない。

## 5. gates

1. eta0、zero moments、iteration 0から開始し、objective増加でもearly stopせず100回を完走する。
2. 1 stepごとにstate iterationが1だけ進み、100回目のcandidate state/evaluationを返す。
3. accepted stepのbacktracked step数、総backtrack数、最大値、最小eta FD stepを集計する。
4. 4種のdeclared numerical failureを区別し、最後にcommit済みのstate/evaluationを保持する。
5. initial failureと予期しない例外をstatusへ変換せず伝播する。
6. resultへtest metric、barrier selection、sweep、artifact、GKP値が混入しない。

## 6. 実装前に確認した一次資料

- PyTorchはoptimizerの一回更新を `step()` とし、外側の固定loopから呼ぶ。本packetも既存の
  一回更新と100回runnerを分離する。
  <https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html>
- Optaxはoptimizer stateを明示的に受け、新stateを返すpure transformationとして定義する。
  本packetもcommit済みstateを次stepへ渡す。
  <https://optax.readthedocs.io/en/stable/api/transformations.html>
- SciPy `OptimizeResult` はsolution、success/status、objective、iteration数を分離して返す。
  本packetは科学的verdictを混ぜず、terminal stateと停止理由を構造化する。
  <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html>
- repository `fit_bbdagS_lossy_mixed` とexp18はeta0 `0.8`、100回の短縮Stage 1はIssue #140で
  事前宣言済みである。
