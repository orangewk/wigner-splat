# 三原子 exact block-frame preparation (FR) — statement wip

日付: 2026-08-10 / 著者: 本線 / status: **v0.14.3 — FR-S1′/FR-S1″ accepted、base FR-S4-0 interface accepted (R-S4-0 R9 PASS、fixed SHA `56498bb`)、補題 RF accepted(R-RF R2 PASS `9f19389`、minors `c271919`)、`root-far` row resolved + 昇格監査 accepted(R-RF-PROMOTE、§10.7)、polynomial ΣA program PΣ-1/2/3/4 accepted(R-PS4 R3 PASS `58b9c9f`、§10.5.4/§10.7)、S4b-COV0/COV1 accepted(R-COV1 R4 PASS `c36d818`、§10.5.5)— **S4b closure 完結**、**S4a program 完結・(S4-Ew) 閉鎖**(§10.8 全 8 packet accepted、R-EW R2 PASS `b39216f`)、S4c open**

> 本ファイルを c=3 FR の唯一の authoring location とする。由来は
> [三原子一遷移文書 §3.7.5](2026-08-09-three-atom-one-transition--wip.md)の命題 DC-NG。
> DC-NG は固定 SHA `1392266` の R-DCNG(A1–A7) PASS。tree-envelope QR5(U_T) は
> 固定 SHA `27a1817` の R-P3 PASS。本ファイルはその先の未証明契約を定義する。

## 1. 目的と非目的

目的は、三原子の**与えられた一つの係数表示**に付随する individual envelope U_F を救うことではない。
near-phantom 族では direct U_F transfer と、予定していた QR5 child から U_F へ戻す旧 DC bridge が
同時に破れる。必要なのは、三原子 **span 全体**の中で cancellation-aware な exact frame を選び直すこと。

この仕様は次を主張しない。

- direct U_T→U_F 比較。
- wrapper Γ(3) の値または上界。
- QR5 だけから Gram 一様可逆性が従うこと。
- FR の存在証明。以下は proof obligation の固定である。

## 2. 入力

コンパクトな Gaussian parameter class K_{δ,R} 内の三原子列

  u_{j,m} = Φ(ξ_{j,m})  (j=1,2,3),

と V_m := span{u_{1,m},u_{2,m},u_{3,m}} を取る。本仕様は補題 N の**一つの衝突cluster**を入力とし、
constant-gauge quotient 後に一つの `d_Ω`-衝突 cluster (`ξ_{j,m}→ξ*`、全 j)を入力とする。
`d_Ω` は粗い cluster 分離にだけ使い、衝突内部の scale は次の weighted metric で測る。

active node ごとに pivot leaf `j_0` を固定し、共通 metaplectic gauge `U_m` で
`Φ(ξ_{j_0,m})` を真空へ移す。生じる非零 scalar は原子係数へ exact に吸収し、gauge 後の parameter を
`(A_{j,m},B_{j,m})`、pivot を `(0,0)` と書く。真空 stabilizer は
`(A,B)↦(e^{2iφ}A,e^{iφ}B)` なので、

  d_w((A,B),(A′,B′)) := max(|A−A′|^{1/2}, |B−B′|)

は residual gauge に依存しない。`|·|^{1/2}` の snowflake 三角不等式と max 構成から `d_w` は metric である。
以下 `d_w(ξ_{i,m},ξ_{j,m})` は、この共通 gauge 後の parameter 座標間距離の略記とする。
node scale を

  s_m := max_{i,j} d_w((A_{i,m},B_{i,m}),(A_{j,m},B_{j,m})) → 0

と定義する。pivot の選択は permutation/chart data に含める。`s_m` が 0 へ行かない別 cluster は
入力前に `d_Ω` で分離し、L3/cluster tree の別節点で扱う。

leaf weight w=1 は再帰の終端とし、距離正規化を行わない。w≥2 の active cluster node では、
normalized distance `d_w(ξ_{i,m},ξ_{j,m})/s_m` を部分列で全対収束させる。極限 0 の pair は
proper child cluster とし、その child scale で同じ操作を再帰する。c=3 では tree shape は single-scale triple または
2+1(root scale)の pair child(single scale)だけで、再帰深さは高々2。各 active node では非零 pair-distance ratio が
正の下限を持つ。この nested tree、r := dim V_m、pivot permutation を部分列で固定する。
constant gauge を先に quotient する。すなわち radial 表現で q_i−q_j≡const(同値に対応する
Fock 原子が非零定数比)なら、その定数を係数へ吸収して同一原子として exact に合算する。
合算係数が 0 なら削除し、併合後の leaf weight w ∈ {1,2,3}、r := dim V_m ≤ w、tree を再固定する。
基底変換係数の m 一様有界性は要求しない(補題 N の N3′ と整合)。

radial restriction z=te^{iθ} では各 exact 結合を二次位相指数和として読む。one-transition chart では、
pair が全 K 上 held、triple が source interval 上 held という三原子文書の規約を用いる。

## 3. exact block tree

枠候補 h_{ℓ,m} は原子の exact 有限結合

  h_{ℓ,m} = Σ_{j=1}^3 a_{ℓj,m}u_{j,m}

であり、原子 index の grouping として rooted binary block tree を付す。tree 自体は θ に依存させず、
各 radial restriction は同じ grouping を継承する。

- leaf: 一つの原子。
- internal node: 子 A,B の exact 和 H=A+B。
- node envelope: U_H(t) := max(log|A(t)|, log|B(t)|)。零点では log 0 := −∞。

三原子の非自明な tree shape は、置換を除けば「pair block + singleton」だけである。tree shape と
pivot permutation は有限なので、必要なら部分列で固定する。node envelope は解析上の補助量であり、
旧 parent U_F への逆比較を要求しない。

## 4. 予想 FR3(one-transition exact block-frame preparation)

上の入力に対し、部分列と r 本の exact 結合 h_{1,m},…,h_{r,m} を選び、
v_{ℓ,m}:=h_{ℓ,m}/‖h_{ℓ,m}‖ と置くと、次を同時に満たせると予想する。

| ID | obligation | acceptance condition |
|---|---|---|
| FR1 | exact span | span{h_{ℓ,m}:ℓ≤r}=V_m。削除は exact rank drop のときだけ |
| FR2 | finite chart | permutation・tree shape・valuation profile が部分列上で固定。F3′ 後の Route A′ では rate degeneration は SVD の特異値が担い、有限 label へ列挙しない |
| FR3 | generalized-atom type | 共通 cluster base ξ_{*,m}→ξ* と jet-degree label d_ℓ を持ち、各有限 v_{ℓ,m} が (X)/(L-d) を満たす。特に非零 P_ℓΦ(ξ*) (deg P_ℓ=d_ℓ) へ norm 収束。旧 `o′_ℓ≤w−1, deg P_ℓ≤2o′_ℓ` 帳簿は F3′ により撤回。plain c=3 の上界 d_ℓ≤5 は [補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md) が R-W PASS (`1b3e337`)。nested 2+1 の (X)/(L-d) は FR-S1″ が R-A″ PASS (`61111cc`)。c=3 の遠方成長 target は §10 の弱形 (E-w)へ仕様改訂中。(E-d) は一般 c の再帰義務として残す。枠本数 r≤w≤3 |
| FR4 | Gram | Gram(v_{1,m},…,v_{r,m}) の最小固有値が m 一様に正 |
| FR5 | node kernel | 各 radial internal node はその node envelope 固有の reviewed kernel を、m と θ に一様な定数で持つ。2+1 held node は QR5(U_T) |
| FR6 | global envelope | c=3 では各 v_{ℓ,m} が §10 の (E-w) と、改訂後の N3′/N4 acceptance を満たす。定数は (c=3,δ,R,per-node segmentation/flag の安定化定数) のみに依存し m,θ に非依存。(E-d) は一般 c の義務 |
| FR7 | no return | FR5–FR6 の証明で旧 parent U_F への逆比較または旧 DC discount を使わない |

FR1–FR7 が揃って初めて c=3 の補題 N 枠として受理する。QR5 PASS は FR5 の一つの row を供給するだけで、
FR3/FR4/FR6 を閉じない。

## 5. chart 入力として使える既存証明書

三原子一遷移文書の以下は、reduction 完了ではなく pivot/chart 選択の観測量として使う。

- held r=2: one-variable 標準形と pointwise 二側評価。
- held r=1(A): direct transfer。
- held r=1(B): M₁ の小ささ。
- split(i): K2Q-wt による旧 `U_F` direct transfer(chart観測量のみ。S4 root routeには使わない)。
- split(ii): source 上の三者深消滅。
- split(iii): pair principal coefficient の縮退 witness。

証明書がどの FR2 chart を選ぶか、また選んだ chart が FR3/FR4 をどう与えるかは未証明。

## 6. 最小の証明順

1. **[補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md) (plain c=3 valuation 上界)**: F3′ と独立に、相異三原子 span の最大 valuation が 5 以下であることを自己完結に証明する。
2. **FR-S1′ (weighted SVD frame、R-A′ PASS)**: 真空 gauge 後の (2,1)-weighted 距離と J⁵-SVD で、plain single-scale triple の exact 枠を定義する。
3. **nested 2+1 接続**: [static generalized 補題 W′](2026-08-11-three-atom-wronskian-valuation-W--wip.md) と §9 の finite-m FR-S1″ は R-W′ / R-A″ PASS。
4. **FR-S4-0 (interface specification)**: §10 で per-node segmentation、U_H-ledger、(E-w)、kernel/constant 契約を固定する。proof claim は置かない。
5. **FR-S4b (FR5 kernel routing)**: K2/K2Q-aff/QR5 を node ごとに割り当てる。held 2+1 root は QR5-w、far/unheld rootは別obligationとする。
6. **FR-S4a (FR6-core envelope assembly)**: S4b の kernel と C′ chaining から (E-w) を導く。
7. **FR-S4c (FR6/FR7 closure)**: N3′/N4 台帳と no-return audit を閉じる。
8. 固定 SHA で FR1–FR7 を独立再査読する。

## 7. 現在の blocker

plain single-scale triple の FR-S1′ は固定 SHA `ed25401` の R-A′、nested 2+1 の FR-S1″ は
固定 SHA `61111cc` の R-A″で PASS。base FR-S4-0 interface も固定 SHA `56498bb` の R9 で accepted。
補題 RF(§10.5.3)は R-RF R2(fixed SHA `9f19389`、minors `c271919`)で受理され、
`root-far` row は §10.5 の resolved discriminant へ昇格した(`M-ROOT-FAR-KERNEL` 解消)。
polynomial ΣA program は PΣ-1/2/3/4 の全てが accepted(§10.5.4、R-PS4 R3 PASS `58b9c9f`)、
S4b coverage は補題 S4b-COV(§10.5.5、R-COV1 R4 PASS `c36d818`)で閉鎖し、**S4b closure は
完結**した。現在の最初の未解決点は **S4a の envelope assembly**(W1 Child-reserve 以降、
§10.5.4/§10.5.5 の帳簿を消費)であり、S4c の N3′/N4・no-return audit も open のまま。
c=3 の (E-w) や FR5–FR7 の閉鎖はまだ主張しない。

FR-S1′/S1″の設計時に解決した制約として、旧 moment order だけでは消滅速度を記録できず、
(s,0),(2s,0),(3s,s²) 型の異方的退化で零極限になる。従って chart label は exact moment の
非零/零だけでなく、相対 valuation または同値な flag/blow-up 座標を含まなければならない。
以下の F3 witnessはその設計制約の記録であり、現在の追加 blockerではない。

**Flex witness F3 (single-scaleでも生じる evaluation-rank drop)**: parameter path

  ξ(t) = (A(t),B(t)) = (−t²,t)、φ_t(z) := exp(tz−t²z²/2)

の三点 t=0,s,2s は parameter distance が single-scale。exact second difference

  h_s := φ_0−2φ_s+φ_{2s} = −2s³z³−(7/6)s⁴z⁴+O(s⁵)

なので h_s/‖h_s‖ は cubic jet へ向かう。一方 φ′′_0=0 であり、path の length-3 truncation
mod t³ をそのまま evaluation すると三次元枠を見失う。従って「長さ3の点スキームを取れば自動的に
FR3/FR4が出る」という素朴な Route B は不十分。scheme route を使う場合も、evaluation map の rank-drop locus を
追加 blow-up/Fitting flagで解消するか、この witnessを拾う高次 coefficient flagが必要である。
（表示係数は Taylor 展開で厳密に導出。SymPy series は補助検算で一致。）

**Flex witness F3′ (旧次数4帳簿の反例・本 witness の唯一の authoring location)**:
`ψ(u):=exp(u−u²/2)`、`ω:=exp(2πi/3)`、`B_j:=βω^j`、`A_j:=−B_j²` と置く。
二階 divided-difference 係数 `a_j:=1/Π_{i≠j}(B_j−B_i)` に対して

  h_β(z):=Σ_{j=0}^2 a_j exp(B_jz−B_j²z²/2)
          =(β³/20)z⁵−(11β⁶/3360)z⁸+(13β⁹/554400)z¹¹+⋯ .

これは `ψ₂=0` と三乗根配置の `e₁=e₂=0, e₃=β³` から得られる厳密級数である。
従って `h_β/‖h_β‖→z⁵/√(5!)` in ℱ。さらに三原子 span の valuation profile は
`(0,1,5)` で、次数 4 以下の係数行列は rank 2、次数 5 を加えると rank 3 になる。
よって枠の取り替えによって五次方向を避けることはできず、旧 FR3 の
`deg P≤2o′≤4` は**偽**である。この exact 構成は `κ_border^G(|5⟩)≤3` も与える。

F3′ が確立するのは「三原子には次数 5 が必要」という下側だけである。plain c=3 の上界 5 は
[補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md) が R-W PASS (`1b3e337`)。
一般 `w` の候補
`D(w)=(w−1)(w+2)/2`、nested 2+1 への拡張、FR5–FR7 はここでは主張しない。

## 8. FR-S1′ (plain single-scale triple の weighted J⁵-SVD frame)

本節の入力は §2 のうち、proper child を持たない `w=r=3` の single-scale active node に限定する。
従って部分列上で、ある `η>0` に対し全ての相異 pair が

  d_w(ξ_{i,m},ξ_{j,m})/s_m ≥ η

を満たす。pivot を真空にした座標では exact に

  A_{j,m}=s_m²Ā_{j,m},  B_{j,m}=s_m B̄_{j,m},

かつ `|Ā_{j,m}|≤1`, `|B̄_{j,m}|≤1`。部分列を取り、正規化配置
`ϑ_m:=((Ā_{j,m},B̄_{j,m}))_{j=1}^3` は pairwise distinct な `ϑ*` へ収束するとする。

### 8.1 Statement

`J⁵:=span{e_k:=z^k/√(k!):0≤k≤5}`、`π₅` をその ℱ-直交射影とする。gauge 後の
unnormalized atom を

  ū_{j,m}(z):=exp(A_{j,m}z²/2+B_{j,m}z)

とし、

  T_m:ℂ³→J⁵,  a↦π₅(Σ_j a_jū_{j,m})

の SVD を取る。特異値を `σ_{1,m}≥σ_{2,m}≥σ_{3,m}`、右特異ベクトルを
`a_m^(ℓ)` (`‖a_m^(ℓ)‖₂=1`) とし、

  h_{ℓ,m}:=Σ_j a_{j,m}^{(ℓ)}ū_{j,m},
  v_{ℓ,m}:=h_{ℓ,m}/‖h_{ℓ,m}‖

と置く。重複特異値内の基底は一意でなくてよい。有限次元 unitary 群の compactness で、必要なら
さらに部分列を取る。

**FR-S1′ target (plain single-scale c=3)**: m が十分大きいとき、定数 `c₀,C>0` が存在して

1. `σ_{3,m}≥c₀s_m⁵`;
2. `‖(1−π₅)h_{ℓ,m}‖≤Cs_m⁶≤(C/c₀)s_mσ_{ℓ,m}` (全 ℓ);
3. 部分列上で `v_{ℓ,m}→P_ℓ∈J⁵` in ℱ、`{P_1,P_2,P_3}` は正規直交;
4. `span{h_{1,m},h_{2,m},h_{3,m}}=span{ū_{1,m},ū_{2,m},ū_{3,m}}` exact;
5. `Gram(v_{1,m},v_{2,m},v_{3,m})=I+O(s_m)`。

定数依存は compact input class、`η`、固定 pivot/chart のみで、m と radial angle θ には依存させない。
元の gauge 前枠は `U_m^{-1}` で戻す。unitarity と吸収済み nonzero scalar により exact span、norm、Gram は保たれる。

### 8.2 Head factorization and singular-value floor

weighted homogeneous coefficientを `W_k(A,B):=[z^k]exp(Az²/2+Bz)` とすると

  W_k(s²Ā,sB̄)=s^kW_k(Ā,B̄).

正規化配置 `ϑ=((Ā_j,B̄_j))_j` に対して

  T(ϑ)a:=π₅(Σ_j a_j exp(Ā_jz²/2+B̄_jz))

と定義する。`D(s)e_k:=s^ke_k` と置けば exact に

  T_m=D(s_m)T(ϑ_m).                                               (S1)

compact collision-free 集合を

  Θ_η:={ϑ=((Ā_j,B̄_j))_j: |Ā_j|,|B̄_j|≤1,
         pairwise d_w((Ā_i,B̄_i),(Ā_j,B̄_j))≥η}

と置く。`ϑ_m∈Θ_η` であり、[補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md)
の `J⁵` injectivity と compact-family corollary より、`c₀=c₀(η)` として

  σ_min(T(ϑ_m))≥c₀>0.                                             (S2)

`0<s_m≤1` では `‖D(s_m)y‖≥s_m⁵‖y‖` (`y∈J⁵`) なので、(S1)–(S2) から

  σ_{3,m}=σ_min(T_m)≥c₀s_m⁵.                                     (S3)

### 8.3 Fock tail

`|Ā|,|B̄|≤1` 上で

  |W_k(Ā,B̄)|≤C_k,  C_k:=[x^k]exp(x+x²/2).

`‖a_m^(ℓ)‖₁≤√3` と weighted homogeneity より、`k≥6` の係数は
`≤√3 C_k s_m^k`。固定 `s_*∈(0,1)` を取り、十分大きい m で `s_m≤s_*` とすれば

  Σ_{k≥6} 3C_k²k!s_m^{2k}
  ≤s_m^{12} Σ_{k≥6}3C_k²k!s_*^{2(k−6)}
  =:C²s_m^{12}.                                                   (S4)

右辺の級数は有限である。実際、`Σ_k C_k²k!s_*^{2k}` は
`exp(s_*z+s_*²z²/2)` の Fock norm の二乗であり、`s_*²<1` だから有限。
(S4) と (S3) が statement 2 を与える。

### 8.4 Limit frame and exactness

`p_{ℓ,m}:=π₅h_{ℓ,m}/σ_{ℓ,m}` は SVD の左特異ベクトルなので `J⁵` 内で正規直交。
statement 2 と head/tail の直交性から

  ‖v_{ℓ,m}−p_{ℓ,m}‖=O(s_m).

`J⁵` の unit sphere は compact なので部分列上で `p_{ℓ,m}→P_ℓ`、極限も正規直交。
従って gauge 後には `v_{ℓ,m}→P_ℓ`、Gram は `I+O(s_m)`。右特異ベクトル行列は unitary なので
`{h_{ℓ,m}}` と `{ū_{j,m}}` の span は exact に一致する。

残留真空位相を chart で固定すれば、pivot `ξ_{j_0,m}→ξ*` に対応する gauge は部分列上で
`U_m→U_*` strongly と取れる。従って

  ‖(U_m^{-1}−U_*^{-1})x‖=‖x−U_mU_*^{-1}x‖→0

で逆元も strongly 収束し、

  U_m^{-1}v_{ℓ,m}→U_*^{-1}P_ℓ=:Q_ℓΦ(ξ*)  in ℱ.

affine metaplectic 変換は creation operator を `a,a†,1` の一次結合へ移し、Bargmann 表示では
`∂Φ=(Az+B)Φ` だから `deg Q_ℓ≤deg P_ℓ≤5`。これが gauge 前の (L-d) を与える。

limit span は `J⁵` の三次元部分空間なので、その valuation profile は `{0,…,5}` から選ぶ有限集合に属する。
tree shape と pivot permutation も有限なので、さらに部分列を取れば全 label を固定できる。

ここまでで plain single-scale triple に対する FR1、FR2、FR4、FR3 の (X)/(L-d) を与える。
ただし基点から離れた `(E-d)` envelope、FR5、FR6、FR7 は出ないため、FR全体を closed としない。

### 8.5 Acceptance ledger

| ID | 本節での状態 | 残余 |
|---|---|---|
| A′-1 relative `d_w` chart | accepted (R-A′ PASS) | residual vacuum stabilizer invariance と pivot固定 |
| A′-2 head floor `σ_3≥c₀s⁵` | accepted (R-A′ PASS) | 補題 W + compactness + exact factorization |
| A′-3 Fock tail `O(s⁶)` | accepted (R-A′ PASS) | (S4) の一様級数定数 |
| A′-4 norm limit / Gram / exact span | accepted (R-A′ PASS) | SVD と head-tail 直交性 |
| nested 2+1 | accepted (R-A″ PASS) | static generalized W′ + §9 finite-m ν-chart / FR-S1″ |
| `(E-d)` / FR5–FR7 | open, not claimed | FR-S4 |

## 9. FR-S1″ (nested 2+1 の continuous ν-chart frame)

本節の入力は §2 の `w=r=3` のうち、leaf 1,2 が proper pair child、leaf 3 が singleton となる
nested 2+1 active node に限定する。pair child scale を

  τ_m:=d_w(ξ_{1,m},ξ_{2,m}),

root scale を §2 の `s_m` とし、`τ_m/s_m→0` とする。child anchor `u_{1,m}` を pivot にして真空へ
移した gauge で、scalar を吸収した三原子を

  ū_{1,m}=1,
  ū_{2,m}=exp(δA_m z²/2+δB_m z),
  ū_{3,m}=exp(A_m z²/2+B_m z)

と書く。root-scale normalized parameter を

  δĀ_m:=δA_m/s_m²,  δB̄_m:=δB_m/s_m,
  Ā_m:=A_m/s_m²,    B̄_m:=B_m/s_m

とする。定義から `|Ā_m|,|B̄_m|≤1` で、部分列上の root separation として

  max(|Ā_m|^{1/2},|B̄_m|)≥η>0                              (N0)

を固定できる。また

  |δB̄_m|≤τ_m/s_m,  |δĀ_m|≤(τ_m/s_m)²,

なので、次の `t_m` は rate の仮定なしに 0 へ行く。

### 9.1 Continuous ν-chart and exact child frame

root-normalized child exponentの一次・二次係数を同じ線形空間で保持するため

  ν_m:=(δB̄_m,δĀ_m/2)∈ℂ²,
  t_m:=‖ν_m‖₂>0,  ν̂_m:=ν_m/t_m∈S³:={ν∈ℂ²:‖ν‖₂=1}

と置く。`t_m>0` は constant-gauge quotient 後の child leaf が相異なることから従う。部分列上で
`ν̂_m→ν̂_*` としてよい。`ν̂=(ν_1,ν_2)` に対して

  L_{ν̂}(x):=ν_1x+ν_2x²,
  G_{ν̂,t}(x):=(exp(tL_{ν̂}(x))−1)/t       (t>0),
  G_{ν̂,0}(x):=L_{ν̂}(x)                                   (A″1)

と定義する。積分表示

  G_{ν̂,t}=L_{ν̂}∫_0^1 exp(utL_{ν̂})du

により `G` は `S³×[0,t₀]` 上で coefficientwise、`J⁵`、Fock tail のいずれでも `t=0` まで連続である。
finite m の child frameは

  f_{1,m}:=ū_{1,m}=1,
  f_{2,m}:=(ū_{2,m}−ū_{1,m})/t_m,
  f_{3,m}:=ū_{3,m}                                          (A″2)

とする。これは anchor + normalized Newton difference であり、正規化子 `t_m` は root-normalized
parameter だけから作るので `s_m` に依存しない。`t_m>0` では元の三列からの可逆な exact column
変換である。

ここで `ε_m:=d_w(ξ_{1,m},ξ_{2,m})/s_m` として
`δĀ_m=ε_m²χ_{A,m}`, `δB̄_m=ε_mχ_{B,m}` と置く graded chart は採用しない。その差分を `ε_m` で
割ると、`χ_{B,m}` が同時に零へ行く mixed rate で quadratic direction が消え、`t=0` face への
連続性を失う。`ν̂_m` は child profile `(0,1)` と pure quadratic `(0,2)` を同じ compact sphere の
点として保持する。

### 9.2 Compact chart and statement

`0<η≤1` とし

  0<t₀≤min(1/4,η²/8)

を固定する。compact parameter setを

  𝒦_{η,t₀}:={ (Ā,B̄,ν̂,t): |Ā|,|B̄|≤1,
      max(|Ā|^{1/2},|B̄|)≥η, ν̂∈S³, 0≤t≤t₀ }

と置く。child の normalized parameter は `(2tν_2,tν_1)` であり

  d_w((2tν_2,tν_1),(0,0))≤max(√(2t),t)≤η/2.

従って (N0) と三角不等式から singleton は child の両 leaf から `η/2` 以上離れる。

`J⁵` と `π₅` は §8 と同じとする。head map

  S_m:ℂ³→J⁵,  a↦π₅(Σ_{j=1}^3 a_jf_{j,m})

の SVD を取り、特異値を `σ_{1,m}≥σ_{2,m}≥σ_{3,m}`、unit right singular vector を
`a_m^(ℓ)` とする。

  h_{ℓ,m}:=Σ_j a_{j,m}^{(ℓ)}f_{j,m},
  v_{ℓ,m}:=h_{ℓ,m}/‖h_{ℓ,m}‖.

**FR-S1″ target (nested 2+1, c=3)**: m が十分大きいとき、定数 `c₀,C>0` が存在して

1. `σ_{3,m}≥c₀s_m⁵`;
2. `‖(1−π₅)h_{ℓ,m}‖≤Cs_m⁶≤(C/c₀)s_mσ_{ℓ,m}` (全 ℓ);
3. 部分列上で `v_{ℓ,m}→P_ℓ∈J⁵` in ℱ、`{P_1,P_2,P_3}` は正規直交;
4. `span{h_{1,m},h_{2,m},h_{3,m}}=span{ū_{1,m},ū_{2,m},ū_{3,m}}` exact;
5. `Gram(v_{1,m},v_{2,m},v_{3,m})=I+O(s_m)`。

定数依存は compact input class、`η,t₀`、固定 pivot/tree chart のみで、`m,θ` と
`t_m→0` の rateには依存させない。

### 9.3 Exact root factorization and singular-value floor

`(Ā,B̄,ν̂,t)∈𝒦_{η,t₀}` に対して

  Ṫ(Ā,B̄,ν̂,t)a
  :=π₅(a_1+a_2G_{ν̂,t}(x)+a_3exp(Āx²/2+B̄x))

と定義する。`D(s)e_k:=s^ke_k` とすると、(A″1)–(A″2) と weighted homogeneity から exact に

  S_m=D(s_m)Ṫ(Ā_m,B̄_m,ν̂_m,t_m).                         (A″3)

右辺に誤差項はなく、`t_m` の任意 rate は `Ṫ` の compact parameter として残る。

`t>0` では三つの parameter pair は相異なり、(A″2) は可逆 column 変換なので、補題 W の
`J⁵` injectivity から `Ṫ` は単射。`t=0` では列空間は

  span{1,L_{ν̂},exp(Āx²/2+B̄x)}

である。`‖ν̂‖₂=1` と (N0) により [static generalized 補題 W′](2026-08-11-three-atom-wronskian-valuation-W--wip.md)
の `J⁴` injectivity が適用でき、従って `J⁵` map `Ṫ` も単射である。`Ṫ` は
`𝒦_{η,t₀}` 上で連続なので compactness より

  inf_{𝒦_{η,t₀}} σ_min(Ṫ)=:c₀>0.                              (A″4)

`0<s_m≤1` で `‖D(s_m)y‖≥s_m⁵‖y‖` (`y∈J⁵`) だから、(A″3)–(A″4) が target 1 を与える。

### 9.4 Uniform Fock tail

singleton columnには §8.3 の

  C_k:=[x^k]exp(x+x²/2)

を使う。difference column は (A″1) の積分表示と `|ν_1|,|ν_2|≤1` から coefficientwise に

  |[x^k]G_{ν̂,t}|≤D_k,
  D_k:=[x^k](x+x²)exp(t₀(x+x²)).                              (A″5)

`M_k:=max(C_k,D_k)` とする。`‖a_m^(ℓ)‖₁≤√3` なので、`k≥6` の `h_{ℓ,m}` の係数は
`≤√3M_ks_m^k`。固定 `s_*∈(0,1)` を `2t₀s_*²<1` となるよう取り、十分大きい m で
`s_m≤s_*` とすれば

  Σ_{k≥6}3M_k²k!s_m^{2k}
  ≤s_m^{12}Σ_{k≥6}3M_k²k!s_*^{2(k−6)}
  =:C²s_m^{12}.                                                (A″6)

右辺の級数は有限である。`C_k` 部分は §8.3 と同じで、`D_k` 部分は

  (s_*z+s_*²z²)exp(t₀s_*z+t₀s_*²z²)

の Fock normで支配され、quadratic parameter の絶対値 `2t₀s_*²<1` により有限。
(A″6) と target 1 が target 2 を与える。

### 9.5 Limit frame, exact tree, and scope

`p_{ℓ,m}:=π₅h_{ℓ,m}/σ_{ℓ,m}` は `J⁵` 内で正規直交。§8.4 と同じ head-tail 直交性から

  ‖v_{ℓ,m}−p_{ℓ,m}‖=O(s_m),

従って部分列上の正規直交極限、target 3、target 5 を得る。finite m では (A″2) の column変換と
SVD right matrix がともに可逆なので target 4 も exact。

各 `h_{ℓ,m}` は明示的に

  h_{ℓ,m}
  =(a_{1,m}^{(ℓ)}−a_{2,m}^{(ℓ)}/t_m)ū_{1,m}
   +(a_{2,m}^{(ℓ)}/t_m)ū_{2,m}+a_{3,m}^{(ℓ)}ū_{3,m}

と書ける。従って child pair の exact combination と singleton を二子とする pair+singleton tree を持つ。
係数の `1/t_m` 発散は許容され、正規化後frameとtailは(A″4)–(A″6)で一様に制御される。

元の gauge へは §8.4 と同じ strong-continuous unitary sectionで戻す。よって nested 2+1 に対する
FR1、FR4、FR3 の (X)/(L-d) を得る。limit span の valuation profile は `{0,…,5}` から選ぶ有限集合で、
pair+singleton tree と pivot permutation も固定済みなので、さらに部分列を取れば FR2 label も固定できる。
plain FR-S1′ と合わせれば、post-quotient `w=r=3` の single-collision-cluster
入力のこれら四義務を全 tree shape で覆う。`w≤2` は §2 の leaf/c=2 assetsへ送る。ただし
`(E-d)`、FR5–FR7、FR-S4、wrapper Γ(3)、一般 c は
本節から主張しない。

### 9.6 Acceptance ledger

| ID | 本節での状態 | 証拠 / 残余 |
|---|---|---|
| A″-1 `ν̂,t` compact chart | accepted (R-A″ PASS) | (A″1)、graded `d_w` chart を不採用 |
| A″-2 exact factorization / head floor | accepted (R-A″ PASS) | (A″3)–(A″4)、W / W′ |
| A″-3 difference-column Fock tail | accepted (R-A″ PASS) | (A″5)–(A″6) |
| A″-4 limit Gram / exact span / tree | accepted (R-A″ PASS) | SVD + exact column変換 |
| A″-5 FR1/FR2/FR4/FR3(X)(L-d) | accepted (R-A″ PASS) | plain FR-S1′との全tree-shape合成 |
| c=3 `(E-w)` / FR5–FR7 | open, not claimed | §10 S4-0 specification draft、S4b→S4a→S4c が必要 |
| 一般 c `(E-d)` | open, not claimed | 親 node が polynomial generalized atom を消費する再帰義務 |

## 10. FR-S4-0 shared interface specification (proof claim なし)

本節を c=3 FR-S4 の shared interface と packet 順序の唯一の authoring location とする。
[Fable consultation #3](https://github.com/orangewk/wigner-splat/pull/178#issuecomment-5252973388) の
REVISE を入力とするが、本線で次を補正した。実二次式の差から交差数 `≤2` が自動で従うのは
**二つの原子 exponential を比較する pair node だけ**である。root の pair-block `B₁₂` は指数和なので
`log|B₁₂|−log|c₃e^{q₃}|` は二次式ではない。従って root segmentation は既知事実として採用せず、
S4b の split-row audit が供給すべき明示 obligation とする。

本節は仕様だけを固定し、segmentation、kernel routing、(E-w)、N3′/N4 のいずれも証明しない。

### 10.1 Non-circular packet order

依存順を

  S4-0(spec) → S4b(FR5 routing) → S4a(FR6-core) → S4c(FR6/FR7 closure)

と固定する。

| packet | consumes | produces | current state |
|---|---|---|---|
| S4-0 | FR-S1′/S1″、K2/K2Q/QR5、C′ の候補 interface | 本節の型付き interface のみ | **accepted (R-S4-0 R9、fixed SHA `56498bb`)** |
| S4b | S4-0 + reviewed node kernels | per-segment FR5 routing、split-row audit | **closed**(全 6 route resolved + PΣ/RF ledgers + 補題 S4b-COV accepted `c36d818`。旧 exponent-4 split-row audit は v0.8.15 反例で退役し held root は QR5-w へ一本化) |
| S4a | S4b + fixed-SHA PASS の `Cprime_ref` | c=3 weak envelope (E-w) | **closed**(§10.8 全 8 packet accepted、補題 EW = R-EW R2 PASS `b39216f`) |
| S4c | S4a + FR1–FR5 | N3′/N4 ledger、FR7 no-return、c=3 FR acceptance | open, not claimed |

S4a は S4b の kernelを消費するため、旧案 S4a→S4b の順では書かない。

### 10.2 c=3 weak envelope target (E-w)

c=3 milestone で FR6 が要求する遠方成長 target を次の弱形に限定する。

**(E-w)**: compact input class `K_{δ,R}` に対し定数 `C_w,C_lin>0` と `m₀` が存在して、
全 `m≥m₀`、frame index `ℓ`、`z∈ℂ` について

  |(U_m^{-1}v_{ℓ,m})(z)|
  ≤ C_w exp((1−δ/2)|z|²/2 + C_lin|z|).                         (S4-Ew)

定数は `m,ℓ,z,θ` と SVD/Newton coefficient に依存させない。§4 冒頭の L2a′ 消費者監査により、
c=3 の下流で envelope が使われる一様可積分尾部には (S4-Ew) で十分。これは多項式形 (E-d) を
一般に含意しない。一般 c の再帰では親 node が `PΦ` 型 child を消費するので、(E-d) は一般 c の
open obligation として残す。補題 N の N3′/N4 文言は S4c でこの c=3/general-c 分離へ同期する。

### 10.3 Two-level radial segmentation contract

S4b は次の二段階で行い、順序を逆転しない。

1. **S4b-α (interval-independent registry closure)**: §10.4 の `RouteKind` registryを固定する。
   §10.5 の到達可能な categoryは、domainから排除する証明がない限り全てregistryに必要である。
   `state=unresolved` のentryが一つでも残ればここで停止する。各 resolved entryはintervalに依存しない
   有限 `κ̄_route` を持つ。これらから

      κ_chain:=max_{resolved RouteKind} κ̄_route,
      ε_chain:=min(1/2,δ/[8(κ_chain+1)])

   を定める(empty registryのmaxは0)。この段階では `I_k,J_k` や held witnessを使わない。
2. **S4b-β (interval instantiation)**: 固定 ray `z=te^{iθ}`、終点半径 `T≥3` に対し、C′ draftと同じ
   `I_k=[a_k,a_k+1]`, `a_{k+1}=a_k−(1−ε_chain)`,
   `J_k=I_k∩I_{k+1}` (長さ `ε_chain`)を作る(`N≤2T+1`)。endpoint 規約は C′ と同一に固定する:
   `a_1=T−1` から降順、停止は最初の `a_N≤1`。全窓は切断なしの長さ 1 であり
   `a_k ≥ 1−(1−ε_chain) = ε_chain > 0` が自動成立する(窓を `[0,∞)` で切る操作は行わない)。
   半径 ≲ 2 の近原点領域は chaining ledger の外で、C′ 同様 S4a の compact initial estimate が
   掌理する。逐語形は §10.5.4 補題 PΣ-3 (h0)。`J_k=I_k∩I_{k+1}` が定義される `k∈K_T={1,…,N−1}`
   の各 `(I_k,J_k)` に resolved `RouteKind` の `RouteRecord` を割り当て、interval依存の
   domain witnessをここで検証する。最終窓 `I_N` は `TerminalRecord`(§10.5.5)へ送る。

S4b-β は必要なら `I_k` 内を有限 cell `𝒫_{H,k}` に分けてよいが、S4aへ渡す出力は内部cellを
畳み込んだ次のどちらかの **composite unit-step kernel**だけとする。

- `mode = unweighted`:

      sup_{I_k}|H|
      ≤ C_step ε_chain^{−γ_H}
        exp(A_{H,k}+κ_HΛ_{H,k}ε_chain) sup_{J_k}|H|.             (S4-step-u)

- `mode = weighted`:

      ‖e^{−U_H}H‖_{∞,I_k}
      ≤ C_step ε_chain^{−γ_H} exp(κ_HΛ_{H,k}ε_chain)
        ‖e^{−U_H}H‖_{∞,J_k}.                                  (S4-step-w)

現行のreviewed weighted root routeである QR5(U_T) は `(S4-step-w)` 型であり、
`(S4-step-u)` を直接供給しない。
特に weighted estimate から unweighted estimate への変換を暗黙に行ってはならない。その変換には
`sup_{I_k}U_H−inf_{J_k}U_H` が必要で、現在の `A_{H,k}=sup_{I_k}U_H−sup_{J_k}U_H` では足りない。
pair-block の零点近傍ではこの差を一様に抑えられない可能性がある。S4a は mode ごとに別の assembly を
与え、weighted routeから (E-w) へ進む場合は、そのための新しい比較を明示的に証明する。

step cost は §10.4 の `CostSpecEnum` で型付けする。resolved route の cost は `uniform(C̄_route)`、
ただし `root-far` だけが accepted RF proof(§10.5.3)に結合した
`graded-root(C_RF,pair-difference-derivative)` を使う。後者は route ID が
`root-far`、modeがweighted、`κ_H=0`、fixed-SHA accepted RF proofを持つ場合に限る。

acceptance 条件は次の八つ。

1. `uniform(C̄_route)` では `C_step≤C̄_route`、`γ_H`、`κ_H≤κ̄_route` は compact class、node type、
   route labelだけに依存し `m,θ,k,T` に非依存。`graded-root` では interval依存を
   `log C_step,k≤C_RF(1+Λ_{η,k})` の一形だけに限定し、`C_RF` は同じ非依存条件を満たす。
2. uniform routeがcell分割を使う証明では `#𝒫_{H,k}≤N_cell` を一様に示し、その積を一つの
   `C_step` へ吸収する。graded-root route では一様 `N_cell` を要求せず、代わりに
   `N_cell,k≤C_cell(1+Λ_{η,k})` と §10.5.2 RF-2/RF-3 の局所・大域ledgerを証明する。
   分割なしの直接 unit-step kernelでもよい。
3. pair leaf nodeでは `Re(q_1−q_2)+log|c_1/c_2|` が実二次以下なので dominance cellは高々3。
   root pair-block vs singleton ではこの推論を使わず、S4b の **split-row audit under U_H-ledger** が
   一様な root stepを直接証明する。rootで `N_cell` を導入する場合だけ、その一様性も証明する。
4. 各 `I_k`(`k∈K_T`、§10.5.5。`I_N` は `TerminalRecord`)は root level でちょうど一つの
   resolved route recordに覆われる。direct QR5 routeを使うなら
   raw pair-held 条件 `sup_{I_k}|q_2−q_1|≤1/8` の witnessを interval 全体について添付する。
   `RECENTER(C,t_c)` 後のheld cellを使うのは、RF-1/RF-2のexact transition・cell cover・composite
   `RootStep_k` がfixed-SHAで受理された場合だけであり、far/unheld intervalを無証拠にheldへ読み替えない。
5. `κ_H>0` または `A_ledger_kind=phase-lipschitz` の routeは `Λ_{H,k}` を underlying Gaussian
   phase derivativeへ結ぶ `frequency_source/bound_witness` を持ち、
   `Λ_{H,k}≤(1−δ)(a_k+1)+R` を示す。`κ_H=0` かつ `weighted-no-A` の routeだけ
   `frequency_source=NONE` としてよい。
6. S4b の出力は一 interval 当たり一つの `RootStep_k` とする。child kernelはその root stepを証明する
   内部 provenanceであり、S4a が child stepとancestor/root stepを別々に積算してはならない。
7. `coverage_manifest` の重複/欠落、`state=unresolved` の `RouteKind`、未受理 dependency、有限定数の欠落は
   S4b-α を停止させる。unresolved entryを interval recordや仮の modeへ coercionしてはならない。
8. `graded-root` recordをS4aへ渡すには、各recordの `Λ_{η,k}` witnessに加え、同じray全体で
   `Σ_kΛ_{η,k}` を compact collision scaleから抑える accepted ledger refが必要。局所cell数だけを示して
   quadratic growth budgetを未検証のまま (E-w) へ進まない。

この route dataは既存 one-transition cluster tree 内の radial kernel routingを細分するだけで、
多重 cluster transition を扱う L3 や一般 c の multi-transition 帰納を閉じない。root で一様な
いずれの型でも composite root stepが偽なら、S4b は counterexampleとともにS4-0を改訂し、S4aへ進まない。

### 10.4 Node-envelope ledger and no-return vocabulary

binary node `H=A+B` では `U_H=max(log|A|,log|B|)`、unary node `H` では
`U_H=log|H|` とする。unweighted stepだけ

  A_{H,k}:=sup_{I_k}U_H−sup_{J_k}U_H ≥ 0

を持つ。root 2+1 nodeでは `U_H=U_T`。ただし `A_{H,k}` の合計は route shapeにより挙動が違うため、
`κ_H=0` から自動的に消えるとは扱わない。

#### RouteKind (interval-independent discriminated union)

closed-world category enumを

  CategoryEnum := {K2-u,K2Q-aff-u,generalized-singleton-u,QR5-w,
                   root-far,trivial-u}
  CostSpecEnum := {uniform,graded-root}

と固定する(`REFIX` は routeでなく前処理 transitionなので含めない)。`RouteKind` は次の三variantである。

| variant | required fields |
|---|---|
| `resolved` | `(route_id∈CategoryEnum,route_spec_ref,source_ref,assembly_state)`。`(arity,mode,source rule,domain schema,cost spec∈CostSpecEnum,γ,κ̄,inequality,A-ledger rule,assembly rule)` は §10.5 の同じ `route_id` の唯一の `RouteSpec` 行と**全field完全一致**し、個別override不可 |
| `unresolved` | `(route_id∈CategoryEnum,expected_arity∈{unary,binary},missing_obligation_id∈MissingObligationEnum)` のみ。`mode/source_ref/constants/inequality_id` を仮置きしない |
| `excluded` | `(route_id∈CategoryEnum,exclusion_proof_ref)`。`exclusion_proof_ref=(category_id,unreachable_domain_witness_id,canonical_file,anchor,fixed_SHA,PASS)`、`category_id=route_id`、かつ証明statementが「全inputで当該categoryへ到達不能」と受理された場合だけ |

`DomainSchemaEnum` と `MissingObligationEnum` も有限に固定する。

  DomainSchemaEnum := {D-K2,D-K2Q-AFF,D-GENERALIZED-SINGLETON,
                       D-QR5-HELD,D-ROOT-FAR,D-TRIVIAL}
  MissingObligationEnum := {M-K2-STATUS,M-ROOT-FAR-KERNEL}
  (いずれも解消済み。名称は過去の unresolved 記録の参照語彙として enum に残すが、
   現行の RouteSpec row はどれも参照しない。)
  ExclusionWitnessEnum := ∅   (現行S4-0では accepted exclusionなし)

`excluded` は `unreachable_domain_witness_id∈ExclusionWitnessEnum` も要求する。従って現行registryでは
excluded variantを一つも生成できない。将来 category-specific exclusionを受理する場合は、route IDと
到達不能statementを結ぶ witness IDを本enumへ追加してから使う。

各 domain schema の key set は次で固定する。

| domain schema | required keys |
|---|---|
| `D-K2` | `active_children_nonzero`, `c₁c₂≠0`, `q₁−q₂` nonconstant |
| `D-K2Q-AFF` | `active_children_nonzero`, `P≢0`, `c₂≠0`, `deg P≤2`, `q₁−q₂` nonconstant |
| `D-GENERALIZED-SINGLETON` | `P≢0`, `deg P≤2`, unary exact-identity ref |
| `D-QR5-HELD` | `active_children_nonzero`, `c₁c₂c₃≠0`, `B₁₂≢0`, `sup_{I_k}|q₂−q₁|≤1/8` |
| `D-ROOT-FAR` | `active_children_nonzero`, `c₁c₂c₃≠0`, `B₁₂≢0`, `η=q₂−q₁` nonconstant, `q₁−q₃`/`q₂−q₃` nonconstant(§2 constant-gauge quotient witness), collision-scale witness `(|ΔA|≤s_m²,|ΔB|≤s_m)`, `Λ_{η,k}=sup_{I_k}|η′|` witness |
| `D-TRIVIAL` | `c≠0`, unary exact-identity ref |

`D-ROOT-FAR` は補題 RF(§10.5.3、R-RF R2 PASS)の受理に伴い、resolved `root-far` row の
domain schema として active である。`RouteRecord.domain_witness` は全 7 key を式または
identity ref で供給しなければならない(negative path は binding test が固定)。

§10.5 の `RouteSpec` 表を route-specific discriminant の唯一の authoring location とする。各rowは
このIDの一つを使い、自由文のschema/reasonや field overrideを新設しない。新しいkeyや組合せが必要なら
まずS4-0と `RouteSpec` 行を改訂する。

registryは `coverage_manifest=(CategoryEnum,entries)` を持ち、各category IDが resolved/unresolved/excluded の
**ちょうど一つ**として現れること、重複・欠落がともに空集合であることを検査する。この完全性検査の後にだけ
S4b-α の「unresolvedなし」を判定する。これは **registry-level manifest** であり、ray ごとの
interval被覆は別物として `RayCoverageManifest_{θ,T}`(§10.5.5)が担う。両者を混同しない。

`source_ref` も discriminated union とする。

- `external=(kernel_name,canonical_file,anchor,fixed_SHA,PASS)`。`fixed_SHA` は**査読対象 content の
  SHA**であり、`PASS` の効力は canonical authoring file の現行 status ledger にその SHA を明記した
  acceptance 記録が存在する場合に限る(例: QR5 は K2p1 §3.8.6 status 表の
  「PASS(R-P3、fixed SHA `27a1817`)」行が効力の根拠。content SHA 時点の文書自身が
  旧 status を表示していても、acceptance 記録が後続で当該 SHA を指名していれば有効)。
- `intrinsic=(INTERNAL-EXACT,canonical_file,anchor,fixed_SHA,PASS)`。externalと同じ5要素形とし、
  `canonical_file` は本ファイル、`fixed_SHA` は**受理された proof body の content SHA**(nonblocking
  minor 反映後)。効力は §10.7 の対応する acceptance 行(受理 review と content SHA を明記)が
  存在する場合に限る。

resolved entry の `source_ref` は RouteSpec の `source rule` に記された kernel name / canonical file / anchor
と一致しなければ無効である。単に external/intrinsic variantが一致するだけでは足りない。

S4a はこれとは別に

  CprimeSourceRule := (C-prime,
                       docs/2026-08-08-quadratic-phase-turan-K2.md,
                       §3 補題 C′,
                       eb1804acf103d05e3261073405deb1381b44c256, PASS)
  Cprime_ref := validated source_ref.external matching CprimeSourceRule

を必須inputとする。K2 theoremを使わないrouteだけの列でも、C′の chaining calculationを参照するなら
このrefを省略しない。従って `source_ref.external` と同じ検証で、指定 fixed SHA の canonical authoring
location が実際に PASS かを照合する。文字列 `PASS` の自己申告だけでは有効にならず、authoring statusが
不一致または未受理ならS4aを開始しない。現行ruleは R-K2-STATUS R4 が確認した canonical
fixed SHA/PASSを参照する。

`cost spec` も discriminated union とする。

- `uniform(C̄_route)`: `0<C̄_route<∞`、全recordで `C_step,k≤C̄_route`。
- `graded-root(C_RF,pair-difference-derivative)`: `0<C_RF<∞` のinterval-independent template。
  各RouteRecordが `Λ_{η,k}:=sup_{I_k}|η′|` をinstantiationし、
  `log C_step,k≤C_RF(1+Λ_{η,k})`。route ID=`root-far`、mode=weighted、`γ=5`、`κ̄=0`、
  `D-ROOT-FAR`、accepted RF proof refに限る。他routeへの流用と自由な k 依存は禁止する。

`graded-root` の `Λ_{η,k}` は raw coefficientでなく exact exponent difference `η=q₂−q₁` から計算する
node-function level dataである。ただし個別recordの値だけでは足りず、§10.5.2 RF-3のray-wide ledger refを
必須とする。

`A_ledger_kind` は `phase-lipschitz`、`weighted-no-A`、`polynomial-envelope` のいずれか。
`phase-lipschitz` は recordごとに `A_{H,k}≤Λ_{H,k}` を要求する。`weighted-no-A` は
`(S4-step-w)` と `mode=weighted` 専用、`phase-lipschitz` は `mode=unweighted` 専用。
`polynomial-envelope` も `mode=unweighted` とし、`log|P|` を含むためこの局所 boundを仮定しない。
その `assembly_state` は

- `open`、または
- `accepted(assembly_proof_ref)` (`assembly_proof_ref` は canonical authoring location/fixed SHA/PASSを
  検証した external/intrinsic source ref)

だけを許す。bare `accepted` は無効。零点cellを含む別の総和評価が未受理なら (E-w) を結論しない。

#### RouteRecord (interval-dependent instance)

S4b-β の `RouteRecord` は resolved `RouteKind` だけから生成し、次を持つ。

| field | type / validation |
|---|---|
| `kind_ref` | 上の resolved `RouteKind` ID。§10.5 RouteSpecとsource/assembly stateを継承しoverride不可 |
| `node_functions` | `arity=binary` なら exact `(A,B)`、`arity=unary` なら exact `(H)` |
| `domain_witness` | `domain_schema_id` の全 key に対する式またはidentity ref。自由文は禁止 |
| `selection_witness` | `(canonical_node_form,degree_class,root_held_guard,threshold_certificate)`。§10.5.5 の canonical route selector の出力。record の route ID が selector 値と一致しなければ無効。`canonical_node_form∈CanonicalNodeFormEnum`(enum 外は `uncertified` fail-close)。root 2+1 は `root_held_guard∈{held(M_k≤1/8),far(M_k>1/8)}` を `threshold_certificate` 付きで供給(`QR5-w`⇒held、`root-far`⇒far を必須)、非 root は `N/A` |
| `node_path` | fixed tree上の有限 path。公開stepは `root` で終わる |
| `envelope_id` | 上記 `U_H`; root 2+1 は `U_T` |
| `interval_id` | `(k,I_k,J_k,ε_chain)` |
| `frequency_allowance` | `(frequency_source,Λ_{H,k},bound_witness)`。`leaf_phase_max` なら `Λ_{H,k}:=max_j sup_{I_k}|q_j′|≤(1−δ)(a_k+1)+R`; 不使用なら `NONE` と `κ_H=0` |
| `A_ledger_witness` | `phase-lipschitz` の式、`weighted-no-A`、`polynomial-envelope/open`、または `polynomial-envelope/accepted(assembly_proof_ref)`。後者は `assembly_proof_ref` = accepted PΣ-2/PΣ-3(§10.5.4)に加え `frequency_allowance=leaf_phase_max`(補題 PΣ-3 (h2))を必須とし、`NONE` を許さない |
| `step_cost_witness` | `uniform(C̄_route): C_step,k≤C̄_route`、または `graded-root(C_RF,Λ_{η,k},N_cell,k,RF_proof_ref,ray_ledger_ref)`。後者は§10.5.2受理後だけ |
| `named_constants` | `(cost spec,γ_H=γ_route,κ_H≤κ̄_route,source_ref)`。raw係数依存は禁止 |

`RootStep_k` はこの recordを持つ root `node_path` の唯一の公開出力で、child routeは
`kind_ref/domain_witness` の内部 provenanceに畳み込む。S4a は root outputだけを一度ずつ消費する。

S4a は uniform routeについて mode別に

  γ_{*,u/w}:=max_{mode=u/w}γ_route,  C_{*,u/w}:=max_{mode=u/w}C̄_route

を取り(empty modeは `(γ_*,C_*)=(0,1)`)、同じ `ε_chain` を使う。unweighted `phase-lipschitz` recordは
C′ と同じ `ΣA+ΣκΛε_chain` の計算に入れる。`polynomial-envelope/open` が一つでもあれば、
`ΣA` の別証明なしに (E-w) を結論しない。weighted recordは `(S4-step-w)` の積とpointwise envelope growthを
別に帳簿化し、unweighted ledgerへ混ぜない。graded-root recordが受理された場合は
`Σ_k log C_step,k≤C_RF(N+Σ_kΛ_{η,k})` を別行で積算し、uniform の `C_{*,w}^N` へ偽装しない。

FR7 auditで合成式に現れてよい量は

  {RootStep provenance fields, node functions, U_H, compact-class envelope, Fock norm, named constants}

だけ。未列挙 identifierを route outputへ追加する場合はS4-0を先に改訂する。旧 flat parent `U_F`、
旧 DC discount、raw 原子係数、SVD coefficient、`1/t_m` を global comparison の入力にしてはならない。
係数は node functions と `U_H` を通じてのみ kernelへ入る。

### 10.5 Kernel routing interface

route 選択の前に exact zero-pruning を行う。任意の child functionが恒等零ならその childを削り、
残った exact spanで rank と treeを再固定して lower-rank routeへ戻す。従って active binary nodeは
両 child functionが恒等非零であり、その witness `active_children_nonzero=true` を必須 fieldとする。
この前処理は係数の小ささを閾値判定せず、恒等式としてだけ行う。

次表を active `RouteSpec` の唯一の authoring location とする。resolved rowの数値欄は必ず
`uniform(C̄)` またはaccepted RF proofに結合した
`graded-root(C_RF,pair-difference-derivative)`、
`0≤γ<∞`, `0≤κ̄<∞` を満たす。`—` は unresolved であり値を補ってはならない。

| route ID / shape | arity | mode / inequality | source rule | domain schema | `(cost spec,γ,κ̄)` | A-ledger / assembly rule | current obligation |
|---|---|---|---|---|---|---|---|
| `K2-u`: `c₁e^{q₁}+c₂e^{q₂}` | binary | unweighted / S4-step-u | `(K2,docs/2026-08-08-quadratic-phase-turan-K2.md,§2 主結果,eb1804acf103d05e3261073405deb1381b44c256,PASS)` | D-K2 | `(uniform(C_K2),2,1)` | phase-lipschitz / accepted | interval domain witness |
| `K2Q-aff-u`: `Pe^{q₁}+c₂e^{q₂}` | binary | unweighted / S4-step-u | `(K2Q-aff,docs/2026-08-09-quadratic-phase-turan-K2Q-weight21--wip.md,§6.1 K2Q-aff,96671e61ac62fdcf2160f63a03bf4f173f15f14a,PASS)` | D-K2Q-AFF | `(uniform(C_K2Q),4,1)` | polynomial-envelope / accepted(assembly_proof_ref) | `assembly_proof_ref=(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5.4 補題 PΣ-2,4d0f636c6b4c2e05bd09912164f97ff06e35ba41,PASS)+(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5.4 補題 PΣ-3,65bb02ef9f410460f127ad2339e49d8c903fe377,PASS)`、`leaf_phase_max` witness 必須 |
| `generalized-singleton-u`: `Pe^q` | unary | unweighted / S4-step-u | `(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5 generalized-singleton-u,56498bb6e6e53ec7a07bd4c131dae5ec0575be5c,PASS)` | D-GENERALIZED-SINGLETON | `(uniform(1),0,0)` | polynomial-envelope / accepted(assembly_proof_ref) | `assembly_proof_ref=(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5.4 補題 PΣ-2,4d0f636c6b4c2e05bd09912164f97ff06e35ba41,PASS)+(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5.4 補題 PΣ-3,65bb02ef9f410460f127ad2339e49d8c903fe377,PASS)`、`leaf_phase_max` witness 必須 |
| `QR5-w`: `B₁₂+c₃e^{q₃}`, `U_T` | binary | weighted / S4-step-w | `(QR5,docs/2026-08-09-pair-block-kernel-K2p1--wip.md,§3.8.6 QR5(U_T),27a1817150ab7a857cdd00320ed3809c73e3c1bd,PASS)` | D-QR5-HELD | `(uniform(C_T),5,0)` | weighted-no-A / accepted | interval-wide raw-held witness |
| `root-far`: root 2+1 far/unheld | binary | weighted / S4-step-w | `(QR5,docs/2026-08-09-pair-block-kernel-K2p1--wip.md,§3.8.6 QR5(U_T),27a1817150ab7a857cdd00320ed3809c73e3c1bd,PASS)+(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5.3 補題 RF,c271919d330c718a8e6f7d76af7fc1f052aa9d71,PASS)` | D-ROOT-FAR | `(graded-root(C_RF,pair-difference-derivative),5,0)` | weighted-no-A / accepted | interval domain witness(全 7 key)+ `step_cost_witness` |
| `trivial-u`: `ce^q` | unary | unweighted / S4-step-u | `(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5 trivial-u,56498bb6e6e53ec7a07bd4c131dae5ec0575be5c,PASS)` | D-TRIVIAL | `(uniform(1),0,0)` | phase-lipschitz / accepted | `A_{H,k}≤sup_{I_k}|q′|` witness |

`REFIX` は RouteSpec rowでなく前処理 transitionである。`q₁−q₂≡const`, `P≡0`, `c₂=0`、または
child恒等零を exact 併合/zero-pruningし、残った spanで rank/treeを再固定する。

`RECENTER(C,t_c)` もrouteではなく、resolved `root-far` route が各cell `C` でだけ使うexact表示transitionとする。
`η:=q₂−q₁` に対し

  q₂^C(t):=q₂(t)−η(t_c),   c₂^C:=c₂e^{η(t_c)}

と置けば `c₂^Ce^{q₂^C}=c₂e^{q₂}`、従って `B₁₂`、root function `H`、`U_T`、weighted normは
関数として不変で、pair差だけが `η^C(t)=η(t)−η(t_c)` となる。transition recordは
`(cell_id,t_c,exact_identity_ref)` だけを持ち、変換後のraw係数をS4a/FR7出力へ渡さない。
`η` が定数なら本transitionでheld扱いせず、先にconstant-gauge `REFIX`へ送る。

`RouteSpec` の assembly rule `accepted` は対応する intrinsic/external根拠でそのまま受理、`proof-required` は
`assembly_state=open` または `accepted(assembly_proof_ref)` だけを許す。従って K2Q-aff と
generalized-singletonを bare accepted に変更できない。

split(ii)/(iii) は旧 flat `U_F` 三者択一が `I_s` 全体から返す chart 観測であり、exact node function の
shape、unit interval の domain schema、`S4-step` inequality のいずれも供給しない。従って
`RouteKind` / `RouteRecord` categoryではなく、§5 と三原子一遷移文書の chart-only certificateとしてだけ残す。
certificateからFR2 chartへの接続が必要になっても、それはS4bのmissing kernelではなく別のpreparation義務である。

`root-far` はこれと異なり、現行exact treeで到達する。例えば nested 2+1族
`q₁=0`, `q₂=s_m²z`, `q₃=s_mz` (`s_m→0`) のactive pairでは、ray `z=te^{iθ}` 上
`|q₂−q₁|=s_m²t` なので十分遠いunit intervalで `sup|q₂−q₁|>1/8` となり、
raw `D-QR5-HELD` は適用できない。このrowは §10.5.2 の graded interface と §10.5.3 の補題 RF
(R-RF R2 PASS、fixed SHA `9f19389`; minors `c271919`)により resolved であり、
`M-ROOT-FAR-KERNEL` は解消済み。旧 flat `U_F` 転送は引き続き再導入しない。

K2 の査読statusは canonical
[K2 authoring file](2026-08-08-quadratic-phase-turan-K2.md)の R-K2 欄だけを参照する。
`K2-u` と `Cprime_ref` は R-K2-STATUS R4 が確認した同じ canonical fixed SHAを参照する。
K2Q の査読statusは canonical
[K2Q authoring file](2026-08-09-quadratic-phase-turan-K2Q-weight21--wip.md)だけを参照する。

#### 10.5.1 split-(i) exponent-4 root route の退役

三原子一遷移文書 §3.6.2 の旧転送は flat `U_F` / linearized `U′` に対する global estimateとして
保持するが、S4 root `U_T` の unit-stepへは移さない。canonical
[五次共鳴 §3.5](2026-08-09-pair-block-kernel-K2p1--wip.md)(fixed SHA
`27a1817150ab7a857cdd00320ed3809c73e3c1bd`)は、former routeのheld・非定数差・
非零child/linearized polynomial条件を満たしながら tree-envelope exponent 4 を反証する。
従って former category/domain/obligationをregistryから削除し、held 2+1 rootは `QR5-w` へ送る。
far/unheld root は現在 resolved `root-far` row(§10.5.3 補題 RF)が扱う。
旧 `U_F` 転送は引き続き再導入しない。

#### 10.5.2 RF graded interface (accepted specification)

本節を `RF-Spec`(accepted)の唯一のauthoring locationとする。review statusの唯一のauthoring locationは
§10.7 `S4-0.RF`/`S4-0.RF-PROOF` rowである。RF-1–RF-4 と RF proof(§10.5.3)は fixed SHA で受理済みで、
下の discriminant は §10.5 の resolved `root-far` row として active である。

受理後に意図するdiscriminantは route ID=`root-far`、arity=binary、mode=weighted / S4-step-w、
source rule=`(QR5 accepted ref + RF INTERNAL proof ref)`、domain=`D-ROOT-FAR`、
`(graded-root(C_RF,pair-difference-derivative),γ=5,κ̄=0)`、A-ledger=`weighted-no-A` である。
`frequency_source=NONE` とし、`Λ_{η,k}` は原子位相 allowanceでなくgraded step costだけへ入れる。

| ID | specification / acceptance target | current state |
|---|---|---|
| RF-1 exact recenter | 各cell `C` の中心 `t_c` で上の `RECENTER(C,t_c)` を行い、`B₁₂,H,U_T` の不変性と `η^C=η−η(t_c)` をidentityとして検証する。accepted QR5 sourceのraw held keyへは変換後表示を渡し、source statement自体をrecentered-heldへ書換えない | **accepted**(R-RF R2 PASS `9f19389`、minors `c271919`) |
| RF-2 cell chain | `Λ_{η,k}:=sup_{I_k}|η′|`、`h_k:=min(1,(4Λ_{η,k})^{-1})` (`Λ=0` では `h_k=1`)。長さ高々 `h_k`、shift高々 `h_k/2` のoverlap cellで `I_k` を覆い、各cellで `sup|η^C|≤1/8`、`N_cell,k≤4+8Λ_{η,k}` を示す。`J_k` 内のseedからrelative aperture `≥min(1,ε_chain/h_k)`、以後aperture `≥1/2` でQR5-wをchainする | **accepted**(R-RF R2 PASS `9f19389`、minors `c271919`) |
| RF-3 graded ledger | `L_T:=log(max(e,32C_T))`, `C_RF:=8L_T` を規定定数とし、RF-2から `C_step,k≤exp(C_RF(1+Λ_{η,k}))` を導く。collision witnessから全rayで `Λ_{η,k}≤s_m²(a_k+1)+s_m`、`Σ_kΛ_{η,k}≤4[s_m²(T+1)²+s_m(T+1)]` を示す。`s_m≤s_RF:=min(1,sqrt(δ/(64C_RF)))` なら `Σlog C_step,k≤(δ/8)T²+O(T)` として(E-w)のspare budgetへ入る | **accepted**(R-RF R2 PASS `9f19389`、minors `c271919`) |
| RF-4 fail-closed schema | `CostSpecEnum`、`D-ROOT-FAR`、`step_cost_witness`、ray-wide ledger ref、constants tableを同時に検査する。いずれかの欠落、R-RFSPEC未受理、RF proof ref未受理ならactive root-far rowの全discriminantを `—` のまま保つ(受理済みの現在は §10.5 row が全fieldを供給) | status pointer: §10.7 `S4-0.RF`/`S4-0.RF-PROOF` |

RF-2のchainは新しい三項解析kernelを仮定せず、fixed SHA `27a1817` で受理されたQR5の
`C_Tρ^{-5}` aperture形だけを消費する。ただし「短cellを作れば自動で閉じる」とは扱わず、seed cell、
境界cell、overlap multiplicity、hop数、上の規定定数の全てをRF proofで検算する。
real/oscillatoryのfar witnessは `RECENTER` 後の局所変動と `B₁₂` 零点を同時に含むacceptance fixtureとする。

#### 10.5.3 補題 RF の証明(accepted — R-RF R1 受理不可→全件受諾、R2 PASS fixed SHA `9f19389`、minors v0.9.4 `c271919`)

本節を RF proof の唯一の authoring location とする。受理 judgement の authoring location は
§10.7 `S4-0.RF-PROOF` 行。本受理により `root-far` row は resolved、`M-ROOT-FAR-KERNEL` は解消。

**補題 RF**: S4b-β の radial 窓 `I_k`(長さ 1)、overlap `J_k ⊆ I_k`(長さ `ε_chain`、`I_k` の
片端に接する)、衝突 cluster 入力の exact root 2+1 node `H = B₁₂ + c₃e^{q₃}`(active tree:
`c_j ≠ 0`、`q_j` 複素 2 次で **全 pair の差 `q_i−q_j` が非定数** — §2 constant-gauge quotient 済み
入力の domain witness を必須消費する。いずれかの差が定数なら本補題の適用前に `REFIX` 併合へ)、
`U_T = max(log|B₁₂|, m₃)`、`Λ_{η,k} := sup_{I_k}|η′|`(`η := q₂−q₁`)に対し

  ‖e^{−U_T}H‖_{∞,I_k}
  ≤ exp(C_RF(1+Λ_{η,k}))·ε_chain^{−5}·‖e^{−U_T}H‖_{∞,J_k},          (RF)

`C_RF := 8L_T`、`L_T := log max(e, 32C_T)`(`C_T` = accepted QR5 定数)。mode = weighted
(S4-step-w 型)、`γ = 5`、`κ_H = 0`、`frequency_source = NONE`。定数依存は `(C_T, cell 幾何)` のみで、
raw 係数・SVD/frame 係数・`m,θ,k,T` に依存しない。

*証明*

**(1) cell cover(RF-2 幾何)**: `h_k := min(1, (4Λ_{η,k})^{−1})`(`Λ_{η,k} = 0` は `h_k = 1`)。
`J_k` の接する端点を `e₀` とし、cell を `e₀` から反対端へ向けて
`C_i := [x_i, x_i+h_k] ∩ I_k`、`x_i := e₀ + i·h_k/2`(`J_k` が右端なら鏡映)と取り、最後の cell
だけは遠端 anchor `C_last := [端−h_k, 端]` に取り替える(全長 `h_k` を保ち、直前 cell との
overlap ≥ `h_k/2`)。cell 数は `N_k ≤ ⌈2/h_k⌉+1`: `h_k = 1` なら `N_k ≤ 3`、
`h_k = (4Λ)^{−1} < 1` なら `⌈8Λ⌉+1 ≤ 8Λ+2`。いずれも **`N_k ≤ 4+8Λ_{η,k}`** ✓(RF-2 の上界)。
seed は `E₀ := J_k ∩ C₀`、長さ `min(ε_chain, h_k)`。隣接 overlap `E_i := C_{i−1} ∩ C_i` は
長さ ≥ `h_k/2`(相対 aperture ≥ 1/2)。

**(2) RECENTER と held(RF-1)**: 各 `C_i` の中心 `t_i` で `RECENTER(C_i, t_i)`:
`q₂^{C_i} := q₂ − η(t_i)`、`c₂^{C_i} := c₂e^{η(t_i)}` は exact 恒等式
`c₂^{C_i}e^{q₂^{C_i}} = c₂e^{q₂}` を満たし、`B₁₂`・`H`・`U_T`・weighted norm は**関数として不変**、
pair 差だけが `η^{C_i} = η − η(t_i)` に変わる。mean value と `C_i ⊆ I_k` から

  sup_{C_i}|η^{C_i}| ≤ Λ_{η,k}·(h_k/2) ≤ 1/8.

変換後表示 `(c₁, c₂^{C_i}, c₃; q₁, q₂^{C_i}, q₃)` は QR5(fixed SHA `27a1817`)の **raw 仮定**を
`C_i` 上で満たす: `c_j ≠ 0` ✓ / atoms 相異 — `q₂^{C_i}−q₁ = η^{C_i}` は非定数(非定数 2 次の
定数シフト)、`q₂^{C_i}−q₃ = (q₂−q₃)−η(t_i)` は **domain witness の `q₂−q₃` 非定数**から非定数、
`q₁−q₃` 非定数は witness から直接。従って 3 exponent は pairwise 相異 ✓(注意: `q₂−q₃ ≡ const` の
入力では `η(t_i)` がその定数に一致し `q₂^{C_i} = q₃` となり得る — luna R-RF R1 反例
`q=(t², 2t², 2t²−1/256)`。この入力は §2 quotient で上流併合されるため domain 外であり、
witness の必須消費がこの穴を fail-closed に塞ぐ)/ pair held `β_B = sup_{C_i}|η^{C_i}| ≤ 1/8` ✓。
source statement 自体は書き換えず、変換後表示を渡すだけである(RF-1 の規約)。
affine 正規化 `φ_i: [0,1] → C_i` は複素 2 次 class・held 値・`U_T` の pointwise 定義・
相対 aperture を保つので、QR5 は `(K, E) = (C_i, E_i)` に長さ正規化して適用できる。

**(3) QR5 連鎖(RF-2 帳簿)**: 各 `i` で QR5-w:

  ‖e^{−U_T}H‖_{∞,C_i} ≤ C_T·(|E_i|/|C_i|)^{−5}·‖e^{−U_T}H‖_{∞,E_i}.

`i = 0`: `(|E₀|/h_k)^{−5} = max(1, h_k/ε_chain)^5 ≤ ε_chain^{−5}`(`h_k ≤ 1`)。
`i ≥ 1`(最後の anchor cell 込み): aperture ≥ 1/2 ⇒ 定数 ≤ `32C_T`。
`M_i := ‖e^{−U_T}H‖_{∞,C₀∪…∪C_i}` の帰納で(`32C_T ≥ 1`、`E_i` は被覆済み領域内)

  M_0 ≤ C_T ε_chain^{−5}‖·‖_{J_k},  M_i ≤ 32C_T·M_{i−1},

  ‖e^{−U_T}H‖_{∞,I_k} ≤ M_{N_k−1}
  ≤ ε_chain^{−5}(32C_T)^{N_k}‖·‖_{J_k}
  ≤ ε_chain^{−5}·exp(L_T(4+8Λ_{η,k}))‖·‖_{J_k}
  ≤ ε_chain^{−5}·exp(C_RF(1+Λ_{η,k}))‖·‖_{J_k}                    (4+8Λ ≤ 8(1+Λ))

で (RF) が従う。step cost は `Λ_{η,k}` のみを介して graded であり、原子位相 `Λ_{H,k}` の
allowance は使わない(`κ_H = 0`)。∎

**(4) graded ledger の吸収(RF-3)**: 衝突 cluster 入力(`d_w(ξ₁,ξ₂) ≤ s_m`)から
`|ΔA| ≤ s_m²`、`|ΔB| ≤ s_m`、ray `z = te^{iθ}` 上 `η′(t) = ΔA e^{2iθ}t + ΔB e^{iθ}` なので

  Λ_{η,k} ≤ s_m²(a_k+1) + s_m.

S4b-β の窓数は ≤ `2T+1 ≤ 2(T+1)`、`a_k+1 ≤ T+1` だから

  Σ_k Λ_{η,k} ≤ 2(T+1)[s_m²(T+1)+s_m] ≤ 4[s_m²(T+1)² + s_m(T+1)]   (余裕側; RF-3 の上界)。

`s_m ≤ s_RF := min(1, √(δ/(64C_RF)))` なら `4C_RF s_m²(T+1)² ≤ (δ/16)(T+1)²` で、`T ≥ 3` では
`(T+1)² ≤ (16/9)T²` より第一項 ≤ `(δ/9)T² ≤ (δ/8)T²`。残余は `C_RF(2+4s_m)(T+1) = O(T)`。従って

  Σ_k log C_step,k ≤ C_RF·Σ_k(1+Λ_{η,k}) ≤ (δ/8)T² + O(T)

で (E-w) の spare budget に入る。`s_m → 0` なので `m_RF := min{M ∈ ℕ: ∀m≥M, s_m ≤ s_RF}` が存在し、
本補題は `m ≥ m₀ := max(m_{FR-S1′/S1″}, m_RF)` で適用する(threshold 未満の有限個の m は
FR-S1 系と同じ「m 十分大」条項に畳む)。∎

**(5) acceptance fixture(§10.5.2 末尾の要求 — 局所検証、証明には数えない)**:
real witness(`q=(0, s²z, sz)`、`c=(1,1,1)`、`s=0.01`、窓 `[1251,1252]`、`θ=0`):
`Λ_η = 10^{−4}` ⇒ `h = 1`、`N ≤ 4.001`、recentered `sup|η^C| = 5·10^{−5} ≤ 1/8`、
天井 `sup g = 1.000007871 ≤ 2`(sampled)、窓比 `sup_I g/sup_J g ≈ 1.0`(`ε = 0.1`)。
oscillatory witness(`q=(0, is²z, isz)`、`c=(1,−1,1)`、窓 `[t*−0.45, t*+0.55]`、
`t* = 2π/s² ≈ 62831.85` = `B₁₂` 零点): 解析的には `t* ∈ I` なので `min_I|B₁₂| = 0`。
grid(刻み 1/4000、4001 点)は `t*` を格子点 k=1800 に**厳密に含み**、sampled 値
`3·10^{−31}` はその点の mp 丸めである。零点上でも `U_T = 0`(singleton 床)で有限、
天井 `sup g ≤ 2` ✓、recentered held ✓、窓比 ≈ 1.0。
mpmath dps 30(session-local 検証で証明には数えない。head からの再実行 fixture 化は R-RF の指示に従う)。

#### 10.5.4 polynomial ΣA program(PΣ-1/2/3/4 accepted — program closed)

本節を polynomial ΣA program の唯一の authoring location とする。program は
PΣ-1(局所補題)→ PΣ-2(max-envelope lift)→ PΣ-3(ray-wide ledger)→ PΣ-4(route 昇格:
`K2Q-aff-u`/`generalized-singleton-u` の `polynomial-envelope/open` を accepted へ)の 4 packet
に分割し(Sol consultation 2026-08-17 の分割案を採用)、本節は **PΣ-1/PΣ-2/PΣ-3/PΣ-4 の
全てを accepted として主張**する(PΣ-4 = R-PS4 R3 PASS `58b9c9f`)。

> **RetiredClaim: naive-sup-split(設計段階撤回・機械検算可能形)**: 不等式
> `sup_J(log|P|+r) ≥ log sup_J|P| + sup_J r` は**偽**。witness: `I = [0,1]`、`J = [0,ε]`、
> `P = t`、`r = −Mt`、`Mε > 1` で左辺 = `−log M − 1`、右辺 = `log ε`、gap = `1 + log(Mε)`
> (非有界)。従って `A_U` を log|P| 部と r 部の sup 差の和で直接押さえる本線当初案は成立せず、
> 正しい形は下の (ii) のとおり `osc_J r ≤ Λε` 項を伴う(Sol consultation 2026-08-17)。

**補題 PΣ-1**: `I = [a, a+1] ⊂ ℝ`、`J = [b, b+ε] ⊆ I` は**閉区間**、`ε ∈ (0,1]`。
`P ≢ 0` 複素係数 `deg P ≤ 2`、`r: I → ℝ` は連続で `sup_I|r′| ≤ Λ`、`U := log|P| + r`
(`log 0 := −∞`)、`osc_J r := sup_J r − inf_J r` とする。このとき

  (i) sup_I|P| ≤ 8ε^{−2}·sup_J|P|;
  (ii) A_U := sup_I U − sup_J U ≤ log(8ε^{−2}) + (sup_I r − sup_J r) + Λε.

*証明*: (i) `J` の両端 `t₀, t₂` と中点 `t₁` の 3 点 Lagrange 補間で
`P(t) = Σ_i P(t_i)ℓ_i(t)`。`t ∈ I` で分子因子は各 ≤ 1(`|I| = 1`)、分母は
`|t₀−t₁| = |t₁−t₂| = ε/2`、`|t₀−t₂| = ε` なので
`|ℓ₀| ≤ 2ε^{−2}`、`|ℓ₁| ≤ 4ε^{−2}`、`|ℓ₂| ≤ 2ε^{−2}`、合計 `8ε^{−2}`。複素係数は
三角不等式でそのまま通る。
(ii) `sup_I U ≤ log sup_I|P| + sup_I r`。`J` 上の `|P|` の maximizer `t*` で
`sup_J U ≥ U(t*) = log sup_J|P| + r(t*) ≥ log sup_J|P| + sup_J r − osc_J r`、
`osc_J r ≤ Λε`。両者の差に (i) を代入。∎

`P ≡ 0` は route 適用前の exact zero-pruning が排除する。孤立零点は (i)(ii) に影響しない
(`sup_J|P| > 0`)。定数 8 は ε → 0 で漸近的に sharp(下の数値)。

**sharpness**: 配置 `I = [0,1]`、`J = [0,ε]`、評価点 `t = 1` で Lagrange 係数和は厳密に
`ε²Σ|ℓ_i| = 8 − 8ε + ε²`(ε = 0.5/0.1/0.01 で 4.25/7.21/7.9201 — ε → 0 で 8 に漸近、
定数 8 は改善不能)。(ii) の全体も `J = [1−ε,1]`、`P_ε = T₂(2(t−1+ε)/ε − 1)`(Chebyshev)、
`r = −Mt` で漸近 sharp(luna R-PS1 検算: bound との差 `log(8/(8−8ε+ε²)) + Mε → 0`)。
ランダム複素 deg ≤ 2 の 2×10⁴ 配置探索(seed 2、係数 [−1,1]² 一様、診断用・非証拠)で
違反なし(最大比 ×ε² = 1.13)。

**補題 PΣ-2(max-envelope lift — accepted)**: `I = [a, a+1]`、
`J = [b, b+ε] ⊆ I` 閉区間、`ε ∈ (0,1]`。`P ≢ 0` 複素係数 `deg P ≤ 2`、`q₁, q₂` は複素
2 次多項式で `r_i := Re q_i`、`Λ := max_i sup_I|r_i′|` とする。

  (u) unary(`generalized-singleton-u` 形)`H = P e^{q₁}`、`U_H := log|P| + r₁`:
      `A_{U_H} := sup_I U_H − sup_J U_H ≤ log(8ε^{−2}) + (1+ε)Λ`;
  (b) binary(`K2Q-aff-u` 形)`H = P e^{q₁} + c₂ e^{q₂}`(`c₂ ≠ 0`)、
      `U_H := max(log|P| + r₁, log|c₂| + r₂)`: 同じ bound `A_{U_H} ≤ log(8ε^{−2}) + (1+ε)Λ`。

*証明*: **窓 Lipschitz**: `sup_I|r′| ≤ Λ` なら任意の `t_J ∈ J` に対し
`sup_I r ≤ r(t_J) + Λ·sup_{t∈I}|t − t_J| ≤ sup_J r + Λ`(`J ⊆ I`、`|I| = 1`)。
(u) PΣ-1(ii) に `sup_I r₁ − sup_J r₁ ≤ Λ` を代入して
`A ≤ log(8ε^{−2}) + Λ + Λε`。
(b) **max-lift**: 任意の集合 `X` で `sup_X max(U₁,U₂) = max(sup_X U₁, sup_X U₂)`、および
`max_i a_i − max_i b_i ≤ max_i(a_i − b_i)`(`max_i a_i = a_j` とすれば
`a_j − max_i b_i ≤ a_j − b_j`)。よって branch 別に押さえれば足りる:
branch 1 は (u) で `≤ log(8ε^{−2}) + (1+ε)Λ`;branch 2 は定数 `log|c₂|` が差で消え
`A_{U₂} = sup_I r₂ − sup_J r₂ ≤ Λ ≤ log(8ε^{−2}) + (1+ε)Λ`(`log(8ε^{−2}) ≥ log 8 > 0`)。∎

`P ≡ 0` は exact zero-pruning が排除、`c₂ = 0` は (u) に退化(binary route の premise は
`c₂ ≠ 0`)。**interface(PΣ-3 が消費、ここでは非主張)**: phase-lipschitz record の
per-window bound `A_{H,k} ≤ Λ_{H,k}` を、polynomial-envelope record では
`A_{H,k} ≤ log(8ε_chain^{−2}) + (1+ε_chain)Λ_{H,k}` に置換する。加算 penalty
`log(8ε_chain^{−2})` は polynomial-envelope record を消費する窓数 `N_s` に線形で、
`N_s ≤ N ≤ 2T+1 = O(T)`(`N` = §10.3 の総窓数)— ray-wide の二次 budget
`(1−δ/2)T²/2` への吸収は PΣ-3 の義務であり本補題は主張しない。数値診断(非証拠):
ランダム 8×10³ 配置(seed 7、deg ≤ 2 複素 P、2 次 phase、`ε ∈ {0.5, 0.2, 0.1}`、
grid 501/201 点)で違反なし、bound との最小余裕 3.62。

**補題 PΣ-3(ray-wide ledger — accepted)**: `δ ∈ (0,1]`、`R ≥ 0`、
`κ_chain ≥ 0`(compact class `K_{δ,R}` 契約から継承)。§10.3 S4b-β の segmentation を
**C′ と同一の endpoint 規約**で取る:

  (h0) `T ≥ 3`、`β := 1−ε_chain`、`ε_chain = min(1/2, δ/[8(κ_chain+1)])`、
       `a_1 = T−1`、`a_{k+1} = a_k − β`(`k = 1..N`)、停止は最初の `a_N ≤ 1`。
       全窓 `I_k = [a_k, a_k+1]` は切断なしの長さ 1、`a_k ≥ ε_chain > 0`、`N ≤ 2T+1`。

各窓の unweighted record が次を満たすとする:

  (h1) A_ledger_kind ∈ {phase-lipschitz, polynomial-envelope}。前者は `A_{H,k} ≤ Λ_{H,k}`
       (§10.4 の record 義務)、後者は補題 PΣ-2 の premise(deg ≤ 2、2 次 phase)を満たし
       `A_{H,k} ≤ log(8ε_chain^{−2}) + (1+ε_chain)Λ_{H,k}`;
  (h2) frequency witness(`leaf_phase_max` 形): `Λ_{H,k} ≤ (1−δ)(a_k+1) + R`
       (polynomial-envelope の `Λ_{H,k} := max_i sup_{I_k}|r_i′|` は
       `sup_{I_k}|r_i′| ≤ sup_{I_k}|q_i′|` で同じ witness に結ぶ);
  (h3) `κ_H ≤ κ_chain`。

このとき ray 全体の unweighted ledger は

  Σ_{k=1}^{N} [A_{H,k} + κ_H Λ_{H,k} ε_chain]
  ≤ (1−δ/2)·T²/2 + C_ΣA·(T+1),   C_ΣA := 2log(8ε_chain^{−2}) + 4R + 2,

を満たし、`C_ΣA` は `(δ, R, κ_chain)` のみに依存(`m, θ, k, T` 非依存)。

*証明*: (h1)(h3) より各 record で
`A_{H,k} + κ_HΛ_{H,k}ε_chain ≤ log(8ε_chain^{−2}) + (1 + (κ_chain+1)ε_chain)Λ_{H,k}`
(phase-lipschitz は `log(8ε_chain^{−2}) ≥ log 8 > 0` により同形へ緩める)。
`(κ_chain+1)ε_chain ≤ δ/8` だから係数は `1 + δ/8` 以下。
**窓和の算術**: (h0) より `a_k + 1 = T − (k−1)β` で切断なし(`a_k > 0` は停止規則から自動)。

  Σ_{k=1}^{N}(a_k+1) = NT − βN(N−1)/2 = −(β/2)N² + (T+β/2)N。

この二次式の実数上の最大値は `(T+β/2)²/(2β) = T²/(2β) + T/2 + β/8 ≤ T²/(2β) + T` であり、
bound は停止規則の定める `N` に依らず**全ての `N ≥ 1` で成立**する。
`1/β ≤ 1 + 2ε_chain`(`ε_chain ≤ 1/2`)と (h2)(`R ≥ 0`)より

  Σ_k Λ_{H,k} ≤ (1−δ)[(1+2ε_chain)T²/2 + T] + RN。

`ε_chain ≤ δ/8` から二次係数は `(1+δ/8)(1+δ/4)(1−δ) ≤ 1−δ/2`(展開すると差は
`−δ/8 − 11δ²/32 − δ³/32 < 0`)。線形項は `N ≤ 2T+1 ≤ 2(T+1)`、`1+δ/8 ≤ 2`、`R ≥ 0` で
`N log(8ε_chain^{−2}) ≤ 2(T+1)log(8ε_chain^{−2})`、`(1+δ/8)RN ≤ 4R(T+1)`、
`(1+δ/8)(1−δ)T ≤ 2(T+1)`。合わせて主張の形。∎

**scope(非主張)**: 本補題は unweighted record の per-node ray ledger のみ。weighted route
(`QR5-w`/`root-far`)の graded ledger は RF-3(accepted)が別掌理。node 間 assembly・
D-相殺・coverage・(E-w) 本体・近原点領域(半径 ≲ 2、C′ 同様 S4a の compact initial estimate
が掌理)は本補題の非主張。route 昇格(`polynomial-envelope/open` → accepted)は (h2) の
frequency witness を polynomial-envelope record の必須 field に追加する registry 手術を要し、
PΣ-4 として §10.5/§10.4 に実施済み(R-PS4 R3 PASS `58b9c9f`)。数値診断(非証拠): 窓和二次式 bound は
`T ∈ {3..1000} × ε ∈ {0.5..0.01} × 全 N ≤ 3T+3` の掃引で余裕最小 1.39、停止規則の実 N でも
違反なし、係数不等式は `δ ∈ (0,1]` 掃引で余裕最小 1.25×10⁻⁴(δ = 10⁻³)。

| ID | scope | state |
|---|---|---|
| PΣ-1 局所補題 | 本節 (i)(ii) | **accepted**(R-PS1 PASS、fixed SHA `f875d76`; minors `050156b`) |
| PΣ-2 max-envelope lift | `U_H = max(log|P|+Re q₁, log|c₂|+Re q₂)` への持ち上げ | **accepted**(R-PS2 PASS、fixed SHA `540d0c1`; minors `4d0f636`) |
| PΣ-3 ray-wide ledger | C′ 帳簿との合成、二次係数 `1−δ/2` | **accepted**(R-PS3 R2 PASS、fixed SHA `65bb02e`) |
| PΣ-4 route 昇格 | `polynomial-envelope/open` → accepted(assembly_proof_ref) | **accepted**(R-PS4 R3 PASS、fixed SHA `58b9c9f`) |

#### 10.5.5 S4b-COV: canonical route selector と ray coverage(COV0/COV1 accepted — S4b-COV closed)

本節を S4b coverage program の唯一の authoring location とする。program は
COV0(selection schema 手術、proof claim なし)→ COV1(canonical coverage lemma)の 2 packet
に分割する(Sol consultation 2026-08-17 第 2 回の設計を採用)。COV0/COV1 とも accepted
(下表)であり、S4b coverage program は閉鎖済み。

**動機(DomainSchema は selector ではない)**: §10.4 の 6 schema は kernel の適用前提であり、
排他的 partition ではない。実際 (i) `deg P=0` の `P` は `D-K2` と `D-K2Q-AFF` の両方で表現可能、
(ii) 同様に `D-TRIVIAL` と `D-GENERALIZED-SINGLETON` の両方で表現可能、(iii) `D-ROOT-FAR` は
far 条件を key に持たないため held interval でも全 key が成立し得る。従って「schema の排他性」を
証明対象にせず、**canonical route selector の完全・排他的 partition** を証明対象とする。

**canonical node form の閉世界**: selector の定義域を

  CanonicalNodeFormEnum := {root-2+1, binary-pure-atom, binary-poly-deg12,
                            unary-poly-deg12, unary-atom}

に固定する。enum 外の form — 特に `deg P ∈ {3,4,5}` の unary/binary(FR3 は plain c=3 で
`d_ℓ ≤ 5` を許容する)と both-polynomial binary `P₁e^{q₁}+P₂e^{q₂}` — は selector を持たず、
出現した場合は **`uncertified` として S4b-α/β を fail-close** する(仮 route への coercion 禁止)。
「S4b で routing される node form が本 enum に含まれる」ことは未証明であり、補題 S4b-COV の
第一義務 (COV-0) とする。COV-0 が偽なら S4-0 を改訂して route category を追加してから進む。

**canonical route selector**(global exact `REFIX`/zero-pruning を**一度だけ**行った後の
canonical node form に対して定義。interval ごとの tree 再構成は禁止):

1. root 2+1(pair-block + singleton): `M_k := sup_{I_k}|q₂−q₁|` とし、
   `M_k ≤ 1/8` なら `QR5-w`、`M_k > 1/8` なら `root-far`。**等号 `M_k=1/8` は held(`QR5-w`)**。
   閾値の certificate は `|η(t)|²` の閉区間最大値を端点値と導関数実根から検証する。checker が
   等号側/超過側を証明できない場合は推測で送らず `uncertified` として fail-close する。
2. 非 root binary pure-atom pair(両 child とも `deg=0`): `K2-u`。
3. binary `Pe^{q₁}+c₂e^{q₂}` で `deg P∈{1,2}`: `K2Q-aff-u`。
4. unary `Pe^q` で `deg P∈{1,2}`: `generalized-singleton-u`。
5. unary `ce^q`(`deg P=0`): `trivial-u`。

selector 出力は `RouteRecord.selection_witness`(§10.4)に記録し、route ID と不一致の record は
無効とする。root 2+1 では `QR5-w` record に `root_held_guard=held`、`root-far` record に
`root_held_guard=far` を**必須**とし、`M_k` の閾値判定は `threshold_certificate`
(`|η|²` の端点値+導関数実根による閉区間最大値検証)として witness 内に保存する。
`D-ROOT-FAR` の 7 key に far 条件は**戻さない** — far 条件は schema でなく selector witness が
供給する。held/far が interval 内で閾値を跨ぐ場合も **coverage 用の有限再分割は行わない**:
`M_k` は閉区間 sup による完全二分であり、跨ぐ窓は全体を `root-far` に割り当て、内部は補題 RF の
cell chain が処理する(公開 record は一つのまま)。

**RayCoverageManifest**: 固定 ray `(θ,T)` に対し

  RayCoverageManifest_{θ,T} := (K_T, (R_k)_{k∈K_T}, TerminalRecord),   K_T := {1,…,N−1}。

`J_k = I_k∩I_{k+1}` が定義されるのは `k<N` のみであり、`RouteRecord` は `k∈K_T` にだけ立てる。
最終窓 `I_N ⊂ [0,2]`(停止規約より `ε_chain ≤ a_N ≤ 1`)は **`TerminalRecord`** へ送り、
RouteRecord と二重計上しない。`TerminalRecord` の消費者は S4a の補題 C0(§10.8、accepted
`f31cca0`)であり、chaining ledger の外に置く。**ray ledger の index 契約**:
PΣ-3(unweighted subledger)と RF-3(weighted ledger、独立帳簿)の record 和はいずれも
`k∈K_T` 上で主張する。`k=N` は record を持たず、`A_{H,N}`/`C_step,N` は**定義しない**
(`J_N` を暗黙に再導入しない)。両証明中の等差 majorant(k=1..N の窓和)は各項非負性により
`K_T` 部分和を a fortiori に押さえる。
manifest は各 `R_k` の mode を `ray_mode` witness として出力し、S4a-M1 が weighted/unweighted の
二次 ledger を同一 ray で加算しないことの検査入力とする。

**補題 S4b-COV(canonical root coverage — accepted)**:
compact-class input を exact `REFIX`/zero-pruning して canonical form を固定すると、任意の ray・
`T≥3`・§10.3 pinned segmentation に対し

  (COV-0) canonical form closure: `REFIX`/zero-pruning 後に S4b routing へ到達する全 node form
          は CanonicalNodeFormEnum に含まれる(特に routed node で `deg P ≤ 2`、
          both-polynomial binary 非生成);
  (COV-1) Σ_{ρ∈CategoryEnum} 𝟙_{Sel_ρ(F,I_k)} = 1  (k∈K_T);
  (COV-2) 各 k∈K_T にちょうど一つの RouteRecord `R_k` が構成され、全 required witness を持ち、
          {interval_id(R_k)} = K_T(重複判定は幾何学的点でなく `interval_id`)。

**補題 S4b-COV の証明(accepted — R-COV1 R4 PASS、fixed SHA `c36d818`)**:

*(COV-0) canonical form closure.* 主張は **`S4b RouteRecord` に到達する exact finite-m node**
に限定した reachability invariant であり、全 chart construction の閉世界性ではない。
`RouteRecord` producer は現行 S4-0 interface が宣言する次の閉集合に限る: (g1) atom leaf
`c_je^{q_j}`(枠候補は原子の exact 有限結合 `h_{ℓ,m}=Σ_{j=1}^3 a_{ℓj,m}u_{j,m}`、§3);
(g2) tree node の exact 和 `H=A+B`(§3 の rooted **binary** block tree。c=3 の tree shape は
single-scale triple または 2+1 のみ — いずれも scale label であり root は
pair-block+singleton — 深さ ≤ 2); (g3) `REFIX`(constant-gauge 併合は係数を統合して
純指数和を保ち、zero-pruning は child を削除、rank 低下時は lower-rank route へ**退出**して
c=3 routing の対象外); (g4) `RECENTER`(関数として不変、§10.5)。いずれの生成規則も
多項式因子を導入しない。従って routed node form は
{unary-atom, binary-pure-atom, root-2+1} ⊆ CanonicalNodeFormEnum
に含まれ、rank 3 の root node は常に root-2+1 形である。**非 producer の明示**
(reachability invariant): 一遷移文書 §3.6.1 の exact (2,1) 化の出力 `F_{≤1}=P_Be^{q₁}+c₃e^{q₃}`
(`P_B=(c₁+c₂)+c₂η`)、FR-S1″ の静的極限列 `G_{ν̂,0}=L_{ν̂}`、および split(ii)/(iii) の出力は、
いずれも chart/wrapper 評価の対象であって `RouteRecord` producer ではない(一遷移文書
§3.6.2「本項は flat U_F の旧wrapper/chart評価」、§10.5「exact node function の shape、
unit interval の domain schema、S4-step inequality のいずれも供給しない」
= v0.8.16 reachability audit)。
現行 interface に polynomial-weighted node の生成 transition は存在せず、
binary-poly-deg12 / unary-poly-deg12 は **resolved-but-unreachable**(row は将来の S4-0 改訂
= 例えば split(ii) の routing 昇格に備えて保持するが、record を受け取らない。当該改訂時は
COV-0 の再証明を必須とする)。both-polynomial binary は a fortiori 非生成。
`deg P∈{3,4,5}` について: FR3 の `d_ℓ≤5` は静的極限対象 `P_ℓΦ(ξ*)`(z=0 valuation)に付随し
(補題 W は「rescaling、Fock tail、nested 2+1 は本補題の外」、補題 W′ は「静的極限だけを扱う。
finite-m … は主張しない」と適用範囲を明示)、S4b が routing する finite-m exact node は
その対象外。∎(COV-0)

*(COV-1) selector totality/exclusivity.* 到達可能 form ごとに: unary-atom は `deg=0` なので
clause 5 のみ(clause 3/4 は `deg∈{1,2}`、clause 1/2 は binary を要求)。binary-pure-atom は
非 root(rank 3 の root は root-2+1、root で純 pair が生じる constant-gauge 併合は rank 低下
= c=3 退出)なので clause 2 のみ。root-2+1 は clause 1 のみで、内部の
`M_k ≤ 1/8` / `M_k > 1/8` は compact `I_k` 上の連続関数 `|η|` の sup による完全・排他二分
(等号は held、certificate は §10.5.5 規約)。非到達 enum form の clause 3/4 は空虚に
単価値。enum 外 form は COV-0 より非生成(生成された場合は `uncertified` fail-close が
S4b-α/β を停止し、被覆主張自体が成立しない = fail-closed)。従って `k∈K_T` の各 `I_k` で
`Σ_ρ 𝟙_{Sel_ρ} = 1`。∎(COV-1)

*(COV-2) record 構成.* root record は clause 1 の値により `QR5-w` または `root-far`。
witness 構成: `active_children_nonzero` は zero-pruning 完了から、`c₁c₂c₃≠0` は
**selector が root-2+1 を選んだこと自体**から(zero-pruning 後に三つの非零 leaf が残る場合に
のみ root-2+1 形が成立する。係数が一つでも零なら pruning により binary/unary へ落ち、
lower-rank route に再分類される — rank を根拠にしない)、`B₁₂≢0` は zero-pruning(恒等零
child は削除済み)から、`η=q₂−q₁` nonconstant(および root-far の `q₁−q₃`/`q₂−q₃`
nonconstant)は constant-gauge `REFIX` 完了から。collision-scale witness は §2 の入力仮定
= **単一の `d_Ω`-衝突 cluster** と `s_m := max_{i,j} d_w((A_{i,m},B_{i,m}),(A_{j,m},B_{j,m}))`、
`d_w((A,B),(A′,B′)) := max(|A−A′|^{1/2}, |B−B′|)` から従う: 全 pair で `d_w ≤ s_m` なので
定義より直ちに `|A_i−A_j| ≤ s_m²`、`|B_i−B_j| ≤ s_m`(compactness を出典にしない)。
RF の graded ledger まで主張する場合は `m ≥ m₀` を要求する
(`m₀ := max(m_{FR-S1′/S1″}, m_RF)` なので `m₀ ≥ m_RF`)。
`Λ_{η,k}` witness は exact `η′` の閉区間 sup として計算可能。`D-QR5-HELD` の
`sup_{I_k}|q₂−q₁|≤1/8` は clause 1 の held certificate そのもの。selector の単価値性
(COV-1)より各 `k∈K_T` にちょうど一つの root record が立ち、`{interval_id(R_k)} = K_T`。
child route(clause 2–5)は RootStep_k の内部 provenance であり(§10.3 条件 6)、manifest の
record としては数えない。`I_N` は `TerminalRecord`(§10.5.5)。∎(COV-2)

**scope(非主張)**: 本補題は canonical form の閉世界性・selector 被覆・record 構成可能性
のみを主張する。QR5-w/root-far の kernel 不等式の成立(accepted 済み)、S4a assembly、
(E-w)、chart-only の split(ii)/(iii) の解析的内容は本補題の対象外。**三層の区別**:
(層 1) resolved registry row = kernel capability(reachable producer の存在を含意しない);
(層 2) current producer = COV-0 の帰結として polynomial row には現在存在しない;
(層 3) public RootStep consumer = 現 c=3 の root record は weighted(QR5-w/root-far)のみで、
polynomial-envelope の実 consumer は現在ない(dead generality であって矛盾ではない。
PΣ program の acceptance は capability の証明として有効なまま)。unreachable row の将来
到達可能化(S4-0 改訂)は COV-0 再証明 + R-COV 再査読を必須とする。

| ID | scope | state |
|---|---|---|
| COV0 selection schema 手術 | 本節 + §10.4 `selection_witness`/manifest 分離 | **accepted**(R-COV0 R3 PASS、fixed SHA `256ab38`) |
| COV1 canonical coverage lemma | (COV-0)(COV-1)(COV-2) の証明 + fail-closed mutation tests | **accepted**(R-COV1 R4 PASS、fixed SHA `c36d818`) |

### 10.6 Coefficient-free constants

FR5 の各 kernel 定数は `(γ_H,κ_H,δ,R,route label)` と下表の reviewed/compact dataだけに依存し、
表示係数には依存させない。

| name | meaning / permitted dependency | supplied by |
|---|---|---|
| `c_head` | plain/nested head singular floor (`η,t₀` 等のchart data) | FR-S1′/S1″ |
| `C_tail` | normalized frameのFock tail | FR-S1′/S1″ |
| `C_K2,C_K2Q,C_T` | pair/generalized/root kernel constants | K2/K2Q/QR5。消費時は `max(1,·)` へ正規化してよい(上界定数の拡大は accepted 不等式を保存。RF 帰納の inline 前提 `32C_T ≥ 1` の契約化、§10.8 W3) |
| `cost spec,γ_route,κ̄_route,mode` | interval-independent RouteKind template。uniformまたはaccepted graded-root | S4b-α registry |
| `C_step,k,γ_H,κ_H,ε_chain` | typed RouteRecord / composite unit-step data | S4b-β output |
| `N_cell` / `N_cell,k` | uniform routeの一様cell数 / root-far のgraded cell数 | pairは高々3。root-far は `≤4+8Λ_{η,k}`(補題 RF (1)、accepted) |
| `Λ_{η,k},C_RF,s_RF` | root pair差のcell変動、graded cost定数、large-m threshold | §10.5.2 RF-2/RF-3 + §10.5.3(accepted) |
| `Cprime_ref` | validated external source_ref specialized to C′ | S4a required external input |
| `C_chain,u`, `C_chain,w` | mode別 product/telescoping constants | S4aでtyped kernel dataから別々に構成 |
| `C_w,C_lin` | (S4-Ew) constants | S4a output |

tree depthは高々2だが、S4aが消費するのは各 `I_k` の一つの `RootStep_k` だけである。child constantの
有限積はその root step内部へ一度だけ吸収し、ancestor/rootと別に再積算しない。stopping-time/Bellman
quantityは c=3 S4 のinterfaceへ加えず、一般 c で必要性を再判定する。

### 10.7 S4-0 acceptance ledger

| ID | specification | current state |
|---|---|---|
| S4-0.1 | packet順 S4b→S4a→S4c と非循環input/output | **PASS (R9、`56498bb`)** |
| S4-0.2 | c=3 (E-w)、一般 c (E-d) 保持 | **PASS (R9、`56498bb`)** |
| S4-0.3 | registry→ε_chain→record の順序 + mode別root-step | **PASS (R9、`56498bb`)** |
| S4-0.4 | RouteSpec literal source / root-only積算 / FR7 vocabulary | **PASS (R9、`56498bb`)** |
| S4-0.5 | complete domain keys・category-bound exclusion・status fail-closed | **PASS (R9、`56498bb`)** |
| S4-0.RF | RECENTER exact transition、graded-root cost、D-ROOT-FAR、RF-1–RF-4 fail-closed extension | **PASS (R-RFSPEC R3、fixed SHA `25afe6ebb54f93845d48b8993ff7523f0f2643d8`)** |
| S4-0.RF-PROOF | 補題 RF(§10.5.3): RECENTER 恒等式、cell cover/chain、graded ledger 吸収、fixture | **PASS (R-RF R2、fixed SHA `9f19389`; minors v0.9.4 `c271919`)**。`root-far` row resolved、`M-ROOT-FAR-KERNEL` 解消 |
| S4-0.RF-PROMOTE | `root-far` row の registry 昇格手術(§10.5 row、status surface 同期、fail-closed tests) | **PASS (R-RF-PROMOTE R3、fixed SHA `9cca48d`)**(R1/R2 findings は v0.10.1–v0.10.3 で全件受諾、R4 で tests 確認) |
| S4-0.PS | polynomial ΣA program(§10.5.4 補題 PΣ-1/PΣ-2/PΣ-3) | **PASS**(R-PS1 fixed SHA `f875d76`、minors `050156b`; R-PS2 fixed SHA `540d0c1`、minors `4d0f636`; R-PS3 R2 fixed SHA `65bb02e`) |
| S4-0.PS-PROMOTE | `K2Q-aff-u`/`generalized-singleton-u` の polynomial-envelope 昇格手術(§10.5 rows、§10.4 witness 必須化、fail-closed tests) | **PASS (R-PS4 R3、fixed SHA `58b9c9f`)**(R1/R2 findings は v0.11.8–v0.11.9 で全件受諾、R3 で revert fail-closure を実地確認) |
| S4-0.COV0 | S4b-COV0 selection schema 手術(§10.5.5、§10.4 `selection_witness`、manifest 分離、K_T index 契約) | **PASS (R-COV0 R3、fixed SHA `256ab38`)**(R1/R2 findings は v0.12.2–v0.12.3 で全件受諾。accepted body への in-body 編集は revert し、SHA-256 バイト一致を双方検証) |
| S4-0.COV1 | 補題 S4b-COV((COV-0) reachability invariant、(COV-1) selector 被覆、(COV-2) witness 構成) | **PASS (R-COV1 R4、fixed SHA `c36d818`)**(R1–R3 findings は v0.12.6–v0.12.8 で全件受諾)。**S4b closure 完結** |
| retired split-(i) exponent-4 root route | §10.5.1、canonical 五次共鳴 | retired。held rootは `QR5-w` |
| S4a proofs | §10.8 program | **全 8 packet accepted**: W1 `a59768e`/W2 `a0fcd10`/C0 `f31cca0`/M1 `fd18e9d`/W3 `4086ef9`/W4 `cb87eee`/EW-B・EW `b39216f` — **(S4-Ew) 閉鎖** |
| S4c proofs | N3′/N4 同期、FR7 no-return audit、original/gauged provenance 同期 | open, not claimed |

### 10.8 S4a envelope assembly program(全 8 packet accepted — S4a 完結、(S4-Ew) 閉鎖)

本節を S4a program の唯一の authoring location とする。Sol consultation 第 3 回
(2026-08-17、W1 係数予算監査)の改訂設計を採用し、packet を次に固定する。

**予算の確定(consultation 検算、本線で数値確認)**: accepted L2a′(c=2) の出口係数は
`(1−δ/2)` であり、(E-w) target `(1−δ/2)T²/2` を使い切るため、weighted chain の RF 二次費用
`(δ/8)T²` を加算する余地が**現行の「L2a′ 出口 + RF 加算 ledger」architecture では**ない
(D-相殺で消えるのは `D_H⁻¹D_H` のみ。別 architecture の論理的可能性は排除しないが、
いずれも未証明であり本 program は採らない)。従って本 program は
**c=2 強形出口(係数 `(1−δ)` + 多項式因子)** を W2 で証明する。強形出口では
`(1−δ)T²/2 + (δ/8)T² = (1−3δ/4)T²/2` となり、target まで**二次係数に**なお `(δ/8)T²` の
余裕がある(線形項・多項式因子は別途 `C_lin(T+1)` へ吸収する)。

**語彙**: 全 node は zero-pruning 後で `R_H := ‖H‖_ℱ > 0` とする。binary node `H = X + Y` に

  D_H := max(‖X‖_ℱ, ‖Y‖_ℱ)/R_H,   E_{δ,R}(t) := exp((1−δ)t²/2 + Rt),

unary node `H = X` には `e^{U_H(t)} = |X(z)|`、`D_H := ‖X‖_ℱ/R_H = 1` とする。
per-child strong bound とは `|X(z)| ≤ C_X P_X(t) E_{δ,R}(t) ‖X‖_ℱ`(`C_X > 0` 定数、
`P_X: [0,∞) → [0,∞)` は m 非依存・固定次数の非負係数多項式)の形をいう。raw 原子係数は
いずれの statement にも現れない(proof-local に導入し即座に norm で消去する。
FR7 audit 語彙は不変)。原子 parameter は compact class
`K_{δ,R} = {|A| ≤ 1−δ} × {|B| ≤ R}`(定義の authoring location は K2 文書
`docs/2026-08-08-quadratic-phase-turan-K2.md` §設定)に属するとする。

**補題 W1(Child-reserve interface — accepted、R-W1 R2 PASS `a59768e`)**: binary node `H = X + Y` の
各 child が per-child strong bound を満たすなら、ray `z = te^{iθ}` 上

  e^{U_H(t)} = max(|X(z)|, |Y(z)|)
  ≤ C_res·P(t)·E_{δ,R}(t)·D_H·R_H,   C_res := max(C_X, C_Y)、P := P_X + P_Y。   (W1-exit)

unary node は `e^{U_H} = |X(z)| ≤ C_X P_X E‖X‖ = C_X P_X E·D_H R_H` で同形(`D_H = 1`)。
さらに **singleton child `cΦ(A,B)`(`(A,B) ∈ K_{δ,R}`、`c ≠ 0`)は per-child strong bound を
`C = 1、P = 1` で満たす**:
`|cΦ(A,B)(z)| = |c|e^{Re(Az²/2+Bz)} ≤ |c|e^{|A|t²/2+|B|t} ≤ |c|E_{δ,R}(t)
≤ |c|·‖Φ(A,B)‖_ℱ·E_{δ,R}(t) = ‖cΦ‖_ℱ·E_{δ,R}(t)`
(`‖Φ(A,B)‖_ℱ ≥ |Φ(A,B)(0)| = 1` — 再生核評価 `|f(0)| ≤ ‖f‖e⁰`)。

*証明*: 各因子は非負(`C_X, C_Y > 0`、`P_X, P_Y ≥ 0`、`E > 0`、norm ≥ 0)なので
`max(C_XP_XE‖X‖, C_YP_YE‖Y‖) ≤ max(C_X,C_Y)·(P_X+P_Y)·E·max(‖X‖,‖Y‖)
= C_res·P·E·D_H R_H`(非負量の pointwise max ≤ 和で `P` は固定次数多項式のまま)。
singleton は上の 2 行。∎

pair child(`B₁₂` 型)の per-child strong bound は **W2 の義務であり本補題は主張しない**。
W1 は帰着と語彙のみを供給する。

**補題 W2(Pair norming、c=2 強形 — accepted、R-W2 PASS `a0fcd10`)**: 相異なる
`ξ_i = (A_i, B_i) ∈ K_{δ,R}`(`i = 1,2`)、`c₁c₂ ≠ 0`、`f = c₁Φ(ξ₁) + c₂Φ(ξ₂)` とする。
このとき全 `z = te^{iθ}`(`t ≥ 0`)で

  |f(z)| ≤ C₂(R)·(1+t)²·E_{δ,R}(t)·‖f‖_ℱ,                                  (W2-strong)
  C₂(R) := 1 + K_β(R),   K_β(R) := max{2(1+2R)(1+R), 2√2 + 2(1+R²)}。

定数は `(δ を通さず) R` のみに依存し、`m`、collision scale `s_m`、pair separation いずれにも
依存しない。従って pair child は per-child strong bound を `C = C₂(R)`、`P(t) = (1+t)²` で
満たし、W1 の premise が全 child type で閉じる。

*証明*: **(1) exact divided difference.** `ΔA := A₁−A₂`、`ΔB := B₁−B₂`、
`r := max(|ΔA|, |ΔB|) > 0`(`ξ₁ ≠ ξ₂`)、`ψ := (Φ(ξ₁) − Φ(ξ₂))/r`。線分 path
`(A_τ, B_τ) := (A₂+τΔA, B₂+τΔB)`(`τ ∈ [0,1]`)は `K_{δ,R}` の凸性より class 内に留まり、
`∂_τΦ(A_τ,B_τ)(z) = (ΔA·z²/2 + ΔB·z)·Φ(A_τ,B_τ)(z)` から

  ψ(z) = ∫₀¹ ((ΔA/r)·z²/2 + (ΔB/r)·z)·Φ(A_τ,B_τ)(z) dτ,
  |ψ(z)| ≤ (t²/2 + t)·E_{δ,R}(t).                                          (W2-point)

**(2) 正規化 0–2 jet.** 正規直交基底 `e_k = z^k/√k!` の係数を `f_k := ⟨f, e_k⟩`
(`|f_k| ≤ ‖f‖_ℱ`)とする。`Φ(A,B) = 1 + Bz + ((A+B²)/2)z² + …` より
`Φ₀ = 1`、`Φ₁ = B`、`Φ₂ = (A+B²)/√2`。`a := ΔA/r`、`b := ΔB/r`(`max(|a|,|b|) = 1`)で

  ψ₀ = 0,   ψ₁ = b,   ψ₂ = (a + (B₁+B₂)b)/√2。

**(3) 二分法(jet nondegeneracy).**
- `|b| ≥ [2(1+2R)]⁻¹` なら `|ψ₁| ≥ [2(1+2R)]⁻¹`。
- そうでなければ `|a| = 1` かつ `|B₁+B₂| ≤ 2R` より
  `|ψ₂| ≥ (1 − 2R·|b|)/√2 ≥ (1 − R/(1+2R))/√2 = (1+R)/((1+2R)√2) ≥ 1/(2√2)`。

**(4) 係数の norm 消去.** `f = αΦ(ξ₂) + βψ`、`α := c₁+c₂`、`β := c₁r`(展開して恒等)。
`f₀ = α` より `|α| ≤ ‖f‖`。
- 第 1 case: `f₁ = αB₂ + βψ₁` より
  `|β| ≤ (|f₁| + |α||B₂|)/|ψ₁| ≤ (1+R)·2(1+2R)·‖f‖`。
- 第 2 case: `f₂ = α(A₂+B₂²)/√2 + βψ₂` より(`|A₂| ≤ 1−δ ≤ 1`)
  `|β| ≤ 2√2·(‖f‖ + ‖f‖(1+R²)/√2) = (2√2 + 2(1+R²))·‖f‖`。

いずれでも `|β| ≤ K_β(R)‖f‖`。

**(5) 合成.** `|f(z)| ≤ |α|·|Φ(ξ₂)(z)| + |β|·|ψ(z)|
≤ ‖f‖E_{δ,R}(t) + K_β‖f‖·(t + t²/2)·E_{δ,R}(t)
≤ (1+K_β)·(1 + t + t²/2)·E_{δ,R}(t)·‖f‖ ≤ C₂(R)(1+t)²E_{δ,R}(t)‖f‖`
(`1+t+t²/2 ≤ (1+t)²`)。∎

`c_i = 0` または `ξ₁ = ξ₂` は exact zero-pruning/係数併合で rank ≤ 1 に落ち、W1 の
singleton case が覆う。raw 係数 `c₁, r, α, β` は proof-local であり、statement には
`‖f‖_ℱ` と `(δ,R)` 定数しか現れない(FR7 audit 語彙は不変)。**s_m 相殺の仕組み**:
A-dominant 方向では `r = |ΔA| ~ s²`、B-dominant 方向では `r = |ΔB| ~ s` だが、いずれも
分子(W2-point の `ΔA/r, ΔB/r ≤ 1`)と norming(jet 下界は `r` 正規化後の量)の双方で同じ
`r` が使われるため、`s` 依存因子は statement に残らない。非衝突域 `s ≈ 1` も同一の
jet bound がそのまま覆う。数値診断(非証拠): ランダム 4×10³ 配置(seed 11、`δ = 0.3`、
`R = 1.5`、near-cancellation `c₂ ≈ −c₁`・collision scale `s ∈ [10⁻³,1]` 含む、Gram 閉形式で
`‖f‖` を厳密計算、`t ≤ 10` × 9 方位)で違反なし、bound との最小余裕 ×96。

**補題 C0(Terminal two-anchor — accepted、R-C0 R2 PASS `f31cca0`)**: root node `H = X + Y`
(`X = B₁₂` pair block、`Y = c₃Φ(ξ₃)` singleton、`ξ₃ ∈ K_{δ,R}`、`c₃ ≠ 0`、zero-pruning 後
`R_H = ‖H‖_ℱ > 0`)、`G := e^{−U_T}H`、terminal 窓 `I_N ⊂ [0,2]`(§10.5.5 停止規約)、
`A := ‖H‖_ℱ`、`B := ‖Y‖_ℱ`、`M := max(‖X‖_ℱ, ‖Y‖_ℱ)` とする。このとき

  M·‖G‖_{∞,I_N} ≤ C_anc·A,   C_anc := max{6, (3/2)C_s},                    (C0-product)
  C_s := e²/c_Y,   c_Y := C_Φ⁻¹e^{−2(1−δ)−2R},   C_Φ := [δ(2−δ)]^{−1/4}e^{R²/(2δ)},

同値に `‖G‖_{∞,I_N} ≤ C_anc·D_H⁻¹`(Anchor-D 形)。定数は `(δ,R)` のみに依存。

*証明*: **(1) singleton floor.** atom norm 公式
`‖Φ(A,B)‖² = (1−|A|²)^{−1/2}exp[(|B|²+Re(AB̄²))/(1−|A|²)]` で、`a := |A| ≤ 1−δ` として
`1−a² ≥ δ(2−δ)`、分子 ≤ `|B|²(1+a) ≤ R²(1+a)` より norm の指数は
`≤ R²(1+a)/(2(1−a)(1+a)) = R²/(2(1−a)) ≤ R²/(2δ)`、よって `‖Φ(ξ₃)‖ ≤ C_Φ`。また `t ≤ 2` で
`Re q₃ ≥ −(1−δ)t²/2 − Rt ≥ −2(1−δ) − 2R` なので

  |Y(z)| = |c₃|e^{Re q₃} ≥ |c₃|·e^{−2(1−δ)−2R} ≥ c_Y·B   (全 t ≤ 2、zero-free)。

**(2) singleton-anchored bound.** `e^{U_T(z)} = max(|X(z)|,|Y(z)|) ≥ |Y(z)| ≥ c_Y B` と
再生核評価 `sup_{I_N}|H| ≤ e²A`(`t ≤ 2`)から `‖G‖_{∞,I_N} ≤ e²A/(c_Y B) = C_s·A/B`。

**(3) 二場合分け.** 常に `|G| = |X+Y|/max(|X|,|Y|) ≤ 2` と
`M ≤ A + B`(`‖X‖ = ‖H−Y‖ ≤ A+B`)が成り立つ。
- `A ≥ B/2` のとき: `M ≤ A + B ≤ 3A` なので `M‖G‖ ≤ 3A·2 = 6A`。
- `A < B/2` のとき: `M ≤ A + B < (3/2)B` なので
  `M‖G‖ ≤ (3/2)B·C_s·A/B = (3/2)C_s·A`。

いずれでも (C0-product)。`D_H = M/A` で割れば Anchor-D 形。∎

場合分けは Fock norm のみで判定され、W3 の `G`/`U_T`/record/定数を変更しない(chain との
干渉なし)。旧 design note の `D_H` 非有界 witness はこの補題により無害化される
((C0-product) が `D_H⁻¹` 相殺を供給し、`D_H ~ s⁻²` に対し `‖G‖ = O(s²)`)。
数値診断(非証拠・サンプル依存): 3 class 設定
(`(δ,R) ∈ {(0.3,1.5),(0.05,0.5),(0.5,3)}`)× 1500 配置(seed 23、near-cancellation・
collision・`B₁₂` 零点含む、Gram 閉形式)で違反なし。マージンはサンプル依存であり、
境界配置では floor 比 ~28(`(δ,R)=(0.05,0.5)`)、深い cancellation
`H = Φ(0,0)−2Φ(0,s)+Φ(0,2s)`(`s=10⁻³`、`D_H ≈ 7×10⁵`)で (C0-product) 余裕 ~1.9×10⁴
(luna R-C0 独立検算値)。`C_Φ` の指数は、粗い評価(分子 ≤ 2R²)では `R²/δ` までしか
出ないが、上記の `(1+a)` 相殺により `R²/(2δ)` が成立する(luna R-C0 [C0-01] の鋭化を採用)。

**補題 M1(weighted-root mode audit — accepted、R-M1 R2 PASS `fd18e9d`)**: 補題 S4b-COV(accepted
`c36d818`)の下で、任意の ray `(θ,T)` の `RayCoverageManifest_{θ,T}` について:

  (M1-1) 各 `k ∈ K_T` の root record `R_k` はちょうど一つで、route ∈ {`QR5-w`, `root-far`}、
         mode = weighted、unit step は `(S4-step-w)` 型;
  (M1-2) S4a が `RayCoverageManifest` の公開 `RootStep_k` を消費する **public ray ledger** は
         weighted root step(QR5 の uniform cost `C_T` + RF の graded cost)のみを加算する。
         child route(例: `K2-u`)は `RootStep_k` の内部 provenance として保持し、独立した
         step/ledger として再加算しない(accepted PΣ program は capability として非消費);
  (M1-3) `I_N` は `TerminalRecord` のみで、補題 C0 が消費する(RouteRecord と二重計上しない)。

*証明*: (M1-1) (COV-1)(COV-2) より各 `k ∈ K_T` にちょうど一つの root record が立つ。
(COV-0) より rank 3 の root node は常に root-2+1 形なので、その selector は §10.5.5 の
clause 1 であり、値は `QR5-w`(held)か `root-far`(far)。§10.5 RouteSpec 表より両 route とも
mode = weighted / `(S4-step-w)`、cost spec はそれぞれ `uniform(C_T)`、
`graded-root(C_RF,pair-difference-derivative)`。(M1-2) の非空性の根拠は (COV-2) による各公開 `R_k`
の存在と §10.4 の「S4a は root outputだけを一度ずつ消費する」契約であり、
unweighted/PΣ 項が public root ledger に現れないことは (M1-1) の mode 排他性から従う
(PΣ は capability として保持され、内部 provenance の存在を否定しない)。ledger 非混合の
規定「weighted recordは…unweighted ledgerへ混ぜない」(§10.4)はこの public ledger に
そのまま適用される。(M1-3) は §10.5.5 の `RayCoverageManifest` 定義
(`K_T := {1,…,N−1}`、`I_N` は `TerminalRecord` へ送り二重計上しない)から。∎

本補題は accepted 面(S4b-COV、RouteSpec、§10.4/§10.5.5 契約)の系であり、新しい解析的
主張を含まない。W3 は (M1-1)(M1-2) を、C0/W4 は (M1-3) を消費する。

**補題 W3(Weighted chain — accepted、R-W3 R2 PASS `4086ef9`)**: 補題 M1 の manifest の下、
`m ≥ m₀`(補題 RF の threshold、`m₀ := max(m_{FR-S1′/S1″}, m_RF)`)、`T ≥ 3`、
`G := e^{−U_T}H`。**定数正規化(WLOG)**: 以後 `C_T := max(1, C_T)` と正規化して消費する。
上界定数の拡大は QR5 の accepted 不等式を保存し、補題 RF の証明が inline 前提とする
`32C_T ≥ 1`(§10.5.3 帰納 step)もこれで満たされる(accepted body は不変)。このとき

  ‖G‖_{∞,I_1} ≤ exp((δ/8)T² + C_ch(T+1))·‖G‖_{∞,I_N},                       (W3-chain)
  C_ch := 10·log(1/ε_chain) + 2·log⁺C_T + 6·C_RF,

定数は `(δ, R, ε_chain, C_T, C_RF)` のみに依存(`m, θ, T` 非依存)。

*証明*: (M1-1) より各 `k ∈ K_T` の root record は `QR5-w` か `root-far` で、いずれも
`(S4-step-w)` 型・`κ_H = 0`・`γ_H = 5`:

  ‖G‖_{∞,I_k} ≤ C_step,k·ε_chain^{−5}·‖G‖_{∞,J_k} ≤ C_step,k·ε_chain^{−5}·‖G‖_{∞,I_{k+1}}

(`J_k = I_k ∩ I_{k+1} ⊆ I_{k+1}`、§10.3。envelope は全 k で同一の root `U_T` なので `G` は
ray 全体で一つの関数であり、record 間で weight の乗り換えは起きない)。`k = 1, …, N−1` を
内向きに反復して

  ‖G‖_{∞,I_1} ≤ (Π_{k∈K_T} C_step,k)·ε_chain^{−5(N−1)}·‖G‖_{∞,I_N}。

指数を三分して押さえる(`N−1 ≤ N ≤ 2T+1 ≤ 2(T+1)`):
- **ε 因子**: `5(N−1)log(1/ε_chain) ≤ 10(T+1)log(1/ε_chain)`;
- **QR5-w record**(held 窓): 各 `log C_step,k ≤ log⁺C_T`、合計 `≤ 2(T+1)log⁺C_T`;
- **root-far record**(far 窓): cost を RF の逐語形どおり
  `C_step,k := exp(C_RF(1+Λ_{η,k})) ≥ 1` と選ぶ(§10.5.3
  `‖e^{−U_T}H‖_{I_k} ≤ exp(C_RF(1+Λ_{η,k}))·ε_chain^{−5}·‖·‖_{J_k}`)ので各
  `log C_step,k = C_RF(1+Λ_{η,k}) ≥ 0` であり、far 部分和は RF-3(accepted、`m ≥ m₀` で
  `s_m ≤ s_RF`)の全窓 majorant で押さえられ
  `Σ ≤ (δ/8)T² + C_RF(2+4s_m)(T+1) ≤ (δ/8)T² + 6C_RF(T+1)`
  (§10.5.5 の index 契約: record 和は `k∈K_T`、majorant は k=1..N)。

合計で `(δ/8)T² + [10log(1/ε_chain) + 2log⁺C_T + 6C_RF](T+1)`。∎

**scope(非主張)**: 各 record の `(S4-step-w)` 不等式そのもの(QR5 kernel、補題 RF)と
domain witness の成立は accepted 面(§10.5.3、K2p1 §3.8.6、S4b-COV (COV-2))を引用して
消費するのみで、本補題は再証明しない。混在 ray(held 窓と far 窓が交互に現れる場合)も
同じ積算で覆われる(step は窓ごとに独立で、weight `U_T` は共通)。

**補題 W4(Terminal-cancelled exit — accepted、R-W4 R2 PASS `cb87eee`)**: 補題 M1 の manifest、
`m ≥ m₀`、`T ≥ 3`、root `H = X + Y`(`X = B₁₂`、`Y = c₃Φ(ξ₃)`)、`z₀ = Te^{iθ}` とする。

  |H(z₀)| ≤ 2C₂(R)·C_anc·R_H·(1+T)²·exp((1−3δ/4)T²/2 + (R+C_ch)(T+1)).      (W4-exit)

*証明*: §10.3 の pinned 規約より `a₁ = T−1`、`I₁ = [T−1, T]` なので `t = T` は `I₁` の右端点
として含まれ、`|H(z₀)| = e^{U_T(z₀)}·|G(z₀)| ≤ e^{U_T(z₀)}·‖G‖_{∞,I₁}`。三 accepted 補題を
順に掛ける:
- **exit(W1+W2)**: pair child `X` は W2 より per-child strong bound(`C = C₂(R)`、
  `P_X = (1+t)²` — premise `c₁c₂ ≠ 0` は root witness の `c₁c₂c₃≠0` から、`ξ₁ ≠ ξ₂` は
  accepted (COV-2) の global `REFIX` invariant(`η = q₂−q₁` nonconstant ⇔
  `(A₁,B₁) ≠ (A₂,B₂)`)から従う)、singleton child `Y` は W1 より
  `C = 1`、`P_Y = 1`。(W1-exit) で `C_res = C₂(R)`(`C₂ ≥ 1`)、
  `P(T) = (1+T)² + 1 ≤ 2(1+T)²`:

    e^{U_T(z₀)} ≤ 2C₂(R)(1+T)²·E_{δ,R}(T)·M,   M := max(‖X‖,‖Y‖) = D_H R_H;

- **chain(W3)**: `‖G‖_{∞,I₁} ≤ exp((δ/8)T² + C_ch(T+1))·‖G‖_{∞,I_N}`;
- **anchor(C0)**: `M·‖G‖_{∞,I_N} ≤ C_anc·R_H`。

合成して(`E_{δ,R}(T) = e^{(1−δ)T²/2+RT}`、`RT ≤ R(T+1)`、
`(1−δ)/2 + δ/8 = (1−3δ/4)/2`)

  |H(z₀)| ≤ 2C₂(1+T)²e^{(1−δ)T²/2+RT}·e^{(δ/8)T²+C_ch(T+1)}·(M‖G‖_{∞,I_N})
  ≤ 2C₂C_anc·R_H(1+T)²·e^{(1−3δ/4)T²/2+(R+C_ch)(T+1)}. ∎

定数 `2C₂(R)C_anc` と指数は `(δ, R, ε_chain, C_T, C_RF)` のみに依存(`m, ℓ, θ, T` 非依存)。
二次係数 `(1−3δ/4)/2` は (E-w) target `(1−δ/2)/2` より `δ/8` だけ強い。

**補題 EW-B(original-collision bridge — accepted、R-EW R2 PASS `b39216f`)**: **表記**: §2 の入力列
`ξ_{j,m}`(constant-gauge quotient 後・metaplectic gauge **前**)の parameters を
`(A^orig_{j,m}, B^orig_{j,m})` と書く(§2 の `ξ_{j,m} → ξ*` はこの original 座標での収束)。
original 座標で

  s̃_m := max_{i,j} max(|A^orig_{i,m}−A^orig_{j,m}|^{1/2}, |B^orig_{i,m}−B^orig_{j,m}|)

と定める(§2 の `d_w` と同形、ただし **gauge 前の parameters** に対して)。§2 の入力仮定
(単一 `d_Ω`-衝突 cluster、`ξ_{j,m} → ξ*` 全 j)より `s̃_m → 0` であり、**定義から直ちに**
全 pair で `|ΔA^orig| ≤ s̃_m²`、`|ΔB^orig| ≤ s̃_m`。従って original radial exponent
`q_j(t) = A^orig_j e^{2iθ}t²/2 + B^orig_j e^{iθ}t` の pair 差について
`Λ_{η,k} ≤ s̃_m²(a_k+1) + s̃_m` となり、RF-3 の graded ledger は同一定数のまま `s̃_m` で
再インスタンス化される。EW が route する **ungauged exact tree** の S4b-β domain witness
には当該 node の original parameters を供給する(gauged parameters は FR-S1′/S1″ の
frame construction 専用で、EW manifest へ流用しない — gauged `d_w` の不変性は vacuum
stabilizer に限られ full metaplectic covariance はないため)。具体的には、本適用では
`D-ROOT-FAR` の collision-scale witness slot に `s_m^{EW} := s̃_m` を代入し、
`RouteRecord` の `node_functions`/`q_j`/`η`/`Λ_{η,k}` も original 表現で再インスタンス化する
(accepted COV-2 body は不変 — consumer-side 供給であり再受理不要、content-SHA 規律に整合)。
threshold は
`m̃_RF := min{M: ∀m≥M, s̃_m ≤ s_RF}`、`m₀ := max(m_{FR-S1′/S1″}, m̃_RF)` と読み替える。
`s̃_m` は input atoms のみで決まり `θ, ℓ, T` 非依存(uniformity)。
*証明*: 全て定義と §2 の入力仮定から。∎

(設計記録: gauged 経由の転送(metaplectic 包絡合成)は採らない — squeeze の Bargmann 表示は
weighted composition でなく、unitarity は norm を保存するが pointwise growth を保存しない。
Sol consultation 第 5 回の裁定 A′。)

**補題 EW(c=3 weak envelope (S4-Ew) — accepted、R-EW R2 PASS `b39216f`)**: `m ≥ m₀`(EW-B の
読み替え後)、`F := U_m^{-1}v_{ℓ,m}`(`‖F‖_ℱ = 1`、unitarity)。`U_m^{-1}` は gauged atom を
original atom の非零 scalar 倍へ戻す(§3: exact span・norm・Gram 保存)ので、`F` は
original parameters(`∈ K_{δ,R}`)の ≤3-atom exact 結合であり、canonical tree(COV-0)を持つ。
`L := R + C_ch`、

  C_w := 2C₂(R)·C_anc·e^L,   C_lin := L + 2 = R + C_ch + 2

とすると、全 `m ≥ m₀`、全 `ℓ`、全 `z ∈ ℂ` で

  |(U_m^{-1}v_{ℓ,m})(z)| ≤ C_w·exp((1−δ/2)|z|²/2 + C_lin|z|).            (S4-Ew)

*証明*: `T := |z|`。effective rank(exact `REFIX`/zero-pruning 後)で場合分け:
- **rank 3、T ≥ 3**: 補題 W4 を original tree に適用(witness は EW-B が供給)し
  `R_H = ‖H‖` で正規化:
  `|F(z)| ≤ 2C₂C_anc(1+T)²e^{(1−3δ/4)T²/2+L(T+1)}
  ≤ 2C₂C_anc·e^L·e^{(1−δ/2)T²/2+(L+2)T}`
  (`(1+T)² ≤ e^{2T}`、`(1−3δ/4) ≤ (1−δ/2)`)。
- **rank 2、T ≥ 3**: 補題 W2(premise は REFIX 後の distinct atoms・非零係数):
  `|F(z)| ≤ C₂(1+T)²e^{(1−δ)T²/2+RT} ≤ C₂e^{(1−δ/2)T²/2+(R+2)T}`。
  **rank 1**: W1 singleton case(`C=1、P=1`)で同形。いずれも `C_w ≥ C₂ ≥ 1` に収まる。
- **T < 3(全 rank)**: 再生核評価 `|F(z)| ≤ ‖F‖e^{T²/2} = e^{(1−δ/2)T²/2}·e^{δT²/4}` と
  `δT²/4 ≤ (3δ/4)T`(`T ≤ 3`)、`3δ/4 ≤ 2 ≤ C_lin`。∎

定数 `C_w, C_lin` は `(δ, R, ε_chain, C_T, C_RF)` のみに依存し、`m, ℓ, θ, z` と
SVD/Newton 係数に依存しない((E-w) の「定数非依存」要求は `C_w, C_lin` に対するもの。
`m₀` 自体は入力列の収束速度に依存してよい — (E-w) は `m₀` の存在のみ要求)。**これで
§10.2 の c=3 target (E-w) が S4a program として閉じる。** S4c(N3′/N4 同期、FR7 no-return audit、
original/gauged 記号の provenance 同期)は別 obligation として残る。

**program 表**(state は fail-closed: 受理は fixed-SHA 査読後のみ。依存順は
C0 → M1 → W3 → W4 → EW に改訂 — Sol consultation 第 4 回、M1 の weighted-only 監査を
W3 が消費するため):

| packet | statement / output | state |
|---|---|---|
| W1 Child-reserve interface | 語彙 + (W1-exit) + singleton case | **accepted**(R-W1 R2 PASS、fixed SHA `a59768e`) |
| W2 Pair norming | exact divided difference + 0–2 jet norming で `|f(z)| ≤ C₂(R)(1+t)²E_{δ,R}(t)‖f‖_ℱ`(c=2 強形、`η_sep`/`s_m` 非依存) | **accepted**(R-W2 PASS、fixed SHA `a0fcd10`) |
| C0 Terminal two-anchor | (C0-product) `M‖G‖_{∞,I_N} ≤ C_anc·R_H` ⇔ Anchor-D | **accepted**(R-C0 R2 PASS、fixed SHA `f31cca0`) |
| M1 mode audit | RayCoverageManifest 監査: `k∈K_T` の root record は weighted-only(`QR5-w`/`root-far`)、weighted/PΣ ledger 非加算、`I_N` は TerminalRecord のみ | **accepted**(R-M1 R2 PASS、fixed SHA `fd18e9d`) |
| W3 Weighted chain | `G=e^{−U_T}H` を `k∈K_T` の root record で一度ずつ積算、`‖G‖_{∞,I_1} ≤ e^{δT²/8+C_ch(T+1)}‖G‖_{∞,I_N}`(`m ≥ m₀`、M1/COV 消費) | **accepted**(R-W3 R2 PASS、fixed SHA `4086ef9`) |
| W4 Terminal-cancelled exit | W1/W2 × W3 × (C0-product) の合成で `|H(Te^{iθ})| ≤ 2C₂C_anc·R_H(1+T)²e^{(1−3δ/4)T²/2+(R+C_ch)(T+1)}` | **accepted**(R-W4 R2 PASS、fixed SHA `cb87eee`) |
| EW-B original-collision bridge | `s̃_m`(original 座標)の定義と witness 供給、`m₀` 読み替え、A′ 裁定の記録 | **accepted**(R-EW R2 PASS、fixed SHA `b39216f`) |
| EW final | rank 1/2/3 × `T≥3`/`T<3` の場合分けで (S4-Ew)、`C_w = 2C₂C_anc e^L`、`C_lin = R+C_ch+2` | **accepted**(R-EW R2 PASS、fixed SHA `b39216f`)。**S4a program 完結** |

**U1 の退役(design 決定)**: 現 c=3 の public root record は weighted(`QR5-w`/`root-far`)
のみ(補題 S4b-COV の帰結)なので、unweighted assembly U1 は本証明列の critical path から
外す。accepted PΣ program は capability として保持する(削除しない)。将来 S4-0 改訂で
unweighted root route が到達可能化された場合は U1 を復帰させ、COV-0 再証明と同時に扱う。

**D_H 非有界の witness(design note — 証明ではない)**: path `Φ_s := Φ(0,s) = e^{sz}`
(`s → 0⁺`)で `H_s = Φ₀ − 2Φ_s + Φ_{2s}`(二階差分)を `X_s = Φ₀ − 2Φ_s`、
`Y_s = Φ_{2s}` と分けると、smooth Fock-valued path の二階差分として `‖H_s‖ = O(s²)` が
期待され(非零二階微分 `‖∂_s²Φ(0,s)|_{s=0}‖ = ‖z²‖ > 0` から同 order の下界も期待)、
`‖X_s‖, ‖Y_s‖ → 1` なので `D_{H_s}` は `s⁻²` order で発散すると見込まれる。厳密化は C0
packet の義務とし、ここでは「(W1-exit) 単独では m 一様 exit にならず、C0 の `D_H⁻¹`
reserve との相殺(W4)が必須」という設計判断の根拠としてのみ記録する。

### 10.9 S4c closure(N3′/N4 ledger・FR7 no-return audit・c=3 FR acceptance — proof draft、R-S4C 待ち)

本節を S4c の唯一の authoring location とする。S4c は新しい解析を含まず、(i) N3′/N4 の
c=3/(E-w) 同期帳簿、(ii) FR7 no-return audit、(iii) original/gauged provenance 同期と
c=3 FR acceptance 判定、の三つの監査・同期のみからなる。

**(i) N3′/N4 ledger**: 閉包文書 §4.3 の (N3′)(N4) は一般 `(E-d_ℓ)` 表記だったため、
c=3 具体化注記(v1.8.13)を同 §4.3 に追加した: (N3′) の envelope 要求は c=3 では
(E-w) = (S4-Ew) で読み、(N4) の定数依存は `C_w, C_lin` の
`(δ, R, ε_chain, C_T, C_RF)`-only 依存として実現される(補題 EW、R-EW R2 PASS `b39216f`)。
(E-d_ℓ) は一般 c の open 義務として不変。FR6 行(§4 表)と閉包文書の注記は **split の
境界(c=3/(E-w) vs 一般 c/(E-d))が一致**し、依存定数の列挙は注記側が FR6 行の抽象形を
具体化する(逐語同文ではない)。凍結 snapshot §4.3.4 には触れていない(N3′/N4 は
§4.3 本体 = 非凍結)。

**(ii) FR7 no-return audit(実施記録)**: §10.4 の許可語彙
`{RootStep provenance fields, node functions, U_H, compact-class envelope, Fock norm,
named constants}` に対し、禁止入力 5 種(旧 flat parent `U_F`、旧 DC discount、
raw 原子係数、SVD coefficient、`1/t_m`)の**合成式入力としての**出現を、最終面 =
{§10.8 全 8 補題の statement/proof、§10.5 RouteSpec 全 6 row、§10.5.2–10.5.5 の
accepted 本体}について機械走査 + 逐語確認した。結果:

| 禁止入力 | 出現 | 判定 |
|---|---|---|
| 旧 flat parent `U_F` | §10.8 = 0 件、RouteSpec = 0 件。§10.5.5 (COV-0) に 1 件 — non-producer **排除宣言**の引用のみ | 非混入 |
| 旧 DC discount | 全最終面 0 件 | 非混入 |
| raw 原子係数 | statement には 0 件。W2/C0/EW の proof 内は **proof-local 導入 + 即時 norm 消去**(§10.4 の「係数は node functions と `U_H` を通じてのみ」に適合)。§10.5.3(補題 RF)にも「raw 係数…に依存しない」の排除宣言あり | 非混入 |
| SVD coefficient | §10.8 に 1 件 + §10.5.3 に排除宣言 — いずれも「依存**しない**」の非依存宣言のみ | 非混入 |
| `1/t_m` | 全最終面 0 件 | 非混入 |

(出現記録は §10.8・RouteSpec・§10.5.2–10.5.5 accepted 本体の全最終面を対象とし、
排除文脈/非依存宣言/proof-local 導入は違反に数えない。)

排除文脈での言及(禁止対象を禁止と述べる文)は audit 違反に数えない。fail-closed tests が
§10.8/RouteSpec の禁止 token 不在を固定する。

**(iii) original/gauged provenance 同期と c=3 FR acceptance**:

| witness | 座標系 | 消費者 |
|---|---|---|
| `s_m`(§2 `d_w`、gauged) | metaplectic gauge 後 | FR-S1′/S1″ frame construction のみ |
| `s̃_m`(補題 EW-B、original) | gauge 前(constant-gauge quotient 後) | EW manifest の `D-ROOT-FAR` slot(`s_m^{EW} := s̃_m`)、RF-3 再インスタンス化、`m̃_RF`/`m₀` |

FR ledger の充足根拠(§4 表の各行、fixed SHA):
FR1/FR2/FR4/FR3(X)(L-d) = R-A″ PASS `61111cc`(+ 補題 W = R-W PASS `1b3e337`);
FR5 = S4b closed(全 6 route、QR5 `27a1817`、RF fixed SHA `9f19389`(minors `c271919`)、COV `c36d818`);
FR6 = (E-w) core = S4a closed(補題 EW `b39216f`)+ N3′/N4 同期(本節 (i));
FR7 = 本節 (ii) の audit。
従って **c=3 FR は本 program 内で全行充足**(§4「FR1–FR7 が揃って初めて c=3 の補題 N 枠
として受理する」の条件成立)。表現は保守的に保つ: これは「証明ドラフト・複数 LLM 検算済み・
独立再査読(R-S4C)待ち」の program 内 acceptance であり、閉包文書側の消費(補題 N 本体の
量化完備化、一般 c、系 C1)は閉包文書の義務として残る。

| ID | scope | state |
|---|---|---|
| S4c-i N3′/N4 ledger | 閉包文書 §4.3 v1.8.13 注記 + FR6 との split 境界一致(依存集合は注記側が具体化) | proof draft(R-S4C 待ち) |
| S4c-ii FR7 audit | 禁止入力 5 種 × 最終面の非混入表 + fail-closed tests | proof draft(R-S4C 待ち) |
| S4c-iii FR acceptance | provenance 同期表 + FR1–FR7 充足根拠 | proof draft(R-S4C 待ち) |

## 11. 版履歴

- v0.1(2026-08-10): DC-NG 後の replacement target を single-F wrapper から exact block-frame 問題へ移し、
  FR1–FR7 と最小証明順を定義。証明 claim は置かない。
- v0.2(2026-08-10): R-FRSPEC R1 の S1/S3 を受諾して修正。constant-gauge exact 併合・零和削除後に
  rank/tree を再固定。FR3 に共通基点、per-element order o′≤2、(E-o′)/(X)/(L-o′)、r≤3 を明記し、
  FR6 の N4 許容依存を固定。査読が要求した `Σ(o′+1)≤3` は既存 N1 自体が c=2 Newton 枠に反するため
  採用せず、closure v1.8.11 で N1 を per-element order + cardinality 帳簿へ訂正。
- v0.2.1(2026-08-10): 固定 SHA `4b071c0` の R-FRSPEC R2 **PASS**。非blocking注を反映し、
  post-quotient leaf weight w を定義して FR3 を `o′≤w−1`, `r≤w≤3` と一般 N1 に直結。
- v0.3(2026-08-10): 本線の仕様自己監査で、FR3 の共通基点を保証する入力条件が暗黙だったと判定。
  補題 N の一つの衝突cluster `s_m→0`, `ξ_{j,m}→ξ*` を明示し、非衝突clusterはL3側へ分離。
  R2通過部分は維持するが、入力domain変更を R-FRSPEC R3 で再確認するまで specification review pending。
- v0.4(2026-08-10): R-FRSPEC R3 の H1 を受諾。outer cluster内のzero-ratio pairをproper childへ再帰し、
  c=3でdepth≤2の各active nodeをsingle-scale化。加えて single-scale curvilinear族でも素朴な length-3 evaluation が
  rank dropする Flex witness F3を追加。FR-S1はrate flagに加えてevaluation-rank flagも必要。
- v0.4.1(2026-08-10): 固定 SHA `26106ac` の R-FRSPEC R4 **PASS**。nested tree、F3 の級数と
  Fock norm cubic limit、scheme-route 反証の限定scopeを再検算。非blocking注を反映し、距離正規化を
  w≥2 の active node に限定、w=1 leafを再帰終端と明記。
- v0.5(2026-08-11): Fable consultation response の F3′ を本線で独立検算し受諾。旧 FR3 の
  `deg P≤2o′≤4` を撤回し、F3′ を反例 registry として追加。plain c=3 の補題 W、真空 gauge 後の
  (2,1)-weighted 距離 + J⁵-SVD による FR-S1′、nested 2+1、FR-S4 を別義務へ分離。
- v0.5.1(2026-08-11): plain c=3 の補題 W を独立 authoring location に proof draft として追加。
  本仕様では固定 SHA review pending の入力として参照し、nested 2+1 や FR-S4 の閉鎖には数えない。
- v0.5.2(2026-08-11): 補題 W の R-W1–R-W5 が固定 SHA `1b3e337` で全 PASS。
  nonblocking minor 2 件を補題文書へ反映。plain c=3 の valuation 上界 5 だけを accepted に昇格し、
  nested 2+1・weighted tail・FR-S4 は open のまま維持。
- v0.6(2026-08-11): coarse cluster 分離の `d_Ω` と、真空 gauge 後の局所 weighted metric
  `d_w=max(|ΔA|^{1/2},|ΔB|)` を分離。plain single-scale triple について、J⁵-SVD、補題 W の
  singular-value floor、Fock tail `O(s⁶)`、norm limit/Gram/exact span を FR-S1′ proof draft として追加。
  nested 2+1 と FR-S4 は non-claim のまま。
- v0.6.1(2026-08-11): 固定 SHA `ed25401` の R-A1–R-A6 が全 PASS(blockingなし)。
  nonblocking minor 2 件(適用集合 `Θ_η`、gauge逆元のstrong収束式)を反映。plain single-scale triple の
  FR1/FR2/FR4/FR3(X)(L-d) を accepted に昇格し、次 blocker を nested 2+1 接続へ移した。
- v0.6.2(2026-08-11): Fable consultation #2 の GO を受け、static generalized W′ を補題W文書に
  proof draftとして追加。finite-m nested 2+1 はW′の固定SHA判定後にFR-S1″として書く。
- v0.6.3(2026-08-11): 固定 SHA `57ff88d` の Fable response `5250516558` で
  R-W′1–R-W′5 が全 PASS。static generalized W′ を
  accepted に昇格し、次の未解決点を finite-m ν-chart / FR-S1″ に限定した。
- v0.7(2026-08-11): Fable consultation #2 response `5249981331` に基づき、finite-m nested 2+1 の
  FR-S1″ proof draft を追加。child anchor + s-free
  normalized Newton difference、`ν=(δB̄,δĀ/2)` の continuous compactification、root-scale exact
  factorization、W/W′を用いるhead floor、difference-column tail、exact pair+singleton treeを記載。
  consultation #2 の設計を実装したため、固定 SHA の R-A″ は別モデルによる独立検算を要求する。
- v0.7.1(2026-08-11): 固定 SHA `61111cc` を Luna/xhigh が独立査読し、R-A″1–R-A″6 は
  findingなしで全 PASS (`5252797923`)。FR-S1″を accepted に昇格し、次 blocker を
  `(E-d)` / FR5–FR7 (FR-S4)へ移した。
- v0.8(2026-08-11): Fable consultation #3 の REVISEを受け、FR-S4を
  S4-0→S4b→S4a→S4cへ再分割。c=3 target (E-w)、C′ unit chain、per-node segmentation、
  U_H-ledger、coefficient-free kernel/constant契約をS4-0 specification draftとして追加。
  consultationの交差数根拠はpair nodeにだけ採用し、root pair-block segmentationはS4b obligationへ戻した。
  accepted C′との照合で `A=sup_IU_H−sup_JU_H` を採用し、S4b出力をcell内部を畳み込んだ
  composite unit-step kernelに固定した。
- v0.8.1(2026-08-11): 固定 SHA `b0b9927` の R-S4-0 R1 を受諾。QR5/K2Q-wt の weighted outputを
  unweighted S4-stepへ直結していた型不一致を修正し、mode別の composite root-stepへ分離した。
  root far/unheld intervalを明示的なS4b obligationとし、generalized K2Qのdomain/fallback、root-only積算、
  typed provenanceを追加。K2 statusのauthoring/reference不一致はS4b前の依存監査として残した。
- v0.8.2(2026-08-11): 固定 SHA `2addf4d` の R-S4-0 R2 は T2/T3 PASS、T1/T4/T5 BLOCKED。
  findingsを受諾し、共通 overlap `ε_chain`、空 modeのmax規約、Gaussian phase由来の `Λ` bound witness、
  fixed-SHA source refを持つ discriminated schema、zero-child pruning、generalized singleton routeを追加。
- v0.8.3(2026-08-11): 固定 SHA `1ee86c5` の R-S4-0 R3 は T3/T6 PASS、T1/T2/T4/T5 BLOCKED。
  interval recordから `ε_chain` を逆算する循環を受諾し、S4bを interval-independent `RouteKind` registry
  closureと interval-dependent `RouteRecord` instantiationへ分離。resolved/unresolved、unary/binary、
  external/intrinsic sourceをdiscriminated union化した。generalized singletonの `log|P|` lossを
  phase `Λ` へ誤吸収せず、`polynomial-envelope` assembly obligationとしてS4aへ明示的に残した。
- v0.8.4(2026-08-11): 固定 SHA `54f1eca` の R-S4-0 R4 は T1–T4/T6 PASS、T5 BLOCKED。
  finite `C̄/γ/κ̄` constraints、closed-world `CategoryEnum` と coverage manifest、typed domain/missing-obligation
  enumを追加。C′自体のstatusをkernel routeから独立した `Cprime_ref` で監査し、未受理ならS4aを停止する。
- v0.8.5(2026-08-11): 固定 SHA `7db8dff` の R-S4-0 R5 は T1–T4/T6 PASS、T5 BLOCKED。
  resolved/unresolved tupleへDomain/A-ledger/Missing enum membershipを直接付与。`Cprime_ref`を
  literal PASS tupleからvalidated external `source_ref`の特殊化へ変更し、authoring-status照合を必須化した。
- v0.8.6(2026-08-11): 固定 SHA `6fa5cf3` の R-S4-0 R6 は T1–T4/T6 PASS、T5 BLOCKED。
  route IDと合法だが別route用のfieldを混ぜられる反例を受諾し、§10.5のclosed-world `RouteSpec` 行との
  full-discriminant一致を必須化。polynomial-envelopeはbare acceptedを禁止し、fixed-SHA PASSの
  `assembly_proof_ref`がある場合だけopenからacceptedへ移せる型にした。
- v0.8.7(2026-08-11): 固定 SHA `74947eb` の R-S4-0 R7 は T1–T4/T6 PASS、T5 BLOCKED。
  `D-K2Q-WT` keyを完全列挙し、split witnessをvalidated fixed-SHA ref化。各 RouteSpec source ruleへ
  canonical file/anchor/SHA/statusをliteral記載し、未受理sourceはUNRESOLVEDのまま固定。excluded proofは
  category IDと到達不能statementへ型結合し、現行 `ExclusionWitnessEnum=∅` により迂回を禁止した。
- v0.8.8(2026-08-11): 固定 SHA `f7d6d2c` の R-S4-0 R8 は T1–T4/T6 PASS、T5 BLOCKED。
  intrinsic source unionとRouteSpec source ruleの3要素/4要素不一致を受諾。externalと同型の
  `(name,canonical file,anchor,fixed SHA,status)` 5要素へ統一し、現在はUNRESOLVED/unresolved、
  S4-0固定SHA受理後だけconcrete SHA/PASSへ遷移する規則にした。
- v0.8.9(2026-08-11): 固定 SHA `56498bb` の R-S4-0 R9 は T1–T6 **PASS**。
  S4-0 interfaceだけをacceptedへ昇格し、同SHAをintrinsic source refへ記入。K2/C′/K2Q、root-far、
  split(ii)/(iii)、polynomial ΣA、S4b/a/c、(E-w)、FR-S4全体は未受理/openのまま維持した。
- v0.8.10(2026-08-12): 固定 SHA `965fd3a` の R-K2-STATUS R4 が canonical K2/C′/L2a′ statusをPASS。
  `K2-u` と `Cprime_ref`を同SHA/PASSへ接続。K2Q、root-far、split(ii)/(iii)、polynomial ΣA、
  S4b/a/c、(E-w)、FR-S4全体はopenのまま。
- v0.8.11(2026-08-12): standalone K2Q statusとsplit(i) witness statusの混同を防ぐため、
  `M-SPLIT-I-WITNESS`をclosed-world obligation enumへ追加。validated `split_i_witness_ref`だけで
  解消する規則を定め、`K2Q-wt-w`を`M-K2Q-STATUS + M-SPLIT-I-WITNESS`でfail-closedにした。
  K2Q source rule自体はUNRESOLVEDのまま。
- v0.8.12(2026-08-12): 固定 SHA `bffc3ea` のcanonical K2Q source refと接続gateを根拠に、
  `K2Q-aff-u` / `K2Q-wt-w` のsource refを同SHA/PASSへ接続し、`M-K2Q-STATUS`を除去。
  前者のpolynomial ΣA proof、後者の`M-SPLIT-I-WITNESS`、S4b/a/c、(E-w)、FR-S4全体はopenのまま。
- v0.8.13(2026-08-13): R-SPLIT-Iの型不一致findingを受諾。旧§3.6.2をwitnessへ直結せず、
  exact root `U_T` unit-stepを対象とするS4b split-row audit SI-1–SI-8をproof draftとして追加。
  regular/pair-dip cell、係数非依存cell数、composite root-only ledger、反例時のQR5-w再分類を
  acceptance条件に固定。`M-SPLIT-I-WITNESS`、S4b/a/c、(E-w)、FR-S4全体はopenのまま。
- v0.8.14(2026-08-13): R-SPLITSPEC R1のtyped gap三件を受諾。`D-K2Q-WT`にη/μ、singleton係数、
  held/recenterのcanonical mappingを追加。`SplitCellData`の許容依存・幅・overlap・multiplicityと
  exponent-4 composition refを固定し、`C_split≤C̄_route`をfixed-SHA `constant_provenance_ref`へ結合。
  witness anchorを旧§3.6.2から本節へ移した。証明と`M-SPLIT-I-WITNESS`はopenのまま。
- v0.8.15(2026-08-14): feasibility/counterexample auditで canonical 五次共鳴をformer typed domainへ
  代入し、exact `U_T` exponent-4 root stepが偽と判定。category、domain、obligation、cell/constant
  proof draftを退役し、held rootをreviewed `QR5-w`へ一本化。旧§3.6.2の`U_F`転送とK2Q-wt自体は不変。
- v0.8.16(2026-08-16): reachability auditで、split(ii)/(iii) は旧 flat `U_F` 三者択一のchart-only
  certificateであり、exact node-local `RouteKind`ではないと判定。両route IDとmissing-kernel obligationを
  registryから退役した。非定数pairが遠方でheld条件を外れる明示族により `root-far` は到達可能なので、
  `M-ROOT-FAR-KERNEL`を唯一のunresolved exact-root routing categoryとして維持した。
- v0.8.17(2026-08-16): R-REACH-CLEANUP R1のsurface findingsを受諾。§7 の current blockerを
  accepted済みS4-0からS4b `root-far`へ同期し、F3 witnessを解決済み設計制約として明示した。
  claim-surface testは `root-far` の文字列存在でなく、CategoryEnum・MissingObligationEnum・
  RouteSpec rowの三面結合を検査するよう強化した。
- v0.9(2026-08-17): Fable consultation #4のGOを本線で条件付き受諾。raw held keyを暗黙に
  recentered読みせず、exact `RECENTER(C,t_c)`、`D-ROOT-FAR`、`graded-root` cost、cell/全ray ledgerを
  RF-1–RF-4のspecification draftとして追加した。一様fixed `N_cell` は遠方chirpで不可能なため、
  `N_cell,k≤4+8Λ_{η,k}` と `ΣΛ_{η,k}` のquadratic-budget吸収へ改訂。root-far routeは
  R-RFSPECとRF proofのfixed-SHA acceptanceまでunresolvedのまま維持する。
- v0.9.1(2026-08-17): 固定 SHA `25afe6e` の R-RFSPEC R3でS1–S7が全PASS。RECENTER、cell geometry、
  `C_RF`、ray-wide budget、template/record分離、fail-closed schemaをspecificationとして受理した。
  RF proofは未執筆なので、active `root-far` rowとS4b/a/cはunresolved/openのまま維持する。
- v0.9.2(2026-08-17): 補題 RF の proof draft を §10.5.3 に執筆(担当交代後の本線 = Fable)。
  RF-1 = exact RECENTER 恒等式と QR5 raw 仮定の cell 上検証、RF-2 = cell cover 幾何
  (`N_k ≤ 4+8Λ_{η,k}`)+ seed/anchor cell 込みの QR5-w 連鎖帳簿、RF-3 = graded ledger の
  (E-w) budget 吸収(`s_RF` 閾値、`(δ/8)T²+O(T)`)。real/oscillatory witness の acceptance
  fixture(B₁₂ 零点跨ぎ・recentered held・天井)を局所検証として記録。R-RF fixed-SHA review
  まで root-far row と `M-ROOT-FAR-KERNEL` は unresolved のまま。
- v0.9.3(2026-08-17): luna R-RF R1(受理不可)を全件受諾して修正。[blocking RF-B1] 再中心化は
  q₂ の定数シフトなので `q₂−q₃ ≡ const` 入力で `q₂^C = q₃` となり QR5 相異性が破れる
  (反例 `q=(t²,2t²,2t²−1/256)`)— §2 constant-gauge quotient 済みの domain witness
  (`q₁−q₃`/`q₂−q₃` nonconstant)を `D-ROOT-FAR` の必須 key に追加し、補題 RF が明示消費する形へ
  修正(schema binding test も同時改訂)。[minor RF-M1] fixture 数値を精密化(§10.5.3 (5) 参照 —
  数値の authoring location はそちらに一本化)。[minor RF-M2] 適用閾値
  `m₀ = max(m_{FR-S1′/S1″}, m_RF)` を明示。R-RF R2 待ち。
- v0.9.4(2026-08-17): luna R-RF R2 = **受理可**(blocking/major なし)。minor 3 件を反映:
  [RF-M2-N1] `m_RF` の束縛変数名衝突を解消(`min{M ∈ ℕ: …}`)。[RF-TEST-1] binding test に
  negative path(witness 1 個欠落の synthetic row が equality guard で落ちること)を追加。
  [SURF-1] 版履歴の sampled 数値再記載を §10.5.3 への参照に一本化。
- v0.10(2026-08-17): 補題 RF の受理(R-RF R2 PASS)に伴う registry 昇格。`root-far` row を
  §10.5.2 の意図 discriminant どおり resolved に(source = QR5 `27a1817` + RF INTERNAL `c271919`、
  domain = `D-ROOT-FAR` 全 7 key、`(graded-root(C_RF,pair-difference-derivative),5,0)`、
  weighted-no-A)。`M-ROOT-FAR-KERNEL` 解消、§7/§10.5.2/§10.5.3/§10.7 の状態 surface を同期、
  fail-closed tests を promoted 状態の binding へ書換え(root-far row の完全一致 bind、
  RF row accepted 状態、unresolved token の撤去)。本昇格自体の独立監査 = R-RF-PROMOTE。
- v0.10.1(2026-08-17): luna R-RF-PROMOTE R1 = BLOCKED を全件受諾して修正。[blocking] source_ref
  契約を「fixed_SHA = 査読対象 content の SHA、PASS の効力 = canonical status ledger の acceptance
  記録」と明文化(QR5 `27a1817` の時点表示と受理記録の関係を規約化、intrinsic は §10.7 acceptance
  行を効力根拠に)。[major] stale surface 5 箇所(§10.3 uniform 記述・§10.5.1 末尾・§10.5.2 見出し・
  §10.6 pending 表記・header)を promoted 状態へ同期。[major] tests を強化: 意図 discriminant の
  逐語 bind、stale token 不在、cross-file provenance(K2p1 の QR5 受理記録)、全 6 category row の
  一意性。[minor] M-K2-STATUS の enum 残存に根拠注記。§10.7 に S4-0.RF-PROMOTE 行を新設し
  R2 pending を唯一の pending marker とした。
- v0.10.2(2026-08-17): luna R-RF-PROMOTE R2(受理不可)を全件受諾。[blocking] K2-u/C′ の source
  SHA を canonical K2 ledger の受理 SHA `eb1804a` へ、K2Q-aff-u を canonical K2Q ledger の
  reviewed SHA `96671e6` へ訂正(改訂契約下で全 external ref が canonical ledger と整合)。
  [major] 残存 stale 語彙(`RF candidate`・`RF-CandidateSpec`→`RF-Spec`・graded-root候補・
  候補定数)を accepted 語彙へ置換。[major] tests に全 external source_ref の canonical ledger
  照合(short-prefix 規則込み)・stale token 追補・pending marker 件数 = 1 を追加。R3 再監査待ち。
- v0.10.3(2026-08-17): luna R-RF-PROMOTE R3(tests 残 2 major)を受諾。source_ref の
  **行別 positional binding**(K2-u/K2Q-aff-u/generalized-singleton-u/QR5-w/root-far/trivial-u の
  各 row line 内に kernel/file/anchor/full-SHA tuple を逐語 bind、CprimeSourceRule block も同様)と、
  stale token 追補(`graded-root候補`・`候補定数`)を tests に実装。文書本体は R3 で PASS 済みのため不変。
- v0.10.4(2026-08-17): R-RF-PROMOTE R4 = 条件付き受理(R3 修正の tests 検証 PASS)。luna 指定の
  記載で §10.7 S4-0.RF-PROMOTE 行を PASS(fixed SHA `9cca48d`)へ更新し、pending marker を全廃、
  tests を acceptance 状態へ同期。**root-far 昇格 arc 完結** — S4 route 表は全 6 row resolved。
- v0.11(2026-08-17): Sol high consultation(polynomial ΣA + S4a 設計)を受け、PΣ program を
  4 packet に分割して §10.5.4 に PΣ-1(局所補題)を proof draft として執筆。本線当初の
  直接 sup 分解は Sol 反例(P=t, r=−Mt)で偽と判明し撤回・registry 化。3 点 Lagrange の
  定数 8ε⁻² と osc 項付き (ii) を採用、数値検証(係数和 → 8、2×10⁴ 配置)を記録。
  S4a 側は Sol の D-相殺機構(anchor D⁻¹ × weighted chain × exit D)を設計候補として採用予定
  だが、低自信度 2 補題(Norming/Anchor-D 0.86、mode-coherence 0.88)は本線書き下しと
  独立査読を経るまで非主張。PΣ-2/3/4・S4a-W*/U1/M1/EW・S4c は open。
- v0.11.1(2026-08-17): luna R-PS1 = **受理可**(blocking/major なし)。minor 3 件を反映:
  [PS1-M1] 閉区間前提と osc_J r の定義を明記。[PS1-M2] sharpness を厳密化(係数和の閉形式
  `8−8ε+ε²`、Chebyshev witness、random 探索の seed/domain と非証拠明示)。[PS1-M3] 撤回記録を
  RetiredClaim 形式(偽の不等式 + gap `1+log(Mε)` の witness)へ機械検算可能化。
  PΣ-1 を accepted へ昇格(R-PS1 PASS `f875d76`)。次 = PΣ-2(max-envelope lift)。
- v0.11.2(2026-08-17): 補題 PΣ-2(max-envelope lift)を proof draft として執筆(R-PS2 待ち)。
  unary/binary 両形で `A_{U_H} ≤ log(8ε⁻²) + (1+ε)Λ`。機構 = 窓 Lipschitz
  (`sup_I r − sup_J r ≤ Λ`、|I| = 1)+ max-lift(`max_i a_i − max_i b_i ≤ max_i(a_i−b_i)`)
  + PΣ-1(ii)。binary の第 2 branch は定数消去で log penalty 不要。per-window 加算 penalty
  `log(8ε_chain⁻²)` の O(T) 吸収は PΣ-3 の義務として明示的に非主張。数値診断 8×10³ 配置
  (seed 7)違反なし。
- v0.11.3(2026-08-17): luna R-PS2 = **受理可**(blocking/major なし)。minor 2 件を反映:
  [PS2-m1] status surface 同期(header 版数 v0.10.4 → 現行、§10.5.4 冒頭の「PΣ-1 のみ主張」を
  PΣ-1/PΣ-2 主張・PΣ-3/4 非主張へ)。[PS2-m2] interface 注記の `N_s` を「polynomial-envelope
  record を消費する窓数」と定義し `N_s ≤ N ≤ 2T+1 = O(T)` に修正(旧 `N_s ≤ T+1` は根拠なし)。
  PΣ-2 を accepted へ昇格(R-PS2 PASS、fixed SHA `540d0c1`)。次 = PΣ-3(ray-wide ledger)。
- v0.11.4(2026-08-17): 補題 PΣ-3(ray-wide ledger)を proof draft として執筆(R-PS3 待ち)。
  unweighted ledger `Σ[A + κΛε] ≤ (1−δ/2)T²/2 + C_ΣA(T+1)`、
  `C_ΣA = 2log(8ε_chain⁻²) + 4R + 3`。機構 = PΣ-2 の per-window bound + leaf_phase_max
  witness + 重なり窓の二次式和 `Σ(a_k+1) ≤ (T+1)²/(2(1−ε)) + (T+1)` + 係数吸収
  `(1+δ/8)(1+δ/4)(1−δ) ≤ 1−δ/2`。weighted 側(RF-3)・assembly・(E-w) は非主張。
  frequency witness の registry 必須化は PΣ-4 の手術義務として明示。
- v0.11.5(2026-08-17): luna R-PS3 R1 = blocking 2 件を全受諾。[PS3-B1] segmentation 規約が
  §10.3 と未接続 → PΣ-3 (h0) を C′ の実規約(`a_1 = T−1`、停止 `a_N ≤ 1`、切断なし)へ整合、
  §10.3 に endpoint 規約 pin を追記。[PS3-B2] 0 切断読みでの窓和 bound 破れ(luna 反例
  T=3, ε=0.2 で 14.2 > 14.0)→ 停止規則により切断が構成不能となり解消。窓和は
  `NT − βN(N−1)/2 ≤ T²/(2β) + T`(全 N で成立)へ差し替え、`C_ΣA = 2log(8ε_chain⁻²)+4R+2`
  に改善。[PS3-m1] `δ ∈ (0,1]`、`R ≥ 0`、`κ_chain ≥ 0` を仮説に明記。[PS3-m2] header 版数
  同期。R-PS3 R2 待ち。
- v0.11.6(2026-08-17): luna R-PS3 R2 = **受理可**(finding なし)。B1/B2/m1/m2 の修正を全て
  検証(N < 2T−2 の導出、R1 反例の再試験で 6.6 ≤ 8.625、最終帳簿の欠落なし)。RF-3 の
  accepted 定数は endpoint 規約 pin の下でも不変とクロス検証(`a_k+1 ≤ T ≤ T+1` で
  `Σ_kΛ_{η,k} ≤ 4[s_m²(T+1)²+s_m(T+1)]` 成立)。PΣ-3 を accepted へ昇格
  (R-PS3 R2 PASS、fixed SHA `65bb02e`)。次 = PΣ-4(route 昇格手術)。
- v0.11.7(2026-08-17): PΣ-4 registry 昇格手術(R-PS4 査読待ち)。`K2Q-aff-u`/
  `generalized-singleton-u` の A-ledger を `polynomial-envelope / accepted(assembly_proof_ref)`
  へ更新し、obligation 欄に intrinsic assembly_proof_ref(PΣ-2 = `4d0f636`、PΣ-3 = `65bb02e`
  の full SHA)+ `leaf_phase_max` witness 必須を記載。§10.4 `A_ledger_witness` に
  polynomial-envelope/accepted の frequency witness 必須化(`NONE` 不許可)を追記。
  §10.5.4 表の minors SHA を明示(PΣ-1 `050156b`、PΣ-2 `4d0f636`)。§10.7 に S4-0.PS
  (acceptance 記録)と S4-0.PS-PROMOTE(手術、R-PS4 査読待ち)を新設。fail-closed tests に
  昇格 row の positional binding・stale token 検査・intrinsic SHA prefix 検査を追加。
- v0.11.8(2026-08-17): luna R-PS4 R1 = blocking 1 + major 1 を全受諾。[PS4-B1] stale consumer
  prose 3 箇所を修正(§7 の残余 blocker を「R-PS4 audit + coverage」へ、§10.5.4 冒頭を
  「PΣ-1/2/3 accepted 主張・PΣ-4 手術済み未受理」へ、PΣ-3 scope の「PΣ-4 で行う」を
  「本 version で実施済み(R-PS4 査読待ち)」へ)。[PS4-M1] tests を拡張: active region の
  stale prose 検査、§10.5.4 状態表・§10.7 ledger の行単位 binding(S4-0.PS の 5 SHA、
  S4-0.PS-PROMOTE の査読待ち marker)、promoted row 内の intrinsic SHA tuple を PS-4 専用
  テストへ複製(RF テスト非依存化)。R-PS4 R2 待ち。
- v0.11.9(2026-08-17): luna R-PS4 R2 = major 1 件のみ(revert 5 パターンの fail-closure は
  全て捕捉確認、23 passed)。[PS4R2-M1] 旧文言「PΣ-4 で行う」(空白なし variant 含む)を
  stale token 集合へ追加し、R1 旧文言への差し戻しを fail-closed 化。R-PS4 R3 待ち。
- v0.12(2026-08-17): luna R-PS4 R3 = **PASS**(reviewed SHA `58b9c9f`、findings なし、
  R1 文言への一時差し戻しで 1 failed を実地確認)。S4-0.PS-PROMOTE を PASS へ更新、
  PΣ-4 を accepted へ昇格 — **polynomial ΣA program(PΣ-1/2/3/4)完結**。
  `K2Q-aff-u`/`generalized-singleton-u` は polynomial-envelope/accepted の resolved row と
  なり、S4b closure の残余は interval coverage の RouteRecord 検証のみ。tests を acceptance
  状態へ同期。
- v0.12.1(2026-08-17): Sol high consultation 第 2 回(S4b coverage 設計)を受け、S4b-COV0
  (selection schema 手術、spec-only)を実施(R-COV0 査読待ち)。§10.5.5 新設: DomainSchema
  非排他性の記録(deg P=0 の K2/K2Q・trivial/generalized 重複、D-ROOT-FAR の far 条件欠如)、
  canonical route selector(等号 M_k=1/8 は held、uncertified fail-close)、
  RayCoverageManifest(K_T={1..N−1}、I_N は TerminalRecord へ — J_N 不存在の off-by-one 封じ)、
  補題 S4b-COV(COV-1/COV-2)は open, not claimed。§10.4 に `selection_witness` field と
  registry/ray manifest 分離を追記、§10.3 条件 4・S4b-β を K_T へ同期。採用順序:
  COV1 → W1 → W2 → C0(compact initial estimate mini-packet)→ W3 → W4/U1/M1 → EW。
- v0.12.2(2026-08-17): luna R-COV0 R1 = blocking 2 + major 1 + minor 2 を全受諾。
  [COV0-SEL-01] CanonicalNodeFormEnum の閉世界を明示、enum 外(`deg P∈{3,4,5}`、
  both-polynomial binary)は `uncertified` fail-close、閉世界性は (COV-0) として補題 S4b-COV の
  第一義務に追加(FR3 の `d_ℓ≤5` との整合は未証明と明記)。[COV0-INDEX-02] PΣ-3 の record 和を
  `Σ_{k∈K_T}` へ制限(主張の弱化方向のみ、k=1..N 等差 majorant による部分和抑えを明記)、
  RF-3 に index 注を追加(`C_step,N` 不定義、`J_N` 非再導入)。[COV0-WIT-03] `selection_witness`
  を 4 成分(`threshold_certificate` 追加)、`QR5-w`⇒held / `root-far`⇒far 必須化、far 条件は
  schema でなく selector witness 供給と明記。[COV0-LEDGER-04] 安全側注記を unweighted
  subledger に限定、RF-3 は独立帳簿。[COV0-TEST-05] tests: COV1 premature acceptance の
  active region 全域禁止、closed-world/guard/index fragment binding を追加。R-COV0 R2 待ち。
- v0.12.3(2026-08-17): luna R-COV0 R2 = blocking 1 + major 1 を全受諾。[COV0R2-PROV-01]
  v0.12.2 で accepted proof body(§10.5.3/§10.5.4)へ加えた index 編集は source_ref の
  content-SHA 契約違反 → **全て revert**(PΣ-3 は `Σ_{k=1}^{N}` の accepted 本文へ、RF-3 の
  in-body 注を削除。機械検証: 両 section は pre-COV0 監査状態 `b878577` と一致)。K_T 制限は
  §10.5.5 の consumer-side index 契約のみが掌理する。[COV0R2-TEST-01] tests:
  `selection_witness` field row の完全一致束縛(4-tuple + guard coupling)、補題 S4b-COV
  block 内での (COV-0) 直接検査、accepted PΣ-3 本文の drift 監視と in-body 注の再導入禁止を
  追加。R-COV0 R3 待ち。
- v0.12.4(2026-08-17): luna R-COV0 R3 = **PASS**(reviewed SHA `256ab38`、findings なし。
  §10.5.3/§10.5.4 の SHA-256 バイト一致・mutation 再プローブ 3 種の捕捉・24 passed を確認)。
  COV0 を accepted へ昇格、§10.7 に S4-0.COV0 行を新設、tests を acceptance 状態へ同期。
  S4b closure の残余は COV1(canonical coverage lemma、(COV-0)(COV-1)(COV-2))のみ。
- v0.12.5(2026-08-17): 補題 S4b-COV の証明を proof draft として執筆(R-COV1 待ち)。
  読解調査(§3 枠候補・§10.5 transition 宣言・補題 W/W′ の適用範囲・一遷移文書 split(ii))に
  基づく核心: (COV-0) は「現行 interface の生成規則 (g1)–(g4) はいずれも多項式因子を導入せず、
  routed form は {unary-atom, binary-pure-atom, root-2+1} に収まる」という強形で成立。
  split(ii)/(iii) は chart-only(v0.8.16 reachability audit)で node shape を供給しないため、
  polynomial row(K2Q-aff-u/generalized-singleton-u)は resolved-but-unreachable と位置づけ、
  将来の S4-0 改訂での到達可能化には COV-0 再証明を必須と明記。`d_ℓ≤5` は静的極限対象専用
  (補題 W/W′ の scope 明示)で finite-m routed node に非適用。(COV-1) は rank 3 root が
  常に root-2+1 形であること + M_k 完全二分、(COV-2) は witness 構成の列挙による。
- v0.12.6(2026-08-17): luna R-COV1 R1 = blocking 1 + major 2 + minor 1 を全受諾。
  [COV1-01] (COV-0) を「S4b RouteRecord 到達 node に限る reachability invariant」として
  再定式化し、非 producer(`F_{≤1}`、`G_{ν̂,0}`、split(ii)/(iii) 出力)を出典付きで明示。
  [COV1-02] `c₁c₂c₃≠0` の根拠を rank でなく「selector が root-2+1 を選ぶ ⇔ 三非零 leaf 残存」
  に修正、零係数は lower-rank 再分類と明示。[COV1-03] collision witness を §2 の単一衝突
  cluster 入力 + `d_w`/`s_m` 定義から導出(`d_w ≤ s_m ⇒ |ΔA| ≤ s_m²、|ΔB| ≤ s_m`)、
  compactness 出典を撤回、RF ledger には `m ≥ m₀`(`m₀ ≥ m_RF`)を明示。[COV1-04] 三層区別
  (resolved row = capability / current producer = なし / RootStep consumer = weighted のみ、
  polynomial-envelope は dead generality)を scope に追記。R-COV1 R2 待ち。
- v0.12.7(2026-08-17): luna R-COV1 R2 = minor 1 件のみ(実質 4 指摘は全て修正済みと確認)。
  [COV1R2-01] RF threshold の集合記号による誤記を撤去し、正しい形 `m ≥ m₀`
  (`m₀ := max(m_{FR-S1′/S1″}, m_RF)` より `m₀ ≥ m_RF`)へ本文・履歴とも修正。R-COV1 R3 待ち。
- v0.12.8(2026-08-17): luna R-COV1 R3 = BLOCKED 1 件([COV1R3-01] v0.12.7 履歴が誤記法を
  引用形で再掲)。引用を撤去し全ファイルで集合記号の残存 0 を確認。R-COV1 R4 待ち。
- v0.13(2026-08-17): luna R-COV1 R4 = **PASS**(reviewed SHA `c36d818`、findings なし)。
  補題 S4b-COV を accepted へ昇格、§10.7 に S4-0.COV1 行を新設 — **S4b closure 完結**
  (全 6 route resolved、PΣ-1..4/RF/COV0/COV1 accepted。旧 exponent-4 split-row audit は
  v0.8.15 反例退役で QR5-w へ一本化済み)。§7/§10.1 の blocker 記述を S4a へ更新、tests を
  acceptance 状態へ同期。次 = S4a-W1(Child-reserve)。
- v0.13.1(2026-08-17): Sol high consultation 第 3 回(W1 係数予算監査)。判明した設計修正:
  accepted L2a′(c=2) の `(1−δ/2)` 出口は (E-w) target を使い切り、RF 二次費用と両立しない
  (D-相殺で消えるのは `D_H⁻¹D_H` のみ、conf 0.98)→ W2 = c=2 強形(exact divided
  difference + 0–2 jet norming、`(1+t)²` 因子、`η_sep`/`s_m` 非依存、conf 0.97)を新設。
  U1 は critical path から退役(現 public root は weighted-only、PΣ は capability 保持)、
  M1 は mode audit に縮小、Anchor-D(C0)は存続(design note の `D_{H_s} ~ s⁻²` 見込み)。
  §10.8 を新設し W1(Child-reserve interface)を proof draft として執筆(R-W1 待ち)。
  W2 の jet 計算(`ψ₀=0`、`ψ₁=b`、`ψ₂=(a+(B₁+B₂)b)/√2`、二分法下界 `1/(2√2)`、`K_β(R)`)
  と予算恒等式 `(1−δ)/2 + δ/8 = (1−3δ/4)/2` は本線で算術的に予備検算した(W2 の proof/
  acceptance を意味しない。W2 は open, not claimed のまま)。
- v0.13.2(2026-08-17): luna R-W1 R1 = blocking 2 + minor 3 を全受諾。[W1-01] 符号・多項式
  仮定を明示(`C_X > 0`、`P_X: [0,∞)→[0,∞)` 非負係数固定次数、`P := P_X + P_Y` — pointwise
  max は多項式でないため和に変更)、`K_{δ,R} = {|A|≤1−δ}×{|B|≤R}` の定義と authoring
  location(K2 文書)を明記。[W1-02] unary case を式として定義(`e^{U_H}=|X|`、`D_H=1`)、
  `R_H > 0`(zero-pruning 後)を仮定に追加。[W1-03] 「余地がない」を現行 architecture 限定に
  修正、margin は二次係数のみと明示。[W1-04] `D_H` witness を design note(非証明)へ降格、
  path `Φ_s = e^{sz}` を固定、厳密化は C0 義務。[W1-05] 履歴の jet 検算を「予備検算・W2 の
  proof/acceptance ではない」と注記。R-W1 R2 待ち。
- v0.13.3(2026-08-17): luna R-W1 R2 = **PASS**(reviewed SHA `a59768e`、findings なし)。
  W1 を accepted へ昇格、tests 同期。
- v0.13.4(2026-08-17): 補題 W2(Pair norming、c=2 強形)を proof draft として執筆
  (R-W2 待ち)。機構 = exact divided difference(線分 path、`K_{δ,R}` 凸性)+
  正規化 0–2 jet(`ψ₀=0, ψ₁=b, ψ₂=(a+(B₁+B₂)b)/√2`)+ 二分法(下界 `[2(1+2R)]⁻¹` /
  `1/(2√2)`)+ 係数の norm 消去(`K_β(R)`)。`C₂(R) = 1+K_β(R)`、`s_m`/separation 非依存。
  数値診断 4×10³ 配置(Gram 閉形式、near-cancellation・collision 含む)違反なし余裕 ×96。
- v0.13.5(2026-08-17): luna R-W2 = **受理可**(findings ゼロ)。luna 独自検証: Gram 式を
  係数級数と 70 桁精度で照合(相対誤差 1.5×10⁻⁷⁰)、4 設定 × 31,815 点(δ=0.05、
  R ∈ {0, 1.5, 5}、near-cancellation `‖f‖/max|c_i| ≈ 1.3×10⁻⁷`)で違反なし。
  W2 を accepted へ昇格(R-W2 PASS、fixed SHA `a0fcd10`)、tests 同期。
  次 = C0(Compact anchor — program 最弱点、Sol conf 0.86)。
- v0.13.6(2026-08-17): Sol high consultation 第 4 回(C0 設計)。本線提案の二場合分け
  (`A ≥ B/2` は自明 anchor `|G| ≤ 2` + `M ≤ 3A`、`A < B/2` は singleton floor anchor)が
  成立と裁定(conf 0.99)— **Anchor-D の短い証明が得られ、program 最弱点(0.86)が解消**。
  補題 C0(Terminal two-anchor)を proof draft として執筆(R-C0 待ち)。依存順を
  C0 → M1 → W3 → W4 → EW に改訂、W4 を Terminal-cancelled exit に改名、全 packet
  conf ≥ 0.97。`C_Φ` 指数は当初、粗い評価に基づき本線が安全側へ緩めたが、後続 R-C0 で
  luna が `(1+a)` 相殺による鋭化を提示し consultation 原案の成立を確認(v0.13.7 で採用)。
  数値診断 3 class × 1500 配置で floor/product とも違反なし。
- v0.13.7(2026-08-17): luna R-C0 = minor 2 件のみ(本体不等式は全段確認、Gram 相対誤差
  3.7×10⁻¹⁵ の独立検算つき)。[C0-01] `C_Φ` 指数を鋭化 `R²/(2δ)` へ復帰(分子
  `≤ R²(1+a)` の `(1+a)` 相殺を証明に追記)。[C0-02] 数値マージンの記載をサンプル依存と
  明示し、境界配置(floor 比 ~28)・深 cancellation(余裕 ~1.9×10⁴)の luna 独立検算値を
  併記。R-C0 R2 待ち。
- v0.13.8(2026-08-17): luna R-C0 R2 = **PASS**(reviewed SHA `f31cca0`、findings なし)。
  C0 を accepted へ昇格、tests 同期。S4a 残余 = M1 → W3 → W4 → EW。
- v0.13.9(2026-08-17): 補題 M1(weighted-root mode audit)を proof draft として執筆
  (R-M1 待ち)。accepted 面(S4b-COV、RouteSpec、§10.4/§10.5.5 契約)の系: (M1-1)
  root record は weighted-only、(M1-2) ray 積算は weighted ledger のみ(PΣ は capability
  非消費)、(M1-3) `I_N` は TerminalRecord。新しい解析的主張なし。
- v0.13.10(2026-08-17): luna R-M1 = minor 3 件を全受諾。[M1-2a] (M1-2) を public ray
  ledger に scope 限定(内部 provenance の child route を禁止しない文言へ)。[M1-2b]
  非空性の論理を訂正(根拠 = COV-2 の公開 record 存在 + root-only consumption 契約;
  unweighted 項の不在は mode 排他性から)。[M1-SURFACE] stale status 3 箇所を同期
  (header、§10.5.5 の TerminalRecord 消費者を C0 accepted へ、§10.7 要約行)。
  R-M1 R2 待ち。
- v0.13.11(2026-08-17): luna R-M1 R2 = **PASS**(reviewed SHA `fd18e9d`、findings なし)。
  M1 を accepted へ昇格、tests・status surface 同期。S4a 残余 = W3 → W4 → EW。
- v0.13.12(2026-08-17): 補題 W3(Weighted chain)を proof draft として執筆(R-W3 待ち)。
  (M1-1) の weighted-only record を `(S4-step-w)`(`γ=5`、`κ=0`)で `k∈K_T` 内向きに反復、
  指数を ε 因子 / QR5 uniform / RF graded の三分で押さえ
  `(δ/8)T² + C_ch(T+1)`、`C_ch = 10log(1/ε_chain) + 2log⁺C_T + 6C_RF`。
  kernel 不等式・witness は accepted 面の消費のみ(再証明なし)、混在 ray も同一積算。
- v0.13.13(2026-08-17): luna R-W3 R1 = blocking 1 + minor 1 を全受諾。[W3-01] RF 帰納の
  inline 前提 `32C_T ≥ 1` が未契約 → W3 に WLOG 正規化 `C_T := max(1,C_T)` を明記
  (上界定数の拡大は accepted 不等式を保存、RF body 不変)、§10.6 定数表に消費時正規化
  条項を追記して契約化。[W3-02] RF cost の明示選択
  `C_step,k := exp(C_RF(1+Λ_{η,k})) ≥ 1` を証明に追記(log 非負性の根拠)。R-W3 R2 待ち。
- v0.13.14(2026-08-17): luna R-W3 R2 = **PASS**(reviewed SHA `4086ef9`、findings なし。
  `C_T` は上界としてのみ使用され正規化で全不等式保存、§10.6 追記は consumer-side contract
  として precedent 整合と確認)。W3 を accepted へ昇格、tests・status 同期。
  S4a 残余 = W4 → EW。
- v0.13.15(2026-08-17): 補題 W4(Terminal-cancelled exit)を proof draft として執筆
  (R-W4 待ち)。accepted 済み W1/W2(exit)× W3(chain)× C0(anchor)の三積で
  `|H(z₀)| ≤ 2C₂C_anc·R_H(1+T)²e^{(1−3δ/4)T²/2+(R+C_ch)(T+1)}`。endpoint 被覆
  (`T = a₁+1 ∈ I₁`)、W2 premise の witness 供給、`M‖G‖` 相殺を明示。新しい解析なし。
- v0.13.16(2026-08-17): luna R-W4 = minor 1 件のみ([W4-01] `ξ₁ ≠ ξ₂` の出典を
  D-QR5-HELD の keys でなく accepted (COV-2) の global REFIX invariant へ精密化)。反映済み、
  R-W4 R2 待ち。
- v0.13.17(2026-08-17): luna R-W4 R2 = **PASS**(reviewed SHA `cb87eee`、findings なし)。
  W4 を accepted へ昇格、tests・status 同期。S4a 残余 = EW のみ。
- v0.13.18(2026-08-17): Sol high consultation 第 5 回(EW gauge-representation)。裁定 A′:
  W4 は original 座標の `U_m^{-1}h_{ℓ,m}` へ直接適用し、collision scale は original
  parameters の `s̃_m` で再定義(gauged `d_w` の不変性は vacuum stabilizer 限りで
  full metaplectic covariance なし — COV-2 witness provenance の局所穴)。Option B
  (metaplectic 包絡合成)は不成立(squeeze は weighted composition でない)。
  補題 EW-B(bridge、定義のみ)+ 補題 EW((S4-Ew)、rank 1/2/3 × T 場合分け、
  `C_w = 2C₂C_anc e^L`、`C_lin = R+C_ch+2`)を proof draft として執筆(R-EW 待ち)。
  rank ≤ 2 は W2/W1 で明示定数 calibration(L2a′ 引用不要の形)。
- v0.13.19(2026-08-17): luna R-EW = **受理可**(minor 3 件のみ、数式・定数監査は全段確認)。
  [EW-B-01] original 座標の表記固定を EW-B 内に明記(§2 accepted 面は不変)。
  [EW-PROV-01] `s_m^{EW} := s̃_m` の witness slot 代入と original 再インスタンス化を明文化
  (COV-2 再受理不要と判定)。[minor] (E-w) の定数非依存は `C_w, C_lin` に限る旨を明記
  (`m₀` は収束速度依存で可)。R-EW R2 待ち。
- v0.14(2026-08-17): luna R-EW R2 = **PASS**(reviewed SHA `b39216f`、findings なし)。
  補題 EW-B/EW を accepted へ昇格 — **S4a program 全 8 packet 完結、§10.2 の c=3 target
  (S4-Ew) 閉鎖**。S4-0 → S4b → S4a の全 packet が fixed-SHA 査読つきで closed。
  残余は S4c(N3′/N4 の c=3/(E-w) 同期、FR7 no-return audit、original/gauged provenance
  同期)のみ。tests・status surface 同期。
- v0.14.1(2026-08-17): S4c を proof draft として執筆(R-S4C 待ち、§10.9 新設)。
  (i) 閉包文書 §4.3 に N3′/N4 の c=3/(E-w) 具体化注記(v1.8.13)を追加(§4.3.4 凍結
  snapshot 不可触を確認済み、非主張境界を注記内に明記)。(ii) FR7 no-return audit を
  機械走査 + 逐語確認で実施し非混入表を記録(排除文脈の言及は違反に数えない規約を明文化、
  fail-closed tests で §10.8/RouteSpec の禁止 token 不在を固定)。(iii) original/gauged
  provenance 同期表と FR1–FR7 充足根拠(各 fixed SHA)を記録 — c=3 FR は program 内
  全行充足、表現は「証明ドラフト・複数 LLM 検算済み・独立再査読待ち」で保守的に維持。
- v0.14.2(2026-08-17): luna R-S4C R1 = blocking 2 + major 1 + minor 2 を全受諾。
  [S4C-001] 「同文」を撤回し「split 境界一致 + 依存集合の具体化」へ精密化(FR 文書・
  閉包文書とも)。[S4C-002] 監査表に §10.5.3 の排除宣言を追記し対象範囲を明記、tests を
  §10.5.2–10.5.5 まで拡張(`U_F` は排除文脈 1 件のみを許容する文脈束縛つき)。
  [S4C-003] 閉包文書の active status 2 箇所を更新((E-d) は c=3 blocker でなく一般 c の
  義務、c=3 FR-S4 は program 内 draft 完了・R-S4C 待ち)。[S4C-004] 閉包文書 header の
  版数/日付/PR 参照(#158→#178)と同期注記の v0.14.1 を修正。[S4C-005] FR5 根拠の RF を
  primary SHA `9f19389`(minors `c271919`)へ併記修正。R-S4C R2 待ち。
- v0.14.3(2026-08-17): luna R-S4C R2 = blocking 1 + minor 1。[S4CR2-001] §10.9 状態表の
  「FR6 split 同文性」残存を「split 境界一致(依存集合は注記側が具体化)」へ修正。
  [S4CR2-002] 閉包文書 §11 の PR 参照(#158)を #178 承継の経緯つきで更新。R-S4C R3 待ち。
