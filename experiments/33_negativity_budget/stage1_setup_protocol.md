# 負性予算 sweep Stage 1 setup packet

状態: **setup contract / pre-data-values**

Issue: #140

依存: Packet 1 fixed-beta model、Packet 2 packed parameterization。

本packetは、1つのStage 1 candidate fitが消費するtrain group、explicit grid、初期parameter
vectorを一つのsetup objectとして作る。objective、optimizer、barrier係数selection、sweep、
artifact schema、GKP値、test評価は扱わない。

## 1. authoring location とdata boundary

Stage 1 setupのinput、grid、初期化は本文書を唯一のauthoring locationとする。
`stage1_setup.py` はこの契約を実装し、testはsynthetic dataと独立計算で検査する。

入力できるのはtrain measurement groupだけである。各groupは1 mode、有限実数の
`theta` shape `(1,)` と `X` shape `(N, 1)`、`N >= 2`、正の分散を持つ。
同じthetaを重複groupとして渡さない。入力配列はcopyしてread-onlyにし、呼び出し後の
外部mutationもsetup経由のmutationも許さない。test dataを受け取る引数は設けない。

## 2. train-derived explicit grid

group `a` のtrain sampleを `x_ai`、平均を `mu_a`、母標準偏差を `sigma_a` とする。

`lower_a = min(min_i x_ai, mu_a - 6 sigma_a)`

`upper_a = max(max_i x_ai, mu_a + 6 sigma_a)`

を両端とする1025点の等間隔gridを作る。sample rangeを必ず含み、その外側も6 sigmaまで
検査する。範囲と点数はpublic APIから変更できず、test sampleやfit結果でも変更しない。
train統計、境界、gridのいずれかがfloat64でnonfiniteになればfail closedで拒否する。
group順とtheta順はinput順を保ち、grid配列もread-onlyにする。

## 3. fixed-beta feasible initialization

component shapeはpositive `(R,K,M)=(4,4,1)`、negative `(1,2,1)` とする。

`beta=0`は既存 `MixedSqueezedKetState.random_init(4,4,1,rng=seed)` をそのまま使い、
負成分を作らない。これによりexp18のpositive parameterizationと初期vectorを一致させる。

`beta>0`では、normalized rank-3 core `A` とnormalized rank-1 auxiliary `S` をseedから作る。
`w=1/4` としてphysical referenceを `rho_0=(1-w)A+wS` とし、4つのcolumnをすべて
非零にする。
Packet 1の係数を `c_positive=1+c_negative` とすると、

`rho_B = ((1-w)A + (w+c_negative)S) / c_positive`

`rho_C = S`

とする。したがって初期signed modelは
`c_positive rho_B - c_negative rho_C = rho_0` で、betaにかかわらず物理densityから始まる。
positive側の最後のK=4 columnは、SのK=2 ketを先頭へ埋め、残り2 ketの係数を0とする。

core RNGは整数seed、auxiliary RNGは `seed + 1,000,003` とし、同じ `(beta, seed)` は
barrier係数に依存せず同じ初期vectorを返す。

## 4. setup interface

`prepare_stage1_candidate(train_groups, beta, seed)` は次を返す。

- validated/copied train groups
- explicit grid groupsと、各groupのtrain統計・grid境界record
- betaとcomponent shapeだけを保持するPacket 2 parameterization
- fresh modelをpackしたread-only initial parameter vector

mutable model objectはsetupへ保持しない。後続packetはinitial vectorから評価ごとにfresh stateを
unpackする。

## 5. gates

1. gridがsample rangeとmean±6 sigmaを含み、1025点・train-only・input順に決まる。
2. invalid shape、nonfinite/complex、empty、zero variance、duplicate thetaをfail closedで拒否する。
3. beta=0 initial vectorが既存random initとarray-identicalである。
4. beta>0でpositive/negative normが1、positiveの4 columnがすべて非零で、初期signed
   densityが独立構成した4-column physical referenceと一致する。
5. input mutationがsetupへ伝播せず、返却配列をmutationできず、同じ
   `(train, beta, seed)` が同じsetupを返す。
6. beta domain、seed、float64でnonfiniteになるtrain統計・grid境界をfail closedで検証する。

## 6. deferred packet

次packetがこのsetupを消費し、strict train NLL、Packet 2 barrier、state/eta gradientを
一つのobjective interfaceとして定義する。その後にoptimizer/backtracking、barrier係数selection、
artifact schemaをそれぞれ別packetで追加する。
