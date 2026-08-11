# 補題 W: 三原子 Wronskian valuation 上界 — proof draft

日付: 2026-08-11 / 著者: 本線 / status: **v0.1 proof draft — fixed-SHA review pending**

> 本ファイルを plain c=3 の補題 W とその帰結の唯一の authoring location とする。
> F3′ witness の式と border-rank 帰結は
> [FR仕様 §7](2026-08-10-three-atom-block-frame-preparation--wip.md)を参照し、本書では複製しない。
> 本書は nested 2+1 の一般化原子、一般 c、FR-S4 envelope を主張しない。

## 1. Statement

相異なる parameter pair `(A_j,B_j)∈ℂ²` (`j=1,2,3`) に対し

  p_j(z):=A_jz²/2+B_jz,  u_j(z):=exp(p_j(z)),  W:=span{u_1,u_2,u_3}

と置く。`W` の `z=0` における valuation profile を `v_1<v_2<v_3` とする。すなわち、
Taylor 係数について Gaussian elimination して得られる adapted basis `g_i∈W` の消滅次数
`ord_0(g_i)` を昇順に並べたものとする。

**補題 W (plain c=3)**:

  v_1=0,  v_1+v_2+v_3=3+ord_0 V≤6,  特に v_3≤5,

ここで `ℓ_j(z):=A_jz+B_j` とし、

  V(z):=Π_{1≤i<j≤3}(ℓ_j(z)−ℓ_i(z))
        +det[[1,1,1],[ℓ_1,ℓ_2,ℓ_3],[A_1,A_2,A_3]].

従って、5-jet 切断 `J^5:=span{1,z,…,z^5}` への写像

  T_5:W→J^5,  f↦Taylor_≤5(f)

は単射である。上界 `v_3≤5` は F3′ により sharp である。

## 2. Wronskian factorization

`u_j′=ℓ_ju_j`、`u_j″=(A_j+ℓ_j²)u_j` なので、列ごとに `u_j` を括ると

  Wr(u_1,u_2,u_3)
  =exp(p_1+p_2+p_3) det[[1,1,1],[ℓ_1,ℓ_2,ℓ_3],
                              [A_1+ℓ_1²,A_2+ℓ_2²,A_3+ℓ_3²]].

第三行の線形性と三次 Vandermonde 恒等式より

  Wr(u_1,u_2,u_3)=exp(p_1+p_2+p_3)V(z).                         (W1)

`exp(p_1+p_2+p_3)(0)=1` なので `ord_0 Wr(u_1,u_2,u_3)=ord_0V` である。

第二の determinant は実際には定数である。第二行を
`(A_1,A_2,A_3)z+(B_1,B_2,B_3)` に分けると、`z` の係数は
第一行と第三行を含む determinant `det[1;A;A]=0` だからである。

## 3. `V` is nonzero and `deg V≤3`

`A_j` の一致型で場合分けする。

1. **三つの `A_j` が全て相異**: Vandermonde 積の `z³` 係数は
   `Π_{i<j}(A_j−A_i)≠0`。第二 determinant は定数なので打ち消せない。
2. **ちょうど二つが等しい**: 添字を替えて `A_1=A_2≠A_3` とする。parameter pair が
   相異なので `B_1≠B_2`。Vandermonde 積の `z²` 係数は
   `(B_2−B_1)(A_3−A_1)²≠0`。第二 determinant は定数なので打ち消せない。
3. **三つとも等しい**: parameter pair の相異性から `B_1,B_2,B_3` は全て相異。
   Vandermonde 積は非零定数 `Π_{i<j}(B_j−B_i)`、第二 determinant は第三行が
   第一行の定数倍なので零。

全場合で `V` は非零多項式かつ `deg V≤3`。従って

  ord_0 V≤deg V≤3.                                               (W2)

(W1) は同時に `Wr(u_1,u_2,u_3)≢0` を与えるので `dim W=3` も本書内で従い、
指数多項式独立性の外部補題には依存しない。

## 4. Valuation identity

adapted basis を

  g_i(z)=c_i z^{v_i}+O(z^{v_i+1}),  c_i≠0,  v_1<v_2<v_3

と取る。`g_i` は `u_j` の定数係数基底変換なので、Wronskian は非零定数倍だけ変わる。
一方、上の先頭項を Wronskian に代入すると falling-factorial Vandermonde により

  Wr(g_1,g_2,g_3)
  =(c_1c_2c_3)Π_{i<j}(v_j−v_i)
    z^{v_1+v_2+v_3−3}+higher terms.

`v_i` は相異なるので先頭係数は非零。従って

  ord_0 Wr(u_1,u_2,u_3)=v_1+v_2+v_3−3.                         (W3)

また `u_j(0)=1` なので `W` 上の `z=0` 評価は非零であり `v_1=0`。valuation profile は
非負整数の狭義増加列なので `v_2≥1` である。(W1)–(W3) より

  v_1+v_2+v_3=3+ord_0V≤6,

ゆえに `v_3≤6−0−1=5`。これで補題 W が示された。∎

## 5. J⁵ injectivity and compact-family corollary

`T_5 f=0` なら `ord_0 f≥6`。補題 W の `v_3≤5` に反するので `f=0`、従って `T_5` は単射。

さらに、parameter triple の compact 集合 `Θ` が pairwise collision を避けるとする。係数空間に
標準 `ℓ²`、`J^5` に Bargmann–Fock 計量を入れ、

  T_θ:ℂ³→J^5,  a↦Taylor_≤5(Σ_j a_j exp(A_jz²/2+B_jz))

と置く。各 `T_θ` は単射で、最小特異値は `θ` に連続である。compactness より

  inf_{θ∈Θ} σ_min(T_θ)>0.                                       (W4)

(W4) は single-scale triple の weighted SVD route で使う head bound である。ただし weighted
rescaling、Fock tail、nested 2+1 は本補題の外で、FR-S1′ 側の別証明義務とする。

## 6. Scope ledger

| claim | status | dependency / non-claim |
|---|---|---|
| Wronskian factorization (W1) | proof draft | 直接微分と determinant 恒等式 |
| `V≢0`, `deg V≤3` | proof draft | `A_j` 一致型の三場合 |
| `Σv_i=3+ord_0V≤6`, `v_3≤5` | proof draft | (W1)–(W3) |
| `T_5` injective / compact-family lower bound | proof draft | 補題 W + compactness |
| sharpness `v_3=5` | referenced | FR仕様 F3′ が authoring location |
| nested 2+1 / generalized atoms | open, not claimed | 別補題が必要 |
| 一般 c の次数公式 | open, not claimed | 本書から外挿しない |
| FR3 envelope / FR5–FR7 | open, not claimed | FR-S4 の義務 |
