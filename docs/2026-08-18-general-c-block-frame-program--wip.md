# 一般 c block-frame program (GC) — authoring document

日付: 2026-08-18 / 著者: 本線 / status: **wip(draft PR #178。検証は複数 LLM の
fixed-SHA 査読 + 数値診断のみ — 人間による査読は未実施。外部査読体制は現存しない)**

親文書: [閉包定理](2026-08-02-gaussian-border-rank-closure--wip.md)(§4.3.7 = router、
§10 台帳 G1′ 行が本 program の消費者)。c=3 資産:
[FR 文書](2026-08-10-three-atom-block-frame-preparation--wip.md)(全 packet accepted)、
[補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md)(R-W PASS `1b3e337`)。

## 1. 目的と非目的

**目的**: G1′(一般 c の補題 N 枠 = 閉包定理の主 blocker)を、c=3 で完結した FR 方式の
一般化で閉じる。**route 決定記録(2026-08-18)**: Sol consult #7 の推奨
「一般 FR 主軸 + Prepared Binary Kernel(PBK)層、c=4 pathfinder、GC-4 go/no-go」を
orange が採用(AskUserQuestion 確認済み)。執筆場所 = 本新文書 + closure §4.3.7 router
(accepted 済み c=3 FR 文書へは継ぎ足さない)。

**route の要点**:
- 純粋な「全節点 binary 化 + K2 拡張一本」は**不成立**(Sol 反例: 周波数微分 0, M, 2M の
  等間隔 3 点は「子内部幅 ≪ 子間 gap」の安定 2 分割層を持たない — 組合せ的 binary 化は
  常に可能だが解析的 binary 化は不可能な配置がある)。
- しかし多 block B2 一般形も回避できる: 非相殺原理を「**prepared child 同士の binary
  node kernel(PBK)**」へ縮小する。既知 base = `1|1`(K2)、`2|1`(QR5/RF)。
  **新規 gate = c=4 の `2|2` と `3|1`**。
- **go/no-go 規則**: GC-4A/4B(PBK-22/PBK-31)が blocking counterexample を受けた時点で
  本 route への投資を停止し、K_c 本体(B2+(F1)+S4 層別帰納、closure §4.3.5)へ戻る。

**非目的・非主張**: flat K_c(B2/S4)の閉鎖はここでは主張しない。一般 k の L2b/L3
(閉包文書側 NC 相当の一般化)は本 program の消費者だが別 packet。人間による査読は未実施。
D_W(c) の sharpness は主張しない(上界のみ消費)。

## 2. 三層アーキテクチャ(Sol consult #7)

- **Frame 層**: rate tree(深さ ≤ c−1)、compactified chart、J^{D_W(c)}-SVD、exact span、
  Gram、confluent/generalized limit。c=3 の FR-S1′/S1″ の一般化。
- **PBK 層(Prepared Binary Kernel)**: exact child functions A, B と child certificate を
  入力し、node envelope U_H = max(log|A|, log|B|) に対する composite unit-step kernel を
  返す。入力型は `(w_L, w_R, child certificate)` の一般形で固定し、instance として
  `1|1`=K2、`2|1`=QR5/RF(c=3 資産)、`2|2`・`3|1`(c=4 新規)を証明する。
  PBK の位相分離 case は**binary 化された B2** — B2 型非相殺原理はここに縮小されて残る。
- **Assembly 層**: public ledger は root step だけを一回積算し、child kernel cost は
  provenance に畳む(c=3 の M1/W3 原則、FR §10.8)。**T² budget の深さ重複消費の禁止**が
  本層の核心規約(リスク台帳 R2)。

## 3. 一般補題 W target(GC-1)

**上界(証明 target)**: p_j = A_j z²/2 + B_j z 相異、u_j = e^{p_j} に対し
u_j^{(r)} = e^{p_j} H_r(A_j z + B_j, A_j)、deg_z H_r ≤ r。よって
  Wr(u_1,…,u_c) = e^{Σp_j} V_c(z)、deg V_c ≤ C(c,2) = c(c−1)/2。
相異パラメタの entire 独立性から V_c ≢ 0。adapted valuation profile v_1 < ⋯ < v_c に
c=3 恒等式(補題 W 文書)の一般形 ord₀ Wr = Σv_i − C(c,2) を適用し、v_i ≥ i−1 と併せ
  **v_c ≤ D_W(c) := c(c+1)/2 − 1**(c=2: 2、c=3: 5 を再現。FR 文書 §7 の旧候補
  D(w) = (w−1)(w+2)/2 と同値)。
**記法**: D_W(c) は本 program が下流(J^{D_W(c)}-SVD 等)で消費する**証明対象の上界値**。
到達可能な sharp 最大値は D_W*(c) と書き分ける(D_W*(c) ≤ D_W(c)。D_W*(2)=2、D_W*(3)=5
は既知、c≥4 の値は非主張 — 下の診断は D_W*(4)=8 を示唆)。
GC-1 の受理条件: この勘定の自己完結証明(恒等式の一般 c 版・constant-gauge rank drop
込み・c=2/3 の復元)。

**sharpness(非主張・診断)**: 数値診断(scratchpad `wgen_static_contact.py`、Newton 探索、
スケールゲージ β₁=1 固定、各 120 初期点)では c=3: ord 5 到達・ord 6 解なし(補題 W と
整合 — 手法検証)、**c=4: ord 8 到達・ord 9/10 解なし**。moduli 勘定(ゲージ後 3(c−1)−1 =
3c−4 個)と一致し、sharp 値は D_W*(c) = 3c−4 < D_W(c)(c≥4)の可能性がある。下流は
上界 D_W(c) のみ消費するので、GC-1 は一般式 c(c+1)/2−1 で閉じてよい。**衝突極限でも valuation 5 は到達**
(FR 文書 F3′: 3 乗根配置 A_j = −B_j²、profile (0,1,5)、h_β/‖h_β‖ → z⁵/√5!)—
「静的接触のみの現象」ではない。

**confluent 昇格義務(GC-9)**: finite-m の plain W 上界だけでは衝突境界での一様 SVD floor
は出ない。一般 rate-tree face の generalized P e^q 系に対する confluent W(または
flat-limit jet injectivity)が別途必要 — c=3 で FR-S1″ が果たした役割の一般化。

### 3.1 補題 W_c(一般 valuation 上界 — drafted、査読対象 R-GC1)

**設定**: c ≥ 1、パラメタ対 ξ_j = (A_j, B_j) ∈ ℂ²(j = 1..c)は**相異**
(constant-gauge quotient 済み — 一致対は閉包文書 §4.3.6 N-pre の exact 合算で先に併合し、
併合後の本数を c と読む)。p_j(z) := A_j z²/2 + B_j z、u_j := e^{p_j}。|A_j| < 1 は本補題では
不要(純代数的 — 全て entire)。W := span{u_1, …, u_c}。

**statement(W_c)**: dim W = c であり、任意の z₀ ∈ ℂ と任意の f ∈ W∖{0} に対し
  ord_{z₀} f ≤ D_W(c) = c(c+1)/2 − 1(D_W の記法は §3 — 証明対象の上界値であり、
  sharp 最大値 D_W*(c) の決定は非主張)。
特に z₀ = 0 の adapted valuation profile v_1 < ⋯ < v_c は v_1 = 0、
Σᵢ v_i ≤ c(c−1)、v_c ≤ D_W(c) を満たす。c=2: D_W = 2、c=3: D_W = 5(既存
[補題 W](2026-08-11-three-atom-wronskian-valuation-W--wip.md) の (W2)(W3) と一致)。

**(W_c-1) 導関数の構造**: u_j^{(r)} = H_{r,j}(z)·u_j、H_{0,j} = 1、
H_{r+1,j} = H_{r,j}′ + (A_j z + B_j)H_{r,j}。帰納で deg H_{r,j} ≤ r。∎

**(W_c-2) Wronskian の因数分解**: Wr(u_1,…,u_c) = det(u_j^{(r)})_{r=0..c−1, j=1..c}
= e^{Σ_j p_j} · V_c(z)、V_c := det(H_{r,j})。行 r の各成分の次数 ≤ r なので、
det の多重線形展開の各項の次数 ≤ Σ_{r=0}^{c−1} r = C(c,2)。よって
**deg V_c ≤ C(c,2) = c(c−1)/2**。∎

**(W_c-3) 独立性と Wr ≢ 0**:
(i) *独立性*: 相異対の差 p_i − p_j は非定数(A_i = A_j なら B_i ≠ B_j で 1 次、
A_i ≠ A_j なら 2 次)。閉包文書 §2 の L0(指数多項式独立性 — accepted 資産、定数係数の
場合)より {u_j} は線形独立、dim W = c。
(ii) *解析的 Wronskian 判定(自己完結)*: entire な f_1,…,f_n が線形独立なら
Wr(f_1,…,f_n) ≢ 0。*帰納*: n = 1 自明。f_1,…,f_{n−1} が従属なら f_1,…,f_n も従属で
前提に反するから、f_1,…,f_{n−1} 独立、帰納法の仮定で Wr_{n−1} := Wr(f_1,…,f_{n−1}) ≢ 0。
Wr_n ≡ 0 と仮定する。U := {Wr_{n−1} ≠ 0} は非空開集合。**連結成分を一つ選び C ⊂ U と
する**。C 上で y ↦ Wr(f_1,…,f_{n−1}, y) = 0 は最高階係数 Wr_{n−1} ≠ 0 の (n−1) 階線形
ODE であり、f_1,…,f_{n−1} は C 上の解、かつ C 上でも線形独立(依存関係は一致の定理で
ℂ 全体へ延びるため)なので **C 上の解空間(次元 n−1)を張る**。Wr_n ≡ 0 より f_n も
C 上の解 ⇒ f_n = Σ aᵢfᵢ(定数係数、この成分 C 上)⇒ f_n − Σaᵢfᵢ は C(内点を持つ)で
消える entire 関数 ⇒ 一致の定理で ℂ 全体で 0 ⇒ 従属 — 矛盾(係数 aᵢ が別成分で異なり
得ることは問題にならない: 一つの成分で十分)。∎
(i)(ii) より Wr(u_1,…,u_c) ≢ 0、したがって **V_c ≢ 0** かつ
**ord₀ V_c ≤ deg V_c ≤ C(c,2)**。∎

**(W_c-4) valuation identity(一般 c 版)**: z = 0 の adapted basis を取る:
W の任意の基底の Taylor 係数行列を z-次数の昇順に行簡約すれば、先頭次数が相異なる基底
g_i = c_i z^{v_i} + O(z^{v_i+1})(c_i ≠ 0、v_1 < ⋯ < v_c)が得られる(pivot 次数の集合
= profile は基底の取り方に依らない)。**任意の f = Σ b_i g_i ∈ W∖{0} について
ord₀ f = min{v_i : b_i ≠ 0}** — 先頭項の次数 v_i は相異なので相殺しない。よって
f の valuation は必ず profile の値のいずれかである。基底変換で Wronskian は
非零定数倍しか変わらない。先頭項を代入すると falling-factorial 一般 Vandermonde により
  Wr(g_1,…,g_c) = (Π c_i)·Π_{i<j}(v_j − v_i)·z^{Σv_i − C(c,2)} + higher。
higher が先頭位数へ戻らないこと: det の多重線形展開において各項の位数は
「c 列の次数和 − C(c,2)」以上であり、いずれかの列を v_i より高次の Taylor 項に置き換えると
次数和は狭義に増える。次数が重複する組の determinant は零。よって表示した係数
(相異 v_i で非零)が最低位数に残り、
  **ord₀ Wr(u_1,…,u_c) = Σᵢ v_i − C(c,2)**。∎

**(W_c-5) 上界の組み立て**: (W_c-2)(W_c-3)(W_c-4) より
  Σᵢ v_i = C(c,2) + ord₀ V_c ≤ 2·C(c,2) = c(c−1)。
u_j(0) = 1 ≠ 0 より W の z=0 評価汎関数は非零で **v_1 = 0**。profile は非負整数の狭義増加列
なので v_i ≥ i−1、よって
  v_c ≤ c(c−1) − Σ_{i=1}^{c−1}(i−1) = c(c−1) − (c−1)(c−2)/2 = (c−1)(c+2)/2 = c(c+1)/2 − 1。
f ∈ W∖{0} の ord₀ f は profile の値のいずれか((W_c-4))なので ord₀ f ≤ v_c ≤ D_W(c)。∎

**(W_c-6) 任意中心**: 平行移動 z ↦ z + z₀ は
u_j(z + z₀) = e^{p_j(z₀)} · exp(A_j z²/2 + (A_j z₀ + B_j)z) と、同じ族(A 不変、
B ↦ B + A z₀、非零定数吸収)への写像。相異性は保たれる(A_i = A_j なら B 差不変、
A_i ≠ A_j はそのまま)。よって z₀ における valuation にも同じ上界。∎

**c=2/3 の復元**: c=2: D_W = 2(閉包文書 W2/K2 資産と整合)。c=3: D_W = 5 —
既存補題 W の (W1)〜(W3) はそれぞれ (W_c-2/3)、(W_c-4) の c=3 特殊化(既存文書は
V ≢ 0 を L0 非依存の場合分けで示しており、本補題の (W_c-3)(i) は L0 を引く — 依存は
より広いが L0 は accepted 資産であり循環はない)。F3′(FR 文書 §7)の profile (0,1,5) は
c=3 上界の到達例。∎

**scope(非主張)**: sharpness(§3 の 3c−4 診断は非主張)。衝突境界での一様 SVD floor
(confluent 版 — GC-9)。|A| < 1 での norm 評価。人間による査読は未実施。

## 4. GC packet 台帳(state は fail-closed)

| packet | 依存 | 出力・受理条件 | state |
|---|---|---|---|
| GC-0 consumer audit | なし | 一般 N/NC/L2b/L3 が必要とする外部 target の列挙。最終出力は (E-w) 形で足りるか、(E-d) 多項式形は内部需要のみかを決定 | **accepted**(R-GC0 R1 PASS、fixed SHA `b8167d1`、findings なし) |
| GC-1 W_c | GC-0 | D_W(c) ≤ c(c+1)/2−1 の自己完結証明(本文書 §3.1)。c=2/3 復元 | **drafted(§3.1、査読待ち R-GC1)** |
| GC-2 SPLIT4 | GC-0 | c=4 の全 tree topology・同時分裂の列挙。「安定 binary gap が常に存在」は反例つきで棄却または修正版を証明 | open |
| GC-3 PBK-SPEC | GC-1/2 | exact child・node envelope・reserve・uniform/graded cost・common-zero 規約の型付き interface(proof claim なし) | open |
| GC-4A PBK-22 | GC-3、c=2 資産 | `2|2` composite unit-step kernel。係数非依存・有限-m exact child・ray-wide cost 可算。**go/no-go 関門** | open |
| GC-4B PBK-31 | GC-3、c=3 FR | `3|1` kernel。c=3 child certificate を消費し、旧 U_F/SVD 係数へ戻らない。**go/no-go 関門** | open |
| GC-5 FR4-S1 | GC-1/2 | c=4 全 topology の exact J^{D_W(4)}-SVD frame、compact floor、tail、Gram | open |
| GC-6 ROUTE4 | GC-4A/B/5 | 全 unit interval がちょうど一つの resolved root route を持つ closed-world coverage | open |
| GC-7 ENV4/N4 | GC-6 | root-only assembly、T² budget、c=4 補題 N。**c=4 pathfinder 完結点** | open |
| GC-8 IND | GC-7 | 一般帰納の離散指標と定数 budget(leaf weight・support・valuation/flag の well-foundedness) | open |
| GC-9 CONFL | GC-8 | 全 rate-tree face の confluent injectivity、multi-scale exact factorization、tail | open |
| GC-10 PBK-IND | GC-4A/B/8/9 | (w_L, w_R) に関する prepared binary kernel 帰納 | open |
| GC-11 ASM | GC-10 | 全 tree の root-only route coverage と envelope assembly(child 二重積算なし) | open |
| GC-12 G1′ | GC-9/11 | 一般補題 N → NC → L2b/L3 → G1′ の接続監査(閉包文書側) | open |

工程見積り(Sol、2026-08-18): GC-0〜GC-4 go/no-go = 5–8 作業日、c=4 完結 = 2–3 週、
一般帰納込み全体 = fixed-SHA 査読込み 5–8 週。PBK 失敗で K_c 回帰なら +3–6 週。

## 5. GC-0 consumer audit(accepted — R-GC0 R1 PASS、fixed SHA `b8167d1`)

一般 c の枠(補題 N 一般版)を消費するのは閉包文書の次の 4 系統である。c≤3 の NC program
(閉包 §4.4.1、accepted)の依存構造を一般 c/一般 k に引き直す。

| 消費者 | 必要とする target(一般 c 版) | 形の決定 |
|---|---|---|
| 補題 N(一般 c)量化(閉包 §4.3.6 の一般化) | (N1) 部分列上の norm 収束(枠 → P_ℓΦ(ξ*)、deg P_ℓ ≤ D_W(c))/(N2) Gram 最小固有値の m 一様下界(部分列依存可)/(N3′) 元座標枠の遠方包絡/(N4) 定数の係数非依存(m₀ 存在のみ) | (N3′) は **(E-w) 形(exp((1−δ/2)|z|²/2 + C_lin(c)|z|))で足りる** — c=3 の実績と同型。多項式形 (E-d) は枠**内部**(再帰の子 certificate)にのみ現れ、外部 target ではない |
| L2a′(一般 c)束ね(NC-1 の一般化) | 反証部分列スキーム + (N3′)/(N4)。枠係数 ≤ λ^{−1/2}√r·S、log⁺ 分割 | (E-w) 形で足りる。D_W(c) = O(c²) の悪化は定数 C(c) に入るのみ(log⁺ 構造不変 — Sol 検討済み) |
| L2b/L3(一般 k)(NC-2/NC-3 の一般化) | cluster ごとの一般補題 N + G8(closed `dc76258`)+ L1-b。極限空間 V = span 導来原子、dim 保存(L0 + jet 独立性) | (N1)(N2) を直接消費(c≤3 と同型)。**cluster 数・cluster 内 c の合計 ≤ k で有限** — 帰納は c 単独でよい |
| 主定理 T / 系 C1(全 k) | T: 閉包(G_k) の指数多項式分類、deg P_c ≤ D_W(c)。C1: 半直線台 ∉ 閉包(G_k) ∀k | deg 上界は D_W(c) の**上界のみ**消費(sharp 不要)。C1 は実解析性のみ使うので次数値に非依存 |

**audit 帰結**:
1. **外部 target は (E-w) 形で閉じる**(c=3 と同じ弱形)。(E-d) 多項式形は PBK/Frame 層の
   内部 certificate 語彙としてのみ必要 — 外部 API に出さない。これにより NC 系の一般化は
   c≤3 の証明骨格の置換で済む見込み(量化スキーム不変)。
2. 系 C1(全 k)= 本 program 完結(GC-12)+ 既存 NC 骨格の一般 k 置換で従う —
   G6/G8 は closed 済みなので追加の G 条件は発生しない。
3. 工程上の含意: GC-1(一般 W)と GC-2(SPLIT4)は独立に着工可能。GC-0 の決定
   「外部 = (E-w)」により GC-7 の受理条件が固定される。

**非主張**: 本 audit は proof claim を含まない(依存グラフと形の決定のみ)。

## 6. 早期検証実験台帳

| 実験 | 潰す仮説 | 判定量 | state |
|---|---|---|---|
| W4-JET | D_W(4)=9 の sharpness / より強い bound | Newton 探索の nondegenerate ord 到達(スケールゲージ固定) | **初期結果あり**: c=4 で ord 8 到達・9/10 解なし(§3。診断 — 証明の代替ではない) |
| SPLIT-EQ | 「閾値移動で常に安定二分割できる」 | affine 周波数配置の cluster component 数と internal/cross gap 比 | open(GC-2 入力) |
| PBK22-ADV | prepared `2|2` kernel に有限指数がある | sup_I|H|/max(|A|,|B|) と J 側比の高精度最適化。**両 child が同一点で零になる fixture 必須**(c=3 の pair+singleton には無かった新境界) | open(GC-4A 入力) |
| RESONANCE-4 | 四原子の高次共鳴 | roots-of-unity 型配置で低次 jet を exact 消去し先頭非零次数を計算 | open(W4-JET と統合可) |
| CHART-SVD4 | rate chart の完備性 | `2+2`/`3+1`、s^α・e^{−1/s}・s log(1/s) 経路で factored σ_min が正に留まるか | open(GC-5 入力) |
| BUDGET-TREE | child cost の二重計上 | 全 c≤8 tree・route 列の Σlog C_step の T² 係数 | open(GC-11 入力) |

## 7. リスク台帳

| # | リスク | 順位 | 対処 |
|---|---|---|---|
| R1 | S4 型障害(tropical transition)が PBK `2|2`/`3|1` に再出現 | **本命** | PBK22-ADV/SPLIT-EQ を GC-4 着工前に回す。blocking 反例で K_c 回帰(go/no-go 規則) |
| R2 | tree depth による T² budget の重複消費 | 高 | Assembly 層の root-only 規約(§2)+ BUDGET-TREE で検証 |
| R3 | confluent chart の未記録 rate(F3 型 witness の一般形) | 中 | GC-9 の chart label に相対 valuation/flag を必須化(FR §7 の設計制約を継承) |
| R4 | 一般 W 不成立(valuation 爆発) | 低 | GC-1 の上界証明は次数勘定で閉じる見込み(§3)。数値は 3c−4 to 支持 |

## 8. 版履歴

- v0.3(2026-08-18): R-GC1 R1 findings 適用 — [GC1-01] D_W(上界値)/D_W*(sharp 最大値)の
  記法分離、[GC1-02] Wronskian 判定の連結成分明示、[GC1-03] adapted basis 構成と
  「ord f ∈ profile」の根拠追加、[GC1-04] §5 見出しの状態同期。
- v0.2(2026-08-18): GC-0 accepted(R-GC0 R1 PASS、fixed SHA `b8167d1`、findings なし)。
  §3.1 補題 W_c(GC-1)draft — 一般 valuation identity + Wronskian 次数勘定 +
  自己完結の解析的 Wronskian 判定。
- v0.1(2026-08-18): 新設。route 決定記録(Sol consult #7 + orange GO)、三層
  アーキテクチャ、GC-0〜GC-12 台帳、GC-0 consumer audit draft、W4-JET 初期結果、
  リスク台帳。
