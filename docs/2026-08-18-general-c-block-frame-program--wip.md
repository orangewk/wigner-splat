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
- **go/no-go 規則(v0.11.1 改訂 — 二段階化)**: (第一次)**最小判定集合 =
  {GC-4A.0, A.1, A.2, A.3, GC-4B.0, GC-4C.0}**(§4 台帳)。この集合のいずれかが blocking
  counterexample を受けた時点で本 route への投資を停止し、K_c 本体(closure §4.3.5)へ
  戻る。最小集合の全受理は「**次段へ進む判定**」であり route 成功の宣言ではない。
  (第二次・fail-closed 継続)**それ以降の GC-4 系 packet(A.4–A.6、B 本体、C 本体)の
  いずれかが blocking counterexample を受けた場合も同じ撤退規則が発動する** — route 成功は
  GC-4 全 packet + GC-6 coverage の受理まで宣言しない。(履歴: v0.1 = GC-4A/4B、
  v0.5 = GC-4C 追加、v0.11 = 最小集合、v0.11.1 = 二段階化で「go 確定」表現を撤回。)

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

### 3.1 補題 W_c(一般 valuation 上界 — accepted、R-GC1 R3 PASS、fixed SHA `957b252`)

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
| GC-1 W_c | GC-0 | v_c ≤ D_W(c) = c(c+1)/2−1 の自己完結証明(本文書 §3.1)。c=2/3 復元 | **accepted**(R-GC1 R3 PASS、fixed SHA `957b252`) |
| GC-2 SPLIT4 | GC-0 | c=4 の全 tree topology・同時分裂の列挙。「安定 binary gap が常に存在」は反例つきで棄却または修正版を証明 | **accepted**(R-GC2 R3 PASS、fixed SHA `5bbf183`) |
| GC-3 PBK-SPEC | GC-1/2 | exact child・node envelope・reserve・uniform/graded cost・common-zero 規約の型付き interface(proof claim なし) | **accepted**(R-GC3 R4 PASS、fixed SHA `dc6cac9`) |
| GC-4A.0 PBK22-BRF | GC-3 | simultaneous RECENTER・共通 cell cover・bi-graded ray ledger(held 自動性の正式棄却と graded held 化 — consult #8)。**go/no-go 最小集合** | open |
| GC-4A.1 PBK22-F2 | A.0 | held cell 上の double F2、case (a)/(b)/(c) 骨格、divisor/common-zero stratification。**go/no-go 最小集合** | open |
| GC-4A.2 PBK22-JF9 | A.1 | W_c と log-ratio jet の quantitative bridge(次数予算 9 − d_common、全 compact boundary face)。**最大の go/no-go packet** | open |
| GC-4A.3 PBK22-P4 | A.2 | two-sided SN(numerator/denominator/common-zero)、zero-free tube、10 階上界。**go/no-go 最小集合** | open |
| GC-4A.4 PBK22-WE9 | A.2/A.3 | 局所窓外挿(JF9/P4 の純 consumer) | open |
| GC-4A.5 PBK22-BOOT | A.4 | branch bootstrap、初回のみ ρ⁻⁹ の chain ledger | open |
| GC-4A.6 PBK22-ASM | A.5 | 全場合合成・最終 γ・cost spec・GCRouteSpec 昇格・fail-closed tests | open |
| GC-4B.0 ADAPT31 | GC-3、c=3 FR | triple divisor adapter の feasibility(chart 付き Weierstrass certificate — 接触次数 ≤ 5 だけでは足りず collar 内総零点数/valency が必要。**供給源 2 系統(prepared tree triple / radial 混成 3 原子和)の両方を scope に含む** — GC-4C.0 (3) 表。失敗は 3|1 の重大 no-go 信号)。**go/no-go 最小集合** | open |
| GC-4B PBK-31 | B.0、GC-4A 系 | `3|1` kernel 本体。c=3 child certificate を消費し、旧 U_F/SVD 係数へ戻らない | open |
| GC-4C.0 SIG-AUDIT | GC-2/3 | q-ary radial signature の完全列挙(12)・A/B dispatch 可否・irreducible endpoint 特定・transition 有界性。**go/no-go 最小集合** | **drafted(§8.1、査読待ち R-GC4C0)** |
| GC-4C PBK-M4 | C.0、GC-4A/B | 多分岐 node kernel 本体(`[4]` held + separated compact + dispatch 接続) | open |
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

## 6. GC-2 SPLIT4(c=4 tree topology と node 分割二分法 — accepted、R-GC2 R3 PASS、fixed SHA `5bbf183`)

**入力規約**: 共通 gauge 後の weighted metric d_w = max(|ΔA|^{1/2}, |ΔB|)(FR 文書 §2 —
snowflake 三角不等式で metric)。constant-gauge quotient 済み(重複原子は exact 合算、
w = 残存本数 ≤ 4)、有限 m では原子は相異。**注**: FR §2 は c=3 で「各 active node の
非零 pair-distance ratio が正の下限を持つ」を規約として置いたが、本節ではこれを仮定せず
**補題 SPLIT4 が生入力列から木を構成して導出する**(規約から結論への循環を避ける)。

### 6.1 c=4 tree topology の完全列挙

再帰定義(T(1) = leaf、T(2) = {(1|1)}、T(3) = {(1|1|1), (2|1)})より、w=4 の cluster tree
shape は置換を除いて次の **5 種**:

| # | shape | 深さ | 内部 node 全列挙(個数) |
|---|---|---|---|
| T1 | (1\|1\|1\|1) | 1 | root(arity 4)— 計 1 |
| T2 | (2\|1\|1) | 2 | root(arity 3)+ pair node(1\|1)— 計 2 |
| T3 | (2\|2) | 2 | root(arity 2)+ pair node(1\|1)× **2** — 計 3 |
| T4 | ((1\|1\|1)\|1) | 2 | root(arity 2)+ triple node(1\|1\|1)— 計 2 |
| T5 | ((2\|1)\|1) | 3 | root(arity 2)+ triple node(2\|1)+ pair node(1\|1)— 計 3 |

c=3 の「single-scale triple または 2+1、深さ ≤ 2」(FR §2)の一般化。深さ ≤ 3 = c−1 ✓。

### 6.2 node 型の在庫と kernel 義務クラス

各 topology の内部 node を「children の型(prepared block の重み)」で分類する:

| node 型 | 出現箇所 | kernel 義務 | 資産状態 |
|---|---|---|---|
| 1\|1 | T2/T3/T5 の pair node(T3 は 2 個) | K2 | c=2 資産(accepted) |
| 2\|1 | T5 の triple node | c=3 **nested FR program 複合**(FR-S1″ 枠 + S4 route: QR5/RF/K2 の chart routing)— 単一 kernel ではなく child 準備 certificate として消費 | c=3 資産(accepted) |
| 1\|1\|1 | T4 の triple node | c=3 **plain FR program 複合**(FR-S1′ 枠 + S4 route — RF の一次記述は binary root `2|1` であり、**単独の 3-ary kernel は c=3 資産に存在しない**。plain triple は one-transition chart の pair 形成を経由する S4 複合で処理された) | c=3 資産(accepted、複合として) |
| **2\|2** | T3 root | **新規(binary PBK)** | GC-4A |
| **3\|1** | T4/T5 root(triple = prepared) | **新規(binary PBK)** | GC-4B |
| **2\|1\|1** | T2 root(3 block、うち 1 つ prepared) | **新規(多分岐)** | GC-4C(本 packet で新設) |
| **1\|1\|1\|1** | T1 root(4 singleton) | **新規(4 項。c=3 plain と同様の chart routing 複合になる見込み — 設計は GC-3)** | GC-4C |

**帰結(正直な在庫)**: c=4 の新規 kernel 義務は Sol consult の binary 2 種(`2|2`/`3|1`)
に**多分岐 2 種(`2|1|1`/`1|1|1|1`)が加わる**。多分岐側の設計出発点は「c=3 plain triple が
単独 3-ary kernel なしに chart routing 複合で閉じた」前例の w=4 拡張であり、GC-4C として
台帳に追加した。go/no-go 判定は GC-4A/B/C のいずれかの blocking 反例で発動(§1 の
改訂規則)。

### 6.3 「安定 binary gap」の棄却と修正版二分法

**反例(棄却)**: node の children 位置(周波数勾配)x = (0, M, 2M)(等間隔)では、
**閾値(区間)binary 分割**は {0}|{M,2M}(gap M / 内部幅 M)と {0,M}|{2M}(同)の 2 通り
のみで、cross-gap / max(内部幅)は**いずれも = 1**(最大値 1)— split-scale Taylor の
小パラメタが存在しない(Sol consult #7。kernel 分割は周波数順序を respect する閾値分割に
限る)。さらに interleaved pair 型 x = (0, a, 1, 1+a)(a ≈ 0.62)では最良の閾値分割でも
同比 ≈ **0.62 < 1**、ランダム c=4 配置の約 61% で同比 < 2(数値診断: scratchpad
`split_eq.py` — 診断であり証明の代替ではない)。よって「解析的 binary 分割が常に存在」は
**偽**。

**修正版(補題 SPLIT4 — 生入力からの木構成)**: constant-gauge quotient 済みの衝突
入力列 {ξ_{j,m}}(有限 m で相異、残存本数 w)。**w=1 は leaf(木・scale とも不要)、
w=2/3 は c≤3 の既知 shape(FR §2: (1|1)、(1|1|1)/(2|1))へ dispatch — 以下 w=4 の場合を
述べる**。全体 scale s_m := max_{i,j} d_w(ξ_{i,m}, ξ_{j,m}) とする。部分列が存在して
次が同時に成立する:
(i) 正規化距離 r_{ij,m} := d_w(ξ_{i,m}, ξ_{j,m})/s_m ∈ [0,1] が全対で収束し、
関係 i ~ j :⟺ lim r_{ij,m} = 0 は同値関係。同値類を root の children とし、
サイズ ≥ 2 の類には類内 scale(類内 max 距離)で同じ構成を再帰すると、**木が構成され**、
その shape は §6.1 の 5 種のいずれか(pivot permutation 込みで固定)。
(ii) 構成上、各 node の相異 children 間の正規化距離の極限は正 ⇒ **下限 η > 0**
(有限個の対、η は部分列依存)。すなわちスケール分離(比 → 0)は全て木の辺に吸収され、
node は常に **comparable-gap 多分岐** — 「node 内 binary スケール分割」は構成の後には
存在しない。
(iii) node 内の周波数勾配クラスタリングが必要な場面(radial kernel 適用時)では、
子数 q ∈ {2,3,4} の各 node に対し **Q ≥ 2 を固定し、M* := 16、B := qQ(補題 G を
c = q で適用)** と選べば補題 G(閉包文書 §4.3.5.1、乗法窓鳩ノ巣 — 証明済み資産)の
前提(M* ≥ 16、Q ≥ 2、B = cQ)が各 q ≤ 4 で満たされ、閾値 M₀ ∈ [M*B, M*B^q] で
クラスタ内径 ≤ M₀/Q・クラスタ間隙 ≥ M₀ を同時に確保できる(binary ではなく
**多分岐クラスタ分割**が正しい原始操作。適用位置 x_j = θ′_j(t₀))。

*証明*: (i) **部分列抽出は有限回の入れ子で行う**(深さ ≤ 3・node 数 ≤ 3(§6.1 表)・
各 node の対数 ≤ 6 なので、抽出は有限回 — 対角線法は不要)。手順: (step-1) root で
s_m を実現する対は m ごとに変わり得るが、対は有限個(≤ 6)なので鳩ノ巣で、ある固定対
(i₀,j₀) が無限回最大を実現する部分列を取る(以後 r_{i₀j₀,m} = 1)。(step-2) 同部分列上で
r_{ij,m} ∈ [0,1] の全対収束を Bolzano–Weierstrass(有限対の逐次抽出)で確保。~ の推移性:
d_w は metric(FR §2 — snowflake 三角不等式)なので r_{ik,m} ≤ r_{ij,m} + r_{jk,m} → 0。
root で類が 1 つに潰れないこと: r_{i₀j₀,m} = 1 ↛ 0 より i₀ ≁ j₀ ⇒ 類は ≥ 2 個。
(step-3) サイズ ≥ 2 の各類(≤ 3 本)について、**現在の部分列の上でさらに**類内 scale
s^{(ν)}_m(類内 max 距離 — 有限 m では正)への正規化距離に (step-1)(step-2) を繰り返す。
繰り返し回数は node 数 ≤ 3 で有界なので全 node に共通の部分列が有限回で得られる。
各類のサイズは真に減る(root で ≥ 2 分割)ので再帰は深さ ≤ 3 で終端し、到達可能な
shape は「サイズ 4 の ≥2 分割 × 各部分の再帰形」= §6.1 の 5 種で尽きる。shape・pivot
permutation は有限個なので最後に部分列で固定。(ii) 各 node で相異 children i ≁ j の
定義より lim r_{ij} > 0。全 node の正極限の最小値を η_* とし、**η := η_*/2** と置けば、
ある m₁ 以降の全 m で正規化距離 ≥ η(有限個の収束列なので m₁ は一様に取れる)。
(iii) は補題 G の前提充足の確認のみ(上記の q ごとの選択で直接)。∎

**FR §2 との整合**: c=3 で FR §2 が規約として置いた「非零 pair-distance ratio の正下限」は、
本補題 (ii) の c=3 特殊化として**導出**される(規約は構成の出力を先取りしていた —
循環はない)。

**scope(非主張)**: 本補題は分割の**構造**のみを与える。各 node kernel の存在
(GC-4A/B/C)、(E-w) 包絡、Gram floor は別 packet。radial kernel 側のクラスタ幅と
node scale の整合(補題 G の window と d_w-tree の window の突き合わせ)は GC-3
(PBK-SPEC)の interface 設計に送る。人間による査読は未実施。

## 7. GC-3 PBK-SPEC(prepared node kernel の型付き interface — accepted、R-GC3 R4 PASS、fixed SHA `dc6cac9`。proof claim なし)

本節は仕様であり証明主張を含まない。c=3 の FR-S4-0(FR 文書 §10 — accepted)の契約群を
w=4 の node 在庫(§6.2)へ拡張する。**継承原則**: FR §10.3(two-level segmentation・
(S4-step-u/w)・acceptance 条件 1–8)、§10.4(RouteKind/RouteRecord・source_ref・
cost spec・A_ledger_kind・FR7 許可語彙)、§10.5(exact zero-pruning・RouteSpec 唯一
authoring 原則)、§10.6(coefficient-free constants)は**逐語で継承**し、本節は
**closed-world の差分 enum・差分型のみ**を新設する。FR 側 enum の既存 entry・row は
一切変更しない。

**記法の分離(同名異型の解消)**: FR の `η := q₂ − q₁`(exact exponent difference)は
そのまま。SPLIT4 (ii) の正規化距離下限(accepted §6.3 で η と書いた量 — 本文は不変)は
**本節以後 `η_dw` と表記**する(異なる対象の同名衝突を避ける)。区間対は FR の `(I_k, J_k, ε_chain)` を用い、本 spec 独自の記号
(旧 draft の (E,I)・ρ)は廃止する。

### 7.1 GC 拡張 enum(closed-world)

FR の enum への追加 entry を次で固定する(追加のみ — 既存 entry 不変):

  GCCategoryEnum := CategoryEnum ∪ {PBK-22-w, PBK-31-w, PBK-M-w}
  GCMissingObligationEnum := MissingObligationEnum ∪ {M-PBK-22, M-PBK-31, M-PBK-M}
  GCDomainSchemaEnum := DomainSchemaEnum ∪ {D-PBK-22, D-PBK-31, D-PBK-M}
  GCArityEnum := {unary, binary, ternary, quaternary}(FR の expected_arity を拡張)

**現時点の registry 状態(fail-closed)**: 新設 3 category は全て
`unresolved(route_id, expected_arity, missing_obligation_id)` として登録される
(PBK-22-w: binary/M-PBK-22、PBK-31-w: binary/M-PBK-31、PBK-M-w:
ternary または quaternary/M-PBK-M)。**resolved 化(RouteSpec 行の新設 — mode・
cost spec・γ・κ̄・inequality・source_ref の確定)は GC-4A/B/C の受理と同時にのみ行う**。
それまで S4b-α 相当の registry closure は成立せず、GC-6(ROUTE4)へ進めない —
FR §10.3 acceptance 条件 7 の継承。cost spec の新 variant が必要になる場合
(graded-root の PBK 版等)も、GC-4 受理時に本節を先に改訂してから使う
(FR §10.4「RouteSpec 表が唯一の authoring location」原則の継承)。

**GC 側 authoring 構造(FR 側不変と両立する新設)**:
- **GCRouteSpec 表**(新設 3 category の唯一の authoring location — FR §10.5 表は不変。
  列定義は FR RouteSpec と同一。**現時点で resolved 行は 0 行** — 行の追加は GC-4A/B/C の
  受理と同時にのみ行い、それ以外の方法での resolved 化を禁止する):

  | route_id | arity | mode | domain schema | cost spec | γ | κ̄ | inequality | source rule | assembly rule |
  |---|---|---|---|---|---|---|---|---|---|
  | *(resolved 行なし — GC-4A/B/C 受理待ち)* | | | | | | | | | |

- **GCRouteRecord**: FR §10.4 RouteRecord の全 field を継承し、次の差分を持つ拡張型:
  (a) `node_functions` は arity で判別 — unary `(H)` / binary `(A,B)` / ternary `(A,B,C)` /
  quaternary `(A,B,C,D)`(全て exact 関数)、(b) `reserve_witness`(§7.4)、
  (c) `deep_vanishing_witness`(§7.3 — 条件付き必須 field。条件と検証規則は §7.3 で固定)。
- **GCCoverageManifest** := `(GCCategoryEnum, entries)`: 各 category が
  resolved/unresolved/excluded の**ちょうど一つ**として現れる(FR §10.4 の
  registry-level manifest 規則を GC enum に適用)。ray ごとの interval 被覆は
  FR §10.5.5 `RayCoverageManifest` 形式を GC-6 で instantiate する。

**domain schema の required keys**(witness 型は FR §10.4 の規約に従い式または
identity ref、自由文禁止。各 schema の key set を完全列挙する):

| schema | required keys(完全列挙) |
|---|---|
| `D-PBK-22` | `active_children_nonzero`、`certificate_ref(C_1)`(w=2 variant)、`certificate_ref(C_2)`(w=2 variant)、`nonconstant(q_{C_1} − q_{C_2})`(child 代表指数の exact 差 — constant-gauge quotient witness)、collision-scale witness `(|ΔA| ≤ s_m², |ΔB| ≤ s_m)`、`η_dw` witness(SPLIT4 (ii) の m₁・η_dw 値)、補題 G window witness `(Q, M₀, q=2)` |
| `D-PBK-31` | `active_children_nonzero`、`certificate_ref(C_1)`(w=3 variant: triple-plain または triple-nested)、`certificate_ref(C_2)`(w=1 atom)、`nonconstant(q_{C_1} − q_{C_2})`、collision-scale witness `(|ΔA| ≤ s_m², |ΔB| ≤ s_m)`、`η_dw` witness(SPLIT4 (ii) の m₁・η_dw 値)、補題 G window witness `(Q, M₀, q=2)` |
| `D-PBK-M` | `arity ∈ {ternary, quaternary}`、`active_children_nonzero`、全 child の `certificate_ref`(ternary: w 型 (2,1,1)、quaternary: w 型 (1,1,1,1))、**全 pair (i,j) の** `nonconstant(q_{C_i} − q_{C_j})`、collision-scale witness `(|ΔA| ≤ s_m², |ΔB| ≤ s_m)`、`η_dw` witness(SPLIT4 (ii) の m₁・η_dw 値)、補題 G window witness `(Q, M₀, q = arity)` |

**zero-pruning の継承(明示)**: 任意の child が恒等零(`C_i ≡ 0`)なら削除し、残る
exact span で rank・tree を再固定して lower-arity/lower-w へ redispatch する(§10.5 継承。
tree 再固定は SPLIT4 の再適用)。active node は全 child が `C_i ≢ 0` かつ有限 m で
`‖C_i‖ > 0` — witness `active_children_nonzero` を必須 field とする。

### 7.2 ChildCertificate 型(実在資産と 1:1)

`Child` は `w(C) ∈ {1,2,3}` の discriminated union。**exact 有限原子結合のみ**
(`P e^q` は衝突極限の chart face であり child の型ではない — Sol consult #7 の規約化)。

各 variant の field と source_ref(**FR §10.4 の external/intrinsic 5 要素 tuple
`(kernel_name, canonical_file, anchor, fixed_SHA, PASS)` で 1:1 に指定** — 効力は各
canonical 文書の現行 status ledger に当該 SHA の acceptance 記録が存在する場合に限る):

| variant | fields(全て必須) | source_ref(5 要素 tuple) |
|---|---|---|
| `atom`(w=1) | 係数非零 witness、gauge 後パラメタ | certificate 不要 |
| `pair`(w=2) | divided-difference 0–2 jet frame ref、強形 envelope `(1+t)² E_{δ,R} ‖C‖`(C₂(R))ref、`‖C‖ > 0`、`m₀`、相対 valuation label | jet frame = `(N-P3-pair-frame, docs/2026-08-02-gaussian-border-rank-closure--wip.md, §4.3.6.3, f86acae, PASS)`; 強形 = `(W2, docs/2026-08-10-three-atom-block-frame-preparation--wip.md, 補題 W2(§10.8), a0fcd10, PASS)`; kernel 用 = `(K2, docs/2026-08-08-quadratic-phase-turan-K2.md, 主定理, eb1804a, PASS)`。**J^{D_W(2)}-SVD certificate ではない** — 実在するのは jet frame + 強形包絡 |
| `triple-plain`(w=3) | FR-S1′ 正規化枠(SVD floor = Gram floor を含む)ref、(S4-Ew)/N3′/N4 acceptance ref、chart label(相対 valuation/flag — F3 制約)、`m₀` | 枠 = `(FR-S1′, docs/2026-08-10-three-atom-block-frame-preparation--wip.md, §8, ed25401, PASS)`; envelope/N3′/N4 = `(FR-S4c, 同文書, §10.9, b6bbe01, PASS)` |
| `triple-nested`(w=3) | FR-S1″ `(ν̂,t)`-chart 枠(SVD floor 込み)ref、(S4-Ew)/N3′/N4 acceptance ref、chart label、`m₀` | 枠 = `(FR-S1″, 同文書, §9, 61111cc, PASS)`; envelope/N3′/N4 = `(FR-S4c, 同文書, §10.9, b6bbe01, PASS)` |

**provenance 分離(FR7 継承・fail-closed)**: certificate の内部量(`1/t_m`、SVD 係数、
raw 原子係数、旧 `U_F`、旧 DC discount)は **internal provenance にのみ**現れてよく、
kernel の最終出力・global comparison の入力には使えない。合成式に現れてよい量は
FR §10.4 の許可列挙 {RootStep provenance fields, node functions, U_H, compact-class
envelope, Fock norm, named constants} に **{child certificate の named constants
(有限個の実定数として named_constants 経由)}** を加えた集合に限る(未列挙 identifier の
追加は本節の先行改訂を要する)。`certificate constants` は各 variant の field 列挙に
現れる ref の定数のみ — 無制限の定数持ち込みは禁止。

### 7.3 node envelope と common-zero 規約

- `U_H := max_i log|C_i|`(**q-ary 拡張** — FR §10.4 の binary 定義
  `U_H = max(log|A|, log|B|)` の一般化。これは差分定義であり FR 側の binary 定義は不変。
  零点では log 0 := −∞)。unweighted の `A_{H,k}` 定義も同形で継承。
- **common-zero 規約(c=4 新規 — PBK22-ADV fixture)**: **訂正された前提**: c=3 の
  root 2+1 で存在した床は「accepted C0 の terminal window `I_N ⊂ [0,2]` における相対的
  下界」であり一般的・一様な床ではない(旧 draft の「c=3 では床が自動」は不正確 —
  撤回)。`2|2` 以降は全 children が同一点で同時に零になり得る。契約(typed field と検証規則):
  **`deep_vanishing_witness := (t₀, {ord_i, lead_i}_{i≤q}, σ_dv, switch_witness_id)`** —
  (a) `t₀ ∈ I_k`: 同時深消滅の中心。(b) `ord_i`: child C_i の t₀ における消滅次数、
  検証規則 `ord_i ≤ D_W(w_i)`(child ごと — node 全体の `D_W(4) = 9` と区別。GC-1 消費)。
  (c) `lead_i`: C_i の t₀ での先頭係数(次数 `ord_i` の Taylor 係数)の**非零 witness** —
  下界は `certificate_ref(C_i)` の named constants から供給し、raw 係数の直接持ち込みは
  禁止(§7.2 provenance 分離)。(d) `σ_dv`: 切替閾値 — record は
  `sup_{I_k}|C_i| ≤ σ_dv · (certificate envelope 値)` が**全 i** で成立する場合に限り
  深消滅 record として有効(そうでない区間は通常 route)。(e) `switch_witness_id ∈
  GCSwitchWitnessEnum := {SW-DEEP-VANISH}`(closed enum — 他値は fail-close で
  `uncertified`)。**結合規則**: `deep_vanishing_witness` は 3 schema(D-PBK-22/31/M)
  全てで**条件付き必須** — 条件 (d) が成立する interval の record では必須、不成立なら
  field 自体を置かない(placeholder 禁止)。**この区間で必要になる Remez 型評価は GC-1 が
  供給しない**(GC-1 は valuation 上界のみ)— 当該評価は GC-4A/B/C の証明義務であり、
  PBK22-ADV 実験(§8 — 未実施)がその feasibility 入力である。no-return 継承。

### 7.4 cost の位置づけと reserve

**graded cost 参考表(spec ではない — 非主張の target 注記)**: 既知値は
`1|1`: γ=2(K2)、`2|1` root: γ=5(QR5-w/root-far)。新設 3 category の γ は**未定**で、
RouteSpec 行の新設(= GC-4 受理)まで台帳に値を置かない(γ₂₂ ≥ 5 の「見込み」は §9
リスク台帳の情報であり spec ではない)。

**reserve(typed witness として新設)**: GC 版 RouteRecord は FR §10.4 RouteRecord の
全 field に **`reserve_witness := (node_path, taylor_scope = child-split-scale,
remainder_bound_ref)`** を追加した拡張型とする(FR RouteRecord 自体への field 追加では
ない — GC 側の拡張 record)。意味: split-scale Taylor の剰余評価は child の split scale
までしか使わない(長区間剰余の回避)。設計出所は閉包 §4.3.5.3 の Sol 案 1 —
**historical design 参照であり active proof ではない**(受理済み reserve 実装は
FR §10.8 の W1/C0/W3 + root-only assembly が正)。**public ledger は root step 一回のみ**
(FR §10.3 acceptance 条件 6 の継承。T² budget の深さ重複消費の禁止 — 検証は
BUDGET-TREE 実験 + GC-11)。

### 7.5 非主張

kernel の存在(新設 category の resolved 化・γ の有限性・深消滅区間の Remez 型評価)は
本 spec では主張しない — GC-4A/B/C の証明対象であり、blocking 反例が出れば §1 の
go/no-go 規則が発動する。(E-w) 包絡の組み立て(GC-7)、confluent 枠(GC-9)も範囲外。
本節の enum 拡張は FR 文書の accepted 面を変更しない(FR 側 enum・RouteSpec 行は不変)。
人間による査読は未実施。

## 8. GC-4 packet 本文

**設計記録(Sol consult #8、2026-08-18)**: GC-4A の単一 packet 化は不可(一 packet
一 claim の cadence 違反 + QR5 で実際に循環が発生した箇所の分離)。分解 = §4 台帳の
A.0–A.6 / B.0 / C.0。骨格: simultaneous RECENTER/cell 化 → double F2 → two-sided
divisor stratification → quantitative JF₉ → two-sided P4 → WE₉/bootstrap。
**held 自動性は棄却済み**(反例 AUTO-HELD-22: s_m = m⁻¹、pair 内部 scale m⁻²、
q₂ − q₁ = m⁻⁴t²/2 は t_c = m⁴ 付近の単位区間で recenter 後も sup ≈ 1/2 > 1/8 —
木構成と両立。c=3 の root-far と同機構)。修復 = bi-RF: Λ_{i,k} := sup_{I_k}|η_i′|、
共通 cell cover 上で両 pair を独立に exact RECENTER、cost は
log C_step,k ≲ 1 + Λ_{1,k} + Λ_{2,k}、ray-wide は Σ_k Λ_{i,k} ≲ s_i² T² + s_i T。

### 8.1 GC-4C.0 SIG-AUDIT(q-ary radial signature coverage — drafted、査読対象 R-GC4C0)

**目的**: GC-4C(多分岐 node)の設計監査。radial 周波数クラスタ signature の完全列挙、
GC-4A/B への dispatch 条件の固定、irreducible endpoint の特定、transition 有界性。
**proof claim は (1) の margin 安定性と (5) の初等計数のみ** — kernel の存在は主張しない。

**記号**(本節と A.0 で共用。GCRouteRecord への型付き組み込みは A.0 の spec 改訂で行う):
node の children blocks C_1..C_q(重み w_i、Σw_i ≤ 4)。s_i := child C_i の内部
collision scale。η 系: 各 child 内部の exact exponent 差(pair child なら η_i =
q_{i,2} − q_{i,1})。Λ_{i,k} := sup_{I_k}|η_i′|。x_j(t) := Im q_j′(t) = **原子** j の
radial 周波数勾配(block でなく原子ごと — 集約は (2))。

**(1) signature の完全列挙と margin 安定性**: cell 上で原子勾配の weak ordering を固定
([GC4C0-07] 対応: x_i ≡ x_j の tie は index 順で決定的に破る)。補題 G を cell 中心
t₀ で適用すると、隣接 gap(順序付き原子 4 個で 3 個)は t₀ で **< L = M₀/B か ≥ M₀ の
二択**(補題 G の乗法窓性質 — 中間帯 [L, M₀) の gap は存在しない)。raw signature :=
cut(≥ M₀)部分集合 = **2^{4−1} = 8 通り**(原子レベルで統一 — 節点 arity 依存の
「12」勘定は撤回し、q=3 節点も原子 4 個の signature で読む)。**margin 安定性(証明)**:
区間上の勾配 drift は |x_j(t) − x_j(t₀)| ≤ 2·|t − t₀| ≤ 2(class 正規化 |Im q″| ≤ 2、
単位 cell)なので gap の drift ≤ 4。M₀ ≥ M*B ≥ 16·8 = 128 より
L + 4 = M₀/B + 4 < M₀/2 < M₀ − 8 — cut/uncut の二分類は区間全体で分離を保ち
(internal ≤ M₀/Q + 4、cross ≥ M₀ − 8 ≥ M₀/2)、中間帯への漂着は起きない。∎
([GC4C0-01] 対応 — signature は t₀ で定義し margin で区間へ延ばす。)

**(2) 重み付き集約**: signature は原子集合の順序付き分割を与える。各 group は原子の
exact 部分和(tree child と一致するとは限らない — 混成可)。**outcome 型 = group の
原子数 multiset**: [4]、3|1、2|2、2|1|1、1|1|1|1 の **5 型**。group の内部構造
(prepared tree child を丸ごと含む/混成)は route ID でなく **witness**(ordering・
cut 部分集合・帰属表)に持たせる。

**(3) dispatch 表(条件の固定 — 可否の証明はしない)**:

| outcome 型 | dispatch 先 | 条件・注記 |
|---|---|---|
| 2\|2 | GC-4A | 両 group とも「tree pair と一致」の場合が主経路(certificate 供給可)。**一致は RECENTER 後の値-held witness(sup|η̃| ≤ 1/8 — FR の held は値条件であり勾配条件ではない。[GC4C0-06])が成立する cell に限る** ⇒ dispatch は GC-4A.0(bi-RF held 化)の成立に条件付く。混成 2\|2 の group は K2 型 exact pair として扱う |
| 3\|1 | GC-4B | 「3」= prepared tree triple(certificate 供給)または radial 混成 3 原子和(certificate なし — c=3 kernel 資産で内部処理)。**GC-4B.0 の adapter は両供給源を scope に含む必要**(本監査で B.0 の受理条件へ追記) |
| [4] | GC-4C 本体 | 全原子 comparable — held endpoint。内部構造 {2,2}/{3,1}/{2,1,1}/{1,1,1,1} は witness |
| 2\|1\|1 | GC-4C 本体 | **irreducible 多分岐 endpoint**(§6.2 のとおり GC-4C — [GC4C0-02] 対応で復元) |
| 1\|1\|1\|1 | GC-4C 本体 | 全 gap ≥ M₀ − 8。乗法窓により gap 比有界 ⇒ 再スケールでコンパクト族(縮小の証明は GC-4C 本体の義務) |

**深消滅床の供給源の訂正([GC4C0-03])**: W_c(GC-1)が供給するのは **ord の上界**のみ
であり、GC-3 §7.3 の `lead_i` 非零**下界**や Remez 型評価は供給**しない**。混成 group
(certificate なし)の深消滅 record に必要な quantitative lead 下界は**現時点で供給源が
存在しない open obligation** であり、GC-4A.1/A.2 が新規 interface として author する
(その際 GC-3 §7.3 の供給源規定の改訂を先行させる — FR「spec を先に改訂してから使う」
原則)。本監査はこの gap を隠さず記録する。

**(4) irreducible endpoint**: GC-4C 本体の証明対象 = **[4](held endpoint)・2|1|1・
1|1|1|1 の 3 型**(2|2 → A、3|1 → B)。1|1|1|1 は「B2 多 block 一般形」の
「コンパクト族非相殺(S3/Łojasiewicz 型)」への縮小候補 — 縮小の証明自体は GC-4C 本体の
義務であり本監査は主張しない。

**(5) transition 有界性(証明)**: x_j(t) は affine(class 正規化 |Im q_j″| ≤ 2 —
閉包 §4.3.4)。単位区間上: (i) weak ordering の交差 — 相異なる affine 2 本は高々 1 回
交わる(恒等一致は tie-break で単一関数扱い)ので交差 ≤ C(4,2) = 6。(ii) gap 閾値横断 —
x_i − x_j は affine なので |x_i − x_j| は折れ点 ≤ 1 の区分 affine、水平線 M₀ を高々
2 回横断、計 ≤ 12。∴ signature/ordering event の分割は **≤ 19 cell**。
**勘定の位置づけ([GC4C0-04])**: 19 は signature event のみの分割数である。kernel が
実際に使う cell 系は「signature 分割 × 両 pair の RF held 分割」の**共通細分**であり、
区間分割の細分は breakpoint の和で押さえられるので
  N_cell,k ≤ 18 + (4 + 8Λ_{1,k}) + (4 + 8Λ_{2,k}) + 1 = 27 + 8(Λ_{1,k} + Λ_{2,k})
の **graded 形**になる。FR §10.3 条件 2(graded 側: N_cell,k ≤ C_cell(1+Λ) + ray-wide
ledger)の充足検証は **GC-4A.0 の義務**であり本監査は主張しない — 本監査が確定するのは
「signature 起因の因子は一様(≤ 19)で、graded 性は bi-RF 側からのみ入る」という
分離まで。M4-MULTITRANSITION(無限/非有界 transition)は棄却。∎

**(6) 帰結**: GC-4C 本体の義務 = [4] held + 2|1|1 + separated compact(1|1|1|1)+
(A.0 条件付き)dispatch 接続。8 signature は (1) で網羅・margin 安定、集約 5 型の
dispatch は (3) 表で固定、transition は (5) で有限 cell 化。**scope(非主張)**:
kernel の存在・γ・compact 族非相殺・FR 条件 2 充足・深消滅 lead 下界の供給。
人間による査読は未実施。

## 9. 早期検証実験台帳

| 実験 | 潰す仮説 | 判定量 | state |
|---|---|---|---|
| W4-JET | D_W(4)=9 の sharpness / より強い bound | Newton 探索の nondegenerate ord 到達(スケールゲージ固定) | **初期結果あり**: c=4 で ord 8 到達・9/10 解なし(§3。診断 — 証明の代替ではない) |
| SPLIT-EQ | 「閾値移動で常に安定二分割できる」 | affine 周波数配置の cluster component 数と internal/cross gap 比 | **初期結果あり**(`split_eq.py`: 等間隔で比 = 1、interleaved で ≈ 0.62 — §6.3 が消費。診断) |
| PBK22-ADV | prepared `2|2` kernel に有限指数がある | sup_I|H|/max(|A|,|B|) と J 側比の高精度最適化。**両 child が同一点で零になる fixture 必須**(c=3 の pair+singleton には無かった新境界) | **初期結果あり**(`pbk22_adv.py`: ord-8 共鳴配置 2 例で全 2\|2 分割の子 block は ord 0(co-vanish せず)⇒ weighted 指数 = 8。子 co-vanish は指数を 8−ord(child) へ**下げる**(ord F ≤ D_W*(4) は分割に依らないため)⇒ 指数の本命 = D_W*(4) = 8、安全予算 = D_W(4) = 9。QR5(γ=5=D_W*(3))と同型 — 診断であり証明の代替ではない) |
| RESONANCE-4 | 四原子の高次共鳴 | roots-of-unity 型配置で低次 jet を exact 消去し先頭非零次数を計算 | **W4-JET に統合済み**(ord-8 到達配置 = 4 原子共鳴の実例。診断) |
| CHART-SVD4 | rate chart の完備性 | `2+2`/`3+1`、s^α・e^{−1/s}・s log(1/s) 経路で factored σ_min が正に留まるか | open(GC-5 入力) |
| BUDGET-TREE | child cost の二重計上 | 全 c≤8 tree・route 列の Σlog C_step の T² 係数 | open(GC-11 入力) |
| AUTO-HELD-22 | 「T3 の pair children は node scale で自動 held」 | 反例構成 | **棄却済み**(正本 = §8 設計記録) |
| COMMON-DIVISOR | 両 pair が同一点同次数消滅 + reduced 先頭も相殺で deep-flat が残る | exact 構成と reduced pair の挙動 | open(A.1/A.3 入力) |
| JF-NONCOMPACT | ord F ≤ 9 でも正規化 log jet の最小値が confluent 境界で 0 へ落ちる列 | 正規化列の jet floor 数値 | open(A.2 の主敵) |
| COLLAR-POLE | 実区間で unit 有界でも分母複素零点が collar に接近する列 | V_i の複素零点距離 | open(A.3 入力) |
| TRIPLE-VALENCY | 接触次数 ≤ 5 でも collar 内に 6 個以上の零点を持つ triple | 零点計数 | open(B.0 の主敵) |
| GRADED-BUDGET-DOUBLE | bi-RF cost Λ₁+Λ₂ の provenance/root 二重計上 | ledger 監査 | open(A.0/GC-11 入力) |

## 10. リスク台帳

| # | リスク | 順位 | 対処 |
|---|---|---|---|
| R1 | S4 型障害(tropical transition)が PBK `2|2`/`3|1` に再出現 | **本命** | PBK22-ADV/SPLIT-EQ を GC-4 着工前に回す。blocking 反例で K_c 回帰(go/no-go 規則) |
| R2 | tree depth による T² budget の重複消費 | 高 | Assembly 層の root-only 規約(§2)+ BUDGET-TREE で検証 |
| R3 | confluent chart の未記録 rate(F3 型 witness の一般形) | 中 | GC-9 の chart label に相対 valuation/flag を必須化(FR §7 の設計制約を継承) |
| R4 | 一般 W 不成立(valuation 爆発) | 低 | GC-1 の上界証明は次数勘定で閉じる見込み(§3)。数値は 3c−4 to 支持 |

## 11. 版履歴

- v0.11.1(2026-08-18): R-GC4C0 R1 findings(blocking 6 + minor 2)適用 — [01] signature を
  t₀ 定義 + margin 安定性証明へ、[02] 原子レベル 8 signature に統一・2|1|1 を GC-4C
  endpoint に復元・dispatch 完全表・B.0 の供給源 2 系統化、[03] W_c は ord 上界のみで
  lead 下界は open obligation と訂正(A.1/A.2 + GC-3 改訂先行)、[04] 19 cell と bi-RF
  graded 細分の分離(共通細分の graded 勘定、FR 条件 2 は A.0 義務)、[05] go/no-go の
  二段階化(「go 確定」撤回)、[06] held = 値条件・RECENTER 後 dispatch と記号定義、
  [07] tie-break、[08] AUTO-HELD-22 の正本一元化。

- v0.11(2026-08-18): consult #8(Sol — GC-4 証明設計)を反映: GC-4 を A.0–A.6/B.0/C.0 に
  分解(§4 台帳)、go/no-go 最小集合 = {A.0–A.3, B.0, C.0}(§1 改訂)、§8 設計記録
  (held 自動性の棄却 AUTO-HELD-22 + bi-RF 修復)、§8.1 GC-4C.0 SIG-AUDIT draft
  (12 signature 列挙、dispatch 条件固定、irreducible endpoint、transition 有界性の計数
  証明)、実験台帳に反例仮説 6 本追加。

- v0.10(2026-08-18): GC-3 accepted(R-GC3 R4 PASS、fixed SHA `dc6cac9`)。次 = PBK22-ADV
  実験(GC-4A feasibility 入力)→ GC-4A/B/C。

- v0.9.1(2026-08-18): R-GC3 R3 findings 適用 — [GC3R3-01] D-PBK-31/M の collision-scale
  witness を明記(「同上」全廃)、[GC3R3-02] GCRouteSpec 表を列定義付きで実体化
  (resolved 0 行、追加は GC-4 受理と同時のみ)。
- v0.9(2026-08-18): R-GC3 R2 findings(3 blocking)適用 — [GC3R2-01] GC 側 authoring
  構造の新設(GCRouteSpec 表 = §7.1 唯一 authoring、GCRouteRecord の arity 判別
  node_functions、GCCoverageManifest)、[GC3R2-02] ChildCertificate source_ref を
  5 要素 tuple で実在資産 1:1 に(N-P3 `f86acae`、W2 `a0fcd10`、K2 `eb1804a`、
  FR-S1′ `ed25401`、FR-S1″ `61111cc`、FR-S4c `b6bbe01`)、[GC3R2-03] D-PBK-31/M の
  key 完全列挙 + deep_vanishing_witness の型・検証規則・schema 結合・closed enum。
- v0.8(2026-08-18): R-GC3 R1 findings(8 blocking)適用 — §7 を closed-world 型拡張へ
  全面書き直し: [GC3-01] GC 拡張 enum(GCCategoryEnum/GCArityEnum 等、新設 3 category は
  unresolved 登録)、[GC3-02] 記法分離(η_dw)と FR の (I_k,J_k,ε_chain) への統一、
  [GC3-03] ChildCertificate を実在資産と 1:1 の variant 表に(K2/W2 は jet frame +
  強形包絡 — J^d-SVD ではない)、[GC3-04] provenance 分離の fail-closed 化、
  [GC3-05] zero-pruning 継承の明示、[GC3-06] 床の前提訂正(C0 terminal window 相対下界)+
  deep_vanishing_witness 型 + D_W(w_i)/D_W(4) 区別 + Remez は GC-4 義務、
  [GC3-07] reserve_witness 型新設(§4.3.5.3 は historical 参照に降格、正は FR §10.8)、
  [GC3-08] 許可語彙の fail-closed 列挙。
- v0.7(2026-08-18): GC-2 accepted(R-GC2 R3 PASS、fixed SHA `5bbf183`)。§7 GC-3
  PBK-SPEC draft — PBKNode/Child/PBKResult 型、node envelope と common-zero 規約
  (同時零点は valuation 床 + 深消滅区間の単離)、graded cost 台帳(γ 値は GC-4 の
  証明対象)、reserve 契約(root-only public step)。
- v0.6(2026-08-18): R-GC2 R2 findings 適用 — [GC2R2-01] w ≤ 3 の dispatch を statement に
  明記(5 topology は w=4 限定)、[GC2R2-02] 有限入れ子部分列抽出(最大実現対の鳩ノ巣 +
  逐次 BW + node 数有界)を証明に明示、[GC2R2-03] η := η_*/2 と m₁ 一様性、
  [GC2R2-04] 補題 G を node 子数 q ごとに c=q で適用(B = qQ)。
- v0.5(2026-08-18): R-GC2 R1 findings 適用 — [GC2-01] `1|1|1`/`2|1` の資産帰属を
  「c=3 FR program 複合(単独 3-ary kernel は存在しない)」に訂正、[GC2-02] go/no-go
  規則を GC-4A/B/C に統一(§1 改訂)、[GC2-03] 補題 SPLIT4 を生入力からの木構成に
  書き直し(正下限は導出、FR §2 規約との整合注記)、[GC2-04] 補題 G の前提充足
  (M*=16、Q≥2、B=cQ)を明示、[GC2-05] 等間隔反例を閾値分割に限定し最大値 1 に訂正、
  [GC2-06] topology 表に内部 node 全列挙(個数)を追加。
- v0.4(2026-08-18): GC-1 accepted(R-GC1 R3 PASS、fixed SHA `957b252`)。§6 GC-2 SPLIT4
  draft — c=4 topology 5 種の列挙、node 型在庫(新規 kernel 義務 `2|2`/`3|1` +
  多分岐 `2|1|1`/`1|1|1|1` — GC-4C 新設)、安定 binary gap の棄却(SPLIT-EQ)と
  修正版二分法(補題 SPLIT4 — スケール分離は木の辺、node は comparable-gap 多分岐)。
- v0.3(2026-08-18): R-GC1 R1 findings 適用 — [GC1-01] D_W(上界値)/D_W*(sharp 最大値)の
  記法分離、[GC1-02] Wronskian 判定の連結成分明示、[GC1-03] adapted basis 構成と
  「ord f ∈ profile」の根拠追加、[GC1-04] §5 見出しの状態同期。
- v0.2(2026-08-18): GC-0 accepted(R-GC0 R1 PASS、fixed SHA `b8167d1`、findings なし)。
  §3.1 補題 W_c(GC-1)draft — 一般 valuation identity + Wronskian 次数勘定 +
  自己完結の解析的 Wronskian 判定。
- v0.1(2026-08-18): 新設。route 決定記録(Sol consult #7 + orange GO)、三層
  アーキテクチャ、GC-0〜GC-12 台帳、GC-0 consumer audit draft、W4-JET 初期結果、
  リスク台帳。
