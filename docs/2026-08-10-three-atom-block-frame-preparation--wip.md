# 三原子 exact block-frame preparation (FR) — statement wip

日付: 2026-08-10 / 著者: 本線 / status: **v0.6 — plain補題W R-W PASS、single-scale FR-S1′ proof draft、nested 2+1 / FR-S4 open、R-FRSPEC R5 pending**

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
2. **FR-S1′ (weighted SVD frame)**: 真空 gauge 後の (2,1)-weighted 距離と J⁵-SVD で、各 active single-scale node の exact 枠を定義する。
3. **nested 2+1 接続**: pair child の一般化原子を入力にした補題 W 版を別義務として証明する。
4. **FR-S4 (envelope assembly)**: K2/K2Q/QR5 を node ごとに使い、parent U_F へ戻らず FR6 を導く。
5. 固定 SHA で FR1–FR7 を独立再査読する。

## 7. 現在の blocker

最初の未解決点は FR-S1。旧 moment order だけでは消滅速度を記録できず、
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

正規化配置は compact かつ pairwise separation `η` を持つ。[補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md)
の `J⁵` injectivity と compact-family corollary より

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
| A′-1 relative `d_w` chart | proof draft | residual vacuum stabilizer invariance と pivot固定を§2で明示 |
| A′-2 head floor `σ_3≥c₀s⁵` | proof draft | 補題 W + compactness + exact factorization |
| A′-3 Fock tail `O(s⁶)` | proof draft | (S4) の一様級数定数を検算 |
| A′-4 norm limit / Gram / exact span | proof draft | SVD と head-tail 直交性 |
| nested 2+1 | open, not claimed | generalized-atom W が必要 |
| `(E-d)` / FR5–FR7 | open, not claimed | FR-S4 |

## 9. 版履歴

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
