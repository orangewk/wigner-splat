# 三原子 exact block-frame preparation (FR) — statement wip

日付: 2026-08-10 / 著者: 本線 / status: **v0.8.7 — FR-S1′/FR-S1″ accepted、FR-S4-0 interface revision (R-S4-0 R8 pending)、FR-S4b/a/c open**

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
- split(i): K2Q-wt による direct transfer。
- split(ii): source 上の三者深消滅。
- split(iii): pair principal coefficient の縮退 witness。

証明書がどの FR2 chart を選ぶか、また選んだ chart が FR3/FR4 をどう与えるかは未証明。

## 6. 最小の証明順

1. **[補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md) (plain c=3 valuation 上界)**: F3′ と独立に、相異三原子 span の最大 valuation が 5 以下であることを自己完結に証明する。
2. **FR-S1′ (weighted SVD frame、R-A′ PASS)**: 真空 gauge 後の (2,1)-weighted 距離と J⁵-SVD で、plain single-scale triple の exact 枠を定義する。
3. **nested 2+1 接続**: [static generalized 補題 W′](2026-08-11-three-atom-wronskian-valuation-W--wip.md) と §9 の finite-m FR-S1″ は R-W′ / R-A″ PASS。
4. **FR-S4-0 (interface specification)**: §10 で per-node segmentation、U_H-ledger、(E-w)、kernel/constant 契約を固定する。proof claim は置かない。
5. **FR-S4b (FR5 kernel routing)**: K2/K2Q/QR5 を node ごとに割り当て、split-row を U_H-ledger 下で監査する。
6. **FR-S4a (FR6-core envelope assembly)**: S4b の kernel と C′ chaining から (E-w) を導く。
7. **FR-S4c (FR6/FR7 closure)**: N3′/N4 台帳と no-return audit を閉じる。
8. 固定 SHA で FR1–FR7 を独立再査読する。

## 7. 現在の blocker

plain single-scale triple の FR-S1′ は固定 SHA `ed25401` の R-A′、nested 2+1 の FR-S1″ は
固定 SHA `61111cc` の R-A″で PASS。現在の最初の未解決点は **FR-S4-0 interface specification**。
§10 は specification draft であり、R-S4-0 判定前には c=3 の (E-w) 改訂や FR5–FR7 の閉鎖に数えない。
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
| S4-0 | FR-S1′/S1″、K2/K2Q/QR5、C′ の候補 interface | 本節の型付き interface のみ | specification revision (R-S4-0 R8 pending) |
| S4b | S4-0 + reviewed node kernels | per-segment FR5 routing、split-row audit | open, not claimed |
| S4a | S4b + fixed-SHA PASS の `Cprime_ref` | c=3 weak envelope (E-w) | open, not claimed |
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
   `J_k=I_k∩I_{k+1}` (長さ `ε_chain`)を作る(`N≤2T+1`)。各 `(I_k,J_k)` に
   resolved `RouteKind` の `RouteRecord` を割り当て、interval依存の domain witnessをここで検証する。

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

reviewed QR5(U_T) と K2Q-wt は `(S4-step-w)` 型であり、`(S4-step-u)` を直接供給しない。
特に weighted estimate から unweighted estimate への変換を暗黙に行ってはならない。その変換には
`sup_{I_k}U_H−inf_{J_k}U_H` が必要で、現在の `A_{H,k}=sup_{I_k}U_H−sup_{J_k}U_H` では足りない。
pair-block の零点近傍ではこの差を一様に抑えられない可能性がある。S4a は mode ごとに別の assembly を
与え、weighted routeから (E-w) へ進む場合は、そのための新しい比較を明示的に証明する。

acceptance 条件は次の七つ。

1. `C_step,γ_H,κ_H≤κ̄_route` は compact class、node type、route labelだけに依存し
   `m,θ,k,T` に非依存。
2. cell分割を使う証明では `#𝒫_{H,k}≤N_cell` と内部overlapを示し、その積を一つの `C_step` へ
   吸収する。分割なしの直接 unit-step kernelでもよい。
3. pair leaf nodeでは `Re(q_1−q_2)+log|c_1/c_2|` が実二次以下なので dominance cellは高々3。
   root pair-block vs singleton ではこの推論を使わず、S4b の **split-row audit under U_H-ledger** が
   一様な root stepを直接証明する。rootで `N_cell` を導入する場合だけ、その一様性も証明する。
4. 各 `I_k` は root level でちょうど一つの resolved route recordに覆われる。QR5 routeを使うなら pair-held 条件
   `sup_{I_k}|q_2−q_1|≤1/8` の witnessを interval 全体について添付する。far/unheld intervalを
   held cellへ読み替えず、別 routeまたは未解決 obligationとして残す。
5. `κ_H>0` または `A_ledger_kind=phase-lipschitz` の routeは `Λ_{H,k}` を underlying Gaussian
   phase derivativeへ結ぶ `frequency_source/bound_witness` を持ち、
   `Λ_{H,k}≤(1−δ)(a_k+1)+R` を示す。`κ_H=0` かつ `weighted-no-A` の routeだけ
   `frequency_source=NONE` としてよい。
6. S4b の出力は一 interval 当たり一つの `RootStep_k` とする。child kernelはその root stepを証明する
   内部 provenanceであり、S4a が child stepとancestor/root stepを別々に積算してはならない。
7. `coverage_manifest` の重複/欠落、`state=unresolved` の `RouteKind`、未受理 dependency、有限定数の欠落は
   S4b-α を停止させる。unresolved entryを interval recordや仮の modeへ coercionしてはならない。

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
                   root-far,K2Q-wt-w,split-ii,split-iii,trivial-u}

と固定する(`REFIX` は routeでなく前処理 transitionなので含めない)。`RouteKind` は次の三variantである。

| variant | required fields |
|---|---|
| `resolved` | `(route_id∈CategoryEnum,route_spec_ref,source_ref,assembly_state)`。`(arity,mode,source rule,domain schema,C̄,γ,κ̄,inequality,A-ledger rule,assembly rule)` は §10.5 の同じ `route_id` の唯一の `RouteSpec` 行と**全field完全一致**し、個別override不可 |
| `unresolved` | `(route_id∈CategoryEnum,expected_arity∈{unary,binary},missing_obligation_id∈MissingObligationEnum)` のみ。`mode/source_ref/constants/inequality_id` を仮置きしない |
| `excluded` | `(route_id∈CategoryEnum,exclusion_proof_ref)`。`exclusion_proof_ref=(category_id,unreachable_domain_witness_id,canonical_file,anchor,fixed_SHA,PASS)`、`category_id=route_id`、かつ証明statementが「全inputで当該categoryへ到達不能」と受理された場合だけ |

`DomainSchemaEnum` と `MissingObligationEnum` も有限に固定する。

  DomainSchemaEnum := {D-K2,D-K2Q-AFF,D-GENERALIZED-SINGLETON,
                       D-QR5-HELD,D-K2Q-WT,D-TRIVIAL}
  MissingObligationEnum := {M-K2-STATUS,M-K2Q-STATUS,M-ROOT-FAR-KERNEL,
                            M-SPLIT-II-KERNEL,M-SPLIT-III-KERNEL}
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
| `D-K2Q-WT` | `active_children_nonzero`, `P_nonzero`, `c2_nonzero`, `deg_P_le_2`, `qdiff_nonconstant`, `split_i_witness_ref` |
| `D-TRIVIAL` | `c≠0`, unary exact-identity ref |

§10.5 の `RouteSpec` 表を route-specific discriminant の唯一の authoring location とする。各rowは
このIDの一つを使い、自由文のschema/reasonや field overrideを新設しない。新しいkeyや組合せが必要なら
まずS4-0と `RouteSpec` 行を改訂する。

registryは `coverage_manifest=(CategoryEnum,entries)` を持ち、各category IDが resolved/unresolved/excluded の
**ちょうど一つ**として現れること、重複・欠落がともに空集合であることを検査する。この完全性検査の後にだけ
S4b-α の「unresolvedなし」を判定する。

`source_ref` も discriminated union とする。

- `external=(kernel_name,canonical_file,anchor,fixed_SHA,PASS)`。authoring locationの同一 SHA が PASS の場合だけ有効。
- `intrinsic=(INTERNAL-EXACT,this-file-anchor,accepted-S4-0-SHA)`。本S4-0が固定 SHA で受理された後だけ、
  trivial identity用に有効。

resolved entry の `source_ref` は RouteSpec の `source rule` に記された kernel name / canonical file / anchor
と一致しなければ無効である。単に external/intrinsic variantが一致するだけでは足りない。

S4a はこれとは別に

  CprimeSourceRule := (C-prime,
                       docs/2026-08-08-quadratic-phase-turan-K2.md,
                       §3 補題 C′,
                       UNRESOLVED, unresolved)
  Cprime_ref := validated source_ref.external matching CprimeSourceRule

を必須inputとする。K2 theoremを使わないrouteだけの列でも、C′の chaining calculationを参照するなら
このrefを省略しない。従って `source_ref.external` と同じ検証で、指定 fixed SHA の canonical authoring
location が実際に PASS かを照合する。文字列 `PASS` の自己申告だけでは有効にならず、authoring statusが
不一致または未受理ならS4aを開始しない。現行ruleは `UNRESOLVED` なのでrefは無効であり、固定SHAの
再査読後にrule自体を concrete SHA/PASSへ改訂するまでS4aは開始不能である。

`split_i_witness_ref` も validated external ref とし、現行 source ruleを
`(split-i,docs/2026-08-09-three-atom-one-transition--wip.md,§3.6.2,UNRESOLVED,unresolved)`
とする。固定SHA再査読後にrule自体が concrete SHA/PASSへ改訂されるまで `K2Q-wt-w` のdomainは未受理である。

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
| `node_path` | fixed tree上の有限 path。公開stepは `root` で終わる |
| `envelope_id` | 上記 `U_H`; root 2+1 は `U_T` |
| `interval_id` | `(k,I_k,J_k,ε_chain)` |
| `frequency_allowance` | `(frequency_source,Λ_{H,k},bound_witness)`。`leaf_phase_max` なら `Λ_{H,k}:=max_j sup_{I_k}|q_j′|≤(1−δ)(a_k+1)+R`; 不使用なら `NONE` と `κ_H=0` |
| `A_ledger_witness` | `phase-lipschitz` の式、`weighted-no-A`、`polynomial-envelope/open`、または `polynomial-envelope/accepted(assembly_proof_ref)` |
| `named_constants` | `(C_step≤C̄_route,γ_H=γ_route,κ_H≤κ̄_route,source_ref)`。raw係数依存は禁止 |

`RootStep_k` はこの recordを持つ root `node_path` の唯一の公開出力で、child routeは
`kind_ref/domain_witness` の内部 provenanceに畳み込む。S4a は root outputだけを一度ずつ消費する。

S4a は mode別に

  γ_{*,u/w}:=max_{mode=u/w}γ_route,  C_{*,u/w}:=max_{mode=u/w}C̄_route

を取り(empty modeは `(γ_*,C_*)=(0,1)`)、同じ `ε_chain` を使う。unweighted `phase-lipschitz` recordは
C′ と同じ `ΣA+ΣκΛε_chain` の計算に入れる。`polynomial-envelope/open` が一つでもあれば、
`ΣA` の別証明なしに (E-w) を結論しない。weighted recordは `(S4-step-w)` の積とpointwise envelope growthを
別に帳簿化し、unweighted ledgerへ混ぜない。

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

次表を `RouteSpec` の唯一の authoring location とする。resolved rowの数値欄は必ず
`0<C̄<∞`, `0≤γ<∞`, `0≤κ̄<∞` を満たす。`—` は unresolved であり値を補ってはならない。

| route ID / shape | arity | mode / inequality | source rule | domain schema | `(C̄,γ,κ̄)` | A-ledger / assembly rule | current obligation |
|---|---|---|---|---|---|---|---|
| `K2-u`: `c₁e^{q₁}+c₂e^{q₂}` | binary | unweighted / S4-step-u | `(K2,docs/2026-08-08-quadratic-phase-turan-K2.md,§2 主結果,UNRESOLVED,unresolved)` | D-K2 | `(C_K2,2,1)` | phase-lipschitz / accepted | M-K2-STATUS unresolved |
| `K2Q-aff-u`: `Pe^{q₁}+c₂e^{q₂}` | binary | unweighted / S4-step-u | `(K2Q-aff,docs/2026-08-09-quadratic-phase-turan-K2Q-weight21--wip.md,§6.1 K2Q-aff,UNRESOLVED,unresolved)` | D-K2Q-AFF | `(C_K2Q,4,1)` | polynomial-envelope / proof-required | M-K2Q-STATUS unresolved; ΣA proof別途 |
| `generalized-singleton-u`: `Pe^q` | unary | unweighted / S4-step-u | `(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5 generalized-singleton-u,UNRESOLVED-S4-0-SHA)` | D-GENERALIZED-SINGLETON | `(1,0,0)` | polynomial-envelope / proof-required | S4-0 accepted SHA と ΣA proofが別途必要 |
| `QR5-w`: `B₁₂+c₃e^{q₃}`, `U_T` | binary | weighted / S4-step-w | `(QR5,docs/2026-08-09-pair-block-kernel-K2p1--wip.md,§3.8.6 QR5(U_T),27a1817150ab7a857cdd00320ed3809c73e3c1bd,PASS)` | D-QR5-HELD | `(C_T,5,0)` | weighted-no-A / accepted | interval-wide held witness |
| `root-far`: root 2+1 far/unheld | binary | — | — | — | — | — | M-ROOT-FAR-KERNEL unresolved または accepted exclusion |
| `K2Q-wt-w`: split (i) | binary | weighted / S4-step-w | `(K2Q-wt,docs/2026-08-09-quadratic-phase-turan-K2Q-weight21--wip.md,§6.1 K2Q-wt,UNRESOLVED,unresolved)` | D-K2Q-WT | `(C_21,4,0)` | weighted-no-A / accepted | M-K2Q-STATUS + split_i_witness_ref 未受理 |
| `split-ii`: deep cancellation | binary | — | — | — | — | — | M-SPLIT-II-KERNEL unresolved |
| `split-iii`: pair degeneration | binary | — | — | — | — | — | M-SPLIT-III-KERNEL unresolved |
| `trivial-u`: `ce^q` | unary | unweighted / S4-step-u | `(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5 trivial-u,UNRESOLVED-S4-0-SHA)` | D-TRIVIAL | `(1,0,0)` | phase-lipschitz / accepted | S4-0 accepted SHA + `A_{H,k}≤sup_{I_k}|q′|` witness |

`REFIX` は RouteSpec rowでなく前処理 transitionである。`q₁−q₂≡const`, `P≡0`, `c₂=0`、または
child恒等零を exact 併合/zero-pruningし、残った spanで rank/treeを再固定する。

`RouteSpec` の assembly rule `accepted` は対応する intrinsic/external根拠でそのまま受理、`proof-required` は
`assembly_state=open` または `accepted(assembly_proof_ref)` だけを許す。従って K2Q-aff と
generalized-singletonを bare accepted に変更できない。

split(ii)/(iii) は旧 wrapper 用 certificate であって転送 kernelではない。S4-0 では port 可能と仮定しない。
S4b は「frame の singular-value floorで当該rowが排除される」「新しいnode-local kernelが要る」
「S4-0 segmentation自体を改訂する」のいずれかを証明する。

K2 の authoring file は現時点で `R-K2 R1 BLOCKED / R2待ち`、別参照面には `R-K2 R2 PASS` があり、
source statusが不一致である。本節はどちらも裁定しない。固定 SHA の再査読または K2 authoring locationの
status修復が終わるまで `K2-u` は unresolved であり、S4b-α を通過しない。

### 10.6 Coefficient-free constants

FR5 の各 kernel 定数は `(γ_H,κ_H,δ,R,route label)` と下表の reviewed/compact dataだけに依存し、
表示係数には依存させない。

| name | meaning / permitted dependency | supplied by |
|---|---|---|
| `c_head` | plain/nested head singular floor (`η,t₀` 等のchart data) | FR-S1′/S1″ |
| `C_tail` | normalized frameのFock tail | FR-S1′/S1″ |
| `C_K2,C_K2Q,C_T` | pair/generalized/root kernel constants | K2/K2Q/QR5 |
| `C̄_route,γ_route,κ̄_route,mode` | interval-independent RouteKind template | S4b-α registry |
| `C_step,γ_H,κ_H,ε_chain` | typed RouteRecord / composite unit-step data | S4b-β output |
| `N_cell` | cell分割を実際に使う場合のunit interval・node当たりcell数 | pairは高々3、rootは導入時だけS4b obligation |
| `Cprime_ref` | validated external source_ref specialized to C′ | S4a required external input |
| `C_chain,u`, `C_chain,w` | mode別 product/telescoping constants | S4aでtyped kernel dataから別々に構成 |
| `C_w,C_lin` | (S4-Ew) constants | S4a output |

tree depthは高々2だが、S4aが消費するのは各 `I_k` の一つの `RootStep_k` だけである。child constantの
有限積はその root step内部へ一度だけ吸収し、ancestor/rootと別に再積算しない。stopping-time/Bellman
quantityは c=3 S4 のinterfaceへ加えず、一般 c で必要性を再判定する。

### 10.7 S4-0 acceptance ledger

| ID | specification | current state |
|---|---|---|
| S4-0.1 | packet順 S4b→S4a→S4c と非循環input/output | specification revision (R-S4-0 R8 pending) |
| S4-0.2 | c=3 (E-w)、一般 c (E-d) 保持 | specification revision (R-S4-0 R8 pending) |
| S4-0.3 | registry→ε_chain→record の順序 + mode別root-step | specification revision (R-S4-0 R8 pending) |
| S4-0.4 | RouteSpec literal source / root-only積算 / FR7 vocabulary | specification revision (R-S4-0 R8 pending) |
| S4-0.5 | complete domain keys・category-bound exclusion・status fail-closed | specification revision (R-S4-0 R8 pending) |
| S4b/a/c proofs | none | open, not claimed |

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
