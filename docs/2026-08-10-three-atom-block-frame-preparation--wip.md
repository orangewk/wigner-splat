# 三原子 exact block-frame preparation (FR) — statement wip

日付: 2026-08-10 / 著者: 本線 / status: **v0.7 — plain FR-S1′ R-A′ PASS、static generalized W′ R-W′ PASS、finite-m FR-S1″ proof draft (R-A″ pending)、FR-S4 open**

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
| FR3 | generalized-atom type | 共通 cluster base ξ_{*,m}→ξ* と jet-degree label d_ℓ を持ち、各有限 v_{ℓ,m} が改訂後の (E-d)/(X)/(L-d) を満たす。特に非零 P_ℓΦ(ξ*) (deg P_ℓ=d_ℓ) へ norm 収束。旧 `o′_ℓ≤w−1, deg P_ℓ≤2o′_ℓ` 帳簿は F3′ により撤回。plain c=3 の上界 d_ℓ≤5 は [補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md) が R-W PASS (`1b3e337`)。nested 2+1 は別義務。枠本数 r≤w≤3 |
| FR4 | Gram | Gram(v_{1,m},…,v_{r,m}) の最小固有値が m 一様に正 |
| FR5 | node kernel | 各 radial internal node はその node envelope 固有の reviewed kernel を、m と θ に一様な定数で持つ。2+1 held node は QR5(U_T) |
| FR6 | global envelope | 各 v_{ℓ,m} が補題 N の N3′/N4 envelope を満たす。定数は (c=3,δ,R,one-transition/flag の安定化定数) のみに依存し m,θ に非依存 |
| FR7 | no return | FR5–FR6 の証明で旧 parent U_F への逆比較または旧 DC discount を使わない |

FR1–FR7 が揃って初めて c=3 の補題 N 枠として受理する。QR5 PASS は FR5 の一つの row を供給するだけで、
FR3/FR4/FR6 を閉じない。

## 5. chart 入力として使える既存証明書

三原子一遷移文書の以下は、reduction 完了ではなく pivot/chart 選択の観測量として使う。

- held r=2: one-variable 標準形と pointwise 二側評価。
- held r=1(A): direct transfer。
- held r=1(B): M₁ の小ささ。
- split(i): K2Q-wt による direct transfer。
- split(ii): source 上の三者深消滅。
- split(iii): pair principal coefficient の縮退 witness。

証明書がどの FR2 chart を選ぶか、また選んだ chart が FR3/FR4 をどう与えるかは未証明。

## 6. 最小の証明順

1. **[補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md) (plain c=3 valuation 上界)**: F3′ と独立に、相異三原子 span の最大 valuation が 5 以下であることを自己完結に証明する。
2. **FR-S1′ (weighted SVD frame、R-A′ PASS)**: 真空 gauge 後の (2,1)-weighted 距離と J⁵-SVD で、plain single-scale triple の exact 枠を定義する。
3. **nested 2+1 接続**: [static generalized 補題 W′](2026-08-11-three-atom-wronskian-valuation-W--wip.md) は R-W′ PASS。ν-chart を持つ finite-m FR-S1″ を §9 に proof draft として置き、固定 SHA の R-A″ 待ち。
4. **FR-S4 (envelope assembly)**: K2/K2Q/QR5 を node ごとに使い、parent U_F へ戻らず FR6 を導く。
5. 固定 SHA で FR1–FR7 を独立再査読する。

## 7. 現在の blocker

plain single-scale triple の FR-S1′ は固定 SHA `ed25401` の R-A′で PASS。現在の最初の未解決点は
**nested 2+1 接続**である。static generalized W′ は R-W′ PASS、finite-m ν-chart は §9 の
FR-S1″ proof draftとして起草済みだが、R-A″ 判定前なので accepted には数えない。
旧 moment order だけでは消滅速度を記録できず、
(s,0),(2s,0),(3s,s²) 型の異方的退化で零極限になる。従って chart label は exact moment の
非零/零だけでなく、相対 valuation または同値な flag/blow-up 座標を含まなければならない。

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
| nested 2+1 | proof draft (R-A″ pending) | static generalized W′ は R-W′ PASS。finite-m ν-chart / FR-S1″ は §9 |
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
| A″-1 `ν̂,t` compact chart | proof draft (R-A″ pending) | (A″1)、graded `d_w` chart を不採用 |
| A″-2 exact factorization / head floor | proof draft (R-A″ pending) | (A″3)–(A″4)、W / W′ |
| A″-3 difference-column Fock tail | proof draft (R-A″ pending) | (A″5)–(A″6) |
| A″-4 limit Gram / exact span / tree | proof draft (R-A″ pending) | SVD + exact column変換 |
| A″-5 FR1/FR2/FR4/FR3(X)(L-d) | proof draft (R-A″ pending) | plain FR-S1′との全tree-shape合成 |
| `(E-d)` / FR5–FR7 | open, not claimed | FR-S4 |

## 10. 版履歴

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
