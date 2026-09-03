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
| GC-4A.3b PBK22-D10 | A.1/A.2a/A.3a/A.2b | 10 階上界・scale cap(WE₉ の純入力)— collar unit 両側 bound、u′ 明示 bound 経由の Cauchy 10 階、正規化剰余 R̂(θ) ≤ C·θ¹⁰ | **accepted(§8.12、R-GC4A3B R2 PASS、fixed SHA `b75aa85`)** |
| GC-4A.4 PBK22-WE9 | A.0/A.1/A.2a/A.2b/A.2c/A.3a/A.3b | 局所窓外挿(JF₉/d10 の純 consumer)— Chebyshev 係数補題、κ 上界式(深平坦 ⇒ 定量的 near-QR)、二次比枝の kernel 不等式 ρ⁻² | **accepted(§8.13、R-GC4A4 R2 PASS、fixed SHA `9f1a18d`)** |
| GC-4A.5a0 PBK22-QRG | A.2a/A.4 | exact QR(v ≡ 0)の大域化 — 恒等定理で Φ_p ≡ 0 を entire 恒等式へ、WE-3 の分枝接続条件を無条件供給(consult #14) | **accepted(§8.14、R-GC4A5A0 R4 PASS、fixed SHA `68d114a`)** |
| GC-4A.5a1 PBK22-PTN-SPEC | consult #15、GC-2、GC-3(D-PBK-22)、GC-4C.0、A.2a/A.2b/A.3a/A.3b/A.4/A.5a0 | BORD-22/PTN-22 の **interface 型固定(proof claim なし)** — raw projective pair・stratum record・t3 witness・window contract(zf 条件必須 — §9 BORD22-PROBE F1b が裏付け)・projective common-zero 拡張・exact QR exit・(PTN-22) statement 登録・ptn22_witness-v1 | **accepted(§8.16、R-GC4A5A1 R4 PASS、fixed SHA `5d7400a`)** |
| GC-4A.5a PBK22-COND9 | **BORD-22/PTN-22(blocking obligation — consult #15)**、A.2a/A.2b/A.2c/A.3a/A.3b/A.4/A.5a0 | projective one-hop conditioning — **定理 draft は R1 で撤回**。再設計: PTN-SPEC(interface — A.5a1、§8.16 accepted `5d7400a`)+ BORD-22(GC-5-T2)+ PTN-22(GC-5-T3)。COND9 は PTN-22 からの reduction packet に降格。**A.5a は PTN-22 受理まで open** | **withdrawn → 再設計中(§8.15 追記)** |
| GC-4A.5b PBK22-RESTART | A.5a/A.3a | g-small ⇒ 実 root/pole 排除 ⇒ zf_witness 再選択(ZF-2 再実行)⇒ fresh principal branch。cell 境界 handoff | open |
| GC-4A.5c PBK22-CHAIN | A.5a/A.5b | 閾値二分岐(σ ≥ τρ⁹/D_ch → (c-ii) 型 / σ < → chain)、初回のみ ρ⁻⁹、D_ch = C_init·B^{N_hop+1} ledger、深平坦 kernel 完成(QR5 P3 ledger 移植) | open |
| GC-4A.6 PBK22-ASM | A.5(:= 集約 {A.5a0, A.5a, A.5b, A.5c} — 本行で正式定義。§8.3/§8.4/§8.12 等の accepted 本文中の「A.5」参照はこの集約を指す)| 全場合合成・最終 γ・cost spec・GCRouteSpec 昇格・fail-closed tests | open |
| GC-4B.0 ADAPT31 | GC-3、c=3 FR、A.2b atlas | triple divisor adapter の feasibility(chart 付き Weierstrass certificate — 接触次数 ≤ 5 だけでは足りず collar 内総零点数/valency が必要。**供給源 2 系統(prepared tree triple / radial 混成 3 原子和)の両方を scope に含む** — GC-4C.0 (3) 表。失敗は 3|1 の重大 no-go 信号)。**go/no-go 最小集合** | **accepted(§8.9、R-GC4B0 R8 PASS、fixed SHA `eee39bf`。受理時は TN-3 条件付き go — TN-3 は GC-5-T1(`906bd1a`)で解消し、条件解除 = feasibility go)** |
| GC-4B PBK-31 | B.0、GC-4A 系 | `3|1` kernel 本体。c=3 child certificate を消費し、旧 U_F/SVD 係数へ戻らない | open |
| GC-4C.0 SIG-AUDIT | GC-2/3 | 原子レベル radial signature の完全列挙(8)・margin 安定性・A/B/C dispatch 表・irreducible endpoint 特定・transition 有界性。**go/no-go 最小集合** | **accepted**(R-GC4C0 R3 PASS、fixed SHA `aa95124`) |
| GC-4C PBK-M4 | C.0、GC-4A/B | 多分岐 node kernel 本体(`[4]` held + separated compact + dispatch 接続) | open |
| GC-5-T0 BORD-3 | c=3 資産(補題 W_c/W′、FR-S1′ §8.4/A′-4 (L-d)、FR-S1″ §9.3–9.5 (L-d)、Fock RKHS 評価、2 原子 confluent 補題 (B3-4a)) | 3 原子 border 極限の**点一様 ord ≤ 5**(moving-center sequence 形 — TN-3 の消費補題。consult #13 で独立 packet 先行と裁定) | **accepted(§8.10、R-BORD3 R6 PASS、fixed SHA `87863cc`)** |
| GC-5-T1 TN-3 | GC-5-T0 | 比較補題 TN-3 本体 — **BORD-3 の (B3-2)–(B3-4) が任意列に対して証明されたため curve selection は不要化**(consult #13 α′ の部分解析幾何は消滅)。列の対偶だけの短い系 | **accepted(§8.11、R-TN3 R2 PASS、fixed SHA `906bd1a`)** |
| GC-5-T2a BORD22-ATLAS | GC-5-T0/T1 資産、A.5a1(interface — accepted `5d7400a`)、GC-2/GC-3 | **有限 chart coverage theorem**(consult #16 で T2 を 3 分割): within-child merge/prune 反復 + cross-child matching(合算禁止 — 相殺記録のみ)、support rank routing、root/child 3-scale rate atlas(比の再帰 blow-up で有限)、QR/outer-inner common-zero/denominator chart、**W_zf 静的被覆(W ∖ Σ の被覆 + 移管領域 Σ の帰属排反 — bubble-routing 被覆補題)**。受理条件 = 「任意の admissible T3 列が lower-rank / QR exit / 有限 chart のいずれかへ必ず入る」の一主張のみ | **accepted(§8.17、R-T2A R9 PASS、fixed SHA `08c2d0e`)**(A.5a blocking obligation — T2b/T2c/T3 受理まで A.5a open) |
| GC-5-T2b BORD22-FRAME | —(集約行: T2b := {T2b-0, T2b-i, T2b-ii} — consult #17 で 3 分割)| **tree-Newton 経路は R-T2B R1(blocking 6)で撤回** — 再設計 = **J⁹-SVD/graph frame + framed \| overflow 二択**(§8.18 追記)。構造原理(carrier 成分直交 block 対角・二段正規化)は存置し下位 packet が再消費 | **withdrawn → 再設計(3 分割 — 下 3 行)**(A.5a blocking obligation) |
| GC-5-T2b-0 GAUGE-SCALE-ADAPTER | GC-5-T2a(accepted `08c2d0e`)、FR §8.4 gauge section、§8.9 追記 | **atlas_witness-v1 → frame_input-v2 の前処理補題** — common_gauge_record-v1(pivot leaf・同一 U_n の pair 両成分適用・scalar 吸収表・全 4 原子の K_{δ_ℱ,R_ℱ} 所属 evidence・strong section evidence)+ **node_scale_bridge**(d_parabolic / t_increment の型分離 — d²/2 ≤ t ≤ (√5/2)d、統一しない)+ **TR3(root_far \| root_collapse) versioned sublabel**(T2a 非改変の下流拡張) | **accepted(§8.19、R-T2B0 R3 PASS、fixed SHA `7103b2e` — 箱前提の供給は §8.22 (CC-5) で解消(frame_input-v2.1)[R-T2BII R1-05])** |
| GC-5-T2b-i HEAD9-ACTUAL(旧 HEAD9-FRAME は §8.20 で撤回)| T2b-0(accepted `7103b2e`)、(B3-4) RKHS 規約 | **実 defect 限定の moving-center 二択**(consult #18 — full-span V_n 単位球の strong compactness は PTN-22 が消費しない過剰目標として非目標化): β_n := ‖J⁹_{ζ_n}f_n‖ の **head_good(weak/compact-open 極限 f_* ≠ 0・ord_{ζ_*} ≤ 9)\| head_overflow(typed candidate — PS-9 detected は生成しない、橋は T2c-ov)** | **accepted(§8.21、R-T2BIA R1 PASS、fixed SHA `e5de2f6`)** |
| GC-5-T2b-ii CARRIER-CHART(旧 CHART-FRAME を consult #18 で再定義 — defect 側 chart 消費表の義務は削除(defect は weak 化))| T2b-i(accepted `e5de2f6`)、T2b-0(accepted `7103b2e`)、§8.10 (B3-4a)/(B3-3)/(B3-4)、FR §8.4 | **carrier 側の完結**: 成分別 1/2 原子 strong frame(分離原子・(B3-4a))、⊕ block 対角 Gram の一様床(閉 compact chart constructor 上の下半連続 inf)、**箱供給補題**((CC-5) Möbius margin — T2b-0 の箱前提 obligation を standard box + frame_input-v2.1 で解消 [R-T2BII R1-05])、**raw 再主張系**(gauge の pointwise 移送禁止 — EW-B) | **accepted(§8.22、R-T2BII R3 PASS、fixed SHA `ccb1b6d`)** |
| GC-5-T2c BORD22-FLOOR | T2b 完結(T2b-0 `7103b2e` / T2b-i `e5de2f6` / T2b-ii `ccb1b6d`)| moving-center **projective order ν_ζ = ord(f_*) − min_i ord(B̂_{i,*}) ≤ 9(defect-order 形 — 和の極限は経由しない)**(主張値は予算 9 — D_W*(4) = 8 の sharp 化は別 packet、consult #16)+ 量的連鎖((χ, c₀) ごと — defect: **eventual** ‖J⁹f_n‖ ≥ σ₀(χ,c₀)/2 ≥ (σ₀(χ,c₀)/(2C_R))sup、carrier: 十分先の n で min_{W_core,n(ρ)} max_i\|B̂_i\| ≥ m_C(χ,c₀,ρ)/2 — eventual、上界 M_C = C_R は全 n pointwise)+ 対偶(eventual 形)。ここで BORD-22 を accepted 化。**+ 3+1 mixed-span valuation lemma**(consult #17)。**消費は head_good 枝のみ・floor_input-v1 経由で vanish_flag = none 限定・ρ ≤ r_{S,n} eventual evidence 必須**(head_overflow は T2c-ov へ — 循環なし、consult #18 / R-T2C R7)| **accepted(§8.23、R-T2C R8 受理 SHA `15b272e`、8R)** — **BORD-22(T2 chain)完成**(A.5a blocking obligation は T3 PTN-22 受理まで維持) |
| GC-5-T2c-ov OVERFLOW-PS9-BRIDGE | T2c、§8.16 (PS-9) | **head_overflow_candidate → PS-9 detected の変換**(実 raw defect の window/carrier/denominator を結合し、同一 raw data で ‖g‖_S/((s/L)⁹‖g‖_W) → 0 またはその既証明同値量を示す)。**返り値は detected \| not_proven** — 橋が閉じない場合は `unresolved_head_overflow` で止め、detected を生成しない(consult #18)。配置 = T2c 後・T3 前 | open |
| GC-5-T3 PTN-22 | GC-5-T2c | **projective/weighted 二窓比較** ‖g‖_W ≤ C₂₂(L_C/s)⁹‖g‖_S(interval-scale Remez + denominator floor の合成 — statement 登録 = §8.16 (PS-7)、出力 = (PS-9) valid \| nogo)。**consult #19(Sol)で 3+1 分割**: T3a0 → T3a → T3b → T3c(下 4 行)— 本行は集約。**指数 9 は全経路一回払い**(hop ごと Remez は (L/s)^{9N} を生むため禁止 — Sol 裁定) | open(集約 — **A.5a blocking obligation**、受理まで A.5a/A.5b/A.5c/A.6 open) |
| GC-5-T3a0 PTN-LOWER-FACE | (AT-2) exit 行および chart 枝の非 exit config(synthetic_face の親 — GC-5-T2a)、BORD-3 `87863cc`/TN-3 `906bd1a`、**GC-5-T2b-ii (CC-3) の c₀ witness 構成・GC-5-T2c の c₀ 固定量化規約**(face_approach の c₀ evidence 消費 [R-T3S R3-04])(GC-5-T3 行は親 = 包含であって依存ではない [R-T3S R1-05]) | support rank ≤ 3 の **projective 二窓比較 base**(well-founded support-rank induction の底 — window_contract 継承・projective denominator・rank-4 近傍の摂動安定性。statement = §8.24 (TS-1) — **登録 accepted `dfc572b`(R-T3S 7R)**。**c₀→0 循環切断の要**: atlas lower-rank exit ⇒ 解決済みとしない — consult #19) | **drafted(§8.25、R7 適用済み・査読待ち R-T3A0 R8)**(A.5a blocking obligation — T3 集約経由)、見積 3–5R |
| GC-5-T3a PTN22-ROUTE | T3a0 | 境界 routing 完備化: c₀→0(→ T3a0 induction)・**one_sided ⇒ c₀→0 吸収補題**(固定 K_χ(c₀) の Gram 床 + 係数下界 ⟹ 両成分生存 — 証明できなければ CC-3/CC-7 上流欠陥)・lower-rank/exact-QR/overflow の排他的分岐・T3 入口 gate(floored×head_good のみ、T2c-ov detected→nogo / not_proven→unresolved 停止) | open(A.5a blocking obligation — T3 集約経由)、見積 2–4R |
| GC-5-T3b PTN22-SCALE-HOP | T3a | **scale-covariant 床**: s_n→0 で固定 ρ が消える主縮小 regime(consult #19 の最危険点 1 位)— ρ_n ≍ s_n の core/bubble 分解・rescaled inner chart の carrier floor(s_n 非依存)・bounded-overlap で scale-neutral な有限被覆。statement = §8.24 (TS-2) — **登録 accepted `dfc572b`(R-T3S 7R)** | open(statement 登録済み・証明未着手 — A.5a blocking obligation — T3 集約経由)、見積 5–8R |
| GC-5-T3c PTN22-REMEZ-CLOSE | T3b | violation_sequence-v1 の列-矛盾実行・δ 相殺・**interval-scale Remez 一回払い**(ν ≤ 9 は最終不等式でのみ使用)・C₂₂ = max_{finite routes}[C_geom·(2M_C/m̄_C)·C_Rem]・(PS-9) 出力 | open(A.5a blocking obligation — T3 集約経由)、見積 3–5R |
| GC-5 FR4-S1 | GC-1/2 | c=4 全 topology の exact J^{D_W(4)}-SVD frame、compact floor、tail、Gram、**TN-3(§8.9 比較補題)— GC-5-T1 で解消済み(`906bd1a`)** | open |
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

**§8.9 追記(2026-08-19、[R-TN3 R1-01] — accepted 本文(`eee39bf`)は不変。
chart 箱定数の指定)**: (2c) の K の「閉 chart 箱」は、受理時点で数値を固定
していない chart 定数である。これを **Fock 可容箱 |A_j| ≤ 1 − δ_ℱ、
|B_j| ≤ R_ℱ**(δ_ℱ > 0、R_ℱ — FR 文書の compact class K_{δ,R} と同じ束縛、
§8.10 (B3-1) と同一)**に固定する**。これは未指定だった箱定数の指定であり、
受理済み主張の変更ではない(受理済み主張はすべて chart 定数に相対的)。
以後 §8.9 (2c)・§8.10・§8.11 の K は同一の型を指す。

**§8.9 追記 2(2026-08-19 — TN-3 解消)**: 比較補題 TN-3 は GC-5-T1
(§8.11、R-TN3 R2 PASS、fixed SHA `906bd1a`)で証明された。これにより
(AD-2) の N_T < ∞ は**無条件**に成立し、(AD-4) の「条件付き go」の条件は
**充足済み**(= B.0 は feasibility go)。本文の条件付き文言は受理時
(`eee39bf`)の歴史的記録として不変のまま残す。

### 8.10 GC-5-T0 BORD-3(3 原子 border 極限の点一様 ord 上界 — **accepted、R-BORD3 R6 PASS、fixed SHA `87863cc`**)

**目的**: §8.9 (2c) の比較補題 TN-3(§4 GC-5 受理条件の blocking downstream
obligation)が消費する境界 ord 上界を、sequence/moving-center 形の補題として
閉じる(consult #13(Sol)の裁定: BORD-3 を独立 packet として先行)。
**証明様式([GCBORD3R1-02][03] で全面改稿)**: 極限 h を正規形へ変換する
reduction(R1 版 — h(ζ) = 0 のとき rescale が h を殺す欠陥)は**撤回**し、
**列の各項に対する compact chart 上の定量的不等式(moving-center head floor)
を張り、対偶で閉じる**。これにより (i) 極限の Fock 所属・limit span 所属は
一切不要(compact-open 収束と Cauchy 積分による jet 収束のみ)、(ii) 係数
退化(support-drop・λ_n の射影的発散との組合せ — R1 反例
f_n = e^p − e^{p+s_nq} + s_ne^{q₀})は **単位 ℱ-球面正規化**で自動的に
処理される([GCBORD3R2-03] で frame 係数正規化から変更)。

**(B3-1) statement(sequence/moving-center 形 — [GCBORD3R1-05] で型を自己
完結に)**: K は §8.9 (2c) のパラメタ空間そのもの(‖c‖₂ = 1 の raw 係数球面
× class データ (B_j, A_j) の閉 chart 箱 × 定数 gauge(§8.6 規約)。
**Fock 入力条件 [GCBORD3R3-03]**: 閉 chart 箱は |A_j| ≤ 1 − δ_ℱ、
|B_j| ≤ R_ℱ(δ_ℱ > 0、R_ℱ は chart 定数 — FR 文書の compact class
K_{δ,R} と同じ束縛)を満たすとする。これにより各原子 e^{q_j} は ℱ に属し、
その ℱ-norm は箱上で両側有界 — **merge/
prune 前処理は課さない**: f_p = Σ c_j e^{q_j} は raw 公式として K 全体で定義
され、本 statement は K∖Z₀ の列を量化する)。Z₀ := {p ∈ K : f_p ≡ 0}。
z_c : K → 閉 chart 箱 ⊆ D̄(t₀, R_col) は §8.9 (iii) の型(≺-最小 class の
位相 B — 決定的・連続性は主張しない)。p_n ∈ K∖Z₀、λ_n ∈ ℂ*、
ζ_n := z_c(p_n) とし、
  λ_n f_{p_n} → h  (D̄(t₀, R_out) 上一様 = compact-open)、 h ≢ 0、
  ζ_n → ζ ∈ D̄(t₀, R_col)
とする。このとき **ord_ζ(h) ≤ 5**。
(収束は compact-open で**定義**する。「W̄₃ の元」という集合名は使わない。)

**(B3-2) step 0: exact-merge routing と pattern 分類([GCBORD3R2-01] で
lower-arity route を復元)**: raw K は exact merge(q_a = q_b)・係数零を含む
ので、まず部分列上で **exact 一致 pattern を固定**し、一致 class を合併
(f は不変 — 係数は和)。**合併係数が零になる面(c_a + c_b = 0 — 個々の
係数が非零でも起こる [GCBORD3R3-04])も部分列上で pattern として固定**し、
零係数 class を prune → 再度一致 pattern を確認、と**反復して安定化**させる
(class 数は単調減少するので反復は ≤ 2 回で停止)。安定表現の相異 class 数を
m ∈ {1, 2, 3} とする(この表現では対距離 > 0・係数非零が各 n で成立 —
以下の d/s 比・Newton frame が well-defined)。
- m = 1: f_n = c e^{q}、ord ≤ 0 — 自明。
- m = 2: 下の (B3-3)〜(B3-5) の 2 class 版(pattern は分離/collapse の 2 つ、
  極限 span は plain 2 class または span{e^p, L e^p}(L 非定数 deg ≤ 2 —
  (A″1) の 2 原子版)、span の任意中心 ord ≤ 2)。
- m = 3: 対距離 d_{ab}(n)、s(n) := max d_{ab}(n) > 0 を取り、部分列上で各
  d_{ab}、比 d_{ab}/s、s を収束させる。**三角不等式により o(s) の対は高々
  1 つ**(2 対が o(s) なら第 3 対も o(s) となり s = max と矛盾)。pattern:
  (P1) **1|1|1**(全対距離下界 > 0)/(P2) **2|1**(1 対のみ → 0、第 3 は
  下界 > 0)/(P3) **coarse 3・plain**(s → 0、全比に下界 > 0)/
  (P4) **coarse 3・nested 2+1**(s → 0、ちょうど 1 対が o(s))。
係数の相対退化・λ_n の射影的発散は分類に関与しない(以下の unit-sphere
論法が吸収)。

**(B3-3) Fock 正規化と RKHS 評価([GCBORD3R2-02][03] で座標 dilation を
全廃)**: R1–R2 版の w/x 再正規化は**撤回**(dilation の向きが逆で分離下界が
出ず、正しい向きでは raw jet に s⁵ 重みが残り raw frame 係数ノルムでは床が
張れない — R2 反例 ‖J⁵f_n(0)‖ ≍ s² 参照)。代わりに **FR 資産と同じ Fock
空間 ℱ のノルムで正規化する**(R2 反例では ‖f_n‖_ℱ ≍ s² で jets と同率 —
比は一様)。box パラメタでは各原子の ℱ-norm は両側有界で、
  **(i) RKHS 評価**: ℱ は再生核 Hilbert 空間 — 点評価・0..5 階微分汎関数は
  中心 ∈ D̄(t₀, R_out) の compact 範囲で一様有界。特に
  sup_{D̄(t₀,R_out)} |f| ≤ C_R ‖f‖_ℱ(C_R は box 定数)。
V_{p} := span{e^{q_j}} ⊆ ℱ(merge/prune 後の m 次元部分空間)。

**(B3-4a) 2 原子 confluent 補題([GCBORD3R3-02] — P2/m=2 の frame を
自前で閉じる: FR-S1″ (A″1) は root-normalized 資産なので raw scale には
引用だけで流用しない)**: 対 (q_a, q_b) が raw scale で合流(δq := q_b − q_a、
ν_n := (δB, δA/2) → 0、t_n := ‖ν_n‖₂ > 0)するとき、Newton frame
  {e^{q_a}, (e^{q_b} − e^{q_a})/t_n} = {e^{q_a}, e^{q_a}·L_{ν̂_n}∫₀¹
   exp(u t_n L_{ν̂_n}) du}
((A″1) と同じ積分表示 — ここでは raw 変数 z、L_{ν̂}(z) = ν̂₁z + ν̂₂z²)は
ν̂_n ∈ S³ の部分列収束 ν̂_n → ν̂* の下で **ℱ-strong に
{e^{q_a*}, L_{ν̂*}(z) e^{q_a*}} へ収束**する。証明: 被積分関数
exp(q_a + u t L_{ν̂}) は指数の二次係数が |A_a|/2 + u t|ν̂₂| ≤ (1 − δ_ℱ)/2 +
t_n → (1 − δ_ℱ)/2 < 1/2 なので(t_n 十分小で)一様に ℱ の compact 部分に
入り、パラメタ (u, t, ν̂, q_a) に ℱ-norm 連続 — 積分の連続性で結論。∎
極限 frame は独立(L_{ν̂*} ≠ 0 非定数 deg ≤ 2)。

**(B3-4) 単位 ℱ-球面上の moving-center jet floor([GCBORD3R2-03]、
[GCBORD3R3-01][02] で P3/P4 を (L-d) 引用に再構成)**: 主張 —
  **∃σ₀ > 0(pattern chart 定数): ∀n, ∀v ∈ V_{p_n}, ∀ζ' ∈ D̄(t₀,R_col):
  ‖J⁵_z v(ζ')‖ ≥ σ₀ ‖v‖_ℱ**(部分列の pattern を固定した上で)。
証明(背理法 + strong limit 分類): 反例列 v_n ∈ V_{p_n}(‖v_n‖_ℱ = 1)、
ζ'_n → ζ'、‖J⁵v_n(ζ'_n)‖ → 0 を取る。各 pattern で **ℱ-strong 収束する
正規直交(または一様可逆 Gram の)frame** と、その極限 span の任意中心 ord
上界を与える:
  (P1) frame = 分離原子(ℱ-連続)。極限 span = plain 3 class ⇒ **GC-1
    W_c(3)**(任意中心)⇒ ord ≤ 5。
  (P2) frame = (B3-4a) の 2 原子 Newton frame + 分離 singleton。極限 span =
    span{e^p, P e^p, e^q}(P = L_{ν̂*} 非定数 deg ≤ 2、r = q − p 非定数 —
    **P2 では singleton が raw 距離で分離**するので r ≢ const は真)⇒
    **static W′**(任意中心 — 平行移動で P, r の非定数性は不変)⇒ ord ≤ 4。
  (P3)(P4) coarse 3([GCBORD3R3-01] — W′ は適用不能: raw 極限で全 class が
    一致し r ≡ 0。代わりに **FR の raw-gauge (L-d) 分類を消費**): P3 は
    FR-S1′ の single-scale plain chart(比の下界 — 部分列極限で chart の
    compact 集合に入る)、P4 は FR-S1″ の 𝒦_{η,t₀} chart への包含を明示
    ([GCBORD3R4-03]): 「o(s) の対はちょうど 1 つ」なので singleton 側の
    root-normalized 分離 max(|Ā|^{1/2}, |B̄|) は部分列極限で下界 η > 0 を
    持ち((N0) 充足)、t₀ := min(1/4, η²/8) と固定すると pair の
    root-normalized scale は **0 < t_m ≤ C·(τ_m/s_m) → 0**([GCBORD3R5-01] —
    ≍ は純二次差分 δB = 0 で偽: t_m = ε²/2。上界だけで包含には十分)なので
    十分大きい n で t_m ≤ t₀ — よって列は 𝒦_{η,t₀} に入る。いずれも SVD frame v_{ℓ,m} が strong-continuous
    unitary section で raw gauge へ戻り(FR 文書 §8.4/§9.3–§9.5、A′-4 —
    accepted)、**raw ℱ-strong 極限 U_*^{-1}P_ℓ = Q_ℓΦ(ξ*)、deg Q_ℓ ≤ 5**
    を持つ。よって極限 span の非零元は(deg ≤ 5 多項式)× Φ(ξ*)(非零
    entire)であり、**任意中心で ord ≤ deg Q ≤ 5**(多項式因子の重複度)。
  (m = 2) (B3-4a) の frame ⇒ span{e^p, L e^p}(または分離 2 class)⇒
    非零元 (α + βL)e^p の任意中心 ord ≤ deg L ≤ 2。
**係数有界性の鎖([GCBORD3R4-02])**: 各 pattern の frame を w_{ℓ,n}
(ℱ-strong 収束、極限 w_{ℓ,*} は独立 — P1/P2/m=2 は W′ の Wronskian 非零・
分離性、P3/P4 は正規直交の strong 極限)とし、v_n = Σ_ℓ b_{ℓ,n} w_{ℓ,n} と
書く。Gram 行列 G_n := (⟨w_{ℓ,n}, w_{ℓ',n}⟩) は G_* := (⟨w_{ℓ,*}, w_{ℓ',*}⟩)
へ収束し、極限 frame の独立性から G_* > 0(P3/P4 では G_* = I)。
1 = ‖v_n‖² = b_n^* G_n b_n ≥ λ_min(G_n)‖b_n‖² と λ_min(G_n) → λ_min(G_*) > 0
から **b_n は有界** — 部分列で b_n → b_*、
v_n → v := Σb_{ℓ,*}w_{ℓ,*} ∈ ℱ strong、‖v‖² = b_*^*G_*b_* = lim b_n^*G_nb_n
= **1 ≠ 0**、v ∈ 極限 span。(P3/P4 の raw-gauge frame は **w_{ℓ,n} := U_n^{-1}v_{ℓ,n}**(v_{ℓ,n} =
gauged 空間の SVD frame、U_n = gauge unitary — w_{ℓ,n} は V_{p_n} を張る)で、
strong unitary section U_n → U_* により
**w_{ℓ,n} = U_n^{-1}v_{ℓ,n} → U_*^{-1}P_ℓ = Q_ℓΦ(ξ*)** — FR §8.4 の鎖
[GCBORD3R5-02]。)
**moving-center RKHS 連続性([GCBORD3R4-03])**: ℱ の k 階微分評価汎関数の
核 K^{(k)}_ζ は ζ に norm 連続(Fock 核の正則性)で、ζ ∈ D̄(t₀,R_col) の
compact 範囲上 norm 有界。よって
  |J^k v_n(ζ'_n) − J^k v(ζ')| ≤ ‖v_n − v‖_ℱ·‖K^{(k)}_{ζ'_n}‖ +
   ‖v‖_ℱ·‖K^{(k)}_{ζ'_n} − K^{(k)}_{ζ'}‖ → 0
— J⁵v(ζ') = lim J⁵v_n(ζ'_n) = 0 ⇒ ord_{ζ'}(v) ≥ 6 — 各行の上界 ≤ 5 と
矛盾。∎
(J⁵ の中心は D̄(t₀,R_col) の任意点で floor が張れる — z_c の値も含む。)

**(B3-5) 定量鎖と対偶([GCBORD3R1-02][03] — 極限は動かさない)**: (B3-3)(i)
と (B3-4) の合成(v = f_{p_n}、ζ' = ζ_n)で、部分列の pattern chart 上
  **‖J⁵_z f_{p_n}(ζ_n)‖ ≥ σ₀ ‖f_{p_n}‖_ℱ ≥ (σ₀/C_R)·sup_{D̄(t₀,R_out)}
  |f_{p_n}|**。
対偶: ord_ζ(h) ≥ 6 と仮定すると J⁵h(ζ) = 0。compact-open 収束は Cauchy 積分
により全階導関数の内部一様収束を与え、移動中心 ζ_n → ζ でも
‖J⁵_z (λ_n f_{p_n})(ζ_n)‖ = |λ_n|·‖J⁵_z f_{p_n}(ζ_n)‖ → ‖J⁵h(ζ)‖ = 0
([GCBORD3R3-05] — 以下すべて |λ_n|)。上の一様比較から
|λ_n| sup|f_{p_n}| → 0、すなわち h ≡ 0 — 矛盾。よって ord_ζ(h) ≤ 5。∎
(|λ_n|‖a‖ 型の有界性仮定は不要 — R2 で確認された対偶の論理。この鎖は各
pattern chart 上の **TN-3 型不等式そのもの**であり、GC-5-T1 は K の退化近傍を
これらの chart で覆う被覆論法を担う。)

**(B3-6) sharp 性**: 5 は sharp — F3′(正本: FR 文書 §7)の witness を
(B3-1) の形に移すと: p_n = F3′ の node 列(係数は ‖c‖₂ = 1 に正規化 —
定数倍は λ_n 側へ)、λ_n := (正規化係数での ‖h_β‖)⁻¹。**z_c との接続
([GCBORD3R4-01])**: F3′ の class 位相は β の 3 乗根配置なので
ζ_n = z_c(p_n) ∈ {βω^j}(≺-最小の 1 点)であり |ζ_n| = β → 0、すなわち
ζ = 0。極限は z⁵ 方向(正規化定数倍)で **ord_ζ(h) = ord_0(z⁵) = 5** —
(B3-1) の形のまま上界 5 が到達される。

**scope(非主張)**: c ≥ 4 の border ord 上界(GC-9 の confluent 昇格義務は
別)、有効定数(存在のみ)、TN-3 本体(GC-5-T1)、人間による査読は未実施。

### 8.11 GC-5-T1 TN-3(比較補題本体 — **accepted、R-TN3 R2 PASS、fixed SHA `906bd1a`**)

**目的**: §8.9 (2c) の比較補題 TN-3(§4 GC-5 受理条件の blocking downstream
obligation)を BORD-3(§8.10、accepted `87863cc`)の系として閉じる。
consult #13 の α′ 設計(curve selection + 弧 leading-term)は、BORD-3 の
(B3-2)–(B3-4) が**任意の列**に対して証明されたことで不要化された — 残るのは
列の対偶のみ。

**(T1-1) statement(§8.9 (2c) の TN-3 そのもの)**: K, Z₀, z_c は §8.9 (2c)
= §8.10 (B3-1) の型 — **§8.9 追記(chart 箱定数の指定)により両者の K は
同一**([R-TN3 R1-01] で接続を明示。Fock 入力条件は未固定だった箱定数の
指定であり、§8.9 の受理済み主張と矛盾しない)。
  **∃ c_TN > 0: ∀p ∈ K∖Z₀: ‖J⁵f_p(z_c(p))‖₂ ≥ c_TN · sup_{D̄(t₀,R_out)}
  |f_p|**。

**(T1-2) 証明**: 背理法 — 反例列 p_n ∈ K∖Z₀ を
R(p_n) := ‖J⁵f_{p_n}(z_c(p_n))‖ / sup_{D̄(t₀,R_out)}|f_{p_n}| → 0 と取る
(inf = 0 なら存在)。§8.10 step 0(反復 merge/prune の pattern 固定)と (B3-2) の分類で
部分列の pattern を固定する(m ∈ {1,2,3}、m = 3 は P1–P4 — 分類は係数・
正規化に依らず任意の K∖Z₀ 列に適用可能)。ζ_n := z_c(p_n) ∈ 閉箱 ⊆
D̄(t₀, R_col) は部分列で収束。すると (B3-4) の単位 ℱ-球面 jet floor
(moving center 込み — v = f_{p_n}/‖f_{p_n}‖_ℱ、ζ' = ζ_n)と (B3-3)(i) の
RKHS 評価により、その部分列上
  ‖J⁵f_{p_n}(ζ_n)‖ ≥ σ₀‖f_{p_n}‖_ℱ ≥ (σ₀/C_R)·sup_{D̄(t₀,R_out)}|f_{p_n}|
— すなわち R(p_n) ≥ σ₀/C_R > 0。R(p_n) → 0 と矛盾。∎
(「全ての部分列がさらに正の下界を持つ部分列を含む」ので liminf R > 0、
よって inf R =: c_TN > 0。c_TN の有効値は非主張(存在のみ)。)

**(T1-3) 消費関係**: (B3-4) の floor は pattern chart 定数 σ₀、RKHS 定数
C_R はいずれも §8.10 で確立済み。本節は新しい解析を含まない(系)。

**(T1-4) 帰結(TN-3 obligation の解消 — 受理後に §4/§8.9 の状態表面を
annotation で更新する予定。accepted 本文は不変)**: TN-3 の解消により
§8.9 (AD-2) の N_T < ∞ は無条件化し、(AD-4) の B.0 条件付き go は
feasibility go に昇格する。§9 TN3-RATIO 診断(plateau・c_TN > 0 整合)は
本補題と整合。

**scope(非主張)**: c_TN・N_T の有効値、c ≥ 4 版、GC-5 本体(FR4-S1)、
人間による査読は未実施。

### 8.12 GC-4A.3b PBK22-D10(collar 10 階上界と scale cap — **accepted、R-GC4A3B R2 PASS、fixed SHA `b75aa85`**)

**目的**: A.3a の zf_witness collar(§8.5 (ZF-3))上で、WE₉(A.4)が消費する
**u の 10 階導関数上界と正規化剰余の scale cap** を明示定数で閉じる(QR5 の
two-sided P4 と同配置の 2|2 版)。**依存は A.1(divisor_record)・A.2a(u の
分解・分枝)・A.3a(collar)・A.2b((N-0) λ)のみ** — A.2c/A.4 以降への循環
なし。log の分枝定数は使わない(u′ 経由で回避 — (D10-3))。

**(D10-1) collar 上の unit 両側 bound**: (ZF-1) より collar 上
z_i ∈ B** := [−25/8, 25/8] × i[−(π + 5/4), π + 5/4](B* + drift ≤ 1)。
- **D3/E branch(V_i = E(z_i)、E(z) = (e^z − 1)/z)**: B** 上 **|E| ∈
  [1/25, 48]**。証明: |z| ≤ 1/2 では |E − 1| ≤ Σ_{k≥1}(1/2)^k/(k+1)! ≤ 0.3
  ⇒ |E| ∈ [0.7, 1.3]。|z| ≥ 1/2 では |z| ≤ √((25/8)² + (π+5/4)²) ≤ 5.4 と
  |e^z| ≤ e^{25/8} ≤ 22.8 から上界 |E| ≤ 23.8/0.5 ≤ 48。下界は
  |e^z − 1| ≥ 0.22 の場合分け: (i) |Re z| ≥ 1/4 ⇒ |e^z − 1| ≥
  ||e^{Re z}| − 1| ≥ 1 − e^{−1/4} ≥ 0.22。(ii) |Re z| < 1/4(このとき
  |Im z| ≥ √(1/4 − 1/16) ≥ 0.43)で |Im z| ∈ [0.43, π − 0.43] ⇒
  |Im e^z| = e^{Re z}|sin Im z| ≥ e^{−1/4}·sin 0.43 ≥ 0.31。(iii) |Re z| < 1/4
  で |Im z| ∈ (π − 0.43, π + 5/4] ⇒ cos(Im z) ≤ −cos(5/4) ≤ −0.31 ⇒
  Re e^z ≤ −0.31e^{−1/4} ≤ −0.24 ⇒ |e^z − 1| ≥ 1.24(Im z < 0 は共役対称)。
  よって |E| ≥ 0.22/5.4 ≥ 1/25。∎
- **D1/D2 branch(V_i = 1 − e^{∓z_i}、collar 上 |Re z_i| ≥ 7/8 — (ZF-1))**:
  |e^{∓z}| = e^{∓Re z} ≤ e^{−7/8} = 0.41686…([GC4A3BR1-02] — 丸めは厳密値で)
  ⇒ **|V_i| ∈ [1 − e^{−7/8}, 1 + e^{−7/8}] ⊆ [0.58, 1.42]**。∎
- **log 微分の bound**: E′(z) = (e^z(z−1) + 1)/z² は B** 上 |E′| ≤ 600
  (|z| ≥ 1/2: ≤ (22.8·6.4 + 1)·4 ≤ 600、|z| < 1/2: 級数で ≤ 0.75)⇒
  **|E′/E| ≤ 600·25 = 1.5×10⁴**。D1/D2: |V′/V| = |e^{∓z}/(1 − e^{∓z})| ≤
  e^{−7/8}/(1 − e^{−7/8}) = 0.7148… ≤ 0.72([GC4A3BR1-02] — 0.42/0.58 =
  0.724 では出ないため厳密値で評価)。(数値診断: B** 格子 801² で実測 |E| ∈ [0.19, 7.0]、
  |E′/E| ≤ 0.9 — 主張は証明可能な安全側。診断であり証明の代替ではない。)

**(D10-2) reduced 多項式の bound**: zf_witness invariant (i)(実部距離
≥ ρ/13)と r_S ≤ ρ/26 により、collar 点 w と各 reduced 零点 ζ は
|w − ζ| ≥ |Re w − Re ζ| ≥ ρ/13 − ρ/26 = **ρ/26**。よって
  |(log(P̃₁/P̃₂))′(w)| ≤ Σ_{ζ ∈ zeros(P̃₁)∪zeros(P̃₂)} 1/|w − ζ| ≤ 4·26/ρ
  = **104/ρ**
(零点は計 ≤ 4 — (ZF 前提)。P̃ の値そのものの両側 bound は本 packet では
不要 — u′ 経由(D10-3)のため。)

**(D10-3) u′ の明示 bound と Cauchy 10 階([設計注] |u| の bound は log の
分枝・偏角定数を要するため使わない — u′ は分枝に依らない)**: A.2a の分解
  u′ = (log(P̃₁/P̃₂))′ + (V₁′/V₁ − V₂′/V₂)·(z の連鎖) + (r₁ − r₂)′
において、d/dt log V_i = (E′/E または V′/V)(z_i)·z_i′(t)、collar 上
|z_i′| ≤ Λ_{i,k} + 1((ZF-1) の drift 計算と |η̃_i″| ≤ 1/16、|y| ≤ r_S ≤ 1)。
(r₁ − r₂)′ は affine: (r₁ − r₂)′(w) = δa·w + δb、係数
(δa, δb) は cell record の r 係数から **exact 減算**で得る([GC4A3BR1-03] —
未定義入力の解消)。T_C := sup_{w ∈ collar(S, r_S)} |w|(zf_witness の S・r_S
から計算可能な検証値)として
  **M_r′ := |δa|·T_C + |δb|**(検証式付きの型 — 自由文でない)。
branch は **pair ごとに独立**([GC4A3BR1-04])なので、pair i の branch_i ∈
{D1, D2, D3} に応じ M_{logV,i}′ := 1.5×10⁴(D3)/ 0.72(D1/D2)。合成:
  **M₁ := 104/ρ + Σ_{i=1,2} M_{logV,i}′·(Λ_{i,k} + 1) + M_r′**
(旧式の 1.5×10⁴(Λ₁+Λ₂+2) は D3/D3 の worst case — per-branch 式が正)。
が collar(S, r_S) 上の |u′| の上界。t ∈ S に対し D̄(t, r_S) ⊆ collar なので
Cauchy 積分により
  **M₁₀ := sup_S |u^{(10)}| = sup_S |(u′)⁽⁹⁾| ≤ 9!·M₁·r_S^{−9}**。
v := u − T₂u は v⁽¹⁰⁾ = u⁽¹⁰⁾(T₂ は二次)なので同じ上界。∎

**(D10-4) scale cap と正規化剰余([GC4A3BR1-01] で λ の向きを訂正、
[GC4A3BR1-05] で適用域を契約化)**: A.2b は y = λ(t − t₀)・𝒥_n = v⁽ⁿ⁾/λⁿ と
定義する(λ は周波数次元 — 長さの逆)ので、正規化座標の単位球 |y| ≤ θ に
対応する t-半径は θ/λ。外挿半径を
  **ℓ_ext := min(r_S/2, 1/λ)**(λ = §8.6 (N-0) の global λ。**前提: (N-0)
  の merge/prune 後 r ≥ 2** — r ≤ 1 は低 arity/exact exit で本 packet の
  適用外(λ 未定義))
に cap する。**適用域の契約**: t₀ := center(S)(実数)、外挿点は **実軸上**
x ∈ ℝ、|x − t₀| ≤ θ·ℓ_ext(θ ∈ (0, 1])。ℓ_ext ≤ r_S/2 ≤ ρ/52 < |S|/2 =
ρ/26 なので **Taylor 線分 [t₀ − θℓ_ext, t₀ + θℓ_ext] ⊂ S** — M₁₀ =
sup_S|u⁽¹⁰⁾| の適用域と整合(複素外挿は非主張 — WE₉ が必要とすれば collar
全体の 10 階 bound は同じ Cauchy で r_S/2-collar 上に出るが、契約は実軸に
限定する)。9 次 Taylor 剰余:
  |R₉(x)| ≤ M₁₀·(θℓ_ext)¹⁰/10! ≤ (9!·M₁/r_S⁹)·(θ·r_S/2)¹⁰/10!
  = **(M₁·r_S/10240)·θ¹⁰ =: R̂(θ)**
— **θ¹⁰ 減衰の正規化剰余 bound**(WE₉ は θ を小さく取って JF₉ の jet 床に
勝たせる — その不等式自体は A.4 の義務)。ℓ_ext ≤ 1/λ の cap により外挿点の
正規化座標は |y| = λ|x − t₀| ≤ θ ≤ 1 — 𝒥_n との整合。∎

**(D10-5) 出力契約(型付き — fail-closed)**: A.4 が消費する interface:
  `d10_witness-v1 := (cell_id, zf_witness 参照,
   **branch_1, branch_2 ∈ {D1, D2, D3}(pair ごとに独立 — [GC4A3BR1-04])**,
   pair 別 unit 両側 bound((D10-1) の表値 × 2), (δa, δb)(r 係数の exact
   減算), T_C, M_r′ = |δa|T_C + |δb|, M₁(per-branch 式),
   M₁₀ ≤ 9!·M₁·r_S^{−9}, **ℓ_ext = min(r_S/2, 1/λ)**, t₀ = center(S),
   R̂(θ) = (M₁·r_S/10240)·θ¹⁰, 適用域 flag(実軸・線分 ⊂ S))`
— 欠落 = record 生成禁止。divisor_record・zf_witness と同じ cell 粒度。
**versioned 消費**: A.4(WE₉)の消費条件は d10_witness-v1 を指名して結合する
(A.4 起草時に消費契約を versioned で宣言 — 本 packet は供給側のみ)。

**scope(非主張)**: WE₉ の外挿不等式本体(A.4)、γ・kernel 指数(A.5/A.6/
GC-5)、u の値の bound(分枝定数 — A.5 bootstrap の義務と同配置)、人間に
よる査読は未実施。

### 8.13 GC-4A.4 PBK22-WE9(局所窓外挿 — **accepted、R-GC4A4 R2 PASS、fixed SHA `9f1a18d`**。非 blocking 注: (WE-3) の g = |1+H|/|H| は §8.3 正規定義 |1+H|/max(1,|H|) の上界表現 — 結論不変)

**目的**: 深平坦 (c-i)(§8.3 (F2²-3))で、JF₉ target(consult #9 受理形 —
「v ≡ 0(二次比枝)または max_{3≤n≤9−d₀}|v⁽ⁿ⁾(t₀)|/(κλⁿ) ≥ c_J」、床は
A.2b/A.2c、claim 域は GCRouteRecord-v4([R-GC4A5A0 R3-01] で v3 から置換 — §8.14))と d10_witness-v1(§8.12)を消費し、
**局所窓外挿の不等式群**を明示定数で閉じる。**純 consumer** — 新しい床・
collar 解析は含まない。分岐合成・γ 確定は A.5/A.6 の義務。

**(WE-0) 前提と記号**: cell(A.0/A.1)・(c-i)(σ := sup_{J_k}|1 + H| <
c₁ρ⁹、(a) 否により J_k 上 |H| ∈ [e^{−1}, e])・zf_witness(S、r_S)・
d10_witness-v1(t₀ = center(S)、ℓ_ext = min(r_S/2, 1/λ)、R̂(θ))・
GCRouteRecord-v4 全 verified([R-GC4A5A0 R3-01] で v3 から置換 — v4 = §8.14。A.2c の claim 域は v3 部分で不変)。A.2a より J_k 上
u = Log(−H) は principal で **|u| ≤ 2|1 + H| ≤ 2σ**。u = p + v(p = T₂u)。

**(WE-1) Chebyshev 係数補題(初等・自己完結)**: q を deg ≤ 9 の多項式、
sup_{[−1,1]}|q| ≤ M とする。q = Σ_{k≤9} c_k T_k(Chebyshev 展開 — 係数は
c_k = (2/π)∫₀^π q(cos φ)cos(kφ)dφ(k ≥ 1)、c₀ は 1/π)で |c_k| ≤ 2M。
T_k の単項係数の絶対値和は
  ‖T_k‖₁ = 1, 1, 3, 7, 17, 41, 99, 239, 577, 1393(k = 0..9、直接検算可能、
  Σ_{k≤9} ‖T_k‖₁ = 2378)
なので、q の単項係数 a_j は |a_j| ≤ 2M·2378 ≤ **C₉·M、C₉ := 4756**。
半径 r・**任意中心 c** の実区間 [c − r, c + r] へは y = (x − c)/r の置換で
**|a_n|·rⁿ ≤ C₉·sup_{|x−c|≤r}|q|**([GC4A4R1-02] — a_n は **(x − c)ⁿ 中心
Taylor 係数**。通常の単項係数ではない)。deg ≤ 2 版は
**C₂ := 2(1 + 1 + 3) = 10**。∎

**(WE-2) κ 上界(深平坦 ⇒ 定量的 near-QR — v ≢ 0 枝)**: JF₉ target の
v ≢ 0 枝で、ある n ∈ [3, 9 − d₀] が |v⁽ⁿ⁾(t₀)| ≥ c_J·κ·λⁿ。u の t₀ での
Taylor 係数は次数 3..9 で v のそれと一致(p = T₂u は次数 ≤ 2)。半径
r := θ·ℓ_ext(θ ∈ (0, 1]、Taylor 線分 ⊂ S — d10 の適用域契約)の実区間で
(WE-1) を T⁹u = u − R₉ に適用:
  (c_J κ λⁿ/n!)·rⁿ = |a_n|rⁿ ≤ C₉·sup_{ball}|T⁹u| ≤ C₉·(2σ + R̂(θ))。
λr ≤ λℓ_ext ≤ 1 より (λr)ⁿ/n! ≥ (λr)⁹/9!。整理して **∀θ ∈ (0, 1]:
  κ ≤ κ_WE(θ; σ) := 9!·C₉·(2σ + R̂(θ)) / (c_J·(λθℓ_ext)⁹)**
— 深平坦度 σ が κ(QR locus からの横断残差)を上から抑える = **配置は
定量的に二次比枝近傍**。θ の最適化・near-QR 合成は A.5/A.6 の義務(menu
規約 — (F2²-3) の c₁ ceiling と同配置)。∎

**(WE-3) 二次比枝の kernel 不等式(v ≡ 0 枝)**: u = p(deg ≤ 2)とする。
**分枝接続条件(A.5 供給 — 型付き消費)**: u = p が I_k 全体で有効
(bootstrap witness)。**展開中心は c_k := center(J_k)**([GC4A4R1-01] —
t₀ = center(S) は一般に center(J_k) でないため、WE-3 は t₀ を使わない。
p は大域二次式なので任意中心の Taylor 展開が exact)。J_k = [c_k − ρ/2,
c_k + ρ/2] 上 |p| ≤ 2σ に (WE-1) の C₂ 版(中心 c_k・半径 ρ/2):
|b_j|(ρ/2)^j ≤ 10·2σ = 20σ(b_j は (x − c_k)ʲ 中心係数、j = 0, 1, 2)。
I_k 上 |x − c_k| ≤ 1 なので
  sup_{I_k}|p| ≤ Σ_j 20σ·(2/ρ)^j ≤ 140σρ⁻²(ρ ≤ 1)。
(c-i) では σ < c₁ρ⁹ ≤ 10⁻²ρ⁹ なので sup_{I_k}|p| ≤ 1.4ρ⁷ ≤ 1.4、
|1 − e^p| ≤ |p|e^{|p|} ≤ 4.1·140σρ⁻²、|H| = e^{Re p} ≥ e^{−1.4} ⇒
  g = |1 + H|/|H| ≤ e^{1.4}·574σρ⁻² ≤ 2400σρ⁻²(I_k 上)。
‖g‖_{J_k} ≥ σ/e((c-i) の argmax 点 — (F2²-3) と同計算)と合わせ
  **‖g‖_{I_k} ≤ 2400σρ⁻² ≤ 2400e·ρ⁻²·‖g‖_{J_k} ≤ 6600·ρ⁻²·‖g‖_{J_k}**
— 二次比枝の kernel 指数は **2**(ρ⁻⁹ 予算に対し余裕)。∎

**(WE-4) 出力契約(型付き — fail-closed)**: A.5/A.6 が消費する interface:
  `we9_witness-v1 := (cell_id, d10_witness-v1 参照, GCRouteRecord-v4 参照([R-GC4A5A0 R3-01] で v3 から置換),
   **d₀ = ord_{t₀}D(divisor_record 参照 — (ZF-3) の規約どおり S 中心 t₀ で
   exact に読み直した値。gcd transition 後は current rank の record を指名)**
   ([GC4A4R1-03]),
   branch flag(v ≡ 0 / v ≢ 0 — JF₉ target の二分岐),
   v ≢ 0 ⇒ κ_WE(θ; σ) の式(θ は自由パラメタ — A.5/A.6 の menu),
   v ≡ 0 ⇒ kernel 定数 6600ρ⁻²(分枝接続 witness を A.5 から要求 —
   欠落時は record 生成禁止))`
— divisor_record・zf_witness・d10_witness と同じ cell 粒度。

**scope(非主張)**: near-QR(κ ≤ κ_WE)からの kernel 合成・θ menu・
γ 確定(A.5/A.6)、分枝接続(A.5)、床 c_J の供給(A.2b/A.2c — 消費のみ)、
人間による査読は未実施。

**§8.13 追記(2026-08-19、[R-GC4A5A0 R2-01][R3-01])**: WE-0/WE-4 の record
参照は **GCRouteRecord-v4**(§8.14 — v3 不変 + JF₉ 分岐 flag + flag = v≡0 の
とき qr_global_witness required)へ**本文置換済み**(R2 の宣言のみの追記では
consumer 型が閉じないという R3 指摘に従い、reviewer 明示指示による accepted
本文中の参照 2 箇所の置換を実施 — inline marker と版履歴 v0.28.9 に監査痕跡。
数学的内容は不変: v4 は v3 の versioned 拡張で、WE-2(v ≢ 0 枝)の消費内容は
不変、WE-3(v ≡ 0 枝)は v4 の qr_global_witness を分枝接続条件として消費)。

### 8.14 GC-4A.5a0 PBK22-QRG(exact QR の大域化 — **accepted、R-GC4A5A0 R4 PASS、fixed SHA `68d114a`**)

**目的**: JF₉ target の **v ≡ 0 枝**(二次比枝)を大域化し、WE-3(§8.13)の
分枝接続条件を**無条件で**供給する(consult #14 の A.5 再分解 — 最軽量の
base face を先に閉じる)。

**(QRG-1) 恒等定理による大域化([GC4A5A0R1-01] — 成立域は実区間)**:
A.2a が supplies するのは**実区間 W 上**の v := u − T₂u ≡ 0(JF₉ target の
第一枝 — 複素 collar 上の主張は仮定しない)。p := T₂u(二次)とおくと
W 上 u = p、すなわち −H = e^p、すなわち
  **Φ_p := B₁ + e^p B₂ = 0 が実区間 W の各点で成立**。
B₁、B₂、e^p はいずれも entire(B_i = 有限指数和 × 多項式構造 — A.0/A.1 の
cell データ、p は二次多項式)なので Φ_p も entire。W は非退化実区間 =
**集積点を持つ零集合** ⟹ 恒等定理により **Φ_p ≡ 0 on ℂ**。∎

**(QRG-2) 帰結(大域二次比 witness)**: B₁ = −e^p B₂ が ℂ 上成立。
- **H = −e^p として大域延長**: B₂ の零点では B₁ も同時に零(恒等式)なので
  H = B₁/B₂ の特異点は除去可能 — **I_k 上 H は解析的で pole なし**、
  1 + H = 1 − e^p(**Log・分枝は一切不要** — WE-3 の「u = p が I_k 全体で
  有効」より強い形で分枝接続条件が充足)。
- **g の評価は WE-3 がそのまま適用可能**: sup_{J_k}|1 − e^p| = σ から
  C₂-Markov(中心 c_k = center(J_k))で ‖g‖_{I_k} ≤ 6600ρ⁻²‖g‖_{J_k} —
  **(c-i) の v ≡ 0 枝の kernel はこれで閉鎖**(chain・conditioning 不要 —
  consult #14「chain より先に閉じられる」)。

**(QRG-3) 出力契約(型付き — versioned schema、[GC4A5A0R1-02][03])**:
  `qr_global_witness := (cell_id,
   α 参照: **q_band_witness-v3 の (α₀, α₁, α₂) と同一オブジェクト参照**
   (raw 係数は p_k = α_k·λᵏ の導出値 — λ = §8.6 (N-0)。独立に値を持たない
   ので一致検証は参照同一性で閉じる),
   恒等式 ref: Φ_p ≡ 0((QRG-1) — §7.1 の identity ref 規約),
   **source 一致 field**: W 上 u = p の検証値(v ≡ 0 判定の source =
   JF₉ target 第一枝 + T₂u = p の定義的一致),
   **I_k 接続 field**: 1 + H = 1 − e^p が I_k 上恒等((QRG-2) の導出 ref —
   WE-3 の要求『u = p が I_k 全体で有効』を **Log/branch 不要の強い形**で
   充足する: WE-3 の証明が使うのは |1 − e^p| と |H| = e^{Re p} のみ))`
**schema 拡張**: `GCRouteRecord-v4 := GCRouteRecord-v3(不変)+
(JF₉ 分岐 flag; flag = v≡0 のとき qr_global_witness を **required field**)`
— v3 は in-place 変更しない(versioned 拡張規約)。v4 で flag = v≡0 かつ
qr_global_witness 欠落 = **record 生成禁止(closed-world fail-closed)**。
WE-3 の消費は v4 record を指名する。cell 粒度。

**scope(非主張)**: v ≢ 0 枝(A.5a COND9)、chain・ledger(A.5c)、
restart(A.5b)、人間による査読は未実施。

### 8.15 GC-4A.5a PBK22-COND9(projective one-hop conditioning — **定理 draft 撤回**(R-GC4A5A R1 blocking 7 + consult #15)。(C9-1)(C9-2) の初等評価のみ存置、(C9-3)〜(C9-5) は**失敗した候補経路の記録**(効力なし)。再設計 = PTN-SPEC + BORD-22/PTN-22 — 下記追記)

**目的**: consult #14 の主エンジン — **一 hop の projective conditioning**
  **(C9) ‖g‖_W ≤ B_C·(L_C/s)⁹·‖g‖_S**
(g := |1 + H|/max(1, |H|)、H = reduced ratio(§8.3 (F2²-4) — P̃₁, P̃₂ 互いに
素)、S = [t_c − s/2, t_c + s/2] ⊂ W(長さ L_C ≤ 1、W ⊂ cell 窓)、B_C は
chart 定数、s ∈ (0, L_C/2])を確立する。A.5c(CHAIN)がこれを反復消費する。
係数への線形性より **σ-方向の一様性は自動**(g は config の scalar 倍で
不変)— 危険は指数側のみ(§9 COND9-PROBE: slope ≈ 1 ≪ 9、反証材料)。

**(C9-1) g の三分法(初等)**: 任意の t で
  |H(t)| ≥ 2 ⇒ g(t) ≥ 1 − 1/|H| ≥ 1/2、
  |H(t)| ≤ 1/2 ⇒ g(t) = |1 + H| ≥ 1/2、
  |H(t)| ∈ (1/2, 2) ⇒ g(t) = |1 + H|/max(1, |H|) ∈ [|1+H|/2, |1+H|]。
よって **g < 1/2 の点では |H| ∈ (1/2, 2) かつ g ≍ |1 + H|(factor 2)**。
また常に g ≤ 2。H の pole(P̃₂ 零点)・零点(P̃₁ 零点)では g = 1 —
g は (t, config) の**連続関数**(reduced H は meromorphic、g は H = 0, ∞ を
通して連続延長 — 互いに素 + (ZF-1) の V 非零により分母消滅は H = ∞ のみ)。

**(C9-2) 自明 case**: sup_S g ≥ 1/2 なら ‖g‖_W ≤ 2 ≤ 4·‖g‖_S ≤
B_C(L_C/s)⁹‖g‖_S(B_C ≥ 4)✓。以下 sup_S g < 1/2 とする — S 上
|H| ∈ (1/2, 2)、g ≍ |1 + H|、u = Log(−H) が S 上 principal で |u| ≤ 2·sup_S g
(A.2a と同計算)。

**(C9-3) 列コンパクト性の骨格(BORD-3/TN-3 と同型)**: (C9) の否定 —
配置列 θ_n(compact chart 箱、‖·‖ 正規化)、scale s_n、比
Q_n := ‖g_n‖_S/((s_n/L_C)⁹‖g_n‖_W) → 0 — を取り、部分列で θ_n → θ*、
s_n → s* ∈ [0, L_C/2] とする。
- **(C9-3a) 固定 scale(s* > 0)**: (t, θ) ↦ g は compact 上一様連続なので
  g_n → g_* 一様。Q_n → 0 と ‖g_n‖_W ≤ 2 から ‖g_*‖_{S*} = 0、すなわち
  S* 上 1 + H_* ≡ 0。H_* は meromorphic なので**恒等定理により W 全体で
  H_* ≡ −1**、よって g_* ≡ 0 on W。このとき ‖g_n‖_W → 0 なので比の分母も
  退化 — 正規化列 ĝ_n := g_n/‖g_n‖_W を **(C9-4) の blow-up** で処理する
  (H_* ≡ −1 の locus = p ≡ 0 ∧ v ≡ 0 の完全平坦面)。‖g_*‖_W > 0 の場合は
  Q_n → Q_* = ‖g_*‖_{S*}/((s*/L)⁹‖g_*‖_W) > 0(分子 > 0 — 前段)で矛盾 ✓。
- **(C9-3b) 縮小 scale(s* = 0)**: (C9-4) の jets 床が (s_n/L)⁹ の指数を
  ちょうど供給する — 以下。
**(C9-4) blow-up と ord ≤ 9 床(strata 被覆 — 全て accepted 資産の消費)**:
(C9-2) 後の flat 域では g ≍ |1 + H| = |F|/|B₂-reduced 相当|(F := 数え上げ
前の分子 — 1 + H は S 近傍で解析的、|H| ∈ (1/2, 2) により分母は
max(|B₁|, |B₂|) と factor 3 で同値)。1 + H = 1 − e^{p + v}(A.2a 分解)で、
両窓比較は **(p, v) の二成分**に分解される:
  - **p 成分(deg ≤ 2)**: C₂-Markov(§8.13 (WE-1)、中心 t_c・半径 s/2)で
    |p 係数|(s/2)^k ≤ 20·sup_S|u| ⇒ sup_W|p| ≤ C_p·(L_C/s)²·sup_S|u|。
  - **v 成分**: JF₉ target の二分岐(GCRouteRecord-v4):
    (i) **v ≡ 0**: A.5a0 の大域恒等式 — v 寄与なし。
    (ii) **v ≢ 0**: S 中心の jets 3..9−d₀ は上に C₉-Markov(≤ C₉(2 sup_S|u|
    + R̂)/rⁿ)、下に A.2c 床(max ≥ c_Jκλⁿ)で挟まれ、v の W 上の値は
    **有限次元極限族の norm 比較**で評価する: 正規化列 v̂_n :=
    v_n/‖v_n‖_{C⁰(W)} の極限は、A.2b atlas の chart 極限族(plain 4 class /
    confluent / Z/G / QR-collapse)に属し、その **S-消滅次数は ≤ 9**:
      plain 4 class = GC-1 W_c(4)(ord ≤ 9、任意中心)/
      2 指数 confluent = §8.7 W_CONFL(2,2)(≤ 6)・混合消去(≤ 8)/
      1 指数 collapse = Π₄(≤ 4)/ Z/G = §8.8 ZG-NF の床 /
      exact QR face = (i) へ retract(A.5a0)。
    S-消滅次数 ≤ 9 の非零極限は sup_S ≥ c·(s/L)⁹·sup_W を満たす(deg ≤ 9
    Taylor 主部 + Markov — §8.13 (WE-1) の逆向き適用、剰余は d10 の R̂ 型)
    ⇒ 極限族の一様定数 c_* > 0(compact 上の下半連続 inf — TN-3 の
    (B3-4)→(T1-2) と同じ論理)⇒ 十分大きい n で
    **sup_S|v_n| ≥ (c_*/2)(s_n/L)⁹ sup_W|v_n|**。
  - **合成**: sup_W|u| ≤ sup_W|p| + sup_W|v| ≤ C_p(L/s)²·sup_S|u| +
    (2/c_*)(L/s)⁹·sup_S|v| ≤ B′·(L/s)⁹·sup_S|u|(sup_S|v| ≤ sup_S|u| +
    sup_S|p| ≤ (1 + 2C₂·10)sup_S|u| — S 上の p 係数評価から)。
  - **u → g の変換**: flat 域では g ≍ |1 − e^u| ≍ |u|(|u| ≤ 1/2 圏 —
    W 上 |u| が 1/2 を超える場合はその点で g ≥ c₀(初等下界)となり
    (C9-2) 型の自明化で吸収)。∎(骨格 — chart 別定数の勘定は (C9-5))
**(C9-5) chart 別定数と fail-closed**: (C9-4)(ii) の極限族所属・床消費は
GCRouteRecord-v4 の verified witness 群(q_band_witness-v3・zf・d10・
qr_global(分岐時))を要求する — 欠落 = record 生成禁止。B_C は
  B_C := max(4, B′·(u→g 変換定数)²)
の chart 定数(有効値は非主張 — 存在のみ)。出力契約:
  `cond9_witness := (cell_id, we9_witness-v1 参照, hop 幾何(t_c, s, W),
   B_C ref, (C9-2)/(C9-4) の分岐 flag)` — cell 粒度、A.5c が反復消費。

**scope(非主張)**: B_C の有効値、hop の反復・ledger(A.5c)、restart
(A.5b)、c ≥ 4 一般(GC-5)、人間による査読は未実施。

**§8.15 追記(2026-08-19 — 定理 draft の撤回と再設計、consult #15)**:
R-GC4A5A R1(blocking 7)により (C9-3)〜(C9-5) の証明経路は**成立しない**
(gcd 遷移で reduced g の config 連続性が偽 — 反例 B₁ = t, B₂ = t + ε の
inner bubble [ξ : ξ+1]/ metadata compactness の流用 / Taylor 剰余の W-norm
流用 = consult #14 の棄却した罠の移転 / W 上 branch 未定義)。consult #15
(Sol)の裁定:
- **必要資産は plain TN-4 でなく PTN-22**(分母込み projective/weighted
  Remez 比較 — ‖(B₁+B₂)/max(|B₁|,|B₂|)‖ の二窓比較)。
- **full FR4 の前倒しは不要** — T3 = 2|2 専用の **BORD-22**(2|2 限定
  border 分類: exact merge/support drop・child confluence・二層 blow-up・
  係数退化・QR transverse blow-up・gcd inner bubble・projective 分母)を
  最小 packet として先行し、その系として PTN-22。T3 閉包が他 topology を
  要求した時点でのみ full BORD-4/TN-4 へ昇格。
- **gcd 遷移は raw projective pair (B₁, B₂) で扱う**(gcd を取らない —
  共通零点は最初の非零 jet pair [a_k : b_k] の projective 値 + outer/inner
  chart 被覆。reduced g の大域連続関数化は放棄)。
- **COND9 は「PTN-22 を入力とすれば従う」reduction/interface packet まで
  しか受理対象にならない** — BORD-22/PTN-22 は A.5a の **blocking
  obligation**(GC-5 側に置いても A.5 は受理まで open のまま — 「送り」で
  resolved 化しない)。
- リスク: 現 C9-3〜5 経路 = 赤(死)/ COND9 定理自体 = 黄〜橙(反例なし)/
  PTN-22 = 橙。見積り: 2|2 限定で 3–4 proof packet・6–12 round、full FR4 は
  8–10 packet・20+ round。
- **no-go 判定基準の明文化**: exponent > 9 の bubble、または exponent 9 でも
  定数が 0 へ落ちる列が出れば PBK22 の明確な no-go 信号。

### 8.16 GC-4A.5a1 PBK22-PTN-SPEC(BORD-22/PTN-22 interface — **accepted、R-GC4A5A1 R4 PASS、fixed SHA `5d7400a`**)

**目的**: consult #15 の再設計に基づき、A.5a の blocking obligation である
BORD-22(GC-5-T2)/ PTN-22(GC-5-T3)の **interface 型を proof claim なしで
固定**する。両 packet と COND9 reduction(A.5a 本体)はこの型のみを消費する。
本 packet は**いかなる不等式・分類の成立も主張しない** — 型・witness 契約・
statement 登録のみ。

**(PS-1) 対象 pair(raw projective 処理 — gcd 大域連続化の放棄)
[R-GC4A5A1 R1-01]**: 型は **2 層**とする — 一次対象は cell 局所の raw
analytic pair **𝐁 := (B₁, B₂)**(§8.3 (F2²-1) の記号のまま —
B_i = P_iV_ie^{r_i}、**未約分**)、二次対象は divisor_record(§8.3 (F2²-4))
経由の reduced pair **𝐁̃ := (P̃₁V₁e^{r₁}, P̃₂V₂e^{r₂})**(P̃₁, P̃₂ 互いに素)。
weighted ratio g := |B₁ + B₂|/max(|B₁|, |B₂|)((F2²-2) と同一)は**共通
scalar gauge 不変**(𝐁 → (cΨB₁, cΨB₂)、c ∈ ℂ*、Ψ 非零解析)であり、
(F2²-4) の exact 相殺により **g(𝐁) = g(𝐁̃)**。(PTN-22) の比較対象は g
(gauge 不変量)、BORD-22 の正規化・分類対象は **𝐁̃ の common gauge
quotient**。reduced ratio H = B̃₁/B̃₂ を **config 大域の連続関数として扱わ
ない**(R-GC4A5A R1 反例: B₁ = t, B₂ = t + ε の inner bubble [ξ : ξ+1])。

**(PS-2) stratum record(divisor/gcd 層別の witness 化)**:
  `stratum_record := (cell_id, divisor_record 参照(§8.3 (F2²-4)),
   d₀ := ord_{t₀}D(divisor_record から exact — **未約分 pair 𝐁 の共通因子
   D の消滅次数**。A.2a の予算 N = 9 − d₀・A.3a (ZF-3) の読み直しと
   **同一オブジェクト** [R-GC4A5A1 R1-01]),
   𝐁̃ の近接共通零点ごとの消滅次数対 (ord B̃₁, ord B̃₂)(退化列で発生する
   **reduced pair の共通零点 — D の零点とは別物**),
   gcd-jump provenance(外側 config との次数差))`
— fail-closed: field 欠落 = record 生成禁止(R-GC4A5A R1 finding 6 の d₀
interface 不一致の解消枠)。

**(PS-3) t3 witness(2|2 topology の型)[R-GC4A5A1 R1-03]**:
  `t3_witness := (cell_id, SPLIT4 分割 witness(GC-2 — 4 原子の 2|2 pairing),
   **D-PBK-22 record 参照**(GC-3 §7.3 の required keys 完全列挙 —
   **active_children_nonzero**(消費条件: 両 child C_i ≢ 0 — 不成立なら
   zero-pruning 継承で redispatch、t3_witness 生成禁止 [R-GC4A5A1 R2-01])、
   certificate_ref(C₁)/certificate_ref(C₂)(w=2 variant)、
   nonconstant(q_{C₁} − q_{C₂})、collision-scale witness、η_dw witness、
   補題 G window witness — を **identity ref で消費**。自由 flag での代替
   禁止), pairing margin(GC-4C.0 dispatch 表参照))`
— BORD-22 の分類対象は**この witness が指す 2|2 限定族のみ**(他 topology =
scope 外。T3 閉包が他 topology を要求した時点で full BORD-4/TN-4 へ昇格 —
consult #15)。

**(PS-4) window contract(窓幾何の同一性 + zf 条件 — 型必須)
[R-GC4A5A1 R1-02]**:
  `window_contract := (W(cell 窓、|W| = L_C ≤ 1), S = [t_c − s/2, t_c + s/2]
   ⊂ W, s ∈ (0, L_C/2],
   zf_scope := (zf_witness 参照(A.3a (ZF-3) — 保証域は **S と
   collar(S, r_S) のみ**), **W_zf 被覆 witness**(W ∖ collar(S, r_S) 上の
   reduced 零点・V 零点の排除、または当該零点近傍の (PS-5) chart への
   routing 済み証明 — **A.3a は供給しない**。供給は BORD-22/A.5b の証明
   義務であり本 packet は型のみ)),
   we9 同一性: we9_witness-v1 参照(§8.13)+ d10_witness-v1 参照(§8.12)
   — source 窓 S の**同一オブジェクト参照**、関係 flag ∈ {identical,
   contained, disjoint-forbidden},
   λ(A.2b chart scale、y = λ(t − t₀)— 同一オブジェクト参照)と
   ℓ_ext = min(r_S/2, 1/λ)(§8.12 — 同一オブジェクト参照)の整合 field)`
— **zf/stratum 条件は省略不能**(設計根拠: R-GC4A5A R1 finding 5・
consult #15。数値裏付けは §9 BORD22-PROBE — **診断ポインタ、結果の正本は
§9**であり本節は再記述しない [R-GC4A5A1 R1-06])。W_zf 被覆 field の欠落 =
witness 不成立(fail-closed)。物理 scale s と chart scale λ の換算は record
内で完結させる(暗黙換算の禁止 — R-GC4A5A R1 finding 6)。

**(PS-5) projective common-zero 拡張**: 𝐁 の共通零点 t₀(P̃ 互いに素でも
V/e^r 込み pair の近接零は退化列で発生し得る)では
k := min(ord_{t₀}B₁, ord_{t₀}B₂)、projective 値 = 最初の非零 jet 対
[a_k : b_k]。被覆は **outer chart(|t − t₀| ≥ δ)+ inner chart
(t − t₀ = δξ、ξ compact)の 2 枚** — chart 間で連続極限の一致は**要求
しない**。要求は「任意の退化列が有限枚の outer/inner chart のどれかに入る」
(被覆完備性 — BORD-22 の証明義務)。

**(PS-6) exact QR exit**: JF₉ 分岐 flag(GCRouteRecord-v4)= v ≡ 0 の場合、
二窓比較に入る前に A.5a0 QRG(§8.14)へ retract — qr_global_witness 必須
(fail-closed)。PTN-22 の対象は v ≢ 0 枝のみ — **この排他は (PS-9) の
discriminated union が型強制する** [R-GC4A5A1 R1-04]。

**(PS-7) (PTN-22) statement の登録(証明なし)**:
  **(PTN-22) ‖g‖_W ≤ C₂₂ · (L_C/s)⁹ · ‖g‖_S**
(g は (PS-1)、窓と条件は (PS-4)、C₂₂ は chart 定数 — 有効値非主張・存在
のみ、指数 9 = D_W(4) 予算)。**本 packet はこの不等式を主張しない** — 型の
固定と statement の登録のみ。証明は BORD-22(先行)の系として行う
(consult #15 の順序)。

**(PS-8) BORD-22 coverage checklist(分類義務の正本化 — 証明なし)**:
BORD-22 は少なくとも次を chart 被覆に含む: ① exact merge/support drop
② child pair の confluence(片側・両側)③ root scale/child scale の二層
blow-up ④ 係数退化 ⑤ exact QR locus への transverse blow-up ⑥ gcd inner
bubble((PS-5))⑦ projective 分母の一様処理。§8.15 追記(consult #15)の
checklist を本 (PS-8) が正本化する。

**(PS-9) 出力契約(discriminated union)[R-GC4A5A1 R1-04][R1-05]
[R2-02][R3-01]**:
  `ptn22_witness-v1 := valid | nogo`(ちょうど一方 — closed-world)。
  **相互排他は branch constructor で型表現する**: valid の scan field は
  checked_clear constructor 専用、nogo の scan field は detected constructor
  専用 — detected を持つ record を valid として構成することは**型上不可能**
(prose 制約でなく constructor 分離 [R-GC4A5A1 R3-01]):
  - `valid := (cell_id, stratum_record, t3_witness, window_contract,
     JF₉ 分岐 flag = **v ≢ 0 必須**(GCRouteRecord-v4 参照 — v ≡ 0 では
     valid の生成を**禁止**し、(PS-6) の retract 先 qr_global_witness
     (§8.14)の ref を消費側が代わりに要求する), C₂₂ ref,
     scan = **checked_clear(evidence ref)**(no-go 検査済み・検出なしの
     evidence — この constructor 以外は型に存在しない。未検査 = scan field
     を構成できない = valid 生成禁止))`
  - `nogo := (cell_id, scan = **detected(evidence ref)**(この constructor
     以外は型に存在しない — evidence = exponent > 9 bubble の族 witness /
     定数 → 0 列の witness(§8.15 追記の判定基準と同一物)))`
  **消費規則**: COND9 reduction(A.5a)・A.5c が消費できるのは **valid
  のみ** — nogo の証明経路での消費は禁止し、§4 の go/no-go 判定へ送付する。
  fail-closed: 未検証 field の欠落 = witness 不成立。

**scope(非主張)**: (PTN-22) の証明、BORD-22 の分類・floor・被覆完備性の
証明、C₂₂ の有効値、COND9 reduction 本体、A.5b/A.5c/A.6、人間による査読は
未実施。

**§8.16 追記(2026-08-22 — BORD-22 骨格、consult #16)**: Sol 裁定
(`sol-bord22-consult.md`)の設計記録:
- **二段正規化**: 単一 λ_n 𝐁̃_n では QR 極限 (H, −H) で分子が消えるため不十分。
  gauge section U_n(FR と同じ strong-continuous unitary — PS-1 の一般解析
  gauge は g には無害だが Fock 等長性を与えない)を先に固定し、
  **carrier 𝐂_n := ρ_n⁻¹U_n𝐁̃_n**(ρ_n = ‖·‖_⊕ = Hilbert 直和 norm — 成分別
  正規化は相対振幅を壊すため不採用)と **defect f_n := δ_n⁻¹(C₁,n + C₂,n)**
  の二段 frame に分ける。
- **分母処理は chart atlas の一軸**(付録でない): W_zf 上の carrier 床
  m_C ≤ max(|C₁|, |C₂|) ≤ M_C が projective 版で新たに必要な床。片側
  ℱ-strong 零 → outer chart [1:0]/[0:1](g → 1、生存成分の零点近傍のみ
  inner へ)/ 両側関数零 = frame compactness の失敗(起きない事が証明義務)
  / 一点共倒れ = common-zero bubble(最初の非零 jet pair + inner chart)。
- **step 0**: within-child は BORD-3 と同じ merge/prune 反復。**cross-child
  は合算禁止** — exact exponent 一致は matching(0/1/2 本)として記録し、
  matched 項の係数相殺(全相殺 = exact QR / 部分相殺 = lower-support face)
  のみ扱う。child 恒等零 = active_children_nonzero 失敗 → redispatch。
- **rate atlas**: root scale s₀ + child scales s₁, s₂ の比を再帰 blow-up して
  有限列挙(個別関数形 s^α, e^{−1/s} の列挙はしない)。真正 crux = root も
  合流する場合の iterated divided-difference/SVD frame(span{Q_ℓ e^q},
  deg Q_ℓ ≤ 9)。A.2b の 21 chart は metadata/jet-floor atlas であり
  Fock-strong frame・carrier 床は未供給 — 流用不可。
- **床の主張形**: moving-center 二段 statement。projective order
  ν_ζ = ord_ζ(F) − min(ord_ζC₁, ord_ζC₂) **≤ 9(予算)** — D_W*(4) = 8 は
  診断仮説のまま(sharp 化を critical path に入れない)。
- **W_zf の帰属分割**: BORD-22(T2a)= 静的有限被覆の証明
  (T2a R4 で「W ∖ Σ の被覆 + 移管領域 Σ の帰属排反」に精密化
  [R-T2A-R5-01] — Σ = 境界 margin、被覆は受け手 cell の義務)/
  A.5b = chain 上の選択の witness 化(被覆の再証明はしない)。A.3a の W 全域単純拡張は不採用
  (§9 BORD22-PROBE の無条件反例が否定)。
- **packet 分割**: T2a ATLAS(被覆完備性のみ)→ T2b FRAME → T2c FLOOR →
  T3 PTN-22 の 4 packet(consult #15 の見積から 1 本増)。最初の着工 =
  **T2a、受理条件は被覆完備性の一主張のみ**。
- **no-go 監視点**: 最危険 = **carrier 床 m_C の消失**(指数自体より)。
  次点 = QR transverse × common-zero bubble の同時退化(合成交差での
  defect Gram 潰れ)。追加 fixture 5 種(QR×BUBBLE / DOUBLE-BUBBLE /
  CARRIER-SWITCH / TWO-LEVEL-SVD / PROJECTIVE-FLOOR)— weighted ratio の
  横ばいだけでは床の定数崩壊を見逃すため、床そのものの傾きを測る。

### 8.17 GC-5-T2a BORD22-ATLAS(T3 = 2|2 有限 chart coverage — **accepted、R-T2A R9 PASS、fixed SHA `08c2d0e`**)

**目的**: BORD-22 の第一 packet(consult #16 の 4 分割)。主張は一つ:

**(AT) 被覆完備性**: 任意の admissible T3 列 {θ_n}(各 θ_n は §8.16 の
t3_witness(D-PBK-22 record 込み)と **window_geometry** を持つ配置)に
対し、ここで **window_geometry := (PS-4) window_contract から W_zf 被覆
witness field を除いた部分型**(W, S, s, zf_witness(S/collar 域),
we9/d10/λ/ℓ_ext 参照)— **W_zf 被覆は本 packet の出力であって入力に仮定
しない**(循環排除 [R-T2A-R4-01]: 完全な window_contract は
window_geometry + 本 packet の wzf_cover を合成して下流(T3/A.5c)が
構成する)。このとき、
部分列 {θ_{n_k}} が存在して次の**ちょうど一つ**が成立する:
  (i) **lower-rank exit** — step-0 で child 恒等零(active_children_nonzero
      失敗)または support rank ≤ 3(rank 3 = BORD-3 資産 / rank ≤ 2 = pair
      資産へ redispatch — GC-3 zero-pruning 継承)。
  (ii) **exact-QR exit** — cross-child 全 matched 項の係数相殺(§8.16
      (PS-6) へ retract)。
  (iii) **有限 pattern chart 族 𝒜₂₂ のある chart に入る** — chart 族 =
      {PL4, CF1, CF2, XC1, XC2, TR3, RTC, QRT, CZB}((AT-2) の決定 list が
      正本 — cross-child cluster 類 XC1/XC2・3 点類 TR3 を含む [R-T2A-02])。
frame 収束・limit span の解析・Gram・床は**非主張**(T2b/T2c の義務)。

**(AT-0) step-0 routing(constant-gauge 同値と matching の型
[R-T2A-01])**: 原子 occurrence は t3_witness の label a ∈ {11, 12, 21, 22}
(child i の第 j 原子)で固定する。指数の **constant-gauge 同値**:
q_a ≃ q_b :⟺ q_a − q_b ≡ γ_ab(定数)— 定数は係数側へ exact に移る
(c_b e^{q_b} = (c_b e^{γ_ab})e^{q_a})。**within-child merge** は ≃ 同値類
ごとの係数の exact 合算 c_a + c_b e^{γ_ab}、prune は合算値 0 の類の消去 —
child 内原子数(≤ 2)を厳減させるので反復 ≤ 3 で安定 ✓。child ≡ 0(全類
prune)→ active_children_nonzero 失敗 → (i)。**cross-child matching**
(合算禁止 — consult #16): 安定化後、各 child 内の指数は ≃ 非同値なので
  M := {(a, b) : a ∈ child1, b ∈ child2, q_a ≃ q_b}
は**部分 matching**(μ := |M| ∈ {0, 1, 2} — well-defined ✓)。各 edge は
**係数 witness** (c_a, c_b, γ_ab) と相殺値 c_a + c_b e^{γ_ab}(exact)を
持つ。全 edge 相殺かつ M が両 child の全原子を被覆 → exact QR — この分岐は
(PS-6) の retract であり **exit record に qr_global_witness(§8.14)の
ref を必須で持つ**(欠落 = exit 不成立 — fail-closed)。部分相殺 = 分子の
lower-support face label。出力型:
`step0_record := (原子 label 集合, ≃ 類 + gauge 定数 γ_ab, 合算係数
(exact 値 ref), M と各 edge の係数 witness・相殺 flag, face label)`。
〔[R-T3A0 R7-01] reviewer 指示による追記(in-place、前例 [R-T2BII R1-02]
[R-T2C R7-01]): 合算係数 field の表現を明示する — **全類 ledger**: 反復
merge/prune の各段で合算値を持つ全類(prune で消去された類も (類 id,
child label, 合算値 0 exact, 元係数 ref) の entry として保持)を記録し、
**active 類集合**(合算値 ≠ 0 の生存類 — 上の「原子 label 集合」「≃ 類」
はこちら)と分離する。prune = active 類集合からの除去であって ledger からの
削除ではない。§8.24 の prune_record-v1・lower_rank_record-v1 はこの
ledger から導出される。〕

**(AT-1) rate 座標(4 点 cluster tree — child 割当と独立 [R-T2A-02])**:
安定化後の全原子対 (a, b)(within/cross の別を問わず ≤ 6 対)に
**pairwise collision scale**
  s_ab := d_w(q_a, q_b) = max(|ΔA_ab|^{1/2}, |ΔB_ab|)
(**§6 の d_w と同一物** [R-T2A-R2-01]。A = 指数の二次係数、B = 一次係数、
Δ は constant-gauge 除去後。D-PBK-22 collision-scale witness の
|ΔA| ≤ s_m², |ΔB| ≤ s_m は「s_m ≥ s_ab」と同値 — 型接続 ✓)を与える。
s_ab = 0 ⟺ q_a ≃ q_b であり、within-child は安定化済みで ≃ 非同値、
cross-child の ≃ は matching edge として (AT-0) が記録済みなので、
**未 matched 対の s_ab は正**。root 正規化 s₀ := max_{ab} s_ab とし、比
s_ab/s₀ ∈ [0, 1](compact — 分母正)の部分列極限を取り、極限 0 の cluster
内で再帰的に同じ正規化を繰り返す(各段で未確定比が厳減 → 有限深さ)。
階層 clustering により
**rooted cluster tree**(葉 = 原子 label、internal node = 分離 scale 水準、
全 internal node に scale を割当)が定まる。**child 割当(2|2 labeling)は
木と独立の葉 label** — 木が child 境界と揃う保証はない(例:
q₁₁ = 0, q₁₂ = δt, q₂₁ = δεt, q₂₂ = δ(1+ε)t では cross-child 対 {11,21},
{12,22} が細 scale δε で cluster し、child 内距離は粗 scale δ —
[R-T2A-02] の反例をそのまま XC2 類に収容)。4 葉 rooted tree × 2|2
labeling は有限個 ✓。node scale 比の再帰 blow-up は各段で未確定比の個数を
厳減させるので有限深さで停止 ✓。root scale s₀ = root node の scale、
s₀ → s* > 0 / 0 の二分岐を重ねる。

**(AT-2) compact 化と割当決定 list(全域性・排反性 [R-T2A-03])**:
部分列安定化の対象量を型で固定する — 各量は compact 距離空間に値を取る:
- 係数 vector (c_a): common gauge quotient 後**単位球に正規化**(compact。
  成分 → 0 = 係数退化 flag)。
- scale 比: [0, ∞](compact)。
- P̃ 零点: **ℂP¹ 値**(degree drop の無限遠逃避を含めて compact)、位置は
  W̄ 相対で記録。
- matched face の相殺残差: 正規化係数の連続関数(消滅 flag)。
- **零点対距離は chordal(ℂP¹)距離 d_c で測る [R-T2A-R4-02]**(通常距離
  は不可: P̃₁ = 1 + εt² は判別式 −4ε → 0 だが根距離 2/√ε → ∞ — これは
  重根化でなく両根の無限遠逃避 = **degree-drop**(先頭係数退化 flag の
  一種)であり、ℂP¹ では両根が ∞ に収束する)。「discriminant → 0 と
  同値」の旧主張は撤回([R-T2A-R3-02] の表現を本項で置換)。
- cross-side 零点対の d_c: [0, diam ℂP¹](compact)— **消滅 flag は極限点
  が有限 affine chart(W-relevant 域)にある場合のみ CZB として発火**。
  極限点 = ∞ は degree-drop flag へ。
- **same-side 零点対の d_c(成分 i ごと)**: 同様 — 消滅 + 有限極限点 =
  **重根化 flag**(係数退化と独立: P̃₁ = (t−2)² − ε², P̃₂ = 1 は係数非退化
  のまま重根化)、消滅 + 極限 ∞ = degree-drop flag。
よって対角部分列で**全 flag が同時に安定**する ✓。**割当は決定 list**
(上から順に最初に該当する行 — 排反は判定順序で強制、全行の条件は安定化
済み flag のみで判定可能):
  1. child 恒等零、または総 support rank ≤ 3 → **(i)**。**support rank :=
     within-child 安定化後の ≃ 類の総数 Σm_i(cross-child 相殺は数えない —
     carrier の次元 [R-T2A-R2-02])**。よって exact-QR(両 child 非零・
     μ = 2 で全相殺)は rank 4 のまま本行に該当しない — 行 1/2 は排反 ✓。
     **再判定の well-founded measure は Σm_i 自身であり、再判定を発火させる
     のは within-child pruning のみ**(係数退化 flag により正規化係数成分
     → 0 となった原子を極限配置から除く操作 — Σm_i を必ず ≥ 1 減らす)。
     部分的 cross-child 相殺は Σm_i を変えないため**再判定を発火させない**
     (face label として行 3 以降に流れる — [R-T2A-R3-01])。よって再判定は
     高々 3 回で終端 ✓(旧 SD label は本行に吸収)。
  2. 全 matched edge 相殺 + qr_global_witness ref → **(ii)**。
  3. QR 近接 flag(相殺残差 → 0、exact 相殺でない)→ **QRT**。
  4. **cross-side 零点対の d_c 消滅 flag(有限極限点)** → **CZB**
     (outer/inner — (PS-5))。極限点 ∞ の消滅は degree-drop flag として
     行 5–9 へ([R-T2A-R4-02])。**same-side 重根化 flag は本行に該当しない**((PS-5) は
     両側 common zero 用 — P̃₁ = (t−a)², P̃₂ = 1 は互いに素のまま
     [R-T2A-R2-03])。**same-side の routing predicate([R-T2A-R3-02]
     明示)**: 重根化 flag = true は chart 割当を変えず(判定は行 5–9 の
     木型へそのまま進む)、効果は wzf_cover 側のみ — 当該 2 零点を
     **重複度 2 の単一零点として記録**する(Re 投影 clustering の一 case
     として同一 cluster に落ちる — U・radii は cluster 単位 [R-T2A-R8-01])。
  5. 木 = 全分離 → **PL4**。
  6. within-child 対のみ合流(1 child / 2 child)→ **CF1 / CF2**。
  7. cross-child 対の合流(1 対 / 2 対)→ **XC1 / XC2**。
  8. 3 原子 cluster → **TR3**。
  9. 全 4 原子合流(root)→ **RTC**(T2b の crux 送り)。
**全域性**: 行 5–9 は 4 葉 rooted tree の cluster 型 {全分離, 対 1(within/
cross), 対 2(within×2 / cross×2 / 混在 → 対の label で 6–7 に分配), 3 点,
4 点} を尽くす(有限列挙 ✓)。行 1–4 は flag による事前分岐。よって
安定化済み部分列は必ずちょうど一つの行に落ちる — leftover なし ∎。
(各 chart の limit span の解析は T2b — 本 packet は割当の全域性のみ。)

**(AT-3) W_zf 被覆(固定配置 + 部分列一様化 [R-T2A-04])**: 固定配置では
§8.3 (F2²-1) の全 branch |V_i| ≥ 0.27(cell 全域)より 𝐁̃ 成分の零点は
P̃_i の零点に限られ **各 ≤ 2・計 ≤ 4 個**、P̃₁, P̃₂ 互いに素より exact 共通
零点なし。**W-relevance の定義([R-T2A-R3-03][R-T2A-R4-02][R-T2A-R8-01])**: 被覆に
関与するのは **W-relevant 零点**(ℂP¹ の有限 affine chart に属し、かつ
dist(Re z_j, W) < r_S のもの — ∞ 近傍の零点は有界集合を離れるので
W-relevant になり得ず、Re は有限 chart でのみ使う)のみ — それ以外の零点は
被覆簿記から除外する(W 上の下界は距離が直接供給、exclusion 不要)。
  **atlas cluster 集合の定義([R-T2A-R8-03])**: C = 全 Re 投影 cluster、
**C_atlas := C ∖ dom(handoff.transfer_clusters)** — **U_c・r_c・cluster 表
の radii・(α)(δ)(γ) の domain はすべて C_atlas に限定**する(transfer
cluster は U も r も持たない — r_c → 0 の型参照は発生しない)。除外域 U は
**C_atlas の cluster 単位**で構成する([R-T2A-R6-01] — 下記分離極限
分岐): **U_c := {t ∈ W : |t − x_c| < r_c}**(c ∈ C_atlas。W との交わり
として定義 — **U_c ⊂ W は構成から自明** ✓)。**W_reg の定義
([R-T2A-R4-03][R-T2A-R7-01])**:
**W_reg := W ∖ (collar(S, r_S) ∪ ⋃_{c ∈ C_atlas} U_c ∪ Σ)**
(補集合として定義 — 分割恒等式は自明。実質の主張は「W_reg 上に
W-relevant 零点がない」= 下記 (δ))。**Σ は移管領域**
(atlas 時点で本 cell が被覆しない領域と明示 — (AT) の被覆主張は
「W ∖ Σ の被覆 + Σ の帰属排反」であり、Σ の被覆は受け手 cell の義務
(chain 接続時に receiver_check で検証 — A.5b/A.5c)。Σ = ∅ の場合は
従来どおり全被覆)。**部分列一様化**: 零点
位置は ℂP¹ compact なので部分列で z_{j,n} → z_j* が収束し、次の排反分岐が
安定する:
- **分離極限** → **Re 投影 cluster 統合と radii([R-T2A-R6-01])**:
  被覆は実区間 W 上で行うため、まず W-relevant 零点を **Re 投影の
  clustering** で統合する — pairwise |Re z_j − Re z_k| の部分列極限が 0 の
  対を同一 cluster に(複素平面で相異なる零点でも投影が衝突し得る — 例
  P̃₁ = t(t − i) の零点 0, i は Re 共に 0 → **1 cluster に統合**、CZB や
  重根化 flag とは独立の純被覆簿記)。cluster c の代表点 x_c = 投影の
  中点、**重複度 = 構成零点の個数和**、
  **r_c := (min cluster 間 Re 距離 ∧ dist(x_c, ∂W) ∧ r_S)/3**
  (**空集合規約** = min の対象が空なら当該項は +∞(項が落ちる)
  [R-T2A-R5-03])。cluster 間距離は安定化後**正**(距離 → 0 の対は同一
  cluster に統合済み — 構成から)⇒ r_c は **n によらず下に正** ⇒ 被覆が
  **n 一様半径**で成立 ✓(U は cluster 単位: U_c := {t ∈ W :
  |t − x_c| < r_c})。**x_c ∉ W の cluster**(実部投影が W 外・r_S 未満)と
  **dist(x_c, ∂W) → 0 の cluster** は分離極限分岐でなく **handoff の
  transfer_clusters へ routing**(下記 — U を作らない)[R-T2A-R5-03]
  [R-T2A-R6-02][R-T2A-R7-03]。排反は極限値で判定。
- **零点対の衝突**(|z_{j,n} − z_{k,n}| → 0)→ (AT-2) 行 4 CZB に該当し
  bubble chart へ routed(当該近傍の被覆役は inner chart が引き継ぐ —
  W_reg から除外)✓。
- **∂W への接近・外部投影** → **handoff record(単一 record 型 —
  R6 の 2 branch union を置換 [R-T2A-R7-02])**:
  `handoff := (Σ := {t ∈ W : dist(t, ∂W) < ρ_b}(witnessed ρ_b > 0 —
  **record レベルで束縛**、全 field が同一 Σ を参照),
  target cell_id(§8.1 左閉右開規約による帰属),
  receiver_check(receiver_geometry_ref, evidence: Σ ⊂ W′ の検証記録),
  **transfer_clusters: {c ↦ evidence((B(x_c, ρ_c^tr) ∩ W) ⊂ Σ)}**(map —
  複数 cluster 可 [R-T2A-R7-02]。対象 = **外部投影 cluster(x_c ∉ W)と
  境界接近 cluster(dist(x_c, ∂W) → 0)の両方** [R-T2A-R7-03] —
  後者は r_c → 0 で (γ) と矛盾するため U を作らず Σ へ移管する。
  ρ_c^tr = witnessed 影響半径、evidence が Σ の十分な広さを検証 —
  不足 = 構成不能))`
  (W′ = 受け手 cell の window geometry。receiver_check は atlas 生成時
  **pending 可**だが、pending の間 **(δ) checked_zero_free は「W ∖ Σ」域
  のみを証書し、Σ を被覆済みに数えることは構成上不可能**
  ([R-T2A-R4-03])。A.5c は receiver_check が埋まるまで witness を消費
  禁止(fail-closed))。**transfer_clusters の cluster は (α)/(γ) の
  index 集合から型上除外される**(下記結合条件 — evidence なしの除外は
  構成不能)。**handoff は option 型**([R-T2A-R8-02]):
  `handoff := None | Some(上記 record)` — **total accessor を型で定義**:
  Σ(None) := ∅、transfer_clusters(None) := ∅(absent 側でも field
  projection が常に定義され、(α)/(γ) の index 式 C ∖ dom(transfer_clusters)
  は全 case で well-defined)。**receiver_check は discriminated union**:
  `receiver_check := pending | checked(evidence: Σ ⊂ W′ の検証記録)`
  (pending の効果は (δ) の Σ 対象外規約と A.5c 消費禁止 — 上記)。
  routing の動的選択は A.5b、**本 packet は margin の型と帰属の排反
  のみ**。
- **S̄ への接近** → zf_witness(A.3a (ZF-3))の invariant (i)
  (dist(Re z, S) ≥ ρ/13)の検証で排除(fail-closed — ref 必須)。
one-sided 零点近傍での g の極限挙動は**主張しない**(T2b/T2c [R-T2A-05])。
`wzf_cover record := (零点リスト(ℂP¹・重複度), **cluster 表
{c ↦ (構成零点, x_c, 重複度和)}**, radii **r_c**(正値 witness — index は
cluster [R-T2A-R7-01]), zf_witness 参照, handoff record(transfer 時 —
上記), invariants)`
**invariant の typed constructor([R-T2A-R3-04][R-T2A-R4-04] — §8.16
(PS-9) の branch constructor と同方式。引数型・結合条件込みで固定し、
任意 ref の差し込みを排除する)**:
  (α) `checked_subset(defs: {c ↦ U_c 定義 record})` — **結合条件**:
      index 集合 = **Re 投影 cluster の集合から handoff.transfer_clusters
      を除いたもの**と 1:1(過不足 = 構成不能 [R-T2A-R6-02]
      [R-T2A-R7-02]。除外は transfer evidence がある cluster のみ —
      evidence なしの除外は型上不可能)。包含は定義 U_c := B(x_c, r_c) ∩ W
      から構成的。
  (δ) `checked_zero_free(table: 端点表 record)` — 端点表 = W ∖ Σ を有限個
      の区間端点で分割し各小区間の帰属(W_reg / collar / U_c)を列挙
      [R-T2A-R7-01]、
      **各 W-relevant 零点 j(c(j) ∈ C_atlas)について
      |Re z_j − x_{c(j)}| < r_{c(j)}(= Re z_j ∈ U_{c(j)} の membership)の
      検証行を含む**(distance-to-W_reg 形は cluster 中点からの偏差で
      破れ得るため membership 形に変更 [R-T2A-R8-01] — 零点が自 cluster の
      U に入っていれば W_reg = W ∖ (… ∪ U ∪ Σ) の零点自由性が従う。
      c(j) ∈ dom(transfer_clusters) の零点は evidence(影響域 ⊂ Σ)により
      Σ 側 — 検証行の対象外 [R-T2A-R6-02][R-T2A-R7-03])。
      **結合条件**: 零点行は零点リストと 1:1、区間列は W ∖ Σ を尽くす
      (端点の全順序検証)。証書内容 = 「W_reg 上に W-relevant 零点なし」
      (**Σ は対象外 — 移管領域**。旧 (β) checked_cover は本 constructor
      に置換: 分割恒等式は W_reg の定義から自明のため、証書すべきは
      零点自由性 [R-T2A-R4-03])。
  (γ) `checked_positive(bounds: {c ↦ 有理下界 q_c > 0})` — **結合条件**:
      (α) と同一 index 集合(= cluster − transfer_clusters)、r_c ≥ q_c の
      検証値 ref(境界接近 cluster は transfer 側に居るため r_c → 0 との
      矛盾は生じない [R-T2A-R7-03])。
— invariant は **record 生成時の検証条件**(constructor が組めない =
record 生成禁止 — (ZF-3) と同型)。この record は **(PS-4) zf_scope の W_zf 被覆 witness の
静的成分を instantiate** する(動的選択 = A.5b — consult #16 帰属分割)。

**(AT-4) 出力契約 [R-T2A-05][R-T2A-R2-05]**: `atlas_witness-v1 :=
(cell_id, t3_witness 参照, **window_geometry 参照([R-T2A-R4-01] —
入力は W_zf field を除いた部分型。完全な (PS-4) window_contract は本
witness の wzf_cover と合成して下流が構成する)**, step0_record,
cluster tree 型(node scale 付き),
wzf_cover record((AT-3) — (PS-4) W_zf 静的成分),
exit = **lower_rank(redispatch record)| exact_qr(qr_global_witness
ref)| chart(chart label)** の discriminated union — exact_qr 側は
qr_global_witness ref を **constructor 引数**として持ち、ref なしの
exact_qr は型上構成不能((PS-9) の valid | nogo と同じ branch
constructor 方式))`
— fail-closed は **field の存在 + checked invariant**((AT-3) の
(α)(δ)(γ) — 旧 (β) は (δ) checked_zero_free に置換済み [R-T2A-R5-02]。
invariant 不成立 = witness 生成禁止)。T2b はこの
witness の chart label ごとに frame を建てる。
∎(被覆完備性のみ — 各 chart の解析は T2b/T2c)

**scope(非主張)**: 各 chart の limit span の正しさ・Fock-strong 収束・
Gram 床・carrier 床 m_C の一様性・ord/projective order 床・(PTN-22)・
A.5b 動的 restart・有効定数、人間による査読は未実施。

### 8.18 GC-5-T2b BORD22-FRAME(chart 別 strong frame — **tree-Newton 経路撤回**(R-T2B R1 blocking 6 + consult #17)。(B22-0) 二段正規化・(B22-1) 成分直交 block 対角・(B22-2a) は T2b-0/i/ii が再消費、**(B22-2b)〜(B22-5) は失敗経路の記録**(効力なし [R-T2B0 R1-01] — tree-Newton とその派生 claim(chart 別 frame 族・Gram 鎖の適用・span 表(TR3 deg ≤ 4 を含む)・frame_witness-v1)は全て撤回。span 表の正は consult #17: TR3-root_far deg ≤ 5 / root_collapse deg ≤ 9)。再設計 = §8.18 追記)

**目的**: T2a atlas_witness(chart label 確定済みの部分列)上で、consult #16
の二段正規化 — **carrier pair 𝐂_n ∈ ℱ⊕ℱ** と **defect f_n ∈ ℱ** — の
Fock-strong 収束 frame・exact limit span・Gram 床を chart ごとに建てる。
**ord 上界・carrier 床 m_C の値・moving-center 床は非主張**(T2c の義務)。

**(B22-0) 入力と二段正規化**: 入力は atlas_witness-v1(§8.17 — exit =
chart(label) の枝のみ。lower_rank/exact_qr は T2b に入らない)と
window_geometry。chart 箱は Fock-admissible(|A| ≤ 1 − δ_ℱ、|B| ≤ R_ℱ —
§8.9 追記の chart box 定数、(B3-1) と同一の束縛)とする。gauge section
**U_n** は FR §8.4 の strong-continuous unitary gauge section(accepted 資産
— recenter/rescale を chart 箱 K_{δ_ℱ,R_ℱ} 内へ写す)を pair の両成分に
**共通に**適用する(common gauge quotient の代表選択 — 成分別 gauge は
(PS-1) の相対振幅を壊すため禁止、consult #16)。正規化:
  ρ_n := ‖U_n𝐁̃_n‖_⊕(‖(u, v)‖_⊕² := ‖u‖_ℱ² + ‖v‖_ℱ²)、
  **𝐂_n := ρ_n⁻¹U_n𝐁̃_n**(‖𝐂_n‖_⊕ = 1)、
  δ_n := ‖C_{1,n} + C_{2,n}‖_ℱ、**f_n := δ_n⁻¹(C_{1,n} + C_{2,n})**
(δ_n = 0 は exact QR で atlas が (ii) に routing 済み — T2b の定義域では
δ_n > 0 ✓)。step-0 安定化(AT-0)後の各成分は **≤ 2 原子**:
C_{i,n} = Σ_{j≤m_i} c_{ij,n} e^{q_{ij,n}}(m_i ∈ {1, 2})。

**(B22-1) carrier frame(成分直交 ⟹ Gram block 対角)**: ℱ⊕ℱ で
⟨(u, 0), (0, v)⟩_⊕ = 0 — **成分をまたぐ Gram 交差項は恒等的に零**であり、
carrier の joint Gram は **G_⊕ = diag(G₁, G₂) と block 対角**になる
(cross-child の解析は carrier 側には現れない — 現れるのは defect 側のみ。
これが本 packet の構造原理)。各成分の frame は m_i で分岐:
- **m_i = 1**: 単原子 e^{q}/‖e^{q}‖ — chart 箱で ℱ-norm 連続、strong 収束
  ((B3-1) と同じ box 束縛)。G_i = 1。
- **m_i = 2・分離**(within-child 合流 flag なし): 2 原子、対距離下界 > 0
  ⟹ 極限原子は相異なり独立 — G_i → G_{i,*} > 0。
- **m_i = 2・合流**(CF/RTC 等で当該 child が合流): **(B3-4a) の 2 原子
  Newton frame をそのまま消費**(§8.10 accepted — 積分表示、ℱ-strong 極限
  {e^{q*}, L_{ν̂*}e^{q*}}、L_{ν̂*} ≢ 0 非定数 ⟹ 独立)。
いずれも child frame の strong 極限は独立 ⟹ G_{i,*} > 0 ⟹
**G_{⊕,*} = diag(G_{1,*}, G_{2,*}) > 0**(chart 定数の床 — 有効値非主張)。
(B3-4) の Gram 鎖(G_n → G_* > 0 ⟹ 単位球係数有界 ⟹ strong 極限・norm 1)
を ‖𝐂_n‖_⊕ = 1 に適用し **𝐂_n → 𝐂_* strong、‖𝐂_*‖_⊕ = 1** ✓。成分消滅
flag(‖C_{i,*}‖ = 0 の側)は部分列で安定し、atlas の outer routing
([1:0]/[0:1])と整合する(消滅側の極限挙動の解析は T2c — 本 packet は
flag の安定化のみ)。

**(B22-2) defect frame(≤ 4 原子 cluster — child label は無関係)**:
f_n は**和**なので ℱ 内の ≤ 4 原子系であり、child 割当は frame 構成に
関与しない(atlas の cluster tree(AT-1 — child 独立)だけが構造を決める。
XC 系 chart が CF 系と同じ frame 族に落ちるのはこのため)。安定化済み
cluster tree T に沿って frame を建てる:
- **(B22-2a) 対 cluster**: (B3-4a) の Newton frame(引用 — 再証明しない)。
**【以下 (B22-2b)〜(B22-5) は撤回済み・効力なし(R-T2B R1 + consult #17
[R-T2B0 R1-01][R2-01])— tree-Newton とその派生 claim の全体。新設計
(J⁹-SVD/graph frame・frame_outcome-v2)は T2b-i/ii が §8.20 以降で
与える。以下は失敗経路の記録のみ】**

- **(B22-2b) tree-Newton frame(k ≤ 4 原子、深さ ≥ 2 の木 — 撤回済み
  記録)**: 木 T の内部 node を細 scale から粗 scale の順に処理し、
  **反復差分商 frame** を作る: 各 node で、その子 cluster の代表元
  (処理済み frame の第 0 ベクトル = 当該 cluster の基準原子)の対に
  (B3-4a) と同じ正規化差分商
    D_node := (代表₂ − 代表₁)/t_node(t_node = node scale の正規化距離)
  を割当て、frame := {基準原子} ∪ {各 node の D_node を、その node より細の
  frame ベクトルに乗る形で展開したもの}(k 原子 → k 本 — 次元勘定 ✓)。
  **積分表示の帰納**: (B3-4a) の表示を node ごとに適用すると、各 frame
  ベクトルは
    (Π_{node ∈ path} L_{ν̂_node} の主部 + 高次補正)· e^{q_基準} の形の
  ℱ-値積分で書け、chart 箱束縛(二次係数 < 1/2 一様)の下でパラメタに
  ℱ-norm 連続 — **部分列で ℱ-strong 極限 {Q_ℓ e^{q*}} を持つ**(Q_ℓ =
  差分方向の極限多項式の積、**deg Q_ℓ ≤ 2 × (path 上の node 数) ≤ 6**)。
  **独立性(方向非衝突時)**: 各 L_{ν̂*} は非零・非定数(ν̂ ∈ S³ 正規化)
  なので、path の node 集合が異なる frame ベクトル同士は Q_ℓ の**次数が
  厳増**し独立 ✓ — ただし異 path で同次数となる場合(例: 木 (12)(34) の
  2 対方向)は L 同士の比例が起こり得る。
  **方向衝突 sub-recursion([B22-2b-r])**: 極限方向対が比例
  (ν̂*_a ∥ ν̂*_b)で {Q_ℓ} が従属になる場合、当該対の**次階差分商**
  (D_a − κ_n D_b)/t′_n(κ_n = 比例係数の n 実現値、t′_n = 正規化残差
  scale)を frame ベクトルに置換して再収束させる。**停止性**: 各再帰は
  正規化方向データ(node ごとの ν̂ ∈ S³ — 有限次元)の**追加の exact 一致を
  極限で強制**し、未一致パラメタの実次元を厳減させる ⟹ 再帰深さ ≤ 4
  (有限次元の厳減)✓。各再帰は Q の次数を高々 +2 する — k ≤ 4 で総次数
  ≤ 6 + 2·(再帰) だが、**T2c の消費は deg ≤ 9 予算内であることのみ要求**
  し、超過が起こる場合は当該 chart を **RTC-deep sub-chart** として記録
  (T2c が予算判定 — 本 packet は frame の存在と次数の上界記録のみ)。
- **(B22-2c) chart 別 frame 族**(atlas label → frame): PL4 = 4 分離原子 /
  CF1 = (B3-4a) 対 + 2 分離 / CF2 = (B3-4a) 対 × 2 / XC1・XC2 = 同上
  (対の child 所属のみ異なる — defect frame は同形)/ TR3 = (B22-2b)
  3 原子木 + 1 分離 / RTC = (B22-2b) 4 原子木 / QRT・CZB = **下部の木
  pattern の frame を継承**(これらの chart label の役割は T2c の中心選択・
  分母処理であり、frame は木構造のみで決まる)。

**(B22-3) Gram 床と strong 極限の鎖**: (B3-4) の鎖をそのまま適用する —
各 chart の frame w_{ℓ,n}((B22-1)(B22-2))は ℱ-strong 収束し極限は独立
⟹ G_n → G_* > 0 ⟹ 単位球の係数有界 ⟹ **V_n := span{w_{ℓ,n}} の任意の単位
ベクトル列は部分列で ℱ-strong 極限(norm 1・極限 span 所属)を持つ**。
f_n(‖f_n‖_ℱ = 1、f_n ∈ V_n^{defect})と 𝐂_n(‖·‖_⊕ = 1)の双方に適用 ✓。
moving-center RKHS 連続性((B3-4) 末尾)も chart 箱ごと不変に成立 —
**J^9 版**(k ≤ 9 階微分評価汎関数の norm 連続・compact 一様有界)を同文で
記録する(T2c が消費)。

**(B22-4) exact limit span 表(ord 上界は非主張 — T2c)**:
  | chart | defect 極限 span |
  | PL4 | plain 4 class {e^{q_j*}} |
  | CF1/XC1 | {e^{p}, L e^{p}, e^{q}, e^{r}}(L 非定数 deg ≤ 2) |
  | CF2/XC2 | {e^{p}, L₁e^{p}, e^{q}, L₂e^{q}}(= {P₁e^{p}, P₂e^{q}} 形) |
  | TR3 | {Q₀e^{p}, Q₁e^{p}, Q₂e^{p}, e^{q}}(deg Q ≤ 4) |
  | RTC | {Q_ℓ e^{q*}}(ℓ ≤ 3、deg Q_ℓ ≤ 6 + sub-recursion 加算・記録付き) |
  | QRT/CZB | 下部木 pattern の span を継承 |
carrier 極限は成分ごとに {原子} / {e^{q*}, L e^{q*}}(m_i 別)。

**(B22-5) 出力契約**: `frame_witness-v1 := (atlas_witness 参照(chart 枝),
gauge section record(U_n — FR §8.4 型), carrier frame record(成分別
m_i・frame 型・G_{i,*} > 0 witness), defect frame record(木 T、frame 型
(分離 / (B3-4a) / tree-Newton + sub-recursion 深さと次数記録), G_* > 0
witness), limit span label((B22-4) の行 — 生成元の型付き記述),
J⁹ RKHS record((B22-3)))` — fail-closed(field 欠落・invariant 不成立 =
witness 生成禁止)。T2c はこの witness のみを消費して床を張る。∎

**scope(非主張)**: 各 span の ord/projective order 上界(T2c — W_c(4)/
W_CONFL/W′/混合消去の消費先)、carrier 床 m_C の値と一様性(T2c)、
moving-center 床・量的連鎖・対偶(T2c)、(PTN-22)(T3)、有効定数、
人間による査読は未実施。

**§8.18 追記(2026-08-22 — tree-Newton 撤回と再設計、consult #17)**:
R-T2B R1(blocking 6)の核心 = (B22-2b) の独立性論法が偽(次数厳増は
L₁ = z, L₂ = z², L₃ = z + z² の三者従属を排除しない — pairwise 比例検出の
sub-recursion では rank drop を捕捉不能)+ 停止測度未定義。consult #17
(Sol、`sol-t2b-consult.md`)の裁定:
- **証明エンジンの交換**: tree-Newton(組合せ的独立性)を撤回し、
  **J⁹-rank-revealing SVD/graph frame** に置換 —
  α_n := inf{‖P₉v‖ : v ∈ V_n, ‖v‖_ℱ = 1}(P₉ = 0..9 次 jet への直交射影)
  を正本とする(基底不変・多者従属を最小特異値で一括検出 — greedy pivot の
  順序依存も排除)。W_n := P₉V_n の正規直交基底 p_ℓ を持上げ
  w_ℓ := (P₉|_{V_n})⁻¹p_ℓ = p_ℓ + A_np_ℓ(graph operator
  A_n := (I−P₉)(P₉|_{V_n})⁻¹)とすれば **G_n = I + A_n*A_n ≥ I** —
  独立性を次数・方向の組合せから証明する必要が消滅する。
- **framed | overflow の型付き二択**: liminf α_n > 0 = non-overflow(frame
  成立)/ α_n → 0 = **overflow**(単位ベクトルの 0..9 jet 質量消滅 —
  §8.15 追記の no-go 基準「指数 9 の定数 → 0」への **bridge evidence 付き
  witness** として出力)。**循環の切り方**: non-overflow 列のみ T2c の床が
  frame を消費、overflow 列は frame を消費せず no-go 判定へ —
  「T2c で overflow の空性を証明」はしない(それは循環)。出力型 =
  `frame_outcome-v2 := framed(frame_witness) | overflow(overflow_witness
  := (exact 単位ベクトル列と係数, gauge 後中心と moving center の対応,
  ‖P₉v_n‖ → 0 の記録, 潰れる床定数の特定, PS-9 detected(evidence) への
  変換証明))`。
- **残る証明義務**: strong compactness は「低 grade に質量が残る」だけでは
  出ない — **tail-tightness 補題**(α ≥ ε の chart 列で A_n が有限 rank
  同一化後 operator-norm precompact — Gaussian Taylor remainder / 係数
  recurrence から)が T2b-i の実質。
- **正規化子は統一しない**: d_w = max(|ΔB|, |ΔA|^{1/2})(parabolic rate
  atlas 用 — T2a 不変)と t = ‖(ΔB, ΔA/2)‖₂(差分商の除数 — B3-4a と
  同一)を型分離し、**node_scale_bridge**(d²/2 ≤ t ≤ (√5/2)d — 二側
  t ≍ d は偽: 純二次差分で d = ε, t = ε²/2)で接続。差分商は常に t 割り
  (純二次差分でも極限方向 z² が生存)。
- **TR3 は二分岐**: root_far(3 原子 cluster と singleton の root 距離が
  正極限)= BORD-3 の E₃ = span{Q₀e^p, Q₁e^p, Q₂e^p}(**deg ≤ 5** —
  R1 指摘どおり deg ≤ 4 は撤回)+ span{e^q}(q − p ≢ const)/
  root_collapse(root scale → 0 — singleton も合流、e^p ∈ E₃ の危険で
  4 本目を失い得る)= nested 3+1 の 4 原子 J⁹ frame(deg ≤ 9)。
  sublabel は T2a 非改変の versioned 下流拡張(T2b-0)。T2c には
  **3+1 mixed-span valuation lemma** が別途必要(義務登録済み — §4)。
- **common gauge 契約**: frame_input-v2 := (atlas_witness-v1 ref,
  common_gauge_record-v1(pivot leaf・section id・U_n・scalar 吸収表・
  変換後原子表・全 4 原子 box 所属 evidence・strong section evidence・
  node_scale_bridge 表))— accepted atlas を書き換えず **T2b-0 の前処理
  補題**として構成。「全原子を原点へ」は RTC/TR3-collapse 限定(root-far
  は pivot のみ原点・分離原子は box 内)。
- **chart 一様 Gram floor**: 閉 compact K_χ(rate・pivot・permutation・
  boundary strata 込み)+ support rank 一定 + strong frame 収束 + 全境界点
  で極限独立 + strong section ⟹ λ_min G は下半連続、compact 上 inf > 0。
  **overflow locus を除いた集合は非 compact** — α ≥ ε_χ の閉 subchart 分割
  で扱う(または空性の独立証明 — T2c の床とは別経路)。
- **packet 3 分割**(consult #16 の 4 分割を改訂 — T2b := {T2b-0
  GAUGE-SCALE-ADAPTER(1–2R), T2b-i HEAD9-FRAME(3–5R), T2b-ii
  CHART-FRAME(2–3R)})。T2b 全体 6–10 round、T2c 3–5 round 見込み。

### 8.19 GC-5-T2b-0 GAUGE-SCALE-ADAPTER(atlas → frame の前処理補題 — **accepted、R-T2B0 R3 PASS、fixed SHA `7103b2e`**。半箱前提の供給は T2b-ii obligation — それまで条件付き constructor)

**目的**: consult #17 の 3 分割の第 1 packet。accepted な atlas_witness-v1
(§8.17)を書き換えずに、T2b-i/ii が消費する **frame_input-v2** を構成する
前処理補題と型を固定する。frame 収束・α_n・overflow・span・Gram・床は
**非主張**(T2b-i/ii)。

**(AD22-0) 型定義**:
  `frame_input-v2 := (atlas_witness-v1 参照(chart 枝),
   chart_sublabel((AD22-3) — root_scale_limit constructor からのみ生成),
   common_gauge_record-v1)`
  `common_gauge_record-v1 := (pivot_leaf(決定的規約 — 下記), section_id,
   U_n(FR §8.4 gauge section — 消費条件付き), scalar_absorption_table
   (gauge が各原子に生む非零 scalar の exact 係数吸収 — 原子 label ごと),
   transformed_atom_table(変換後の (B, A) パラメタ — exact),
   half_box_premise evidence(raw 原子の半箱所属 — (AD22-2) [R-T2B0
   R1-03]), section_param_bound_ref(FR §8.4 のパラメタ作用有界性 —
   消費条件), all_atoms_in_K evidence(変換後 4 原子すべての K_{δ_ℱ,R_ℱ}
   所属検証), strong_section evidence(U_n → U_* strongly の検証 ref),
   root_scale_limit((AD22-3) [R-T2B0 R1-05]),
   node_scale_bridge 表(合流 node ごと — 下記))`
  `node_scale_bridge := (対象 node(**合流 node のみ** — 分離 node は
   差分商を取らないため bridge 不要、型で除外 [R-T2B0 R1-02]),
   代表葉対(決定的規約 — (AD22-2) [R-T2B0 R1-04]),
   d_parabolic(= (AT-1) の s_ab — rate atlas 側の参考値。**gauge 前後の
   保存は主張しない**(EW-B: full metaplectic covariance なし)
   [R-T2B0 R2-02]),
   **d_frame := max(|ΔB′|, |ΔA′|^{1/2})**(transformed_atom_table の
   **変換後差分から再計算** — bridge 不等式の d は常にこちら),
   t_increment := ‖(ΔB′, ΔA′/2)‖₂(**同じ変換後差分** — (B3-4a) と同一),
   ν̂ := (ΔB′, ΔA′/2)/t ∈ S³, exact_difference_ref,
   verified: **d_frame ≤ 1**(合流 node は d_frame → 0 なので十分先の
   部分列で成立 — 不成立の有限先頭部は record 生成禁止 = 部分列規約),
   verified: d_frame²/2 ≤ t ≤ (√5/2)d_frame(**同一座標系の対なので
   (AD22-1) がそのまま適用** [R-T2B0 R2-02]))`
— fail-closed: field 欠落・verified 不成立 = record 生成禁止。

**(AD22-1) bridge 不等式(初等)**: d := max(|ΔB|, |ΔA|^{1/2}) ≤ 1、
t := (|ΔB|² + |ΔA|²/4)^{1/2} に対し **d²/2 ≤ t ≤ (√5/2)d**。
証明: (下界)d = |ΔB| なら t ≥ |ΔB| = d ≥ d²(d ≤ 1)≥ d²/2。
d = |ΔA|^{1/2} なら t ≥ |ΔA|/2 = d²/2。(上界)|ΔB| ≤ d、|ΔA| ≤ d² ≤ d
より t ≤ (d² + d⁴/4)^{1/2} ≤ d(1 + 1/4)^{1/2} = (√5/2)d。∎
**二側比較 t ≍ d は主張しない**(偽 — 純二次差分 ΔB = 0, ΔA = ε² で
d = ε, t = ε²/2。consult #17)。差分商は常に **t で割る**(純二次差分でも
極限方向 ν̂ → (0, 1)、L_ν̂ → z² が生存 — (B3-4a) の正規化と同一)。

**(AD22-2) pivot 規約と gauge の共通適用(前処理補題)**: 主張 — atlas の
chart 枝 witness(安定化済み部分列)に対し frame_input-v2 が構成できる。
- **pivot_leaf の決定的規約([R-T2B0 R1-04] — tie-break 込み)**:
  chart label で分岐 — 全原子合流系(RTC / TR3-root_collapse)は root
  cluster の label 最小原子、それ以外は**最細 scale cluster の label 最小
  原子**。**tie-break**: 最細 scale cluster が複数(例: (12)(34) の 2 対)
  なら「構成原子の最小 label が最小の cluster」を選ぶ(label 全順序による
  決定的規約 — 「部分列で固定」に依存しない well-definedness)。cluster が
  自明なら label 最小原子。permutation も同時に固定。
  **node 代表葉対の規約**: 各 internal node の差分は「左子 cluster の
  label 最小葉、右子 cluster の label 最小葉」の対で取る(左右 = 最小
  label 側を左とする決定的順序)— (B3-4a) の t は二原子差分の量なので、
  node 単位の (ΔA, ΔB) はこの代表葉対の transformed_atom_table 値から
  exact に読む(exact_difference_ref = 代表葉対 ref)。
- **U_n の消費条件**: FR §8.4 の gauge section を pivot の (B, A) 中心で
  適用する。消費条件 = pivot パラメタが chart 箱(Fock-admissible
  K_{δ_ℱ,R_ℱ} — §8.9 追記)に属すこと(atlas の chart 箱束縛から充足 —
  verified field)。**同一 U_n を pair 両成分の全 4 原子に適用**する:
  gauge の作用は指数パラメタの exact affine 変換 + 原子ごとの非零 scalar
  であり、scalar は係数へ exact に吸収(scalar_absorption_table —
  g は共通 scalar gauge 不変なので (PS-1) と整合、成分別 gauge は使わない
  ✓)。変換後パラメタは transformed_atom_table に exact 記録。
- **全原子の box 所属([R-T2B0 R1-03] — FR §8.4 だけからは導けない)**:
  前提を型に置く: **半箱前提** — raw 原子パラメタが半サイズ箱
  |A_j| ≤ (1 − δ_ℱ)/2、|B_j| ≤ R_ℱ/2 に属すこと(evidence ref 必須、
  欠落 = record 生成禁止)。**供給源は本 packet では未確定** — F2²/A.0 の
  held witness は sup_cell|η̃_i| ≤ 1/8 のみで半箱を供給しない(旧記述は
  撤回 [R-T2B0 R2-03])。**半箱前提の供給(chart 正規化層での証明)は
  GC-5-T2b-ii の chart 箱定義に obligation として登録**(§4 台帳 —
  T2b-ii 受理まで adapter は条件付き constructor: premise が埋まった
  record のみ生成可能で、それまでは fail-closed に閉じる)。このとき pivot 相対
  差分は |ΔA| ≤ 1 − δ_ℱ、|ΔB| ≤ R_ℱ を満たし、FR §8.4 section の
  パラメタ作用の有界性(**消費条件として section_param_bound_ref を型に
  追加** — section が指数パラメタに exact affine 変換 + scalar を与え、
  変換後パラメタが pivot 相対差分の連続有界像であること)と併せて
  **変換後 4 原子すべてが閉 Fock-admissible 箱 K_{δ_ℱ,R_ℱ} に属す**。
  RTC/TR3-collapse では全差分 → 0 なので変換後原子は原点近傍(自動)✓、
  root-far の分離原子は半箱前提が直接効く ✓。検証は record 生成時
  (fail-closed)。
  **「全原子を原点へ」は RTC / TR3-root_collapse 限定**(全差分 → 0 なので
  変換後全原子 → 原点)。root-far 系では pivot のみ原点、分離原子は箱内に
  残る(consult #17)✓。
- **strong section**: U_n のパラメタ(pivot の (B, A))は部分列で収束
  (chart 箱 compact)し、FR §8.4 の section は strong-continuous(accepted
  資産)— よって **U_n → U_* strongly**(evidence = パラメタ収束 ref +
  section の strong-continuity ref)✓。∎
**(AD22-3) TR3 sublabel(versioned 下流拡張 — T2a 非改変)
[R-T2B0 R1-05]**: adapter は typed constructor
  `root_scale_limit := far(evidence ref) | collapse(evidence ref)`
を common_gauge_record-v1 の field として持つ — evidence = atlas_witness の
cluster tree 型 field(node scale 付き — (AT-1) の安定化記録)の root node
scale 極限の ref(**判定不能 = record 生成禁止** — fail-closed。新しい判定
は導入しない — coverage theorem の再開不要、consult #17)。sublabel は
  `chart_sublabel := TR3(root_far) | TR3(root_collapse) | none`
として **frame_input-v2 の明示 field** に置き(型に追加)、root_scale_limit
constructor からのみ生成可能とする(atlas_witness 本体は不変)。

**scope(非主張)**: frame の strong 収束・α_n と overflow・exact span・
Gram 床・chart 一様床(T2b-i/ii)、ord 上界・量的連鎖(T2c)、有効定数、
人間による査読は未実施。

### 8.20 GC-5-T2b-i HEAD9-FRAME(**撤回 — R-T2BI R1 blocking 5 + consult #18**。full-span tail-tightness は「修正で閉じる規模ではない」と裁定(recurrence の反例 e^{ηz²}・multiplier 型未定義・block Gram 不足・PS-9 bridge 不成立)。**本節全体は失敗経路の記録(効力なし)** — 再設計 = §8.20 追記 + §8.21 HEAD9-ACTUAL)

**目的**: consult #17 の第 2 packet(crux)。frame_input-v2(T2b-0
`7103b2e` — 条件付き constructor)の defect 空間
V_n := span{変換後 4 原子} ⊂ ℱ に対し、**J⁹-rank-revealing frame** を建て、
出力を **frame_outcome-v2 := framed | overflow の型付き二択**で与える。
chart 別の消費表・一様 Gram 床・span の ord 上界は非主張(T2b-ii/T2c)。

**(H9-0) 設定**: gauge 後座標(T2b-0)で J⁹ := span{z^k : k ≤ 9} ⊂ ℱ
(Fock 単項式は直交 — P₉ = Taylor 級数の次数 ≤ 9 切断 = 直交射影 ✓)。
V_n = span{e^{q′_{j,n}} : j ≤ 4}(変換後原子 — transformed_atom_table、
全原子 K_{δ_ℱ,R_ℱ} 所属(T2b-0 evidence)、step-0 安定化済みで相異なる)。
  **α_n := inf{‖P₉v‖_ℱ : v ∈ V_n, ‖v‖_ℱ = 1}**
(= P₉|_{V_n} の最小特異値 — 基底不変。多者従属・rank drop を一括検出)。

**(H9-1) 有限 n での単射性(GC-1 の消費)**: v ∈ V_n ∖ {0} が P₉v = 0 を
満たすと、v は非零 4 原子指数和で ord₀(v) ≥ 10 — **GC-1 W_c(4)**
(ord ≤ D_W(4) = 9、任意中心 — accepted `957b252`)に矛盾。よって
P₉|_{V_n} は単射で **α_n > 0(各 n)** ✓。

**(H9-2) 二択(部分列安定化)**: α_n ∈ (0, 1] の部分列極限で
  **(framed) liminf α_n =: ε > 0** / **(overflow) α_n → 0**
のちょうど一方が成立(compact — [0, 1] の部分列収束)。以下 framed 枝で
frame を構成し、overflow 枝は (H9-5) の witness を出力する。

**(H9-3) framed 枝の frame 構成(graph operator — 独立性の組合せ論証を
消去)**: W_n := P₉V_n ⊂ J⁹ は 4 次元(単射性)。J⁹ は **10 次元** なので
W_n の正規直交基底 p_{ℓ,n}(ℓ ≤ 4)は部分列で p_{ℓ,n} → p_{ℓ,*} に収束
(有限次元 compact ✓ — Grassmann 極限も 4 次元: 正規直交性の極限保存)。
持上げ
  **w_{ℓ,n} := (P₉|_{V_n})⁻¹p_{ℓ,n} = p_{ℓ,n} + A_n p_{ℓ,n}**、
  A_n := (I − P₉)(P₉|_{V_n})⁻¹(graph operator、rank ≤ 4、
  ‖A_n‖ ≤ ‖(P₉|_{V_n})⁻¹‖ ≤ 1/α_n ≤ 2/ε(十分先))
とすると {w_{ℓ,n}} は V_n の基底で、**Gram G_n = I + (A_np_ℓ, A_np_{ℓ'})
≥ I**(unnormalized — 下界が構成から自動)✓。strong 収束は (H9-4)。

**(H9-4) tail-tightness 補題(本 packet の実質)**: 主張 — framed 枝
(α_n ≥ ε/2)の chart 列上、‖v_n‖_ℱ ≤ M の任意の v_n ∈ V_n は
**一様 tail 減衰** Σ_{k>K}|⟨v_n, z^k⟩|²/‖z^k‖² ≤ τ(K) → 0(K → ∞、
τ は box・M のみ依存)を持つ。従って {A_np_{ℓ,n}} は相対 compact で、
部分列により **w_{ℓ,n} → w_{ℓ,*} ℱ-strong、G_* ≥ I、極限 span は 4 次元**。
証明:
- **(i) 分離 cluster の角度下界**: 原子を atlas cluster(d_frame 極限 > 0
  の対は別 cluster)で分け v = Σ_c v_c(cluster 部分)と書く。相異 cluster
  の正規化原子対の Gram は、pairwise d_frame ≥ d₀ > 0 の **compact 配置
  集合上で連続かつ < 1** — compactness で一様 < 1 − c(d₀)。よって
  cluster 分解は有界: ‖v_c‖ ≤ C(d₀)‖v‖(有限次元 frame の角度論法)。
- **(ii) cluster 内の定数係数化**: cluster c 内は ΔA → 0(d_frame → 0 は
  |ΔA|^{1/2} → 0 を含む)。cluster 代表の A_c で
  u_c := e^{−A_c z²} v_c と置くと(乗算作用素 e^{±A_cz²} は
  |2A_c| ≤ 1 − δ_ℱ により **δ_ℱ margin 付きの weighted Fock 間で有界** —
  tail 減衰は margin を消費して両方向に移送可能)、u_c は
  **線形指数 e^{μ_j z} + 小二次補正**(|補正指数| ≤ |ΔA| → 0)の ≤ 4 項和。
- **(iii) 係数 recurrence(annihilator ODE)**: 補正なしの主部は定数係数
  作用素 **L_c := Π_j(D − μ_j)**(可換 — 係数 = μ の基本対称式、box 有界)
  で消える: L_c u_c = E_c u_c(E_c = 二次補正から生じる摂動項 —
  係数 O(|ΔA|)·(z·低階))。Taylor 係数(Fock 正規化 â_k := a_k√(k!))への
  recurrence は、k ≥ K₀(box) で
    |â_{k+4}| ≤ (C_box/√k)·max(|â_k|, …, |â_{k+3}|)
  の形(D は次数を 1 下げ z 乗算は √k 重み — 主部・摂動とも同型で摂動は
  さらに |ΔA| 小)⟹ 窓 max が幾何減衰 ⟹ **‖v_c‖ ≤ C‖v‖ のみに依存する
  一様 tail 減衰**(係数 b_j の大きさに依存しない — v_c が ODE の解空間に
  属す事実だけを使う)✓。
- **(iv) 合成**: (i) の有界分解 + (iii) の cluster 別 tail + (ii) の margin
  移送で v の一様 tail。相対 compact 性(有界 + 一様 tail = ℱ で
  precompact)から strong 収束部分列 ✓。G_n → G_* ≥ I(内積の strong
  連続)、極限 span 次元 = 4(G_* ≥ I ⟹ 独立)∎。
**J⁹ の中心規約**: P₉ は gauge 後の原点中心 — moving-center 版は T2c が
(B22-3) 型 RKHS 連続性(J⁹ 汎関数の norm 連続・compact 一様有界 —
(B3-4) 末尾と同文)で消費する(本 packet は原点中心の二択のみ)。

**(H9-5) overflow witness(no-go への bridge — 循環なし)**: α_n → 0 の
枝では単位ベクトル v_n ∈ V_n(‖v_n‖ = 1、‖P₉v_n‖ = α_n → 0)を取り、
  `overflow_witness := (v_n の exact 係数列(原子基底)、gauge 後中心と
   元 moving center の対応(T2b-0 の U_n record)、‖P₉v_n‖ → 0 の記録、
   潰れる床の特定(T2c の σ₀ 型 jet 床 — J⁹ 質量消滅はその定数 → 0 と
   同値)、PS-9 detected(evidence ref) への変換証明(J⁹ 質量消滅 =
   「指数 9 でも定数が 0 へ落ちる列」(§8.15 追記の no-go 基準)の witness
   化 — 変換は同一対象の記録形式の書換えのみで数学的内容は同一))`
**消費規則(循環の切断 — consult #17)**: framed のみ T2c の床が消費する。
overflow は frame を消費せず **§4 go/no-go 判定へ送付**(T2c で overflow の
空性を証明することはしない — それは循環。overflow が実在すれば PBK22 の
正式 no-go outcome)。**出力**:
  `frame_outcome-v2 := framed(frame_witness-v2) | overflow
   (overflow_witness)`
  `frame_witness-v2 := (frame_input-v2 参照, {p_{ℓ,*}}, {w_{ℓ,n}} の
   strong 収束記録, G_* ≥ I witness, 極限 span 生成元(型付き — 各
   w_{ℓ,*} = p_{ℓ,*} + (I−P₉) 成分), tail-tightness record(K₀, τ),
   α 下界 ref)` — fail-closed。

**scope(非主張)**: chart 別の exact span 消費表・一様 Gram 床(subchart
分割込み — T2b-ii)、span の ord/projective order 上界・moving-center 床・
量的連鎖(T2c)、overflow の空性(主張しない — 二択の型のみ)、有効定数、
人間による査読は未実施。

**§8.20 追記(2026-08-22 — 撤回と再設計、consult #18)**: R-T2BI R1 の
blocking 5(核心 = tail-tightness の recurrence が二次補正で破れる —
u = e^{ηz²/1} 型で â の減衰は 1/√k 型でなく幾何比型・摂動扱いは |ΔA|√k
非有界で不可)を受けた consult #18(Sol、`sol-t2bi-consult.md`)の裁定:
- **主張の弱体化が正道**: PTN-22 が消費するのは実 defect の jet 床と
  carrier 床であり、「4 次元 defect span 全体の strong compactness」は
  消費されない過剰目標 — critical path から外す(full-span 定理は将来の
  一般 FR4 資産として独立可)。
- **再設計 = 実 defect 限定の weak compactness**: f_n(実 defect、単位
  norm)と moving center ζ_n に対し **β_n := ‖J⁹_{ζ_n}f_n‖** を正本とし、
  head_good(liminf β ≥ ε — weak 極限 f_* ≠ 0、ord_{ζ_*} ≤ 9、compact-open
  収束で T2c の有限窓比較に十分)| head_overflow(typed candidate)の
  二択。撤回対象: 4 次元 limit span / defect Gram floor / graph operator
  precompactness / 全 v ∈ V_n の tail-tightness。
- **full-span を維持する場合の正道**(不採用 — 参考記録): J⁹-relative
  confluent secant compactification(configuration × secant plane の graph
  closure + collision blow-up + 一般化差分商列 + 強 weighted Fock の
  compact embedding)。heat relation 2∂_AΦ = ∂_B²Φ により単純な Hilb⁴ では
  jet image が rank drop するため追加 blow-up が必要。Wronskian ODE 正規化
  単独は衝突面の pivot 交代・次数落ちで一様化不能。
- **PS-9 bridge は独立 packet**(T2c-ov OVERFLOW-PS9-BRIDGE — T2c 後・
  T3 前): α/β の jet witness は PS-9 detected の要求(raw pair・window・
  zf・実二窓比の定数崩壊)と同値でない。実 defect 化 + 変換証明で
  detected | not_proven を返し、閉じなければ unresolved_head_overflow で
  止める(detected の勝手な生成禁止)。
- **係数規約の正本**: q(A, B; z) = (A/2)z² + Bz(Fock 可容 |A| < 1、
  (B3-4a) の ν = (ΔB, ΔA/2) と整合)。§8.20 撤回稿の e^{−A_cz²} は係数 2
  の誤り。e^{Az²/2} の Fock 係数幾何率は √|A|。weighted Fock ℱ_γ
  (‖f‖²_γ = Σ|a_k|²k!γ^{−k}、γ_s < γ_t で compact embedding、
  e^{Cz²/2}: ℱ_{γ_s} → ℱ_{γ_t}(γ_t ≥ γ_s + |C|)有界)は補助道具。
- **packet 再編**: T2b-i HEAD9-ACTUAL(2–3R)/ T2b-ii CARRIER-CHART
  (2–3R — defect 側義務を削除し carrier 完結 + 半箱供給)/ T2c FLOOR
  (3–5R — head_good のみ消費)/ **T2c-ov OVERFLOW-PS9-BRIDGE(2–4R —
  新設)**。合計 8–13 round 見込み。

### 8.21 GC-5-T2b-i HEAD9-ACTUAL(実 defect の moving-center J⁹ 二択 — **accepted、R-T2BIA R1 PASS、fixed SHA `e5de2f6`**)

**目的**: consult #18 の再設計。対象は **実 defect のみ** —
  f_n := (C_{1,n} + C_{2,n})/δ_n
(frame_input-v2.1([R-T2BII R1-02] で v2 から置換 — §8.22 (CC-5)。T2b-0 `7103b2e` の条件は同補題で充足)の変換後原子
から exact に構成、‖f_n‖_ℱ = 1、δ_n > 0(exact QR は atlas が exit 済み)。
f_n ∈ V_n は **finite-n exact membership** としてのみ記録する)。full-span
(V_n 単位球全体)の strong compactness・4 次元 limit span・defect Gram
床は**非目標**(§8.20 追記 — PTN-22 が消費しない)。

**(HA-1) 正本量**: 中心列 ζ_n ∈ D̄(t₀, R_col)(T2c の chain が供給する
moving center — window_geometry の compact 中心域)に対し
  **β_n := ‖J⁹_{ζ_n} f_n‖**
(J⁹_ζ := 0..9 階微分評価汎関数 vector。Fock 再生核の正則性により ζ ↦
J⁹_ζ は norm 連続・compact 中心域で一様有界 — (B3-4) 末尾の RKHS 規約と
同文、上界 C_R)。β_n ∈ [0, C_R]。

**(HA-2) 二択(部分列)**: 部分列上で
  **head_good: liminf β_n =: ε > 0** / **head_overflow: β_n → 0**
のちょうど一方(compact — [0, C_R])。ε は列ごとの存在のみ(chart 一様
下界は T2c の義務 — 本 packet は sequence 形)。

**(HA-3) head_good 枝(weak/compact-open 極限)**: ℱ の閉単位球は weak
compact — 部分列で f_n ⇀ f_*(weak)、ζ_n → ζ_*。J⁹ 評価汎関数は有限個の
norm 連続汎関数なので weak 収束と中心収束の合成で
  **J⁹_{ζ_n}f_n → J⁹_{ζ_*}f_***
(|⟨f_n, K_{ζ_n}^{(k)}⟩ − ⟨f_*, K_{ζ_*}^{(k)}⟩| ≤ |⟨f_n − f_*,
K_{ζ_*}^{(k)}⟩| + ‖f_n‖·‖K_{ζ_n}^{(k)} − K_{ζ_*}^{(k)}‖ → 0 — 第 1 項は
weak 収束、第 2 項は核の norm 連続性)。よって ‖J⁹_{ζ_*}f_*‖ ≥ ε > 0 ⟹
**f_* ≢ 0 かつ ord_{ζ_*}(f_*) ≤ 9** ✓。さらに単位球の weak 収束は、再生核
の局所一様有界性(compact 集合上 sup|f_n(z)| ≤ C_K)と正規族論法により
**compact-open 収束(全階導関数の内部一様収束込み)**へ移る — T2c の
有限窓上の jet/Taylor 比較にはこれで十分(norm 1 の strong 極限・span
所属は不要 — consult #18)✓。

**(HA-4) head_overflow 枝(typed candidate — 橋は別 packet)**:
  `head_overflow_candidate := (frame_input-v2.1 ref([R-T2BII R1-02] で
   v2 から置換)(実 raw defect の provenance — minimizer 実現問題は生じ
   ない: f_n 自体が raw pair 由来),
   ζ_n 列 ref, β_n → 0 の記録, weak 極限の記録(f_* = 0 か否かを含む))`
— **PS-9 detected はここでは生成しない**(jet witness と PTN-22 定数崩壊
の同値は未証明 — 変換は GC-5-T2c-ov の義務。橋が閉じるまで
`unresolved_head_overflow` で止まる — fail-closed)。

**(HA-5) 係数規約(正本化)**: q(A, B; z) = (A/2)z² + Bz、Fock 可容
|A| < 1(chart 箱は |A| ≤ 1 − δ_ℱ)。(B3-4a) の ν = (ΔB, ΔA/2)・T2b-0 の
d_frame/t と整合。weighted Fock ℱ_γ の型(§8.20 追記)は**登録のみ**
(本 packet では消費しない)。

**(HA-6) 出力契約**: `head_outcome-v1 := head_good(good_witness) |
head_overflow(head_overflow_candidate)`(branch constructor — (PS-9)
方式)、
  `good_witness := (frame_input-v2.1 ref([R-T2BII R1-02] で v2 から置換), ζ 列 ref, ε 下界 ref(列ごとの
   存在のみ), weak/compact-open 極限記録, ord_{ζ_*} ≤ 9 の記録)`
— fail-closed(field 欠落 = witness 不成立)。**T2c は head_good のみ
消費**(head_overflow は T2c-ov へ — 循環なし)。∎

**scope(非主張)**: full-span strong compactness・limit span・defect
Gram(非目標 — §8.20 追記)、carrier frame・半箱供給(T2b-ii)、chart
一様 jet 床・jet-to-window 定量鎖・projective order・carrier 床(T2c)、
overflow → PS-9 bridge(T2c-ov)、有効定数、人間による査読は未実施。

### 8.22 GC-5-T2b-ii CARRIER-CHART(carrier 側の完結と箱供給 — **accepted、R-T2BII R3 PASS、fixed SHA `ccb1b6d`**)

**目的**: consult #18 再編の第 3 packet。**carrier 側を完結**させる:
成分別 strong frame、⊕ block 対角 Gram の chart 一様床、**T2b-0 の箱前提の
供給(obligation 解消)**、中心・scale mapping。defect 側は T2b-i
(head_outcome-v1、`e5de2f6`)が既に閉じており本 packet は関与しない。

**(CC-1) 成分直交(再掲・消費)**: ℱ⊕ℱ で ⟨(u, 0), (0, v)⟩_⊕ = 0 —
carrier の joint Gram は **G_⊕ = diag(G₁, G₂) の block 対角**(§8.18
(B22-1) の存置部分を本 packet が正式に消費 — cross-child 項は carrier 側に
現れない)。

**(CC-2) 成分別 frame**: 各成分 C_{i,n}(step-0 安定化後 m_i ∈ {1, 2}
原子)に対し:
- **m_i = 1**: 正規化単原子 — chart 箱で ℱ-norm 連続、strong 収束
  (パラメタ収束 ⟹ 原子の ℱ-連続性 — (B3-3) の box 束縛と同文)。
  G_i = 1。
- **m_i = 2・分離**(within-child 合流 flag なし): 対距離下界 d₀ > 0 の
  閉 chart 上、正規化 2 原子の Gram は連続で対角外 |⟨φ_a, φ_b⟩| < 1 —
  compact 上一様 < 1 − c(d₀) ⟹ **G_i 一様可逆**。strong 収束は原子の
  ℱ-連続性から ✓。
- **m_i = 2・合流**: **(B3-4a) の 2 原子 Newton frame をそのまま消費**
  (accepted `87863cc` — 積分表示、ℱ-strong 極限 {e^{q*}, L_{ν̂*}e^{q*}}、
  L_{ν̂*} ≢ 0 非定数 ⟹ 極限独立。除数 t は T2b-0 node_scale_bridge の
  t_increment と同一物 — 座標整合は T2b-0 R2-02 で確定済み)。
極限独立 ⟹ G_{i,*} > 0(各境界点)。

**(CC-3) chart 一様 Gram 床(compact chart constructor 込み
[R-T2BII R1-01])**: carrier chart の **constructor を型で固定**する。
成分 i ごとに 2 型:
  `SEP_i(d₀) := {成分 i の 2 原子対: 変換後対距離 d_frame ≥ d₀、パラメタ
   ∈ K_{δ_ℱ²/2, C_B}((CC-5) の箱)}`(閉 — 距離下界・閉箱の共通部分)、
  `CONF_i(d₀) := {同: d_frame ≤ 2d₀、正規化方向 (t, ν̂) ∈ [0, t₀] × S³ に
   compact 化((B3-4a) の座標)}`(閉)
(m_i = 1 は単原子 chart — 閉箱のみ)。**d₀ は t₀/√5 以下に取る**
(bridge t ≤ (√5/2)d_frame と d_frame ≤ 2d₀ から t ≤ √5·d₀ ≤ t₀ —
CONF の (B3-4a) 適用域 t ≤ t₀ が帯全体で保証される [R-T2BII R2-01])。
帯 d_frame ∈ [d₀, 2d₀] は両 chart が重複被覆する(どちらの
frame も有効: SEP は d ≥ d₀ の一様 Gram、CONF は t ≤ t₀ の Newton frame —
境界遷移は被覆重複で処理し、単一 chart 内の frame 切替は行わない)。
K_χ(c₀) := (成分別 chart 型の積)×(係数単位球の閉部分集合
{|c_a| ≥ c₀ ∀a})— **c₀ > 0 ごとに閉 compact の有限積 ✓**
([R-T2BII R2-02] — 係数消滅面を「除外」するのでなく、**閉集合族
{K_χ(c₀)}_{c₀>0} で覆う**: atlas chart 枝(係数退化 flag = false)の部分列
は正規化係数の極限が非零なので liminf|c_a| > 0 — **c₀ witness**(有理
下界 ref)を chart 割当 record に持ち、当該列は十分先で K_χ(c₀) に入る。
rank-drop 極限列(flag = true)は atlas (AT-2) 行 1 が (i) へ exit 済みで
本 packet の定義域に入らない — 「境界で frame 次元が変わる」case は
どの K_χ(c₀) にも現れない ✓)。**support rank 一定**: chart 枝の部分列
では step-0 安定化で各 n の原子数が固定 ✓。以上で consult #17
§5 の (a)(b) が実体化し、(c) frame map の ℱ-norm 連続 / strong 収束
((CC-2))、(d) 全境界点の極限独立((CC-2))、(e) strong section
(T2b-0)と併せ、x ↦ λ_min G_⊕(x) は下半連続 — compact 上の inf が各点
正値から **inf_{K_χ(c₀)} λ_min G_⊕ > 0**(c₀ ごとの chart 定数 — 有効値
非主張。背理法
版: λ_min → 0 の列 → strong frame 収束で G → G_* > 0 と矛盾 — (B3-4) の
Gram 鎖と同文)✓。**carrier に overflow locus は存在しない**(成分 ≤ 2
原子で全境界点の frame が strong に閉じ独立 — defect 側の α/β の様な
質量逃避機構が生じない。consult #17 §5 の「α ≥ ε_χ subchart 分割」は
carrier には不要)。

**(CC-4) carrier strong 極限と成分消滅 flag**: ‖𝐂_n‖_⊕ = 1 と (CC-3) の
Gram 床 ⟹ 係数有界 ⟹ 部分列で **𝐂_n → 𝐂_* strong、‖𝐂_*‖_⊕ = 1**。
成分消滅 flag(‖C_{i,*}‖ = 0 の側)は部分列で安定し、atlas の outer
routing([1:0]/[0:1])と整合(消滅側の g への影響の解析は T2c の分母床の
義務 — 本 packet は flag の安定化のみ)。

**(CC-5) 箱供給補題(T2b-0 obligation の解消 — Möbius margin)**:
T2b-0(`7103b2e`)の半箱前提(|A_j| ≤ (1−δ_ℱ)/2)は**不要に強い**。
正しくは: raw 標準箱 **|A_j| ≤ 1 − δ_ℱ、|B_j| ≤ R_ℱ**((B3-1)/§8.9 追記
の standing 束縛)から、pivot の metaplectic 正規化(squeeze で
A_pivot → 0、Weyl で B_pivot → 0 — FR §8.4 の normal form 化)後の
変換後係数が
  **1 − |A′_j| ≥ (1 − |A_j|)(1 − |A_p|)/(1 + |A_j||A_p|) ≥ δ_ℱ²/2**
(disk の Möbius 縮小率 — 初等: squeeze の A への作用は単位円板の Möbius
変換 A ↦ (A − A_p)/(1 − Ā_pA)、|A′| ≤ (|A| + |A_p|)/(1 + |A||A_p|) と
1 − その右辺 = (1−|A|)(1−|A_p|)/(1+|A||A_p|))、
**|B′_j| ≤ C_B := R_ℱ/Δ + 2R_ℱ/√Δ**(Δ := δ_ℱ(2 − δ_ℱ) — FR G8-b/c の
squeeze/Weyl 作用式からの明示 bound [R-T2BII R1-02]: squeeze の分母
1 − |A_p|² ≥ Δ と Weyl 混合項の √ 重み)を満たす — すなわち**変換後 4
原子は K_{δ_ℱ²/2, C_B} に属す**(Fock-admissible ✓)。
**versioned 置換(完全型 — GCRouteRecord v3→v4 前例と同方式
[R-T2BII R1-02])**:
  `frame_input-v2.1 := (atlas_witness-v1 参照(chart 枝),
   chart_sublabel((AD22-3)), common_gauge_record-v1.1)`
  `common_gauge_record-v1.1 := common_gauge_record-v1 の
   half_box_premise field を
   standard_box_premise(検証規則: record 生成時に各原子の
   |A_j| ≤ 1 − δ_ℱ、|B_j| ≤ R_ℱ を verified — evidence = (B3-1)/§8.9
   追記の standing 束縛 ref)+ box_supply_ref(本 (CC-5) 補題)で置換した
   もの — **他 field(pivot_leaf・section_id・U_n・scalar 吸収表・変換後
   原子表・**section_param_bound_ref**(T2b-0 の section 消費条件 —
   [R-T2BII R2-03] で列挙に明示)・all_atoms_in_K・strong_section・
   root_scale_limit・node_scale_bridge)はすべて不変(型不変条件)**`
(v2 定義本文は不変 — 下流の正本は v2.1。**consumer の完全置換**: §8.21
(HA-1)/(HA-6) と本 §8.22 の frame_input-v2 参照は v2.1 に置換
[R-T2BII R1-02 — reviewer 指示による versioned 置換、[R-GC4A5A0 R3-01]
前例]。T2b-0 の条件付き constructor の条件は standard box(standing
束縛)+ 本補題で充足される — obligation 解消)。

**(CC-6) raw 再主張系(pointwise gauge 移送の禁止 — EW-B 準拠
[R-T2BII R1-03])**: gauge unitary は pointwise growth を保存しないため、
**空間座標の対応写像は定義しない**(旧 center_scale_map 案は撤回 —
FR §8.4 が与えるのは (A, B) パラメタ作用と Fock unitary であり座標 affine
map ではない)。代わりに **raw 再主張**で接続する:
- **(CC-6a) defect の raw 系**: §8.21 (HA-1)–(HA-3) の論証は f の
  provenance(原子構造・箱・gauge)を一切使わない(単位 norm・weak
  compact・核 norm 連続のみ)。よって **raw defect
  f_n^{raw} := (B̃₁ + B̃₂)/‖B̃₁ + B̃₂‖_ℱ と raw 中心 ζ_n ∈ D̄(t₀, R_col)
  に対しても同文で成立**(本 packet が系として主張 — 証明は (HA-3) の
  逐語適用。**T2c はこの raw 版のみを消費**し、gauge 後版との pointwise
  同一視は行わない)。
- **(CC-6b) carrier frame の raw 引き戻し**: (CC-2) の frame は gauge 後
  空間で構成されるが、strong section U_n → U_*((AD22-2))により
  **w^{raw}_{ℓ,n} := U_n^{-1}w_{ℓ,n} は raw 空間で ℱ-strong 収束し、Gram
  は unitary 不変で (CC-3) の床がそのまま移る**((B3-4) の
  w = U^{-1}v 鎖 [GCBORD3R5-02] と同文 — pointwise 移送は不要、strong
  収束と Gram のみを運ぶ)。
- 型: `raw_restatement := (raw defect 定義 ref, (CC-6a) 系 ref,
  引き戻し frame 記録((CC-6b)), 検証: 「T2c の全消費は raw 座標」flag)`
(暗黙換算の禁止 — R-GC4A5A R1 finding 6 の系譜)。

**(CC-7) 出力契約(typed constructor — [R-T2BII R1-04])**:
`carrier_witness-v1 := (frame_input-v2.1 ref,
 成分別 frame 記録(m_i・chart 型(SEP/CONF/単原子)・strong 収束 ref),
 floor_checked(chart ref, (CC-3) の下半連続 inf 論証 ref — evidence なし
 では構成不能),
 vanish_flag := **none(evidence: 両成分の norm 極限が正である検証 ref +
 atlas outer routing 不在の検証)**| one_sided(side ∈ {[1:0], [0:1]},
 evidence: 消滅側成分の norm 極限 ref + **atlas outer routing との一致
 検証**(不一致 = 構成不能))— 全 variant が checked
 [R-T2BII R2-04],
 raw_restatement((CC-6) — 検証 flag 込み))`
— fail-closed は **checked constructor 方式**(evidence 引数なしの
constructor は型に存在しない — (PS-9) 方式)。**T2c の消費 branch を型で
明示**: T2c は (head_outcome-v1 = head_good) × (carrier_witness-v1 の
raw_restatement 検証済み)の対のみを消費する(head_overflow × 任意は
T2c-ov へ)。〔[R-T2C R7-01] reviewer 指示による追記(in-place、前例
[R-T2BII R1-02]): T2c の消費はさらに **floor_input-v1(§8.23)経由で
vanish_flag = none に限定** — one_sided variant の routing は T3 の明示
義務(§8.23 消費契約)。〕∎

**scope(非主張)**: 分母床 m_C の値と一様性・jet-to-window 定量鎖・
projective order(T2c)、overflow bridge(T2c-ov)、有効定数、人間による
査読は未実施。

### 8.23 GC-5-T2c BORD22-FLOOR(chart 床・量的連鎖・projective order — **accepted、R-T2C R8 受理 SHA `15b272e`**)

**目的**: consult #18 再編の最終 proof packet。head_outcome-v1(T2b-i
`e5de2f6` — (CC-6a) の raw 版)と carrier_witness-v1(T2b-ii `ccb1b6d`)を
消費し、chart ごとの **defect jet 床 σ₀ / carrier 床 m_C の存在(または
overflow candidate の構成)**、**projective order ν ≤ 9**、量的連鎖を張る。
本 packet の受理で **BORD-22(T2 chain)完成**。(PTN-22) の二窓 Remez
合成は T3、overflow → PS-9 bridge は T2c-ov(非主張)。

**入力バンドル型** [R-T2C R5-02]: 上流の accepted 型(atlas_witness-v1 /
frame_input-v2.1 / carrier_witness-v1)は c₀ を field として保持しない
ため、本 packet の chart 参照は次のバンドル型で行う(上流型は不変更 —
c₀ の evidence 実体は §8.22 (CC-3) の coefficient lower-bound c₀ witness
構成):
  **floor_input-v1 := (provenance := (θ 列 ref, ζ 列 ref, 部分列
  selector), atlas_witness-v1 ref(chart 枝), c₀ witness((CC-3) の
  K_χ(c₀) 族所属 evidence — 下界値 c₀ 込み), frame_input-v2.1 ref,
  carrier_witness-v1 ref(raw_restatement 検証済み、**vanish_flag = none
  限定** — one_sided variant は K_χ(c₀) の係数下界との両立が未証明のため
  本 packet の消費対象外で、one_sided pair の routing(lower-rank 面接近
  の atlas exit 等)は T3 の明示義務 [R-T2C R6-03]), head_outcome-v1 ref,
  **checked_same_provenance**(全 ref が同一 provenance — 同一 chart・
  同一 raw pair 列・同一 ζ 列・同一部分列 — から導出されたことの検証
  constructor [R-T2C R6-01]))`。
以下「chart ref(c₀ witness 込み)」はすべて floor_input-v1 への参照 —
FL22-3/FL22-4 の分子(jet 床)と分母(carrier 床)は
checked_same_provenance により**同一列で消費される**ことが型で保証される。

**(FL22-1) chart 別 defect jet 床の二択([R-T2C R1-01] で量化を型固定)**:
**量化の型**: `admissible pair := (θ 列(実 config — 各 θ_n は
t3_witness/window_geometry 持ち、atlas chart 枝 χ・c₀ witness 付き —
**枝が χ で一定の列(全要素が χ witness を持つ)**), ζ 列(compact
中心域 D̄(t₀, R_col) 内))`。**c₀ は量化の固定パラメータ** [R-T2C
R4-02]: admissible pair は **c₀ witness が固定値 c₀ 以上のもの**に限る
(σ₀(χ, c₀)・m_C(χ, c₀, ρ) は (χ, c₀) ごとの主張 — これで両対角列は
threshold 以降**単一の compact K_χ(c₀) 内**に留まり、(CC-3) の閉性・
Gram 床・strong compactness が適用可能。pair ごとに c₀^{(k)} → 0 となる
列は本量化の対象外 — その routing は消費契約の violation_sequence 型で
T3 義務として扱う)。**inf は chart
点(閉包点)ではなく admissible pair 全体を走る** — 閉包の非実現点
(t = 0 面等)は量化に現れない(稠密性論法は不要):
  **σ₀(χ, c₀) := inf{liminf_n β_n^{raw}(θ, ζ) : admissible pair}**。
二択:
- **σ₀ > 0(床成立)**: chart 定数として登録(有効値非主張)。
- **σ₀ = 0**: 各 k で liminf < 1/k の pair (θ^{(k)}, ζ^{(k)}) を取り、
  各々から β < 1/k を実現する添字を選ぶ**対角列**(θ^{(k)}_{n_k},
  ζ^{(k)}_{n_k})を作る — **添字は各 pair の K_χ(c₀) 所属 eventual
  threshold N^{(k)}((CC-3) の「十分先で K_χ(c₀)」)より後から選ぶ**:
  liminf < 1/k は「β < 1/k を実現する添字が無限個ある」ことなので
  N^{(k)} 以降にも必ず存在する [R-T2C R3-03] — 対角列は**実 config の admissible T3 列**
  (各要素が実 config — 元 pair の要素だから)で β → 0。**全要素が χ 枝の
  実現 config**(量化が χ の admissible pair に限られ、枝は構成上一定 —
  **atlas 再通過は不要**で lower-rank / exact-QR への exit は起こり得ない
  [R-T2C R2-05])。したがって各要素の χ atlas witness・c₀/box data が
  **frame_input-v2.1 の型をそのまま満たし**、T2b-i の **head_overflow 枝の
  実現**として head_overflow_candidate を χ 内で構成、T2c-ov へ送付(**本 packet はここで
  停止し床を主張しない** — fail-closed。overflow の空性証明はしない、
  consult #18 の循環切断)。
以下 (FL22-2)–(FL22-5) は σ₀ > 0 の chart(または head_good 部分列)上の
主張。

**(FL22-2) carrier 床 m_C(raw 側・ρ-erosion core + 移動円板 Hurwitz
[R-T2C R1-02][R1-03][R2-01][R2-02])**: 対象は **raw 正規化 pair
𝐁̂_n := 𝐁̃_n/‖𝐁̃_n‖_⊕**(gauge 側 𝐂_* への (AT-3) 適用はしない — EW-B)。

**(a) core の定義(ρ-erosion)**: pair の各 n と ρ > 0 に対し。m_C の
量化域は型で固定する [R-T2C R6-02][R7-02]:
  **admissible_pair_ρ := admissible pair((FL22-1) の型 — χ 枝一定・
  c₀ 固定)+ eventual ρ ≤ r_{S,n} evidence(十分先で ρ ≤ r_{S,n})**
— r_S は window witness の pair ごとの量なので共通下界は仮定せず、
eventual 条件を型の field として束縛する。(b) の margin min(ρ, r_{S,n})
= ρ は threshold 以降で成立
  **W_core,n(ρ) := closure{t ∈ W_reg,n : dist(t, ⋃_c U_{c,n} ∪ Σ_n) ≥ ρ}**
— W̄ 内の有界閉集合なので **compact、min は達成される**(W の左閉右開
規約は closure で処理 — 追加される極限点も dist ≥ ρ を保つ [R-T2C
R2-02])。空なら min := +∞(当該 n は寄与しない)。**core の非空性と
帯域 W_reg ∖ W_core(ρ) の処理(bubble 近傍 routing)は T3 の hop 幾何の
義務**として witness に記録(本 packet は ρ ごとの床のみ主張)。

**(b) 点ごとの円板 zero-freeness**: t ∈ W_core,n(ρ) と B̂_{i,n} の任意の
零点 z_j について、(AT-3) の checked_zero_free membership より
Re z_j ∈ ⋃_c U_{c,n} ∪ Σ_n(W-relevant — **U_c membership しか与えないが
t の側が集合 ⋃U ∪ Σ から距離 ≥ ρ にいる**ので十分 [R-T2C R2-01])または
dist(Re z_j, W) ≥ r_S(非 W-relevant)。いずれでも
  **|z_j − t| ≥ |Re z_j − t| ≥ min(ρ, r_{S,n}) = ρ**(threshold 以降
  [R-T2C R6-02])
— 実部距離が複素距離の下界(Im 方向は無条件)なので、**B̂_{i,n} は複素
円板 D(t, ρ) 上 zero-free**。

**(c) sequence-inf と移動円板矛盾論法**:
  **m_C(χ, c₀, ρ) := inf{liminf_n min_{W_core,n(ρ)} max_i|B̂_{i,n}| :
  admissible_pair_ρ}**([R-T2C R7-02] — 量化は evidence 付き pair のみ。
  evidence を持たない pair は m_C の量化外で、その消費は T3 の routing
  義務)。
これが 0 と仮定する。対角列(実 config — 全要素 χ 枝、atlas 再通過不要。
**添字は各 pair の K_χ(c₀) 所属 threshold 以降から選ぶ** — liminf の低値
実現添字は無限個あるので threshold 後にも選べる [R-T2C R3-03])で min
達成点 t_m ∈ W_core,m(ρ) を取り max_i|B̂_{i,m}(t_m)| → 0。**raw
strong 極限**: (CC-6b) の引き戻し frame の raw ℱ-strong 収束と Gram 床は
K_χ(c₀) 所属の**要素ごと一様性質**なので対角列にそのまま適用でき、部分列
で 𝐁̂_m → 𝐁̂_* strong(‖𝐁̂_*‖_⊕ = 1)、t_m → t_*(W̄ compact)。十分先で
D(t_*, ρ/2) ⊂ D(t_m, ρ) なので各 B̂_{i,m} は**固定円板 D(t_*, ρ/2) 上
zero-free**、strong ⟹ 局所一様収束(RKHS)⟹ **Hurwitz**: 各成分極限は
D(t_*, ρ/2) 上 zero-free か恒等零。両成分は t_* で消える(max → 0 の
極限値)から zero-free 側は不可能 ⟹ 両成分とも円板上恒等零 ⟹ entire 関数
の一致定理で全平面恒等零 ⟹ ‖𝐁̂_*‖_⊕ = 0 ≠ 1 **矛盾** ⟹
**m_C(χ, c₀, ρ) > 0**(各 ρ で・無条件 — carrier に overflow 機構がない
ため二択不要 ✓。可変 W_reg,n 上の Hurwitz や固定領域の下半連続は不使用
[R-T2C R2-02])。上界 M_C は box の RKHS 評価(sup ≤ C_R‖·‖_ℱ)から ✓。

**(FL22-3) 量的連鎖(raw 座標・eventual 形 [R-T2C R1-04])**: σ₀ > 0 の
chart 上、任意の admissible pair は liminf β_n ≥ σ₀ を満たすので、
**十分大きい n で**
  **‖J⁹f_n^{raw}(ζ_n)‖ = β_n ≥ σ₀/2 ≥ (σ₀/(2C_R))・sup_{D̄(t₀,R_out)}
  |f_n^{raw}|**
(消費可能な床は σ₀/2 — 「全 n で ≥ σ₀」は liminf からは出ない(反例
β_n = σ₀ − 1/n)。eventual 形は T3 の対偶/chain 消費に十分)。
**g への正確な接続(δ の消去)**: 恒等式
  **g_n(t) = δ_n・|f_n^{raw}(t)| / max_i|B̂_{i,n}(t)|**、
  δ_n := ‖B̃₁+B̃₂‖_ℱ/‖𝐁̃_n‖_⊕
(f^{raw} = (B̃₁+B̃₂)/‖B̃₁+B̃₂‖、B̂ = B̃/‖𝐁̃‖_⊕ — 全て raw)。δ_n は
**t に依らない共通因子**なので、二窓比 ‖g‖_W/‖g‖_S では**厳密に相殺**
する — T3 が消費するのは f^{raw} の jet 床(分子)と carrier 床(分母、
W_core(ρ) 上 — core 非空性と帯域 routing は T3 義務)のみで δ は現れない
✓。**carrier 床も eventual 形** [R-T2C R3-02]: m_C(ρ) は inf-liminf 型
なので pointwise には使えず、任意の admissible pair で liminf min ≥
m_C(ρ) から **十分大きい n で min_{W_core,n(ρ)} max_i|B̂_{i,n}| ≥
m_C(ρ)/2**(消費床は m_C(ρ)/2 — defect 側の σ₀/2 と同じ半減 eventual
規約。上界側は pointwise: max_i|B̂_{i,n}| ≤ C_R‖B̂_{i,n}‖_ℱ ≤ C_R =: M_C
は RKHS 評価で全 n 成立)。**hop 幾何(S, W, s)への接続は
T3 の義務**(本 packet は床の存在のみ)。

**(FL22-4) projective order ν ≤ 9(主張域 = W_core(ρ)、defect-order 形
[R-T2C R1-05][R2-04])**:
対象は **reduced pair 𝐁̃**((PS-1) — g の比較対象。raw 共通因子 D は
(F2²-4) で g から exact に消えており本節に現れない)。head_good 部分列の
弱極限 f_*((HA-3) raw 版 — f_* ≠ 0、ord_{ζ_*}(f_*) ≤ 9)と raw carrier
極限 𝐁̂_* に対し、**ν を defect order で直接定義**:
  **ν_{ζ_*} := ord_{ζ_*}(f_*) − min_i ord_{ζ_*}(B̂_{i,*})**。
**和の極限 F_* = lim(B̂_{1,n}+B̂_{2,n}) は経由しない** [R-T2C R2-04]:
B̂_{1,n}+B̂_{2,n} = δ_n·f_n^{raw}((FL22-3) の δ_n)で **δ_n の下界は
主張されず**、δ_n → 0 なら和の極限の ord は ord(f_*) と一致しない。
しかし T3 が消費する g の分子は (FL22-3) の恒等式で δ_n·|f^{raw}| —
**δ は二窓比で厳密相殺**するため、T3 に必要なのは f_* 側の ord(jet 床
経由)と carrier 側の ord のみで、**和の ord はどこにも使われない**。
**中心と core の型接続** [R-T2C R3-01]: ν の主張は **core-interior 中心
の pair(十分先で ζ_n ∈ W_core,n(ρ) が成立 — witness に記録)に限る**
(ζ 列の一般域は D̄(t₀,R_col) — core 外中心の pair は本 packet 非主張で、
bubble / collar 側 hop は T3 の routing 義務)。このとき (FL22-2)(b) より
各 B̂_{i,n} は D(ζ_n, ρ) 上 zero-free、ζ_n → ζ_* だから十分先で
D(ζ_*, ρ/2) ⊂ D(ζ_n, ρ) — 固定円板 D(ζ_*, ρ/2) 上で Hurwitz: 各成分極限
は**恒等零 or 円板上 zero-free**。両成分恒等零は ‖𝐁̂_*‖_⊕ = 1 に矛盾する
ので、非恒等零の成分は ζ_* で非零(floor input は **vanish_flag = none
限定** [R-T2C R6-03] — one_sided は消費対象外)⟹
**min_i ord_{ζ_*}(B̂_{i,*}) = 0** ⟹
**ν_{ζ_*} = ord_{ζ_*}(f_*) ≤ 9** ✓。**cluster U / CZB / Σ 域の中心は
本 packet の主張域外** — これらは (AT-3) 被覆により T3 の hop 幾何から
除外・移管され(W_reg + collar 側で Remez を張る)、bubble 内部の解析が
必要になる場合は T3 が (PS-5) inner chart を消費する(𝐁̃ の近接共通零点の
inner scaling・極限移送は (PS-2)/(PS-5) の型のまま — 本 packet 非主張
[R-T2C R1-05]: 旧稿の「還元」文言は撤回)。
**3+1 mixed-span valuation lemma(consult #17 obligation の解消)**:
HEAD9-ACTUAL 設計では ord ≤ 9 が (HA-3) で **chart 非依存に**出るため、
span 別 valuation は不要化された(obligation discharge)。記録として初等
証明も付す: v = P e^{p} + c e^{q}(deg P ≤ 5、q − p ≢ const)なら
(D − q′)v = (P′ + P·(p − q)′)e^{p} は(deg ≤ 6 多項式)× e^p なので
ord((D − q′)v) ≤ 6、微分は ord を高々 1 下げるので **ord(v) ≤ 7 ≤ 9** ✓。

**(FL22-5) 対偶と BORD-22 headline(chain 消費形)**: 任意の admissible
T3 列は、(AT)(atlas)により lower-rank / exact-QR exit または chart 枝に
入り、chart 枝では (FL22-1) の二択により
  **(good) jet 床 σ₀ + carrier 床 m_C + ν ≤ 9 が成立** /
  **(overflow) head_overflow_candidate が T2c-ov へ送付される**
のちょうど一方。対偶形(TN-3 型): 床成立 chart では「深く消える列」は
存在しない — **eventual 一様比較** [R-T2C R2-03]: 任意の admissible pair
で十分大きい n において ‖J⁹f_n(ζ_n)‖ ≥ (σ₀/(2C_R))・sup|f_n|((FL22-3)
の eventual 形 — 全 n の強形は主張しない)。∎
**消費契約(eventual → pointwise の橋の型)[R-T2C R3-04][R4-03]**:
(PS-7) の登録 interface は pointwise 二窓不等式で eventual 型を持たない
ため、floor_witness-v1 の消費は**列-矛盾 schema に型固定**し、schema の
入力を型で縛る:
  **violation_sequence-v1 := (floor_input-v1 ref(checked_same_
  provenance で本 θ/ζ 列に束縛 — carrier_witness.vanish_flag = none を
  継承 [R-T2C R7-01]), θ 列 ref(各要素の t3_witness・
  window_geometry・χ atlas witness — **wzf_cover.checked_zero_free
  evidence 込み**(FL22-2 の円板論法の入力)), ζ 列 ref(D̄(t₀, R_col)
  所属 evidence), chart 安定化 evidence(atlas chart 有限性による部分列
  抽出), 共通 c₀(固定 — 全要素の (CC-3) c₀ witness ≥ c₀), K_χ(c₀)
  eventual threshold, core 非空性 evidence(**同一 ρ・同一 threshold
  以降で eventual に成立**), core-interior 中心 flag(十分先で
  ζ_n ∈ W_core,n(ρ)), **ρ ≤ r_{S,n} eventual evidence** [R-T2C R6-02],
  **head_outcome = head_good(good_witness ref — f_* ≠ 0・ord ≤ 9)**
  (head_overflow 列には本 schema を付けられない — 型で排除 [R-T2C
  R5-03]), raw_restatement 検証 ref, **checked_same_provenance**
  (good_witness・raw_restatement・carrier witness が本 field の θ 列・
  ζ 列・同一部分列から導出されたことの検証 constructor [R-T2C R6-01]),
  違反度 → ∞ 記録)` [R-T2C R5-04]。
T3 は「(PTN-22) の一様定数が存在しない」と仮定して違反 config 列を抽出
し、**violation_sequence-v1 を構成できた場合に限り**違反列が (χ, c₀) の
admissible pair を成して eventual 床(β_n ≥ σ₀/2、min max ≥ m_C(ρ)/2)
が十分先で適用され、違反度 → ∞ と矛盾 — 矛盾法は tail のみを使うため
有限初期区間の吸収は schema に内蔵され、pointwise な (PS-7) 不等式は
「一様定数の存在」としてこの矛盾から導出される。**witness の各 field が
構成できない違反列(c₀^{(k)} → 0 / core 空 / 中心が core 外)の routing
は T3 の明示義務**(rank-drop 面接近は atlas exit 行・bubble/collar 側は
inner chart / hop 幾何 — 本 packet 非主張)。導出の実行は T3 の義務、
消費経路の型のみここで登録 [R-T2C R4-03]。
**出力契約**: `floor_witness-v1 := (chart ref(c₀ witness 込み),
 outcome := floored(σ₀ 存在 ref, m_C(ρ) 存在 ref(ρ 記録、量化 =
 admissible_pair_ρ [R-T2C R7-02]、core 非空性義務 = T3), M_C ref, ν ≤ 9 記録(defect-order 形、**core-interior 中心
 flag** [R-T2C R3-01]), 連鎖不等式記録(**defect・carrier 両側 eventual
 形 flag 付き**(σ₀/2、m_C(ρ)/2)、消費 = violation_sequence-v1 経由の
 列-矛盾 schema 限定 [R-T2C R3-04][R4-03]))| deferred(head_overflow_candidate ref —
 T2c-ov 送付記録)、raw_restatement 検証 flag((CC-6)))` — fail-closed
(branch constructor 方式)。T3 は floored のみ消費。

**scope(非主張)**: (PTN-22) の二窓 Remez 合成と C₂₂(T3)、overflow →
PS-9 detected の橋(T2c-ov)、overflow の空性、有効定数、COND9
reduction・A.5b/A.5c/A.6、人間による査読は未実施。

**追記(consult #19、Sol、2026-08-22 — T3 骨格裁定)**: 受理後の T3 着工
諮問に対する裁定。(i) **単一 T3 packet は却下** — T3a0 PTN-LOWER-FACE /
T3a PTN22-ROUTE / T3b PTN22-SCALE-HOP / T3c PTN22-REMEZ-CLOSE の 3+1
分割(§4 台帳)。(ii) **最危険点の更新**: T2c が固定 (χ,c₀,ρ) 内の床を
確保した結果、危険は境界パラメータへ移動 — 危険度順に (1) ρ/r_S・bubble
scale の縮退(s_n→0 で固定 ρ 不存在 — 主縮小 regime、T3b)、(2) c₀→0 の
lower-rank projective 境界(**BORD-3/TN-3 は PTN-22 の lower-rank 版では
ない** — 暗黙使用は完全な循環。support rank の well-founded induction +
rank ≤ 3 base 定理 T3a0 の先行受理で切断)、(3) core 空/Σ handoff の
有限 scale-neutral cover、(4) one_sided(固定 (χ,c₀) + Gram 床 ⟹ 両成分
生存の短補題で c₀→0 枝へ吸収 — 「g→1 だから自明」処理は却下)、(5) 通常
の Remez 代数。(iii) **指数 9 の出所の確定**: head_good の J⁹ +
projective order ν ≤ 9 + interval-rescaling Remez **一回** — 補題 G の
乗法窓は周波数 gap の閾値窓であり (L_C/s)⁹ の指数源ではない(用語注意)。
hop ごとの order-9 Remez は (L/s)^{9N_hop} を生むため却下 — bubble/
collar/handoff は bounded-overlap・同 scale 移送として定数のみ払う。
(iv) **中心の構造的不一致**: S は collar 内にあり自然な source 中心は
通常 W_core 外 — jet 用中心 ζ_S と projective 用中心 ζ_P を分ける schema
v2、または scale-neutral hop の中心移送補題が必要(単一中心の暗黙同一視
は却下)。(v) **着工指示**: T3 本文の前に **T3a0 の lower-rank projective
statement と T3b の scale-covariant floor statement の 2 本だけを正確に
起こす**(→ §8.24)。総見積 14–24R(計画値 16–20R)。

### 8.24 GC-5-T3 statement 登録(consult #19 着工指示 — TS-1/TS-2、登録のみ・証明非主張。**accepted、R-T3S R7 受理 SHA `dfc572b`**)

**目的**: consult #19 (v) の指示に従い、T3 本文着工前に危険度上位 2 点の
**statement を正確な型で登録**する(PTN-SPEC 方式 — 主張はしない。証明
義務はそれぞれ T3a0 / T3b)。

**補助型の登録(上流 accepted 型からの導出 — 上流本文は不変更)
[R-T3S R4-01][R4-02]**: TS-1 が参照する 2 つの object は上流に型として
存在しないため、accepted な step0_record((AT-0))の field から**導出
constructor** で定義する:
- **`c0_witness-v1`(config-level — chart-level の (CC-3) c₀ witness と
  区別)** := `(config ref, step0_record ref(raw 合算係数 c̄_k の exact 値
  — 安定化後の生存 ≃ 類 k), gauge_transform_ref := (§8.19 common_gauge_
  record-v1.1 の **scalar_absorption_table**(係数吸収の記録 — 係数変換
  c̄_k ↦ c̃_k の源はこちら)+ **transformed_atom_table**(変換後の原子
  (B, A) パラメータの記録 — 類 label k と原子の対応付けに使う)[R-T3S
  R6-01]。chart 枝 χ の config は T2b-0 adapter の入力なので両 field を
  必ず持つ), **c₀(config) := min_k |ĉ_k|、ĉ := c̃/‖c̃‖₂**((CC-3) と**同一
  座標**: scalar absorption 後の係数を係数単位球 ‖·‖₂ = 1 に正規化 — 正規化
  は計算で定まり追加 evidence 不要。生存類は c̃_k ≠ 0 なので c₀(config) > 0),
  rank_drop_flag(AT-2 行 (i) の判定 ref — true でも構成可能: 係数退化列を
  定義域から外さないのが本型の目的))` — constructor
  `derived_from(step0_record ref, scalar_absorption_table ref,
  transformed_atom_table ref, AT-2 判定 ref)`(step0 単独からは導出しない
  — 係数変換・原子対応・判定は別 accepted 型の field [R-T3S R5-02]
  [R6-01])、field 欠落 = 構成不能。**座標の同一性は定義で
  固定**(c₀(config) は (CC-3) の係数球上の量そのもの)なので、(CC-3) の
  chart-level c₀ witness「安定化部分列上 inf_n c₀(config_n) ≥ c₀」との関係
  は座標変換なしの inf 関係のみ — その検証(inf ≥ c₀ の evidence 照合)が
  T3a の義務。c₀^{(n)} → 0 は c₀(config_n) → 0 の意味で読む。
- **`prune_record-v1`** := step0_record の**射影**(消去 list は**空でも
  よい** [R-T3S R5-01]): `(step0_record ref, pruned_classes := 消去された
  ≃ 類の list(各要素: child label ∈ {1,2}, 類 id, 合算係数 = 0 の exact
  evidence ref — step0_record の合算係数 field; within-child の類消去も
  含む), support_before(prune 前の原子 label 集合), support_after(prune
  後), active_children_nonzero 判定 ref)` — constructor
  `derived_from_step0(step0_record ref)`。消去 child label は**導出量**:
  child i が dead ⟺ その全類が pruned_classes に含まれる。
- **`lower_rank_record-v1`(AT-2 行 (i) exit の全域型)** := `(prune_record-
  v1, support_rank_record := (m₁, m₂ := 各 child の生存 ≃ 類数, r := m₁ +
  m₂ ≤ 3), 生存構造 := two_children(m₁, m₂ ≥ 1)| one_component(i*)
  (m_{3−i*} = 0 — 導出))`。行 (i) の両 sub-case — **child 恒等零**(prune で
  m_i = 0)と**両 child 非零の support rank ≤ 3**(pruned_classes が空
  または within-child のみ)— を共に覆い、全 exit で構成可能(step0_record
  は常に存在する)✓。atlas_witness-v1 の lower-rank exit が持つ
  「redispatch record」は、本 packet 以降 **lower_rank_record-v1 を必須
  field として含む**(§8.17 の型は不変更 — 拡張は下流の消費契約として
  本節に登録: (AT-2) 行 (i) exit を T3a0 が消費する際 lower_rank_record-v1
  を構成できなければ lower_face_input-v1 は不成立、fail-closed)。

**(TS-1) T3a0 PTN-LOWER-FACE statement(support rank ≤ 3 の projective
二窓比較 — well-founded induction base)[R-T3S R1-01][R1-02]**:
- **closed-world 定義**(すべて構成子付き):
  - `rank_r_config-v1 := (r ∈ {1, 2, 3}, 親 T3 config ref(admissible
    T3 列の要素 — t3_witness 持ち), step-0 prune 後の**生存 raw pair**
    𝐁_r(§8.17 行 (i) — active_children_nonzero が false の child は除去、
    within-child ≃-class の総数 = r), **reduced pair** 𝐁̃_r(𝐁_r から
    (PS-1)/(PS-2) の exact 共通因子 D_r を消したもの — D_r は面上で再計算し
    親の stratum_record を流用しない — **型束縛** [R-T3S R2-02][R3 補足]:
    `stratum_record_r` := (PS-2) の stratum_record と**同名 field** で
    face 用に再計算した record `(cell_id_r, divisor_record_r 参照(§8.3
    (F2²-4) の方法を 𝐁_r に適用), d₀,r := ord D_r(exact), 𝐁̃_r の近接
    共通零点ごとの消滅次数対 (ord B̃₁,r, ord B̃₂,r), gcd-jump provenance
    (親 config との次数差))` を面上の 𝐁_r から独立に計算し、
    `checked_face_exactness`(D_r が 𝐁_r の exact 共通因子である検証 ref)
    と `not_parent_reuse`(親 record の id と異なり、計算 evidence が face
    pair を入力にしていることの検証 constructor)を必須とする), 生存構造
    constructor(**排他的・total** [R-T3S R2-01][R3-02]):
    **two_children**(両 child ≢ 0 の evidence = lower_rank_record-v1 の
    m₁, m₂ ≥ 1 — r = 2+1 / 1+1 等 — stratum_record_r の ord 対 field は
    この枝でのみ二成分)|
    **one_component(i*)**(i* ∈ {1, 2} = 生存 child の label、dead_child
    := 3 − i*。upstream (AT-0) は恒等零 child を step-0 で除去してから
    rank-r pair を作るので、**零 child は保持しない**: 表現は生存成分
    B̃_{i*,r} のみ + dead_child label + **lower_rank_record-v1 ref**(本節
    冒頭の補助型 — prune_record-v1 + support_rank_record、生存構造はそこ
    から導出 [R-T3S R4-02][R5-01])。両 child 恒等零は t3_witness と矛盾し
    構成不能))`。
  - **one_component(i*) contract**(total 化 [R-T3S R2-01][R3-02]):
    片 child が死んだ config は (PS-1) の二成分 g(B₂ ≢ 0 前提)の対象外
    なので、**one-component 専用契約**で閉じる: 生存成分 B̃_{i*,r}(i* は
    どちらでもよい — 契約は i* について対称)に対し g_r :≡ 1
    (B̃_{i*,r} ≠ 0 の点では |B̃_{i*,r}|/|B̃_{i*,r}| = 1、零点では連続延長
    = 1 — 0/0 点は除去可能)。この枝では分母床が不要なので
    `face_wzf_cover := not_needed(one_component)` 構成子を取る(恒等零
    成分の零点集合は全窓で (AT-3) の有限零点前提と両立しないため、AT-3 は
    **適用しない**)。PTN_r は C = 1・ν = 0 で自明(`trivial_one_component`)。**量化域**: 「admissible
    rank-r config」= admissible T3 列の要素から AT-2 行 (i) exit で得られる
    rank_r_config-v1 全体(それ以外の rank-r 対象は本 statement の量化外)。
  - `g_r := |B̃_{1,r} + B̃_{2,r}| / max_i |B̃_{i,r}|`(**two_children 枝
    のみ** — reduced pair 上、(PS-1) の g と同形。one_component 枝の g_r は
    上の専用契約で定義)。non-trivial 主張は two_children 枝のみ。
  - `ν_r`: **r のみに依存し config に依存しない**一様指数(chart 定数
    ではなく face 定数)。登録は ν_r ≤ 9 のみ(ν₃ ≤ 5 は目標であって約束
    ではない)。
- **入力型**: `lower_face_input-v1 := (AT-2 exit witness(行 (i) 判定 ref),
  rank_r_config-v1, window_contract_r(下記), face_approach_witness-v1
  (下記 — induction 接続時のみ必須))`。
- **window_contract_r(継承の型 — §8.16 (PS-4) と field 単位で整合)**:
  (PS-4) の window_contract は W・S・s・zf_scope(zf_witness + W_zf 被覆
  witness)・we9/d10/λ/ℓ_ext の**同一オブジェクト参照**を要求し、AT-2 は
  window_geometry のみを入力し W_zf は T2a の wzf_cover 出力で合成する
  (§8.17)。face 側では次の 3 群に分けて fail-closed に束縛する:
  **(PS-4) の全 field を列挙して群割当する** [R-T3S R2-04]: W, S, s,
  zf_scope = (zf_witness, W_zf 被覆 witness), we9_witness ref, d10_witness
  ref, **relation flag ∈ {identical, contained, disjoint-forbidden}**, λ,
  ℓ_ext — 以下の 3 群で漏れなく束縛する:
  - **同一オブジェクト継承(幾何 — 親と identity ref を共有)**: W, S, s,
    λ, ℓ_ext, r_S、および zf_witness の**制限**(生存 child の V は親の V 族
    の部分集合 — 制限 evidence ref。A.3a (ZF-3) の保証域 S + collar は不変)。
  - **face 側再導出(pair 依存 — 親から流用不可、T3a0 の構成義務)**:
    `face_wzf_cover`((AT-3) の方法を生存 reduced pair 𝐁̃_r に再適用した
    W_zf 被覆 witness — 親の wzf_cover は親 pair の零点に対するもので、
    prune 後の零点集合は全く異なるため継承しない。two_children 枝で必須、
    one_component 枝は not_needed(one_component))、`face_jet_witness`
    (we9/d10 の rank-r 類似物 — 構成子 := derived(ref)| not_needed
    (evidence: rank r で当該 witness を消費する下流不在の証明)。いずれか
    必須)、**`face_relation_flag`**(face_jet_witness の source 窓と S の
    関係 ∈ {identical, contained, disjoint-forbidden} — we9 が pair 依存で
    再導出されるため flag も face 側で再評価。face_jet_witness =
    not_needed のときは not_needed(同 evidence) — 欠落は不可)。
  - `inherit_identity_ref`: 親 window_contract オブジェクトへの参照
    (同一性の検証 constructor `checked_inherited` — **上記列挙の全 field
    について群割当が済んでいることを検証**する)。
  いずれの field も欠落 = window_contract_r 不成立(fail-closed)。
- **登録 statement(PTN_r、r ≤ 3、two_children 枝)**: 各 r に対し定数
  C_r > 0 と一様指数 ν_r ≤ 9 が存在し、全 admissible rank-r config で
    **‖g_r‖_W ≤ C_r・(L_C/s)^{ν_r}・‖g_r‖_S**。
- **摂動安定性(induction 接続点)**: `face_approach_witness-v1 :=
  (rank-4 列 ref(admissible T3 列 — AT-2 行 (i) で exit **しない**要素で、
  **chart 枝 χ 一定の atlas_witness-v1 ref を各要素が持つ** evidence 付き),
  face 列 ref(各 n で同要素の生存 child 係数を落とした rank_r_config —
  同 provenance、checked_same_provenance), 近接 evidence(落とした
  成分の係数 → 0 の記録 — **`c0_seq_ref` := 各要素の config-level
  `c0_witness-v1`(本節冒頭の補助型 — step0_record + scalar_absorption_
  table + transformed_atom_table + AT-2 判定から導出、c₀(config) は (CC-3)
  座標の係数球上の量。(CC-3) の chart-level witness ではない [R-T3S
  R4-01][R6-02])への identity ref の列**。
  **floor_input-v1 自体は参照しない**: floor_input-v1 は固定 c₀ の量化を
  要求し c₀^{(n)} → 0 列はその量化外(§8.23)なので producer にならない
  [R-T3S R3-03]。同一正規化
  ‖𝐁̂_n‖_⊕ = 1・同一係数列であることの検証 constructor
  `checked_same_c0_provenance` を必須とし、T3a の c₀ → 0 枝は**この型の
  object のみ**を消費する), 比較 statement(登録のみ): 定数 C_face が存在し
  limsup_n ‖g_n‖_W/‖g_n‖_S ≤ C_face・limsup_n ‖g_{r,n}‖_W/‖g_{r,n}‖_S
  — **成立しない場合は nogo 構成子**(rank-4 近傍で face の比が破綻する
  反例 ref)で停止)`。
- **明示非主張**: C_r・C_face の有効値、TN-3 からの直接導出(TN-3 は
  scalar jet/sup 比で分母付き PTN ではない — consult #19 Q2(a))、rank ≤ 2
  の two_children 枝の自明性、face_approach 比較の成立。**出力契約**:
  `ptn_lower_face-v1 := proven(C_r 存在 ref, ν_r ≤ 9 記録,
  face_approach 記録)| trivial_one_component(i*, lower_rank_record-v1 ref)|
  nogo(反例 ref)` — fail-closed(構成子名は上の契約と同一 [R-T3S R3-01])。

**(TS-2) T3b PTN22-SCALE-HOP statement(scale-covariant carrier floor)**:
- **regime**: PTN-22 は s_n → 0 を許し、r_{S,n} は通常 source scale と
  共に 0 へ落ちる — 固定 ρ > 0 の admissible_pair_ρ 量化(§8.23)が空に
  なる主縮小 regime。**m_C(ρ_n) の rate 無制御なそのまま使用は不可**
  (consult #19 Q2(e))。
- **rescale schema(証明側の入力型 [R-T3S R1-03])**: 不等式の値は物理
  座標のままで良い(pullback は点ごとの値を保つ — rescale が変えるのは
  **域の n 一様性**であり、compactness 論法の側で必要)。型:
  `rescale_input-v1 := (s_n, t_{c,n}(S の中心), rescale map
  y = (t − t_{c,n})/s_n, rescaled domain Ŵ_core,n := (W_core,n(ρ_n) −
  t_{c,n})/s_n(**固定 compact 集合 K̂ ⊂ ℝ 内に n 一様に入る evidence**),
  rescaled pair(pullback B̂_{i,n}(t_{c,n} + s_n y) — 値は保存、Fock norm
  は保存されない旨を記録し正規化は物理側 ‖𝐁̂_n‖_⊕ = 1 のまま),
  **零点自由 margin**(rescaled 座標で成分零点は Ŵ_core,n から距離 ≥ κ —
  ρ_n = κ s_n の設計目的。これが §8.23 admissible_pair_ρ の eventual
  ρ ≤ r_{S,n} evidence の代替 witness: ρ_n ≤ r_{S,n} eventual evidence
  **または** rescaled zero-free witness のいずれか必須),
  **core 非空 evidence**(W_core,n(ρ_n) ≠ ∅ eventual — §8.23 規約の
  min = +∞ による vacuous floor を型で排除))`。
- **登録 statement**: chart (χ, c₀) ごとに定数 κ(χ) > 0 と
  **m̄_C(χ, c₀) > 0** が存在し、ρ_n := κ・s_n として rescale_input-v1 を
  持つ十分先の n で
    **min_{W_core,n(ρ_n)} max_i|B̂_{i,n}| ≥ m̄_C(s_n 非依存)**
  (物理座標の値 — rescaled 座標でも同じ数)。
- **被覆(erosion band を含む [R-T3S R1-04])**: §8.23 の W_core,n(ρ) は
  U ∪ Σ から距離 ≥ ρ の部分のみで、距離 0〜ρ_n の **erosion band** が
  残る。被覆は **ρ_n-拡大 bubble** で張る(全て同一 n に束縛 [R-T3S R2
  補足]): U_{c,n}⁺ := B(x_{c,n}, r_{c,n} + ρ_n) ∩ W、Σ_n⁺ := Σ_n の W 内
  ρ_n-近傍。すると W_reg,n ∖ W_core,n(ρ_n) ⊂ ⋃_c U_{c,n}⁺ ∪ Σ_n⁺ で band が
  塞がり、**W = collar ∪ W_core,n(ρ_n) ∪ ⋃_c U_{c,n}⁺ ∪ Σ_n⁺** が被覆と
  なる。bounded overlap は**拡大族 {U_{c,n}⁺, Σ_n⁺}** について主張し(rescaled 座標で
  拡大幅は定数 κ)、拡大 bubble 上の inner-chart 解析(projective floor)は
  T3b の証明義務。移送は scale-neutral(指数 9 の一回払い設計と両立 —
  定数のみ払う)。
- **明示非主張**: m̄_C・κ の有効値、rescaled chart が新しい border frame
  を要求しないこと(要求する場合 20R 超 — consult #19 Q5)、T2c の固定 ρ
  床からの直接導出(rescale 極限は新しい compactness 論法が要る)、拡大
  bubble 上の floor。**出力契約**: `scale_floor-v1 := proven(κ ref, m̄_C
  存在 ref, rescale_input-v1 ref, bounded_overlap witness(拡大族), 拡大
  bubble cover 記録)| nogo(m̄_C 消失列 ref — この場合 BORD-22 は full
  BORD-4/TN-4 昇格へ)` — fail-closed。

**scope(非主張)**: TS-1/TS-2 の証明(T3a0/T3b)、T3a routing 補題
(one_sided ⇒ c₀→0)、T3c 合成、C₂₂、人間による査読は未実施。

### 8.25 GC-5-T3a0 PTN-LOWER-FACE(support rank ≤ 3 の projective 二窓比較 base — drafted、R7 適用済み、査読対象 R-T3A0 R8)

**目的**: consult #19 の順序どおり T3 の底。§8.24 (TS-1) の登録 statement
PTN_r を two_children 枝(r ∈ {2, 3})で証明し、one_component 枝を契約で
閉じ、face 側 field の再導出義務を構成し、face_approach を (α) 非 deep-flat
sub-case で二側比較として証明・(β) deep-flat sub-case と (γ) 次 face への
order drop を typed routing で送る。**主張は 1 つ**: PTN_r(two_children、
ν_r = 5、C_r は c₀ 非依存、(L_C/s)⁵ 形)。

**(LF-0) 座標: cell の単位化 dilation [R-T3A0 R1-04][R1-05]**: cell 窓 W
(|W| = L_C ≤ 1、中心 t₀)を y := (t − t₀)/L_C で **単位区間 Ŵ = [−1/2, 1/2]**
に移す(scalar dilation — metaplectic ではない)。Gauss 原子 e^{q_j(t)} を **t₀ 中心座標**
u := t − t₀ で q_j = (A_j/2)u² + B_j^{(t₀)}u + const と書く(B_j^{(t₀)} は
t₀ 中心の線形係数 — (LF-2) box_fit はこの座標での raw 箱を受け取る
[R-T3A0 R2-02])。u = L_C y で
  e^{q_j} = (定数) · e^{(Â_j/2)y² + B̂_j y}、
  **Â_j := A_j L_C²、B̂_j := B_j^{(t₀)} L_C**
となり、定数因子は係数へ吸収(その後 ‖ĉ‖₂ = 1 に再正規化 — 二窓比
sup_W/sup_S と g は定数倍・再パラメタ化で不変)。t₀ 中心 raw 箱
|A_j| ≤ 1 − δ_ℱ、|B_j^{(t₀)}| ≤ R_ℱ の下で
  **|Â_j| ≤ (1 − δ_ℱ)L_C² ≤ 1 − δ_ℱ、|B̂_j| ≤ R_ℱ L_C ≤ R_ℱ**
— **窓の位置 t₀ の一様 bound は不要**(T₀ を撤廃)。
source 窓は Ŝ = [ŝ_c − ŝ/2, ŝ_c + ŝ/2]、**ŝ := s/L_C ∈ (0, 1/2]**、
ŝ_c ∈ Ŵ。以後すべて y 座標で論じ、**(L_C/s)⁵ = ŝ⁻⁵ が直接現れる**(物理
s⁻⁵ 形と λ 換算は撤回 — chart scale λ の下界は不要 [R1-04])。

**(LF-0′) TN-3 の moving-center 系(K_face 上)[R-T3A0 R1-02]**:
  **K_face := {‖ĉ‖₂ = 1} × {(Â_j, B̂_j) : |Â_j| ≤ 1 − δ_ℱ、|B̂_j| ≤ R_ℱ}**
  (3 原子、定数 gauge §8.6 規約)、chart 円板 D̄(0, R_col := 1) ⊃ Ŵ、
  D̄(0, R_out := 2)。
**主張**: ∃c_face > 0: ∀p ∈ K_face ∖ Z₀、∀ζ′ ∈ D̄(0, 1):
  **‖J⁵f_p(ζ′)‖₂ ≥ c_face · sup_{D̄(0,2)}|f_p|**。
**証明**: (T1-2) を逐語 — 反例列 (p_n, ζ′_n) で比 → 0 を取り、(B3-2) の
pattern 固定、ζ′_n → ζ′ ∈ D̄(0,1)(compact)、**(B3-4) は ∀ζ′ ∈ D̄(t₀, R_col)
の moving-center 床**(σ₀‖v‖_ℱ、中心は任意点 — (B3-5) 末尾の注記)と
(B3-3)(i) の RKHS 評価で部分列上 ‖J⁵f_{p_n}(ζ′_n)‖ ≥ (σ₀/C_R) sup|f_{p_n}|
— 矛盾。(T1-1) との差は **中心を z_c(p) から任意点 ζ′ ∈ D̄(0, R_col) に
置換した点のみ**で、(B3-4) がその一般性を既に持つ。**箱定数の変更**
(R_col = 1、R_out = 2 — 箱 (δ_ℱ, R_ℱ) は同一)について: (B3-2)–(B3-5) は箱の
compact 性・Fock 所属 |Â| ≤ 1 − δ_ℱ < 1・R_col < R_out のみを使い、具体値に
依存しない(§8.10 の定数 σ₀、C_R は箱定数の関数として存在)— 本系は
その instance(**有効値非主張**)。∎

**(LF-1) 単一原子 child と分母の非零性(rank ≤ 3 の構造)[R-T3A0
R1-01]**: two_children で r = m₁ + m₂ ≤ 3、m_i ≥ 1 ⟹ **min(m₁, m₂) = 1**:
ある child が単一 ≃ 類 = 単一原子。その label を 2 に揃えるため **typed
relabel** を前置する [R-T3A0 R3-03]:
  `relabel_witness-v1 := (π := child 交換 (1 ↔ 2), π の**全 record への
  適用**(child label を持つ全 record を列挙 [R-T3A0 R4-03]): step0_record
  (原子 label 第 1 桁交換)・lower_rank_record-v1((m₁, m₂) 交換)・F2 record
  (B₁ ↔ B₂)・c0_witness-v2(類 id 更新 — 値は不変)・box_fit(原子ごとの
  箱 evidence の label 更新)・rescale_record((ĉ_j, Â_j, B̂_j) の label
  更新)・drop_set(k_min・mate の id 更新)・synthetic_records(step0_syn
  以下の label 交換)・face_hypotheses((H1)/(H2) の child 割当交換)・
  face_approach_witness-v2(θ 列・face 列の provenance に π 適用を記録)・
  window_contract_r-v2(不変), checked_invariants: 関数 B₁ + B₂ 不変・
  gcd D 不変・g 不変((F2²-2) G(w) = G(1/w))・K_face の元 p̂ 不変・
  **selector_transport** [R-T3A0 R5-03]: c0_witness-v2 の k_min と mate は
  π 後に**再導出せず π(k_min)、π(mate) に transport** する(同値最小係数が
  child 1/2 に跨る tie では label 全順序の tie-break が π-不変でないため —
  transport 後の k_min が argmin 集合に属すること(係数値 = c₀(config))を
  検証 `checked_selector_valid`); drop_set・origin・rank_r_config-v2 も
  同様に transport(値の再導出をしない), **checked_relabel_commutes**:
  導出 record ごとに derived(π(入力)) = π(derived(入力))(prune /
  lower_rank / stratum / synthetic_step0 / rank_r_config-v2 / origin の各
  constructor について検証 — c0 selector は transport 規則により可換性
  ではなく checked_selector_valid で担保))`
— 単一原子 child が label 1 の場合は relabel_witness を適用してから以下を
読む(「WLOG」の実体は provenance 込みのこの構成子)。以後 B₂ = ĉ₂e^{q̂₂}。**F2 record は使わない**(F2 は
二原子対の補題で単一原子用の w を持たない): 直接
  **P₂ := ĉ₂(定数)、V₂ := 1、r₂ := q̂₂**
と置く(B_i = P_iV_ie^{r_i} の形に自明に整合)。指数関数は零を持たないので
**B₂ は ℂ 全域で非零** ✓。D = gcd(P₁, P₂) は定数(reduced = raw、
stratum_record_r は d₀,r = 0 の退化 record — 構成可能)、H := B₁/B₂ は
**entire**、g = G(H)((F2²-2))。B₂ の両側評価(Ŵ 上、|y| ≤ 1/2):
  |e^{q̂₂(y)}| ∈ [e^{−C_box}, e^{C_box}]、C_box := (1 − δ_ℱ)/8 + R_ℱ/2
  ⟹ **κ_B := sup_Ŵ|B₂| / inf_Ŵ|B₂| ≤ e^{2C_box}**
— |ĉ₂| は分子分母で相殺し **κ_B は c₀ に依存しない** ✓(T3a の induction
接続で本質的)。

**(LF-2) 入力 field の構成と versioned 型 [R-T3A0 R1-03][R1-08]**: §8.24
の v1 型を prose で再解釈せず、**v2 を明示定義し v1 からの constructor
写像を与える**(§8.24 本文は不変更):
- `lower_face_input-v2 := lower_face_input-v1 の field を次のとおり置換
  [R-T3A0 R6-03]: **AT-2 exit witness → origin**、**rank_r_config-v1 →
  rank_r_config-v2**(stratum_record_r が生存構造条件付き — one_component
  の not_needed を格納できる)、window_contract_r → v2、face_approach_
  witness-v1 → v2; + box_fit + rescale_record + face_hypotheses-v1`。
  order_drop の参照先 lower_face_input-v2 は one_component face でも
  この constructor で構成可能。
  - **`box_fit`**: face の raw 原子が **t₀ 中心座標**で raw 箱 |A_j| ≤
    1 − δ_ℱ、|B_j^{(t₀)}| ≤ R_ℱ に入る evidence — **親 config の
    common_gauge_record-v1.1 が持つ standard_box_premise(§8.22 (CC-5) —
    raw 原子の箱前提)の部分集合継承**(identity ref + checked_subset
    [R-T3A0 R2-01]。§8.19 の all_atoms_in_K は**変換後原子**の所属で
    参照しない)。構成子: `from_standard_box_premise(親 chart 中心 = t₀ の
    evidence — window_contract の λ field は y = λ(t − t₀) で同じ中心を
    使う)| explicit(t₀ 中心線形係数の計算 ref と bound の検証)`。gauge 後
    の箱((CC-5) transformed box)は**参照しない** — TN-3 の K は raw 原子・
    raw 関数上の量化であり、(CC-6) の raw ↔ gauge pointwise 移送禁止に
    抵触しない [R1-03]。
  - **`rescale_record`**: (LF-0) の (t₀, L_C) と (Â_j, B̂_j, ĉ_j) の
    exact 計算 ref、‖ĉ‖₂ = 1 再正規化 ref、K_face 所属の検証 ref。
  - **同一関数 evidence**: F̃ := B₁ + B₂ が raw 3 原子和 Σ ĉ_je^{q̂_j} と
    **同一の関数**であること — child 1 の B₁ = P₁V₁e^{r₁} は (F2²-1) の
    「cell 上の等式」で raw 2 原子和に等しく(F2 record の identity 継承)、
    B₂ は (LF-1) の直接定義。TN-3 は raw 関数 f_p に対する主張なので、
    F̃ = f_{p̂}(p̂ := rescaled face config ∈ K_face)として消費する。
  - **`origin`(face の出所 — v1 の AT-2 exit witness field を一般化
    [R-T3A0 R2-03])**: `exit_face(AT-2 行 (i) exit witness、lower_rank_
    record-v1)| synthetic_face(親 rank-4 config ref(chart 枝 — AT-2 で exit
    **しない**要素)、**drop_set**(落とす ≃ 類の集合 — 同一 child 内:
    {k_min} で 2+1 face、{k_min, mate} で当該 child 全消去 = one_component
    face [R-T3A0 R3-05])、**synthetic_records** [R-T3A0 R3-01][R4-01][R4-02] :=
    (**step0_record_syn**: 親 step0_record と**同型の正式な step0_record**
    を constructor `synthetic_step0(親 step0_record ref, drop_set)` で生成 —
    **AT-0 の全 field を次の規則で再生成** [R-T3A0 R5-01]: (i) 所属写像
    cls: 原子 label a ∈ {11,12,21,22} ↦ ≃ 類 id(親 step0_record の類 field
    から読む); 落とす原子集合 := cls⁻¹(drop_set); (ii) **active 類集合** :=
    親の類 ∖ drop_set、active 原子 label 集合 := 親 ∖ cls⁻¹(drop_set)
    (gauge 定数 γ_ab は生存類対でそのまま); (iii) **合算係数 ledger は
    全類(消去類を含む)について保持** [R-T3A0 R6-01]: 生存類は親の
    exact 値、**drop_set の類は 0(exact — 置換による)を ledger に
    (類 id, child label, 値 0, 親の元値 ref) として記録** — AT-0 の native
    step0_record の全類 ledger(§8.17 [R-T3A0 R7-01] 追記)と同じ表現で、
    prune_record-v1 の射影 derived_from_step0 はこの ledger から
    pruned_classes と zero evidence を読む(型付き導出 ✓); (iv) matching
    M_syn := 親 M のうち両端点が active 原子の edge に制限し、各生存 edge の
    係数 witness (c_a, c_b, γ_ab) と相殺 flag は**親の値を継承**(生存係数は
    不変なので相殺値も不変); (v) face label := **AT-0/AT-2 の順序付き
    再適用** [R-T3A0 R6-02]: AT-2 は support rank ≤ 3 の lower-rank exit を
    exact-QR(rank 4 限定)より先に判定するので、synthetic face(rank ≤ 3
    by construction)の label は**常に lower-rank exit label**(two_children
    | one_component(i*) — support_rank_record から)。exact-QR flag・
    qr_global_witness は生成しない(rank 4 でないため不適用)。M_syn は
    data として保持するのみ。なお 1+1 face で cross-child ≃ 一致 + 係数
    exact 相殺なら F̃ ≡ 0 となり得るが、これは exact-QR exit ではなく
    (LF-4) 冒頭の「F̃ ≡ 0 ⟹ g ≡ 0 ⟹ PTN 自明」枝で処理する(2+1 face は
    未 match 類が残るので F̃ ≢ 0)。生成後に step0_record の型検証(全
    field 充足)を通す。**これは親の exact
    cancellation ではなく「係数を 0 に置いた関数」の正式 record** — 下流
    (LF-4) は face 関数の原子構造しか使わないので十分,
    **prune_record-v1 := derived_from_step0(step0_record_syn)** — 既存の
    射影 constructor をそのまま適用し、zero evidence は step0_record_syn の
    合算係数 field(= 0)から読む(型契約どおり [R4-02]),
    lower_rank_record-v1: drop 後の (m₁, m₂) と生存構造の導出,
    **stratum_record_r(drop_set 依存 [R4-01])**: two_children(drop_set =
    {k_min}、残る child 2 が単一原子)では D 定数 — d₀,r = 0 の退化 record
    evidence / **one_component(drop_set = {k_min, mate}、残るのは 2 原子
    child 1 のみ)では stratum_record_r := not_needed(one_component)**(§8.24
    の one_component 契約は分母・AT-3 を保持しない),
    係数を 0 に置いた関数の exact 計算 ref)`。face_approach の
    face 列は **synthetic_face** で構成する(v1 の「AT-2 exit で得られる」
    量化域を v2 で拡張 — 同時に **rank_r_config-v2** を明示定義 [R-T3A0
    R5-02]: rank_r_config-v1 の field のうち lower_rank_record-v1 ref を
    origin 経由の ref に置換し、**stratum_record_r を生存構造条件付き field
    に変更**: two_children ⟹ stratum_record_r 必須(v1 と同じ)、
    one_component(i*) ⟹ stratum_record_r := not_needed(one_component)
    (§8.24 の one_component 契約は分母・AT-3 を保持しないため — v1 では
    格納不能だった constructor を v2 で合法化。§8.24 本文は不変更、
    versioned 型変更として本節に登録)。他 field は v1 と同名で保持)。
  - **`face_hypotheses-v1`((LF-4) が実際に使う仮定の列挙 — 両 origin から
    供給)**: (H1) child 1 は **(H1a)** held cell 上の 2 原子 child で F2
    record を持つ(exit_face: 親の identity 継承 / synthetic_face:
    relabel 後 drop_set は child 2 側なので child 1 は親と同一 — identity
    継承)**または (H1b)** 単一原子((LF-1) と同じ直接定義 P₁ := ĉ₁、V₁ := 1、
    r₁ := q̂₁ — **r = 2 の 1+1 枝** [R-T3A0 R3-02])、(H2) child 2 は単一原子
    ((LF-1) の直接定義)、(H3) box_fit、(H4) window_geometry の同一
    オブジェクト継承(W, S, s, t₀)。**(LF-4) の証明は child 1 を「F̃ が cell
    上で raw 原子和に等しい」ことにしか使わない**((H1a) は (F2²-1) の等式、
    (H1b) は定義)ので (H1a)/(H1b) いずれでも成立し、t3_witness(2|2 限定)は face に要求しない — face は 2|2
    topology ではなく、その witness 生成は不要かつ不可能。
  - v1 → v2 写像 [R-T3A0 R3-01]: **v1 の「AT-2 exit witness」field は v2
    では origin field に置換される**(v1 の値は origin = exit_face(…) として
    埋め込む — v2 は v1 の全 field を保持するのではなく、この 1 field を
    origin に**置換**した型)。他の v1 field(rank_r_config・window_contract_r・
    face_approach_witness)は同名で保持、新 field(box_fit・rescale_record・
    face_hypotheses)は**必須**(欠落 = v2 不成立、fail-closed)。
- `window_contract_r-v2 := window_contract_r(v1)` で face_wzf_cover の
  constructor を **derived(AT-3 法)| denominator_nonvanishing(単一原子
  child の (LF-1) 定義 ref)** に拡張(two_children r ≤ 3 では常に後者が
  取れる — 分母 𝔇 := max(|B₁|, |B₂|) ≥ |B₂| > 0 が**点ごとに**成立し(B₂ は
  零点を持たない — gcd の D とは別記号 [R-T3A0 R4-04])零点 bubble 被覆は
  不要。**|B₂| の一様下界は主張しない**(ĉ₂ → 0 を許す)— 係数比は (LF-1)
  の κ_B で相殺される)。
  face_jet_witness := not_needed(evidence: 本 packet は (LF-0′) の jet 床を
  直接消費し、we9/d10 類似物を消費する下流は存在しない)、
  face_relation_flag := not_needed(同 evidence)。v1 の他 field 不変。
- **`c0_witness-v2 := c0_witness-v1 + (argmin 類 id k_min(c₀(config) =
  |ĉ_{k_min}| を実現する類 — 同点は label 全順序で tie-break), class-mate
  係数 ĉ_mate(k_min と同じ child の他方の類の係数 — 当該 child が単一類
  なら none))`** — constructor は v1 と同一入力(step0・
  scalar_absorption_table・transformed_atom_table・AT-2 判定)からの導出
  [R-T3A0 R2-04]。
- `face_approach_witness-v2 := face_approach_witness-v1 の全 field(θ 列・
  face 列・checked_same_provenance・c0_seq_ref・checked_same_c0_provenance —
  不変、ただし c0_seq_ref は c0_witness-v2 の列)+ ratio_branch := vanishing(部分列 selector, r_{n_k} → 0 evidence)|
  bounded_below(部分列 selector, r* > 0 evidence)(r_n := |ĉ_{k_min}|/|ĉ_mate|
  — mate は非 exit rank-4 で必ず存在 [R5-04]; face は k_min 類を落とした
  もの、ĉ_mate が face の単一原子係数)+ subsequence_transport(選択部分列
  への違反度・c0_seq_ref の制限 + checked_same_provenance 再検証 —
  T3c schema の消費契約 [R-T3A0 R4-05][R5-04])+ 比較記録(**任意の部分列
  のさらなる部分列上でちょうど一つ**) :=
  alpha_proven(C_face = 3)| beta_routed(face_deep_flat-v1 ref)|
  order_drop(**synthetic_face(drop_set = 当該 child の全類)の one_component
  face の lower_face_input-v2 ref** — 同じ synthetic_records で構成可能
  [R-T3A0 R3-05])| nogo(反例 ref)`
  (v1 の nogo constructor は保持)。**比較 statement は v2 で versioned
  replacement** [R-T3A0 R6-04]: v1 の登録形 limsup R₄ ≤ C_face limsup R₃
  (全列)を、「任意の部分列に対しさらなる部分列上で alpha_proven |
  beta_routed | order_drop のちょうど一つ」に**置換**する(v1 の limsup 形
  は、全部分列が vanishing かつ (α) の場合に v2 の系として回復 — v2 は
  v1 より弱い契約であり、その旨を明示する)。ptn_lower_face-v2 の出力
  contract の face_approach 記録はこの v2 三分岐と一致。
- domain_fit は**不要**((LF-0) で Ŵ ⊂ D̄(0, 1/2) ⊂ D̄(0, R_col = 1)、
  ŝ_c ∈ Ŵ、ŝ ≤ 1/2 ≤ R_out − R_col = 1 が構成的に成立 [R1-04][R1-05])。

**(LF-3) 補題(jet → 区間 sup — Taylor/Cauchy)**: F を D̄(ζ, R) 上解析、
M_R := sup_{D̄(ζ,R)}|F|、ζ ∈ ℝ、S := [ζ − ŝ/2, ζ + ŝ/2]、0 < ŝ ≤ R とする。
  **sup_S |F| ≥ c₅ (ŝ/2)⁵ max_{j≤5} |F^{(j)}(ζ)|/j! − 2 M_R (ŝ/(2R))⁶**
(c₅ > 0 は絶対定数: deg ≤ 5 多項式の [−1, 1] 上 sup と係数 max の
有限次元ノルム同値)。証明: F(ζ + u) = Σ_{j≤5} F^{(j)}(ζ)u^j/j! + R₆(u)、
Cauchy より |R₆(u)| ≤ M_R (|u|/R)⁶/(1 − |u|/R) ≤ 2M_R(ŝ/(2R))⁶(|u| ≤ ŝ/2
≤ R/2)。多項式部は x := 2u/ŝ ∈ [−1, 1] で Σ b_j x^j、b_j = F^{(j)}(ζ)(ŝ/2)^j/j!、
sup ≥ c₅ max|b_j| ≥ c₅ (ŝ/2)⁵ max_j |F^{(j)}(ζ)|/j!(ŝ/2 ≤ 1)。∎
**適用域**: (LF-4) では R := R_out − R_col = 1、ŝ ≤ 1/2 ≤ R で常に充足 ✓。

**(LF-4) PTN_r の証明(two_children、r ∈ {2, 3} — 2+1 と 1+1 の両枝)**:
y 座標で F̃ := B₁ + B₂ = f_{p̂}(p̂ ∈ K_face — 3 原子、r = 2 の 1+1 枝は
係数 1 個が 0 の点 ✓)。1+1 枝では child 1 も単一原子((H1b))で H は
entire かつ非零 — 以下の連鎖は child 1 の構造を「F̃ = raw 原子和」以外に
使わないのでそのまま適用 [R-T3A0 R3-02]。F̃ ≡ 0 なら
g ≡ 0 で PTN_r は自明(0 ≤ 0)— 以下 p̂ ∈ K_face ∖ Z₀。
**Case (a) source 上の block 支配**((F2²-3)(a) 逐語): ∃y* ∈ Ŝ で
max(|H(y*)|, 1/|H(y*)|) ≥ e ⟹ g(y*) ≥ 1 − 1/e ⟹ **‖g‖_Ŵ ≤ 2 ≤ 3.2‖g‖_Ŝ** ✓。
**Case (a) 否**: Ŝ 全体で e^{−1} ≤ |H| ≤ e。このとき
  ‖g‖_Ŝ ≥ sup_Ŝ |1 + H|/e = sup_Ŝ(|F̃|/|B₂|)/e ≥ sup_Ŝ|F̃| / (e·sup_Ŵ|B₂|)、
max(1, |H|) ≥ 1 より g ≤ |1 + H| = |F̃|/|B₂| なので
  ‖g‖_Ŵ ≤ sup_Ŵ|F̃| / inf_Ŵ|B₂|。
**(LF-0′) の消費**: 中心 ζ′ := ŝ_c ∈ Ŵ ⊂ D̄(0, 1): ‖J⁵F̃(ŝ_c)‖₂ ≥ c_face·M、
M := sup_{D̄(0,2)}|F̃|。max_{j≤5}|F̃^{(j)}(ŝ_c)|/j! ≥ ‖J⁵F̃(ŝ_c)‖₂/(5!√6) ≥
c_face M/(5!√6)。(LF-3) を R = 1、D̄(ŝ_c, 1) ⊂ D̄(0, 2) ⟹ M_R ≤ M で適用:
  sup_Ŝ|F̃| ≥ c₅(ŝ/2)⁵ c_face M/(5!√6) − 2M(ŝ/2)⁶
  = (ŝ/2)⁵ M [c₅c_face/(5!√6) − ŝ] ≥ c_* ŝ⁵ M
(ŝ ≤ ŝ₀ := c₅c_face/(2·5!√6) で角括弧 ≥ c₅c_face/(2·5!√6);
ŝ ∈ [ŝ₀, 1/2] では **同じ中心 ŝ_c の長さ ŝ₀ の部分区間 Ŝ₀ ⊂ Ŝ に
小 ŝ の評価を再適用**: sup_Ŝ|F̃| ≥ sup_{Ŝ₀}|F̃| ≥ c_* ŝ₀⁵ M ≥ c_* ŝ₀⁵ ŝ⁵ M
(ŝ ≤ 1/2 < 1)— 以後 c_* を c_* ŝ₀⁵ に取り直せば全 ŝ ∈ (0, 1/2] で
sup_Ŝ|F̃| ≥ c_* ŝ⁵ M [R-T3A0 R2-05]。**c_* > 0 の存在**、有効値非主張。ŝ₀ ≤ 1/2 は c₅ ≤ 1、c_face ≤ … の
規約で保証 — ŝ₀ > 1/2 なら ŝ₀ := 1/2 に切り下げる)。Ŵ ⊂ D̄(0, 2) より
sup_Ŵ|F̃| ≤ M。合成:
  **‖g‖_Ŵ ≤ M/inf_Ŵ|B₂| ≤ sup_Ŝ|F̃|/(c_* ŝ⁵ inf_Ŵ|B₂|)
  ≤ (e·κ_B/c_*)·ŝ⁻⁵·‖g‖_Ŝ = C_r·(L_C/s)⁵·‖g‖_S**
(y 座標の sup は物理座標の sup と同一 — 再パラメタ化)。
**C_r := max(3.2, e κ_B/c_*) — c₀ 非依存 ✓、ν_r = 5 ≤ 9 ✓**。∎

**(LF-5) one_component(i*) 枝**: §8.24 の専用契約(g_r ≡ 1、
trivial_one_component)— 証明不要(定義)。lower_rank_record-v1 の m_{3−i*}
= 0 から構成子が導出される。

**(LF-6) face_approach(rank-4 列の face 近接)[R-T3A0 R1-06][R1-07]**:
rank-4 config θ_n(chart 枝、AT-2 で exit しない)で、c0_witness-v2 の
argmin 類 k_min の係数を ε_n := ĉ_{k_min,n}、class-mate を ĉ_n := ĉ_mate,n
とする(**|ε_n| = c₀(config_n) は定義** [R-T3A0 R2-04])。k_min が child 1
側なら **relabel_witness-v1 を全 record に適用**してから読む(以後 k_min ∈
child 2 [R-T3A0 R3-03])。face は drop_set = {k_min} の synthetic_face
(2+1): child 2 = ĉ_n e^{q̂} + ε_n e^{q̂′} → 単一原子 ĉ_n e^{q̂}。
**mate の存在** [R-T3A0 R5-04]: 親 θ_n は chart 枝で AT-2 (i) exit しない
⟹ support rank = 4 = 2 + 2、両 child が 2 生存類 ⟹ **k_min の class-mate は
必ず存在**(ĉ_mate = none は起こらない — 型で排除)。
**ratio_branch(部分列 selector 付き [R-T3A0 R4-05][R5-04])**: r_n :=
|ε_n|/|ĉ_n| に対し、任意の部分列はさらに部分列を取って **vanishing
(r_{n_k} → 0)** または **bounded_below(r_{n_k} ≥ r* > 0)** の**ちょうど
一方**に入る(liminf の二択)。**T3c schema への束縛**: 消費側(§8.23 の
列-矛盾 schema)は違反列から部分列を抽出して使うので、比較契約を
「**任意の部分列に対し、さらなる部分列上で alpha_proven / beta_routed /
order_drop のちょうど一つが成立**」の形で供給し(§8.24 の limsup 形は
全部分列が vanishing かつ (α) の場合にそのまま回復 — 一般には routing
record が契約)、選択部分列には **subsequence_transport**(違反度 → ∞
evidence と c0_seq_ref の n_k 制限、checked_same_provenance の再検証)を
必須 field として付ける(部分列は null 列・発散列の性質を保存)。
**vanishing 枝**で以下の (α)/(β)。**bounded_below 枝**: |ĉ_{n_k}| ≤
|ε_{n_k}|/r* → 0 なので child 2 全体が消える regime — **order_drop**:
drop_set = {k_min, mate} の synthetic_face(one_component(1) face —
synthetic_records で構成可能、PTN は trivial_one_component)への routing
(部分列 selector・subsequence_transport を record に含める)[R-T3A0
R3-05]、本節非主張(rank-4 列自体の PTN は T3a)。
同一 θ 列・同一窓 (Ŵ, Ŝ) 上で face 側 g₃ := G(H₃)、H₃ := B₁/B₂⁽³⁾、
B₂⁽³⁾ := ĉ_n e^{q̂}、rank-4 側 g₄ := G(H₄)、H₄ = B₁/B₂⁽⁴⁾ = H₃/(1 + η_n)、
η_n := (ε_n/ĉ_n)e^{q̂′ − q̂}、|η_n| ≤ r_n e^{2C_box} =: η̄_n → 0 on Ŵ。
**G の chordal Lipschitz 性**: G(w) = |1 + w|/max(1, |w|) は ℂP¹ 上連続で
|w| ≤ 1 では |∇G| ≤ 1、|w| ≥ 1 では G(w) = |1 + 1/w| は 1/w について
|∇| ≤ 1 — chordal 距離 d_c に関して **Lipschitz(定数 L_G ≤ 2)**。
w ↦ w/(1 + η) は |η| ≤ 1/2 で d_c(w/(1+η), w) ≤ 4|η|(∞ を含む ℂP¹ 上一様
— Möbius 変換の chordal 評価)。よって **|g₄ − g₃| ≤ 8 η̄_n =: ε′_n**
on Ŵ(pointwise、同一窓)。
- **(α) 非 deep-flat**: ε′_n ≤ ‖g₃‖_Ŝ/2 のとき、‖g₄‖_Ŵ ≤ ‖g₃‖_Ŵ + ε′_n、
  ‖g₄‖_Ŝ ≥ ‖g₃‖_Ŝ − ε′_n ≥ ‖g₃‖_Ŝ/2 ⟹
  R₄ := ‖g₄‖_Ŵ/‖g₄‖_Ŝ ≤ 2R₃ + 2ε′_n/‖g₃‖_Ŝ ≤ 2R₃ + 1 ≤ **3R₃**
  (R₃ ≥ 1 — Ŝ ⊂ Ŵ)。**二側比較 limsup R₄ ≤ C_face limsup R₃、C_face = 3**
  ✓(§8.24 face_approach の登録形そのもの)。合わせて (LF-4) より
  R₄ ≤ 3C_r(L_C/s)⁵ — rank-4 近傍 config の PTN が face から継承される。
- **(β) deep-flat**: ε′_n > ‖g₃‖_Ŝ/2 ⟹ ‖g₃‖_Ŝ < 2ε′_n → 0、(LF-4) より
  ‖g₃‖_Ŵ ≤ 2C_r(L_C/s)⁵ ε′_n — face の g₃ が cell 全域で ε_n 程度に
  小さい regime(3 原子部分 F̃₃ ≲ |B₂|·ε′_n(L_C/s)⁵)。これは λ_n := 1/ε_n
  の border 再正規化で「3 原子 border 極限 + 単位原子」型の rank-4 列に
  なる regime であり、rank-3 face の PTN では制御できない。**typed
  routing**: `face_deep_flat-v1 := (face_approach_witness-v2 ref(θ 列・
  face 列・provenance・c0_seq_ref を含む — 型充足 [R1-07]), ε′_n 列 ref,
  ‖g₃‖_Ŝ < 2ε′_n の evidence, 各 n の ŝ_n(**一様性は主張しない** — s_n → 0
  の scale 解析は T3b の入力), λ_n 再正規化 record)` を構成して **T3a の
  c₀ → 0 枝へ送付**(本 packet 非主張)。

**(LF-7) 出力契約**: `ptn_lower_face-v2 := proven(C_r 存在 ref((LF-4) —
c₀ 非依存 flag, (L_C/s)⁵ 形), ν_r = 5 記録, face_approach 記録 :=
alpha_proven(C_face = 3)| beta_routed(face_deep_flat-v1 ref)| order_drop
(synthetic one_component face ref))| trivial_one_component(i*,
lower_rank_record-v1 ref)|
nogo(反例 ref)`。v1(§8.24)からの写像: proven の 3 field は v1 と同名、
face_approach 記録が v1 の単一 ref から 3 分岐 constructor に拡張(v1 の
nogo は保持)。

**scope(非主張)**: C_r・c_*・c_face・c₅ の有効値、(β) deep-flat の解決
(T3a)、order_drop 後の rank-2 face の再帰(同じ (LF-4) が r = 2 で適用
可能だが接続は T3a)、rank-4 の PTN 本体(T2c/T3c)、人間による査読は
未実施。

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
| COND9-PROBE | A.5a COND9 の線形 one-hop conditioning が成立しない(比 ‖g‖_W/‖g‖_S が (L/s)⁹ 予算を破る) | 2\|2 near-QR 族(pairing 摂動 + p 二次)で R(s) := sup_W g / sup_S g を random 3000+ + Nelder-Mead adversarial、s 対数列 5 点 + confluent 許容変種 | **結果**(`cond9_probe.py`): adversarial max R は s = 10⁻¹→10⁻³ で 2.9×10² → 1.6×10³(**slope ≈ 1 ≪ 9**)、confluent 許容でも ~10³ vs 予算 10¹⁸⁺ — **no-go 信号なし**(consult #14 の黄赤リスクへの経験的反証材料。Nelder-Mead は ord-9 同調方向を見つけにくく sharp 指数の証明代替ではない。診断) |
| BORD22-PROBE | BORD-22/PTN-22 の未検査機構(consult #15 指摘: gcd-jump inner bubble・exact QR tangent・support drop×scale collapse・rate mismatch・adversarial 共退化)に no-go 信号(指数 > 9 / 定数→0)がある | R(s) := sup_W g/sup_S g を 5 族で測定(bubble 配置 3 変種・QR tangent δ 5 桁・support drop・rate mismatch ladder・Nelder-Mead 60 起点 × s 5 点) | **結果**(`bord22_probe.py`): ① bubble を W∖S に置いた**無条件版は R ≈ 0.25/ε で非有界**(反例族 — 素の二窓不等式は偽、zf/stratum 条件が型必須である設計裏付け。§8.16 (PS-4) が消費)② 同族 ZF collar 条件付きは plateau(~10、ε 5 桁で有界)③ QR tangent slope ≈ 1.0(δ 5 桁で安定)④ support drop / rate mismatch slope ≤ 0.42 ⑤ adversarial slope ≈ 0.90 ≪ 9・max R ≈ 2.8×10³ vs 予算 10²⁷ — **条件付き族に no-go 信号なし**。診断であり証明の代替ではない |
| BORD22-FLOOR-PROBE | consult #16 の no-go 監視点 — **床そのもの**(carrier m_C / defect jet 床 / Gram 最小固有値)が退化列で 0 へ落ちる(weighted ratio の横ばいに隠れる定数崩壊) | fixture 5 種(consult #16 指定): PROJECTIVE-FLOOR(QR 接近 ε 4 桁 × random 40)/ QR×BUBBLE(δ = ε^a、零点距離 = ε^b 独立)/ DOUBLE-BUBBLE(S 内 + W∖S の 2 bubble 異 scale)/ CARRIER-SWITCH(支配交代 + 相殺 + support drop 同時)/ TWO-LEVEL-SVD(s₁ = s₀²、s₂ = e^{−1/s₀}、L²(S) Gram — Fock の代理)。norm は複素箱 sup の代理 | **結果**(`bord22_floor_probe.py`): ① defect jet 床・carrier 床は QR 接近で **slope ≈ 0(崩壊なし)** ② QR×BUBBLE の m_C は bubble routing 後 plateau または緩多項式減衰(slope ≤ 0.5)③ DOUBLE-BUBBLE の条件付き R ≤ 7 ④ CARRIER-SWITCH: support drop 自体のコストは有界(< ×2)、m_C は周波数広がり λ に指数依存 = **chart 箱定数の非大域一様性**(設計整合 — chart 内固定)⑤ raw-atom Gram は数値零まで崩壊 = **想定どおり**(T2b が raw atom でなく divided-difference/SVD frame を使う設計根拠)— **床の no-go 信号なし**。診断であり証明の代替ではない |
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

- v0.29.55(2026-09-03): R-T3A0 R7(blocking 1 + 軽微 1)適用 — [R7-01]
  reviewer 指示により §8.17 (AT-0) の step0_record 出力型に in-place 追記
  (audit marker、前例 [R-T2BII R1-02][R-T2C R7-01]): 合算係数 field は
  全類 ledger(prune 済み類も合算値 0 entry として保持)で、active 類集合と
  分離 — prune_record-v1 / lower_rank_record-v1 の導出元を正本側で保証。
  §8.25 synthetic 側の参照を同追記に向けた。軽微: lower_face_input-v2 の
  face_hypotheses-v1 表記統一。

- v0.29.54(2026-09-03): R-T3A0 R6(blocking 4)適用 — [R6-01]
  synthetic_step0 に全類の合算係数 ledger(消去類は 0 と親元値 ref を
  保持)を導入し、prune_record-v1 の射影が ledger から pruned_classes と
  zero evidence を型付きに読めるように。[R6-02] face label を AT-0/AT-2 の
  順序付き再適用(rank ≤ 3 ⟹ 常に lower-rank exit label)に修正、exact-QR
  flag / qr_global_witness の生成を撤回(1+1 の exact 相殺は F̃ ≡ 0 自明枝)。
  [R6-03] lower_face_input-v2 の field 置換(origin・rank_r_config-v2・
  window_contract_r-v2・face_approach_witness-v2)を明示。[R6-04] 比較
  statement を v2 の versioned replacement(部分列三分岐 — v1 limsup 形は
  α 全域の場合の系)と明示し、出力契約と一致させた。

- v0.29.53(2026-09-03): R-T3A0 R5(blocking 4)適用 — [R5-01]
  synthetic_step0 を AT-0 全 field の意味的再生成規則(所属写像 cls・原子/
  類の除去・生存 edge の係数 witness/相殺 flag 継承・face label 規則の
  再適用・exact-QR flag → F̃ ≡ 0 自明枝)で規定。[R5-02] rank_r_config-v2 を
  明示定義し stratum_record_r を生存構造条件付き field に(one_component
  で not_needed を合法化 — versioned)。[R5-03] relabel_witness に
  selector_transport(k_min/mate/drop_set/origin/rank config は再導出せず
  transport、checked_selector_valid)を追加し、可換性検証対象に
  synthetic_step0・rank_r_config-v2・origin を追加。[R5-04] 非 exit rank-4
  では mate が必ず存在することを型で明記(none 枝除去)、比較契約を
  「任意の部分列のさらなる部分列上でちょうど一つ」+ subsequence_transport
  (違反度・c0_seq_ref の制限)で T3c schema に束縛。

- v0.29.52(2026-09-03): R-T3A0 R4(blocking 5 + nonblocking 1)適用 —
  [R4-01] synthetic_records を drop_set 依存にし、one_component では
  stratum_record_r := not_needed(one_component)。[R4-02] step0_record_syn を
  constructor synthetic_step0 で生成する正式な step0_record(係数 0 置換・
  M 再計算・型検証)とし、prune_record-v1 は既存射影 derived_from_step0 で
  接続(親の exact cancellation ではない旨明記)。[R4-03] relabel_witness
  の π 適用対象に box_fit・rescale_record・drop_set・synthetic_records・
  face_hypotheses・face_approach を追加し checked_relabel_commutes を導入。
  [R4-04] 分母を 𝔇 := max(|B₁|,|B₂|) と別記号化し「点ごとに > 0、一様下界
  非主張、係数比は κ_B で相殺」に修正。[R4-05] dominant_ratio を
  ratio_branch := vanishing | bounded_below(部分列 selector・provenance
  再検証付き)に置換。nonblocking: lower_face_input-v2 の定義文を「AT-2 exit
  witness は origin に置換」で統一。

- v0.29.51(2026-09-03): R-T3A0 R3(blocking 5)適用 — [R3-01] v1 → v2 で
  AT-2 exit witness field を origin に置換(保持ではない)と明示し、
  synthetic_face に synthetic_records(step0_syn・prune・lower_rank・
  stratum_record_r の導出)を必須化。[R3-02] face_hypotheses (H1) を
  (H1a) 2 原子 + F2 record | (H1b) 単一原子直接定義に分岐し、(LF-4) が
  child 1 を「F̃ = raw 原子和」以外に使わないことを明示して 1+1 枝を閉じる。
  [R3-03] relabel_witness-v1(child 交換 π の全 record 適用 + 不変量検証)を
  定義し、WLOG を provenance 込みの構成子に置換。[R3-04] rescale_record
  から T₀ を除去。[R3-05] order_drop の対象を drop_set = child 全類の
  synthetic one_component face として実構成。同期: §4 T3a0 依存に
  synthetic_face の親(chart 枝の非 exit config)を明示; v0.29.50 の
  「R_ℱ のみ」は正確には K_face・C_box が (δ_ℱ, R_ℱ) に依存の意。

- v0.29.50(2026-09-03): R-T3A0 R2(blocking 5)適用 — [R2-01] box_fit の
  参照先を親 common_gauge_record-v1.1 の standard_box_premise(raw 箱前提)
  の部分集合継承に是正(all_atoms_in_K は変換後原子で不適)。[R2-02] T₀ を
  撤廃 — 箱前提を t₀ 中心座標の線形係数 B^{(t₀)} で受け取り、dilation 後
  |B̂| ≤ R_ℱ L_C ≤ R_ℱ で一様(K_face・C_box も R_ℱ のみ)。[R2-03]
  rank_r_config-v2 に origin := exit_face | synthetic_face を追加し、face
  列は synthetic_face で構成; (LF-4) が使う仮定を face_hypotheses-v1
  (H1–H4)として列挙し t3_witness を face に要求しない。[R2-04]
  c0_witness-v2(argmin 類 id・class-mate 係数)を導出型として追加、
  dominant 条件を比 |ε_n|/|ĉ_n| → 0(dominant_ratio)で型化。[R2-05]
  (LF-4) の大 ŝ 域を中心部分区間 Ŝ₀ ⊂ Ŝ への再適用で閉じる。

- v0.29.49(2026-09-03): R-T3A0 R1(blocking 8)適用 — §8.25 全面改稿。
  [R1-04][R1-05] cell を単位長に dilation する座標 (LF-0) を導入し、TN-3 の
  箱充足・中心域・(L_C/s)⁵ 形を構成的に同時充足(物理 s⁻⁵ と λ 換算を
  撤回、domain_fit 不要化、(LF-3) 適用域 ŝ ≤ 1/2 ≤ R = 1)。[R1-02] moving-
  center 系 (LF-0′) を K_face 上で (T1-2) 逐語 + (B3-4) の任意中心性から
  証明(箱定数非依存の instance として)。[R1-01] 単一原子は F2 record を
  使わず P₂ := ĉ₂、V₂ := 1、r₂ := q̂₂ と直接定義。[R1-03] box_fit を親の
  all_atoms_in_K(raw)の部分集合継承に変更し、同一関数 evidence
  ((F2²-1) の cell 上等式)を明示 — gauge 後箱は参照しない。[R1-06]
  face_approach (α) を G の chordal Lipschitz 性で二側比較 limsup R₄ ≤
  3 limsup R₃ として証明、dominant_atom_floor を型付き前提化し不成立は
  order_drop 構成子。[R1-07] face_deep_flat-v1 に face_approach_witness-v2
  ref を含め、ŝ_n の一様性非主張を明記。[R1-08] lower_face_input-v2 /
  window_contract_r-v2 / face_approach_witness-v2 / ptn_lower_face-v2 を
  明示定義し v1 からの constructor 写像を記載。

- v0.29.48(2026-09-03): **§8.25 GC-5-T3a0 PTN-LOWER-FACE 起草** — (LF-0)
  jet→区間 sup 補題(Taylor/Cauchy + deg ≤ 5 多項式のノルム同値)、(LF-1)
  rank ≤ 3 two_children では単一原子 child が F2 の D1/D2 枝で cell 上非零
  ⟹ H entire・κ_B は c₀ 非依存、(LF-2) face 側 field の discharge
  (denominator_nonvanishing 構成子・not_needed・box_fit 部分集合継承・
  domain_fit)、(LF-3) PTN_r 証明: (a) block 支配は (F2²-3) 逐語、(a) 否は
  TN-3 (T1-1) の J⁵ 床 + (LF-0) で sup_S|F̃| ≥ c_* s⁵ M ⟹ ‖g‖_W ≤
  (eκ_B/c_*) s⁻⁵ ‖g‖_S、ν_r = 5、chart 座標換算は λ record 内完結、(LF-4)
  one_component 契約、(LF-5) face_approach: (α) 非 deep-flat を C_face = 4 で
  証明、(β) deep-flat は face_deep_flat-v1 で T3a へ typed routing、(LF-6)
  出力契約(§8.24 型への versioned 追加)。

- v0.29.47(2026-09-03): **§8.24 GC-5-T3 statement 登録 accepted**(R-T3S
  R7、受理 SHA `dfc572b`、全 7 ラウンド: R1 closed-world 化・window_contract
  継承の field 分離・rescale schema・拡大 bubble 被覆、R2–R6 は上流型との
  参照整合 — one_component の total 化、stratum_record_r、c0_witness-v1 /
  prune_record-v1 / lower_rank_record-v1 の導出型登録、(CC-3) 座標の固定、
  §8.19 実 field への provenance 是正)。TS-1/TS-2 は登録のみで証明未着手
  (T3a0 / T3b)。次: T3a0 PTN-LOWER-FACE 起草(consult #19 の順序)。

- v0.29.46(2026-09-03): R-T3S R6(blocking 2)適用 — [R6-01] c̃ の導出元を
  §8.19 の実 field に合わせ scalar_absorption_table(係数吸収)+
  transformed_atom_table(原子パラメータ・類対応)の両参照に是正、
  constructor 入力に scalar_absorption_table を追加。[R6-02]
  face_approach_witness-v1 の c0_seq_ref 記述(active interface)を現行
  constructor の provenance に同期。

- v0.29.45(2026-09-03): R-T3S R5(blocking 2)適用 — [R5-01]
  prune_record-v1 を「消去 ≃ 類 list(空可、within-child 含む)」に一般化
  し、AT-2 行 (i) exit の全域型 lower_rank_record-v1 := (prune_record,
  support_rank_record (m₁, m₂), 生存構造 導出)を登録 — child 恒等零と
  両 child 非零 rank ≤ 3 の両 sub-case を覆う。redispatch record への
  必須化・one_component・出力契約・two_children evidence の参照先をこれに
  統一。[R5-02] c0_witness-v1 の c₀(config) を (CC-3) と同一座標で定義
  (transformed_atom_table による scalar absorption 後の係数を係数単位球で
  正規化)、constructor を derived_from(step0, transformed_atom_table,
  AT-2 判定)に是正、座標同一性を定義で固定し T3a 義務を inf 関係の照合
  のみに縮小。

- v0.29.44(2026-09-03): R-T3S R4(blocking 2)適用 — [R4-01] config-level
  `c0_witness-v1` を §8.24 冒頭に登録(step0_record の合算係数 exact 値から
  c₀(config) := min|c̄_k| を導出、rank_drop_flag = true でも構成可能 —
  (CC-3) の chart-level witness はその inf 側で、整合検証は T3a 義務)。
  c0_seq_ref はこの型を参照(v0.29.43 の「(CC-3) の config ごとの構成」
  という記述は誤りで、本版で訂正)。[R4-02] `prune_record-v1` を
  step0_record の射影として登録(消去 child・類ごとの合算 = 0 の exact
  evidence・前後 support・active_children_nonzero 判定 ref)、(AT-2) 行 (i)
  exit の redispatch record に必須 field として下流契約で要求(§8.17 本文は
  不変更)。one_component(i*) と出力契約の参照先を prune_record-v1 に統一。

- v0.29.43(2026-09-03): R-T3S R3(blocking 4 + 補足)適用 — [R3-01] 出力
  契約の構成子名を trivial_one_component(i*, prune record ref)に統一。
  [R3-02] one_component を生存 label i* ∈ {1,2} で total 化(零 child は
  step-0 除去済みのため保持せず、dead_child label + prune record ref で
  表現)。[R3-03] c₀ evidence を floor_input-v1 参照から切り離し、要素ごとの
  (CC-3) c₀ witness への identity ref 列 c0_seq_ref + chart 枝一定の
  atlas_witness ref に束縛(固定 c₀ 量化外の c₀ → 0 列に producer を与える)。
  [R3-04] §4 T3a0 依存に GC-5-T2a/T2b-ii/T2c を明示。補足: face record を
  (PS-2) と同名 field の stratum_record_r(cell_id_r・divisor_record_r・
  d₀,r・ord 対・gcd-jump provenance)に改名。

- v0.29.42(2026-09-03): R-T3S R2(blocking 4)適用 — [R2-01] 生存構造を
  排他的・total な two_children | one_component 構成子にし、one_component
  専用契約(g_r ≡ 1 連続延長・face_wzf_cover = not_needed・AT-3 不適用・
  trivial_one_component)を定義。[R2-02] D_r を divisor_record_r((PS-2)
  同型)+ checked_face_exactness + not_parent_reuse で型束縛。[R2-03]
  face_approach の c₀ evidence を floor_input-v1 の c₀ witness への
  identity ref(c0_ref)+ checked_same_c0_provenance に接続。[R2-04]
  window_contract_r で (PS-4) 全 field を列挙し群割当、relation flag を
  face_relation_flag として再導出群に追加、checked_inherited が全 field の
  群割当を検証。補足: 被覆集合を同一 n に添字束縛。

- v0.29.41(2026-09-03): R-T3S R1(blocking 5)適用 — [R1-01] TS-1 を
  closed-world 化(rank_r_config-v1: r ∈ {1,2,3}・生存 raw/reduced pair・
  面上再計算の D_r・two_children | single_child 構成子; g_r の定義と
  single_child 自明枝; ν_r は r のみ依存の一様指数; face_approach_witness-v1
  の型と nogo 構成子)。[R1-02] window_contract_r を (PS-4) と field 単位で
  整合: 幾何は同一オブジェクト継承(W/S/s/λ/ℓ_ext/r_S + zf_witness 制限)、
  pair 依存 field(W_zf 被覆・we9/d10 類似物)は face 側再導出義務、
  inherit_identity_ref + checked_inherited。[R1-03] TS-2 に
  rescale_input-v1(rescale map・n 一様 compact 域・値保存/norm 非保存の
  記録・零点 margin κ・core 非空 evidence)を追加、ρ ≤ r_{S,n} evidence の
  代替 witness を明示。[R1-04] 被覆を ρ_n-拡大 bubble U_c⁺/Σ⁺ で張り
  erosion band を塞ぐ(bounded overlap は拡大族に対して主張)。[R1-05]
  §4 台帳の T3a0 依存から親行を除去(包含であって依存ではない)。

- v0.29.40(2026-08-22): **consult #19(Sol、T3 骨格裁定)記録**(§8.23
  追記)— 単一 T3 却下、T3a0 LOWER-FACE / T3a ROUTE / T3b SCALE-HOP /
  T3c REMEZ-CLOSE の 3+1 分割(§4 台帳に 4 行追加、見積計 14–24R)。
  最危険点は固定 (c₀,ρ) 床の境界一様化(ρ/scale 縮退 > c₀→0 lower-rank
  循環 > cover > one_sided)。指数 9 は J⁹ + ν ≤ 9 + Remez 一回払い —
  補題 G は指数源ではない(用語注意)。**§8.24 起草**: 着工指示に従い
  TS-1(lower-face PTN statement — window 継承・face_approach・一様予算
  9)/ TS-2(scale-covariant floor — ρ_n ≍ s_n・m̄_C の s 非依存・
  bounded overlap)を登録のみ(証明非主張)で追加。

- v0.29.39(2026-08-22): **GC-5-T2c BORD22-FLOOR accepted**(R-T2C R8、
  受理 SHA `15b272e`、全 8 ラウンド: R1-R2 数学的再構成(σ₀ 量化型・
  raw 側 m_C・ρ-erosion core・移動円板 Hurwitz・defect-order ν・eventual
  連鎖)、R3-R7 型配管(core-interior 中心・c₀ 固定・floor_input-v1・
  violation_sequence-v1・provenance 束縛・admissible_pair_ρ・vanish_flag
  伝播)。**BORD-22(T2 chain: T2a ATLAS → T2b-0/i/ii → T2c FLOOR)
  完成**。次: GC-5-T3 PTN-22(二窓 Remez 合成)と GC-5-T2c-ov
  OVERFLOW-PS9-BRIDGE。claim 水準は不変: 証明ドラフト・複数 LLM の
  fixed-SHA 査読+数値診断のみ・人間による査読は未実施。

- v0.29.38(2026-08-22): R-T2C R7(blocking 2)適用 — [R7-01]
  vanish_flag = none 限定を最終消費型まで伝播: violation_sequence-v1 に
  floor_input-v1 ref を必須化(provenance 束縛で継承)、§8.22 (CC-7) の
  消費宣言に reviewer 指示の in-place 追記(audit marker、前例
  [R-T2BII R1-02])、§4 台帳の消費契約を同期。[R7-02] admissible_pair_ρ
  型を導入し m_C の set-builder と floor_witness の量化 field を型束縛
  (evidence なし pair は量化外 — routing は T3 義務)。

- v0.29.37(2026-08-22): R-T2C R6(blocking 3)適用 — [R6-01]
  floor_input-v1 に provenance(θ 列・ζ 列・部分列 selector)と
  checked_same_provenance constructor を追加(FL22-3/4 の分子・分母の
  同一列消費を型で保証)、violation_sequence-v1 にも同 constructor。
  [R6-02] ρ の量化域を「十分先で ρ ≤ r_{S,n} の evidence を持つ pair」に
  限定(r_S の共通下界は仮定しない — eventual 条件を witness 化)、
  (b) の margin を min(ρ, r_{S,n}) = ρ(threshold 以降)に更新。[R6-03]
  floor input を vanish_flag = none に限定 — one_sided は K_χ(c₀) 係数
  下界との両立未証明のため消費対象外、routing は T3 明示義務。FL22-4 の
  one_sided 消費記述を撤回。

- v0.29.36(2026-08-22): R-T2C R5(blocking 4)適用 — [R5-01] §4 台帳を
  (χ, c₀) パラメータ表記(σ₀(χ,c₀)/2・m_C(χ,c₀,ρ)/2)に同期(補記:
  v0.29.35 の [R4-01] 同期は上界 M_C = C_R 全 n pointwise を含む)。
  [R5-02] floor_input-v1 バンドル型を導入 — 上流 accepted 型は不変更の
  まま c₀ witness((CC-3) 構成)を第一級 field 化し、chart 参照を全て
  バンドル経由に。[R5-03] violation_sequence-v1 に head_outcome =
  head_good(good_witness ref)を必須化(head_overflow 列への床誤適用を
  型で排除)+ 同一 pair への raw_restatement link。[R5-04] 同型に θ 列
  (t3_witness・window_geometry・checked_zero_free evidence)・ζ 列
  (中心域所属)・core 非空性の同一 ρ/threshold eventual 条件を追加。

- v0.29.35(2026-08-22): R-T2C R4(blocking 3)適用 — [R4-01] §4 台帳の
  carrier 床を eventual 形 m_C(ρ)/2(min_{W_core,n(ρ)}、十分先)に同期。
  [R4-02] c₀ を admissible pair 量化の固定パラメータに昇格(両対角列が
  単一 compact K_χ(c₀) に残留 — c₀^{(k)} → 0 列は量化外)。[R4-03] 消費
  契約に violation_sequence-v1 型を登録(共通 c₀・threshold・core 非空・
  core-interior 中心 flag・違反度記録)— witness 構成不能な違反列
  (c₀ → 0 / core 空 / 中心 core 外)の routing を T3 明示義務化。

- v0.29.34(2026-08-22): R-T2C R3(blocking 4)適用 — [R3-01] ν 主張を
  core-interior 中心 pair(十分先で ζ_n ∈ W_core,n(ρ)、witness flag)に
  型限定し、固定円板 D(ζ_*,ρ/2) の Hurwitz で min ord = 0 を導出。
  [R3-02] carrier 床を eventual 形 m_C(ρ)/2 に半減(inf-liminf の
  pointwise 使用を撤回、M_C は RKHS で全 n)。[R3-03] 両対角列の添字選択
  を K_χ(c₀) 所属 threshold 以降に明示(liminf の無限個実現)。[R3-04]
  floor_witness の消費を列-矛盾 schema に型固定 — eventual 床から
  pointwise (PS-7) への橋は「違反列抽出 → chart 安定化 → tail で矛盾」で
  有限初期区間吸収を schema に内蔵、導出実行は T3 義務。

- v0.29.33(2026-08-22): R-T2C R2(blocking 5)適用 — [R2-01][R2-02]
  (FL22-2) を ρ-erosion core W_core,n(ρ)(compact・min 達成・左閉右開は
  closure 処理)+ 点ごとの円板 D(t,ρ) zero-freeness(U_c membership と
  t 側の erosion 距離で成立)+ 移動円板 Hurwitz(固定円板 D(t_*,ρ/2) 上
  の矛盾論法 — 可変 W_reg,n 上の Hurwitz を撤回)に再構成。core 非空性・
  帯域 routing は T3 義務として witness 記録。[R2-03] (FL22-5) と §4 台帳
  の stale 強形を eventual σ₀/(2C_R) 形に同期(有限初期区間は T3 吸収の
  型付き契約)。[R2-04] ν を defect-order 形で直接定義(和の極限 F_* を
  撤回 — δ_n 下界は非主張、δ は二窓比相殺で和の ord は不要)。[R2-05]
  σ₀=0 対角列の atlas 再通過を撤回 — 量化が χ 枝限定なので対角列は構成上
  全要素 χ で frame_input-v2.1 の型を直接満たす。

- v0.29.32(2026-08-22): R-T2C R1(blocking 5)適用 — [R1-01] σ₀ の量化を
  admissible pair(実 config 列 × 中心列)に型固定(閉包点は量化外 —
  稠密性不要)、σ₀ = 0 の対角列構成(chart 残留は要求しない)。[R1-02]
  [R1-03] m_C を raw 正規化 pair で直接証明(raw Gram 鎖 + 実部距離が複素
  距離を抑える complex 帯 zero-freeness + Hurwitz + sequence-inf 型一様化
  — carrier は二択不要で無条件正)。[R1-04] 連鎖を eventual 形 σ₀/2 に修正
  + g = δ|f|/max|B̂| の恒等式と二窓比での δ 厳密相殺を明示。[R1-05] ν ≤ 9
  の主張域を W_reg に限定(bubble 域の還元文言を撤回 — T3 の (PS-5) 消費
  に送る)。

- v0.29.31(2026-08-22): **§8.23 GC-5-T2c BORD22-FLOOR 起草** — chart 別
  σ₀ の二択(床 or 実 config 由来 overflow candidate — 空性証明はしない)、
  carrier 床 m_C(Hurwitz + 単位 norm + 下半連続 inf)、量的連鎖(raw
  座標)、ν ≤ 9((HA-3) 消費 — 3+1 valuation lemma obligation を不要化で
  解消、初等証明付記)、対偶 headline、floor_witness-v1(floored |
  deferred)。

- v0.29.30(2026-08-22): **GC-5-T2b-ii CARRIER-CHART 受理**(R-T2BII R3
  PASS、fixed SHA `ccb1b6d`、3 round)。**T2b chain 完結**(T2b-0 3R /
  T2b-i 1R / T2b-ii 3R = 計 7R — consult #18 見積 6–10R 内、2 経路撤回
  込み)。次 = T2c BORD22-FLOOR(head_good × carrier_witness の消費)。

- v0.29.29(2026-08-22): R-T2BII R2(blocking 4)適用 — [R2-01] d₀ ≤ t₀/√5
(帯全体で (B3-4a) 適用域を保証)。[R2-02] K_χ(c₀) の閉集合族化(係数
  下界 c₀ witness — 除外でなく被覆、rank-drop 面はどの K_χ(c₀) にも
  現れない)。[R2-03] v1.1 の不変 field 列挙に section_param_bound_ref を
  明示。[R2-04] vanish_flag = none も checked 化(両成分非消滅 + routing
  不在の evidence)。

- v0.29.28(2026-08-22): R-T2BII R1(blocking 5)適用 — [R1-01] carrier
  chart constructor(SEP/CONF の閉集合型・重複帯被覆・rank-drop 面の
  atlas exit 明示)。[R1-02] B bound を明示(C_B = R_ℱ/Δ + 2R_ℱ/√Δ、
  Δ = δ_ℱ(2−δ_ℱ))+ frame_input-v2.1 の完全型(v1.1 record・型不変条件・
  consumer 置換 — §8.21 の参照を v2.1 へ、[R-GC4A5A0 R3-01] 前例)。
  [R1-03] center_scale_map 案を撤回し **raw 再主張系**へ(defect は raw で
  (HA-3) 逐語適用、carrier は U_n^{-1} 引き戻し — pointwise gauge 移送の
  全面禁止、EW-B 準拠)。[R1-04] carrier_witness を checked constructor 化
  (floor_checked / vanish_flag の atlas 一致検証)+ T2c 消費 branch の型
  明示。[R1-05] 台帳同期(T2b-ii 行の obligation 解消・依存追加、T2b-0 行
  pointer 更新)。

- v0.29.27(2026-08-22): **§8.22 GC-5-T2b-ii CARRIER-CHART 起草** —
  成分直交 block 対角の正式消費、成分別 frame(単原子 / 分離 2 原子 /
  (B3-4a))、chart 一様 Gram 床(下半連続 inf — carrier に overflow locus
  なし)、**箱供給補題**(Möbius margin 1−|A′| ≥ δ_ℱ²/2 — T2b-0 の半箱
  前提を standard box + 本補題の frame_input-v2.1 で versioned 置換、
  obligation 解消)、center_scale_map、carrier_witness-v1。

- v0.29.26(2026-08-22): **GC-5-T2b-i HEAD9-ACTUAL 受理**(R-T2BIA R1
  PASS、fixed SHA `e5de2f6`、**1 round**)。consult #18 の弱体化再設計が
  一発通過 — 実 defect 限定 + weak/compact-open で crux が閉じた。次 =
  T2b-ii CARRIER-CHART。

- v0.29.25(2026-08-22): **§8.20 HEAD9-FRAME 撤回**(R-T2BI R1 blocking 5
  — tail-tightness recurrence の反例ほか)+ consult #18(Sol)記録:
  full-span strong compactness は PTN-22 非消費の過剰目標として非目標化、
  実 defect 限定の weak compactness へ再設計、PS-9 bridge の独立 packet 化
  (T2c-ov 新設)、係数規約 q = (A/2)z² + Bz 正本化、weighted Fock 型登録、
  packet 再編(T2b-i HEAD9-ACTUAL / T2b-ii CARRIER-CHART / T2c /
  T2c-ov)。**§8.21 GC-5-T2b-i HEAD9-ACTUAL 起草** — β_n = ‖J⁹_{ζ_n}f_n‖
  の head_good | head_overflow 二択、weak/compact-open 極限(f_* ≠ 0・
  ord ≤ 9)、typed overflow candidate、head_outcome-v1。

- v0.29.24(2026-08-22): **§8.20 GC-5-T2b-i HEAD9-FRAME 起草** — α_n(J⁹
  最小特異値)の framed | overflow 二択、W_c(4) 消費による有限 n 単射性、
  graph operator frame(G ≥ I 自動)、**tail-tightness 補題**(分離
  cluster 角度下界 + cluster 内定数係数 annihilator ODE の係数 recurrence
  幾何減衰 + e^{Az²} の δ_ℱ margin 移送)、overflow witness(no-go bridge
  — 消費規則で循環切断)、frame_outcome-v2 / frame_witness-v2。

- v0.29.23(2026-08-22): **GC-5-T2b-0 GAUGE-SCALE-ADAPTER 受理**(R-T2B0
  R3 PASS、fixed SHA `7103b2e`、3 round)。半箱前提の供給は T2b-ii
  obligation として open(adapter は条件付き constructor)。次 = T2b-i
  HEAD9-FRAME(crux)。

- v0.29.22(2026-08-22): R-T2B0 R2(blocking 3)適用 — [R2-01] 撤回 marker
  を (B22-2b) 直前へ移動(派生 claim 全体を効力なしに)。[R2-02] bridge の
  d を変換後差分から再計算する d_frame に変更(d_parabolic は参考値 —
  gauge 前後の保存を主張しない、EW-B 整合)。[R2-03] 半箱前提の供給主張を
  撤回し(F2²/A.0 は sup|η̃| ≤ 1/8 のみ)、供給 obligation を T2b-ii の
  chart 箱定義に登録 — adapter は条件付き constructor として fail-closed。

- v0.29.21(2026-08-22): R-T2B0 R1(blocking 5)適用 — [R1-01] §8.18 の
  撤回範囲を (B22-2b)〜(B22-5) 全体に拡大(派生 claim・TR3 deg ≤ 4 も
  効力なし明示)。[R1-02] node_scale_bridge を合流 node 限定にし
  verified: d ≤ 1 を必須 field 化。[R1-03] box 所属を半箱前提
  (|A| ≤ (1−δ_ℱ)/2 — F2²/A.0 供給の verified premise)+
  section_param_bound_ref で証明構造化。[R1-04] pivot と node 代表葉対の
  tie-break を label 全順序で決定的に。[R1-05] root_scale_limit :=
  far | collapse の typed constructor と chart_sublabel field を追加。

- v0.29.20(2026-08-22): **§8.19 GC-5-T2b-0 GAUGE-SCALE-ADAPTER 起草** —
  frame_input-v2 / common_gauge_record-v1 / node_scale_bridge の型定義、
  bridge 不等式 d²/2 ≤ t ≤ (√5/2)d(初等証明、二側比較は非主張)、
  pivot 決定的規約と U_n 共通適用の前処理補題(box 所属・scalar 吸収・
  strong section)、TR3(root_far | root_collapse) versioned sublabel。

- v0.29.19(2026-08-22): **§8.18 tree-Newton 経路撤回**(R-T2B R1 blocking
  6 — 独立性論法の反例・停止測度未定義)。consult #17(Sol)裁定を §8.18
  追記に記録: J⁹-SVD/graph frame + framed | overflow 二択(循環の切り方
  込み)、tail-tightness 補題、d/t 型分離 + node_scale_bridge、TR3 二分岐
  (root_far deg ≤ 5 / root_collapse deg ≤ 9)、frame_input-v2 adapter、
  chart 一様 Gram floor 条件、**T2b の 3 分割**(T2b-0/T2b-i/T2b-ii —
  §4 台帳に行追加、T2c に 3+1 mixed-span valuation lemma 義務追加)。

- v0.29.18(2026-08-22): **§8.18 GC-5-T2b BORD22-FRAME 起草** — 構造原理 =
  「carrier は ℱ⊕ℱ 成分直交で Gram block 対角(成分別 ≤ 2 原子 = BORD-3
  資産)/ 新規性は defect(和)側の ≤ 4 原子 cluster frame に集中」。
  二段正規化(B22-0)、成分別 carrier frame(B22-1)、tree-Newton frame +
  方向衝突 sub-recursion(B22-2b — 新規補題)、chart 別 frame 族
  (B22-2c)、Gram 鎖の J⁹ 版(B22-3)、exact limit span 表(B22-4)、
  frame_witness-v1(B22-5)。ord 上界・m_C・床は T2c 送り(非主張)。

- v0.29.17(2026-08-22): **GC-5-T2a BORD22-ATLAS 受理**(R-T2A R9 PASS、
  fixed SHA `08c2d0e`、9 round)。被覆完備性 (AT) が確定 — T3 列は
  lower-rank / exact-QR / 有限 chart 族 𝒜₂₂ = {PL4, CF1, CF2, XC1, XC2,
  TR3, RTC, QRT, CZB} のいずれかへ必ず入る。次 = T2b FRAME(crux)。

- v0.29.16(2026-08-22): R-T2A R8(blocking 3)適用 — [R8-01] 残存 U_j
  表記を cluster 化(row 4 predicate・W-relevance 見出し)、(δ) の検証行
  を membership 形(Re z_j ∈ U_{c(j)})に変更(中点偏差で distance 形が
  破れる問題の解消)。[R8-02] handoff を option 型化(None | Some、
  total accessor Σ(None) = ∅ / transfer_clusters(None) = ∅)、
  receiver_check を pending | checked(evidence) の union 化。[R8-03]
  **C_atlas := C ∖ dom(transfer_clusters)** を明示し U_c/r_c/radii/
  (α)(δ)(γ) の全 domain を C_atlas に限定(transfer cluster は U も r も
  持たない — r_c → 0 参照の消滅)。

- v0.29.15(2026-08-22): R-T2A R7(blocking 3)適用 — [R7-01] cluster 表記
  を被覆定義全体に伝播(U_c/r_c/⋃U_c/W_reg/端点表/record field)。
  [R7-02] handoff を単一 record 型に再構成(Σ を record レベルで束縛、
  transfer_clusters map で複数 cluster 対応、receiver_check を field と
  して明示)。[R7-03] 境界接近 cluster(r_c → 0)を transfer_clusters へ
  移管し (γ) の正値条件との矛盾を解消(W = [0,1), Re z_n = 1 − 1/n 反例
  の収容)。

- v0.29.14(2026-08-22): R-T2A R6(blocking 2)適用 — [R6-01] Re 投影
  clustering を導入(投影衝突対は 1 cluster に統合 — 例 P̃₁ = t(t−i) の
  零点 0, i を収容。U・radii・invariants を cluster 単位に変更、cluster 間
  距離は構成から正)。[R6-02] handoff を discriminated branch 化
  (boundary_margin | exterior_zero(影響域 ⊂ Σ evidence))、(α)/(γ) の
  index 集合から exterior_zero cluster を evidence 付きでのみ除外可能に。

- v0.29.13(2026-08-22): R-T2A R5(blocking 3)適用 — [R5-01] Σ 精密化を
  §8.16 追記(consult 記録)と §4 台帳行に同期(audit marker 付き)。
  [R5-02] (AT-4) の invariant 参照を (α)(δ)(γ) に修正(削除済み (β) への
  参照を除去)。[R5-03] 半径規約の精密化: 全項 Re 投影後の実距離、空集合
  規約(min 対象が空 = 項が落ちる)、Re z_j ∉ W の W-relevant 零点は境界
  分岐へ routing、(δ) の検証行を dist(Re z_j, W_reg) ≥ r_j 形に変更。

- v0.29.12(2026-08-22): R-T2A R4(blocking 4)適用 — [R4-01] 入力を
  window_geometry(W_zf field を除いた部分型)に分離し循環を排除(完全な
  window_contract は wzf_cover と合成して下流が構成)。[R4-02] 零点対距離
  を chordal(ℂP¹)距離に変更(「discriminant → 0 と同値」を撤回 —
  P̃₁ = 1 + εt² 反例は degree-drop へ routing、消滅 flag は有限極限点のみ
  発火、Re は有限 affine chart 限定)。[R4-03] W_reg を補集合として定義、
  Σ を移管領域と明示((AT) は「W ∖ Σ の被覆 + Σ の帰属排反」に精密化、
  pending receiver で Σ を被覆済みに数えることを型上不可能化、
  receiver_check constructor(Σ ⊂ W′ evidence))。[R4-04] invariants を
  引数型・結合条件込みの constructor に固定((β) checked_cover を (δ)
  checked_zero_free に置換 — 証書対象は W_reg の零点自由性)。

- v0.29.11(2026-08-22): R-T2A R3(blocking 4)適用 — [R3-01] 再判定の
  well-founded measure を Σm_i に固定(発火は within-child pruning のみ、
  部分的 cross-child 相殺は発火させない)。[R3-02] same-side 零点対距離を
  compact 化量に追加(重根化 flag は係数退化と独立 — 反例
  P̃₁ = (t−2)² − ε² を収容)+ routing predicate 明示(chart 割当不変・
  被覆側で重複度統合)。[R3-03] W-relevance 前置と
  U_j := B(Re z_j, r_j) ∩ W の構成的定義(⊂ W 自明化)、handoff に
  receiver_ref(pending 可・A.5c 消費時必須の fail-closed 規則)。
  [R3-04] invariants を typed constructor 化(checked_subset /
  checked_cover(端点表 evidence)/ checked_positive)。

- v0.29.10(2026-08-22): R-T2A R2(blocking 5)適用 — [R2-01] s_ab を §6
  の d_w = max(|ΔA|^{1/2}, |ΔB|) と同一物として型接続(A = 二次係数、
  root 正規化 s₀ = max s_ab、未 matched 対の s_ab > 0)。[R2-02] support
  rank := within-child 安定化後の ≃ 類総数(cross-child 相殺は数えない)
  — exact-QR(rank 4)と行 1 の排反を確定。[R2-03] 零点衝突を cross-side
  (→ CZB)と same-side 重根化(→ 重複度付き U_j + 係数退化 flag)に分離。
  [R2-04] r_j に dist(z_j, ∂W) を追加(U_j ⊂ W が定義から従う)、handoff
  を型付き record 化(margin Σ・target cell_id・帰属排反)、invariant (β)
  に Σ を明示。[R2-05] exit を discriminated union 化(exact_qr は
  qr_global_witness ref を constructor 引数に)、invariants を checked
  constructor 化。

- v0.29.9(2026-08-22): R-T2A R1(blocking 5)適用 — [01] constant-gauge
  同値・matching edge・係数 witness の型定義、exact-QR exit に
  qr_global_witness ref 必須化。[02] rate atlas を child 割当と独立な
  4 点 cluster tree に一般化(反例の cross-child 細 scale cluster を
  XC1/XC2 類として chart 族に追加、全 internal node に scale)。[03]
  compact 化対象量の型固定(係数単位球・ℂP¹ 零点・[0,∞] 比)+ 割当を
  決定 list 化(SD の (i) 終端性 = rank 厳減、全域性 = 木型の有限網羅)。
  [04] W_zf 被覆の部分列一様化(分離極限 = n 一様半径 / 衝突 = CZB
  routing / 境界 = handoff / S̄ 接近 = zf invariant (i))+ wzf_cover の
  verified invariants (α)(β)(γ)。[05] atlas_witness に window_contract
  identity ref 追加、g → 1 の越境主張を削除、fail-closed を invariant
  検証込みに強化。

- v0.29.8(2026-08-22): **§8.17 GC-5-T2a BORD22-ATLAS 起草** — 被覆完備性
  (AT) の一主張(step-0 有限安定化 + cross-child matching、cluster tree
  有限再帰 blow-up、chart 割当表 PL4/CF1/CF2/RTC/SD/QRT/CZB、W_zf 静的
  被覆(|V| ≥ 0.27 全 branch cell 全域 ⇒ 零点 ≤ 4)、atlas_witness-v1)。
  **§9 BORD22-FLOOR-PROBE 記録**(結果の正本は §9)。

- v0.29.7(2026-08-22): **consult #16(BORD-22 骨格、Sol)記録** — §8.16
  追記(二段正規化 carrier/defect、cross-child matching(合算禁止)、
  3-scale rate atlas、床 ν_ζ ≤ 9(予算)、W_zf 帰属分割、no-go 監視点)。
  §4 台帳: GC-5-T2 を **T2a ATLAS / T2b FRAME / T2c FLOOR** に 3 分割
  (+T3 で計 4 packet)。次の着工 = T2a(被覆完備性の一主張のみ)。

- v0.29.6(2026-08-22): **GC-4A.5a1 PBK22-PTN-SPEC 受理**(R-GC4A5A1 R4
  PASS、fixed SHA `5d7400a`、4 round)。BORD-22/PTN-22 の interface 型が
  固定され、次の着工対象は GC-5-T2 BORD-22 本体(T3 = 2|2 限定 border
  分類 — crux)。

- v0.29.5(2026-08-22): R-GC4A5A1 R3(blocking 2)適用 — [R3-01] (PS-9) の
  相互排他を branch constructor で型表現(valid.scan = checked_clear 専用 /
  nogo.scan = detected 専用 — prose 後置き制約を廃止)。[R3-02] テストを
  構造化: PS block 単位の分割検査(PS-3 の active_children_nonzero と生成
  禁止条件の結合、PS-5 被覆条件、PS-9 の valid/nogo sub-block に対する
  constructor 排他(valid 側に detected 不在・nogo 側に checked_clear
  不在)、消費規則の同一 block 内結合)。

- v0.29.4(2026-08-22): R-GC4A5A1 R2(blocking 3)適用 — [R2-01] (PS-3) の
  required keys 列挙に active_children_nonzero を消費条件付きで追加。
  [R2-02] nogo_scan record を checked_clear | detected の discriminated
  status 化(valid は checked_clear 必須 — detected は nogo variant へ強制)。
  [R2-03] テストに active_children_nonzero / common gauge quotient /
  (PS-5) 2 chart / (PTN-22) statement / v ≡ 0 生成禁止 / checked_clear
  必須 / nogo 消費禁止の検証を追加。

- v0.29.3(2026-08-22): R-GC4A5A1 R1(blocking 6)適用 — [R1-01] 𝐁 を §8.3
  の未約分 pair に戻し raw/reduced の 2 層型化(d₀ = ord D は未約分 pair と
  同一オブジェクト、𝐁̃ の近接共通零点は別 field)。[R1-02] zf_scope 分割
  (A.3a の保証域は S/collar のみ — W_zf 被覆 witness を独立 field 化、供給
  は BORD-22/A.5b の義務)+ we9/d10/λ/ℓ_ext の同一オブジェクト参照明示。
  [R1-03] t3_witness を GC-3 D-PBK-22 required keys への identity ref に変更
  (自由 flag 禁止)、台帳依存に GC-3/GC-4C.0 追加。[R1-04][R1-05]
  ptn22_witness-v1 を valid | nogo の discriminated union 化(valid は
  v ≢ 0 必須 + nogo_scan record、nogo は証明経路での消費禁止)。[R1-06]
  (PS-4)・v0.29.2 の probe 結果再記述を削除(正本 = §9)。テストを実質化。

- v0.29.2(2026-08-22): **§8.16 GC-4A.5a1 PBK22-PTN-SPEC 起草**(consult #15
  の再設計第一歩 — BORD-22/PTN-22 interface 型の固定、proof claim なし):
  raw projective pair(gcd 大域連続化の放棄)、stratum_record(d₀ 同一
  オブジェクト)、t3_witness、window_contract(zf 条件型必須・disjoint
  禁止・λ/s 換算閉包)、projective common-zero 拡張(outer/inner 2 chart)、
  exact QR exit、(PTN-22) statement 登録、ptn22_witness-v1(no-go field
  付き)。§4 台帳に A.5a1 / GC-5-T2 BORD-22 / GC-5-T3 PTN-22 行を追加。
  **§9 BORD22-PROBE 行を記録**(結果の正本は §9 — 本欄では再記述しない
  [R-GC4A5A1 R1-06] で数値の再記述を削除)。

- v0.29.1(2026-08-19): **COND9 定理 draft 撤回** — R-GC4A5A R1(blocking 7:
  gcd 遷移の config 連続性反例・metadata/関数族 compactness 混同・Taylor 剰余
  の W-norm 流用・W branch 未定義・d₀/λ/s interface・型/台帳)により
  (C9-3)〜(C9-5) の証明経路は不成立(失敗経路として記録保存)。consult #15
  (Sol、`sol-cond9-consult.md`): 必要資産 = **PTN-22**(projective/weighted
  二窓比較)+ **BORD-22**(T3 = 2|2 限定 border 分類 — full FR4 の前倒しは
  不要、T3 で閉じなければ昇格)。gcd 遷移は raw projective pair + inner
  bubble chart で扱う。COND9 は reduction packet に降格、BORD-22/PTN-22 を
  A.5a の blocking obligation に登録。リスク: COND9 定理自体は黄〜橙(反例
  なし — §9 COND9-PROBE 整合)、no-go 判定基準を明文化(exponent > 9 bubble
  または定数 0 落ち列)。

- v0.29.0(2026-08-19): **GC-4A.5a0 PBK22-QRG 受理**(R-GC4A5A0 R4 PASS、
  fixed SHA `68d114a`、4 round — R3 で reviewer 明示指示による WE9 v4 置換を
  含む)。**§8.15 GC-4A.5a PBK22-COND9 起草** — g の三分法(g < 1/2 ⟹
  |H| ∈ (1/2,2) ⟹ g ≍ |1+H|)、列コンパクト性(固定 scale = 一様連続 +
  恒等定理、縮小 scale = (p, v) 分解: p は C₂-Markov (L/s)²、v は正規化極限の
  S-消滅次数 ≤ 9(W_c(4)/W_CONFL/混合/Π₄/ZG-NF/A.5a0 の strata 被覆)+
  compact 下半連続 inf)、cond9_witness 契約。

- v0.28.9(2026-08-19): R-GC4A5A0 R3(blocking 1)適用 — **WE-0/WE-4 の
  GCRouteRecord 参照を v3 から v4 へ本文置換**(accepted §8.13 内の参照
  2 箇所 + 目的文 1 箇所。R2 の宣言型追記では consumer 型が閉じないという
  reviewer 明示指示による編集 — inline marker [R-GC4A5A0 R3-01] を各所に
  付し、§8.13 追記を「置換済み」に更新。数学的内容・v3 定義は不変)。テストを
  consumer 型検証に強化(WE9 節内に v3 生参照が残らないこと)。

- v0.28.8(2026-08-19): R-GC4A5A0 R2(blocking 1)適用 — §8.13 追記(accepted
  本文不変)で WE-0/WE-4 の record 参照を GCRouteRecord-v4 に versioned 更新
  (消費契約の型整合)。整合検出テストを追加(§8.13 節内に v4 参照が存在する
  こと)。§9 に COND9-PROBE 診断行を追加(one-hop 比 R(s) の実測: adversarial
  slope ≈ 1 ≪ 9、confluent 許容でも max ~10³ vs 予算 10¹⁸⁺ — no-go 信号
  なし。Nelder-Mead は ord-9 同調方向を見つけにくいため sharp 指数の証明
  代替ではない)。

- v0.28.7(2026-08-19): R-GC4A5A0 R1(blocking 5)適用 — [01] QRG-1 の成立域を
  実区間 W に訂正(恒等定理は零集合の集積点形で適用 — A.2a は複素 collar 上の
  v ≡ 0 を供給しない)。[02] WE-3 接続を型付き field 化(source 一致 +
  I_k 接続 — Log 不要の恒等式形が要求より強いことを明記)。[03]
  **GCRouteRecord-v4** を versioned 宣言(v3 不変 + JF₉ 分岐 flag +
  qr_global_witness required — closed-world fail-closed)、α は v3 field への
  同一オブジェクト参照に(独立値を持たせない)。[04] A.5 を集約
  {A.5a0, A.5a, A.5b, A.5c} として §4 で正式定義(accepted 本文の旧「A.5」
  参照を有効なまま保つ)、A.6 依存を更新。[05] claim-surface テストに QRG
  schema 存在検査を追加(「29 tests」を QRG の検証根拠として引用しない)。

- v0.28.6(2026-08-19): consult #14(Sol、`sol-boot-consult.md` — A.5 設計):
  生 Taylor hop は**棄却**(剰余が chart スケールで支配)、full-tube root
  repulsion は**反例で偽**(paired complex roots の G/gcd-near 配置 —
  H = −(t−iδ)/(t−i(δ+η)) は η ≪ δ で任意深平坦のまま root が実軸接近)。
  採用骨格 = **projective one-hop conditioning(主)+ 有限次元 norm 比較
  (従)+ RESTART/CHAIN(外側)**。κ-small ⇒ parameter-distance small は
  accepted 資産から出ない(A.2c は κ ≤ C·dist のみ — 逆向き不成立)ことを
  確認。A.5 を **A.5a0 QRG / A.5a COND9(黄赤 — 最大 no-go gate)/
  A.5b RESTART / A.5c CHAIN** に再分解(§4 台帳)。予想 round 合計 8–13。
  §8.14 A.5a0 を起草(恒等定理による exact QR 大域化 — H = −e^p の pole 除去
  可能性・分枝不要化・WE-3 閉鎖)。

- v0.28.5(2026-08-19): **GC-4A.4 PBK22-WE9 受理** — R-GC4A4 R2 PASS(luna
  gpt-5.6-luna xhigh、fixed SHA `9f1a18d`、blocking なし、2 round)。
  we9_witness-v1(κ_WE 式・二次比枝 kernel 6600ρ⁻²)が A.5/A.6 の入力として
  確定。GC-4A 残 = A.5(BOOT)・A.6(ASM)。

- v0.28.4(2026-08-19): R-GC4A4 R1(blocking 5)適用 — [01] WE-3 の展開中心を
  c_k = center(J_k) に変更(t₀ = center(S) ≠ center(J_k) — 任意中心 Markov で
  処理、t₀ は WE-3 で不使用)。[02] WE-1 の係数を中心 Taylor 係数として明示。
  [03] we9_witness-v1 に d₀ の型付き provenance(divisor_record 参照・S 中心
  読み直し・gcd transition 時の current rank 指名)。[04] §4 依存欄に
  A.0/A.1 追加。[05] v0.28.0 記載の旧 ℓ_ext 式に訂正注記。

- v0.28.3(2026-08-19): GC-4A.4 PBK22-WE9 起草 — §8.13: (WE-1) Chebyshev
  係数補題(‖T_k‖₁ 表による初等自己完結、C₉ = 4756、C₂ = 10)、(WE-2)
  深平坦 ⇒ κ ≤ κ_WE(θ; σ)(JF₉ target v ≢ 0 枝 + d10 R̂(θ) の消費 —
  定量的 near-QR)、(WE-3) 二次比枝の kernel 不等式 ‖g‖_I ≤ 6600ρ⁻²‖g‖_J
  (分枝接続は A.5 供給の型付き条件)、(WE-4) we9_witness-v1 契約。

- v0.28.2(2026-08-19): **GC-4A.3b PBK22-D10 受理** — R-GC4A3B R2 PASS(luna
  gpt-5.6-luna xhigh、fixed SHA `b75aa85`、blocking なし、2 round)。
  d10_witness-v1(collar 10 階上界・scale cap)が WE₉(A.4)の入力として確定。

- v0.28.1(2026-08-19): R-GC4A3B R1(blocking 5)適用 — [01] λ の向きを訂正
  (A.2b は y = λ(t−t₀) — 外挿半径は ℓ_ext = min(r_S/2, **1/λ**)、正規化座標
  |y| = λ|x−t₀| ≤ θ)、(N-0) r ≥ 2 の前提を明記(低 arity は適用外)。
  [02] D1/D2 の数値を厳密値で評価(e^{−7/8}/(1−e^{−7/8}) = 0.7149 ≤ 0.72 —
  0.42/0.58 = 0.724 の丸め破綻を修正)。[03] M_r′ を検証式付きで定義
  ((δa,δb) = r 係数の exact 減算、T_C = collar sup、M_r′ = |δa|T_C+|δb|)。
  [04] branch を pair ごとに独立化(branch_1, branch_2、per-branch
  M_{logV,i}′、M₁ の per-branch 式)。[05] Taylor 適用域を契約化(t₀ =
  center(S)、実軸、線分 ⊂ S — ℓ_ext ≤ ρ/52 < |S|/2)。d10_witness-v1 に
  versioned 化、§4 依存欄を同期(A.1/A.2a 追加)。

- v0.28.0(2026-08-19): GC-4A.3b PBK22-D10 起草(orange GO — GC-4A 鎖の完成を
  GC-5 本体より先行する裁定)— §8.12: collar unit 両側 bound(E-branch の
  初等場合分け |E| ∈ [1/25, 48]、D1/D2 の指数評価、数値診断で margin 確認)、
  reduced 零点距離 ρ/26 による log 微分 bound、**u′ 経由の Cauchy 10 階**
  (log の分枝定数を回避)、scale cap ℓ_ext = min(r_S/2, λ)(→ v0.28.1 で min(r_S/2, **1/λ**) に訂正)と正規化剰余
  R̂(θ) = (M₁r_S/10240)θ¹⁰、型付き d10_witness 契約。

- v0.27.8(2026-08-19): **GC-5-T1 TN-3 受理** — R-TN3 R2 PASS(luna
  gpt-5.6-luna xhigh、fixed SHA `906bd1a`、blocking なし)。**TN-3 blocking
  downstream obligation は解消** — §8.9 追記 2 で (AD-2) N_T < ∞ の無条件化
  と (AD-4) 条件充足(B.0 = feasibility go)を記録、§4 台帳(GC-5 受理条件・
  B.0 行)を同期。go/no-go 最小集合の唯一の条件付き要素が外れ、**第一段 go
  判定は無条件化**。

- v0.27.7(2026-08-19): R-TN3 R1(blocking 1)適用 — §8.9 末尾に**追記**
  (accepted 本文 `eee39bf` は不変): (2c) の K の「閉 chart 箱」を Fock 可容
  箱(|A| ≤ 1−δ_ℱ、|B| ≤ R_ℱ — K_{δ,R} と同じ束縛)に固定。未指定だった
  chart 箱定数の指定であり受理済み主張の変更ではない。T1-1 に接続を明示、
  T1-2 の sup 定義域を明記(minor)。

- v0.27.6(2026-08-19): **GC-5-T0 BORD-3 受理** — R-BORD3 R6 PASS(luna
  gpt-5.6-luna xhigh、fixed SHA `87863cc`、blocking なし)。6 round の主要
  訂正史: R1 = frame span 吸収と定量鎖への転換、R2 = Fock ノルム正規化
  (dilation 全廃)、R3 = P3/P4 の raw-gauge (L-d) 分類 + (B3-4a) 自前証明、
  R4 = Gram 鎖・RKHS 評価式・chart 包含の明記、R5 = 表記修正。**§8.11
  GC-5-T1 TN-3 を系として起草**(BORD-3 の (B3-2)–(B3-4) が任意列で成立する
  ため curve selection・部分解析幾何は不要化 — consult #13 α′ の簡約)。

- v0.27.5(2026-08-19): R-BORD3 R5(blocking 2 — 表記レベル)適用 — [01] P4 の
  t_m ≍ τ/s を撤回し 0 < t_m ≤ C·(τ_m/s_m) → 0 に(純二次差分 δB = 0 で ≍ は
  偽 — 包含には上界で十分)。[02] unitary section の式を訂正:
  w_{ℓ,n} := U_n^{-1}v_{ℓ,n} → U_*^{-1}P_ℓ = Q_ℓΦ(ξ*)(U_nU_n^{-1} は
  書き誤り)。

- v0.27.4(2026-08-19): R-BORD3 R4(blocking 3 — いずれも記述不足の明記要求)
  適用 — [01] B3-6 の F3′ witness と z_c の接続(ζ_n = z_c(p_n) ∈ {βω^j} →
  0 = ord-5 点)。[02] 係数有界性の Gram 鎖(G_n → G_* > 0、
  1 = b^*G_nb ⟹ b 有界 ⟹ strong 極限 ‖v‖ = 1)と P3/P4 の unitary section
  経由の frame 収束鎖を明記。[03] moving-center RKHS 連続性の評価式
  (微分評価核の norm 連続性・有界性)と P4 の 𝒦_{η,t₀} 包含
  (η = (N0) 部分列下界、t₀ = min(1/4, η²/8)、t_m → 0 ≤ t₀)を明記。

- v0.27.3(2026-08-19): R-BORD3 R3(blocking 5)適用 — [01] P4 の W′ 適用を
  撤回(raw 極限で r ≡ 0 — R3 反例)。P3/P4 を **FR raw-gauge (L-d) 分類**に
  再構成: SVD frame の strong unitary section(FR §8.4/§9.3–9.5、A′-4)で
  raw ℱ-strong 極限 Q_ℓΦ(ξ*)(deg Q_ℓ ≤ 5)— 多項式次数から任意中心
  ord ≤ 5。[02] (A″1) の root-normalized 資産を raw scale に流用せず、
  **2 原子 confluent 補題 (B3-4a) を自前で証明**(積分表示 + Fock 入力条件で
  ℱ-strong 連続)— P2/m=2 の frame を閉鎖。[03] Fock 入力条件(|A| ≤ 1−δ_ℱ、
  |B| ≤ R_ℱ — FR K_{δ,R} と同じ束縛)を (B3-1) の型に明記。[04] merge/prune
  を反復安定化(合併係数零 c_a + c_b = 0 の pattern 固定)。[05] λ_n → |λ_n|
  表記修正。非 blocking: B3-6 に F3′ witness の (B3-1) 形対応を記載、§4
  依存列を拡張。

- v0.27.2(2026-08-19): R-BORD3 R2(blocking 3)適用 — [01] 証明 step 0 に
  exact-merge routing を復元(部分列で一致/零係数 pattern 固定 → 合併・
  prune、m ∈ {1,2,3}、m ≤ 2 の低 arity 鎖を明示 — raw K の exact-merge 面で
  d/s 比・Newton frame が未定義になる漏れを解消)。[02][03] w/x 座標 dilation
  を全廃(向きが逆・正しい向きでは raw jet に s⁵ 重み — R2 反例 ‖J⁵‖ ≍ s²)
  — **Fock ノルム正規化**に置換: RKHS 評価 sup ≤ C_R‖f‖_ℱ + 単位 ℱ-球面上の
  moving-center jet floor(背理法: 各 pattern の frame の strong 収束
  ((A″1)/A′-4)+ 極限 span 分類(W_c(3)/W′/FR-S1′ e^qΠ₅)+ RKHS jet 連続性
  で床)。FR-S1′ の消費を復活(P3 の limit span ⊆ e^qΠ₅)。

- v0.27.1(2026-08-19): R-BORD3 R1(blocking 5)適用 — 証明核を全面改稿。
  [01] 係数退化 × λ_n 射影発散の組合せ(R1 反例 span{e^p, qe^p, e^{q₀}})は
  **frame 係数の span 吸収**で処理(分類は距離 pattern のみ、係数は関与
  しない)。[02][03] 「極限を affine 変換で正規形へ」の reduction を撤回
  (h(ζ) = 0 で rescale が h を殺す欠陥)— **列の各項への compact chart 上の
  定量鎖(sup 上界 + moving-center head floor)+ 対偶**に置換。極限の Fock/
  limit span 所属は不要になり、FR-S1′ の消費も不要化(FR-S1″ は (A″1) chart
  連続性のみ消費)。[04] η = 1 主張を撤回し、pivot と ζ_n の不一致は**中心を
  chart の独立座標に含める**ことで解消。[05] K/z_c/Z₀ の型を自己完結に
  (merge/prune 前処理を課さない raw 公式)。FR-S1′ の「等号→包含」も修正
  (minor)。

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
