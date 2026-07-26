# 2026-07-26 preprint v2 訂正リスト（先出し）

状態: proposed（管理役が組み立てた素案。方針判断は 2026-07-26 に orange が決定済み — 末尾「決定事項」参照）

公開済み: [doi:10.5281/zenodo.21457049](https://doi.org/10.5281/zenodo.21457049)
（*Compact physical Gaussian-ket models for homodyne quantum-state tomography*, v1, 2026-07）

## この文書の目的

訂正版を出す方針は **B（K_ε ノート完成と同時にまとめて）** で確定している
（目標 2026-08-01、ハード 08-03）。Zenodo の操作は orange の手が要るので、
**当日の作業を「貼り付けと投稿」だけに縮める**ために、直すべき箇所を事前に確定しておく。

対象は `docs/preprint/preprint.md`（投稿ソース）と、そこからビルドされる
`docs/preprint/preprint.pdf`。

---

## 訂正 1【必須】§3.4 — "cutoff-stable" と数値レンジ

**場所**: `docs/preprint/preprint.md:247` 付近（非包含解析の "The boundary is thin, however:" の直後）

**現在の文言（公開済み）**:

> direct best-approximation fits approach the target to $1$--$2\times10^{-3}$ in $1 - F$
> (cutoff-stable best-found values, hence upper bounds on the true distance)

**何が誤りか**: 2 点ある。

1. **数値レンジ**: 引用されている 1–2×10⁻³ は採点カットオフ n_score = 8 の値。
   最大採点カットオフ n = 12 では **≈2–3×10⁻³**
2. **安定性の主張**: "cutoff-stable" は偽。全 K でカットオフとともに単調増加している

`experiments/20_noninclusion/results_routeB.json`（squeezed 系列、seed 3 本の best）から
再取得した実測値:

| n_score | K=2 | K=4 | K=8 |
|---|---|---|---|
| 8 | 2.50e-3 | 1.60e-3 | 1.36e-3 |
| 10 | 3.21e-3 | 2.20e-3 | 1.98e-3 |
| 12 | 3.44e-3 | 2.37e-3 | 2.17e-3 |

**根本原因**: `experiments/20_noninclusion/routeB.py` が判定文をハードコードで印字していた
（PR #106 / #107 で修正済み。AGENTS.md の規律 3 はこの事故から来ている）。

**置換案**:

> direct best-approximation fits approach the target to $\approx 2$--$3\times10^{-3}$
> in $1 - F$ at the largest scored cutoff ($n_{\text{score}} = 12$; best-found values,
> hence upper bounds on the true distance). The series is still increasing with the
> scoring cutoff, so the infinite-cutoff limit is unresolved.

**変わらないもの**: 定性的な結論（"the boundary is thin"、Route B が上界であって下界でないこと、
best-found $\eta'$ が 0.648–0.661 で正値性境界に押し付けられていること）は影響を受けない。

**リポジトリ側の対応状況**: README / README.ja / routeB.py / ノート §7.3 は訂正済み。
**公開済み preprint と、そこにリンクしたアウトリーチメールだけが旧文言のまま残っている。**

---

## 訂正 2【強く推奨】§4 Discussion の C4 段落 — 先行研究の欠落

**場所**: `docs/preprint/preprint.md:318` 付近（"One speculative direction seems worth naming (C4)."）

**現在の文言（公開済み、要旨）**: 状態が要求するガウス成分数を資源カウントと見なす方向を
「投機的な方向」として提示し、既存階層との区別が必要だと述べたうえで、
stellar rank（Chabaud et al.）と coherent-state decomposition rank の 2 つを名指しし、

> Whether "Gaussian count" differs meaningfully from those hierarchies […] is exactly
> what would need to be established. We flag this as speculation: no result in this
> paper establishes it.

と締めている。

**何が問題か**: **その量は既に定義されている。** 一次ソース確認済み:

- **Hahn, Takagi, Ferrini, Yamasaki**, *Classical simulation and quantum resource theory of
  non-Gaussian optics*, [arXiv:2404.07115](https://arxiv.org/abs/2404.07115)（2024-04-10 投稿）。
  abstract に "define measures of non-Gaussianity quantifying this simulation cost,
  which we call the **Gaussian rank and the Gaussian extent**" とある。
  Gaussian rank = 重ね合わせに必要なガウス状態の最小個数、すなわち C4 が
  「how many Gaussians is this state」と呼んでいる量そのもの

つまり preprint（2026-07）は、**2 年以上前に定義済みの量を「これから確立が必要な投機」として
提示している**。これは新規性の誤主張ではない（"speculation" と明示しているので主張はしていない）が、
**先行研究の見落としとして読まれる**。#71 の Gate S で既に「新尺度」主張は撤回済みであり、
公開物だけがその判断を反映していない状態になっている。

**推奨対応**: C4 段落を、投機の提示から**既存研究への接続**へ書き換える。骨子:

- ガウス成分数を非古典性の資源カウントと見る枠組みは HTFY [2404.07115] が
  Gaussian rank / Gaussian extent として既に定式化している
- 近似版への拡張は stellar rank について Hahn, Garnier, Ferrini, Ferraro, Chabaud
  [2410.23721]（approximate stellar rank）
- 近似 coherent-state rank の下界研究は Cottier–Chabaud [2604.00766]
- 本論文の実測（cat は 2 成分、実データでのランク／成分数の飽和点が小さいこと）は、
  この既存の量に対する**実験側の観測**として位置づけられる

**一次ソース確認状況**（規律 1、いずれも 2026-07-26 に管理役が arXiv abstract を直接取得）:

| 文献 | 著者・投稿日 | 確認できた記述 |
|---|---|---|
| [2404.07115](https://arxiv.org/abs/2404.07115) | Hahn, Takagi, Ferrini, Yamasaki / 2024-04-10 | "define measures of non-Gaussianity quantifying this simulation cost, which we call the **Gaussian rank and the Gaussian extent**" |
| [2410.23721](https://arxiv.org/abs/2410.23721) | Hahn, Garnier, Ferrini, Ferraro, Chabaud / 2024-10-31（v5: 2026-04-30） | "extending the stellar rank to the **approximate stellar rank**, which serves as an operational measure of non-Gaussianity" |
| [2604.00766](https://arxiv.org/abs/2604.00766) | Cottier, Chabaud / 2026-04-01 | *Lower Bounds on Coherent State Rank*、"initiate a systematic study of **lower bounds on the approximate coherent state rank**" |

**限界**: 3 本とも確認したのは abstract であり本文ではない。とくに 2410.23721 について
「fidelity ボールによる ε 緩和」という具体的な定義形は abstract からは確認できていないので、
v2 本文では **abstract で確認できた粒度（"approximate stellar rank" への拡張）までしか書かない**。
定義の細部に踏み込む記述が必要になったら、その時点で本文を取得して確認する。

**任意**: K_ε ノートが同時に公開されるなら、C4 から companion note への参照を張れる。
特に Theorem C′（同じ状態がガウス粒では 2 個、pre-loss operator rank では無限）は
C4 の「cat は stellar rank 無限だがガウスケット 2 個で足りる」という観察を定理として
精密化したものなので、接続の価値が高い。ノートの公開形態が決まってから判断する。

---

## 訂正しないもの

- **`experiments/20_noninclusion/out_routeB*.log`** — 当時の主張の記録であり書き換えない
  （何をいつ主張していたかの証拠性を保つ）
- **v1 そのもの** — Zenodo 上に残す。これが正しい振る舞い
- **abstract** — 訂正 1・2 はいずれも本文中であり、abstract の記述は影響を受けない。
  したがって **Zenodo の Description 欄は v1 のまま**でよい（orange の作業が 1 つ減る）
- **著者・ORCID・ライセンス（CC-BY-4.0）・キーワード** — 変更なし

---

## orange の作業手順（当日）

1. `docs/preprint/preprint.md` に訂正 1・2 を適用（本線または管理役が PR で先に用意する）
2. PDF を再ビルド:

   ```bash
   pandoc docs/preprint/preprint.md -o docs/preprint/preprint.pdf --pdf-engine=xelatex
   ```

3. Zenodo の当該レコードで **"New version"** を選択（concept DOI 配下に v2 が付く。
   v1 の DOI は生き続ける）
4. 新しい PDF をアップロード、Description は v1 のまま
5. Version 欄を `v2` に、Additional notes に訂正内容の要約を記載

## 決定事項（orange、2026-07-26）

| 論点 | 決定 | 備考 |
|---|---|---|
| 訂正 2（C4 の先行研究追記）を v2 に含めるか | **含める** | 訂正 1 と一度に出す。Zenodo 操作は 1 回 |
| 旧 DOI を貼ったアウトリーチ受信者へ通知するか | **通知しない** | concept DOI が最新版を指すことに依拠する。管理役は通知側に理があると述べたが、orange の判断で不通知 |
| preprint.md 本体への適用 PR を先に作るか | **いま作る** | 当日の作業を Zenodo 操作だけに縮める |

決定者: orange。提案・素案作成: Claude（管理役）。

---

作成: Claude（管理役）2026-07-26。実測値は `results_routeB.json` から再取得、
arXiv:2404.07115 は abstract を直接取得して確認した。
