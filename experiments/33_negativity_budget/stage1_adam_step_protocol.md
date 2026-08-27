# 負性予算 sweep Stage 1 Adam step packet

状態: **one-step optimizer contract / pre-data-values**

Issue: #140

依存: Stage 1 train objective。

本packetは、objectiveの現在gradientからAdam候補を一つ作り、strict objectiveが定義できる
最初のscaleだけをcommitする一回の状態遷移を定義する。100-iteration runner、停止status、
barrier係数selection、sweep、artifact、実データ値、test評価は扱わない。

## 1. authoring location と固定schedule

一回のAdam更新、moment commit、feasibility backtrackingは本文書を唯一のauthoring
locationとする。objective値・gradientの定義は `stage1_objective_protocol.md` を参照する。

| 項目 | 固定値 / 意味 |
| --- | --- |
| learning rate | `0.05`。exp18 baselineと同一 |
| Adam beta1 / beta2 / epsilon | `0.9 / 0.999 / 1e-8`。exp18 baselineと同一。moment更新の補数係数は、同じfloat64演算順を保つためexp18と同じリテラル `0.1 / 0.001` を使う |
| backtrack scale | `1, 1/2, ..., 1/2^16` |
| acceptance | candidateでstrict objective valueが定義されfinite |

16回の縮小は、最小scale `1/65536` まで約5桁を探索しつつ、candidate value評価を最大17回へ
固定するpre-dataのengineering capである。統計的意味や収束保証は持たない。

## 2. immutable optimizer state

`Stage1AdamState` はpacked state parameters、eta logit、state-plus-logit gradientと同長の
first/second moments、完了済みiteration数を保持する。配列は有限実数のcopyをread-onlyで
保持し、second momentは非負、iterationは非負整数とする。

本packetは初期state helperを設けない。後続runnerがsetup initial vector、eta初期値、zero
moments、iteration 0からstateを構築する。これによりeta初期値とrunner scheduleを先取りしない。

## 3. one-step transition

入力stateの完了済みiterationを `k` とし、objectiveのpacked gradientを `g` とする。
exp18と同じAdam式でiteration `k+1` のtrial moments、bias correction、full updateを計算する。

full updateをparametersとeta logitへ同じscaleで適用し、objectiveのvalue-only経路を評価する。
invalidならscaleを1/2へ縮め、最初のvalid candidateを採用する。gridの負densityはbarrierの
対象であり、train strict likelihoodが定義できる限りcandidate拒否理由にしない。

accepted時だけ、candidate parameters、eta logit、**full gradientから作ったtrial moments**、
iteration `k+1` を新しいread-only stateへcommitする。backtrack scaleはmomentを縮めない。
全17候補がinvalidなら `NoFeasibleAdamStep` を返し、入力stateもtrial momentsもcommitしない。

## 4. feasibility と objective decrease の分離

本backtrackingはArmijo/Wolfe line searchではなく、strict objectiveの定義域を守るだけである。
Adam updateは降下方向とは限らないため、objective decreaseをacceptance条件へ混ぜない。
validだがobjectiveが増えたcandidateもこのone-step interfaceではacceptする。収束・停止判断は
後続runner packetが別に定義する。

current objective/gradientがnonfinite、eta gradientがunavailable、analytic Jacobian対象外なら、
本packetは例外を変換せずfail closedで上へ返す。candidate valueのinvalidだけをbacktrackする。

## 5. result interface

`Stage1AdamStepResult` はaccepted state、source/candidate evaluation、backtrack回数、採用scale、
objectiveが使ったeta finite-difference stepを返す。fit status、test metric、解釈文は含めない。

## 6. gates

1. beta=0、zero moments、iteration 0、backtrackなしの一歩がexp18 Adam式と一致する。
2. nonzero momentsとiterationでbias correctionが独立計算と一致する。
3. parametersとeta logitへ同じscaleを適用し、最初のvalid candidateだけをcommitする。
4. accepted時はfull gradientのtrial momentsをcommitし、全候補invalid時は入力を変更しない。
5. objective decreaseを要求せず、validな増加candidateもacceptする。
6. invalid shape、length、nonfinite gradient/moment/updateをfail closedで拒否する。
7. resultへrunner status、barrier selection、実データ値、test metricが混入しない。

## 7. 実装前に確認した一次資料

- Optax backtracking line searchはAdam updateが降下方向とは限らず、Armijo条件が成立しない場合を
  明記する。本packetはこの理由でdecrease条件を使わない。
  <https://optax.readthedocs.io/en/latest/api/generated/optax.scale_by_backtracking_linesearch.html>
- PyTorch AMPはgradientがnonfiniteならoptimizer stepをskipし、parameterへcommitしない。
  <https://docs.pytorch.org/docs/main/notes/amp_examples.html>
- PyTorch autograd mechanicsは未定義演算を後からmaskせず、演算前に定義域を分ける。
  <https://docs.pytorch.org/docs/stable/notes/autograd.html>
- repository `fit_bbdagS_lossy_mixed` は上記Adam定数・bias correctionを使うexp18 baselineである。
