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
`MixedSqueezedKetState` modelとする。負性予算を `0 <= beta < 1/2` とし、
pre-normalizationの正・負massを `1-beta` と `beta` に固定する。報告modelは

`rho_beta = ((1-beta) rho_B - beta rho_C) / (1-2 beta)`

である。したがってtraceは1だが、`beta > 0`ではPSDも測定密度の非負性も保証しない。
`beta` はこの差分構成のpre-normalization負mass比であり、Fock射影後の負固有値絶対値和や
Wigner負体積とは別の量である。

同じloss channel parameter `eta` を両成分へ適用してから線形結合する。
`beta=0`では負成分を構築せず、既存のpositive modelとparameterizationごと同一にする。

## 3. fail-closed evaluation boundary

- 各measurement groupは `X` shape `(N, M)`、`theta` shape `(M,)`、`N >= 1` とし、
  不一致はdensity評価前に拒否する。
- forward評価はsigned densityをclip・floor・renormalizeしない。
- held-out sampleの1点でもdensityが非finiteまたは0以下なら、そのfitはinvalidとし
  NLLを返さない。
- 正の全sampleに対してだけ、per-sample `-log(p)` とそのmeanを返す。
- dense-grid barrierとそのgradientはpacket 2で追加する。packet 1のmodelを変更せず消費する。

## 4. packet 1 gates

1. `beta=0`が既存`lossy_pdf_mixed` / `nll_lossy_mixed`と一致する。
2. 各成分densityが正規化されている場合、signed densityも積分1になる。
3. 負densityを観測可能な形で保持し、strict NLLが拒否する。
4. beta domain、成分shape、mode不一致、非finite normをfail closedで拒否する。
