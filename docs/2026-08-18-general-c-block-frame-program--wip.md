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
| GC-4A.0 PBK22-BRF | GC-3 | simultaneous RECENTER・共通 cell cover・bi-graded ray ledger(held 自動性の正式棄却と graded held 化 — consult #8)。**go/no-go 最小集合** | **accepted**(R-GC4A0 R4 PASS、fixed SHA `742c96a`) |
| GC-4A.1 PBK22-F2 | A.0 | held cell 上の double F2、case (a)/(b)/(c) 骨格、divisor/common-zero stratification。**go/no-go 最小集合** | **accepted**(R-GC4A1 R2 PASS、fixed SHA `50a4e45`) |
| GC-4A.2a JF9-EXACT | A.1 | exact bridge(p = T₂u、v = u − p、Φ_p := B₁ + e^p B₂、ord Φ_p ≥ d₀ + N + 1)、d₀ := ord_{t₀}D と N = 9 − d₀ の予算(**次数でなく局所消滅次数** — consult #9 訂正)、二次比枝(v ≡ 0 → deg≤2 route)の分岐、jet の exact recurrence。**go/no-go 最小集合** | **accepted**(R-GC4A2A R2 PASS、fixed SHA `5bb69af`) |
| GC-4A.3a PBK22-ZF | A.1 | reduced zero-free collar(numerator/denominator/common-zero)のみ先行(A.2 への循環依存を解消 — QR5 の P4 collar 部と同配置)。10 階上界は非主張。**go/no-go 最小集合** | **accepted**(R-GC4A3A R2 PASS、fixed SHA `926093c`) |
| GC-4A.2b JF9-NORM | A.2a/A.3a | **有限 chart atlas 方式(consult #10 で v1 の大域 X̄ 路線を撤回)**: merge-first 前処理、ChartSpec 8 家族、決定的 selector + 部分列網羅性補題、chart-local κ_C、chart 別 exact jet map、confluent prefactor 次数 gate | **accepted(R-GC4A2B R9 ACCEPTED、fixed SHA `a2302f3` — v1 大域路線の撤回から R2–R8 の 8 round を経て受理。8 責務 8/8)** |
| GC-4A.2c CONFL22 | A.2b | 床の証明: 各 terminal chart の inf > 0(W_c(r)/QR5 明示計算/**W_CONFL(2,2) v2: deg ≤ 2・sharp 目標 B_CONFL = 6(消去法必須 — crude Wronskian 不可、失敗は no-go 信号。deg ≤ 1 部分形は 4)**/principal-part・gcd)、交差 face の transverse 単射性、overlap 比較から c_J = min c_C/K_C > 0。**最大の go/no-go packet** | open |
| GC-4A.3b PBK22-D10 | A.3a/A.2b | 10 階上界・scale cap(WE₉ の純入力) | open |
| GC-4A.4 PBK22-WE9 | A.2/A.3 | 局所窓外挿(JF9/P4 の純 consumer) | open |
| GC-4A.5 PBK22-BOOT | A.4 | branch bootstrap、初回のみ ρ⁻⁹ の chain ledger | open |
| GC-4A.6 PBK22-ASM | A.5 | 全場合合成・最終 γ・cost spec・GCRouteSpec 昇格・fail-closed tests | open |
| GC-4B.0 ADAPT31 | GC-3、c=3 FR | triple divisor adapter の feasibility(chart 付き Weierstrass certificate — 接触次数 ≤ 5 だけでは足りず collar 内総零点数/valency が必要。**供給源 2 系統(prepared tree triple / radial 混成 3 原子和)の両方を scope に含む** — GC-4C.0 (3) 表。失敗は 3|1 の重大 no-go 信号)。**go/no-go 最小集合** | open |
| GC-4B PBK-31 | B.0、GC-4A 系 | `3|1` kernel 本体。c=3 child certificate を消費し、旧 U_F/SVD 係数へ戻らない | open |
| GC-4C.0 SIG-AUDIT | GC-2/3 | 原子レベル radial signature の完全列挙(8)・margin 安定性・A/B/C dispatch 表・irreducible endpoint 特定・transition 有界性。**go/no-go 最小集合** | **accepted**(R-GC4C0 R3 PASS、fixed SHA `aa95124`) |
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

**設計記録(Sol consult #9、2026-08-18 — JF₉ の target 修正)**: 生の JF₉
(max_{3≤n≤9}|u⁽ⁿ⁾|/(κλⁿ) ≥ c_J、λ = pair 成分 max)は**偽** — 反例 =
**二次比枝**: B₁ = −e^{Q(t)}B₂(Q 二次。例: η = ε²t、Q = εt — 真正な階層的 2|2・
held・collar 付きで u = Q ⇒ u⁽ⁿ⁾ = 0(n ≥ 3))。**route no-go ではなく分岐不足**。
修正 target(A.2a/c の受理形): **p := T₂u、v := u − p として「v ≡ 0(二次比枝 —
deg≤2 Chebyshev/Remez route へ)または max_{3≤n≤9−d₀}|v⁽ⁿ⁾(t₀)|/(κλⁿ) ≥ c_J**」。
κ = 二次比 locus からの adapted 横断残差、λ = Φ_p := B₁ + e^p B₂ の 4 位相の共通
gauge 後 weighted 座標 max(F2 分解の成分別正規化は人工特異面を作るため禁止 —
child log は log(e^{z_i}−1) に再結合)。橋: v の 0..N 消滅 ⇒ ord Φ_p ≥ d₀ + N + 1
(Φ_p = D e^p C₂(1 − e^v))⇒ N = 9 − d₀ で ord ≥ 10 ⇒ 真正 4 原子面では W_c(4) に
矛盾。**confluent 面(正規化極限が P e^q 型 — 例 z_ε = ε(1+t): E → 1・零点 collar 外・
(e^{z_ε}−1)/ε → 1+t)は主境界として残り、plain W_c では閉じない** ⇒ 限定版
**W_CONFL(2,2)** が A.2c の新義務(s_i → 0 が入力なので内部衝突は例外でなく主経路)。
退化極限の三分岐: exact merge → W_c(c′<4)(有利)/ Φ_p ≡ 0 → 二次比枝 /
P e^q → W_CONFL。A.2/A.3 は循環(JF が collar を仮定・collar が A.2 に依存)のため
**A.2a / A.3a / A.2b / A.2c / A.3b に再分解**(§4 台帳 v0.15)。

**設計記録(Sol consult #8、2026-08-18)**: GC-4A の単一 packet 化は不可(一 packet
一 claim の cadence 違反 + QR5 で実際に循環が発生した箇所の分離)。分解 = §4 台帳の
A.0–A.6 / B.0 / C.0。骨格: simultaneous RECENTER/cell 化 → double F2 → two-sided
divisor stratification → quantitative JF₉ → two-sided P4 → WE₉/bootstrap。
**held 自動性は棄却済み**(反例 AUTO-HELD-22: s_m = m⁻¹、pair 内部 scale m⁻²、
q₂ − q₁ = m⁻⁴t²/2 は t_c = m⁴ 付近の単位区間で recenter 後も sup ≈ 1/2 > 1/8 —
木構成と両立。c=3 の root-far と同機構)。修復 = bi-RF: Λ_{i,k} := sup_{I_k}|η_i′|、
共通 cell cover 上で両 pair を独立に exact RECENTER、cost は
log C_step,k ≲ 1 + Λ_{1,k} + Λ_{2,k}、ray-wide は Σ_k Λ_{i,k} ≲ s_i² T² + s_i T。

### 8.1 GC-4C.0 SIG-AUDIT(q-ary radial signature coverage — accepted、R-GC4C0 R3 PASS、fixed SHA `aa95124`)

**目的**: GC-4C(多分岐 node)の設計監査。radial 周波数クラスタ signature の完全列挙、
GC-4A/B への dispatch 条件の固定、irreducible endpoint の特定、transition 有界性。
**proof claim は (1) の margin 安定性と (5) の初等計数のみ** — kernel の存在は主張しない。

**記号**(本節と A.0 で共用。GCRouteRecord への型付き組み込みは A.0 の spec 改訂で行う):
node の children blocks C_1..C_q(重み w_i、Σw_i ≤ 4)。s_i := child C_i の内部
collision scale。η 系: 各 child 内部の exact exponent 差(pair child なら η_i =
q_{i,2} − q_{i,1})。Λ_{i,k} := sup_{I_k}|η_i′|。x_j(t) := Im q_j′(t) = **原子** j の
radial 周波数勾配(block でなく原子ごと — 集約は (2))。
**η̃_i := η_i − η_i(t_c)**(cell 中心 t_c での RECENTER 後の exponent 差 — FR の
`η^C(t) = η(t) − η(t_c)` と同一対象。held witness は sup_cell|η̃_i| ≤ 1/8 の値条件)。

**(1) signature の完全列挙と margin 安定性**: cell 上で原子勾配の weak ordering を固定
([GC4C0-07] 対応: tie-break は **(a) 恒等一致 x_i ≡ x_j は index 順で単一関数扱い、
(b) 孤立交差点 x_i(t*) = x_j(t*) では t* を cell 境界に採り、境界点の帰属は左閉右開
規約 + index 順、**で決定的に固定)。補題 G を cell 中心
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
| 2\|2 | GC-4A | 両 group とも「tree pair と一致」の場合が主経路(certificate 供給可)。**一致は RECENTER 後の値-held witness(sup_cell|η̃_i| ≤ 1/8、η̃ は本節冒頭の定義 — FR の held は値条件であり勾配条件ではない。[GC4C0-06])が両 pair で成立する cell に限る** ⇒ dispatch は GC-4A.0(bi-RF held 化)の成立に条件付く。混成 2\|2 の group は K2 型 exact pair として扱う |
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

### 8.2 GC-4A.0 PBK22-BRF(bi-RF: simultaneous RECENTER と graded cell ledger — accepted、R-GC4A0 R4 PASS、fixed SHA `742c96a`)

**目的**: AUTO-HELD-22(§8 設計記録 — held 自動性の反例)の正式修復。2|2 node の
両 pair を同時に held 化する cell cover の構成、bi-graded cost 勘定、ray-wide ledger、
および必要な spec 追補(§8.2.5)。**kernel 不等式そのものは主張しない**(A.1 以降)。

**設定**: T3 node、exact children B_1(原子 1,2)・B_2(原子 3,4)。η_i = pair i の
exact exponent 差。**s_i := child B_i の内部 collision scale**(pair 内 d_w 距離の最大値 —
child ごとに定義)とし、**pair 別 collision witness |ΔB_i| ≤ s_i、|ΔA_i| ≤ s_i²** を
用いる(ΔA_i, ΔB_i は **§6 の共通 gauge 後の parameter 座標**での pair i 内差分 —
[GC4A0R2-03] 対応。D-PBK-22 の従来 key は全体 s_m のみだったため、§8.2.5 で schema へ
`child_collision_witness_i` を追加する — [GC4A0-03] 対応)。
ray z = te^{iθ}、区間系 I_k = [a_k, a_k+1](FR §10.3 S4b-β を逐語継承)、
Λ_{i,k} := sup_{I_k}|η_i′|。η̃_i は §8.1 の定義(cell 中心 recenter 後)。
**入力仮定(閾値の非空性の根拠 — [GC4A0R3-03])**: 入力は GC-2 SPLIT4 の衝突列
(全体 scale s_m → 0)であり、proper child cluster の内部 scale は
s_i ≤ s_m · (正規化距離比 → 0) → 0(SPLIT4 (i) の child 形成の定義)。よって
**s_i(m) → 0** が入力から従い、以下の eventual 閾値 m_BRF0/m_BRF1 は非空。

**(BRF-1) 勾配の明示評価**: radial 制限で η_i(t) = ΔB_i e^{iθ} t + ΔA_i e^{2iθ} t²/2
なので η_i′(t) = ΔB_i e^{iθ} + ΔA_i e^{2iθ} t、よって
  Λ_{i,k} ≤ s_i + s_i²(a_k + 1)、  |η_i″| = |ΔA_i| ≤ s_i²。∎

**(BRF-2) held 化 cell cover**: m_BRF0 := min{M : ∀m ≥ M, max_i s_i(m)² ≤ 1/16}(eventual 量化 — [GC4A0-02]。§6.3 の SPLIT4 閾値 m₁ とは別記号 — [GC4A0R2-05])とし m ≥ m_BRF0。
h_k := min(1, 1/(16Λ_{1,k}), 1/(16Λ_{2,k})) と置き、I_k を長さ ≤ h_k の半開 cell に
等分割(左閉右開、境界帰属は §8.1 の規約)。cell 数は
  N^{RF}_{cell,k} ≤ ⌈1/h_k⌉ ≤ 1 + 16(Λ_{1,k} + Λ_{2,k})。
各 cell の中心 t_c で**両 pair を独立に exact RECENTER**(FR §10.5 の RECENTER(C,t_c) を
pair ごとに適用 — e^{η_i(t_c)} を係数へ吸収する exact transition。損失なし)。
**held 検証**: cell 上 |t − t_c| ≤ h_k/2 なので
  sup_cell|η̃_i| ≤ Λ_{i,k}·(h_k/2) + |η_i″|·(h_k/2)²/2 ≤ 1/32 + s_i²/8 ≤ 1/32 + 1/128 < 1/8。
よって各 cell で両 pair とも値-held(§8.1 dispatch 表の witness が成立)。∎

**(BRF-3) 共通細分の graded 勘定**: kernel が使う cell 系 = signature 分割(§8.1(5)、
breakpoint ≤ 18)と本節 RF 分割の共通細分。breakpoint の和より
  N_{cell,k} ≤ 19 + 16(Λ_{1,k} + Λ_{2,k}) ≤ 19·(1 + Λ_{1,k} + Λ_{2,k})
— **graded 形 N_{cell,k} ≤ C_cell(1 + Λ_{1,k} + Λ_{2,k})、C_cell = 19**。∎
(FR §10.3 条件 2 の graded 側の N_cell 要件はこの形で供給する。条件 2 の**完全充足**
(RF-2/RF-3 型の局所・大域 ledger を含む)の最終検証は cost spec が resolved 行に載る
A.6 の義務 — 本 packet は勘定の supply のみ。)

**(BRF-4) ray-wide ledger**: N ≤ 2T + 1、a_k + 1 ≤ T(FR §10.3 の区間系)と (BRF-1) より
  Σ_{k∈K_T} Λ_{i,k} ≤ s_i·(2T+1) + s_i²·T·(2T+1) ≤ 3(s_i T + s_i² T²)  (T ≥ 3)。
よって Σ_k N_{cell,k} ≤ 19(2T+1) + 3·16·Σ_i(s_i T + s_i² T²) — **一次項 O(T) +
collision-scale 減衰つき二次項 O(s²T²)**。∎

**(BRF-5) budget 吸収**: (E-w) 系の組み立て(GC-7)が消費する指数予算に対し、
ray-wide の log 総 cost は bi-graded template より
  Σ_k log C_step,k ≤ C_BRF·Σ_k(1 + Λ_{1,k} + Λ_{2,k}) ≤ C_BRF[(2T+1) + 3Σ_i(s_iT + s_i²T²)]
((BRF-4))。その二次成分は **C_led := 3·C_BRF**(bi-graded template 定数から導出、
0 < C_led < ∞ — [GC4A0R2-04])を用いて ≤ C_led·Σ_{i=1}^{2} s_i²T²。これは pair 数 2 を
織り込んだ閾値
m_BRF1 := min{M : ∀m ≥ M, max_i s_i(m)² ≤ δ/(32 C_led)}([GC4A0-01][GC4A0-02] 対応)以降
  C_led·Σ_i s_i²T² ≤ 2·C_led·(δ/(32C_led))·T² = δT²/16
に吸収され、(E-w) の指数 (1−δ/2)T²/2 + δT²/16 ≤ (1−δ/4)T²/2 を保つ
((1−δ/2)/2 + δ/16 ≤ (1−δ/4)/2 ⟺ δ/16 ≤ δ/8 ✓)。m_BRF := max(m_BRF0, m_BRF1) の
存在のみ要求(N4 量化と整合 — c=3 の m̃_RF と同型)。∎

#### 8.2.5 spec 追補(§7 への packet 発行改訂 — GC-3 の authoring 原則に従う。
本追補は §7 の closed-world schema への**明示的結合**であり、accepted 本文は不変)

- **GCCostSpecEnum の新設(closed-world)**: `GCCostSpecEnum := CostSpecEnum ∪
  {bi-graded}`(FR の CostSpecEnum = {uniform, graded-root} は不変)。
  `bi-graded(C_BRF, (Λ_{1,k}, Λ_{2,k}), N_cell,k, ray_ledger_ref)` —
  **0 < C_BRF < ∞ の interval-independent template**([GC4A0R3-02]。FR の
  uniform/graded-root と同じ正値性拘束)。各 record が両 Λ を instantiation し
  log C_step,k ≤ C_BRF(1 + Λ_{1,k} + Λ_{2,k})。
  **PBK-22-w 専用**(他 route への流用禁止 — graded-root の規律を継承)。
  ray_ledger_ref は (BRF-4) 型の ray-wide 上界の accepted ref を必須とする
  (局所値のみでの (E-w) 進行を禁止)。GCRouteSpec 表(§7.1)の cost spec 列は以後
  GCCostSpecEnum から取る(resolved 行新設時 — 現在 0 行のまま)。
- **versioned schema extension(accepted §7.1 は逐語凍結 — [GC4A0R3-01] 対応)**:
  新 schema ID を closed-world で追加する:
  `GCDomainSchemaEnum-v2 := GCDomainSchemaEnum ∪ {D-PBK-22v2, D-PBK-31v2, D-PBK-Mv2}`。
  各 v2 schema の required keys := **対応する v1 schema の全 key(§7.1 の accepted 表を
  逐語参照)+ `child_collision_witness_i`(全非 atom child i)**。
  `child_collision_witness_i := (s_i, {(|A_u − A_v| ≤ s_i², |B_u − B_v| ≤ s_i)}_{u<v ∈ J_i})`
  — J_i = child C_i の内部原子集合(w_i = |J_i| ≥ 2)、
  **s_i := max_{u<v ∈ J_i} d_w(ξ_u, ξ_v)**(child 内部 d_w 最大距離)、差分は
  **§6 の共通 gauge 後の parameter 座標**で取る(d_w = max(|ΔA|^{1/2}, |ΔB|) ≤ s_i ⟺
  |ΔA| ≤ s_i² かつ |ΔB| ≤ s_i)。w_i = 2 は対 1 組、w_i = 3 は全 3 組を列挙
  ([GC4A0R2-02] — 一般形)。**GCRouteSpec の resolved 行(GC-4 受理時に新設)は
  domain schema 列に v2 ID を用いる** — v1 ID は歴史的参照として凍結され、record 生成には
  以後使わない(fail-closed: v1 での record 生成を禁止)。
- **GCRouteRecord への field 追加**: `recenter_witness :=
  { cell_id ↦ (cell 端点(左閉右開), t_c(cell), exact transition ref(pair 1),
  exact transition ref(pair 2), sup_cell|η̃_1| ≤ 1/8 の式 witness,
  sup_cell|η̃_2| ≤ 1/8 の式 witness) }` — **interval 内の全 cell を走る有限 map 型**
  ([GC4A0-04] 対応。record は interval 単位、witness は cell 粒度)。
- **二重計上禁止(GRADED-BUDGET-DOUBLE 対応)**: bi-RF cost は root ledger の
  N_cell/step_cost にのみ現れる。child certificate は cost を持たない(frame 層の
  データであり、kernel cost の供給源に使わない)。

**scope(非主張)**: kernel 不等式(A.1–A.3)、深消滅 lead 下界(A.1/A.2 — §8.1 (3) の
open obligation)、FR §10.3 条件 2 の完全充足(A.6)、(E-w) 組み立て(GC-7)。
人間による査読は未実施。

### 8.3 GC-4A.1 PBK22-F2(double F2・対称正規化・case 骨格・divisor 層別 — accepted、R-GC4A1 R2 PASS、fixed SHA `50a4e45`)

**設定**: §8.2 の出力(m ≥ m_BRF、held 化 cell cover — 各 cell で両 pair とも
sup|η̃_i| ≤ 1/8)。F = B₁ + B₂、U_H = max(log|B₁|, log|B₂|)。区間対 (I_k, J_k)、
ρ := ε_chain(FR §10.3)。zero-pruning 済み(B_i ≢ 0 — §7.1 継承)。

**(F2²-1) double F2(cell ごと)**: 各 cell 上で held なので補題 F2(K2p1 §2 —
accepted 資産)を各 pair に適用でき、
  B_i = P_i(t) · V_i(t) · e^{r_i(t)}  (cell 上)
を得る。branch は pair ごと独立に D1/D2(P_i = 定数、|V_i| ∈ [0.84, 1.16])または
D3(P_i = 真正 deg ≤ 2 多項式で **P_i の零点 = B_i の零点**、|V_i| ∈ [0.27, 3.5])。
r_i = 基準二次位相。branch 判別(ν_i = Re w_i の三分岐)は cell witness に記録。∎
(F2 の前提 β ≤ 1/8 は A.0 の held witness がそのまま供給する。)

**(F2²-2) 対称正規化と g の定義([GC4A1-01] 対応)**: B₂ ≢ 0 より H := B₁/B₂ は
**ℂP¹ 値の有理型関数**として区間全体で well-defined(B₂ のみの零点では H = ∞、
共通零点では正則化商の値 — 有理型関数として除去可能)。
  G(w) := |1 + w| / max(1, |w|)  は **ℂP¹ 上の連続関数**(G(∞) := 1 — |w| → ∞ で
  |1+w|/|w| → 1)であり、**g := G(H(t)) と定義する**。
B₁, B₂ が同時に零でない点では F = B₂(1+H)、U_H = log|B₂| + log max(|H|,1) より
**g = e^{−U_H}|F| の exact 恒等式**が成立。共通零点(U_H = −∞、e^{−U_H}|F| は
∞·0 型で未定義)では g は上の定義による**連続延長**であり、これが以後の kernel の
対象量である(検算例: B₁ = B₂ = t ⇒ H ≡ 1 ⇒ g ≡ 2、B₁ = t, B₂ = −t ⇒ H ≡ −1 ⇒
g ≡ 0 — 各 ord・先頭係数比 λ の場合は g(t₀) = G(λ)、次数差がある場合は G(0) = G(∞) = 1)。
**天井 g ≤ 2 は ℂP¹ 全体で exact に成立**(G ≤ 2)。G(w) = G(1/w) の対称性より
以後 WLOG の index 交換が合法。∎

**(F2²-3) case 骨格と (a)/(b)/(c-ii) の完結**: σ := sup_{J_k}|1 + H|。
- **(a) source 上の block 支配**: ある t* ∈ J_k で max(|H(t*)|, 1/|H(t*)|) ≥ e のとき、
  WLOG |H(t*)| ≥ e(対称性)で g(t*) = |1+H|/|H| ≥ 1 − 1/e ≥ 0.63。天井より
  **‖g‖_{I_k} ≤ 2 ≤ 3.2 ‖g‖_{J_k}** ✓(QR5 (a) の 2|2 版 — singleton 不要のため
  §3.2 移植すら不要の初等閉鎖)。
- **(b) 比較可能・非深相殺**: (a) 否(J_k 全体で e^{−1} ≤ |H| ≤ e)かつ σ ≥ 1/10:
  t* = argmax|1+H| で g(t*) ≥ σ/e ≥ 1/(10e) ⇒ **‖g‖_{I_k} ≤ 2 ≤ 20e·‖g‖_{J_k}** ✓。
- **(c-ii) 中間深度**: (a) 否かつ c₁ρ⁹ ≤ σ < 1/10: 同様に ‖g‖_{J_k} ≥ σ/e ≥ c₁ρ⁹/e ⇒
  **‖g‖_{I_k} ≤ (2e/c₁)·ρ⁻⁹·‖g‖_{J_k}** ✓。**c₁ の menu 規約([GC4A1-02] 対応)**:
  本 packet は **standing ceiling c₁ ∈ (0, 10⁻²]** を先に固定する(QR5 の menu は
  ρ⁵ 用で流用不可のため、PBK22 用の制約を独立に宣言)。最終値は A.4/A.5 の menu が
  この ceiling 内で確定する。上の場合分けは任意の c₁ ∈ (0, 10⁻²] について排反・網羅
  ((a) 否の下で σ の三分割 [0, c₁ρ⁹) / [c₁ρ⁹, 1/10) / [1/10, ∞) — ρ ≤ 1 より
  c₁ρ⁹ ≤ 10⁻² < 1/10 ✓)。
- **(c-i) 深平坦**: (a) 否かつ σ < c₁ρ⁹ — 以下の層別の後、JF₉(A.2)・two-sided
  P4(A.3)・WE₉(A.4)へ。**本 packet はここを閉じない**。∎

**(F2²-4) divisor 層別(deep-flat 域の前処理)**:
- **共通因子の exact 相殺(cell 局所 — [GC4A1-03])**: 各 cell 上で
  D := gcd(P₁, P₂)(モニック代表、deg D =: d_common ≤ 2)、P_i = D·P̃_i
  (P̃₁, P̃₂ 互いに素)。**divisor データは cell 局所**であり(P_i は cell ごとの F2
  出力 — J_k 全体の単一 D は存在しない)、A.2 へは
  `divisor_record := {cell_id ↦ (branch 対, P₁, P₂, D, P̃₁, P̃₂)}` を渡す。cell 境界の
  帰属は §8.1 の左閉右開規約。D1/D2 branch の P_i は定数なので、非自明な D は
  **D3–D3 cell に限る**。
  F = D·F̃(F̃ := P̃₁V₁e^{r₁} + P̃₂V₂e^{r₂})かつ
  U_H = log|D| + Ũ_H(Ũ_H := max(log|P̃₁V₁e^{r₁}|, log|P̃₂V₂e^{r₂}|))なので
  **g = e^{−Ũ_H}|F̃| = g̃ — 共通因子は weighted ratio から exact に消える**。
  深平坦解析は互いに素な reduced pair (P̃₁, P̃₂) に帰着し、A.2 の次数予算は
  9 − 2·d_common … ではなく **W_c の ord F = ord D + ord F̃ 分解により
  ord F̃ ≤ 9 − (D の消滅次数)** の形で消費する(正確な予算勘定は A.2 の義務)。
- **片側零点の非深平坦性(観察)**: t₀ が P̃₁ のみの零点なら近傍で |H| 小 ⇒
  |1+H| ≈ 1 — 深平坦集合から自動排除。P̃₂ のみの零点(H の極)も対称に排除
  (g → 1)。**定量的 tube(排除近傍の幅と定数)は A.3 の義務** — 本 packet は
  層別(numerator-only / denominator-only / common)の三分岐と各分岐の行き先のみを
  固定する。
- **lead 下界 obligation の候補解消経路(§8.1 (3) の送り事項 — [GC4A1-04] で表現を
  訂正: obligation は A.2 受理まで open のまま)**: F2 により block は **exact 多項式
  因子 P_i** を持つので、深平坦比較を |P̃₁| vs |P̃₂| の直接比較に置き換える経路が
  開ける — ただし F2 は P̃_i の先頭係数の**一様下界を与えない**ため、これは
  「候補経路」であり解消ではない。定量比較の成立可否は A.2(JF₉)の証明義務。
  A.2 が受理された場合に限り、GC-3 §7.3 の lead_i field を「P̃_i の係数 witness」へ
  差し替える spec 改訂(versioned 方式)を行う。∎

**(F2²-5) 深平坦窓の u-形**: (c-i) の J_k 上(σ < c₁ρ⁹ ≤ 10⁻²(c₁ ceiling と ρ ≤ 1
より)・|H| ∈ [e^{−1}, e])では
−H が 1 近傍にあり、u := Log(−H)(principal)が定義され |u| ≤ 2|1 + H| ≤ 2c₁ρ⁹、
  u = log(P̃₁/P̃₂) + log(V₁/V₂) + (r₁ − r₂) − iπ (mod 2πi、cell 上の分枝固定)
— 「deg ≤ 2 有理 log + 有界単位 log + 二次多項式」の形。全窓への分枝接続は
A.5(bootstrap)の義務(QR5 P3 と同配置)。∎

**scope(非主張)**: (c-i) の閉鎖(JF₉/P4/WE₉/BOOT/ASM)、γ の確定、
V_i の複素 collar 評価(A.3 — COLLAR-POLE 対応)、FR 条件の最終充足(A.6)。
人間による査読は未実施。

### 8.4 GC-4A.2a JF9-EXACT(exact bridge と有限 m 二分岐 — accepted、R-GC4A2A R2 PASS、fixed SHA `5bb69af`)

**設定**: A.1 の (c-i) 深平坦窓 W ⊂ J_k(σ = sup|1+H| < c₁ρ⁹、|H| ∈ [e⁻¹, e]、
u = Log(−H) 解析的、|u| ≤ 2c₁ρ⁹)、cell 局所 divisor_record(D、P̃_i、C_i := B_i/D)。
t₀ ∈ W。**入力仮定**: node の 4 原子は constant-gauge quotient 済みで相異
(全対の指数差が非定数 — SPLIT4/§7.1 の quotient 規約)。本 packet は
**有限 m の exact 主張のみ**を行う — 一様定数(κ、λ、c_J)は A.2b/A.2c の義務。

**(EX-1) Taylor gauge**: p := T_{2,t₀}u(u の t₀ における 2 次 Taylor 多項式)、
v := u − p。構成より v(t₀) = v′(t₀) = v″(t₀) = 0 が exact に成立。v は W 上解析的。∎

**(EX-2) 橋の恒等式**: Φ_p := B₁ + e^{p} B₂ と置く。W 上で e^{u} = −H = −B₁/B₂
(u の定義)より B₁ = −e^{u}B₂、よって
  Φ_p = (−e^{u} + e^{p})B₂ = e^{p}B₂(1 − e^{v}) = **D · e^{p} · C₂ · (1 − e^{v})**。∎

**(EX-3) 消滅次数の橋**: v ≢ 0 かつ v⁽ⁿ⁾(t₀) = 0(n = 0..N)なら
ord_{t₀}(1 − e^{v}) = ord_{t₀} v ≥ N + 1(1 − e^{w} の w = 0 での単純零 × 合成)。
d₀ := ord_{t₀} D、ord C₂ ≥ 0 より
  **ord_{t₀} Φ_p ≥ d₀ + N + 1**。∎

**(EX-4) 有限 m 二分岐(本 packet の主定理)**: N := 9 − d₀ とする。次のいずれかが
成立する:
  **(i) v ≡ 0(W 上)** — このとき u = p(二次)、B₁ = −e^{p}B₂、Φ_p ≡ 0。
  **二次比枝**として deg≤2 route(A.4 系で処理する Chebyshev/Remez 枝)へ dispatch。
  **(ii) (v⁽³⁾, …, v⁽ᴺ⁾)(t₀) ≠ (0, …, 0)** — jet 床の有限 m 形。
*証明*: (i) 否(v ≢ 0)とし、v⁽ⁿ⁾(t₀) = 0(n = 3..N — 0..2 は (EX-1) で自動)と仮定
して矛盾を導く。(EX-3) より ord Φ_p ≥ d₀ + N + 1 = 10。Φ_p は 4 つの二次位相
{g_{1,1}, g_{1,2}, p + g_{2,1}, p + g_{2,2}}(g_{i,j} = pair i の原子指数)の指数結合で、
係数は元の原子係数(非零 — zero-pruning 済み)。場合分け:
- **(a) shifted 4 位相の全対差が非定数**: Φ_p は真正 4 原子結合(≢ 0 — 相異
  指数系の非零係数結合は L0 で非零)なので **W_c(4)(§3.1、任意中心)より
  ord ≤ D_W(4) = 9** — 10 と矛盾。
- **(b) shifted 位相のある対の差が定数**(c = 0 の exact 一致を含む —
  g_{1,j} − (p + g_{2,l}) ≡ c ∈ ℂ の場合、指数は定数倍で比例。[GC4A2A-01] 対応:
  pair 内は η_i 非定数なので pair 間対のみ起き得る): 定数差対を e^{c} の係数吸収で
  exact に合算(constant-gauge equivalence — 閉包 §4.3.6 N-pre と同じ操作)し、
  全対差が非定数な c′ < 4 本の系に帰着。
  - 合算後も非零項が残るなら W_c(c′) より ord ≤ D_W(c′) ≤ D_W(3) = 5 < 10 — 矛盾。
  - 合算で全係数が消えるなら Φ_p ≡ 0 ⇒ (EX-2) より 1 − e^{v} ≡ 0(D, e^{p}, C₂ ≢ 0)
    ⇒ v は 2πiℤ 値の局所定数 ⇒ **W は区間(連結)**なので v は定数、v(t₀) = 0 より
  **v ≡ 0** — (i) 否に矛盾([GC4A2A-03]: 連結性を明記)。
いずれの枝でも矛盾するので (ii) が成立。∎
(注: 一致の判定・合算は**有限 m の exact 操作**であり、衝突「極限」の confluent 現象は
ここでは生じない — それは A.2b/c の一様性解析の対象。)

**(EX-5) jet の exact recurrence(authoring location)**: u の jets は
log-微分の三角再帰で exact に計算する: L_i := (log B_i)′ = B_i′/B_i とし、
B_i の Taylor 係数 {b_{i,n}}(原子指数の指数級数 — E 型再帰で exact)から、
B_i′ = L_i · B_i の Taylor 展開
  **(n+1)·b_{i,n+1} = Σ_{j=0}^{n} ℓ_{i,j} · b_{i,n−j}**  (ℓ_{i,j} = L_i の j 次係数)
を ℓ_{i,·} について三角に解く([GC4A2A-02] 訂正 — 検算: B = e^s なら b_n = 1/n!、
ℓ₀ = 1、ℓ_{j≥1} = 0 で両辺 (n+1)/(n+1)! = Σ 1/(n−j)!·[j=0] ✓。b_{i,0} = B_i(t₀) ≠ 0 の
chart — 零点 chart では divisor_record 経由で C_i に対し同じ再帰)。
u′ = L₁ − L₂ より **u の (n+1) 次 Taylor 係数 = (ℓ_{1,n} − ℓ_{2,n})/(n+1)**(n ≥ 0)、
u(t₀) = Log(−H(t₀))。
数値検証(JF-NONCOMPACT fixture)はこの再帰を唯一の jet 計算法とする
(finite difference 禁止 — consult #9)。∎

**scope(非主張)**: 一様 jet 床(κ・λ・c_J — A.2b/A.2c)、collar(A.3a)、
deg≤2 枝の処理(A.4 系)、10 階上界(A.3b)。人間による査読は未実施。

### 8.5 GC-4A.3a PBK22-ZF(reduced zero-free collar と窓再配置 — accepted、R-GC4A3A R2 PASS、fixed SHA `926093c`)

**設定**: A.1 の cell(両 pair held、F2 branch 固定、divisor_record)と (c-i) 深平坦
状況。reduced 零点 = P̃₁ の零点(≤ 2)∪ P̃₂ の零点(≤ 2)、計 ≤ 4 個(cell 局所)。
V_i = E(z_i(t))(E(z) = (e^z − 1)/z)。**依存は A.1 のみ**(A.2 系への循環なし)。
10 階上界・Cauchy 評価は A.3b の義務(本 packet は collar の幾何のみ)。

**(ZF-1) V 単位の零点自由複素 collar(graded)**: E の零点は z ∈ 2πiℤ∖{0}。
F2(D3 branch)より実軸上 z_i(t) ∈ B* = [−17/8, 17/8] × i[−(π+1/4), π+1/4]、
特に |Im z_i| ≤ π + 1/4 で 2π までの余白 ≥ 2π − (π+1/4) = π − 1/4 > 5/2。
複素方向 |y| ≤ h ≤ 1 の帯での drift は、η̃_i が二次(η̃_i″ = η_i″ 定数)なので
Taylor 展開が exact に
  z_i(t+iy) − z_i(t) = iy·η̃_i′(t) − y²·η̃_i″/2
となり([GC4A3A-02] — 帯上評価の根拠)、(BRF-1) の |η_i″| = |ΔA_i| ≤ s_i² ≤ 1/16
(m ≥ m_BRF0)と |η̃_i′(t)| ≤ Λ_{i,k} より
  |z_i(t+iy) − z_i(t)| ≤ |y|·(Λ_{i,k} + s_i²·h/2) ≤ (Λ_{i,k} + 2)|y|。よって
  **h_V := min(1, 1/(Λ_{1,k} + 2), 1/(Λ_{2,k} + 2))**
の複素 collar 上で drift ≤ 1、すなわち |Im z_i| ≤ π + 1/4 + 1 < 2π。
**E の零点は純虚(2πiℤ∖{0})なので |Im z_i| < 2π だけで除外される**(実部の
B* 逸脱 ≤ 17/8 + 1 は無関係 — [GC4A3A-01] の表現修正)。
**D1/D2 branch([GC4A3A-01] 閉鎖)**: V_i = 1 − e^{∓z} の零点は z ∈ 2πiℤ(z = 0
込み)。z ≠ 0 の零点は上と同じ |Im| 勘定で除外。z = 0 は F2 の D1: Re z ≥ 15/8
(D2: ≤ −15/8)と drift ≤ 1 より collar 上 **Re z ≥ 7/8 > 0(D2: ≤ −7/8 < 0)** で
除外。**V₁, V₂ は collar 上零点なし**。∎

**(ZF-2) SN-2|2: 窓再配置の鳩ノ巣**: N_A := 13 とし、J_k(長さ ρ = ε_chain)を
等分した部分窓 S_1, …, S_{13}(長さ ℓ := ρ/13、半開)を考える。排除判定を**狭義**で
  S_j 排除 :⟺ ∃ reduced 零点 z: dist(Re z, S_j) < ℓ
と置く。**各零点が排除する部分窓は高々 3 個**: Re z を含む(または最近接の)窓 S_j に
対し、S_{j±2} 以遠は dist ≥ ℓ(隣窓 1 本分)なので排除されない(境界配置でも
dist = ℓ は狭義判定で非排除)。零点 ≤ 4 個で排除 ≤ 12 < 13 — **少なくとも 1 個の
部分窓 S が残り、dist(Re z, S) ≥ ℓ = ρ/13(全 reduced 零点 z)**。
S の複素 collar 半径を **r_S := min(ρ/26, h_V)** と取れば、collar 内の任意の点と
零点の実部距離 ≥ ρ/13 − ρ/26 = ρ/26 > 0 — collar は全 reduced 零点と全 V 零点
((ZF-1))を含まない。**零点自由複素 collar 付き source 窓 S の存在**。∎
(注: 排除判定は Re z のみで行う — Im z ≠ 0 の複素零点は実部が S から遠ければ
collar(幅 r_S ≤ ρ/26)に入らない。Im 方向は r_S ≤ h_V が V 側を、多項式零点は
実部距離が押さえる。)

**(ZF-3) 出力契約(型付き — [GC4A3A-03])**: A.2b/A.3b が消費する interface:
  `zf_witness := (cell_id, S = [a_S, b_S)(半開・端点は ℝ、b_S − a_S = ρ/13),
   r_S ∈ (0, min(ρ/26, h_V)], h_V ∈ (0, 1],
   zeros_P̃₁ / zeros_P̃₂ : ℂ 値リスト(重複度込み、各 ≤ 2),
   invariants: (i) ∀z ∈ zeros_P̃₁ ∪ zeros_P̃₂: dist(Re z, S) ≥ ρ/13、
   (ii) collar(S, r_S) 上 V₁V₂ ≠ 0((ZF-1))、
   (iii) S ⊂ J_k)`
— invariants は record 生成時の検証条件(fail-closed: 不成立なら record を作らない)。
divisor_record と同じ cell 粒度。深平坦判定(A.1 の σ)は S 上で再評価する
(J_k 深平坦 ⇒ S ⊂ J_k でも深平坦 — sup の部分集合単調性)。d₀ = ord_{t₀}D は
S の中心 t₀ で読み直す(divisor_record から exact)。
**scope 明記([GC4A3A-04])**: 本 collar が除外するのは **reduced 零点(P̃₁/P̃₂)と
V 零点のみ** — 共通因子 D の零点は除外せず、d₀ = ord_{t₀}D として A.2a の予算
N = 9 − d₀ に保持される(common-zero は §8.3 (F2²-4) の exact 相殺で g から消えて
おり、collar の対象ではない)。∎

**scope(非主張)**: collar 上の導関数上界(10 階 — A.3b)、一様定数の compactification
(A.2b/c)、S 上の kernel 不等式。人間による査読は未実施。

### 8.6 GC-4A.2b JF9-NORM(有限 chart atlas と正規化 — **R-GC4A2B R9 ACCEPTED、fixed SHA `a2302f3`**)

**設計裁定(consult #10 — R1 の 6 blocking への回答)**: v1 の大域 X̄・大域 metric・
大域連続 J は**撤回**(それらの修理は GC-9 級の compactification 本体に膨張する)。
QR5 P2 と同じ**有限 chart 方式**を採る: 各 chart の閉座標箱のみ compact とし、
大域貼り合わせを要求しない。**本 packet は正の床を主張しない**(床 = A.2c)。

**(N-0) 前処理(exact — chart 選択より先)**:
(0a) 中心化 x := t − t₀、各位相 q_j(x) = A_jx²/2 + B_jx + γ_j の γ_j を係数へ吸収。
(0b) **merge-first**: (A_j, B_j) が一致する原子を constant-gauge class として exact 合算、
零係数 class を削除。残存 class 数 r:
  r = 0 ⇒ Φ_p ≡ 0 = QR exit(v ≡ 0)。r = 1 ⇒ 単原子 exit(低 arity)。
  2 ≤ r ≤ 4 ⇒ このとき初めて **λ := max_{a<b} max(|B_a − B_b|, |A_a − A_b|^{1/2}) > 0**
  (merge 後は全対の (A,B) 差非零 — [GC4A2B-02] 解消)。
(0c) **gauge section の明示([GC4A2BR3-05]、[GC4A2BR4-04] で決定的に)**:
ℂ 上の全順序 z ≺ w :⟺ Re z < Re w ∨ (Re z = Re w ∧ Im z < Im w)、class (A,B) には
(A, B) の辞書式でこの ≺ を適用。merge 後の class は (A,B) が相異なる((0b))ので
この順序は strict — **anchor := ≺-最小 class(一意・計算可能)**、q̄ := その位相。
残る class の絶対座標 = anchor との差(減算 — 除算でないので発散しない)。
|A_a − A_anchor| ≤ λ²、|B_a − B_anchor| ≤ λ(λ の定義 = 対差の weighted max)なので
λ-正規化座標 ((A_a−A_anchor)/λ², (B_a−B_anchor)/λ) は閉単位円板に入る
(部分列コンパクト性の前提が成立)。
共通 gauge は **Φ_p = e^{q̄}·Σ c_j e^{q_j − q̄} の非零共通因子 quotient**
([GC4A2B-07] — 「係数不変」表現を撤回)+ 係数の **sup-norm 正規化 ‖c‖_∞ = 1**
([GC4A2BR2-01] — lexicographic pivot = 1 は非コンパクト((ε,1) ↦ (1,ε⁻¹) の発散)の
ため撤回。‖c‖_∞ = 1 の球面はコンパクト)。
**座標値域表(閉箱)**: merge 後 class 位相 **((A_a − A_anchor)/λ², (B_a − B_anchor)/λ)**
∈ 閉単位円板((0c) の anchor 差 — |A_a − A_anchor| ≤ λ²、|B_a − B_anchor| ≤ λ)、
係数 ∈ {‖c‖_∞ = 1} 球面、θ ∈ S¹、rate flag 比 ∈ [0,1]、
E_i chart 座標 ∈ 各 F2 branch の**閉**領域(D3: 閉単位円板 — 中心 0 は除かず、
E_i = 0 は boundary_routes で D_{i,0} chart へ送る面。D1/D2: 閉単位円板)、δ_i ∈ [0,1]、
τ ∈ [0,1]、ζ ∈ 閉円板 ∪ {∞}(ζ⁻¹ chart で被覆)。**band 境界は半開(左閉右開)+
優先順位で一意**(selector の各判定は「≥ ε(inner)」で発火、「< ε」で次段 — 決定的)。

**(N-1) ChartSpec 型**:
  `ChartSpec := (chart_id, domain_predicate, centered_coordinates, gauge_section,
   coefficient_pivot, λ, small_parameters, rate_flag,
   diagnostic_generators R_C(床契約には不使用 — (N-6)(6e)), κ_C := κ∘param_C, R_Q,
   normalized_jet_map 𝒥_C, boundary_routes, overlap_certificates)`

**GCRouteRecordEnum-v2([GC4A2BR5-B06] — versioned 拡張、accepted §7.1 は不変)**:
A.2b を消費する record は
  `GCRouteRecord-v2 := GCRouteRecord(§7.1) + (chart_id, q_band_witness,
   zero_flag_witness, boundary_route_chain)`
を必須とする。field 型([GC4A2BR7-B04] で有限型を完備化):
- `chart_id ∈ GCChartIdEnum := {M_0, M_1, M_2, M_3, M_4, R, D_{1,0}, D_{1,∞},
  D_{2,0}, D_{2,∞}, S_{1≺2}, S_{2≺1}, C_1, C_2, C_1^{(2)}, C_2^{(2)}, C_12,
  C_12^{(2)}, Z, G, Q_C}`(有限 enum — 21 値。列挙外は record 生成禁止)。
- `face_id ∈ FaceIdEnum := {coeff-zero-a (a = 1..4), E_i-zero, E_i-infty (i = 1,2),
  tau-zero, gcd-exact, kappa-zero}`(有限 enum — (N-5) route 表と 1:1)。
- `target_chart_id ∈ GCChartIdEnum ∪ {exit-v0, exit-low-arity}`。
- `rank_before ∈ {0..4} × {0..9}`(rank = (r, 9−d₀))、
  `rank_after ∈ ({0..4} × {0..9}) ∪ {exit}`([GC4A2BR8-B04] — union 型)。
  **非終端 entry**(target_chart_id ∈ GCChartIdEnum)は verified flag
  `rank_after <_lex rank_before` 必須(strict 降下 — flag 不成立は record 生成禁止)。
  **終端 entry**(target_chart_id ∈ {exit-v0, exit-low-arity})は rank_after = exit
  で chain はそこで終端(以降の entry を持つ record は生成禁止)。
- `q_band_witness := (α₀, α₁, α₂ ∈ ℂ の実値, verified flags |α_k| ≤ R_Q (k=0,1,2))`
  ((6a) の p ∈ 𝒬_band 保証 — 欠落・violation flag は record 生成禁止)。
- `zero_flag_witness := (min_i |B_i(t₀)| の実値, ≥ ε_Z の verified flag)`(structural
  chart のみ — Z/G 行きは flag 不成立で記録)。
- `boundary_route_chain := 有限列 [(face_id, target_chart_id, rank_before, rank_after)]`
  ((N-5) の rank strict 降下の検証列)。
**v1 GCRouteRecord による A.2b 消費は禁止(fail-closed)** — D-PBK-22v2 と同じ
versioned 拡張様式。

**(N-2) 基本 chart 表**(交差は新 chart でなく **ordered rate flag** で表す):

| chart | 主座標・小パラメタ | chart 上の床(A.2c の証明対象 — ここでは宣言) |
|---|---|---|
| M_r(merge/低 arity) | merge 後 class 位相 ((A_a−A_anchor)/λ², (B_a−B_anchor)/λ)((0c) anchor 差)、projective 係数(r ≤ 3) | r=0: v≡0 exit。r=1: 単原子 exit(jet・overlap 契約対象外)。r∈{2,3}: W_c(r) 系 |
| R(regular) | 位相 pivot・係数 pivot・E_i が {0,1,∞} から離隔・scale 比下方離隔 | max|𝒥_{R,n}| ≥ c_R·κ(非消滅 = W_c(4)) |
| D_{i,0}/D_{i,∞} | E_i = rω / ω/r(r ↓ 0、|ω| = 1) | QR5 P2 の E→0,∞ 型明示計算(片 pair 単原子化) |
| S_{1≺2}/S_{2≺1} | τ = λ₁/λ₂(または逆数)、支配側 λ = 1 正規化、劣位側は 0/1 次 divided-difference moment | surviving moment 通常 ⇒ 低 arity floor、退化 ⇒ C_i へ |
| C_i / C_i^{(2)}(片側 confluent、affine / 二次退化) | δ_i = s_i/λ、方向 h_i、係数 (a_i, b_i)(C_i^{(2)} は (a_i, b_i, c_i) — deg ≤ 2)。**flag 判定: |β_i| ≥ ε_C·|ΔA_i|·w(affine)/ < (quadratic — 半開)**、β_i = ΔB_i + ΔA_i t₀、w = 窓幅 | 極限 (a_i + b_i h_i (+ c_i h_i²))e^{q_i} — 低 arity/混合 floor |
| C_12 / C_12^{(2)}(両側 confluent) | (δ₁, δ₂) + 両 divided-difference 座標(deg ≤ 2 まで — 閉箱: 係数 ∈ ‖·‖_∞ = 1 球面) | 極限 P₁e^{q₁} + P₂e^{q₂}(**deg ≤ 2**)⇒ **W_CONFL(2,2) v2(B_CONFL = 6 目標)** |
| Z/G(zero・gcd) | reduced 零点の正規化座標 **ζ := λ(z − t₀)**(と ζ⁻¹ chart)、分子/分母 root separation | 非共通 root = log principal part floor、両側近接 = gcd divided-difference、exact 一致 = D 再取得 |
| Q_C(QR blow-up) | 統一 κ((N-6))の blow-up: 0 < κ < ε_Q 帯、**座標 = structural 座標 + κ のみ**(κ は連続 — (6b))。Q₀ の α は座標でなく record 注記([GC4A2BR7-B03]) | max|𝒥_{C,n}|/κ ≥ c_{Q,C}(A.2c の主 transversality 義務) |

**(N-3) collar scaling の訂正([GC4A2B-04] 解消)**: 正規化変数は y = λ(t − t₀) なので
零点座標は **ζ = λ(z − t₀)**(v1 の「零点位置/λ」は逆 — 撤回)。zf_witness invariant
(i) は **|ζ| ≥ λρ/13** となり、**λ → ∞ では零点は無限遠へ出る**(collar 侵入なし)。
λρ → 0 の場合のみ Z chart に入る。分子・分母零点の同時近接は G chart、exact 一致は
D の再取得(gcd-transition)。「侵入は生じない」の v1 宣言は撤回し、Z/G chart が吸収。

**(N-4) gcd-transition([GC4A2B-03] の d₀ 問題)**: d₀ は位相座標にしない。record に
  `(source_d₀, target_d₀ ≥ source_d₀, gcd_transition_ref)`
を持たせ、境界で d₀ が増える場合は **jet range 埋め込み**
  {3, …, 9 − d₀⁺} ⊆ {3, …, 9 − d₀}
により、境界 floor(短い range)が元の max(長い range)へそのまま埋め込まれる
(max の単調性 — 証明は自明)。∎

**(N-5) selector と部分列網羅性**: 固定小定数列
0 < ε_Q ≪ ε_G ≪ ε_Z ≪ ε_C ≪ ε_S ≪ ε_D < 1([GC4A2BR5-B08] で ε_Z を追加)
と inner/outer band で、優先順位
  (1) exact exit →(2) pivot 固定 →(3) QR-near →(4) zero/gcd →(5) confluent
  →(6) scale 分離 →(7) D1/D2 →(8) regular
の **first-match selector**([GC4A2BR7-B05] で述語を完備化)を定義する。
**各段の domain predicate(上から評価し最初に成立した段が chart を割り当てる —
決定性は述語の計算可能性と評価順、網羅性は段 (8) が補集合であることから従う)**:

| 段 | predicate(すべて computable、半開規約: 「< ε」で発火・「≥ ε」で次段) | 割当 |
|---|---|---|
| (1) | merge 後 r ≤ 1(exact)、または κ = 0(exact — (6d)) | exit(v≡0 / 単原子) |
| (2) | 常に成立(anchor := ≺-最小 class — (0c)。割当でなく gauge 固定) | — |
| (3) | 0 < κ < ε_Q | Q_C |
| (4) | **段内順序([GC4A2BR8-B05]): (4a) 零点 exact 一致(→ D 再取得)→ (4b) min_i |B_i(t₀)| < ε_Z(→ Z)→ (4c) 分子分母零点の ζ 距離 < ε_G(→ G)**。段内も first-match。witness = `zero_flag_witness` | D / Z / G |
| (5) | δ_i = s_i/λ < ε_C(片側 → C_i、両側 → C_12。sub-chart は N-8 の β 比 flag で ^{(2)} 系へ — 半開) | C 系 |
| (6) | τ := min(λ₁,λ₂)/max(λ₁,λ₂) < ε_S。**λ_i の定義([GC4A2BR8-B05]): λ_i := max(|ΔB_i|, |ΔA_i|^{1/2})(side i の pair 内差 — child_collision_witness の s_i と同じ configuration データ。global λ とは別物)**。S_{1≺2} は λ₁ ≤ λ₂(半開: 等号は 1≺2 側) | S_{1≺2}/S_{2≺1} |
| (7) | |E_i| < ε_D または |E_i| > 1/ε_D。**両 i 成立時は最小 index i = 1 を chart に採用し、他方は ordered rate flag に記録([GC4A2BR8-B05] — index tie-break)** | D_{i,0}/D_{i,∞} |
| (8) | 上記いずれも不成立(補集合) | R |

よって任意の admissible 配置は**ちょうど 1 つ**の割当を受ける(first-match +
段 (8) 補集合)。structural chart((5) 以降と M_r)では |B_i(t₀)| ≥ ε_Z が
routing による定義的下限。複数退化の同時発生は **ordered rate flag**(最初の pivot 退化量
ε_{π₁} を選び ε_{π₂}/ε_{π₁}, … ∈ [0,1] を記録 — 有限 permutation)で表す。
**網羅性補題(A.2b の主証明 — [GC4A2BR4-05] で境界処理を補完)**: 任意の
admissible 配置列は、merge-first exit に入るか、有限部分列上で
(chart_id, pivot, rate flag, d₀-transition type) が固定され、その chart の
**閉座標箱内で収束部分列を持ち、極限は boundary_routes の有限鎖の後にある chart の
domain 内点に対応する**。
*証明*: (i) 選択肢(chart_id ≤ 8 家族・pivot ≤ 有限・flag permutation ≤ 有限・
d₀-transition ≤ 有限)は全て有限なので鳩ノ巣で部分列固定。固定後の座標は各 chart の
定義により**閉**箱に値を取る((N-2) — D3 も閉円板に修正済み)ので
Bolzano–Weierstrass で極限が閉箱内に存在。
(ii) **境界の処理**: band 境界は半開 + 優先順位なので、任意の極限配置は selector で
**ちょうど 1 つ**の chart に割り当てられる(述語の分割 — ping-pong なし)。極限が
固定 chart の domain 内点ならそこで終了。境界面(座標箱の閉包にのみ属す点)なら
boundary_routes が送り先を与える。**boundary_routes の全列挙
([GC4A2BR5-B05])**:

| face | 送り先 | rank への作用 |
|---|---|---|
| band 境界(ε_Q/ε_G/ε_Z/ε_C/ε_S/ε_D、E_i band)| route ではない — 半開分割で selector が一意割当 | 不変(遷移なし) |
| κ = 0(exact QR — [GC4A2BR7-B02]) | v ≡ 0 exit((6c)(6d)) | 終端(rank_after = exit — [GC4A2BR8-B04]) |
| 係数消滅面 c_a = 0(任意 chart) | M_{r−1} 家族(r−1 ≤ 1 なら exit-v0/exit-low-arity の終端 entry) | r 減(終端時は rank_after = exit) |
| E_i = 0 / ∞(D3 中心・ζ⁻¹ chart の 0) | D_{i,0} / D_{i,∞}(単原子化) | r 減 |
| τ = 0(S) | 劣位側消滅 → M_{r′} | r 減 |
| 零点 exact 一致(G) | D 再取得((N-4) gcd-transition) | d₀ 増 |
| δ_i = 0(C の極限面) | 遷移なし — C chart の domain 内点(limit object) | 不変 |

**真の遷移は離散 rank rank := (r, 9 − d₀) の辞書式を strict に下げ、鎖に沿って
r は非増加・d₀ は非減少(表の全行で単調)**。
r ∈ {0..4}、d₀ ∈ {0..9} なので鎖長 ≤ 4 + 9 = 13 で必ず domain 内点に到達
(r = 0/1 は merge/低 arity exit)。∎(大域 X̄ の compact 性をこれで**置換**。)

**(N-6) 統一 κ([GC4A2BR4-01][02] — 親定義を実体化し chart-local を恒等写像に還元)**:

**(6a) 𝒬_band の明示定義**: λ-正規化変数 y = λ(t − t₀) 上の二次多項式
  𝒬_band := { Q(y) = α₂y² + α₁y + α₀ : (α₂, α₁, α₀) ∈ ℂ³, |α_k| ≤ R_Q }
(閉 polydisc — compact)。**R_Q は global 宣言定数**(全 chart 共通 —
[GC4A2BR5-B01]: chart 別にすると overlap 上で κ の値が一致しない。ChartSpec の
R_Q 欄は global 定数への参照)。
**座標接続([GC4A2BR5-B02])**: p = T₂u は t 座標の二次多項式
p(t) = p₀ + p₁(t−t₀) + p₂(t−t₀)²。y = λ(t−t₀) との同一視は
**Q(y) := p(t)、α_k := p_k/λᵏ**(k = 0,1,2)。よって
  **p ∈ 𝒬_band ⟺ |p_k|/λᵏ ≤ R_Q (k = 0,1,2)**
であり、`q_band_witness` の α 座標はこの λ-正規化係数(型は (N-1)
GCRouteRecord-v2)。witness が欠落・違反する record は生成禁止(unresolved)。
「p が探索集合に入る」ことは受理済み record の**型的保証**であり、証明義務は
witness 検査に還元される。

**(6b) κ の親定義と連続性([GC4A2BR5-B03] — 係数ベクトルを撤回し C⁰ ノルムへ)**:
共通 gauge((0c))の y 座標で Φ_Q := B₁ + e^Q B₂(side 関数は y 座標表示)とし、
  **κ(x) := min_{Q ∈ 𝒬_band} sup_{|y| ≤ 1} |Φ_Q(x)(y)|**。
merge・係数ベクトルは**定義に使わない**(Q の変動で q₁ と q₂ + Q が一致し class 数が
変わる問題 — B03 — は sup ノルムでは生じない: 次元概念そのものが不要)。
連続性: (x, Q) ↦ Φ_Q(x) は閉円板上一様収束位相で連続(整関数、係数は閉箱座標と
α の連続関数、compact 上一様)、sup ノルムは C⁰(D̄) 上連続、compact な 𝒬_band 上の
min は Weierstrass で**到達**し、κ は chart 閉箱上**連続**(compact 族上の min の
一様連続性)。**κ = 0 ⟺ ∃Q₀: Φ_{Q₀} ≡ 0 on |y| ≤ 1 ⟺ Φ_{Q₀} ≡ 0**(整関数の
一致定理 — 閉円板上の零は全域零)。
**Q₀ の決定的選択([GC4A2BR6-07]、役割は [GC4A2BR7-B03] で record 注記に限定)**:
argmin 集合は compact(κ を実現する Q の集合 = 連続関数の水準集合 ∩ 𝒬_band —
閉かつ有界)。その上で (Re α₂, Im α₂, Re α₁, Im α₁, Re α₀, Im α₀) の
**辞書式最小元**(compact 集合上の逐次座標最小化 — 各段で非空 compact に絞られ、
6 段で一意)を Q₀ と定める。**α(Q₀) は chart 座標ではなく record の決定的注記**
(argmin の極限跳びによる選択写像の不連続は網羅性補題に影響しない — 補題の
compactness は structural 座標 + κ(いずれも連続)のみで走り、選択写像の連続性を
要求しない)。overlap 上の record 同一性は同一 configuration に同一 tie-break を
適用することで従う(点ごとの一意性のみ使用)。

**(6c) κ = 0 ⟺ v ≡ 0**:
(⇐) v ≡ 0 ⇒ Φ_p ≡ 0(A.2a (EX-4))、p ∈ 𝒬_band((6a) の witness)⇒ κ ≤ 0、
ノルムの非負性から **κ = 0**。
(⇒)([GC4A2BR8-B01] — R7 版の 4 項恒等式論法は Φ_Q の向きを取り違えており
撤回。(6b) の sup ノルム化により、そもそも**指数多項式の独立性論法自体が不要**に
なっていたことを明記し、以下の直接論法に全面置換):
κ = 0 ⇒ min の到達点 Q₀ で **Φ_{Q₀} = B₁ + e^{Q₀}B₂ ≡ 0(関数として — (6b) の
一致定理)**。よって {B₂ ≠ 0}(B₂ ≢ 0 なので開稠密)上で
  −B₁/B₂ = e^{Q₀}、すなわち −H = e^{Q₀}
⇒ u := Log(−H) = Q₀ + 2πik(接続成分ごとに局所定数)⇒ T₂u = Q₀ + 定数
⇒ **v = u − T₂u ≡ 0**(定数と 2πik は T₂ 減算で消える)。∎
この論法は side 関数の内部構造(P_i、V_i = E(z_i)、confluent か否か)に
**一切依存しない** — chart 場合分け・class 独立性(L0)・有理性はいずれも不要
(いずれも κ が係数ベクトル norm だった旧版((6b) v0.19.3 以前)の遺物)。
(補題 EL は本節では不要になったが、A.2c の W_CONFL 証明が参照するため定義は
保持する。)
**補題 EL(有理・指数排除)**: r 非定数多項式なら e^r は有理式でない。
*証明*: e^r = R 有理なら r′ = R′/R。R′/R は |x| → ∞ で → 0(単純極の和)、
r′ は非零多項式で減衰しない。矛盾。∎

**(6d) QR-near 述語と ε_Q([GC4A2BR4-02]、[GC4A2BR7-B02] で κ = 0 を分離)**:
**κ = 0 は exact QR exit**((6c) より v ≡ 0 — merge-first (0b) の r = 0 exit と同種の
exact exit であり、Q_C を含むどの chart にも入らない)。
QR-near flag := (**0 < κ(x) < ε_Q**)。Q_C の適用域は κ > 0 に限られ、床の式
max|𝒥_n|/κ ≥ c_{Q,C} は常に well-defined(0/0 は生じない — κ → 0 での商の挙動は
A.2c の transversality 義務)。
ε_Q は (N-5) の宣言定数列の最小元。**structural chart 上で κ ≥ ε_Q は selector の
routing 規則による定義的事実**(κ < ε_Q の配置は優先順位 (3) で Q_C へ送られ、
structural chart には入らない)— 下限の「証明」は不要で、κ の計算可能性
((6b) の到達 min)だけが必要。

**(6e) chart-local κ_C は恒等**: **κ_C := κ ∘ param_C**(chart parametrization との
合成 — 親 κ と同一関数の座標表示)。overlap 上で κ_C = κ_{C′}(同一 configuration の
同一関数値)は**定義から恒等**。旧 R_C tuple(支配側係数・moment・零点間隔等)は
**diagnostic generators に降格**し、床契約には使わない(床は κ のみ参照)。
κ_C = 0 ⟺ v ≡ 0 は (6c) を各 chart の class 構造で読むだけで全 8 家族に成立。

**(N-6′) λ の統一と overlap 移送([GC4A2BR4-03] — 損失を 1 に潰す)**:
**λ_C := λ(global、(N-0))を全 chart で共通とする** — D/Z の zoom 座標(ζ 等)は
chart 内部座標であり、**jet の正規化は常に global λ で行う**(chart 別スケールを
導入しない)。**normalized jet の定義は一本化([GC4A2BR5-B04])**:
  **𝒥_n := v⁽ⁿ⁾(t₀)/λⁿ**(raw — κ を含めない。κ-正規化は床の式の側に置く:
  structural 床は max|𝒥_n| ≥ c_C·κ、Q_C 床は両辺を κ で割った表示
  max|𝒥_n|/κ ≥ c_{Q,C} — 同一量の同値表示)。
λ・v とも chart 非依存なので 𝒥_n は **chart 非依存の内在量**。一般遷移式
  𝒥_{C′,n} = 𝒥_{C,n}·(λ_C/λ_{C′})ⁿ、床の移送損失 ≤ K_λ⁹·K_κ = K^{10}
(n ≤ 9 — 床の式が κ を 1 回含むため)は保持するが、統一により
**K_λ = K_κ = 1、global K = 1**(移送は無損失)。overlap_certificates の実値表
(**対象は structural chart 対のみ — r ≤ 1 exit は jet・overlap 契約対象外**
([GC4A2BR5-B05]: λ は r ≥ 2 でのみ定義。exit の床は W_c(1) 以下の直接評価)):

| 隣接対(優先段) | K_λ | K_κ | 根拠 |
|---|---|---|---|
| (Q_C, Z/G), (Z/G, C), (C, S), (S, D), (D, R), (M_r(r≥2), 近接 chart) 全対 | 1 | 1 | λ 統一((N-6′))・κ 統一((6e) 恒等) |

A.2c の床合成は c_J = min_C c_C / K^{10} = min_C c_C(K = 1)。

**(N-7) normalized jet map**: 各 chart で 𝒥_{C,n} := v⁽ⁿ⁾(t₀)/λⁿ(λ は global —
(N-6′))の **exact 式**:
- **M_r chart([GC4A2BR4-05] — 供給)**: (EX-5) 再帰そのもの(b₀ = B_i(t₀))。
  M_r の閉箱上では selector により |B_i(t₀)| ≥ ε_Z(これ未満は Z chart へ)なので
  分母は ε_Z で下に有界 — jet map は閉箱上連続。
- R/D/S chart: (EX-5) の log-微分再帰(b₀ = B_i(t₀) ≠ 0 の通常 Taylor chart —
  下限 ε_Z は M_r と同じ selector 規則)。
- **Z/G chart([GC4A2BR2-04] — 供給)**: t₀ 自身は零点でない(zf invariant (i):
  reduced 零点は t 座標で S から ≥ ρ/13 — 有限 m で C_i(t₀) ≠ 0 exact)ので、
  divisor 除去後の C_i に (EX-5) 再帰を適用(b₀ = C_i(t₀) ≠ 0)。有理 log 部は
  exact 公式 dⁿ/dyⁿ log(y − ζ_j) = −(n−1)!/(ζ_j − y)ⁿ で principal part を分離した
  合成式(u = Σ_j ±log(y − ζ_j) + 単位 log + 二次、jets は各項の和)。gcd 遷移では
  D の再取得後に C_i を読み直す(divisor_record の gcd_transition_ref)。
- C_i/C_12: divided-difference 座標での jets(多項式 × 指数の Leibniz 展開 — exact)。
- Q_C: jet map は raw 𝒥_n をそのまま使う(**再定義しない** — [GC4A2BR6-04])。κ での
  除算は床の式 max|𝒥_n|/κ ≥ c_{Q,C} の側にのみ現れる(κ → 0 での商の挙動は A.2c の
  transversality 義務として宣言のみ)。
([GC4A2B-06] 解消 — 「EX-5 のみ参照」を撤回し chart ごとに供給。)

**(N-8) confluent prefactor 次数 gate v2([GC4A2BR2-05] — deg ≤ 1 主張を撤回し
二分岐に弱める)**: pair i の t₀ 中心展開で affine 係数 β_i := ΔB_i + ΔA_i t₀、
二次係数 ΔA_i/2。**rate flag `affine-dominant` vs `quadratic-degenerate`** を
|β_i| と |ΔA_i|·(窓幅) の比で定義(band 定数 ε_C、半開規約)。
- **affine-dominant**: 正規化極限方向 h_i は affine(二次項は weighted witness
  |ΔA_i| ≤ s_i² と δ_i = s_i/λ から O(δ_i) で消える — v2 でもこの計算は有効)。
  prefactor deg ≤ 1。
- **quadratic-degenerate**(luna の反例 β_i ≈ 0 — 例: ΔB_i = −ΔA_i t₀): 正規化
  極限方向は y² 成分が支配し得る — **prefactor deg ≤ 2 を上限として認める**。
  この corner は rate flag で C_i^{(2)}/C_12^{(2)} sub-chart に route する。
**W_CONFL(2,2) の statement v2(A.2c で証明)**: q₁ − q₂ 非定数二次、**deg P_i ≤ 2**、
F = P₁e^{q₁} + P₂e^{q₂} ≢ 0 ⇒ ord_{t₀}F ≤ **B_CONFL**。数値診断(scratchpad、
Newton 探索): **deg ≤ 2 で genuine ord は 6 で頭打ち**(ord 6 = 200/200、≥ 7 解なし)
— sharp 目標 B_CONFL = 6。deg ≤ 1 部分形は sharp 4(consult #10 の消去骨格)。
**警告(A.2c の難度上方修正)**: deg ≤ 2 では crude Wronskian 勘定(6 関数系)の
上界は 9 を超えるため不十分 — **消去法による sharp 型証明が A.2c の必須義務**
(fallback なし。失敗すれば go/no-go の no-go 信号)。予算整合: B_CONFL = 6 ≤ 9 で
橋(ord Φ_p ≥ 10)と矛盾可能 ✓。

**scope(非主張)**: 床(c_J・c_{Q,C} — A.2c)、W_CONFL(2,2) の証明(A.2c)、
QR5 明示計算の移植(A.2c)、10 階上界(A.3b)。人間による査読は未実施。

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
| JF-NONCOMPACT | ord F ≤ 9 でも正規化 log jet の最小値が confluent 境界で 0 へ落ちる列 | **境界 continuation**(exact jet recurrence、高精度、ε 対数列、R_ε = max_{3≤n≤9−d₀}|v⁽ⁿ⁾|/(κλⁿ) の傾き判定 — finite difference 禁止)。fixture: ①二次比族(κ=0 分類の検証)②near-quadratic 族 η₁=η₂+δt² ③両 pair confluent 族 ④混成 scale 族 ⑤gcd-jump 族 ⑥**confluent 直接族 P₁e^{q₁}+P₂e^{q₂} の ord/jet 最小特異値探索(真の no-go テスト — 非零・非二次比配置が 0..9 jet を同時消滅させれば GC-4A no-go)** | **fixture ⑥ 結果**: deg ≤ 1 で genuine ord ≤ 4(150/150 到達・≥5 なし)、**deg ≤ 2 で ord ≤ 6(200/200 到達・≥7 なし)** — いずれも予算 9 内で **no-go 信号なし**。W_CONFL v2 の sharp 目標 = 6(deg≤1 部分形は 4、consult #10 消去骨格。crude Wronskian は deg≤2 で不十分 — A.2c は消去法必須)。①〜⑤ open。診断であり証明の代替ではない |
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

- v0.20(2026-08-18): **GC-4A.2b 受理** — R-GC4A2B R9 ACCEPTED、fixed SHA `a2302f3`
  (blocking/minor なし、8 責務 8/8)。§8.6 は以後 immutable(status 注記を除く)。
  go/no-go 最小集合の受理状況: A.0/A.1/A.2a/A.3a/A.2b/C.0 = 6/8、残り A.2c・B.0。

- v0.19.7(2026-08-18): R-GC4A2B R8 findings(blocking 3 + minor 1)適用 — [B01]
  R7 の 4 項恒等式論法は Φ_Q の向き(e^Q は B₂ 側)を取り違えており撤回。sup ノルム
  化した (6b) では κ = 0 が一致定理で関数レベルの Φ_{Q₀} ≡ 0 を与えるため、
  −B₁/B₂ = e^{Q₀} ⇒ u = Q₀ + 2πik ⇒ v ≡ 0 の**直接論法**に全面置換(chart 場合分け・
  L0・有理性がすべて不要になったことを明記)。[B04] boundary_route_chain の
  rank_after を union 型(∪ {exit})にし、終端 entry(exit-v0/exit-low-arity)は
  strict 降下条件の対象外・chain 終端と定義。[B05] 段 (4) の段内順序(4a exact →
  4b ε_Z → 4c ε_G)、段 (6) の λ_i 定義(pair 内差の weighted max — global λ と別物)、
  段 (7) の index tie-break を追加。[minor] v0.19.5 の撤回済み有理式主張に追記注記。

- v0.19.6(2026-08-18): R-GC4A2B R7 findings(blocking 5)適用 — [B01] **数学的訂正**:
  V_i = E(z_i) は超越的整関数で v0.19.5 の「多項式比 = 有理式」主張は誤り(撤回)。
  confluent (6c) は z₁z₂ 払いの 4 項指数多項式恒等式 + L0 型完全対消滅の場合分け
  (pairing 2 通り、E(−z) = e^{−z}E(z))で v ≡ 0 を再証明。[B02] κ = 0 を exact QR
  exit として分離(Q_C 適用域 = 0 < κ < ε_Q、0/0 排除、route 表に行追加)。
  [B03] α(Q₀) を chart 座標から record 注記に降格(網羅性補題は structural 座標 +
  κ の連続量のみで走る — 選択写像の連続性不要)。[B04] GCChartIdEnum(21 値)/
  FaceIdEnum/rank 型 + strict 降下 flag で record schema を完備化。[B05] selector を
  first-match 方式の段別 predicate 表として完備化(網羅性 = 段 (8) 補集合)。

- v0.19.5(2026-08-18): R-GC4A2B R6 対応。**工程ミスの記録**: v0.19.4 の適用スクリプトが
  途中 assert で write 前に停止し、[B04 の一部]/[B05]/[B06]/[B07]/[B08] が
  ディスク未反映のまま R6 に出た(v0.19.4 の版履歴記載は先行して書かれており不正確
  だった — 本版で実体を適用)。加えて R6 新規 findings: [R6-04] Q_C jet map の κ 付き
  再定義の残骸を raw 𝒥_n に統一、[R6-06] confluent (6c) の式に V_i を含めて修正
  (P₁V₁/P₂V₂ も有理式 — 補題 EL の適用は不変)、[R6-07] Q₀ の決定的 tie-break
  (argmin compact 上の辞書式最小)を定義。

- v0.19.4(2026-08-18): R-GC4A2B R5 findings(blocking 8 + minor 2)適用 — [B01] R_Q を
  global 定数に、[B02] p(t) と Q(y) の座標接続(α_k := p_k/λᵏ)で witness を型付け、
  [B03] κ の定義を係数ベクトルから閉円板 sup ノルムに変更(merge 次元問題の根絶、
  一致定理で κ=0⟺Φ_{Q₀}≡0)、[B04] 𝒥_n := v⁽ⁿ⁾/λⁿ に一本化(κ は床の式の側)、
  [B05] boundary_routes 全列挙表 + r≤1 exit を jet/overlap 契約から除外 + r/d₀ 単調性
  明示、[B06] GCRouteRecord-v2(q_band_witness/zero_flag_witness/boundary_route_chain
  の型)を versioned 拡張として宣言、[B07] anchor 差座標を値域表・N-2 表に波及、
  [B08] ε_Z を selector 定数列と stage (4) 述語に実装。

- v0.19.3(2026-08-18): R-GC4A2B R4 findings(blocking 5 + minor 1)適用 — [01] 𝒬_band の
  閉 polydisc 明示 + `q_band_witness`(p ∈ 𝒬_band の fail-closed 型保証)+ κ の連続性/
  min 到達(chart 別固定次元)+ κ=0⟺v≡0 の双方向証明(confluent 側は補題 EL)、
  [02] QR-near 述語 = (κ < ε_Q) の定義的下限、R_C を diagnostic に降格し κ_C := κ∘param_C
  (恒等)、[03] λ_C := global λ に統一 ⇒ K_λ = K_κ = 1・global K = 1(overlap 移送無損失、
  実値表)、[04] anchor を ≺(Re, Im 辞書式)の一意最小 class として決定的に定義、
  【注記(2026-08-18 追記): 本版の R6-06 対応に含まれた「P₁V₁/P₂V₂ は有理式」主張は
  誤りであり v0.19.6/v0.19.7 で撤回・置換済み】、
  [05] D3 を閉円板に修正(E_i = 0 は boundary route)+ 網羅性補題に rank (r, 9−d₀) の
  strict 降下による境界鎖の停止証明 + M_r jet map(ε_Z 下限)供給、[06] status surface
  同期(R5 査読対象)。

- v0.19.2(2026-08-18): R-GC4A2B R3 findings(blocking 5)適用 — [01] κ の統一親定義
  (band 内二次 gauge 上の最小化 — 全 chart 共通、κ_R ≡ 1 規約を撤回)、[02] 遷移損失を
  K¹⁰ に訂正 + λ_C の定義と overlap certificate の実体化、[03] C^{(2)} sub-chart の
  正式登録(β 判定不等式・半開規約・閉箱)、[04] §4 A.2c 行と chart 表を W_CONFL v2
  (deg ≤ 2、B_CONFL = 6)に同期、[05] gauge anchor(lexicographic 最小 class)の明示。

- v0.19.1(2026-08-18): R-GC4A2B R2 findings(blocking 5 + minor 1)適用 — [R2-01]
  係数正規化を ‖c‖_∞ = 1 球面へ変更(pivot=1 の非コンパクト性を撤回)+ 座標値域表 +
  band 半開規約、[R2-02] R_C を全 8 chart 家族で具体化 + fail-closed 未固定禁止 +
  overlap/遷移比較補題(隣接対 ≤ 7、K 比)、[R2-03] jets の chart 非依存性による遷移
  恒等式(床の移送 ≤ K⁹ 損失)、[R2-04] Z/G chart の jet map 供給(C_i(t₀) ≠ 0 exact +
  log principal part 公式)、[R2-05] **prefactor gate を二分岐に弱化**(affine-dominant
  deg ≤ 1 / quadratic-degenerate corner deg ≤ 2 — luna の反例 β = ΔB + ΔA·t₀ ≈ 0 を
  受諾)+ W_CONFL v2(deg ≤ 2、sharp 目標 6 — 数値 200/200、**A.2c は消去法必須で
  難度上方修正**)、[R2-06] 実験台帳の crude ≤ 11 表記を v2 結果に同期 + 本 resolution
  対応の記録。

- v0.19(2026-08-18): consult #10(Sol — A.2b アーキテクチャ裁定)により §8.6 を v2 へ
  全面改稿: 大域 X̄/metric/大域 J を撤回し QR5 P2 型の有限 chart atlas へ(merge-first
  前処理で λ > 0、ChartSpec 8 家族、ζ = λ(z−t₀) の collar scaling 訂正、gcd-transition
  record と jet range 埋め込み、決定的 selector + 部分列網羅性補題、chart-local κ_C と
  overlap 比較、chart 別 jet map、confluent prefactor deg ≤ 1 gate の証明、
  W_CONFL(2,2) statement 確定(crude ≤ 7・sharp ≤ 4 骨格))。R1 の 6 blocking は
  全てこの再構成で responsibility が固定された。

- v0.18(2026-08-18): GC-4A.3a accepted(R-GC4A3A R2 PASS、fixed SHA `926093c` — 最小集合
  6/8)。§8.6 GC-4A.2b JF9-NORM draft — global scale λ(weighted 座標 max、λ > 0)、
  adapted residual κ(QR locus への距離 — jet 逆算禁止)、compact 配置空間 X̄
  (confluent 面は divided-difference chart で付加)、境界面 closure 表(10 面)、
  A.2c への修正床 statement 宣言(J ≥ c_J·κ)。

- v0.17.2(2026-08-18): R-GC4A3A R1 findings 適用 — [01] D1/D2 の z=0 を実部勘定
  (collar 上 |Re z| ≥ 7/8)で閉鎖、E 零点の純虚性による除外表現に修正、[02] 帯上
  drift の Taylor 根拠を明示、[03] zf_witness を invariants 付きの型付き契約に、
  [04] scope に「D の零点は d₀ で保持(collar 対象外)」を明記。

- v0.17.1(2026-08-18): §8.5 (ZF-2) の鳩ノ巣を狭義判定で厳密化(各零点の排除 ≤ 3 窓、
  境界配置込み。draft の導出痕跡を除去)。
- v0.17(2026-08-18): GC-4A.2a accepted(R-GC4A2A R2 PASS、fixed SHA `5bb69af` — 最小集合
  5/8)。§8.5 GC-4A.3a PBK22-ZF draft — V 単位の graded 零点自由 collar(h_V)、
  SN-2|2 鳩ノ巣(N_A = 13、dist ≥ ρ/13 の source 窓)、zf_witness 出力契約。

- v0.16.1(2026-08-18): R-GC4A2A R1 findings 適用 — [01] (b) を「定数差(c=0 一致を
  含む constant-gauge equivalence)」に拡張し網羅化(v0.16 の「exact 一致」表現を上書き)、
  [02] 三角再帰を (n+1)b_{n+1} = Σ ℓ_j b_{n−j} に訂正(B=e^s 検算付き)+ u 係数式の
  添字修正、[03] W の連結性(区間)を明記。

- v0.16(2026-08-18): §8.4 GC-4A.2a JF9-EXACT draft — Taylor gauge(v = u − T₂u)、
  橋の恒等式 Φ_p = De^pC₂(1−e^v)、消滅次数の橋(ord ≥ d₀+N+1)、有限 m 二分岐
  (v ≡ 0 の二次比枝 or jet 3..9−d₀ 非全零 — shifted 一致は exact merge で W_c(c′) へ、
  全相殺は v ≡ 0 に回収)、jet の exact 三角再帰。

- v0.15.1(2026-08-18): JF-NONCOMPACT fixture ⑥ の初期結果を記録(confluent (1,1) 面の
  genuine ord ≤ 4 — no-go 信号なし。診断)。

- v0.15(2026-08-18): consult #9(Sol — JF₉ 設計)反映: 生 JF₉ の反例(二次比枝)と
  修正 target(v ≡ 0 or 横断残差 κ 床)、Φ_p 橋(ord ≥ d₀+N+1、予算は ord_{t₀}D)、
  confluent 面の主境界性と W_CONFL(2,2) 義務、A.2/A.3 の循環解消再分解
  (A.2a/A.3a/A.2b/A.2c/A.3b — go/no-go 最小集合を更新)、JF-NONCOMPACT の
  boundary-continuation fixture 6 本。

- v0.14(2026-08-18): GC-4A.1 accepted(R-GC4A1 R2 PASS、fixed SHA `50a4e45`)。
  最小集合 3/6(C.0・A.0・A.1)。次 = A.2 JF₉(設計 consult #9 → draft)。

- v0.13.1(2026-08-18): R-GC4A1 R1 findings 適用 — [01] g を ℂP¹ 値有理型 H の連続関数
  G(H) として再定義(共通零点で well-defined、恒等式は共通零点外で exact、検算例付き)、
  [02] c₁ の standing ceiling (0, 10⁻²] を PBK22 用に独立宣言(場合分けの排反・網羅を
  任意の c₁ で保証)、[03] divisor_record の cell 局所性と境界規約、[04] lead 下界は
  「候補解消経路」に訂正(obligation は A.2 受理まで open — v0.13 の「解消経路」表現を
  本版で上書き)。

- v0.13(2026-08-18): GC-4A.0 accepted(R-GC4A0 R4 PASS、fixed SHA `742c96a`)。
  §8.3 GC-4A.1 PBK22-F2 draft — double F2、対称正規化恒等式 g = |1+H|/max(1,|H|)
  (exact 天井 2)、case (a)/(b)/(c-ii) の初等完結、divisor 層別(共通因子の exact
  相殺 g = g̃、片側零点の排除観察、lead 下界 obligation の構造的解消経路)、
  深平坦窓の u-形。

- v0.12.3(2026-08-18): R-GC4A0 R3 findings(BLOCKED)適用 — [R3-01] accepted §7.1 を
  逐語復元し、拡張を versioned schema(GCDomainSchemaEnum-v2 = v1 + D-PBK-22v2/31v2/Mv2、
  resolved 行は v2 のみ使用・v1 凍結)へ変更、[R3-02] bi-graded に 0 < C_BRF < ∞ の
  正値性拘束、[R3-03] s_i(m) → 0 の入力仮定(SPLIT4 の child 形成から)を明記し
  閾値の非空性を根拠づけ。

- v0.12.2(2026-08-18): R-GC4A0 R2 findings 適用 — [R2-01] §7.1 canonical schema 表へ
  child_collision_witness_i を追補マーカー付きで反映、[R2-02] 一般 w_i child の witness
  型(全内部対の差分列挙)、[R2-03] 差分の座標束縛(§6 共通 gauge 後)、[R2-04]
  C_led := 3C_BRF の導出と正値性、[R2-05] BRF 閾値を m_BRF0/m_BRF1/m_BRF に改名
  (§6.3 の m₁ との衝突解消)。

- v0.12.1(2026-08-18): R-GC4A0 R1 findings(blocking 5)適用 — [01] 閾値を δ/(32C_led)
  へ(pair 数 2 の係数)+ 吸収算術の明示、[02] m₀/m₁ を eventual 量化(∀m ≥ M)へ、
  [03] pair 別 collision witness の定義と D-PBK-22/31/M への key 追加、[04]
  recenter_witness を cell 粒度の有限 map 型へ、[05] GCCostSpecEnum の closed-world
  新設と GCRouteSpec への結合明記。

- v0.12(2026-08-18): GC-4C.0 accepted(R-GC4C0 R3 PASS、fixed SHA `aa95124`)。
  §8.2 GC-4A.0 PBK22-BRF draft — 勾配評価・held 化 cell cover(sup|η̃| < 1/8 検証)・
  共通細分 graded 勘定(N_cell ≤ 19(1+Λ₁+Λ₂))・ray-wide ledger(≤ 3(sT + s²T²))・
  budget 吸収(m₀′ 存在)+ §8.2.5 spec 追補(bi-graded cost variant、recenter_witness、
  二重計上禁止)。

- v0.11.2(2026-08-18): R-GC4C0 R2 findings 適用 — [R2-01] §4 台帳 GC-4C.0 行を
  8 signature 表記へ同期、[R2-02] tie-break を孤立交差点・cell 境界帰属まで拡張、
  [R2-03] η̃ の正式定義(FR の η^C と対応)を記号定義に追加。

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
