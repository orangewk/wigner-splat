# 三原子 exact block-frame preparation (FR) — statement wip

日付: 2026-08-10 / 著者: 本線 / status: **specification only — v0.5.2、F3′ により旧次数帳簿を撤回、plain補題W R-W PASS、R-FRSPEC R5 pending、FR-S1′未証明**

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
constant-gauge quotient 後の基点について

  s_m := max_{i,j} d(ξ_{i,m},ξ_{j,m}) → 0、ξ_{j,m} → ξ*  (全 j)

を仮定する。s_m が 0 へ行かない別 cluster は入力前に分離し、L3/cluster tree の別節点で扱う。

leaf weight w=1 は再帰の終端とし、距離正規化を行わない。w≥2 の active cluster node では、
normalized distance d(ξ_{i,m},ξ_{j,m})/s_m を部分列で全対収束させる。極限 0 の pair は
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
Wronskian 補題 W の執筆・固定 SHA 査読後に採否を決める。一般 `w` の候補
`D(w)=(w−1)(w+2)/2`、nested 2+1 への拡張、FR5–FR7 はここでは主張しない。

## 8. 版履歴

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
