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
上界 D_W(c) のみ消費するので、GC-1 は一般式 c(c+1)/2−1 で閉じてよい。**衝突極限でも valuation 5 は到達**(F3′ — 具体配置・profile・極限式の
正本は FR 文書 §7。本文書は消費値のみ参照)— 「静的接触のみの現象」ではない。

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
より広いが L0 は accepted 資産であり循環はない)。F3′(正本: FR 文書 §7)は c=3 上界の到達例。∎

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
| GC-4A.2c-core | A.2b、**主張域は GCRouteRecord-v3 条件付き(充足可能性は GC-5/GC-6 送り)** | W_CONFL(2,2) v2 消去法(正本 §8.7 (FL-2)、B = 6)/混合消去 ≤ 8/regular・C collapse/Z/G 以外の strata 床(consult #12 で component 分割) | **accepted(R-GC4A2CCORE R4 ACCEPTED、fixed SHA `c0c9e05`。A.2c-Z `5ea87ec` と併せトップレベル A.2c 確定)** |
| GC-4A.2c-Z ZG-NF | A.2c-core | Z/G 床: 同時 matching + projectivized defect の有限層別還元(consult #12 骨格)+ 全 box 最終合成 c_J | **accepted(R-GC4A2CZ R3 ACCEPTED、fixed SHA `5ea87ec`)**(トップレベル A.2c は core 受理を待って確定) |
| GC-4A.3b PBK22-D10 | A.3a/A.2b | 10 階上界・scale cap(WE₉ の純入力) | open |
| GC-4A.4 PBK22-WE9 | A.2/A.3 | 局所窓外挿(JF9/P4 の純 consumer) | open |
| GC-4A.5 PBK22-BOOT | A.4 | branch bootstrap、初回のみ ρ⁻⁹ の chain ledger | open |
| GC-4A.6 PBK22-ASM | A.5 | 全場合合成・最終 γ・cost spec・GCRouteSpec 昇格・fail-closed tests | open |
| GC-4B.0 ADAPT31 | GC-3、c=3 FR、A.2b atlas | triple divisor adapter の feasibility(chart 付き Weierstrass certificate — 接触次数 ≤ 5 だけでは足りず collar 内総零点数/valency が必要。**供給源 2 系統(prepared tree triple / radial 混成 3 原子和)の両方を scope に含む** — GC-4C.0 (3) 表。失敗は 3|1 の重大 no-go 信号)。**go/no-go 最小集合** | **accepted(条件付き go — §8.9、R-GC4B0 R8 PASS、fixed SHA `eee39bf`。TN-3 は GC-5 受理条件)** |
| GC-4B PBK-31 | B.0、GC-4A 系 | `3|1` kernel 本体。c=3 child certificate を消費し、旧 U_F/SVD 係数へ戻らない | open |
| GC-4C.0 SIG-AUDIT | GC-2/3 | 原子レベル radial signature の完全列挙(8)・margin 安定性・A/B/C dispatch 表・irreducible endpoint 特定・transition 有界性。**go/no-go 最小集合** | **accepted**(R-GC4C0 R3 PASS、fixed SHA `aa95124`) |
| GC-4C PBK-M4 | C.0、GC-4A/B | 多分岐 node kernel 本体(`[4]` held + separated compact + dispatch 接続) | open |
| GC-5-T0 BORD-3 | c=3 資産(補題 W_c/W′/FR-S1′/FR-S1″) | 3 原子 border 極限の**点一様 ord ≤ 5**(moving-center sequence 形 — TN-3 の消費補題。consult #13 で独立 packet 先行と裁定) | **drafted(§8.10、査読待ち R-BORD3 R1)** |
| GC-5-T1 TN-3 | GC-5-T0 | 比較補題 TN-3 本体(curve selection + 弧 leading-term + BORD-3 消費 — §8.9 (2c) の blocking obligation 解消) | open(GC-5-T0 受理後に着工) |
| GC-5 FR4-S1 | GC-1/2 | c=4 全 topology の exact J^{D_W(4)}-SVD frame、compact floor、tail、Gram、**TN-3(§8.9 比較補題 — B.0 counting の blocking downstream obligation。未解消の間 N_T 存在は条件付き)** | open |
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
  tau-zero, gcd-exact, kappa-zero, zeta-collision, zeta-infty}`(有限 enum —
  (N-5) route 表と 1:1。zeta-collision/zeta-infty は [GC4A2CR2-03] で追加)。
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
| 零点 exact 一致(G)(face_id = gcd-exact) | D 再取得((N-4) gcd-transition) | d₀ 増 |
| 零点衝突(Z 内、分子同士/分母同士 — face_id = zeta-collision) | 重複度統合後の Z(零点個数減 — 座標次元減の sub-box)または gcd-exact 経由で D | 不変(座標簿記)/ d₀ 増 |
| ζ → ∞(Z の ζ⁻¹ chart 原点 — face_id = zeta-infty) | 零点が collar 外へ = 零点個数減の Z sub-box | 不変(座標簿記) |
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

### 8.7 GC-4A.2c CONFL22(chart 床の証明 — **A.2c-core: R-GC4A2CCORE R4 ACCEPTED、fixed SHA `c0c9e05`**。A.2c-Z: §8.8 受理済み `5ea87ec`。**トップレベル A.2c は両 component 受理により確定**)

**設計記録(Sol consult #12、2026-08-18 — Z/G 床の裁定)**: R11–R14 の 4 round で
Z/G 零点近接の incremental 設計(band 分割→3 分割→cluster 評価→摂動補題)が
連続差し戻しとなったため Sol に裁定を求めた。裁定:
(i) **正規形路線は条件付き採用** — ただし逐次摂動除去でなく「small-root の
**同時最大 matching** → exact 因子除去 / **projectivized defect** → 正規形」+
EX-4 零集合一致 + defect strata 横断性。
(ii) 技術骨格: **§8.8 (NF-1)〜(NF-7) を参照**(唯一の authoring location —
[GC4A2CZR2-m2] で純 pointer 化)。
(iii) **component 分割**: A.2c-core(W_CONFL・mixed 消去・regular/C collapse・
Z/G 以外の strata — 本節の現内容から Z/G 固有部を除いたもの)と A.2c-Z
(§8.8: ZG-NF 補題・Z/G frontier 横断性・全 box 最終合成)に分け、component
acceptance とする。「Z/G 条件付きで A.2c 受理」とは記録しない。
(iv) no-go 評価: **amber 維持(中低 → 中)** — 1/4 反例・κ 乗法式誤り・
first-match 干渉は設計欠陥であり定理の反例ではない。実質的未解決義務は
δ/ζ^{n+1} 型摂動と 2 対同時 defect kernel。kernel に非 QR 方向が見つかれば red。
(v) 見積り: きれいに書き直して 3–4 round。
**本節(A.2c-core)の scope から Z/G strata の床・Z/G frontier・最終合成
最終合成(現 (NF-7))は除外され A.2c-Z へ移管** — (v-d′) の Z/G 分岐・(FL-4) の Z/G 帰着の
Z 固有部・[R12][R13] 系の零点近接ブロックは A.2c-Z の起草時に ZG-NF 形式で
全面書き直しとなる(現テキストは設計履歴として残置、効力は A.2c-Z に従う)。

**目的(core — [GC4A2CCORE-R2-02] で縮小)**: **非 Z/G の各 proof box** で
相対床 φ ≥ c·κ を証明し、per-box 床定数を供給する(global 合成 c_J は
§8.8 (NF-7) の義務)。**A.2c(core + Z)が GC-4A 系の go/no-go の本丸**である。

**設計記録(Sol consult #11、2026-08-18 — confluent-QR 角の裁定)**:
R2 併行で自己検出した 2 つのギャップ(FL-2 の床変換は「係数全零」でなく
「非零 QR 対象 ⇒ κ = 0」しか出ない/QR stratum の線形化で prefactor deg が
4 に上がる)に対し Sol 裁定:
(i) **一般の deg ≤ 4 二指数族に次数低下はない**(Π₂ + PΠ₂ = Π₄ — 多項式除法。
数値の sharp 10 は正しい)— 大域消去路線 (a) は不採用。
(ii) **exact QR 上では QR 恒等式(補題 EL ⇒ 指数差定数・prefactor 比例)が
二指数を一指数へ collapse させ、線形化は δΦ = e^qR、R ∈ Π₂ + PΠ₂ ⊆ Π₄ ⇒
ord δΦ ≤ 4(sharp)**。予算衝突は QR 横断線形化には現れない。
(iii) 採用路線 = **(b) proof atlas の selector からの分離 + stratified
transversality**。rescaling は T Z_QR に**含まれる**(⊕ は二重計上)。微分は
‖c‖₂ slice 上で行い、有限次元 norm 同値(‖c‖₂/‖c‖_∞ ∈ [1,2])で sup 正規化へ
戻す。(iv) no-go 評価 = **amber・中低**。真の no-go 信号は「refined stratum 上で
T Z_QR でない核方向」か「singular frontier(gcd-jump/degree-drop/Q-band 境界)
への列で φ/κ → 0 が再分類不能」の 2 つのみ。child-QR の pipeline 排除 (c) は
根拠なし、jet 拡張 (d) は不要、K_c 回帰 (e) は no-go test 失敗時のみ。

**(FL-0) proof cover と床の統一形式(consult #11 (iii) の採用 —
[GC4A2CR2-01] の Q_C 混在問題を根本解消)**:
**proof atlas は selector から分離する**。A.2b の selector・chart(受理済み —
不変)は record 簿記に使い、床の証明は **proof box の有限 cover** 上で行う:
各 structural chart の閉箱 K_C を **d₀ 分枝**で有限細分した閉集合族
  **K_{C,k} := closure{x ∈ K_C : d₀(x) = k}(k ∈ {0, 1, 2})**
(d₀(x) := ord_{t₀} gcd(P₁, P₂) は x の関数 — 上半連続なので各分枝の閉包は閉。
record chart の追加ではなく A.2c 内部の証明用 cover)。QR pairing 型 σ は
**box の添字ではなく**、box 内部の Z_QR の stratification((6-ii))の label で
ある([GC4A2CR4-03] — box 所属を σ で決める必要はない)。
**Q_C は record/帯域簿記専用に降格し、proof cover は structural chart のみ**。
**被覆補題([GC4A2CR4-03] — 写像でなく被覆で十分)**: 任意の admissible 配置
x は、selector の段 (3) を飛ばした first-match(段 (4)–(8) の述語は全域 —
段 (8) は補集合)で定まる structural chart C(x) の閉箱に属し、さらに自分の
d₀(x) 分枝 K_{C(x),d₀(x)} に属す。よって有限閉被覆 {K_{C,k}} は admissible
配置全体を覆う。**床は各 box 上の主張**なので、合成(§8.8 (NF-7))は
「x を含むいずれかの box の床」を適用すればよく、box への一意割当は不要。∎
高 d₀ 点が低 d₀ 分枝の閉包に入る場合の jet range は (N-4) の埋め込みが処理。
各 proof box 上で
  床関数 φ(x) := max_{3 ≤ n ≤ 9 − d₀} |𝒥_n(x)|(𝒥_n = v⁽ⁿ⁾(t₀)/λⁿ、
  添字範囲は box ごとに固定 ⇒ φ 連続)
に対し **∃c > 0: φ(x) ≥ c·κ(x)(∀x ∈ box)** を主張する。証明の共通骨格:
  (i) φ と κ の連続性(§8.6 (N-7) exact jet map と (6b))、
  (ii) **零集合一致**: 各 box で φ = 0 ⟹(EX-3 橋 + box の ord 上界補題
    W_c / W_CONFL / 混合消去)⟹ Φ_p ≡ 0 ⟹ κ = 0(§8.6 (6c))。
    逆向きは自明(κ = 0 ⇒ v ≡ 0 ⇒ φ = 0)— **{φ = 0} = {κ = 0} = Z_QR ∩ box**。
  (iii) **QR 近傍の相対床**: (FL-6) の stratified transversality が
    φ ≥ a·dist(x, Z_QR) と κ ≤ b·dist(x, Z_QR) から φ/κ ≥ a/b を与える。
  (iv) **QR から離れた閉領域**: {dist ≥ h₀} ∩ box は compact で φ > 0
    (零集合一致)⇒ inf φ =: c′ > 0、κ ≤ C_box ⇒ φ/κ ≥ c′/C_box。
frontier(gcd-jump・degree-drop・低 rank 面)は rank/次数の低い box から
**帰納的に処理**する((N-5) の rank 降下 — 有限鎖)。有限 cover 上の global min の
合成は §8.8 (NF-7) が行う。

**(FL-1) genuine 配置 chart(R、M_r(r ∈ {2,3,4})、S の非退化部)**:
φ_C(x) = 0 とは jets 3..9−d₀ の全消滅。x は admissible な有限 r-class 配置なので、
A.2a (EX-3) の橋 ord_{t₀}Φ_p ≥ d₀ + N + 1(N = 9 − d₀)により ord ≥ 10 の
deep vanishing が起こるが、(EX-4) の場合分け(r = 4)または同型の W_c(r) 勘定
(r ∈ {2,3}: Φ_p は r-class 指数結合、GC-1 補題 W_c より ord ≤ D_W(r) ≤ 5 < 10)
により Φ_p ≢ 0 では不可能。Φ_p ≡ 0 ⟺ v ≡ 0 ⟺ κ = 0(§8.6 (6c))は
κ > 0 と矛盾。∎(新しい解析は不要 — 受理済み A.2a/GC-1/A.2b の合成。)

**(FL-2) 補題 W_CONFL(2,2) v2 の証明(両側 confluent — C_12/C_12^{(2)})**:
*主張*: F = P₁e^{q₁} + P₂e^{q₂}、deg P_i ≤ 2、r := q₂ − q₁ 非定数(deg ≤ 2)、
F ≢ 0 ⇒ ord_{t₀} F ≤ 6。deg P_i ≤ 1 部分形では ord ≤ 4。
*証明*(消去法 — e^{q₁} で割り q₁ = 0、t₀ = 0 に正規化し、ord₀F ≥ 7 と仮定):
**Step 1(e^r の消去)**: P₂e^r = F − P₁ を微分して (P₂′ + P₂r′)e^r = F′ − P₁′。
2 式から e^r を交差消去:
  (P₂′ + P₂r′)·F − P₂·F′ = (P₂′ + P₂r′)·P₁ − P₂·P₁′  … (★)
**Step 2(次数勘定)**: (★) 右辺は多項式で deg ≤ max(3 + 2, 2 + 1) = 5
(deg(P₂′ + P₂r′) ≤ max(1, 2+1) = 3)。左辺の ord₀ ≥ min(ord F, ord F′) ≥ 6。
非零多項式 deg ≤ 5 の零位数は ≤ 5 なので **右辺 ≡ 0**:
  r′P₁P₂ = P₁′P₂ − P₁P₂′  … (†)
**Step 3(両者非零の排除)**: P₁, P₂ ≢ 0 とする。h := (P₂/P₁)e^r は {P₁ ≠ 0} 上で
h′ = e^r·[P₂′P₁ − P₂P₁′ + r′P₁P₂]/P₁² = 0((†))。よって接続成分ごとに定数、
P₂e^r − C·P₁ は整関数で開集合上 0 なので一致定理より **P₂e^r = C·P₁(全域)**。
C = 0 なら P₂ ≡ 0 で矛盾。C ≠ 0 なら e^r = C·P₁/P₂ は有理式 — **補題 EL**
(§8.6 (6c)。r 非定数多項式なら e^r は有理式でない)に矛盾。
**Step 4(片側零)**: P₂ ≡ 0 ⇒ F = P₁、deg ≤ 2 < 7 ⇒ F ≡ 0(仮定に矛盾)。
P₁ ≡ 0 ⇒ ord F = ord P₂ ≤ 2 < 7 で矛盾。∎
deg ≤ 1 部分形: (★) 右辺 deg ≤ max(2+1, 1+0) = 3、ord F ≥ 5 で同勘定 ⇒ ord ≤ 4。∎
*数値整合*: §9 JF-NONCOMPACT fixture ⑥(deg≤1: 150/150 が ord 4・≥5 なし、
deg≤2: 200/200 が ord 6・≥7 なし)と bound が一致(sharp)。
*床への変換*: C_12 系 chart の limit object は係数球面 ‖·‖_∞ = 1 上(§8.6 (N-2))。
まず **d₀ ≤ 2 は構造的上界([GC4A2CR1-03] で記号を A.1 に整合)**:
A.1 divisor_record の定義どおり **D = gcd(P₁, P₂)**(P_i は生の prefactor、
deg P_i ≤ 2)、reduced prefactor **P̃_i := P_i/D は互いに素**。
deg D ≤ 2 ⇒ d₀ = ord_{t₀}D ≤ deg D ≤ 2、かつ **deg P̃_i ≤ 2 − deg D ≤ 2 − d₀**。
C chart では prefactor は divided-difference 極限として現れるが、divisor データは
divisor_record の gcd_transition_ref で遷移する(§8.6 (N-4))— 以下の場合分けは
この reduced 次数 2 − d₀ を使う。
φ = 0 ⇒(EX-3 の橋)reduced part の ord ≥ 10 − d₀。**d₀ 場合分け**(gcd を
除くと reduced prefactor の次数が d₀ だけ下がることを使う — D の因子は両
prefactor から exact に割れる):
  - d₀ = 0: deg P̃ ≤ 2、W_CONFL bound 6 < 10 ✓
  - d₀ = 1: deg P̃ ≤ 1、W_CONFL(deg ≤ 1)bound 4 < 9 ✓
  - d₀ = 2: deg P̃ = 0(定数)⇒ 2-class 指数結合、W_c(2) = 2 < 8 ✓
いずれの d₀ でも reduced ord ≥ 10 − d₀ は該当 bound を超えるため
**Φ_p ≡ 0 が強制される** ⟹ v ≡ 0 ⟹ **κ = 0**(零集合一致 — (FL-0)(ii))。
(R1 版の「係数全零 ⇒ 球面と矛盾」は誤り(consult #11 で確認): 球面上の
**非零 QR 対象**(P̃₁ ∝ P̃₂ ∧ 位相差 = 二次 + 定数)は φ = 0 を実現するが、
それは κ = 0 の点であり相対床 φ ≥ c·κ と整合する。W_CONFL の役割は零集合の
**分類**(nonlinear zero set = QR 対象のみ)であって係数排除ではない。)∎

**(FL-2b) 片側 confluent の混合系(C_i/C_i^{(2)})**:
*主張*: F = P e^{q₀} + c₃e^{q₃} + c₄e^{q₄}(deg P ≤ 2、q₀/q₃/q₄ の差は
pairwise 非定数、c₃c₄ ≠ 0 または片方零)⇒ F ≢ 0 なら ord_{t₀}F ≤ 8。
*証明*(逐次消去): D := d/dy とする。
(a) F₁ := (D − q₃′)F は c₃e^{q₃} を exact に消し、
  F₁ = (P′ + PΔ₀₃′)e^{q₀} + c₄Δ₄₃′e^{q₄}、ord F₁ ≥ ord F − 1。
  ここで Δ_{ab}′ := q_a′ − q_b′(affine、非零 — 位相差非定数)。prefactor deg:
  side-0 は ≤ 3、side-4 は ≤ 1。
(b) F₂ := (D − q₄′)²F₁ は (affine)e^{q₄} を exact に消し(各 (D − q₄′) が
  prefactor 次数を 1 ずつ下げる)、F₂ = R e^{q₀}、deg R ≤ 3 + 2 = 5、
  ord F₂ ≥ ord F − 3。
(c) R ≢ 0 なら ord F₂ = ord R ≤ 5 ⇒ ord F ≤ 8。
(d) R ≡ 0 の場合: (D − q₄′)² の e^{q₀} 成分への作用は多項式写像
  T: G ↦ G″ + 2G′Δ₀₄′ + G(Δ₀₄′² + Δ₀₄″)。Δ₀₄′ = ay + b(a = A₀ − A₄、
  b = B₀ − B₄)とすると([GC4A2CR1-06] で場合分けを補完):
  a ≠ 0 なら T は deg d ↦ deg d + 2、leading 係数 ×a² ≠ 0 で単射。
  a = 0 なら b ≠ 0(位相差非定数)で T = G″ + 2bG′ + b²G は deg d ↦ deg d、
  leading 係数 ×b² ≠ 0 で単射。いずれも **T 単射**。
  よって R ≡ 0 ⇒ side-0 prefactor (P′ + PΔ₀₃′) ≡ 0 ⇒(同じ leading 勘定で)
  P ≡ 0 ⇒ F₁ = c₄Δ₄₃′e^{q₄} ⇒ ord F₁ ≤ 1 ⇒ ord F ≤ 2。いずれでも ord F ≤ 8。∎
(c₄ = 0 かつ R ≡ 0 の枝では P ≡ 0 から F = c₃e^{q₃}、ord F = 0 ≤ 8 —
[GC4A2CR1-06] の訂正: F ≡ 0 ではない。)予算整合: 8 ≤ 9 ✓。
*床への変換*: (FL-2) と同じ compactness + 球面正規化 + d₀ 場合分け(d₀ ≤ 2 は
(FL-2) と同じ構造的上界):
  - d₀ = 0: 本 bound 8 < 10 ✓
  - d₀ = 1: reduced prefactor deg ≤ 1 — 消去勘定を再実行すると (a) の side-0
    deg ≤ max(0, 1+1) = 2、(b) の R deg ≤ 2 + 2 = 4 ⇒ bound ≤ 3 + 4 = 7 < 9 ✓
  - d₀ = 2: reduced prefactor 定数 ⇒ 3-class 指数結合、W_c(3) = 5 < 8 ✓
いずれの d₀ でも bound 超過により Φ_p ≡ 0 ⟹ κ = 0(零集合一致 —
(FL-2) と同じ訂正が適用される)。∎

**(FL-3) M_r(r ∈ {2,3})の limit-object 床**: 極限対象は r-class 指数結合
(prefactor なし)。GC-1 W_c(r): ord ≤ D_W(r) = r(r+1)/2 − 1 ≤ 5 < 7。
(FL-2) と同じ変換で床が出る。∎(r = 4 内部点は (FL-1) が処理。)

**(FL-4) Z/G chart【[GC4A2CCORE-R2-03]: 本 block の Z/G 固有主張は
non-operative(正本 = §8.8 ZG-NF)— 以下は「Z/G 内点 = genuine 配置」の
観察のみ core の active claim として残る】**:
*鍵となる観察*: Z/G chart の domain 内点は **genuine な有限 2|2 配置の
座標表示に過ぎない**(零点座標 ζ_j + unit データは §8.6 (N-7) の
再パラメタ化であり、対象クラスは変わらない)。よって零点排除 (iii) は
**(FL-1) がそのまま適用される**(EX-3 橋 + EX-4 二分法は B_i(t₀) の大小や
零点の位置に依存しない有限配置の定理)。Z/G 固有の「新しい極限対象クラス」は
存在しない: 閉箱の境界面(ζ 衝突 = G/D、ζ → ∞ = ζ⁻¹ chart、係数消滅・
confluence 等)はすべて boundary_routes((N-5))で他 chart に送られ、鎖の
終端対象は genuine 配置((FL-1))か confluent prefactor 対象((FL-2)/(FL-2b))の
いずれかに分類される。∎
**d₀ ≥ 3 の record は生成禁止(fail-closed — (FL-2) の構造的上界 d₀ ≤ 2 により
空虚に真)**。

**(FL-5) D/S chart([GC4A2CR1-04] — exact 極限写像を供給)**:
- **D_{i,0}/D_{i,∞}**: domain 内点(E_i band 内)は genuine 配置 ⇒ (FL-1)。
  **E_i の型付き定義([GC4A2CR2-02] — §8.3 には無いためここで定義し、§8.6 (N-2) の
  「D3: 閉単位円板」と整合させる)**: pair i の 2 原子を係数絶対値の pivot 順
  (|c_{ia}| ≥ |c_{ib}|、等号は ≺ で tie-break)に取り、
    **E_i := c_{ib}/c_{ia} ∈ 閉単位円板**。
  **exact 極限写像**: この pivot 表示で pair i の side 関数は
    B_i = c_{ia}(e^{q_{ia}} + E_i·e^{q_{ib}})。
  E_i → 0 で **B_i → c_i e^{q_{ia}}·(unit) を係数ごと exact に収束**(E_i は
  線形パラメタ — 差は |E_i|·sup|e^{q_{ib}}·unit| で閉箱上一様)。極限対象 =
  3-class genuine 配置 ⇒ (FL-1) の W_c(3) 勘定(D_W(3) = 5 < 10 − d₀ ∀d₀ ≤ 2)。
  E_i → ∞ は ζ⁻¹ 側で同型(役割交換)。∎
- **S_{1≺2}/S_{2≺1}**: domain 内点は genuine 配置 ⇒ (FL-1)。**τ = 0 面の exact
  極限写像(moment 座標の型付き定義 — [GC4A2CR2-02])**: 劣位 pair(scale
  λ_sub := min(λ₁, λ₂))の side 関数を pair 平均位相 q̄ := (q_a + q_b)/2 と
  半差 Δ := (q_a − q_b)/2 で書くと恒等式
    c_ae^{q_a} + c_be^{q_b} = e^{q̄}[(c_a + c_b)cosh Δ + (c_a − c_b)sinh Δ]。
  Δ = (ΔB·y + ΔA·y²/2)/2 は τ → 0 で weighted witness(|ΔB| ≤ λ_sub、
  |ΔA| ≤ λ_sub²)により閉箱上一様に 0 へ(cosh/sinh の Taylor 剰余は
  |Δ| ≤ 1 で絶対収束級数の尾 — 一様)。**moment 座標**: Δ̂ := Δ/λ_sub
  (正規化方向 — 閉箱値)、劣位 side の λ_sub-展開係数
    m₀ := c_a + c_b、m₁ := (c_a − c_b)、m₂ := (c_a + c_b)/2
  を用いた exact 展開 e^{q̄}[m₀ + m₁·(Δ̂λ_sub) + m₂·(Δ̂λ_sub)² + O(λ_sub³)]
  の λ_sub-次数ごとの主要項を projective 正規化(‖(m₀, m₁λ_sub, m₂λ_sub²)‖∞
  で割る — S chart の閉箱座標)したもの。正規化極限は
  **deg ≤ 2 prefactor 対象** — (FL-2b) の混合系 F = P e^{q̄} +
  (支配 pair の 2 class)そのもの(N-8 の affine/quadratic 二分岐とも整合)。
  床は (FL-2b) の bound 8 と d₀ 場合分けで閉じる。moment 全退化
  (m₀ = m₁ = m₂ = 0 方向)は係数消滅面 = boundary_routes の c_a = 0 行で
  M 系へ(rank 降下)。∎
  (QR5 P2 の kernel 指数計算は本 packet では消費しない — ord 上界はすべて
  W_c(r)/W_CONFL/混合消去で自給。[GC4A2CR1-04] の「外部参照」問題は解消。)

**(FL-6) stratified transversality(consult #11 の骨格 — **scope 限定
([GC4A2CCORE-R1-02]): 本節の主張は非 Z/G strata に対する generic collapse/
tube 補題であり、Z/G strata(零点近接・Taylor/pole 分割)への適用は §8.8
ZG-NF が本補題を消費する形で行う(依存方向: core → ZG-NF、循環なし)**)**:
*主張*: 各 proof box で φ(x) ≥ a·dist(x, Z_QR ∩ box)(a > 0 は box 定数)。
*証明*(6 段):
**(6-i) QR incidence の定義と接空間(consult #11 Q3、[GC4A2CR3-03] で適用域を
限定)**:
  Z̃ := {(x, Q) : Φ_Q(x) ≡ 0}、Z_QR := x-射影。**各 smooth stratum の内部
(Q-band 内部・射影が非特異な branch 上)** で接空間は
  **T_x Z_QR = {ξ : ∃Q̇ ∈ Π₂, δ_ξB₁ + e^Q(δ_ξB₂ + Q̇B₂) = 0}**。
Q-band 境界では Q̇ は tangent cone に制限され、射影特異点では branch union と
なるが、**そうした点はすべて (6-ii) の frontier stratum に分類され、(6-v) の
法束論法はそこでは使わない**((6-vi) の tube 帰納が処理)。
  side rescaling (δB₁, δB₂) = (aB₁, bB₂) は QR 点で Q̇ = a − b を選べば
  この式を満たすので **rescaling は T Z_QR に含まれる**(R1–R2 版の
  「⊕ rescaling」は二重計上 — 撤回)。
**(6-ii) stratum 分類(proof box ごと)**:
  - **regular stratum**(4 class 分離 band 内): W_c(4) 独立性により QR は
    位相の完全対形成 {q₁a, q₁b} = {Q + q₂a, Q + q₂b} + 係数対条件。明示
    パラメタ化(side-2 データ, Q, 定数差対)で smooth。
  - **C stratum**(confluent box): 補題 EL により P₁ ∝ P₂ ∧ fitted Q 後の
    指数差 = 定数。パラメタ化(片側 prefactor, 共通位相データ)で smooth。
  - **mixed / gcd-jump / degree-drop / Q-band 境界**: 別 stratum とし、
    QR 恒等式の成立が追加の confluence/係数消滅を強制する場合は frontier
    stratum(より低い rank/次数の box)へ送る — (FL-0) の帰納処理。
  これで「Z_QR 全体を単一 manifold と扱う」誤りを避ける。
**(6-iii) 核の特徴づけ = T Z_QR(collapse 論法 — [GC4A2CR3-01] で stratum
別に修正)**: QR 点 x* で δ𝒥(ξ) = 0 とすると δv の jets 3..(9−d₀) が全零。
橋の微分は v = 0 上で
  **δΦ_p = −De^pC₂·δv** ⇒ ord δΦ_p ≥ 10。
一方 QR 点では fitted Q による **pair ごとの collapse** が働く:
- **regular stratum**(2|2 対形成 {q₁a, q₁b} = {Q+q₂a, Q+q₂b}): 各対が
  1 指数に collapse し、線形化は **2 指数系**
    δΦ_p = e^{q₁a}R_a + e^{q₁b}R_b、R_a, R_b ∈ Π₂
  (係数摂動 deg 0 + 位相・gauge 摂動 deg ≤ 2 — prefactor は定数なので
  P·δq 型の次数上昇はない)。q₁a − q₁b 非定数なので **W_CONFL v2 の bound 6**
  が適用され、ord ≥ 10 > 6 ⇒ δΦ_p ≡ 0。
- **C stratum**(confluent — P₁ ∝ P₂ ∧ fitted 指数差定数): 全体が 1 指数に
  collapse し δΦ_p = e^q·R、R ∈ Π₂ + PΠ₂ ⊆ Π₄ ⇒ ord ≤ 4(sharp 4 —
  consult #11 Q1)。10 > 4 ⇒ δΦ_p ≡ 0。
いずれの stratum でも δΦ_p ≡ 0、すなわち ξ は (6-i) の incidence 式を満たし
**ker δ𝒥 = T Z_QR**。一般の deg ≤ 4 二指数族(sharp 10 — §9 DEG4-SHARP)は
いずれの stratum の線形化にも現れない(regular では prefactor 定数、C では
一指数)。
**(6-iv) 滑らかな正規化 slice**: ‖c‖_∞ = 1 球面は tie 点で非滑らか。微分は
**‖c‖₂ = 1 slice** 上で行い、norm 同値で sup 正規化へ戻す。
**変換式([GC4A2CR12-05]、[GC4A2CR13-08] で記号を整理)**: slice の取り替えは
全係数の一斉 rescale c ↦ sc(s ∈ [1, s_max])。**φ は不変**(v = log 比の
jets — side scale は T₂ が殺す)、**κ は 1 次同次**(Φ_Q は係数に線形)。
ℓ² slice 上の床を **φ ≥ a·κ|_{ℓ² slice}** と書くと(a は ℓ² 正規化での床
定数 — 線形床)、sup 正規化点 x では ℓ² 正規化点 x_ℓ = s⁻¹x に対し
κ(x) = s·κ(x_ℓ)、φ(x) = φ(x_ℓ) なので
  **φ(x) = φ(x_ℓ) ≥ a·κ(x_ℓ) = (a/s)·κ(x) ≥ (a/s_max)·κ(x)**
— 線形床が線形床に移り、損失は s_max の 1 乗(4 係数: 2、joint: √6)。
旧「(定数)^9」は撤回済み。
**(6-v) 法束の最小特異値と Taylor([GC4A2CR3-02]、[GC4A2CR4-01][02] で
順序と frontier 横断性を精密化)**:
**(v-a) 内在的 witness と Q-band 境界 strata の排除([GC4A2CR7-B1] で定義域と
supply を A.2a/GCRouteRecord の実 interface に接続)**:
**主張域の明示([GC4A2CR10-B1] で v3 に統一)**: 本 packet の床は
**A.2a-admissible 窓上の非終端配置**(u = Log(−H) が A.2a の branch 決定
(§8.4 — 窓上の固定 branch)で定義され、**GCRouteRecord-v3**((v-a))の
witness 群が全て verified の record が生成し得る配置)に対する主張である — 床の消費元(JF₉ target)もこの窓上でのみ κ-正規化 jet を
要求するため、これは制限ではなく contract の一致。**u の branch は A.2a の
決定で固定**されるので p(x) := T₂u(x) は一価・滑らか(円筒 quotient は不要 —
R6 版の ℂ/2πiℤ 記述は撤回し、𝒬_band は §8.6 の ℂ³ polydisc のまま)。
  **Z_QR := {x ∈ 主張域 : Φ_{p(x)}(x) ≡ 0}**(witness は p(x) 一意 —
  min 選択・canonical strip とも不要)。
κ = 0 ⟺ x ∈ Z_QR は q_band_witness(p(x) ∈ 𝒬_band — typed fail-closed)の
下で (6c) と同値。
**band 所属は定義的([GC4A2CR8-B1] — 解析的 supply 主張を撤回)**:
p(x) ∈ 𝒬_band は **q_band_witness(fail-closed)の verified flag そのもの**
であり、主張域(witness 全 verified の record が生成し得る配置)では
**定義により成立**する — record ごとの log-jet 上界を global 定数に集約する
解析的評価は床の証明には**不要**(R7 版の C_p supply chain 主張は撤回)。
witness の**充足可能性**(実際の PBK-22 route record が flag を満たすこと)は
record 生成側の義務であり、**GC-5/GC-6 への明示的送り**とする(scope 参照)。
**境界 stratum の排除 — GCRouteRecord-v3 の正式宣言([GC4A2CR9-B1])**:
  `GCRouteRecord-v3 := GCRouteRecord-v2(§8.6 (N-1) — 不変) +
   q_band_witness-v3`、
  `q_band_witness-v3 := (α₀, α₁, α₂ の実値 — **α_k := p_k/λᵏ**(p(x) = T₂u の
   t₀ 中心係数 p_k、k = 0,1,2), verified flags **|α_k| ≤ R_Q/2**)`。
v2 の q_band_witness(|α_k| ≤ R_Q)は不変のまま、v3 は flag を強める方向の
versioned 拡張。**型不変条件([GC4A2CR10-B1])**: v3 の α field は v2 の
α field と**同一値**でなければならない(α_k = p_k/λᵏ、p = T₂u、λ = §8.6 (N-0)
の global λ — 重複 witness が別値を持つ record は生成禁止(fail-closed))。
**A.2c の床は v3 record のみを消費**し、主張域を
  **「GCRouteRecord-v3 が生成し得る(全 flag verified の)配置」**
と厳密に定義する(v2-のみの record は本 packet の主張域外)。この域では p(x) ∈ 𝒬_band 内部(margin 2 倍)が**型的に**
成立 ⇒ **Q-band 境界 stratum は内在的 incidence に対して空(定義的)**。
(FL-0)(ii) の Φ_p ≡ 0 ⇒ κ = 0 は κ ≤ sup|Φ_{p(x)}| = 0 で直ちに閉じる。
**(v-b) stratum poset の順序 = 次元([GC4A2CR4-01]、[GC4A2CR5-B2] で型別
次元表を供給 — §8.6 の rank (r, 9−d₀) とは別の A.2c 内部順序)**: Z_QR の
strata は (6-ii) の明示パラメタ化で各々局所閉・有限個。frontier 型ごとの
追加閉条件とそれが拘束する**自由パラメタ**:

**stratification は raw 係数の固定 ambient で取る([GC4A2CR6-B2]、
[GC4A2CR7-B2] で次元勘定を実体化)**:
**固定 ambient([GC4A2CR8-B2]、[GC4A2CR9-B2] で box 家族別に分離)**:
(0c) gauge 固定後の生データを **box 家族別の compact ambient** に載せる:
  - **plain 家族(M/R/S/D/Z/G — prefactor 座標なし)**:
    X_amb := {(c_j) : ‖c‖₂ = 1} × {anchor 差 ∈ 閉円板 ⊂ ℂ⁶}
    (実次元 7 + 12 = 19)。
  - **C 家族(prefactor 対象 — [GC4A2CR10-B2] で joint 球面に統一)**:
    全 class の scale データを**単一の joint ℓ² 球面**に載せる:
    C_12 型は {(P₁, P₂) ∈ ℂ³×ℂ³ : ‖(P₁,P₂)‖₂ = 1}(実次元 11)、
    C_i 型は {(c₃, c₄, P) ∈ ℂ²×ℂ³ : ‖(c₃,c₄,P)‖₂ = 1}(実次元 9)—
    plain 係数と prefactor 係数を**同じ球面**で正規化するので、
    **P_i = 0 面と c_a = 0 面は同種の「class scale 消滅」face** になり
    ([R10-B2c] の別座標問題を解消)、effective coefficient の別定義は不要。
    X_amb := {joint 球面} × {anchor 差閉円板}(実次元 11+12 = 23 / 9+12 = 21)。
**境界 strata の訂正([R10-B2a])**: 球面に境界面はない — X_amb の境界は
anchor 差閉円板の球面のみ(λ 正規化で max = 1 が常時成立するため、この面は
内部点の再表示)。
**P_i = 0 face の routing([R10-B2b])**: joint 球面上の P_i = 0 は当該
confluent class の消滅 = **support-drop frontier** で、送り先は当該 class を
除いた **plain / 低 support の C 家族 box**(残る class の joint 球面へ再正規化
— 球面上 ‖残り‖₂ = 1 に rescale する連続写像)。jet range は不変(d₀ は残存
class 対の divisor データ — 死んだ class の d₀/deg label は drop)。
各 ambient は compact。帰納は stratum の実次元(家族横断で有限個・上界 23)に
関して行う。
**局所閉有限分割**: 離散 label(support pattern ⊆ {1..4}、d₀ ∈ {0,1,2}、
raw deg 対 ∈ {0,1,2}²、QR pairing 型)の各値組合せに対し、
  stratum := {label の等式条件} ∖ {より深い label の条件}
は「解析的等式系 ∖ 閉集合」= **局所閉**。label 組合せは有限なので分割は有限。
**境界 strata の列挙([GC4A2CR11-B2] — 旧「P 閉箱の面」の列挙を撤回)**:
X_amb 自体の境界は **anchor 差閉円板の球面のみ**(ℓ² 球面と joint 球面に
境界はない)。この面は §8.6 (N-0) の λ 正規化により内部点の再表示(max = 1 は
定義で常時成立)。degree branch の境界 = raw 先頭係数消滅(下表)、d₀ branch
の境界 = 下表の消滅条件、class scale 消滅(P_i = 0 / c_a = 0 — joint 球面上の
同種 face)= support-drop routing(上記 — 残存 class の球面再正規化 +
label drop。**C_i の c_a = 0 面も同じ routing** — joint 球面上で対称)。
**limit object の正規化との同値**: §8.6 (N-2) の C 系 limit object は
‖·‖_∞ = 1 球面で受理済み(不変)。proof cover 側の joint ℓ² 球面とは
(6-iv) の norm 同値(定数 ∈ [1, √6])で相互変換され、床定数の有限損失のみ —
両正規化の併存は矛盾ではなく slice の取り替え。
**frontier の余次元 ≥ 1(型別)**:

| frontier 型 | 追加方程式(X_amb 上の解析関数) | 余次元根拠 |
|---|---|---|
| support 減 | c_a = 0 | c_a は X_amb の自由座標(球面 slice 上で局所自由)— 1 複素条件で実余次元 2 |
| confluence 到達 | (ΔA, ΔB)_pair = (0,0) | 位相差は自由座標 — 実余次元 4 |
| gcd-jump(ord_{t₀}: k → k+1) | **座標消滅条件そのもの([GC4A2CR8-B2] — d₀ は「点 t₀ での ord」なので subresultant は不要)**: t₀ 中心座標で d₀ ≥ 1 ⟺ P₁(t₀) = P₂(t₀) = 0(2 複素条件)、d₀ ≥ 2 ⟺ さらに P₁′(t₀) = P₂′(t₀) = 0(計 4 複素条件) | 各条件は raw 係数の**線形**関数で、stratum {d₀ = k} 内部では次の条件が非零(d₀ = k の定義)⇒ 零集合は proper(線形部分空間との交差)= 実次元 strict 減 |
| degree-drop | raw 先頭係数 = 0 | 先頭係数は自由座標 — 実余次元 2 |

connected 解析的 stratum 上で恒等零でない解析関数の零集合は**実次元を strictly
下げる**(解析集合の次元論)ので、frontier 関係は dim を strictly 下げ、
帰納は **dim に関して** well-founded(strata 有限個・dim ≤ N_amb)。
**(v-c) 全 stratum 型での collapse([GC4A2CR5-B3] — mixed の空性で完備化)**:
(6-iii) の二分法(regular = 2 指数 deg ≤ 2 → W_CONFL 6 / C = 1 指数 Π₄ →
ord ≤ 4)の適用範囲:
- **mixed(C_i 型 — 片側 confluent・片側 2 class)の内部に QR 点は存在しない**:
  QR 恒等式 P₁e^{q₀} + e^Q c₃e^{q₃} + e^Q c₄e^{q₄} ≡ 0 は **3 相異 class の
  指数多項式恒等式**であり、多項式 prefactor 付き独立性((FL-2b)(d) と同じ
  T 単射性の逐次消去、または W_c 系)により全係数零を強制 — stratum 内部
  (class 相異・係数非零)と矛盾。よって mixed box の Z_QR は frontier
  (C_12 型 confluence または support 減)にのみ現れ、**mixed 型の線形化
  collapse は不要**(各 frontier 型が処理)。d₀ = 2 の FL-2b 比較懸念も同時に
  消滅(mixed の QR 線形化そのものが空)。
- gcd-jump: jet range が {3..9−d₀} に縮むが d₀ ≤ 2 で 10 − d₀ ≥ 8 > 6 > 4 は
  保たれ、regular / C の二分法がそのまま成立。
- degree-drop・support-drop: prefactor / 指数が減るだけで同じ二分法のより
  簡単なインスタンス(support が「片側全滅」に達する面は (v-d′) — Z_QR が
  接近しない)。
よって **QR 点を持つ各 stratum で ker δ𝒥 = T S**((6-iii) の論法)。
**(v-d) 帰納法**:
*基底*(dim 最小の strata — frontier なし・閉): 法単位球面束 compact、
σ(x*, ξ) := max_n |δ𝒥(ξ)| は連続・(v-c) より各点正 ⇒ σ₀ > 0。
*帰納段*: dim = D の stratum S_σ の frontier strata S_τ(dim < D)には tube 床
(半径 h_τ の管状近傍 N_τ で φ ≥ a_τ·dist(·, Z_QR))が確立済み。
**S_σ ∖ ∪_τ N_τ は compact**(閉包から frontier の開近傍を除いた閉集合 —
closure(S_σ) ∖ S_σ ⊆ ∪_τ N_τ)。その上の法単位球面束は compact ⇒
σ₀(σ) > 0 ⇒ tube 半径 h_σ := σ₀(σ)/(2C₂)。
**(v-e) 一様 Taylor 定数**: C₂ := sup_box ‖Hess_x (𝒥_n)_n‖(exact jet 式は
閉箱の正規化座標で解析的、compact 上で有限)。tube 内で
φ(x) ≥ σ₀(σ)·h − C₂h² ≥ (σ₀(σ)/2)·h(h := dist ≤ h_σ)。
**(v-d′) 定義域と面延長([GC4A2CR6-B4]、[GC4A2CR7-B4] — 「終端 box」方式を
撤回し、面延長補題で置換)**: 床の主張域は (v-a) の A.2a-admissible 窓上の
**非終端配置(merge 後 r ≥ 2)**。R7-B4 の指摘どおり「終端 box への routing で
退化が解消される」は selector から導出できないため**撤回**し、代わりに:
**面延長補題(box 家族別 — [GC4A2CR8-B4])**: 各 proof box の φ と κ は
**box の閉座標域全体(全ての面を含む)へ連続に延長する**。
*証明*: (a) φ = max_n |𝒥_n|: 𝒥_n は v の jets。side の log の発散し得る成分は
**定数(log スケール — 例: log c₂)と二次以下(位相)のみ**であり、いずれも
T₂ 減算が exact に消すため、v の jets 3..9−d₀ は係数消滅面・side 縮退面まで
含めて box データの連続関数。分母の一様下界は **box 家族別**:
  - M/R/S/D 系 box: b₀ = B_i(t₀)、selector の ε_Z 下限((N-5) 段 (4) —
    これらの box は |B_i(t₀)| ≥ ε_Z の領域)。
  - **Z/G 系 box【[GC4A2CCORE-R3-02]: 本項目は historical / non-operative —
    正本 = §8.8 ZG-NF】**([GC4A2CR9-B4]、[GC4A2CR10-B4] の設計履歴):
    (N-7) の Z/G jet map を **log 微分形** u′ = C₁′/C₁ − C₂′/C₂ +
    (divisor・二次項)で評価する。比 C_i′/C_i は係数 scalar に**不変**
    (scalar の log は定数で T₂ が殺す)。正規化は先頭係数でなく
    **C̃_i := C_i/‖C_i‖₂(係数ベクトルの ℓ² 正規化 — [R10-B4b]:
    degree-drop 面でも定義される。C_i ≡ 0 は class 死 = routed frontier)**
    とし、C̃_i′/C̃_i = C_i′/C_i(scale-free)。
    【以下の零点近接ブロックは **historical / non-operative**
    ([GC4A2CCORE-R2-03] — 正本は §8.8 ZG-NF。設計履歴として残置し、
    active claim surface から除外する】
    **零点近接の分割([GC4A2CR13-01][02][03] — 全面再構成)**:
    **前提となる構造的事実**: (ZF-1) により V-unit の零点は collar に入らない
    ので、**collar 内の零点は P̃_i 由来のみ = 各 side 高々 2 個・計 ≤ 4 個**
    (deg P̃_i ≤ 2)。よって「cluster」は高々 2 元であり、多重スケール階層は
    生じない。
    **first-match 順序([R13-01] — §8.6 (N-5) 段 (4) の内部順序に整合)**:
    (4a) 零点 exact 一致(cross-side)→ D、(4b) same-side 近接 → Z sub-box、
    (4c) cross-side 近接(ε_G 帯)→ G — 同時成立時はこの順の first-match
    (排他性は半開 band + 順序評価)。
    **same-side 2 元 cluster の下界([R13-02] — 「強め合い」三角不等式を撤回し
    連続 2 指数評価に置換)**: same-side 零点は同符号 σ・高々 2 個。
    x := ζ₁/ζ₂(|x| ≤ 1 に取る)に対し、任意の n で
      max(|xⁿ + 1|, |x^{n+1} + 1|) ≥ 1/4
    (両方 < 1/4 なら |xⁿ| ≥ 3/4 かつ x = x^{n+1}/xⁿ は B(−1,1/4) の 2 元の比
    で |x − 1| ≤ 2/3 — すると xⁿ は 1 の近傍冪の回転で偏角が π に届くには
    |x| ≤ 1 との併用で |xⁿ + 1| ≥ 1/4 に矛盾 — 初等算術)。よって
      max_{n, n+1} |σ(ζ₁^{−n} + ζ₂^{−n})| ≥ |ζ₂|^{−n}/4
    が **どの連続 2 指数の組でも**成立し、jets 範囲 {3..9−d₀}(長さ ≥ 5 ≥ 2)
    内で発散が genuine。単独零点(cluster サイズ 1)は自明に |ζ|^{−n}。
    **定量的発散と M の有限性([R13-03])**: 小零点集合
    S_small := {j : |ζ_j| < r_pole} は上記 first-match の後、(i) 空、(ii) 単独、
    (iii) same-side 2 元 cluster、のいずれか(cross-side 小対は (4a)(4c) で
    routed 済み、same-side 3 個以上は零点数上限 ≤ 2/side で不可能)。
    残余 M := sup(S_small 外の零点 principal part + unit log-jet + 二次項)は、
    S_small 外の零点が定義により |ζ| ≥ r_pole、unit log-jets(≤ 9 階のみ必要)
    が (ZF-1) collar 零点自由 + compact 両側有界の Cauchy 評価で有界、なので
    **有限(box 定数)**。**r_pole := min((2·(1+4M))^{−1/3}, ε_G-band/2)**
    (band 上限により S_small の要素は互いに collision 帯内 = (ii)(iii) の形に
    限られることが幾何的に保証される)。(ii)(iii) いずれも上の下界から
    |ζ| < r_pole ⇒ φ ≥ (1/4)|ζ|^{−3} − M ≥ 1。
    **cross-side 近接(G box)と η ≳ κ 帯([R13-05])**: 下の摂動補題は
    η ≤ κ·c_lower/(2(1+c_lower)C_pert) の帯でのみ使い、**η がそれより大きく
    δ < ε_G のままの領域は gcd-jump stratum の tube((v-d) の大域次元帰納 —
    d₀-jump strata は帰納の正式な一員でありその tube 床が近傍を覆う)が
    処理する** — 摂動補題単独での被覆主張は撤回。
    **G-box 摂動補題([GC4A2CR12-03]、[GC4A2CR13-04][06] で定量化と帰納を
    完備化)**: cross-side 近接対 (ζ_a 分子側, ζ_b 分母側)(δ := ζ_b − ζ_a、
    |δ| < ε_G band)。**x∖pair の定義**: 分子から因子 (y − ζ_a)、分母から
    (y − ζ_b) を除いた配置 — P̃ の deg が両側 1 ずつ下がる **同じ Z/G 家族の
    低 deg-branch box** の点(raw ambient では因子除去は係数の多項式写像)。
    u の差は exact に log(1 + w)、w := δ/(y − ζ_b)、collar 上
    |w| ≤ η := |δ|/d_collar(d_collar := collar 距離下限 — box 定数)。
    **jets 摂動**: |dⁿ/dyⁿ log(1+w)|_{y=0}| ≤ n!·η/(d_collar·(1−η))ⁿ(Cauchy —
    log(1+w(y)) は |w| < 1 の帯で解析的)⇒ |φ(x) − φ(x∖pair)| ≤ C_jet·η、
    C_jet := 9!/(d_collar(1−η₀))⁹(η₀ < 1/2 の band 上限)。
    **κ 摂動**: Φ_Q(x) = (y − ζ_a)/(y − ζ_b)·Φ_Q(x∖pair) 型の乗法摂動で、
    collar 上 |(y−ζ_a)/(y−ζ_b) − 1| ≤ η ⇒ sup-norm の差 ≤ η·sup|Φ_Q| ≤
    η·C_box ⇒ |κ(x) − κ(x∖pair)| ≤ C_box·η。**C_pert := max(C_jet, C_box)**
    (明示 — [R13-04])。
    **帰納([R13-06])**: 零点個数 ≤ 4(構造的上限)に関する有限帰納。
    **base case = collar 内零点 0 個**: jet map は解析的で principal part 項
    なし — plain box の compact 勘定((FL-1) 型)が床を与える。帰納段: 上の
    摂動評価で
      φ(x) ≥ c_lower·κ(x) − (1 + c_lower)C_pert·η
    となり、η ≤ κ(x)·c_lower/(2(1+c_lower)C_pert) の帯では床が定数半分で移送。
    それ以外の帯は [R13-05](gcd-jump stratum tube)。exact 一致(δ = 0)は
    D 再取得((N-4))。
    **pole zone / Taylor zone の分離([GC4A2CR12-04]、[GC4A2CR13-07] で
    proof box を正式に再構成)**: Z/G 系の proof box 集合を次で**置き換える**:
      - **Taylor box** := {∀j: |ζ_j| ≥ r_pole} ∩ (元の box 閉域)
        — compact(compact の閉部分集合)。この box 上で jets は解析的、
        **C₂ := sup_{Taylor box} ‖Hess (𝒥_n)‖ < ∞**(compact 上の連続関数)。
        (v-d)(v-e) の tube 帰納・FL-6 の C² 論法は **Taylor box を proof box
        として**走る(有限 cover の再構成 — Z/G 系の cover 要素は Taylor box)。
      - **pole zone** {∃j: |ζ_j| < r_pole} は proof box に**含めない**:
        そこでは上の定量的発散が **直接床 φ ≥ 1 ≥ (1/C_box)·κ** を与える
        (Taylor・tube 論法は不使用 — [R12-04] の衝突は proof box の再定義で
        消滅)。
    C̃_i(t₀) = 0(t₀ 自身が零)の面は divisor/d₀ 簿記の routed 面。
(b) κ = min_Q sup|Φ_Q|: Φ_Q は box データの連続関数族(compact 一様)なので
min-sup も連続 — 全域で定義済み。∎
**帰結(core scope — [GC4A2CCORE-R3-02] で範囲を明示)**: **非 Z/G の**各
box の床 φ ≥ c·κ は**閉座標域全体**で証明される(tube 帰納 + compactness —
(v-d)。Z_QR に属す面点は strata として tube が覆い、属さない面点は零集合一致で
φ > 0 の compact 勘定に入る)。被覆((FL-0))は有限個の compact box の和で、
「終端 box」選択や side 全滅面の κ 下界(R6 撤回済み)は不要。renormalize
座標間の比較不等式も不要 — φ・κ・λ は intrinsic(§8.6 (N-6′))。
**Z/G 系 box の同型の勘定は §8.8 ZG-NF が正本として遂行する。**
*被覆*: Z_QR ∩ (box 閉域) ⊆ ∪_σ N_σ(各点は自分の stratum の tube か、より
低次元 frontier の tube に入る)、tube の外 {dist(·, Z_QR) ≥ min_σ h_σ} ∩
(box 閉域)は compact((v-d′) 面延長補題により φ・κ は閉域全体で連続)で
零集合一致から φ > 0 ⇒ inf =: c′ > 0。床定数は **有限個の (a_σ, h_σ, c′) の
min** — 移送は明示的([GC4A2CR7-B3a]: R6 撤回済みの c_side への依存を除去)。
**(6-vi) 相対床への変換([GC4A2CR7-B3b] で Lipschitz を supply)**:
*κ の Lipschitz 性(各 box 閉域上)*: Φ_Q(x)(y) は box 座標 x と Q の各成分に
ついて多項式 × 指数の有限合成で、compact な (box) × 𝒬_band × {|y| ≤ 1} 上で
一階偏導関数が有界 ⇒ x ↦ sup_{|y|≤1}|Φ_Q(x)| は Q に一様に Lipschitz
(定数 = 導関数上界)。min_Q は Lipschitz を保存(min の 1-Lipschitz 性)。
よって **κ は各 box 閉域上 Lipschitz(定数 C_L は box 定数)**。
κ|_{Z_QR} = 0 と併せ κ(x) ≤ C_L·dist(x, Z_QR)(**下界は不要**)。
よって tube 内で φ/κ ≥ a_σ/C_L、tube 外で φ/κ ≥ c′/C_box。
∎(SING-FRONTIER(§9)はこの帰納の**数値検証(診断)**であり、証明上の
open 義務ではない — [GC4A2CR3-02] の「open のまま床を主張」状態を解消。)
*数値診断*: §9 QC-TRANSV 行を参照(数値結果・件数・統計は §9 のみに記載 —
[GC4A2CR5-m1]。診断であり証明の代替ではない)。

**(FL-7′) core 側の供給([GC4A2CCORE-R1-01] — 全体合成は §8.8 (NF-7) が
唯一の authoring location)**: 本節(core)は **非 Z/G の各 structural proof
box の床定数 c > 0** を供給する(Q_C は簿記専用・r ≤ 1 exit は対象外 —
従前どおり)。**全体の c_J = min の合成は §8.8 (NF-7) に一本化**し、core 側
では主張しない(二重主張の解消)。

**scope(非主張)**: kernel 指数(GC-5)、10 階上界(A.3b)、**dispatch 経路
B(3|1)・C(多分割)の床(= GC-4B/GC-4C 系 packet — §8.7 の「C chart」の床とは
別物。[GC4A2CR1-07] の表記衝突を解消)**、c_J の数値評価(存在のみ主張 —
有効定数は非主張)、**q_band_witness-v3 の充足可能性(実 route record が
margin flag を満たすこと — record 生成側 = GC-5/GC-6 の義務、[GC4A2CR8-B1])**。
**status 注記([GC4A2CR13-minor])**: §8.6 の「B_CONFL = 6 目標」「sharp 目標」は
受理時点(a2302f3)の status 表記であり不変のまま残る — W_CONFL の証明の正本は
本 §8.7 (FL-2) で、その効力は本 packet の受理時に確定する(§4 の state 列が
唯一の status pointer)。人間による査読は未実施。


### 8.8 GC-4A.2c-Z ZG-NF(Z/G 床の正規形還元 — **R-GC4A2CZ R3 ACCEPTED、fixed SHA `5ea87ec`**)

**目的**: Z/G 系 proof box の床 φ ≥ c·κ を、consult #12 の裁定骨格
「同時 matching + projectivized defect の有限層別還元」で証明し、
最終合成 c_J = min c > 0((NF-7))を完成させる。§8.7 の [R12][R13] 系零点近接ブロックは
本節が正本として**置換**する(旧文は設計履歴)。

**(NF-1) 固定閾値(循環の解消、[GC4A2CZR1-B1] で annulus gap を排除)**:
r₀ < min(ε_G/4, 1/4) を固定。**small-root zone の閾値は r₀ に統一**:
S_i := {side i の零点 : |ζ| < r₀}(各 ≤ 2)。
M₀ := sup_{box 閉域}(**|ζ| ≥ r₀** の零点項 + unit log-jets(≤ 9 階)+
二次項)— r_pole に依存しない box 定数で、(ZF-1) collar 零点自由 + compact
両側有界の Cauchy 評価により有限。**S_i(< r₀)と M₀(≥ r₀)で全零点が
過不足なく分担され、[r_pole, r₀) の gap は生じない**(small zone 内の複数零点
は (NF-5) が**結合して**評価する — 個別に M へ逃がさない)。その後
  **r_pole := min(r₀, [24(M₀ + 1)]^{−1/3})**。

**(NF-2) 同時最大 matching([GC4A2CZR1-B2] で目的関数と型を修正)**:
matching の対象は **ラベル付き root occurrence**([GC4A2CZR2-B2]):
occurrence := (side i, 根の値 ζ, 重複 index k ∈ {1, 2})(double root は
k = 1, 2 の 2 occurrence — (NF-6) の対称係数座標と整合)。edge 集合の順序は
(重み降順, side-1 occurrence の ≺ 辞書式(値 → index), side-2 の同)で固定し、
**辞書式最大の max-weight matching** を取る — 完全に決定的。2r₀ < ε_G/2 より
S₁ × S₂ の全 cross 対は G-band 内。bipartite graph(S₁, S₂; 全 cross 対)の
**max-weight matching**(重み: exact 一致対 = 2、approximate 対 = 1 —
**exact 対の除去を最優先する目的関数**。同重みの tie は ≺ 辞書式で決定的)を
一度に取る。exact 一致対は共通因子として除去((NF-3))、approximate 対は
defect 座標へ((NF-4))、unmatched occurrence は片 side のみに 0/1/2 個残る
((NF-5))。first-match の順序干渉は matching の同時性により生じない。

**(NF-3) exact 共通因子の除去**: 線形因子は projective 正規化
ℓ_ζ(y) = αy + β、|α|² + |β|² = 1(ζ = ∞ も同一 compact 族)。共通因子 A を
除いた配置を x′ とすると B_i(x) = sA·B_i(x′)(s = scale)、
  **u(x) = u(x′)、φ(x) = φ(x′)**(log の完全 cancel — d₀ 再中心化不要)、
  **Φ_Q(x) = sA·Φ_Q(x′) ⇒ κ(x) ≤ |s|‖A‖_∞·κ(x′) ≤ L_A·κ(x′)**。
床の移送は**この片側評価のみで足りる**(reduced 床 φ(x′) ≥ c′κ(x′) ⇒
φ(x) = φ(x′) ≥ c′κ(x′) ≥ (c′/L_A)κ(x) — Remez 型逆向き比較は不要)。
s の上限は次数 ≤ 2 の係数ノルム同値。

**(NF-4) approximate 対の同時 defect**: matching が k ≤ 2 対のとき
A₁ := Π_j ℓ_{ζ_{1j}}、A₂ := Π_j ℓ_{ζ_{2j}}、reduced 配置 x′ に対し**正しい恒等式**
  **Φ_Q(x) = A₂·Φ_Q(x′) + (A₁ − A₂)·B₁(x′)**
⇒ κ(x) ≤ L₀κ(x′) + L₁‖A₁ − A₂‖_∞。jet 側は近似でなく **exact defect**
  J(x) − J(x′) = (−(n−1)!·Σ_j(ζ_{1j}^{−n} − ζ_{2j}^{−n}))_{n=3..9−d₀}
(摂動量は |δ| でなく **この weighted jet defect そのもの**で測る — R14 の
d_collar 定数化の誤りの訂正)。defect ノルム
  **Δ_ZG := ‖A₁ − A₂‖_∞ + ‖J(x) − J(x′)‖_∞**
で二分する:
- **転送帯** Δ_ZG ≤ c_tr·κ(x): reduced 床 + 上の片側 κ 評価 + jet defect の
  三角不等式で床が定数損失つきで移る。
- **defect 帯**(補集合): Δ_ZG を **projectivize** し、defect-normal stratum
  上の横断性として扱う((NF-6))。
2 対の誤差を逐次処理しないため、proximity 組合せと誤差蓄積は同時に消える。

**(NF-5) unmatched pole face(same-side 補題)**: unmatched 小零点は片 side
のみ・0/1/2 個。2 個(same-side cluster)の場合、x := ζ₁/ζ₂(|x| ≤ 1)に対する
**補題 SS**: max(|xⁿ + 1|, |x^{n+1} + 1|) ≥ **1/12**(|x| ≤ 1、**3 ≤ n ≤ 8**)。
*証明*: 両方 ≤ 1/12 なら |xⁿ| ≥ 11/12、
|x − 1| = |x^{n+1} − xⁿ|/|xⁿ| ≤ (2/12)/(11/12) = 2/11、
|xⁿ − 1| ≤ n|x − 1| ≤ 8·2/11 = 16/11(|x| ≤ 1)、
∴ |xⁿ + 1| ≥ 2 − 16/11 = 6/11 > 1/12 — 矛盾。∎
役割: 単独/same-side 2 元の unmatched pole face で **projectivized jet が
非零**であることの保証(任意の近接配置への直接適用ではない)。
**pole-face 床の結合評価([GC4A2CZR1-B1])**: reduced 配置 x′(matched 対は
除去/defect 処理済み)の unmatched 零点(≤ 2、同 side)について:
単独(ρ := |ζ|): |𝒥_n| ≥ ρ^{−n} − M₀(定数は M₀ に統一 —
[GC4A2CZR2-m1])。**[r_pole, r₀) の帯は pole face ではなく §8.7 の Taylor box
が担当**(jets 有界の compact 勘定)。2 元(ρ₁ ≤ ρ₂ < r₀): ζ₁^{−n} を括り
出して補題 SS を (1 + xⁿ)(x = ζ₁/ζ₂、|x| ≤ 1)に適用 —
  max_{n, n+1}|ζ₁^{−n} + ζ₂^{−n}| ≥ ρ₁^{−n}/12
(**小さい方の零点の冪で下界 — ρ₂ の位置に依存しない結合評価**)。
いずれも ρ₁ < r_pole ⇒ max_n|𝒥_n| ≥ r_pole^{−3}/12 − M₀ ≥ 1
(r_pole の定義から)。jets 範囲は長さ ≥ 5 ≥ 2 なので連続 2 指数の組が取れる。

**(NF-6) defect strata の横断性と frontier**: Z/G の strata を明示列挙:
exact 共通因子数 k ∈ {0,1,2}/matched-pair defect の support と ordered rate/
unmatched side と個数 {0,1,2}/same-side double root/degree-drop/support-drop/
gcd-jump/confluence label。double root の局所座標は根順序でなく**対称係数**
(中心・判別式)。exact-factor stratum の接空間は
  δB_i = (δA)B_i′ + A·δB_i′(共通 δA は QR incidence の接方向)、
法方向 = reduced 配置の法方向 + cross-side imbalance defect。
**defect-kernel 補題([GC4A2CZR1-B3] — consult #12 の未解決義務の証明)**:
defect 方向 = 対ごとの根摂動 (δζ_{1j}, δζ_{2j})(j ≤ 2、方向数 ≤ 4 複素)。
jet defect の全微分は exact 式の微分
  ∂/∂ζ [−(n−1)!·ζ^{−n}] = n!·ζ^{−(n+1)}
により、行列 **V := [n!·ζ_{ij}^{−(n+1)}]_{n=3..9−d₀; (i,j)}**(±符号は side)。
列は節点 ζ_{ij} の冪 (ζ^{−4}, …, ζ^{−(10−d₀)})ᵀ。**double root の扱い
([GC4A2CZR2-B3])**: same-side double root(節点一致)では素朴な列が一致して
しまうため、**対称係数座標(中心 e₁・判別式方向 e₂ — (NF-6))での微分列**を
使う: 一致節点 ζ の defect 方向は
  中心方向 = ζ^{−(n+1)} 列、判別式方向 = (n+1)·ζ^{−(n+2)} 列(冪の微分)
の **confluent(Hermite)Vandermonde 対**となる。相異なる base 節点 +
重複度込み総列数 ≤ 4 ≤ 行数 7 − d₀ ≥ 5 の **confluent Vandermonde は
非特異**(Hermite 補間節点の標準事実 — minor は Π n! · Π w^{冪} ·
Π_{a<b}(w_b − w_a)^{m_am_b} 型で base 節点相異により非零)。
単根のみの場合は通常の generalized Vandermonde(共通冪 ζ^{−4} を括った
minor が節点相異により非零)。いずれも**単射**。
**unit・二次項は defect 微分に現れない**(defect は exact principal-part 差
のみ — 旧 FL-4 の Vandermonde が失敗した unit 干渉問題はここでは構造的に
不在)。よって **defect-normal 方向に kernel はない**。
一般の Q での δΦ_Q から fitted p = T₂u での δΦ_p への移行は §8.7 (6-iii) の
gauge 最小化(jets 0..2 の吸収)と同じ — jet kernel に入れば橋により
ord δΦ_p ≥ 10 ⇒ 既存 collapse(regular: 2 指数 deg ≤ 2 → W_CONFL 6/
confluent: 1 指数 Π₄ → 4)で **δΦ_p ≡ 0 ⇒ kernel = incidence tangent ⊕ 0
(defect 成分なし)**。
**compactness**: projectivized defect-normal 球面束は stratum の frontier
tube を除いた compact core 上で取り((§8.7 (v-d) の次元帰納をそのまま適用 —
strata は (NF-6) の列挙で有限・次元順)、最小特異値正。same-side/unmatched
pole face が kernel に入らないことは補題 SS + (NF-5) の結合評価が保証。
**依存方向([GC4A2CCORE-R2-01] で一方向に統一)**: ZG-NF が core の generic
(FL-6) 補題(非 Z/G collapse/tube)を**消費する**(core → ZG-NF の一方向。
(FL-4)/(FL-6) が本補題を参照するのではない)。証明の重複記載はしない。

**(NF-7) 合成([GC4A2CZR1-m2] で状態整合)**: 本節は ZG component の床定数を
供給する。**global c_J = min c > 0(全 structural proof box の有限 min、
K = 1)の合成は、A.2c-core の受理を前提に本節が authoring location として
宣言する**(core 未受理の間は条件付き — トップレベル A.2c の受理条件)。

**scope(非主張)**: §8.7 core の非主張項目に同じ + ZG-NF の数値検証
(SING-FRONTIER — 診断)。人間による査読は未実施。


### 8.9 GC-4B.0 ADAPT31(triple divisor adapter の feasibility — **accepted(条件付き go)、R-GC4B0 R8 PASS、fixed SHA `eee39bf`**。TN-3 は §4 GC-5 受理条件の blocking downstream obligation)

**目的**: 3|1 dispatch の「3」側(3 原子和)に対する **chart 付き Weierstrass
certificate** の型と構成可能性を確立する。接触次数 ≤ 5(W_c(3))は点での ord
上界であり collar 内の**総零点数**を制御しない — 後者が divisor 抽出の前提。
失敗は 3|1 経路の重大 no-go 信号(§4 台帳)。

**(AD-1) certificate 型(typed・fail-closed — [GC4B0R1-04][GC4B0R2-04] で
§7.1 規約(式または identity ref、自由文禁止)に完全整合)**:
  `TripleWeierstrassCert := (s, P, V, r, witnesses)`。
  field 型: s ∈ ℂ*(値域 witness 付き)/ P = Π_j(y − ζ_j)^{m_j}(monic、
  重複度付き根リスト (ζ_j, m_j) から**構成的に定義**、Σm_j = deg P ≤ N_T)/
  r ∈ Π₂(係数 3 組 ∈ ℂ³ 閉箱)/ **V := B/(s·P·e^{r})(商としての定義式 —
  identity B ≡ sPVe^r は定義により恒等成立)**。
  **root-coincidence witness の型([GC4B0R3-04]、[GC4B0R4-03] で領域・相異
  条件を追加 — 外部根の反例(例: 根 3 ∉ D(t₀,2))を排除)**:
  `(root_list (ζ_j, m_j)_j — **∀j: ζ_j ∈ D(t₀, R_col) の内部 ∧ ζ_j 相異** ∧
   B は D̄(t₀, R_out) 上解析的(R_col > 0 は chart 固定の正定数);
    (a) ord-一致: ∀j, B の ζ_j での 0..m_j−1 階 jet 消滅 ∧ m_j 階 jet 非零
        の検証値(有限個の等式/不等式),
    (b) 計数一致: 偏角原理の輪郭積分 N(B; D̄(t₀, R_col)) の整数値 = Σ_j m_j,
    (c) 境界非零: inf_{|z−t₀|=R_col} |B| > 0 の検証値)`
  — (a)(b)(c) が全て成立するとき、かつそのときに限り V は D̄(t₀, R_col) 上
  **正則かつ零点自由な unit** として well-defined(可除性は (a)、他零点の
  不在は (b)(c))。
  witnesses: `(zero_count ≤ N_T 検証値, R_col, sup|V|・inf|V| 両側 bound,
  重複度付き根リスト(A.3a zf_witness 同形式), s 値域, P 係数域,
  root-coincidence witness)` — 欠落・不一致 = record 生成禁止(fail-closed)。

**(AD-2) counting 補題(N_T の存在 — [GC4B0R1-01][02] で mini-atlas と
Rouché 論法に全面改稿)**: 主張([GC4B0R7-01] で定理文自体を条件付きに訂正)— **比較補題 TN-3 が
成立すれば、正規化 triple 族の collar 内零点数は一様上界 N_T < ∞ を持つ**
((2c) 段 1 は無条件に成立、段 2 が TN-3 を消費 — TN-3 は blocking downstream
obligation として §4 GC-5 受理条件に登録 [GC4B0R6-01])。
*(2a) 3-class mini-atlas*(A.2b の pair atlas からの「導出」主張は撤回 —
本 packet が同じ設計 pattern で **3-class 専用の有限 chart 族**を定義する):
  (i) **plain**(3 class 相異・分離 ≥ band): 係数 ℓ² 球面 × anchor 差閉円板。
  (ii) **片側 confluent**(1 対が band 内): 対を divided-difference 再正規化
    した deg ≤ 1 prefactor 対象 + 独立 1 class — (prefactor 係数, 残 class
    係数) の joint ℓ² 球面 × 閉円板。
  (iii) **全 confluent(chain 込み・直径 < 2ε_T)**: 入力は **merge-first /
    zero-prune 後に class 数がちょうど 3**(対距離すべて > 0・係数すべて非零)
    の triple に限る([GC4B0R5-01] — W_c(3) の適用前提を型に昇格。型付き
    witness: 相異検証値(min 対距離 > 0)+ prune 済み flag。exact merge・
    係数零で class 数が 3 未満に落ちる入力は **lower-arity route**(2 class =
    pair 側 A.2b 系 certificate、単一 class = 自明 P = 1)へ exit し (iii) に
    入らない)。z_c := cluster の ≺-最小 class の位相 B(tie は ≺ の Re/Im
    辞書式で一意)— 型 [GC4B0R6-02]: **z_c : K → (class 位相の閉 chart 箱)
    ⊆ D̄(t₀, R_col)**(chart 制約として class 位相箱 ⊆ D̄(t₀, R_col) を課す —
    cluster 中心は collar 内の複素点。選択は決定的だが**連続とは主張しない**)。
    正規化([GC4B0R4-01] — 旧「deg ≤ 2 prefactor」は F3′ 反例(正本: FR 文書
    §7)により撤回済み): g := f/‖J⁵f(z_c)‖₂(J⁵ = 0..5 階 jet ベクトル)。
    上記前提下で **GC-1 W_c(3)(D_W(3) = 5)により ord_{z_c} f ≤ 5、すなわち
    J⁵f(z_c) ≠ 0** — g は well-defined。jet cap 5 の根拠 = D_W(3) と F3′ の
    sharp 性。**raw exact merge(直径 0 の実入力)と、counting 閉包の直径 0
    面(jets 正規化極限対象 = 球面 jet の deg ≤ 5 多項式 × e^q が張る blow-up
    face — F3′ 型極限を含む)は別物**([GC4B0R5-02]): 前者は selector 以前に
    lower-arity へ route され (iii) に現れない。後者は (2c) 段 2 の compact 化
    にのみ現れる極限対象で、その非零性は jet ノルム 1 の継承で保証される。
**3-class selector 述語表([GC4B0R2-02])**: 対距離 d_{ab} :=
max(|B_a − B_b|, |A_a − A_b|^{1/2})、d_min := min 対(tie は ≺)。
  | 段 | predicate(半開: < で発火) | chart |
  |---|---|---|
  | (1) | d_min ≥ ε_T | (i) plain |
  | (2) | d_min < ε_T ∧ 第三 class の両対距離 ≥ ε_T | (ii)(pair = d_min 対) |
  | (3) | それ以外(補集合 — **chain cluster を含む**: 三角不等式により **cluster 直径 < 2ε_T**。(iii) の jet 正規化は直径・valuation に依らず一様) | (iii) |
first-match で全域一意(段 (3) は補集合 — 網羅的・排他的)。
**chain cluster の処理([GC4B0R3-01][GC4B0R4-01][GC4B0R5-01])**:
段 (3) の入力は「全対 < ε_T」とは限らない(chain 例: d₁₂ < ε_T、d₂₃ < ε_T、
d₁₃ ∈ [ε_T, 2ε_T))が、merge/prune 後の相異 3 class で直径 ∈ (0, 2ε_T) なので
(iii) の jet 正規化族が一様に覆う(直径 0 の実入力は lower-arity route)。
**compact 性の分離([GC4B0R2-01]、[GC4B0R5-03] で対象を関数族に変更)**:
半開 band は **record 割当専用**。counting の証明は chart metadata の閉包 box
ではなく、(2c) の **パラメタ空間 K 上の関数族**(連続写像 p ↦ f_p の像と
その極限)に対して行う — metadata(jets 球面・直径・中心)は g を一意に
定めず、その compact 性は関数族の compact 性を意味しない(R5 指摘)。
*(2b) 各 chart 閉包上の非零性([GC4B0R2-03] — 球面 face の場合分け)*:
(i) 球面は**係数ベクトル全体の非零**を与える(個別係数の零面を含む)—
not-all-zero 係数の相異 3 指数結合は GC-1 W_c(3) 独立性で f ≢ 0 ✓。
(ii) joint 球面 ⇒ (P₁, c₃) ≠ (0, 0)。場合分け: 両方非零 → q₁ − q₃ 非定数
(chart 前提: 第三 class は対から band 分離)の prefactor 付き混合系 —
§8.7 (FL-2b)(d) 型の逐次消去で ≢ 0。P₁ = 0(c₃ ≠ 0)→ 単一指数 ≢ 0 ✓。
c₃ = 0(P₁ ≠ 0)→ 多項式 × 指数 ≢ 0 ✓。
(iii) ‖P‖ = 1 の多項式 × 指数で自明に ≢ 0 ✓。
**luna 反例 f_ε = (e^{−εz} − 2 + e^{εz})/√6 の処理**: ε → 0 で生データは
一様に 0 へ退化するが、この列は (ii)→(iii) の band で再正規化され、
**零点集合は scalar 倍で不変**(f と f/ε² は同じ零点)なので、零点数の評価は
再正規化代表(非零)に対して行えばよい — 生データの 0 退化は counting に
影響しない。
*(2c) counting の 2 段分解と Rouché([R1-02] 撤回、[GC4B0R3-02] 半径分離、
[GC4B0R5-03] で関数族ベースに全面改稿)*: 計数対象は certificate の複素
collar D̄(t₀, R_col)。外側 buffer 半径 **R_out := 2R_col**(chart 定数)。
- **パラメタ空間 K**(chart ごと): 係数 c ∈ ℓ² 単位球面 ⊂ ℂ³ × class データ
  (B_j, A_j) ∈ 閉 chart 箱 × 定数 gauge 固定(§8.6 規約)。z_c は K の型付き
  関数。**p ↦ f_p は K → C(D̄(t₀, R_out)) の連続写像**(明示的指数和公式・
  データ有界 — F3′ 型(正本: FR 文書 §7)の係数発散は divided-difference
  座標の産物であり、
  raw 係数球面を使う K では起きない)。
- **Z₀ := {p ∈ K : f_p ≡ 0}**(閉 — 具体的には exact 一致 class の合併後に
  全合併係数が零、という実代数的条件)。
- **(段 1: Z₀ 外 — 無条件)**: 任意の開近傍 U ⊇ Z₀ に対し K∖U は compact で
  各 f_p ≢ 0。p₀ ごとに R′ ∈ (R_col, R_out) を |z−t₀| = R′ 上 f_{p₀} ≠ 0 に
  選べば、Rouché により p₀ の近傍で
  N(f_p, D̄(t₀, R_col)) ≤ N(f_{p₀}, D̄(t₀, R′)) < ∞ — 有限被覆で一様上界。
- **(段 2: Z₀ 近傍 — TN-3 に条件付き)**: g_p := f_p/‖J⁵f_p(z_c)‖₂
  (K∖Z₀ 上 well-defined — (2a)(iii))。**比較補題 TN-3**:
  ∃ c_TN > 0: ∀p ∈ K∖Z₀: ‖J⁵f_p(z_c)‖₂ ≥ c_TN · sup_{D̄(t₀,R_out)} |f_p|。
  TN-3 が成立すれば {g_p} は一様有界 ⇒ 正規族(Montel)⇒ 任意の局所一様
  極限 g* は jet ノルム 1 を継承 — 詳細 [GC4B0R6-02]: 点列 pₙ に対し
  z_c(pₙ) は閉箱 ⊆ D̄(t₀, R_col) 内なので部分列で z* へ収束し、局所一様収束は
  全階導関数の局所一様収束を与える(Weierstrass)から
  ‖J⁵g*(z*)‖₂ = lim ‖J⁵g_{pₙ}(z_c(pₙ))‖₂ = 1(**z_c の連続性は不要** —
  compact 選択 + 部分列で足りる)⇒ **g* ≢ 0** ⇒ 段 1 と同じ Rouché 有限
  被覆が {g_p} の閉包上で成立。零点集合は
  scalar 不変(N(g_p) = N(f_p))なので、両段合わせて chart ごとの
  N_T(chart) < ∞、chart 有限個 ⇒ **N_T := max < ∞**。∎(TN-3 条件付き)
  **TN-3 の状態([GC4B0R6-01] で位置付けを訂正)**: 未証明の **blocking
  downstream obligation**(§4 GC-5 受理条件に登録)。q_band_witness-v3 充足
  可能性(witness 生成義務)と同列とした R5 時点の扱いは**撤回** — TN-3 は
  N_T 存在そのものを支える counting の核心であり、解消まで counting 主張は
  条件付きに留まる。支持: (a) 1-パラメタ解析弧上では divided-difference
  leading 項 h_v ≢ 0 への収束から比が正極限を持つ(h_v の ord_{z_c} 上界には
  c=3 閉包資産の contact bound の消費を想定 — 適用条件の確認込みで義務に
  含める)、(b) §9 TRIPLE-VALENCY 診断(正規化 scale で max 5 — 証明の代替
  ではない)。候補経路: (α) 実解析族の curve selection / Łojasiewicz、
  (β) ≤3 項二次位相指数和への Turán–Nazarov 型 doubling、(γ) 多項式係数線形
  ODE の零点計数評価。
(生データでの零点数は位相スケールとともに増大する(§9 TRIPLE-VALENCY 診断)
ため、**正規化座標での主張が本質** — 「接触次数だけでは足りない」の正体。)

**(AD-3) 供給源 2 系統の被覆(GC-4C.0 (3) 表の要件 — [GC4B0R1-03] で
membership witness を型として要求)**: SPLIT4 の node witness(gap/scale)や
SIG-AUDIT の signature witness は、それ自体では正規化 triple 族への所属を
供給**しない**(R1 指摘どおり)。そこで adapter の入力型として
  `triple_membership_witness := chart family label で判別する tagged union
   ([GC4B0R2-04]、[GC4B0R3-03] で型を閉鎖): (i) plain ⇒ (係数 ℓ² 球面値
   ∈ ℂ³, anchor 差 ∈ 閉円板², d_min ≥ ε_T 検証値) / (ii) ⇒ (**joint 球面値
   ∈ ℂ³**(deg ≤ 1 prefactor の 2 係数 + 独立 class 係数 1 — ℂ⁴ は誤記で
   訂正), divided-difference 内部座標 ∈ **閉円板**, 第三 class 分離検証値) /
   (iii) ⇒ (**jets 0..5 の球面値 ∈ ℂ⁶**, cluster 直径 ∈ **(0, 2ε_T)**,
   cluster 中心 ∈ 閉円板, 相異検証値・prune flag)`([GC4B0R4-02][GC4B0R5-01]
   — record は merge/prune 後の相異 3 class のみ。直径 0 は lower-arity route
   で本 variant に入らない。counting 閉包の直径 0 blow-up face は record 型
   ではなく (2c) 段 2 の証明対象 [GC4B0R5-02])
— 各 variant は有限次元型(**record 割当専用 — compact 性は主張しない**
[GC4B0R6-03]: (iii) の直径 (0, 2ε_T) は開区間であり compact でない。counting
用の compact 空間は (2c) の K とその閉包(直径 0・merge/prune 境界面を含む)
で、record domain とは分離される)。**fail-closed で要求**(欠落 = adapter
適用不可 = record 生成禁止)。
- **prepared tree triple**(SPLIT4 経由): witness の導出義務は record 生成側
  (tree node データ → 正規化)にあり、**GC-5/GC-6 送り**(q_band_witness-v3
  の充足可能性と同じ規約)。
- **radial 混成 3 原子和**(SIG-AUDIT 経由): 同上(signature データ →
  正規化の導出義務を record 生成側に送る)。
両系統とも witness が供給されれば (AD-2) の族に入り、**同一の certificate 型
が適用可能**(feasibility はこの型レベルで閉じ、witness 充足は生成側義務)。∎

**(AD-4) feasibility 判定(条件付き — [GC4B0R6-01] で降格)**: (AD-1) の
型は (AD-2) の N_T(型付き定数)と A.1/A.3a の既存 witness 規約のみで構成
可能であり、型レベルで構成を妨げる障害は存在しない。ただし **N_T の存在は
TN-3 に条件付き**であり、TN-3 は witness 生成可能性と同列ではなく counting の
核心を支える **blocking downstream obligation**(§4 GC-5 受理条件に登録)。
よって B.0 の判定は **条件付き go — TN-3 未解消の間、3|1 経路の counting は
未確立**。TN-3 の反例(比較定数 c_TN の非存在)が出れば B.0 は撤回され GC-4
の no-go 信号となる。数値診断は **§9 TRIPLE-VALENCY 行を参照**(数値の
authoring location は §9 のみ — [GC4B0R3-minor]。診断であり証明の代替では
ない)。

**scope(非主張)**: 3|1 kernel 指数の本体(GC-4B)、N_T の有効値、
**比較補題 TN-3**(多パラメタ一様性は未証明 — GC-5 blocking downstream
obligation。解消まで N_T 存在・counting 主張は条件付き)、triple の
deep-flat 解析(GC-4B 系)、人間による査読は未実施。

### 8.10 GC-5-T0 BORD-3(3 原子 border 極限の点一様 ord 上界 — drafted、査読対象 R-BORD3 R1)

**目的**: §8.9 (2c) の比較補題 TN-3(§4 GC-5 受理条件の blocking downstream
obligation)が消費する境界 ord 上界を、**accepted c=3 資産の pointer 消費**で
sequence/moving-center 形の補題として閉じる(consult #13(Sol)の裁定:
経路 α′ = curve selection + 弧 leading-term + BORD-3。BORD-3 を TN-3 に埋め
込まず独立 packet として先行させる)。finite-m の W_c から border 版への
「自動保存」は主張しない — 各 stratum の極限 span を担当する accepted 資産を
個別に消費する。

**(B3-1) statement(sequence/moving-center 形)**: K は §8.9 (2c) の
パラメタ空間(‖c‖₂ = 1、class データ閉箱、gauge 固定 — §8.6 規約)、
Z₀ := {f ≡ 0}。p_n ∈ K∖Z₀、λ_n ∈ ℂ*、ζ_n := z_c(p_n)(§8.9 (iii) の型:
閉箱 ⊆ D̄(t₀, R_col))とし、
  λ_n f_{p_n} → h  (D̄(t₀, R_out) 上一様 = compact-open)、 h ≢ 0、
  ζ_n → ζ ∈ D̄(t₀, R_col)
とする。このとき **ord_ζ(h) ≤ 5**。

**収束 topology の宣言**: 本 packet の border 極限は上記 compact-open 収束で
**定義**する(「W̄₃ の元」という集合名は本文書では使わない — 曖昧さ回避、
consult #13)。FR 資産(Fock/J⁵ 収束)との橋は (B3-4)。

**(B3-2) 不変性 reduction**: ord は (i) scalar 倍、(ii) z の affine 置換
z = ζ + s·w(s ≠ 0)、(iii) 共通非零因子 e^{q} の乗除、で不変。よって部分列を
取り、各 separation pattern の標準正規化(中心 ζ へ平行移動 + 適切な scale s
での再正規化 + 定数 gauge)後の極限が下表の normal form に一致することを示せば
よい。**pattern 分類の網羅性**: 対距離 d_{ab}(n)(§8.9 の d = max(|ΔB|,
|ΔA|^{1/2}))は有界なので部分列上で各々収束。s(n) := max 対距離とすると、
三角不等式により **s(n) より真に速く 0 へ行く対は高々 1 つ**(2 対が o(s) なら
第 3 対も o(s) となり s = max と矛盾)— よって pattern は下表の 5 行で網羅
(係数退化 = support-drop は各行に横断的で、最終行に統合)。

**(B3-3) stratum 被覆(consult #13 の設計 — coarse 2|1 と「coarse 3 内の
nested 2+1」は別資産が担当する点に注意)**:

| pattern(部分列上) | 正規化後の極限 span | 消費資産(pointer) | ord 上界 |
|---|---|---|---|
| 1\|1\|1(全対距離下界 > 0) | plain 3 class 指数和 | GC-1 W_c(3)(§3.1 — 任意中心で成立) | 5 |
| coarse 2\|1(1 対のみ → 0、singleton 距離下界 > 0) | span{e^p, P e^p, e^q}、P 非定数 deg ≤ 2、r = q − p 非定数 | 補題 N-P4 の極限 span(閉包文書 §4.3.6)+ **static W′**(W 文書 §6: w₃ ≤ 4、profile (0,2,4) sharp) | 4 |
| coarse 3・plain(全収縮、全対 ≍ s) | e^{q} Π₅(deg ≤ 5 多項式 × 指数) | FR-S1′(FR 文書 §8、R-A′ PASS)— 非零元の ord = 多項式因子の重複度 ≤ 5 | 5 |
| coarse 3・nested 2+1(1 対 τ = o(s)) | J⁵ 内の 3 次元 limit span(ν-chart) | FR-S1″(FR 文書 §9、R-A″ PASS、compact chart 𝒦_{η,t₀})— head SVD floor により非零極限の J⁵ ≠ 0 | 5 |
| support-drop / exact merge / 係数消滅(class 数 ≤ 2 へ退化) | span{e^p, P e^p}(deg ≤ 2)または plain ≤ 2 class | ν-chart(FR-S1″ (A″1) と同型の 2 原子版)+ W_c(≤2)(D_W(2) = 2)。(α + βP)e^p の ord ≤ deg P ≤ 2 | 2 |

いずれの行も上界 ≤ 5 — (B3-1) が従う。**5 は sharp**(F3′ — 正本: FR 文書
§7。coarse 3・plain 行で到達)。

**(B3-4) topology 橋と chart 包含**:
- ord_ζ(h) ≤ 5 は **J⁵h(ζ) ≠ 0 と同値**であり、J⁵ 汎関数(0..5 階 jet)は
  compact-open 収束・Fock/J⁵ 収束のいずれでも連続(一様収束 ⇒ Cauchy 積分
  公式で全階導関数が内部一様収束)。FR 資産の結論(limit span の J⁵ 単射性)
  は本 packet の compact-open 極限にそのまま移送される — 両 topology の極限が
  同じ jets を持つため。
- **chart 包含**(consult #13 の未確認条件): coarse 3 の正規化
  s(n) := max 対距離で root-normalized parameter は |Ā|, |B̄| ≤ 1 かつ
  max(|Ā|^{1/2}, |B̄|) = 1 — FR-S1″ の (N0) は **η = 1 で充足**し、K の閉箱は
  affine 正規化を介して 𝒦_{η,t₀} に写る(t₀ 制約は τ/s → 0 の部分列で充足)。
  Fock norm 資産の消費はこの正規化座標上でのみ行い、結論(J⁵ ≠ 0)だけを
  (B3-2) の不変性で raw 座標へ戻す。

**(B3-5) 証明**: λ_n f_{p_n} → h ≢ 0 とする。部分列で separation pattern を
(B3-2) の分類に固定。各行で: 標準正規化を施した列は当該資産の compact chart
に入り、正規化列の極限 h̃(h の affine/scalar/gauge 変換 — ≢ 0)は資産の
limit span に属する。資産の ord 上界(表)により ord_{0}(h̃) ≤ 5、不変性で
ord_ζ(h) = ord_0(h̃) ≤ 5。∎

**scope(非主張)**: c ≥ 4 の border ord 上界(GC-9 の confluent 昇格義務は
別)、有効定数(存在のみ)、TN-3 本体(GC-5-T1)、人間による査読は未実施。

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
| QC-TRANSV | Q_C transversality に chart 内部の構造的縮退(線形化 rank 落ち)がある | δv-jets 3..9 の線形化 7×4 行列(δu = δB₁/B₁ − δB₂/B₂、構造 null 2 方向 quotient)の σ_eff を random + adversarial 探索 | **初期結果あり**(`qc_transversality2.py`: random 4844 配置で σ_eff > 0(中央値 0.11)、adversarial 零接近は全て routed 境界(confluent 帯・係数消滅面)接近 — **内部縮退未検出**。§8.7 (FL-6) が消費。診断であり証明の代替ではない) |
| DEG4-SHARP | 二指数・deg ≤ d prefactor 系の sharp ord(FL-6 の次数爆発懸念の検証) | Newton 探索(scale gauge 固定、genuine 到達) | **結果**: sharp = 2d + 2(d=1: 4、d=2: 6、d=3: 8、d=4: 10 到達・11 なし)。d = 4 は予算 10 と衝突するが、consult #11 裁定 + §8.7 (6-iii)(regular = 2 指数 deg≤2 → W_CONFL 6 / C = 1 指数 ord ≤ 4)により **QR 横断線形化には現れない**(この主張の証明本体は (6-iii) — 本行は診断・裁定の記録)。 |
| SING-FRONTIER | singular frontier(gcd-jump・degree-drop・Q-band 境界)近傍で φ/κ の下限が (6-v) tube 帰納の定数より劣化する | frontier 近傍の高精度 continuation(ε 対数列) | **結果**(`sing_frontier.py`: 3 frontier 型 × ε 対数列 6 桁・各 254 配置)— 係数消滅面・cross-side gcd-jump は **plateau(劣化なし)**。confluent 帯内部への continuation のみ **σ_eff ~ d³(多項式・指数 3)** — flat/指数型崩壊ではなく、band 閾値 ε_G での chart handoff 定数が ε_G³ でスケールすることを意味する(**GC-5 の定数追跡は ε_G³ を予算化** — 設計入力。band 内部は confluent chart に route 済みで plain 線形化は不使用のため blocking 信号ではない)。診断であり証明の代替ではない |
| COLLAR-POLE | 実区間で unit 有界でも分母複素零点が collar に接近する列 | V_i の複素零点距離 | open(A.3 入力) |
| TRIPLE-VALENCY | 接触次数 ≤ 5 でも collar 内の零点数が非有界になる triple 族 | 偏角原理による零点計数(random 12000 + スケール比較) | **結果**: 正規化スケール(chart 座標相当)で最大 5(|y| ≤ 1.5)、非正規化は位相スケールと共に増大(scale 3: 14 / scale 8: 35)⇒ **正規化族での一様上界に整合・非有界の反例なし**(§8.9 (AD-2) が消費。診断) |
| TN3-RATIO | TN-3(§8.9 比較補題)の c_TN が存在しない(比 ‖J⁵f(z_c)‖/sup|f| が Z₀ 近傍で 0 へ潰れる) | mpmath 50 桁で F3′ 型・GEN(divided-difference 退化係数)・CHAIN の 3 族 × δ 対数列 8 桁 + float64 adversarial(random 20000 + Nelder-Mead 連鎖)。探索箱は実測データの現実域(|B| ≤ 2.5、|A| ≤ 0.8 — PR #179 Endo/Kawasaki 条件参照) | **結果**(`tn3_ratio.py`/`tn3_adv.py`): 全 3 族で **plateau(slope ≈ 0** — F3′: 0.672 / GEN: 0.073 / CHAIN: 0.046)、confluent 方向の減衰信号なし。adversarial 最小 ≈ 3.7e-5 は**非 confluent 配置**(sep 0.79・箱境界張り付き)の指数成長由来で restart 連鎖でも崩壊せず — **c_TN > 0 に整合・反例信号なし**(診断であり証明の代替ではない。TN-3 の証明義務(GC-5)は不変) |
| GRADED-BUDGET-DOUBLE | bi-RF cost Λ₁+Λ₂ の provenance/root 二重計上 | ledger 監査 | open(A.0/GC-11 入力) |

**実測ベンチマーク候補(pointer)**: 公開 homodyne/quadrature データの調査は
PR #179 の brief(`docs/2026-08-19-public-homodyne-data-brief--recorded.md` —
優先 Endo/Kawasaki、確度 A–D 付き)を正本とする。GC-5 以降のデータ層設計の
入力であり、本文書は再記述しない。

## 10. リスク台帳

| # | リスク | 順位 | 対処 |
|---|---|---|---|
| R1 | S4 型障害(tropical transition)が PBK `2|2`/`3|1` に再出現 | **本命** | PBK22-ADV/SPLIT-EQ を GC-4 着工前に回す。blocking 反例で K_c 回帰(go/no-go 規則) |
| R2 | tree depth による T² budget の重複消費 | 高 | Assembly 層の root-only 規約(§2)+ BUDGET-TREE で検証 |
| R3 | confluent chart の未記録 rate(F3 型 witness の一般形) | 中 | GC-9 の chart label に相対 valuation/flag を必須化(FR §7 の設計制約を継承) |
| R4 | 一般 W 不成立(valuation 爆発) | 低 | GC-1 の上界証明は次数勘定で閉じる見込み(§3)。数値は 3c−4 to 支持 |

## 11. 版履歴

- v0.27.0(2026-08-19): GC-5 着工(orange GO)— consult #13(Sol、
  `sol-tn3-route-consult.md`): TN-3 証明経路は α′(curve selection + 弧
  leading-term + BORD-3 消費)を採用、**BORD-3 を独立 packet として先行**、
  J⁵ は minimal sharp のまま維持(m > 5 への弱化は不採用)、β(Turán–Nazarov
  拡張)/γ(ODE 零点計数)は反証時の fallback。§8.10 GC-5-T0 BORD-3 を起草
  (sequence/moving-center 形、5 stratum 被覆表、topology 橋、chart 包含)、
  §4 台帳に GC-5-T0/T1 行を追加。

- v0.26.9(2026-08-19): GC-5 前診断 2 本の結果を §9 に記録 — SING-FRONTIER
  (係数消滅・gcd-jump plateau / confluent 帯内部のみ σ_eff ~ d³ = handoff
  定数 ε_G³ の設計入力、blocking 信号なし)、TN3-RATIO 新設(3 族 δ 対数列
  plateau + adversarial 崩壊なし — c_TN > 0 に整合)。実測ベンチマーク候補の
  pointer(PR #179 brief)を §9 末尾に追加。いずれも診断であり証明の代替では
  ない(TN-3 の GC-5 証明義務は不変)。

- v0.26.8(2026-08-19): **GC-4B.0 ADAPT31 受理** — R-GC4B0 R8 PASS(luna
  gpt-5.6-luna xhigh、fixed SHA `eee39bf`、blocking なし、29 tests 通過)。
  受理は**条件付き go の feasibility packet** として: AD-2 の定理文は
  「TN-3 成立 ⇒ N_T < ∞」の条件付き主張、AD-4 は条件付き go、TN-3 は §4
  GC-5 受理条件の blocking downstream obligation。これにより **go/no-go
  最小集合 {A.0, A.1, A.2a, A.3a, A.2b, A.2c(core+Z), B.0, C.0} は 8/8
  受理** — 第一段 go 判定の成立条件を満たす(判定記録は別途)。

- v0.26.7(2026-08-19): R-GC4B0 R7(blocking 2)適用 — [01] AD-2 の定理文
  自体を条件付きに訂正(「TN-3 が成立すれば N_T < ∞」— 証明状態注記のみの
  条件付けでは headline が無条件主張のままという指摘)。[02] claim-surface
  テストの FR §7 pointer 検査を (2c) 節切り出しに強化(文書全体の pointer
  では (2c) の pointer 削除を検出できないため)。

- v0.26.6(2026-08-19): R-GC4B0 R6(blocking 4)適用 — [01] TN-3 の位置付けを
  訂正: witness 生成義務と同列とした R5 の扱いを撤回し、**blocking downstream
  obligation** として §4 GC-5 受理条件に登録。AD-4 を**条件付き go** へ降格
  (TN-3 未解消の間 3|1 counting は未確立。反例が出れば B.0 撤回 = GC-4
  no-go 信号)。[02] z_c の型を閉鎖: z_c : K → 閉 chart 箱 ⊆ D̄(t₀, R_col)、
  tie 規則 = ≺ 辞書式、連続性は主張せず — jet ノルム 1 継承は compact 選択 +
  部分列 + Weierstrass(全階導関数の局所一様収束)で閉じる。[03] tagged union
  variant の「compact 型」主張を撤回(record 割当専用)— counting 用 compact
  空間は (2c) の K の閉包で、record domain と分離。[04] claim-surface テスト
  に F3′ 意味的検査を追加(FR §7 pointer の存在 + 固有式・profile の非再掲)、
  (2c) の F3′ 参照に pointer を付加。

- v0.26.5(2026-08-19): R-GC4B0 R5(blocking 4)適用 — [01] (iii) に W_c(3)
  適用前提(merge/prune 後ちょうど 3 相異 class・非零係数)を型として昇格、
  lower-arity route を明示。[02] raw exact-merge(実入力 — selector 以前に
  route)と counting 閉包の直径 0 blow-up face(jets 正規化極限対象)を分離。
  [03] (2c) を関数族ベースの 2 段分解に全面改稿 — 段 1(Z₀ 外・raw 連続族の
  Rouché 有限被覆)は無条件、段 2(Z₀ 近傍)は比較補題 **TN-3**(jet ノルム
  vs sup ノルムの一様比較)に条件付き。TN-3 は導出義務として GC-5 へ送る
  (候補経路: curve selection / Turán–Nazarov 型 doubling / 多項式係数 ODE
  零点評価。支持: 1-パラメタ弧解析・§9 TRIPLE-VALENCY 診断)。AD-2/AD-4/
  scope の主張文を条件付きに同期。[04] F3′ 再記述を FR 文書 §7 正本への
  pointer に統一(§3・§3.1・§8.9、v0.26.4 記載の表記修整を含む)、本文書を
  claim-surface テスト PR158_CLAIM_DOCS へ追加。

- v0.26.4(2026-08-19): R-GC4B0 R4(blocking 3)適用 — [01] (iii) の「deg ≤ 2
  prefactor」を F3′ 反例(正本: FR 文書 §7)により撤回し、**cluster 中心 jets 0..5 の
  ℓ² 正規化族**に置換(δ > 0 で W_c(3) が非全零を保証、δ = 0 まで連続延長・
  極限は球面上 deg ≤ 5 多項式 × 指数で ≢ 0 — jet cap 5 = D_W(3)・F3′ sharp)。
  [02] tagged union (iii) を jets 球面 ∈ ℂ⁶ + 直径 [0, 2ε_T] + 中心閉円板に
  (内部座標撤廃、直径 0 = exact-merge route)。[03] root list に「D(t₀,R_col)
  内部・相異・B の解析領域・R_col > 0 固定」条件を追加(外部根反例の排除 —
  (a)(b)(c) ⟺ unit が成立)。

- v0.26.3(2026-08-19): R-GC4B0 R3(blocking 4 + minor 1)適用 — [01] chain
  cluster(段 (3) 補集合の実体 — 直径 < 2ε_T の三角不等式)を (iii) の再正規化
  scale = cluster 直径で処理、[02] 計数半径を certificate の D̄(t₀, R_col) に
  一致させ外側 buffer R_out = 2R_col を導入、[03] tagged union の (ii) を ℂ³ に
  訂正 + 全 variant に閉値域(compact 型として閉鎖)、[04] root-coincidence
  witness を検証式 3 点(ord 一致・偏角計数一致・境界非零)で型化、[minor]
  AD-4 の数値再掲を §9 pointer に。

- v0.26.2(2026-08-19): R-GC4B0 R2(blocking 4)適用 — [01] counting の証明域を
  閉包 box の有限閉被覆に分離(半開 band は record 割当専用 — §8.7 (FL-0)
  方式)。[02] 3-class selector 述語表(d_min band 判定 + 第三 class 距離、
  段 (3) 補集合で網羅・排他)。[03] 非零性を球面 face の場合分けで補完
  (係数ベクトル非零 + W_c(3)/混合消去/単独項)。[04] V を商として定義し
  identity を root-coincidence witness で型化(§7.1 規約整合)、
  triple_membership_witness を chart label の tagged union に。[minor] v0.26
  履歴の Hurwitz 記述に撤回注記。

- v0.26.1(2026-08-19): R-GC4B0 R1(blocking 4)適用 — [01] A.2b からの「導出」を
  撤回し 3-class mini-atlas((i) plain / (ii) 片側 confluent divided-difference /
  (iii) 全 confluent、半開 band first-match)を本 packet 内に定義、luna 反例
  f_ε(0 退化)は再正規化 + **零点集合の scalar 不変性**で処理。[02] Hurwitz の
  不正確な言明を撤回し Rouché による**局所有界性**(R′ 円上非零 →
  N(g,R) ≤ N(f,R′))+ compact 有限被覆に置換。[03] triple_membership_witness を
  fail-closed 入力型として要求(導出義務は GC-5/GC-6 送り — 供給源の受理内容を
  超える主張を撤回)。[04] certificate 型に leading scalar s・monic P・
  deg r ≤ 2 明示・重複度付き根リスト・identity 検証 flag を追加(A.1/A.3a 整合)。

- v0.26(2026-08-19): GC-4B.0 ADAPT31 を §8.9 として起草 — (AD-1)
  TripleWeierstrassCert 型(fail-closed)、(AD-2) counting 補題(正規化 chart
  族の compact 性 + Hurwitz 上半連続性で N_T < ∞ — A.2b atlas を基盤に消費
  【注記(2026-08-19 追記): この Hurwitz 言明と A.2b 導出主張は R-GC4B0 R1 で
  撤回され v0.26.1 の Rouché/mini-atlas 版に置換済み】)、
  (AD-3) 供給源 2 系統(SPLIT4 tree triple / SIG-AUDIT radial 混成)の被覆、
  (AD-4) feasibility go 判定。§9 TRIPLE-VALENCY に数値結果(正規化 max 5、
  非正規化はスケール増大 — 非有界反例なし)を記録。

- v0.25(2026-08-19): **GC-4A.2c 確定** — A.2c-core 受理(R-GC4A2CCORE R4、fixed
  SHA `c0c9e05`)+ A.2c-Z 受理済み(`5ea87ec`)により、トップレベル A.2c(chart
  床・c_J = min c > 0)が component 両受理で完成。go/no-go 最小集合は
  A.0/A.1/A.2a/A.3a/A.2b/A.2c/C.0 = **7/8**、残り **B.0(ADAPT31)のみ**。

- v0.24(2026-08-19): **GC-4A.2c-Z 受理** — R-GC4A2CZ R3 ACCEPTED、fixed SHA
  `5ea87ec`(confluent Hermite Vandermonde・決定的 matching・SS 1/12・r_pole
  算術・NF-7 条件付き合成すべて検算通過)。core 側 R3(blocking 2 — stale
  (FL-7) label 3 箇所と Z/G 残骸の non-operative 化)を適用。

- v0.23.4(2026-08-18): R-GC4A2CZ R2(blocking 2 + minor 2)適用 — [B3] double
  root の列一致問題を **confluent(Hermite)Vandermonde**(対称座標の中心/
  判別式方向 = ζ^{−(n+1)} と (n+1)ζ^{−(n+2)} の微分列対、base 節点相異 +
  総列数 ≤ 4 ≤ 行数 5 で非特異)で解消。[B2] occurrence を (side, 値, 重複
  index) でラベル付けし辞書式最大 max-weight matching として決定化。[m1]
  単独根定数を M₀ に統一 + [r_pole, r₀) 帯 = Taylor box 担当を明記。[m2]
  §8.7 consult 記録を純 pointer 化。

- v0.23.3(2026-08-18): R-GC4A2CCORE R2(blocking 3)適用 — [01] 依存方向を
  「ZG-NF が core の generic (FL-6) を消費」の一方向に統一(NF-6 の逆向き参照
  文を修正)、[02] §8.7 目的文から global c_J を除去(core = per-box 供給)+
  FL-0 の旧 FL-7 参照を NF-7 へ、[03] FL-4 の Z/G 固有部と零点近接ブロックを
  historical/non-operative と明示(正本 = §8.8)。

- v0.23.2(2026-08-18): R-GC4A2CCORE R1(blocking 2 + minor 2)と R-GC4A2CZ R1
  (blocking 3 + minor 2)を適用 — core: [01] §8.7 の FL-7 を core 供給
  (FL-7′)に縮小し global c_J を §8.8 (NF-7) に一本化、[02] FL-6 を非 Z/G
  strata の generic 補題に scope 限定(依存方向 core → ZG-NF を明記)、[m1][m2]
  見出し・台帳の状態/依存を更新。Z: [B1] S_i 閾値を r₀ に統一(annulus gap
  排除)+ pole-face 床を結合評価(SS は小さい方の冪で下界 — ρ₂ 非依存)+
  r_pole = min(r₀, [24(M₀+1)]^{−1/3})、[B2] max-weight matching(exact 対
  重み 2 で最優先)+ multiplicity 付き occurrence multiset 型、[B3]
  **defect-kernel 補題の証明**: defect 全微分は n!ζ^{−(n+1)} の generalized
  Vandermonde(≤ 4 列・≥ 5 行・節点相異非零 ⇒ 単射 — unit 干渉は構造的に不在)
  ⇒ defect-normal に kernel なし、compactness は (v-d) 次元帰納で供給、
  [m1] consult 記録の技術骨格重複を §8.8 pointer に縮小、[m2] NF-7 を
  「core 受理前提の条件付き合成」に整合。

- v0.23.1(2026-08-18): §8.8 GC-4A.2c-Z ZG-NF を consult #12 骨格どおり起草 —
  (NF-1) 固定閾値 r₀/M₀/r_pole(循環解消)、(NF-2) bipartite 同時最大 matching、
  (NF-3) projective 因子正規化と片側 κ 評価(Remez 不要)、(NF-4) 正しい恒等式
  Φ_Q(x) = A₂Φ_Q(x′) + (A₁−A₂)B₁(x′) と exact jet defect による Δ_ZG 二分法、
  (NF-5) 補題 SS(1/12、3 ≤ n ≤ 8、初等証明)、(NF-6) strata 列挙・対称係数
  座標・defect-normal 横断性(既存 collapse 参照)、(NF-7) 最終合成。

- v0.23(2026-08-18): **Sol consult #12(Z/G 床の裁定)を §8.7 冒頭に記録し、A.2c を
  component 分割** — A.2c-core(W_CONFL・mixed・collapse・Z/G 以外)と A.2c-Z
  (ZG-NF: 同時 matching + projectivized defect、§8.8 起草予定)。§4 台帳を 2 行に
  分割。トップレベル A.2c は A.2c-Z 完了まで未受理(「条件付き受理」とは記録
  しない — Sol 裁定)。no-go 評価 amber(中低 → 中)。R14 の 6 blocking のうち
  Z/G 固有分は A.2c-Z の全面書き直しに吸収、core 側は次 round で査読。

- v0.22.11(2026-08-18): R-GC4A2C R13 findings(blocking 8 + minor 1)適用 — 構造的
  鍵: **(ZF-1) により collar 内零点は P̃ 由来 ≤ 2/side・計 ≤ 4** — cluster は高々
  2 元で多重スケール階層は生じない。[01] first-match 順序(4a exact → 4b same-side
  → 4c cross-side)。[02] 「同符号強め合い」三角不等式を撤回し、2 元 cluster の
  **連続 2 指数評価** max(|xⁿ+1|, |x^{n+1}+1|) ≥ 1/4 に置換。[03] S_small の
  形の分類(空/単独/same-side 2 元)+ r_pole に band 上限 ε_G/2 を追加(幾何的
  保証)+ M の有限性根拠。[04] C_pert の明示(C_jet = Cauchy、C_box = 乗法
  sup-norm 摂動)。[05] η ≳ κ 帯の被覆を摂動補題から gcd-jump stratum tube
  ((v-d) 帰納の正式な一員)に移管。[06] x∖pair = 因子除去の低 deg-branch box、
  base case = collar 零点 0 個。[07] Z/G proof box を Taylor box に正式再構成
  (C₂ は Taylor box 上の sup — pole zone は直接床で proof box 外)。[08] slice
  変換を線形床→線形床の形で書き直し。[minor] B_CONFL status 注記(正本 = §8.7
  (FL-2)、§8.6 の「目標」表記は受理時点のまま不変)。

- v0.22.10(2026-08-18): R-GC4A2C R12 findings(blocking 4 + minor 2)適用 — [01]
  零点近接を §8.6 routing と整合する 3 分割に再構成(相殺は cross-side のみ —
  same-side は同符号で強め合い Z sub-box でも発散 genuine)。[02] 定量的発散
  (remainder 上界 M の有限性根拠 = band 分離 + (ZF-1) collar 有界 + jets ≤ 9 のみ
  必要、閾値 r_pole = (2M)^{−1/3})。[03] G-box を摂動補題に格上げ(cross-side 対 =
  unit 因子 1 + O(η)、φ・κ とも η-摂動、零点個数の有限帰納で低 box の床へ移送、
  半開 band で排他的)。[04] Z-core を pole zone(直接床 φ ≥ M — Taylor 不要)と
  Taylor zone(C₂ 有限 — tube 帰納の適用域)に分離し FL-6 との衝突を解消。
  [m5] slice 変換式(φ 不変・κ 1 次同次 ⇒ 損失は s_max の 1 乗 — 旧 (定数)^9 は
  撤回)。[m6] §4 A.2c 行の B_CONFL 記載を「正本 = §8.7 (FL-2)、status = state 列」
  に統一。

- v0.22.9(2026-08-18): R-GC4A2C R11 findings(blocking 2)適用 — [B2] 旧「P 閉箱の
  面」列挙の残骸を撤回(境界は anchor 円板球面のみ)、C_i の c_a = 0 面の routing を
  joint 球面の対称 face として明示、§8.6 受理済み ‖·‖_∞ 正規化と proof cover の
  ℓ² slice の norm 同値変換を明記。[B4] 「ζ_j → 0 で必ず発散」を撤回(モーメント
  相殺反例 — 零点対距離 ε^{N+1})し、selector band 分割に置換: Z-box core(零点
  相互分離 ≥ ε_G band)では相殺 partner が不在で発散 genuine((0,∞] 値連続)、
  collision 帯は G/D box の divided-difference/divisor 座標が相殺後の有限値を
  正則値として扱う — 被覆は半開分割で排他的。

- v0.22.8(2026-08-18): R-GC4A2C R10 findings(blocking 5 + minor 2)適用 — [B1]
  主張域参照を v3 に統一 + 型不変条件(v2/v3 の α 同一値、α_k = p_k/λᵏ・p = T₂u・
  global λ への依存を field 制約として明示)。[B2] C 家族の scale データを
  **joint ℓ² 球面**(plain 係数 + prefactor 係数を同一球面で正規化 — P_i = 0 と
  c_a = 0 が同種 face に統一、旧「P 閉箱の面」列挙を撤回、P_i = 0 face の
  routing(残存 class の再正規化 + label drop)を定義)。[B4] C̃ の正規化を
  ℓ²(degree-drop 面でも定義)に変更、面延長補題の値域を **[0, +∞] 値連続**に
  修正(ζ_j → 0 は principal part 発散側 — 床に無害、compactness は正値性 +
  下半連続で走る)。[m1] §4 A.2c 行の「terminal chart」表記を structural proof
  box に同期。[m2] C 家族 joint 球面の norm 同値定数(≤ √6)を (6-iv) に補記。

- v0.22.7(2026-08-18): R-GC4A2C R9 findings(blocking 3 + minor 1)適用 — [B1]
  GCRouteRecord-v3 を正式宣言(α_k := p_k/λᵏ の等式を型定義に内蔵、flag
  |α_k| ≤ R_Q/2、v2 不変・強化方向の versioned 拡張)し、主張域 = 「v3 record が
  生成し得る配置」と厳密化。[B2] ambient を box 家族別に分離(plain 家族は
  P 因子なし・実次元 19、C 家族は P も ℓ² 球面・実次元 30 — (0,0) 零面を球面で
  排除、片側零は support-drop stratum)。[B4] Z/G jet map を log 微分の
  scale-free 形で評価(C_i′/C_i は係数 scalar 不変 — R9-B4 の ε 倍反例は jet 値に
  影響しない)、分母下界は正規化 C̃_i に対する collar 距離 + unit 有界性のみ。
  [m1] collar 距離の表記を正規化座標 |ζ_j| ≥ λρ/13 に統一。

- v0.22.6(2026-08-18): R-GC4A2C R8 findings(blocking 3)適用 — [B1] C_p の解析的
  supply chain 主張を撤回し、band 所属を **fail-closed witness の定義的保証**に
  還元(margin 版 q_band_witness-v3 を versioned 拡張で宣言 — 境界 stratum は
  域上空(定義的)。充足可能性は GC-5/GC-6 の義務として scope に明示)。[B2]
  ambient を ℓ² 球面 slice に変更(tie 面問題回避、N_amb = 31 明示)、境界 strata
  を列挙、gcd-jump 条件を **t₀ での座標消滅(線形条件)**に簡素化(d₀ は点での
  ord — subresultant 撤回)。[B4] 面延長補題を box 家族別に分岐(M/R/S/D = ε_Z、
  Z/G = divisor 除去後 C_i(t₀) と collar 距離・unit 有界性による下界)。

- v0.22.5(2026-08-18): R-GC4A2C R7 findings(blocking 5)適用 — [B1] 主張域を
  A.2a-admissible 窓上の非終端配置に明示(u の branch は A.2a 決定で固定 ⇒ p(x)
  一価 — 円筒 quotient は撤回、𝒬_band は §8.6 の ℂ³ polydisc のまま)、C_p の
  supply を実 interface(位相差 ≤ 2 + log(P̃比)/log(V比) の collar Cauchy 評価
  (zf_witness/divisor_record)+ |u| の record witness)に接続。[B2] 固定 compact
  ambient X_amb の明示 + 離散 label による局所閉有限分割 + frontier 型別の
  余次元表(gcd-jump は subresultant 型多項式 S_k、恒等零でない解析関数の零集合
  = 次元 strict 減)。[B4] 「終端 box 評価」を撤回し**面延長補題**で置換: φ は
  log の定数・二次成分を T₂ が exact に消すため、κ は min-sup の連続性により、
  ともに box 閉座標域全体へ連続延長 ⇒ 床は閉域全体で成立し被覆は有限 compact 和
  (renormalize 間比較も不要 — intrinsic 量)。[B3a] 被覆段落の撤回済み c_side
  依存を除去(R6 との矛盾解消)。[B3b] κ の Lipschitz 性の証明を supply(compact
  上の導関数上界 + min の 1-Lipschitz 性)。

- v0.22.4(2026-08-18): R-GC4A2C R6 findings(blocking 3 + minor 1)適用 — [B1]
  incidence を内在的 fitted p(x) = T₂u で定義(min 選択・canonical strip を撤廃、
  α₀ は Φ_p の 2πi 不変性により円筒 ℂ/2πiℤ 上の量 — 半開 strip の非 compact 性
  minor も解消)、係数比 gap の supply 元を A.0/A.1 held-cell 有界性 witness に
  変更(未定義 ε_band 依存を撤回)、C_p := max(2, C_H + 2π)。[B2] stratification を
  raw 係数の固定 ambient に変更(P̃/deg 分枝は派生量 — coprime 自己矛盾を回避)、
  gcd-jump は subresultant rank 条件で proper 性を証明。[B4] side 全滅面の
  κ ≥ c_side 主張を撤回(交差退化の反例 — R6-B4)し、終端 box 評価方式
  (boundary_routes 有限鎖の終端で全退化が box 正規化により解消 — skip-(3)
  first-match の返す box)に置換。

- v0.22.3(2026-08-18): R-GC4A2C R5 findings(blocking 4 + minor 1)適用 — [B1]
  canonical strip(Im α₀ ∈ [0, 2π))で incidence の 2πik 周期を切り、C_p を明示式
  (α₂,α₁ ≤ 2 × 箱半径、|Re α₀| ≤ log(1/ε_band))に置換(Cauchy 評価の宣言を撤回)、
  R_Q := 2C_p の §8.6 整合(存在宣言のみ受理・値指定は緩む方向の拡張)を明記。
  [B2] frontier 型別の次元表(追加方程式 × 拘束される自由パラメタ × proper 性根拠)
  で dim strict 減を証明。[B3] **mixed C_i box の内部に QR 点が存在しない**こと
  (3 相異 class の prefactor 付き独立性で全係数零)を証明し、mixed 型 collapse を
  不要化(d₀ = 2 比較懸念も消滅)。[B4] 床の定義域を非終端(r ≥ 2・両 side 非空)に
  限定、side 全滅面には Z_QR が接近しない(|e^Q| ≤ e^{3R_Q} 有界 ⇒ κ ≥ c_side > 0)
  ことを証明、intra-side 係数面は intrinsic 量の chart 非依存性で box 跨ぎ移送。
  [m1] §8.7 の数値再掲を削除(authoring location = §9 のみ)。

- v0.22.2(2026-08-18): R-GC4A2C R4 findings(blocking 3 + minor 2)適用 — [01][02]
  (6-v) を精密化: (v-a) R_Q := 2C_p の宣言で Q-band 境界 strata を空に(tangent
  cone 場合分けの循環懸念を根絶)、(v-b) 帰納順序を A.2c 内部の **stratum 次元**に
  変更(frontier は追加の閉条件で dim strictly 減 — §8.6 rank との混同を解消)、
  (v-c) collapse 二分法が全 frontier 型(gcd-jump/degree-drop/support-drop)で
  成立することを明記、(v-e) 一様 Taylor 定数 C₂ の定義。[03→R4-03] proof box を
  K_{C,k}(d₀ 分枝のみ — σ は Z_QR 内部 stratification の label に降格、Q-band
  face 添字は (v-a) で不要化)の**有限閉被覆**に変更し、一意割当を撤廃(床は
  box ごとの主張なので被覆で十分 — 被覆補題)。[m1] QC-TRANSV の数値再掲を削除。
  [m2] FL-7 の合成対象を structural proof box のみに明記(Q_C 除外)。

- v0.22.1(2026-08-18): R-GC4A2C R3 findings(blocking 3 + minor 2)適用 — [01]
  (6-iii) を stratum 別に修正: regular stratum は pair ごと collapse で 2 指数
  deg ≤ 2 系(prefactor 定数なので P·δq 上昇なし)→ W_CONFL bound 6 < 10、
  C stratum は 1 指数 Π₄ → ord ≤ 4 < 10。[02] (6-v) を有限 poset 上の tube 帰納に
  改稿(基底 = 閉 strata、帰納段 = frontier tube を除いた compact 部で σ₀ > 0、
  被覆と定数移送を明示)、SING-FRONTIER を「open no-go」から「帰納の数値検証
  (診断)」に再位置づけ。[03] (6-i) 接空間式を smooth stratum 内部・非特異
  branch に限定(境界は tangent cone — frontier stratum 送りで (6-v) は不使用)。
  [m1] skip-(3) first-match による proof cover への写像と網羅補題、K_{C,d₀,σ,f}
  記法。[m2] QC-TRANSV の authoring location を §9 に一本化、DEG4-SHARP の
  「QR 横断に現れない」を (6-iii) 依存の裁定として明示。

- v0.22(2026-08-18): Sol consult #11(confluent-QR 角の裁定)適用 — §8.7 を
  stratified transversality architecture に改稿: (FL-0) proof cover の selector
  からの分離(Q_C は簿記専用に降格、(support, deg, d₀, QR pairing σ, Q-band face)
  の有限細分、零集合一致 {φ=0} = {κ=0}、frontier の rank 帰納)、(FL-2)/(FL-2b) の
  床変換の結論を「Φ_p ≡ 0 ⇒ κ = 0」に訂正(「係数全零」は誤り — W_CONFL の役割は
  零集合分類)、(FL-6) を 6 段に改稿(incidence 接空間の陽式・rescaling ⊂ T Z_QR
  (⊕ は二重計上で撤回)・stratum 分類・**QR collapse による核特徴づけ
  (δΦ_p = e^qR、R ∈ Π₄ ⇒ ord ≤ 4 vs 橋 ord ≥ 10)**・‖c‖₂ slice・相対床)、
  §9 に DEG4-SHARP(sharp = 2d+2、d=4 の 10 は QR 横断に現れない)と
  SING-FRONTIER(残存 no-go test、A.2c 受理後最優先)を登録。

- v0.21.2(2026-08-18): R-GC4A2C R1 findings(blocking 5 + minor 2)適用 — [01] FL-4 の
  モーメント Vandermonde を撤回(unit-jet 相殺・重複度を扱えない)し「Z/G 内点 =
  genuine 配置の座標表示 ⇒ FL-1 適用、固有の極限対象クラスなし」の帰着に置換。
  [02][05] FL-6 を 5 段の局所商空間証明に全面改稿(Z_QR の W_c(4) 対形成による明示
  パラメタ化、ker J = T Z_QR ⊕ rescaling の W_CONFL 特徴づけ(Q₀ 選択写像不使用)、
  法束球面の compactness、κ の Lipschitz 上界(下界不要)、C² 一様 Taylor)。FL-0 に
  (chart, d₀) 対ごとの床と φ の連続性根拠、Q_C の κ=0 除外を明記。[03] gcd 記号を
  A.1 に整合(D = gcd(P₁,P₂)、P̃ 互いに素、deg P̃ ≤ 2 − deg D)。[04] FL-5 に exact
  極限写像(D: E_i 線形収束、S: cosh/sinh 恒等式 + weighted witness 一様収束 →
  FL-2b 対象)を供給し QR5 外部参照を撤去。[06] T 単射性の a = 0 分岐と c₄ = 0 枝の
  訂正。[07] scope の「C 系」表記衝突を解消(dispatch 経路 B/C と C chart は別物)。

- v0.21.1(2026-08-18): §8.7 起草直後の self-review 修正(査読前)— d₀ の構造的
  上界を 2 に訂正(deg gcd(P̃₁,P̃₂) ≤ 2 — v0.21 の「≤ 3」と書きかけ文は誤り)、
  (FL-2)/(FL-2b) の床変換を d₀ 場合分け(gcd 除去で reduced prefactor 次数が
  d₀ だけ下がる: d₀=1 ⇒ deg≤1 bound、d₀=2 ⇒ 定数 ⇒ W_c(r))で全ケース直接
  閉鎖に書き換え、(FL-4) の short-range 委譲を撤回(d₀ ≥ 3 生成禁止)。

- v0.21(2026-08-18): GC-4A.2c CONFL22 ドラフト起草(§8.7)— (FL-0) 床の統一形式、
  (FL-1) genuine 配置(compactness + EX-3/EX-4 + W_c(r))、(FL-2) **W_CONFL(2,2) v2 の
  消去法証明**(1 回微分の交差消去 + 次数勘定 + 補題 EL、B = 6 / deg≤1 は 4 —
  fixture ⑥ の sharp 値と一致)、(FL-2b) 片側混合系の逐次消去(ord ≤ 8)、
  (FL-3) W_c(r) 帰着、(FL-4) Z/G(collar の E-零点排除 → ≤4 極の 7 連続モーメント
  Vandermonde + d₀ ≥ 4 生成禁止【注記(2026-08-18 追記): この Vandermonde 論法は
  R-GC4A2C R1 [01] で撤回され v0.21.2 の帰着に置換済み】)、(FL-5) D/S 低 arity
  帰着、(FL-6) Q_C
  transversality(exact QR の位相対形成 → 線形化が 2-class deg≤2 系に collapse →
  W_CONFL 適用 + σ_eff compactness。QC-TRANSV 数値診断を §9 に登録)、(FL-7) 合成
  c_J = min c_C > 0(K = 1)。§4 A.2c 行 → drafted。

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
