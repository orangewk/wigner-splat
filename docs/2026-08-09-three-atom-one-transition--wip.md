# 三原子一遷移補題(c = 3)— wip

日付: 2026-08-09 / 著者: 本線 / status: **wip — v0.7.5: plain FR-S1′ R-A′ / nested FR-S1″ R-A″ PASS、split(i) の S4 witnessはopen、次は FR-S4。
F3′ により旧 held 分岐の次数4帳簿は撤回済み。
intended QR5 child への old DC bridge は反例で撤回済み。
五次共鳴が直接反証するのは tree envelope QR5 の指数 4 で、tree 指数の sharp 予想は 5。
tree QR5 は固定 SHA 27a1817 の R-P3 まで PASS。direct U_T→U_F 一様比較は phantom 反例で偽。
DC-NG は固定 SHA 1392266 の R-DCNG(A1–A7) PASS。
次の本体 = cancellation-aware exact block-frame preparation (FR)、多重遷移。旧「Γ(3) ≥ 5」主張は撤回のまま。**

> 位置づけ: 閉包ドラフト §4.3.5.3 の「次の具体タスク」。kernel は
> [K2](2026-08-08-quadratic-phase-turan-K2.md)(c = 2。査読statusは同文書の canonical R-K2 欄を参照)と
> [K2Q](2026-08-09-quadratic-phase-turan-K2Q-weight21--wip.md)(重み (2,1)。査読statusは同文書のcanonical R-K2Q欄を参照)。
> 仕様の土台 = Sol 研究協力回答(2026-08-09、B 節)+ §4.3.5.3 三分岐仕様。

## 1. 主張(案)

F = Σ_{j=1}^{3} c_j e^{q_j}(c_j ≠ 0、q_j 相異なる複素 2 次多項式)、
U_F(t) := max_j (log|c_j| + Re q_j(t))、K 長さ L ⊇ E 長さ ℓ。

**補題 L3a(三原子・一遷移、予想)**:
  ‖e^{−U_F}F‖_{∞,K} ≤ C₃ (L/ℓ)⁴ ‖e^{−U_F}F‖_{∞,E}(C₃ 絶対定数)。
**訂正(v0.4)**: この無条件形は**偽**(§3.6.0 の phantom envelope 反例 — pair の深い係数相殺が
U_F を虚偽に膨らませる)。正しい主張形は「**転送 or 簡約証明書**」の二者択一(§3.6.2)であり、
証明書側は降下 wrapper の表現簡約で処理する。
**訂正 2(v0.6.1、scope 修正)**: 五次共鳴反例
([K(2)+1 文書 §3.5](2026-08-09-pair-block-kernel-K2p1--wip.md))により、
tree envelope U_T を使う QR5 の指数を γ_T(2+1) と書けば **γ_T(2+1) ≥ 5**。
反例 (c₁,c₂,c₃) = (1, −e^{iπ/3}, 1)(1 の原始 6 乗根係数)は**三原子 held(保持枝の内部)**で
比 ~ 0.998·ε⁻⁵(mpmath 検証)。既証明の部分枝(r=2: 8000ε⁻⁴ / r=1(A): 61ε⁻² /
分裂 (i): 100C₂₁s⁻⁴)は**そのまま真**。ただし held 条件だけでは U_T で測ったノルム比を
U_F へ移せず、§3.6.0 の phantom 反例は direct U_T→U_F 一様比較そのものを否定する。
tree QR5 は cancellation-aware block frame の 2+1 節点 kernel に使い、この例から三原子 wrapper の Γ(3) ≥ 5 は
結論しない。Γ(3) の目標指数は open。
「一遷移」= スケール走査 [ℓ, L] で cluster 分裂事象を高々 1 回に
制限した形から始める(§4.3.5.3 (ii): c = 3 の分裂は必ず 3→2+1。三重同時分裂は
閾値の一般位置選択で排除できる見込み — 要検証)。

## 2. 証明アーキテクチャ(三分岐 — Sol B 節を採用)

**分岐 (i) 保持(triple cluster が K まで一体) — 旧次数4ルート撤回**:
旧 prepared-moment 帳簿は `r≤2` から jet degree `≤4` を導いたが、F3′ は moment/order label を越える
cross-degree 相殺で不可避な五次方向を作る。従って「deg 4 Remez を主工具とする」という旧ルートは
active proof ではない。現行の保持枝は
[FR仕様](2026-08-10-three-atom-block-frame-preparation--wip.md)の cancellation-aware exact frame、
plain c=3 補題 W、J⁵-SVD を入口とし、envelope assembly は FR-S4 の open 義務として扱う。

**分岐 (ii) 分裂 3→2+1(split scale s ∈ (ρ, 1))**:
帳簿: ‖Q‖_K/‖Q‖_E = (‖Q‖_K/‖Q‖_{I_s})·(‖Q‖_{I_s}/‖Q‖_E) ≲ s^{−4}·(s/ρ)⁴ = ρ^{−4}
(外側 ε = s、内側 ε = ρ/s — telescoping、二重計上しない)。
- 内側 [E, I_s]: pair は未分裂 → 保持枝の machinery(または pair 側は自明スケール)。
- 外側 [I_s, K]: (2,1) 形 Q₀ = P_B e^{q_B} + c₃e^{q₃}(deg P_B ≤ 2)→ **系 K2Q-wt/aff**。
  実分離・虚分離とも K2Q が周波数一様に処理(dominance peeling の迂回は不要 —
  B2 に渡すのは多 block 段階のみ)。
- 帳簿 metadata: W = 3、d = 2、Δ = 1 − r_B(r_B ∈ {0,1})。r_B = 0 → K2(指数 2)、
  r_B = 1 → K2Q(指数 4)。q_B − q₃ 定数なら d = 1 に正規化してから帰納。

**分岐 (iii)** は証明の分岐ではなく**検証条項**(§4)として分離(Sol 提案採用)。

## 3. 核心 open: Taylor 剰余の吸収(Stab)

共通 weight U の下で Q = Q₀ + R、‖e^{−U}Q₀‖_K ≤ Cε⁻⁴‖e^{−U}Q₀‖_E が既知のとき:
  **(Stab)  ‖e^{−U}Q‖_K ≤ Cε⁻⁴‖e^{−U}Q‖_E + (1 + Cε⁻⁴)‖e^{−U}R‖_K**。
(検算: ‖Q₀‖_E ≤ ‖Q‖_E + ‖R‖_E ≤ ‖Q‖_E + ‖R‖_K、‖Q‖_K ≤ ‖Q₀‖_K + ‖R‖_K の合成。)

含意: 剰余は「原子係数スケールに対して小さい」だけでは**不足**で、
**小区間 E で実測されたノルム ‖e^{−U}Q‖_E に対して** ε⁴ 級に小さい必要がある。
最悪配置(E 上の深い相殺)では実測ノルムが係数スケールより ε⁴ 倍小さくなり得るため、
固定閾値 θ < 1 の cluster 条件だけでは吸収が閉じない(Sol 指摘、自信度 0.65 の難所)。

### 3.1 最悪配置の構成と数値検証(2026-08-09 実施 — 設計判断の材料)

**ST1(naive (Stab) の破綻族 — 解析 + 数値確認)**: sharp 族 Q_τ = (1−e^{τt²})²、
E = [0,ρ]、K = [0,1]。真の比は τ に依らず ‖Q‖_K/‖Q‖_E ≈ (1.0–1.4)·ρ⁻⁴(定理成立)だが、
deg 4 一発切断 + (Stab) の評価は (1+Cε⁻⁴)‖R‖_K ~ τ³ρ⁻⁴ となり真値 τ² を **τ/ρ⁴ 倍過大評価**
(数値: ρ = 0.05、τ = 0.3 で 4.2·10⁴ 倍)。固定閾値 θ の held 領域 τ ∈ (ρ⁴, θ] で無制限に悪化 —
Sol 指摘の定量化。**一発 Taylor + 三角不等式は棄却**。

**ST2(層状転送は閉じる — 解析)**: 同じ族を moment 層 Q = Σ_{k≥2}a_kτ^k t^{2k} に分解し、
**各層を K 単位のまま幾何級数で合算**(ε⁻⁴ の往復増幅を通さない)と、held 条件
τ·diam(K)² ≤ θ < 1 が公比になり Σ_k τ^k ≤ τ²/(1−θ) で閉じる。破綻の原因は剰余の大きさでは
なく (Stab) の帳簿(E ノルムとの比較に ε⁻⁴ を往復させる点)にあった。

**ST3(層間相殺には ρ 非依存の定数床がある — 数値、族限定)**: M₀ = M₁ = 0(valuation r = 2)
の 3 原子族 δ_j = τ(α_jt² + β_jt)、β_j = uα_j + v(このとき layer-2 多項式は
A = S₂·t²(t+u)² と閉形式になり零点を E 内に置ける)で、E ノルムの layer-2 床
τ²|S₂|ρ⁴ に対する最小抑制率をランダム探索 + 局所最適化(各 ρ で 8,000 配置)で測定:
  **min = 0.01471–0.01472 が ρ = 0.1 / 0.05 / 0.02 / 0.01 で一致(4 桁の ρ 範囲で ρ 非依存)**。
含意: layer-3 以降との干渉で床を割る抑制は起きず(次数不一致で B/A が区間上定数に
なれない、の定量版)、**床を割る唯一の経路は S₂ → 0 = valuation 上昇 = (W,d,Δ) の Δ 降下枝**。
限界: 族限定(α_j スカラー型)・数値証拠であり、一般 2 次 α_j(t) と解析証明は次工程。

### 3.2 設計決定(ST1–ST3 に基づく)

**(Stab) を「層状転送補題 + 層床補題」の組に置換する**:
- **補題 LT(層状転送)**: held cluster(公比 θ < 1)で Q = Σ_k M_k-層、各層は deg ≤ 2k の
  多項式 × 共通位相。層ごとに E→K の Remez(指数 2k)を適用し K 単位で幾何合算。
  ε⁻⁴ 増幅の往復を構造的に排除(ST2)。
- **補題 LF(層床)**: prepared chart(M₀ = … = M_{r−1} = 0)で
  ‖e^{−U}Q‖_E ≥ c_r·|M_r-スケール|·ρ^{2r} − (高次層の従属項)。床が不成立 ⇔ 高次層が
  支配 ⇔ 有効 valuation 上昇 — **このときは剰余吸収でなく (W,d,Δ) の Δ 降下枝へ送る**
  (トリガーの定式化 = 「どの層の床が active か」)。数値上の床定数(r = 2、当該族)≈ 0.0147。
- (S-b)(cluster 閾値の再定義)は**不要と判断** — 木構造は §4.3.5.3 のまま。
これは K2Q の (c-i)/(c-ii) 二分岐「深い相殺ほど構造が剛性化する」の c = 3 版であり、
プログラムの哲学(消費 = 降下)と整合する。

## 3.5 保持枝の証明本体(v0.3 — 未レビュー)

設定: 保持枝。gauge を原子 1 に取り(q* := q₁、prepared chart)、
G := e^{−q₁}F = c₁ + c₂e^{η} + c₃e^{μ}(η := q₂−q₁、μ := q₃−q₁、複素 2 次多項式・定数項込み、
原子相異 ⇒ η, μ, η−μ ≢ 0)。
held 条件: **β := max(sup_K|η|, sup_K|μ|) ≤ θ := 1/8**。K 長さ 1(affine 正規化)、E 長さ ε。
valuation: M₀ = Σc_j、M₁ = c₂η + c₃μ。r := min{n: M_n ≢ 0} ≤ 2(3 原子 Vandermonde)。

**重み付きノルムへの変換(luna R1 [blocking] 対応)**: U_F = max_j(log|c_j| + Re q_j) に対し
U_F = Re q₁ + h、h(t) := max(log|c₁|, log|c₂|+Re η, log|c₃|+Re μ)。h は**定数ではない**
(反例: h = 0.05t 型 — luna R1 で確認)が、held 条件から **osc_K h ≤ 2β ≤ 1/4** ⇒
  ‖e^{−U_F}F‖_K/‖e^{−U_F}F‖_E ≤ e^{2β}·sup_K|G|/sup_E|G| ≤ 1.29·sup_K|G|/sup_E|G|。
以下の補題は非重み付き比 sup_K|G|/sup_E|G| を評価し、**重み付き版は ×1.29**(定数に込みで
r = 2: 8000、r = 1(A): 61)。

### 補題 L3a-hold(r = 2)【証明完了 — luna R1 通過(重み補正込み)】

r = 2(M₀ = 0 かつ M₁ ≡ 0)なら **sup_K|G| ≤ 6100 ε^{−4} sup_E|G|**、
重み付き版 **‖e^{−U_F}F‖_K ≤ 8000 ε^{−4}‖e^{−U_F}F‖_E**。

*証明*:
1. **1 変数標準形への還元**: M₁ ≡ 0 ⇔ μ = κη(κ := −c₂/c₃ ∈ ℂ∖{0,1};
   κ = 0, 1 は原子の退化で除外)。M₀ = 0 と併せ c₂ = −κc₃、c₁ = (κ−1)c₃、
   **G = c₃·g_κ(η(t))、g_κ(x) := e^{κx} − κe^{x} + (κ−1)**。
   対称性 g_κ(x) = −κ·g_{1/κ}(κx) により WLOG |κ| ≤ 1
   (|κ| > 1 のときは swap 後の変数 μ = κη に手順 4 の Chebyshev を適用する —
   sup_K|g_κ(η)|/sup_E|g_κ(η)| = sup_K|g_{1/κ}(μ)|/sup_E|g_{1/κ}(μ)| かつ
   (1+|1/κ|)|μ| = (1+|κ|)|η| で条件も保存。luna R1 minor 対応)。
2. **厳密積分表示(Hermite–Genocchi)**: g_κ(x) = κ(κ−1)·[0,1,κ]_ω e^{ωx} より
   **g_κ(x) = κ(κ−1)·x²·∫_Δ e^{(s₁+κs₂)x} ds**(Δ = 単体 {s₁,s₂ ≥ 0, s₁+s₂ ≤ 1}、面積 1/2)。
   (代数検算: [0,1,κ]e^{ωx} = 1/κ + e^{x}/(1−κ) + e^{κx}/(κ(κ−1))、×κ(κ−1) で g_κ ✓。)
3. **pointwise 両側評価**: (1+|κ|)|x| ≤ 1/2 のとき |w(s)x| ≤ 1/2(w = s₁+κs₂)なので
   |e^{wx} − 1| ≤ e^{1/2}−1 ≤ 0.649 ⇒ Re ∫ ≥ (1−0.649)/2 = 0.175、|∫| ≤ e^{1/2}/2 ≤ 0.825。
   ⇒ **0.175·Q|x|² ≤ |g_κ(x)| ≤ 0.825·Q|x|²、Q := |κ(κ−1)|**。
   held 条件で (1+|κ|)|η(t)| ≤ |η(t)| + |μ(t)| ≤ 2β ≤ 1/4 < 1/2 ✓ 全 K 上有効。
   (数値確認: 2·10⁵ サンプルで比 ∈ [0.42, 0.59] — 評価の内側、違反ゼロ。)
4. **η の Chebyshev 外挿**: η 複素 2 次、補題 E(K2)を実部・虚部に適用:
   sup_K|η| ≤ 36ε^{−2}sup_E|η|。
5. 合成: sup_K|G| ≤ 0.825·Q·|c₃|·(36ε^{−2}sup_E|η|)² = 0.825·1296·Q|c₃|ε^{−4}(sup_E|η|)²、
   sup_E|G| ≥ 0.1756·Q|c₃|(sup_E|η|)²(pointwise 下界の sup; 厳密値 (2−e^{1/2})/2 = 0.17564)。
   比 ≤ (e^{1/2}/2)·1296/((2−e^{1/2})/2)·ε^{−4} = 6082.8·ε^{−4} ≤ 6100ε^{−4}
   (丸め帳簿は厳密値で — luna R1 minor 対応)。∎

**注**: 層状転送・層床(§3.2)は r = 2 では**不要になった** — 標準形への還元が pointwise
比較を与えるため。κ → 1(対内衝突 = K2Q 極限)、κ → 0(第 3 原子と定数の衝突)も積分表示が
**一様に**処理する(場合分けなし)。ST3 の数値床 0.0147 の解析的対応物は手順 3 の下界
0.175(×η² の形状因子)。

### 補題 L3a-hold(r = 1)【証明完了 — luna R1 通過(重み補正込み)— 二者択一出力】

r = 1(M₀ = 0、M₁ ≢ 0)のとき、C₂₃ := |c₂| + |c₃|、σ₁ := sup_E|M₁| として、
**次のいずれかが成立**:
- (A) σ₁ ≥ 3C₂₃β²(床 active): **sup_K|G| ≤ 47 ε^{−2} sup_E|G|**(重み付き版 61ε^{−2})。
- (B) σ₁ < 3C₂₃β²(床 inactive): **sup_K|c₂η + c₃μ| ≤ 108 C₂₃β²ε^{−2}** —
  M₁ の小ささの定量証明書。これを「有効 (2,1) 構造への遷移」として使う変換・係数条件は
  **wrapper 側の未証明契約**(luna R1 [major] — 本補題は不等式のみを保証し、
  意味づけは降下 wrapper の設計時に証明する。§5 項目 3–4)。

*証明*: Σc = 0 より G = c₂(e^{η}−1) + c₃(e^{μ}−1) = M₁ + R、
R = c₂(e^{η}−1−η) + c₃(e^{μ}−1−μ)。|e^{x}−1−x| ≤ |x|²e^{|x|}/2 と β ≤ 1/8 より
|R| ≤ 0.57·C₂₃β² on K。
(A): sup_E|G| ≥ σ₁ − 0.57C₂₃β² ≥ σ₁(1 − 0.19) ≥ 0.81σ₁。M₁ 複素 deg ≤ 2 ⇒
sup_K|M₁| ≤ 36ε^{−2}σ₁ ⇒ sup_K|G| ≤ 36ε^{−2}σ₁ + 0.19σ₁ ⇒ 比 ≤ 36.2/(0.81)·ε^{−2} ≤ 47ε^{−2}。
(B): sup_K|M₁| ≤ 36ε^{−2}σ₁ < 108C₂₃β²ε^{−2}。∎

**Sol の三項同時衝突例の整合**: 1 + ωe^{τt} + ω²e^{2τt}(ω = e^{2πi/3})は r = 1
(M₁ = i√3ω·τt ≢ 0)で、τ 小なら (A) 側 — 比 ≤ 47ε^{−2}、真の比 ~ ε^{−1} と整合 ✓。

## 3.6 分裂枝の証明本体(v0.4 — 未レビュー)

### 3.6.0 先行する反例: 素朴な weighted 主張は偽(表現簡約の必要性)

§1 の L3a を「与えられた表現の U_F で無条件に」主張すると**偽**。
**反例(phantom envelope)**: c₁ = 1, q₁ = 0 / c₂ = −e^{−1/10}, q₂ = 1/10(定数差のみ — 原子は相異、
held: β_B = 1/10 ≤ 1/8)/ c₃ = 1, q₃ = −100t。pair は c₁ + c₂e^{q₂} = 1 − 1 = 0 と**恒等的に完全相殺**し
F = e^{−100t}。しかし U_F = max(0, 0, −100t) = 0 on K = [0,1] は phantom な pair 包絡。
E = [0.9,1](ρ = 0.1)で 比 = e^{90} ≈ 10³⁹ ≫ ρ⁻⁴ = 10⁴。
相殺深さ有限(|c₁ + c₂e^{1/10}| = δ > 0)でも δ < e^{−1/ρ} 級で同型の破綻が続く。
2 原子でこの破綻が起きない理由: 完全相殺は包絡の平行(Re q₁ − Re q₂ = 定数)を強制し、
phantom 包絡と生存項の包絡が同形になるため。3 原子では pair 内で平行相殺しつつ
singleton が別形状で生き残れる — c = 3 で初めて現れる現象。
**教訓**: 正しい主張形は「転送 or 簡約証明書」の二者択一(証明の都合ではなく反例が強制する形)。
r = 1 保持枝 (B) と同じ設計思想であり、certificate → 表現簡約(pair 併合)後は上の例でも
U_red = m₃、比 = 1 で転送は自明に回復する。

### 3.6.1 設定と帳簿

**前提(分裂枝の入口)**: recentering 規約(差 η, μ の定数項は E 中心 t_c で評価し係数 c_j 側へ
吸収 — U_F・F は不変)を先に適用し、以下は**すべて recenter 後の座標**で読む。
三原子は **E 上 held**(閉区間、非厳密 sup ≤ 1/8)— これが admissible 集合の非空性を与える
(E 上ですら held でないなら cluster base が E に無く、分裂枝の前提外)。
one-transition scan: s := sup{σ ∈ [ρ, 1]: 三原子が E を含む長さ σ の**閉**区間で held}、I_s ⊇ E 長さ s。
**閉性補題(I_s 上 held)**: σ_n ↑ s の held 区間 I_n ⊇ E は左端点が [0,1] でコンパクト、
部分列極限の区間 I_s ⊇ E(長さ s)上で held 条件(非厳密 ≤)は η, μ の一様連続性により保存。∎
**一遷移仮定**: pair {1,2} は K(長さ 1、affine 正規化)全体で held: **β_B := sup_K|η| ≤ 1/8**。
singleton q₃ には**上側で何の条件も課さない** — K2Q の周波数一様性が分離の定量下界を不要にする
(設計上の要点: 分裂スケールの精密な定義に依存しない)。
帳簿: ε_out = s、ε_in = ρ/s、telescoping で s⁻⁴·(s/ρ)⁴ = ρ⁻⁴(§6.2 K2Q 側と同一)。

**reduction(pair の (2,1) 化)**: P_B := (c₁+c₂) + c₂η(deg ≤ 2)、
F_{≤1} := P_B e^{q₁} + c₃e^{q₃}、R := F − F_{≤1} = c₂(e^{η} − 1 − η)e^{q₁}。
U′ := U_{F_{≤1}} = max(log|P_B| + Re q₁, m₃)、c_B := max(|c₁|,|c₂|)、m_B := Re q₁ + log c_B。

基本評価(K 上 pointwise — 検算済み):
- (a) e^{−U}|R| ≤ (β_B²/2)e^{2β_B} ≤ **0.65 β_B²**(|e^x−1−x| ≤ |x|²e^{|x|}/2 と
  U ≥ m₂ = log|c₂| + Re q₁ + Re η ≥ log|c₂| + Re q₁ − β_B)。
- (b) e^{−U′}|F_{≤1}| ≤ **2**(U′ は F_{≤1} **自身**の包絡 — K2Q (P1)′ と同じ自明上界)。
- (c) U′ − U ≤ log(2 + β_B) + β_B < **1**(|P_B| ≤ (2+β_B)c_B と U ≥ m_B − β_B、m₃ ≤ U)。
- Δ* := sup_{I_s} max(0, U − U′) — 「pair 深消滅 × pair 支配」の同時深度。U − U′ が大きい点では
  |P_B| ≪ c_B(pair の係数相殺)**かつ** m₃ ≪ m_B(singleton が埋没)が同時に起きている。

### 3.6.2 補題 L3a-split-out(外側転送・三者択一)

ω := ‖e^{−U}F‖_{∞,I_s} とすると、**次のいずれかが成立**:

- **(i) 転送**: ω ≥ 2β_B² かつ Δ* ≤ 3 ⇒ **‖e^{−U}F‖_{∞,K} ≤ 100 C₂₁ s⁻⁴ ω**(C₂₁ = K2Q の C₀)。
- **(ii) 三者深消滅証明書**: ω < 2β_B² — 分裂スケール I_s 上で e^{−U}|F| < 2β_B² 一様
  (pair の実振幅 β_B の二乗より深い相殺 = 有効 valuation 上昇の入口)。
- **(iii) pair 縮退証明書**: Δ* > 3 — witness t₀ ∈ I_s で |P_B(t₀)| ≤ 0.06 c_B かつ
  m₃(t₀) ≤ m_B(t₀) − 2.8、従って **|c₁+c₂| ≤ c_B(β_B + 0.06)**(M₀^B の縮退 = 表現簡約 /
  r_B 上昇の入口)。
  §3.6.0 の反例の捕捉(luna R2 [major] 対応 — **座標を統一して読む**): recenter 後は
  η̃ ≡ 0(q₂ − q₁ = 定数)なので下の **η ≡ const 併合 slot** が捕捉(c̃₂ = c₂e^{1/10} = −1、
  |c₁ + c̃₂| = 0 の深い併合 = 簡約証明書)。recenter **前**の表現のまま読むなら (iii) が捕捉
  (Δ* ≈ 5.4、|c₁+c₂| = 0.095)。いずれの座標でも証明書側に落ち、転送は主張されない。

(退化 η ≡ const は K2Q §6.2 の d = 1 正規化: 係数併合で 2 原子に落ち K2 へ;
併合が深い(|c₁ + c₂e^{η}| < e^{−3}c_B)ときは (iii) と同じ簡約 slot。)

*証明 (i)*: 場合分けの前提として **η と μ := q₃−q₁ はともに非定数**とする。μ が定数なら
`c₃e^{q₃}` を exact に `c₁e^{q₁}` へ係数吸収し、残る二原子表示で rank/tree を REFIX するため
K2Q-wt 分岐へ入れない。η は recenter 後 η ≢ 0 と読む — このとき c₂ ≠ 0 より
**P_B = (c₁+c₂) + c₂η ≢ 0** で K2Q-wt の適用条件(P ≢ 0、deg ≤ 2)が満たされる
(η ≡ const は下の併合 slot へ — luna R2 [major] 対応で証明分岐として明示)。
系 K2Q-wt(L/ℓ = 1/s)を (F_{≤1}, U′) に適用:
sup_K e^{−U′}|F_{≤1}| ≤ C₂₁ s⁻⁴ sup_{I_s} e^{−U′}|F_{≤1}|。
I_s 側の重み変換: sup_{I_s} e^{−U′}|F_{≤1}| ≤ e^{Δ*} sup_{I_s} e^{−U}|F_{≤1}|
≤ e³(ω + 0.65β_B²) ≤ e³ · 1.325 ω = 26.61 ω ≤ 26.7 ω(閾値 ω ≥ 2β_B² で剰余 ≤ 0.325ω 厳密;
e³·1.33 = 26.714 は 26.7 を超えるため係数は 1.325 で読む — luna R2 minor 対応)。
K 側の重み変換: sup_K e^{−U}|F| ≤ e^{sup_K(U′−U)} sup_K e^{−U′}|F_{≤1}| + 0.65β_B²
≤ e · C₂₁ s⁻⁴ · 26.7 ω + 0.33 ω ≤ 73 C₂₁ s⁻⁴ ω ≤ 100 C₂₁ s⁻⁴ ω。∎
*証明 (iii) の witness 抽出*: U(t₀) − U′(t₀) > 3 の点で U′ ≥ m₃ より U > m₃ + 3 > m₃、
よって U(t₀) = max(m₁,m₂) ≤ m_B + β_B。U′(t₀) < U − 3 ≤ m_B + β_B − 3 を U′ の両成分に読むと
|P_B(t₀)| < c_B e^{β_B−3} ≤ 0.06 c_B と m_B − m₃ > 3 − β_B ≥ 2.8。
|c₁+c₂| ≤ |P_B(t₀)| + |c₂||η(t₀)| ≤ c_B(0.06 + β_B)。∎

**remark((Stab) 破綻の遮断機構)**: naive (Stab) の τ/ρ⁴ 倍破綻(ST1)は評価 (b) の**天井 2** が
遮断する — 剰余 R は K 単位の絶対定数 0.65β_B² に落ち、s⁻⁴ の往復増幅を一度も通らない
(ST2 の層状哲学の「2 層版」: 層 0–1 = F_{≤1} は K2Q が丸ごと運び、層 ≥ 2 = R は天井の下で静的)。
床(閾値 2β_B²)が破れる場合は吸収を試みず証明書 (ii) へ — §3.2 の「床不成立 ⇔ Δ 降下」の実装。

### 3.6.3 分裂枝の合成(telescoping)

内側 [E, I_s]: s の定義より三原子は I_s 上 held → 保持枝(§3.5、ε_in = ρ/s):
r = 2: 8000(s/ρ)⁴ / r = 1(A): 61(s/ρ)² / r = 1(B): 証明書。
外側 [I_s, K]: L3a-split-out(ε_out = s)。両方が転送側なら:
  ‖e^{−U}F‖_K ≤ 100C₂₁s⁻⁴ · 8000(s/ρ)⁴ ‖e^{−U}F‖_E = 8·10⁵ C₂₁ · ρ⁻⁴ ‖e^{−U}F‖_E
(r = 1 内側は 61(s/ρ)² · 100C₂₁s⁻⁴ ≤ 6.1·10³C₂₁ ρ⁻²s⁻² ≤ 6.1·10³C₂₁ ρ⁻⁴)。
**C_split = 10⁶ C₂₁ ≈ 10⁴⁸**(未最適化 — C₂₁ = 10⁴² が支配。K2Q 真値 ~10³ 級なら C_split ~ 10⁹ 級)。

**証明書出力は 3 系統** — 内側 r = 1(B) / 外側 (ii) / 外側 (iii) — **すべて同一の降下 wrapper slot へ**
(受け渡し契約 = §5 項目 4、未証明。luna R1 [major] と同格の明示 scope)。

**envelope 比較損失の結論(作業計画 3 の問い)**: 損失は有限(≤ e^{Δ*+1} ≤ e⁴ ≈ 55)で、
Δ* > 3 のときは「損失」でなく**構造(pair 縮退)**として証明書化される。
「損失無限大 ⇔ 表現が虚偽包絡」であり §3.6.0 の反例と整合 — 損失と反例は同一現象の二つの顔。

## 3.7 降下 wrapper の設計(v0.5 の履歴 + v0.7 の仕様撤回)

> **現行 status (v0.7)**: §3.7.1 の bridge 不等式自体は正しいが、予定していた exact QR5 child は
> §3.7.5 の near-phantom 族で discount 条件を破る。§3.7.1–3.7.4 は
> 証明書から旧 DC を作ろうとした履歴として保存し、現行の次工程は exact block-frame contract (FR) とする。

目的: 証明書 3 系統(保持 r=1(B) / 分裂 (ii) / 分裂 (iii))を §4.3.5.3 の (W,d,Δ) 降下に
接続する契約。**Sol の中心判定(検算の上受諾)**: 現行の 3 証明書だけから有限状態の strict な
(W,d,Δ) 降下を導く wrapper は**構成できない** — 証明書は有限スケールの開条件(strict 不等式)、
降下 W↓/d↓/Δ↓ は閉じた代数条件(恒等消滅)であり、両者の間に **quantitative preparation**
の橋が必要。証明書の正しい位置づけは「降下」ではなく「**preparation lemma への入力**」。

### 3.7.1 確立した枠組(Sol 提供・検算済み)

**bridge 補題**: N_U(H;A) := ‖e^{−U}H‖_{∞,A}。親 (F,U)・子 (F′,U′)、F = F′ + R、
子 kernel N_{U′}(F′;I) ≤ A·N_{U′}(F′;J) のとき、D_I⁺ := sup_I(U′−U)₊、D_J⁻ := sup_J(U−U′)₊ で
  **N_U(F;I) ≤ e^{D_I⁺+D_J⁻}·A·(N_U(F;J) + N_U(R;J)) + N_U(R;I)**(三角不等式のみ・検算済み)。
**降下契約 (DC)**: 証明書が真の降下 edge であるための必要条件 =
①(W′,d′,Δ′) < (W,d,Δ) 辞書順 ② discount 有界 D_I⁺+D_J⁻ ≤ b + a·log(1/ρ)
③剰余吸収 e^{D}A·N_U(R;J) + N_U(R;I) ≤ C_Rρ^{−γ_R}N_U(F;J)。
(DC) を満たさない証明書は「構造診断」であって「降下」ではない。
**well-foundedness**: 1 ≤ d ≤ W、0 ≤ Δ ≤ W−d より W ≤ 3 の状態は 10 個、strict 降下長 ≤ 9
(検算済み)。ただし**有限停止だけでは一様 kernel は出ない** — 各 edge に (DC) が要る。
**discount 合成則**: nested scale ρ = Πρ_i、各 edge D_i ≤ b_i + a_i log(1/ρ_i) なら
Πe^{D_i} ≤ e^{Σb_i}ρ^{−max a_i}(split の telescoping と同型)。

### 3.7.2 (B) 契約: 部分的解決 + 本線カスケードの反駁

**厳密恒等式(本線、Sol 検証済み)**: κ := −c₂/c₃、e := M₁/c₃ で μ = κη + e は代数的に厳密、
**G = c₃·g_κ(η) + c₃·e^{κη}·(e^{e} − 1)**(数値 2000 配置 ≤ 2·10⁻¹⁴)。
pivot 交換(|c₃| ≥ |c₂| に原子 2,3 を交換)で |κ| ≤ 1、κ 爆発は局所的に除去できる
(ただし外側 pair が固定される分裂枝では global d↓ の根拠には使えない — Sol 注意)。

**direct-transfer 部分枝(証明済み — Sol B.2、定数検算済み)**: a := sup_E|η|、δ := σ₁/|c₃|、
Q := |κ(κ−1)| として、条件 **(T): 0.175Qa² ≥ 2e^{7/32}δ かつ Q ≥ q₀** の下で
sup_E|G| ≥ 0.0875|c₃|Qa² が立ち、
  **sup_K|G| ≤ (30 + 17500/q₀)·ε⁻⁴·sup_E|G|**(重み付きは ×1.29。
  検算: 28.9ε⁻² + 17490/q₀·ε⁻⁴)。(B) のうち (T) を満たす部分は降下不要で自己解決。

**本線の 2 分岐カスケードは偽(Sol B.3 反例 — 本線検算済み、受諾)**:
c₁ = c₂ = −1/2、c₃ = 1、η = x = τt、μ = x/2 + x²/8(κ = 1/2、M₁ = x²/8、r = 1)。
係数退化なし・E 上 η 衝突なしなのに、**g_κ の二次床と e-誤差が 2・3 次で厳密に相殺し
G = x⁴/192 + O(x⁵)**(Taylor 手計算 + 数値で確認)。「床が負けるなら κ 退化 or η 微小」は
閾値調整では修復不能。**必要な第三枝 = 二次 normal 方向の相殺 ⇒ 有効高次 jet**。
ただし exact valuation では本例は依然 r = 1 — Δ↓ と呼ぶには **scale-dependent blow-up
valuation の新定義**とその principal-part kernel が必要。カスケードの有限終端は open
(実質 = 三原子の一様 principalization 補題)。

### 3.7.3 (iii)・(ii) の判定(Sol C/D 節 — 検算済み)

- **(iii) は bridge (DC) を満たさない**: 既知は sup_K(U′−U) < 1 と N_U(R;K) ≤ 0.65β_B² のみで、
  Δ* > 3 は上限を与えず N_{U′}(R;I_s) ≤ e^{Δ*}N_U(R;I_s) は非有界。§3.6.2 の天井 2 が
  剰余を遮断するのは転送枝 (i)(Δ* ≤ 3 かつ ω ≥ 2β_B²)に限る。
- **degree/weight 衝突**: 剰余の二次主部 (c₂/2)η²e^{q₁} は deg 4 — 現行 class の
  旧 `deg P≤2(m_B−1)` では m_B = 3 が要り W = 4 に膨れ、W = 3 帳簿を破っていた。
  この order-only class 自体を F3′ により撤回したため、本項は旧 Taylor 置換ルートの historical failure とする。
- **η ≡ const の exact 併合は closure 簡約にのみ有効**: reduced envelope での d↓(和が 0 なら
  W↓)は exact に成立するが、U_red − U ≤ log 2 の逆向き sup_E(U−U_red) は非有界
  (= phantom envelope 反例)— 旧 U_F-kernel の復元には使えない。
- **(ii) から証明できる構造(Sol D.1)**: 各点で正規化振幅の第 2 位が ≥ (1−δ)/2 ≥ 31/64 —
  **全点で少なくとも二原子が live**(単一原子 dominance 排除)。
- **(ii) は純粋な Δ↓ を強制しない(Sol D.2 反例 — 本線数値検証済み)**:
  q = (0, βt², iθt/s)、c = (1, −1, β²/4)、s = √β/2 で (ii) が成立するが M₀ = β²/4 ≠ 0、
  exact 状態は (W,d,r) = (3,3,0) のまま。(ii) の正しい位置づけは
  **「degeneration variety への接近証明書」**(漸近極限は係数消滅 / support 衝突 /
  blow-up 後 moment 消滅の和集合に入る — 条件付き compactness、Sol 自信度 0.90)。

### 3.7.4 v0.5 時点の残る 2 補題(v0.7 で分解を撤回)

1. ~~**c = 3 quantitative preparation lemma**~~ **旧 DC で QR5 child へ渡す形は撤回**:
   証明書(開条件)から lower stratum の principal part と (DC) を満たす remainder bridge を
   構成する旧目標。§3.7.5 の反例により、少なくとも意図した QR5 edge は成立しない。
2. ~~**exact pair-block kernel K(2)+1**~~ **完了**(tree QR5、固定 SHA `27a1817` の R-P3 PASS):
   pair を Taylor 置換せず exact block B₁₂ = c₁e^{q₁} + c₂e^{q₂} のまま保持し、
   tree envelope U_T := max(log|B₁₂|, log|c₃| + Re q₃) で
   **N_{U_T}(F;K) ≤ Cρ⁻⁵N_{U_T}(F;E)** を与える新 kernel(K2Q ではない —
   振幅 c₁+c₂e^η は deg 2 多項式でない)。phantom pair は包絡から消え、
   e^{−U_T}|F| ≤ 2 が exact、W = 3 帳簿も保存。局所分割案: |P_B| ≳ c_Bβ_B² で
   K2Q + 剰余吸収 / |P_B| ≲ c_Bβ_B² で exact K2 block chart。零点近傍の interval cover と
   P1–P4 と窓 telescoping は独立再査読を通過。direct U_F 比較ではなく preparation の子 kernel。

tree QR5 の閉鎖は有効だが、旧 DC へ接続する設計図は撤回する。

### 3.7.5 old DC→QR5 bridge の no-go と置換先(v0.7 — 現行)

**命題 DC-NG (near-phantom witness)**: 旧計画の二枝、すなわち「parent U_F で direct transfer」または
「exact 2+1 tree を QR5 child とし、§3.7.1 の DC で parent U_F へ戻す」は同時に失敗し得る。

**査読 status**: 固定 SHA `1392266` の R-DCNG(A1–A7) **PASS**。以下の計算、one-transition 適合性、
frequency allowance、結論の scope、FR の未証明表示に finding なし。

*証明*: ρ ↓ 0、K = [0,1]、E_ρ = [1−ρ,1]、M_ρ := (16ρ)⁻¹、δ_ρ := e^{−2M_ρ} とし、

- c₁ = 1、q₁ = 0、c₂ = −1、q₂(t) = δ_ρt、
- c₃ = 1、q₃(t) = −M_ρt

と置く。pair は K 全体で held(sup_K|q₂−q₁| = δ_ρ ≤ 1/8)。E_ρ 中心で recenter すると
triple も held であり、q₃−q₁ の非定数部は E_ρ 上 M_ρρ/2 = 1/32 以下。従ってこの族は
one-transition 入口を満たし、q₁,q₂ は非定数差なので exact duplicate の前処理では消えない。

F_ρ = 1−e^{δ_ρt}+e^{−M_ρt}、individual envelope は
U_F(t) = max(0,δ_ρt,−M_ρt) = δ_ρt on K。t=0 で e^{−U_F}|F_ρ|=1。一方 E_ρ 上
|1−e^{δ_ρt}| ≤ 2δ_ρ ≤ 2e^{−M_ρ(1−ρ)} かつ e^{−M_ρt} ≤ e^{−M_ρ(1−ρ)} なので

  N_{U_F}(F_ρ;K) / N_{U_F}(F_ρ;E_ρ) ≥ (1/3)exp(M_ρ(1−ρ)).

これは任意の固定 C,γ に対する Cρ⁻γ transfer を破る。元の kernel が許す周波数項
e^{κΛρ} も Λρ = M_ρρ = 1/16 で定数に留まり、救済しない。

旧ルートが意図した exact QR5 child は B₁₂ := 1−e^{δ_ρt} と singleton e^{−M_ρt} の
F_ρ = B₁₂+e^{−M_ρt}、U_T := max(log|B₁₂|,−M_ρt)、R=0。E_ρ 上では
log|B₁₂| ≤ −2M_ρ+log 2 < −M_ρt なので U_T = −M_ρt。この edge では D_K⁺ = 0 だが

  D_{E_ρ}⁻ = sup_{E_ρ}(U_F−U_T) = M_ρ+δ_ρ ≍ ρ⁻¹,

なので、旧 DC②の D ≤ b+a log(1/ρ) をどの固定 a,b でも満たさない。remainder は 0 であり、
閾値調整では修復できない。従って direct branch と、予定していた QR5 child への旧 DC bridge が
同時に失敗する。これは別種の child 契約の存在までは否定しないが、現行仕様のままでは次の証明を
開始できないことを示す。∎

**判断**: 失敗したのは exact reduction ではなく、「簡約後も親の phantom envelope へ戻す」要求である。
親 U_F は redundant representation が作った解析上の量なので、reduction 出力では retire しなければならない。

**置換候補 FR**: exact block-frame replacement contract の statement と受理条件 FR1–FR7 は
[FR authoring document](2026-08-10-three-atom-block-frame-preparation--wip.md)へ移管した。ここでは再記述しない。
status は **plain FR-S1′とnested FR-S1″まで accepted / FR全体は未証明**。残りは
`(E-d)`/FR5–FR7 (FR-S4)。QR5 は FR5 の 2+1 node kernel だけを供給する。

従って c=3 の次の blocker は frame 選択そのものではなく、**選択済みの exact cancellation-aware
block frame に `(E-d)` と N3′/N4 envelope を与える FR-S4**である。§3.5/§3.6 の証明書は
pivot/chart 選択の診断には使えるが、それだけで reduction 完了とは数えない。

## 4. sharp test(検証条項)

**(T-4) U_F-flat 四次テスト**: Q_τ = (1 − e^{τt²})²(c = 3)。τ → 0 で τ⁻²Q_τ → t⁴、
包絡は平坦なので、この族を転送する任意の U_F 評価は ε⁻⁴ を消費する
(K2Q の T1 と同型; Sol 検証済み)。無条件 U_F 評価自体は phantom 反例で偽なので、
これを wrapper 全体の Γ(3) 下界とはまだ呼ばない。
**(T-5) 五次共鳴テスト(v0.6 — 決定的)**: (1, −e^{iπ/3}, 1) 共鳴族
([K(2)+1 §3.5](2026-08-09-pair-block-kernel-K2p1--wip.md))⇒ **γ_T(2+1) ≥ 5**。
3・4 次 jet の同時消滅は E = e^{±iπ/3}(原始 6 乗根)で非退化に起き、5 次は
G⁽⁵⁾ = ±2id⁵/√3 ≠ 0 で消せない。tree envelope QR5 の sharp 予想は γ_T(2+1) = 5。
U_F-transfer/wrapper への帰結は bridge 待ちである。

## 5. 作業計画

1. ~~(Stab) 設計判断~~ **完了(§3.1–3.2)**: 層状転送 + 層床 + Δ 降下トリガーに決定。
2. ~~保持枝の証明~~ **完了(§3.5、v0.3 — 未レビュー)**: r = 2 は g_κ 標準形への還元で
   無条件(6100ε⁻⁴)、r = 1 は二者択一(47ε⁻² or 近共線性証明書 → 降下)。
   LT/LF は r = 2 では不要になった(標準形の pointwise 比較が代替)。
   ※ LT/LF の設計は一般 c(標準形還元が効かない d ≥ 3)で再登場する見込み — §3.1–3.2 は保存。
3. ~~分裂枝の執筆~~ **完了(§3.6、v0.4 — 未レビュー)**: 外側 = K2Q-wt + 天井 2 による剰余遮断、
   三者択一(転送 / 深消滅証明書 / pair 縮退証明書)。envelope 損失 ≤ e⁴、無限損失は反例と同一現象。
   副産物: §1 の無条件形は偽(phantom envelope 反例)— 二者択一形へ訂正。
4. **次工程**: [c=3 exact block-frame preparation (FR)](2026-08-10-three-atom-block-frame-preparation--wip.md)
   の plain FR-S1′ / nested FR-S1″ は R-A′ / R-A″ PASS。次は FR-S4。
   内側 r=1(B) / 外側(ii)/(iii)は FR-S4 の pivot/chart 診断に用いる。
5. 敵対的レビュー(luna)→ 数値検証 → 受諾判定(保持枝 R1 済み、分裂枝 §3.6 が対象)。
6. 一遷移制限の除去(多重遷移帰納)— 本補題では扱わない。

## 6. 版履歴

- v0.1(2026-08-09): 骨格。statement 案、三分岐アーキテクチャ(Sol B 節採用)、
  (Stab) の設計候補 2 案、sharp test の分離。
- v0.2(2026-08-09): **(Stab) 設計判断完了**。最悪配置 registry ST1–ST3(naive Stab の
  τ/ρ⁴ 倍破綻・層状転送の成立・層間相殺の ρ 非依存床 0.0147)を構成・数値検証し、
  「層状転送 LT + 層床 LF + Δ 降下トリガー」に決定。(S-b) 閾値再定義は不要と判断。
  数値スクリプト: セッション scratchpad stab_worstcase.py / stab_floor_refine.py(修正版)。
- v0.3(2026-08-09): **保持枝の証明完成(未レビュー)**。核心の発見 = r = 2 では M₁ ≡ 0 が
  μ = κη を強制し **G = c₃·g_κ(η(t)) の 1 変数標準形に完全還元**、Hermite–Genocchi 積分表示
  g_κ(x) = κ(κ−1)x²∫_Δe^{(s₁+κs₂)x}ds から pointwise 両側評価(κ 一様、衝突極限込み)。
  比 ≤ 6100ε⁻⁴(r = 2)/ 47ε⁻² or 近共線性証明書(r = 1)。数値確認: 両側評価 2·10⁵
  サンプル違反ゼロ(実測 [0.42, 0.59] ⊂ [0.175, 0.825])。ST3 の床 0.0147 の解析的説明を獲得。
- v0.3.1(2026-08-09): **luna R1 反映**。核心(標準形還元・HG 表示・pointwise 評価・
  r=1 二者択一・r≤2 恒等性)は全て検算通過、反例候補 7 系統も全て不成立。
  [blocking] 重み付き約分の誤り(U_F − Re q₁ = h は非定数、反例 h = 0.05t)→
  osc_K h ≤ 2β による e^{2β} ≤ 1.29 補正で修正(重み付き定数 8000ε⁻⁴ / 61ε⁻²)。
  [major] (B) の wrapper 受け渡し契約は未証明として明示(守備範囲を不等式のみに限定)。
  [minor] |κ|>1 の swap 変数明記・6100 の丸め帳簿(厳密値 6082.8)。
- v0.4(2026-08-09): **分裂枝の証明本体(§3.6 — 未レビュー)**。①反例発見: 素朴な weighted L3a は
  phantom envelope(pair の恒等相殺 + singleton の別形状生存 — c = 3 で初めて可能)で**偽** →
  §1 を二者択一形に訂正 ②外側転送 L3a-split-out: pair の (2,1) 化 F_{≤1} = P_Be^{q₁} + c₃e^{q₃} に
  K2Q-wt、剰余は天井 e^{−U′}|F_{≤1}| ≤ 2 と絶対評価 e^{−U}|R| ≤ 0.65β_B² で遮断(ST1 破綻の
  構造的回避 = ST2 層状哲学の 2 層版)。三者択一: 転送 100C₂₁s⁻⁴ / 深消滅証明書 ω < 2β_B² /
  pair 縮退証明書 Δ* > 3(witness 付き)③合成 C_split = 10⁶C₂₁ · ρ⁻⁴、証明書 3 系統は
  同一 wrapper slot へ。envelope 損失は ≤ e⁴ で有限、無限損失 ⇔ 虚偽包絡(反例)と同定。
- v0.4.1(2026-08-09): **luna R2(分裂枝)反映**。不等式本体((a)(b)(c)・(i) の変換・
  (ii)(iii) 網羅性・witness・telescoping・反例の数値)は全検算通過。
  [blocking] s = sup の非空性・閉性が未証明 → E 上 held を前提として明示 + 閉性補題
  (閉区間・非厳密 ≤・位置コンパクト性 + 一様連続)を追加。
  [major] 反例の検算座標の混在 → recenter 後(η̃ ≡ 0 = 併合 slot が捕捉)と recenter 前
  ((iii) が捕捉)を分離明記。[major] P_B ≢ 0(η 非定数 ⇔)を証明 (i) の分岐前提として明示。
  [minor] 26.7 の丸め係数を 1.325 に訂正(e³·1.33 = 26.714 > 26.7)。
- v0.5(2026-08-09): **wrapper 設計 = Sol xhigh 協力の成果を検算の上採用(§3.7 全面改稿)**。
  ①中心判定: 証明書(開条件)だけから strict (W,d,Δ) 降下は構成不可 — bridge 補題 +
  降下契約 (DC) を枠組として確立 ②(B) の (T) 部分枝は証明済み((30+17500/q₀)ε⁻⁴ —
  定数検算済み)③本線の 2 分岐カスケードは反駁(G = x⁴/192 反例 — 二次 normal 方向相殺 =
  第三枝が必要、scale-dependent blow-up valuation は新規 open)④(iii) は (DC) 不成立・
  deg/weight 衝突(η² は deg 4)を確認 ⑤(ii) は「二原子以上 live」(証明)+
  「degeneration variety 接近証明書」(D.2 反例で Δ↓ 強制は否定 — 数値検証済み)
  ⑥残る 2 補題に分解: quantitative preparation / exact pair-block kernel K(2)+1。
  数値: sol_wrapper_verify.py(B.3 の 1/192、D.2 の (ii) 成立、B.2 定数)。
- v0.6(2026-08-09、**v0.6.1でscope撤回**): 五次共鳴から Γ(3) ≥ 5 と判断した。五次共鳴反例
  (1, −e^{iπ/3}, 1)([K(2)+1 §3.5] — E² − E + 1 = 0 で 3・4 次 jet 同時厳密消滅、
  mpmath 50 桁で ratio·ε⁵ = 0.99833 一定)は**三原子 held**で保持枝 r=1(B) 穴に住む。
  既証明の部分枝(r=2 / r=1(A) / 分裂 (i))と phantom 反例・二者択一形は全て不変。
  ただし U_T→U_F bridge を示さず wrapper の Γ(3) へ移した点がscope過大だった。
- v0.6.1(2026-08-10): **envelope namespaceを分離**。五次共鳴が直接示すのは
  tree envelope QR5 の γ_T(2+1) ≥ 5。三原子 wrapper の Γ(3) はbridge待ちのopenへ戻した。
- v0.6.2(2026-08-10): tree QR5(U_T) は固定 SHA `27a1817` の R-P3 まで PASS。
  phantom 反例が direct U_T→U_F 一様比較を禁止するため、「bridge待ち」を quantitative
  preparation/DC 待ちへ訂正。exact pair-block kernel を残2補題から閉鎖し、wrapper の残本体を
  preparation lemma(plus 多重遷移)へ縮小。
- v0.7(2026-08-10): **intended QR5 child への old DC bridge を撤回**。§3.7.5 の非定数
  near-phantom one-transition family は direct transfer と D=O(log(1/ρ)) の QR5 bridge を
  同時に破る(別種の child 契約までは排除しない)。親 U_F を
  reduction 後も保持する要求を捨て、
  exact cancellation-aware block-frame contract (FR: span exactness / tree envelope / N2 / N3′–N4)
  を次の authoring target とした。QR5 は FR の 2+1 内部節点 kernel として保持。
- v0.7.1(2026-08-10): 固定 SHA `1392266` の R-DCNG(A1–A7) **PASS**。near-phantom witness の
  held 条件・weighted ratio・tree discount・frequency allowance と、別 child 未排除という scope を再検算。
- v0.7.2(2026-08-11): FR 文書の F3′ を本線で独立検算し、held 分岐の旧
  `moment order≤2 ⇒ jet degree≤4` ルートを撤回。F3′の式はFR文書だけに置き、本書は参照に限定。
- v0.7.3(2026-08-11): FR 文書の plain single-scale FR-S1′ が固定 SHA `ed25401` の
  R-A1–R-A6 で全 PASS。次工程を nested 2+1 一般化原子接続→FR-S4へ更新。
- v0.7.4(2026-08-11): FR 文書の nested 2+1 FR-S1″ が固定 SHA `61111cc` の
  R-A″1–R-A″6 で全 PASS。次工程を `(E-d)` / FR5–FR7 (FR-S4)へ更新。
- v0.7.5(2026-08-13): split(i) のK2Q domainを明確化。`μ=q₃−q₁` が定数なら
  `c₃e^{q₃}` を `c₁e^{q₁}` へexact係数吸収して二原子へREFIXし、K2Q-wt分岐へ入れない。
  §3.6.2の旧U_F転送はS4のU_T unit-step witnessではなく、`M-SPLIT-I-WITNESS`はopenのまま。
