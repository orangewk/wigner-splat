# 補題 W/W′: 三原子 Wronskian valuation 上界

日付: 2026-08-11 / 著者: 本線 / status: **v0.2.1 — plain W accepted (R-W PASS)、static generalized W′ accepted (R-W′ PASS)**

> 本ファイルを plain c=3 の補題 W、static nested-limit の補題 W′、その直接帰結の唯一の authoring location とする。
> F3′ witness の式と border-rank 帰結は
> [FR仕様 §7](2026-08-10-three-atom-block-frame-preparation--wip.md)を参照し、本書では複製しない。
> W′ は `{e^p,Pe^p,e^q}` という静的極限だけを扱う。finite-m nested 2+1 の ν-chart/exact factorization、
> 一般 c、FR-S4 envelope は主張しない。

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

`v_i` は相異なるので先頭係数は非零。

ここで higher terms が同じ位数へ戻って先頭項を消すことはない。Wronskian の多重線形展開で、
各単項式組の位数は「三列の次数和 − 3」であり、いずれかの列を `v_i` より高い Taylor 項へ
置き換えれば次数和は狭義に増える。次数が重複する単項式組の determinant は零なので、表示した
falling-factorial Vandermonde が最低位数の非零係数として残る。

  ord_0 Wr(u_1,u_2,u_3)=v_1+v_2+v_3−3.                         (W3)

また `u_j(0)=1` なので `W` 上の `z=0` 評価は非零であり `v_1=0`。valuation profile は
非負整数の狭義増加列なので `v_2≥1` である。(W1)–(W3) より

  v_1+v_2+v_3=3+ord_0V≤6,

ゆえに `v_3≤6−0−1=5`。これで補題 W が示された。∎

## 5. J⁵ injectivity and compact-family corollary

任意の非零 `f=Σ_i a_i g_i` では、`v_i` が相異なるため、最小の
`v_i` を持つ非零係数の先頭項は他項と相殺しない。従って `ord_0f` はその `v_i` に等しく、特に
`ord_0f≤v_3` である。`T_5 f=0` なら `ord_0 f≥6` だが、補題 W の `v_3≤5` に反するので
`f=0`。従って `T_5` は単射。

さらに、parameter triple の compact 集合 `Θ` が pairwise collision を避けるとする。係数空間に
標準 `ℓ²`、`J^5` に Bargmann–Fock 計量を入れ、

  T_θ:ℂ³→J^5,  a↦Taylor_≤5(Σ_j a_j exp(A_jz²/2+B_jz))

と置く。各 `T_θ` は単射で、最小特異値は `θ` に連続である。compactness より

  inf_{θ∈Θ} σ_min(T_θ)>0.                                       (W4)

(W4) は single-scale triple の weighted SVD route で使う head bound である。ただし weighted
rescaling、Fock tail、nested 2+1 は本補題の外で、FR-S1′ 側の別証明義務とする。

## 6. 補題 W′: static generalized 2+1 limit

二つの child-limit 関数が同じ指数 `e^p` を共有し、singleton が `e^q` である静的空間を考える。
`p,q` は複素二次以下、`r:=q−p` は非定数とする。`P` は非定数多項式 `deg P≤2` とし、

  W_gen:=span{e^p,Pe^p,e^q}

と置く。`P` から定数項を引いても `span{e^p,Pe^p}` は変わらず、`r` の定数項は
singleton の非零 scalar に吸収できるので、wlog

  P(z)=c_2z²+c_1z,  (c_1,c_2)≠(0,0),
  r(z)=az²/2+bz,     (a,b)≠(0,0)

とする。共通の nonvanishing factor `e^p` を掛け外しても各関数の `ord_0` は変わらないため、
`W_gen` の valuation profile は `span{1,P,e^r}` の profile `w_1<w_2<w_3` と同じである。

**補題 W′ (static generalized 2+1)**:

  w_1=0,  w_1+w_2+w_3=3+ord_0H≤6,  特に w_3≤4,

ここで `L:=r′=az+b`、

  H(z):=P′(r″+(r′)²)−P″r′.

上界 `w_3≤4` は `P∝z²`, `r∝z²` の profile `(0,2,4)` で sharp。

### 6.1 Wronskian factorization and nonvanishing

直接計算で

  Wr(1,P,e^r)=e^r H(z),                                         (W′1)

かつ

  H(z)=2a²c_2z³+a(ac_1+4bc_2)z²
       +2b(ac_1+bc_2)z+(ac_1+b²c_1−2bc_2).                     (W′2)

`H` は常に非零である。

1. `a≠0, c_2≠0`: `z³` 係数 `2a²c_2≠0`。
2. `a≠0, c_2=0`: `c_1≠0` なので `z²` 係数 `a²c_1≠0`。
3. `a=0`: `b≠0` で
   `H=b(2bc_2z+bc_1−2c_2)`。`c_2≠0` なら一次係数、`c_2=0` なら定数 `b²c_1` が非零。

従って `dim W_gen=3`、`deg H≤3`。§4 と同じ adapted-basis Wronskian 恒等式から

  w_1+w_2+w_3=3+ord_0H≤6.                                      (W′3)

また `1∈W_gen` なので `w_1=0`。

### 6.2 Refinement from 5 to 4

`ord_0H≤2` なら (W′3) と `w_2≥1` から直ちに `w_3≤4`。

`ord_0H=3` とする。このとき `a,c_2≠0` で、(W′2) の一次・二次係数の消滅から

  b(ac_1+bc_2)=0,  a(ac_1+4bc_2)=0.

もし `b≠0` なら `ac_1+bc_2=ac_1+4bc_2=0` から `3bc_2=0` となり矛盾。
従って `b=0`、さらに `ac_1=0` から `c_1=0`。よって

  P=c_2z²,  r=az²/2,

であり、`e^{az²/2}=1+(a/2)z²+(a²/8)z⁴+⋯` から profile は exact に `(0,2,4)`。
従って全場合で `w_3≤4`、かつ上界は sharp。∎

### 6.3 J⁴ and compact-family corollary

§5 と同様、非零元の消滅次数は `w_3≤4` なので `J⁴` 切断は `W_gen` 上で単射。
さらに `‖(c_1,c_2)‖_2=1` と正規化し、`|a|,|b|≤R`、
`max(|a|^{1/2},|b|)≥η>0` とする compact family 上では、対応する `J⁴` map の
最小特異値は連続・各点正なので一様に正である。

この corollary は finite-m nested chart の `t=0` face にだけ使う。`t>0` child column、ν-chart、
root-scale tail は FR-S1″ 側の別義務である。

## 7. Scope ledger

| claim | status | dependency / non-claim |
|---|---|---|
| Wronskian factorization (W1) | accepted (R-W PASS) | 直接微分と determinant 恒等式 |
| `V≢0`, `deg V≤3` | accepted (R-W PASS) | `A_j` 一致型の三場合 |
| `Σv_i=3+ord_0V≤6`, `v_3≤5` | accepted (R-W PASS) | (W1)–(W3) |
| `T_5` injective / compact-family lower bound | accepted (R-W PASS) | 補題 W + compactness |
| sharpness `v_3=5` | referenced | FR仕様 F3′ が authoring location |
| static generalized W′ factorization / `Σw_i≤6` | accepted (R-W′ PASS) | (W′1)–(W′3) |
| static generalized bound `w_3≤4` | accepted (R-W′ PASS) | §6.2 case split |
| static generalized `J⁴` compact floor | accepted (R-W′ PASS) | W′ + compactness |
| finite-m nested 2+1 / ν-chart | open, not claimed here | [FR文書 §9](2026-08-10-three-atom-block-frame-preparation--wip.md)に proof draft、R-A″ pending |
| 一般 c の次数公式 | open, not claimed | 本書から外挿しない |
| FR3 envelope / FR5–FR7 | open, not claimed | FR-S4 の義務 |

## 8. Review history

- R-W (`1b3e337`, Fable response `5249273110`): R-W1–R-W5 全 PASS、blocking なし。
  §4 の higher-term 非相殺と §5 の `ord_0f≤v_3` を明記する nonblocking minor 2 件を v0.1.1 で反映。
- v0.2(2026-08-11): Fable consultation #2 の GO を受け、static generalized W′ を proof draft として追加。
  finite-m nested chartやFR-S1″の閉鎖には数えず、固定 SHA R-W′ 待ち。
- v0.2.1(2026-08-11): 固定 SHA `57ff88d` の Fable response `5250516558` で
  R-W′1–R-W′5 が全 PASS、blocking なし。
  nonblocking minor 1 件として §4 の宙に浮いた「従って」を削除。static generalized W′ と
  `J⁴` compact floor を accepted に昇格した。finite-m nested 2+1 / FR-S1″ は open のまま。
