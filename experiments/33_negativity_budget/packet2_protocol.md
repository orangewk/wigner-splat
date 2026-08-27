# 負性予算 sweep packet 2: density Jacobian と grid barrier

状態: **packet 2 / pre-data-values**

Issue: #140

本packetは、packet 1のfixed-beta forward modelを変更せず、state parameterに関する
density Jacobianと、呼び出し側が明示したgrid上の負値barrierを定義する。

## 1. authoring location と境界

Packet 2の勾配・barrier契約は本文書を唯一のauthoring locationとする。
`packet2.py` はこの契約を実装し、専用testは中心差分を含む別計算で検査する。
fixed-beta modelの意味、beta範囲、評価時のfail-closed条件は `protocol.md` を参照する。

| 項目 | 本packetでの扱い |
| --- | --- |
| packed state vector | 正成分、続いて負成分。各成分内は既存 `_pack_mixed` と同順 |
| beta | vector外の固定knob。packet 1の値をそのまま消費 |
| eta | Jacobianに含めない。後続optimizerでlogit scalarの別勾配として扱う |
| grid | `(theta, X_grid)` の非空group列を呼び出し側が明示する |
| grid生成規則・barrier係数 | stage 1 protocolでtrain dataだけを使って宣言する |
| optimizer・NLLのinvalid step処理 | stage 1 runner packetへ送る |
| GKP値・stage 1/2 result | 読まない、生成しない |

可変状態はpacked real vectorだけとする。shape-only parameterizationはmutableな状態配列を
保持せず、各評価で正・負成分を新しくunpackする。packet 1で検証済みのmodel objectを
in-place更新しない。

## 2. analytic density Jacobian

1 measurement groupのsample数を `S`、packed parameter数を `P` とすると、
component interfaceはdensity shape `(S,)` とJacobian shape `(S, P)` を同じforward評価から返す。
parameter順は `_pack_mixed` と一致する。total convolution variance
`(1-eta)/2 + extra_noise_var` が `1e-14` 以下のpure-detection経路は、本packetの
rank-R analytic Jacobian対象外として拒否する。

packet 1の係数を `c_positive`, `c_negative`、component density/Jacobianを
`p_B, J_B, p_C, J_C` と書く。signed interfaceは

`p = c_positive p_B + c_negative p_C`

`J = [c_positive J_B, c_negative J_C]`

を返す。`beta=0`では負成分blockを作らず、既存component density/Jacobianと
配列値・parameterizationが同一である。Jacobianはstate parameterだけを微分し、
beta、eta、noise parameterは含まない。

各PSD componentの既存forwardは、丸めでraw numeratorが0以下になった点を0へclipする。
analytic Jacobianも同じ実装関数の導関数として、その点では0を返す。signed合成後は
clip、floor、renormalizeを行わない。

## 3. explicit-grid negativity barrier

measurement group数を `A`、group `a` の明示grid点数を `N_a` とする。barrierは

`B = (1/A) sum_a (1/N_a) sum_i min(p_ai, 0)^2`

とする。sample数をpoolせず、各measurement groupを等しく重み付けする。gradientは

`grad B = (1/A) sum_a (1/N_a) sum_i 2 min(p_ai, 0) J_ai`

である。`p=0`では値・gradientとも0で、二乗hingeはこの境界で1階連続である。
この関数は係数を掛けない裸のbarrierを返す。stage 1 runnerがtrain-onlyの感度確認後に
係数を掛ける。

後続objectiveのeta有限差分はgradientを必要としないため、値だけを返す内部helperを
用意する。公開interfaceは増やさず、値だけの経路とgradient経路は同じ内部reducerを使い、
上の二乗hingeとequal-group meanを別実装しない。

## 4. packet 2 gates

1. component density Jacobianが既存forward値と一致し、全parameterで中心差分と一致する。
2. component Jacobianから集約したNLL gradientが既存analytic NLL gradientと一致する。
3. `beta=0`がcomponent interfaceと配列値まで一致する。
4. signed density Jacobianがpacket 1 forward値および中心差分と一致する。
5. 複数group・不均一点数のbarrierが上式の等group平均と一致し、gradientが中心差分と一致する。
6. parameter長・finite条件、空grid、shape、pure-detection対象外をfail closedで拒否する。
7. rank上限内で一部column normが厳密に0の状態を受け入れ、そのcolumnのdensity寄与と
   一階gradientを0として扱う。

## 5. 実装前に確認した一次資料

- SciPy `NonlinearConstraint`: vector functionのJacobianを `(m, n)` とする契約。
  <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.NonlinearConstraint.html>
- JAX `value_and_grad`: scalar valueとgradientを同じ関数評価のinterfaceで返す設計。
  <https://docs.jax.dev/en/latest/_autosummary/jax.value_and_grad.html>
- PyTorch `gradcheck` mechanics: analytic Jacobianと中心差分Jacobianの独立比較。
  <https://docs.pytorch.org/docs/stable/notes/gradcheck.html>
