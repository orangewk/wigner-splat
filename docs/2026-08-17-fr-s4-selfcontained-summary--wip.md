# c=3 弱包絡評価 (S4-Ew) — 自己完結要約(外部読者向け)

日付: 2026-08-17 / 著者: 本線 / status: **wip — 要約・非規範**

> **地位**: 本稿が述べる結果は**証明ドラフト・複数 LLM 検算済み・fixed-SHA 内部査読済み・独立外部再査読待ち**である。
> 証明の唯一の authoring location は [FR 文書](2026-08-10-three-atom-block-frame-preparation--wip.md) §10(v0.15)であり、
> 本稿と齟齬がある場合は FR 文書が優先する。本稿は新しい主張を導入しない。

## 1. 背景

Gaussian border rank 閉包定理 program([閉包文書](2026-08-02-gaussian-border-rank-closure--wip.md)、draft PR #178)の
補題 N は、衝突する Gaussian 原子族の span に対し cancellation-aware な exact frame(FR1–FR7、FR 文書 §4)を要求する。
c=3(三原子)では FR1/FR2/FR4/FR3(X)(L-d) が既に閉じており(FR-S1′/S1″)、最後に残っていたのが
**FR6 = 遠方成長の一様包絡評価**と FR5/FR7 の同時達成だった。本稿はその核心である弱包絡評価 (S4-Ew) の
statement と証明構造を、FR 文書の履歴・台帳を読まずに追える形で要約する。

## 2. 設定

**Fock space.** `ℱ` は Segal–Bargmann–Fock space: 整関数 `f` で
`‖f‖² := (1/π)∫_ℂ |f(z)|²e^{−|z|²}dA(z) < ∞`。正規直交基底 `e_k = z^k/√k!`、再生核 `K(z,w) = e^{zw̄}`、
従って全 `f ∈ ℱ` で `|f(z)| ≤ ‖f‖e^{|z|²/2}`。

**Gaussian 原子.** `Φ(A,B)(z) := exp(Az²/2 + Bz)`(`|A| < 1` で `Φ(A,B) ∈ ℱ`)。原子 parameter は compact class

  K_{δ,R} := {|A| ≤ 1−δ} × {|B| ≤ R}   (0 < δ < 1、R > 0 固定)

に属するとする。norm は閉形式 `‖Φ(A,B)‖² = (1−|A|²)^{−1/2}exp[(|B|²+Re(AB̄²))/(1−|A|²)]` を持つ。

**入力(衝突 cluster).** 三原子列 `u_{j,m} = Φ(ξ_{j,m})`(`j=1,2,3`、`ξ_{j,m} ∈ K_{δ,R}`)、
`V_m := span{u_{1,m},u_{2,m},u_{3,m}}`。全 j で `ξ_{j,m} → ξ*`(単一衝突 cluster)。原子間の衝突 scale は
weighted metric `d_w((A,B),(A′,B′)) := max(|A−A′|^{1/2}, |B−B′|)` で測り、`s̃_m := max_{i,j}d_w → 0`
(original 座標)。pivot 原子を真空へ移す共通 metaplectic gauge `U_m`(exact unitary、span/norm/Gram 保存)を
frame 構成に使う。

**exact block tree.** frame 候補は原子の exact 有限結合 `h_{ℓ,m} = Σ_j a_{ℓj,m}u_{j,m}` で、
rooted binary block tree を付す: leaf = 原子、internal node `H = X + Y`、node envelope
`U_H(t) := max(log|X(te^{iθ})|, log|Y(te^{iθ})|)`。c=3 の非自明な shape は(置換を除き)
「pair block + singleton」= 2+1 のみで、root envelope を `U_T` と書く。正規化 frame を
`v_{ℓ,m} := h_{ℓ,m}/‖h_{ℓ,m}‖_ℱ`(`r = dim V_m ≤ 3` 本)とする(構成は FR-S1′/S1″、accepted)。

**難所.** 衝突族では結合 norm が原子 norm よりはるかに小さくなり得る(deep cancellation)。実際
`D_H := max(‖X‖,‖Y‖)/‖H‖` は `s̃_m^{−2}` order で発散する witness がある(FR 文書 §10.8 design note)。
従って「各原子の自明評価の和」では m 一様の包絡は出ず、cancellation を保つ機構が必要になる。

## 3. 主結果

**定理 (S4-Ew)**(FR 文書 §10.8 補題 EW、accepted `b39216f`): 上の入力に対し、定数
`C_w, C_lin > 0` と閾値 `m₀` が存在して、全 `m ≥ m₀`、全 frame index `ℓ`、全 `z ∈ ℂ` で

  |(U_m^{−1}v_{ℓ,m})(z)| ≤ C_w · exp((1−δ/2)|z|²/2 + C_lin|z|).

`C_w, C_lin` は `(δ, R, ε_chain, C_T, C_RF)`(§6 の一様定数)のみに依存し、
`m, ℓ, z, θ` と表示係数(SVD/Newton 係数)に依存しない。`m₀` は入力列の収束速度に依存してよい
((E-w) は `m₀` の存在のみ要求)。

**意味**: 自明評価の指数は `(1−δ)|z|²/2 + R|z|` だが、それは**各原子**に対するもの。定理は
cancellation で norm が潰れた**正規化結合**に対して、係数損失 `δ/2·|z|²/2` だけで済む一様包絡を与える。
これが c=3 FR ledger の FR6 を(FR5/FR7 とともに)閉じる。

**非主張**: 多項式形 (E-d)(一般 c の義務として open)、補題 N 本体の量化完備化、閉包定理・系 C1、
一般 c(B2/S4、L2b/L3)。いずれも閉包文書側で open のまま。

## 4. 証明の構造

radial ray `z = te^{iθ}` を固定し `T := |z|` とする。近原点 `T < 3` は再生核評価で直ちに済む
(`e^{T²/2} = e^{(1−δ/2)T²/2}·e^{δT²/4}`、`δT²/4 ≤ (3δ/4)T`)。本体は `T ≥ 3` の rank 3 で、
4 段 pipeline による:

1. **出口 (W1+W2)**: `t = T` で `e^{U_T}` を Fock norm に変換する。pair child には c=2 の**強形** norming
   (係数 `(1−δ)`、W2)が要る — 弱形 `(1−δ/2)` では chain の二次費用 `(δ/8)T²` を吸収する余地が
   ない、という予算計算が W2 の強形を強制する(`(1−δ)/2 + δ/8 = (1−3δ/4)/2 < (1−δ/2)/2`)。
2. **chain (W3)**: 重み付き関数 `G := e^{−U_T}H` を、単位窓分割 `I_k = [a_k, a_k+1]`
   (`a_1 = T−1` から降順、重なり `J_k` は長さ `ε_chain`、窓数 `N ≤ 2T+1`)に沿って内向きに伝播する。
   各窓の一段比較は accepted kernel が供給する(§5 M1/W3): pair 位相が held の窓は一様費用 `C_T`
   (QR5)、far 窓は graded 費用 `exp(C_RF(1+Λ_{η,k}))`(RF)。far 費用の総和は RF の大域台帳により
   `(δ/8)T² + O(T)` に収まる。
3. **終端 anchor (C0)**: 最終窓 `I_N ⊂ [0,2]` で `M·‖G‖_{∞,I_N} ≤ C_anc·‖H‖`
   (`M := max(‖X‖,‖Y‖)`)。singleton child は zero-free なので下から押さえられ、これが
   `D_H` の発散を**厳密に相殺**する(`D_H ~ s̃^{−2}` に対し `‖G‖_{∞,I_N} = O(s̃²)`)。
4. **合成 (W4→EW)**: 三段を掛け合わせ `|H(Te^{iθ})| ≤ 2C₂C_anc·‖H‖·(1+T)²·e^{(1−3δ/4)T²/2+(R+C_ch)(T+1)}`。
   `(1+T)² ≤ e^{2T}` と `(1−3δ/4) ≤ (1−δ/2)` で (S4-Ew) の形に落とす。rank 2 は W2 で、rank 1 は
   自明評価で直接出る。

## 5. 補題チェーン(statement 要約)

以下すべて FR 文書 §10.8 に完全証明がある。`E_{δ,R}(t) := exp((1−δ)t²/2 + Rt)` とする。

**W1(Child-reserve interface、`a59768e`)**: binary node `H = X+Y` の各 child が per-child strong bound
`|X(z)| ≤ C_X P_X(t) E_{δ,R}(t)‖X‖`(`P_X` は固定次数・非負係数多項式)を満たすなら
`e^{U_H} ≤ C_res·P·E_{δ,R}·max(‖X‖,‖Y‖)`(`C_res = max(C_X,C_Y)`、`P = P_X+P_Y`)。
singleton `cΦ(ξ)`(`ξ ∈ K_{δ,R}`)は `C = 1、P = 1` で満たす(`‖Φ‖ ≥ |Φ(0)| = 1`)。

**W2(Pair norming、c=2 強形、`a0fcd10`)**: 相異なる `ξ₁, ξ₂ ∈ K_{δ,R}`、`c₁c₂ ≠ 0`、
`f = c₁Φ(ξ₁) + c₂Φ(ξ₂)` に対し全 `t ≥ 0` で

  |f(te^{iθ})| ≤ C₂(R)·(1+t)²·E_{δ,R}(t)·‖f‖_ℱ,
  C₂(R) = 1 + max{2(1+2R)(1+R), 2√2 + 2(1+R²)}.

定数は `R` のみに依存し、衝突 scale・pair separation に**依存しない**。証明の骨子: 差分商
`ψ := (Φ(ξ₁)−Φ(ξ₂))/r`(`r = max(|ΔA|,|ΔB|)`)を線分 path の積分表示で押さえ(`K_{δ,R}` の凸性)、
`ψ` の 0–2 次 jet(`ψ₀ = 0, ψ₁ = ΔB/r, ψ₂ = (ΔA/r + (B₁+B₂)ΔB/r)/√2`)の二分法で
jet 下界を取り、`f = (c₁+c₂)Φ(ξ₂) + (c₁r)ψ` の係数を `‖f‖` で消去する。深い衝突でも
分子と norming の双方に同じ `r` が現れるため scale 依存が相殺される。

**C0(Terminal two-anchor、`f31cca0`)**: root `H = X + Y`(`X` = pair block、`Y = c₃Φ(ξ₃)` singleton)、
`G := e^{−U_T}H`、`I_N ⊂ [0,2]` で

  max(‖X‖,‖Y‖)·‖G‖_{∞,I_N} ≤ C_anc·‖H‖,   C_anc = max{6, (3/2)C_s}.

証明の骨子: singleton は `t ≤ 2` で zero-free かつ `|Y| ≥ c_Y‖Y‖`(閉形式 norm 上界 + 指数下界)。
`A := ‖H‖`、`B := ‖Y‖` の大小で二場合分け — `A ≥ B/2` なら `|G| ≤ 2` と `M ≤ 3A` で直接、
`A < B/2` なら singleton-anchored bound `‖G‖ ≤ C_s A/B` と `M ≤ (3/2)B` で相殺。

**M1(mode audit、`fd18e9d`)**: 被覆補題(S4b-COV、`c36d818`)の帰結として、公開 ray ledger の
root record は weighted 型(QR5 held / RF far)のみ・各窓ちょうど 1 個・終端窓は C0 専用。
新しい解析的主張を含まない監査補題。

**W3(Weighted chain、`4086ef9`)**: `m ≥ m₀`、`T ≥ 3` で

  ‖G‖_{∞,I₁} ≤ exp((δ/8)T² + C_ch(T+1))·‖G‖_{∞,I_N},
  C_ch = 10·log(1/ε_chain) + 2·log⁺C_T + 6·C_RF.

各窓の一段比較 `‖G‖_{∞,I_k} ≤ C_step,k·ε_chain^{−5}·‖G‖_{∞,I_{k+1}}` を `N−1 ≤ 2(T+1)` 回反復し、
費用を三分割(`ε` 因子は線形、held 窓は一様、far 窓は RF 大域台帳で二次 `(δ/8)T²` + 線形)。
weight `U_T` は ray 全体で共通なので record 間の weight 乗り換えは生じない。

**W4(Terminal-cancelled exit、`cb87eee`)**: W1/W2(出口)× W3(chain)× C0(anchor)の合成:

  |H(Te^{iθ})| ≤ 2C₂(R)·C_anc·‖H‖·(1+T)²·exp((1−3δ/4)T²/2 + (R+C_ch)(T+1)).

二次係数 `(1−3δ/4)/2` は target `(1−δ/2)/2` より `δ/8` だけ強い。

**EW-B(original-collision bridge、`b39216f`)**: chain の witness(位相差の変動 `Λ_{η,k}` 等)を
gauge 前の original 座標で再インスタンス化する。`s̃_m` の定義から直ちに `|ΔA| ≤ s̃_m²`、`|ΔB| ≤ s̃_m` で、
RF 台帳は同一定数のまま適用できる。gauge 経由の転送(metaplectic 包絡合成)は採らない —
unitarity は norm を保つが pointwise growth を保たないため。

**EW(final、`b39216f`)**: `F := U_m^{−1}v_{ℓ,m}`(`‖F‖ = 1`)は original 原子の ≤3 原子 exact 結合。
effective rank(1/2/3)× `T ≥ 3` / `T < 3` の場合分けで (S4-Ew)。
`C_w = 2C₂(R)C_anc·e^L`、`C_lin = L + 2`、`L = R + C_ch`。

## 6. 定数

全定数は `(δ,R)` と 3 個の一様 kernel 定数から閉形式で組み上がる:

| 定数 | 由来 | 値 / 依存 |
|---|---|---|
| `C₂(R)` | W2 | `1 + max{2(1+2R)(1+R), 2√2+2(1+R²)}` |
| `C_Φ, c_Y, C_s` | C0 | `C_Φ = [δ(2−δ)]^{−1/4}e^{R²/(2δ)}`、`c_Y = C_Φ^{−1}e^{−2(1−δ)−2R}`、`C_s = e²/c_Y` |
| `C_anc` | C0 | `max{6, (3/2)C_s}` |
| `ε_chain` | 分割 | `min(1/2, δ/[8(κ_chain+1)])`(route registry から) |
| `C_T` | QR5 kernel(accepted、外部) | held 窓の一様費用。消費時 `max(1,·)` 正規化 |
| `C_RF` | RF kernel(accepted、外部) | far 窓の graded 費用定数(台帳込み) |
| `C_ch` | W3 | `10log(1/ε_chain) + 2log⁺C_T + 6C_RF` |
| `C_w, C_lin` | EW | `2C₂C_anc·e^{R+C_ch}`、`R+C_ch+2` |

## 7. 検証状態

- 各補題は draft → 独立 LLM 査読(fixed-SHA、adversarial findings、blocking は修正まで不受理)→
  acceptance の cadence で閉じた。SHA は §5 の各補題に付記(完全な台帳は FR 文書 §10.7/§11)。
- 数値診断(**非証拠**): W2 は 4×10³ ランダム配置(Gram 閉形式で `‖f‖` 厳密、near-cancellation・
  `s ∈ [10⁻³,1]` 含む)で違反なし・最小余裕 ×96。C0 は 3 class × 1500 配置で違反なし
  (深い cancellation `D_H ≈ 7×10⁵` の配置で余裕 ~1.9×10⁴)。独立検算(70 桁精度)でも違反なし。
- 主張面の整合(禁止語彙 FR7、acceptance 表記、版同期)は repo の
  [claim-surface tests](../tests/test_claim_surface_policy.py)(25 件)で機械監視。

**残余(open)**: c=3 FR arc 全体の外部独立再査読、補題 N 本体の量化完備化、一般 c
((E-d)、B2/S4、L2b/L3)、系 C1。本稿の結果はこれらを主張しない。

## 8. 全証明の所在

| 内容 | 場所 |
|---|---|
| 主結果と S4a 全証明(W1–EW) | FR 文書 §10.8 |
| target (E-w) の正確な仕様 | FR 文書 §10.2 |
| 分割・台帳・route 契約 | FR 文書 §10.3–10.6 |
| QR5 / RF kernel の証明 | FR 文書 §10.5.2–10.5.3(+ K2 系文書) |
| 被覆補題(S4b-COV) | FR 文書 §10.5.5 |
| acceptance 台帳・版履歴 | FR 文書 §10.7 / §11 |
| program 上の位置づけ(補題 N、FR1–FR7) | 閉包文書 §4.3、FR 文書 §1–§4 |

English version: [2026-08-17-fr-s4-selfcontained-summary-en--wip.md](2026-08-17-fr-s4-selfcontained-summary-en--wip.md)
