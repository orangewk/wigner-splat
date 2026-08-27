# 負性予算 sweep Stage 1 objective packet

状態: **objective contract / pre-data-values**

Issue: #140

依存: Packet 1 strict likelihood、Packet 2 density Jacobian / explicit-grid barrier、
Stage 1 candidate setup。

本packetは、一つのsetupを一つのtrain objectiveへ結ぶ。optimizer、invalid stepの
backtracking、barrier係数selection、sweep、artifact schema、実データ値、test評価は扱わない。

## 1. authoring location と入力境界

Stage 1 objectiveの合成、eta parameterization、返却interfaceは本文書を唯一のauthoring
locationとする。strict likelihoodの定義は `protocol.md`、裸のgrid barrierとstate
Jacobianの定義は `packet2_protocol.md`、train/grid生成は `stage1_setup_protocol.md` を参照し、
ここで別実装しない。

`Stage1Objective` は次だけを保持する。

- `prepare_stage1_candidate` が返した一つのsetup
- train-onlyで後続packetが選ぶ有限・非負のbarrier係数 `lambda`

raw train/test group、grid設定、component shapeを別引数として受け取らない。`lambda=0` は
barrierなしの検算を許すが、係数候補と選択規則は後続packetが宣言する。

## 2. objective value

Packet 1のpooled per-sample strict train NLLを `NLL_train`、Packet 2のequal-group
explicit-grid barrierを `B_grid` とし、本packetが新たに定義する合成は

`L = NLL_train + lambda B_grid`

である。train densityのclip、floor、renormalizeを追加しない。train densityが一点でも
nonfiniteまたは0以下ならPacket 1の `NonPositiveDensityError` をそのまま返す。

`Stage1ObjectiveEvaluation` は `objective`、`train_nll`、`barrier`、`eta` の4 scalarだけを
返す。test metric、fit status、解釈文は含めない。

eta有限差分のvalue-only評価ではgrid Jacobianを作らない。Packet 2に追加する
`dense_grid_barrier` と既存 `dense_grid_barrier_and_grad` は同じ内部reducerを使い、
二乗hingeとgroup weightingを二重authoringしない。

## 3. state gradient と eta-logit gradient

etaは既存exp18と同じく `eta=sigmoid(t)` のlogit `t` で渡し、float64で厳密に
`0 < eta < 1` へ写らない値をfail closedで拒否する。

state gradientはPacket 2のsample density Jacobianへstrict NLLのchain ruleを適用し、
Packet 2のbarrier gradientへ `lambda` を掛けて加える。返却gradientはPacket 2 packed
state vectorの後ろへ `dL/dt` を1 scalar連結したread-only vectorとする。

`dL/dt` はobjectiveの同じvalue経路を使う中心差分で計算する。初期stepは `1e-4`。
片側がstrict likelihoodまたは有限性の定義域外ならstepを半分にし、最大12回のhalvingを
許す。両側が有効なstepを得られなければ `EtaGradientUnavailable` として終了する。

## 4. gates

1. valueがPacket 1 strict train NLLとPacket 2 value-only barrierの宣言済み合成に一致する。
2. value-only barrierと既存value-and-gradient barrierが同じ値を返す。
3. beta=0とbeta>0のstate gradientが全packed parameterの独立中心差分と一致する。
4. eta-logit gradientがobjective valueの独立中心差分と一致する。
5. nonpositive train density、invalid setup/parameter/eta-logit/barrier係数をfail closedで拒否する。
6. adaptive eta stepが最初に有効な対称stepを採用し、12 halvingsでも得られなければ停止する。
7. objective resultへtest data、optimizer state、実データ値が混入しない。

## 5. 実装前に確認した一次資料

- SciPy `check_grad`: scalar functionの解析gradientと有限差分を独立比較するinterface。
  <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.check_grad.html>
- JAX `value_and_grad`: 同じscalar objectiveからvalueとgradientを返すinterface。
  <https://docs.jax.dev/en/latest/_autosummary/jax.value_and_grad.html>
- PyTorch autograd mechanics: 未定義演算を後段でmaskせず、演算前に定義域を分ける原則。
  <https://docs.pytorch.org/docs/stable/notes/autograd.html>
- exp18 `fit_bbdagS_lossy_mixed`: eta-logitと `1e-4` 中心差分を使う既存repository baseline。
