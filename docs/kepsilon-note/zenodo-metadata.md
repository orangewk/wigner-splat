# Zenodo 投稿メタデータ（**公開済み** — 実際に投稿した内容の記録）

> **本書は Zenodo にアップロードしない。** 下記の内容をフォームの各欄へ
> 転記するための手元用メモである。Zenodo に添付するファイルは
> `note.pdf` のみ。

## 公開記録（2026-07-30、orange が実施）

| 項目 | 値 |
|---|---|
| version DOI | [10.5281/zenodo.21698700](https://doi.org/10.5281/zenodo.21698700) |
| **concept DOI**（引用に使う。常に最新版を指す） | [10.5281/zenodo.21698699](https://doi.org/10.5281/zenodo.21698699) |
| 添付 | `note.pdf` 134,410 バイト、md5 `8739950d6006af0d82f8cfc90c5950ef` |
| ソース commit | main `4a8aa7f`（全テスト green: 278 passed, 7 skipped, 1 xfailed） |

Zenodo API で照合済み（管理役、2026-07-30）: title / Working paper / 2026-07-30 /
v1 / cc-by-4.0 / 著者 `Kawashima, Wataru` + ORCID / Related works 3 件 /
keywords 9 語 / 添付 PDF は repo の `note.pdf` と md5 一致。

公開直後にメタデータのみ修正した点 2 件（DOI は不変）:

- 著者名が `KAWASHIMA, WATARU` と全大文字で入っていた → preprint v2 の
  `Kawashima, Wataru` へ統一。同一 ORCID の 2 レコードで表記が割れると
  著者ページや引用の集約で別名扱いになる余地がある
- keywords が 8 語で、`zero counting` の欠落と `GKP state`（単数化）・
  `homodyne tomograph`（`tomography` の末尾欠落 = 別語「断層撮影装置」）
  が発生していた → 下記 9 語へ修正

**教訓**: keywords は 1 語ずつ入力する UI なので、貼り付けではなく手入力の
過程で語の脱落・末尾切れが起きる。**Publish 後に API で照合すること**
（`curl -sSL https://zenodo.org/api/records/<id>`）。

---

対象: K_ε 理論ノート `docs/kepsilon-note/note.md` の PDF。
一次資料: タイトル決定 = issue #71 コメント 5124698689（orange、2026-07-30）、
abstract = PR #130 本文の版（同 PR で採用決定・用語精密化済み）。

- **Upload type**: Publication → **Working paper**
  （orange 決定 2026-07-30。ノート自身が冒頭で "Working note for the theory
  companion to the preprint" と自己記述しており、投稿先も未定なので Preprint
  より実態に合う）
- **Title**: Zero-counting lower bounds and measured K–ε curves for approximate Gaussian rank
- **Authors**: Person — Family name `Kawashima`, Given names `Wataru`,
  Identifier (ORCID) `0009-0002-7713-5547`; Affiliations/Role は空のまま
  （preprint v2 と同一。orange 指示 2026-07-30）
- **Publication date**: `2026-07-30`（投稿日 = 公開日。orange 実施 2026-07-30）
- **Version**: `v1`（Version 欄は `Recommended information` の中、Dates と
  Publisher の間にある）
- **Description**（PR #130 本文の abstract をそのまま）:

  We study how many Gaussian components a continuous-variable quantum state
  needs, adopting the approximate Gaussian rank framework of
  Hahn–Takagi–Ferrini–Yamasaki and the fidelity-ball relaxation of the
  stellar-rank literature; no novelty is claimed for the definitions. For
  mixed states we formulate the measure-theoretic ess-sup rank roof over
  generalized ensembles and prove its attainment and Gaussian-channel
  monotonicity — a partial answer, on the rank side, to the
  discrete-versus-continuous decomposition question the cited work leaves
  open. Our main contributions are three. First, for single-mode
  dictionaries of bounded common-squeezing Gaussian atoms, we prove
  zero-counting lower bounds: robust zeros of a target's Bargmann function
  survive fidelity-ball perturbation and are counted against an
  exponential-sum zero budget. The dictionary restriction is provably forced
  — counterexample families show no bound on the unrestricted rank can
  follow from raw disk zero counts alone. Second, an inequivalence theorem:
  the thermal lossy cat of our earlier preprint has Gaussian rank at most 2
  yet no finite-rank pre-loss operator representation at any efficiency,
  separating two natural compressibility notions in one direction. Third,
  measured curves: family-constrained approximation residuals and a
  real-data rank proxy on public GKP homodyne data, and a robust-zero census
  for finite-energy GKP states in which all three computed configurations
  support the lower-bound premises for the untruncated comb. The census is
  numerically supported, not computer-certified (float64 without outward
  rounding; numerical root-finding); a machine-checked claim register binds
  every quoted number to committed artifacts. Multimode extension and a
  general-squeezing plateau conjecture remain open.

- **License**: CC-BY-4.0（PDF 本文。コードは repo 側 MIT のまま — 別物なので
  混同しない。preprint と同条件）
- **Keywords**: approximate Gaussian rank; Gaussian rank; zero counting;
  Bargmann function; robust zeros; GKP states; continuous-variable quantum
  tomography; homodyne tomography; stellar rank
- **Related works**（2026-07-30 実機確認。旧フォームの「Related identifiers」
  ではなく **`Related works`** セクション。`Add related work` ボタンで 1 件ずつ
  追加する。並び順は Funding → Alternate identifiers → **Related works** →
  References。**`Alternate identifiers` は別セクションなので使わない**）:
  - `is supplement to` → doi:10.5281/zenodo.21457048（preprint concept DOI。
    常に最新版を指す）
  - `is supplemented by` → https://github.com/orangewk/wigner-splat（repository）
  - `cites` → doi:10.5061/dryad.t76hdr86j（Konno et al. GKP dataset。
    本文の参照 8′ と対応。#132 で追加済み）
- **Communities**: **使わない**。既存 3 レコード（preprint v1 `21457049` /
  v2 `21600248` / software `21387212`）はいずれもコミュニティ未登録であることを
  Zenodo API で確認済み（2026-07-30）。先例に揃える。コミュニティ登録は相手側
  キュレータの承認プロセスが走る外向きの操作なので、必要になってから別途判断する
- **Alternate identifiers / References / Dates / Funding / Contributors /
  Publisher / Languages**: すべて空のまま

## 添付ファイル（Zenodo にアップロードするのはこれだけ）

`docs/kepsilon-note/note.pdf` — main `4a8aa7f` でコミット済み（#133）。
実 path: `C:\dev\wigner-splat-wt\admin\docs\kepsilon-note\note.pdf`

ビルドレシピ（本線が確定、管理役が独立再現）:

```
pandoc note.md -s -o note.tex --pdf-engine=xelatex -V mainfont=Cambria \
  -V geometry:margin=2.7cm -V fontsize=10pt
xelatex -interaction=nonstopmode note.tex   # 2 回
grep -c "Missing character" note.log        # 0 を確認
```

`.tex` を経由するのは `.log` を残して欠字を機械検査するため。`lualatex` は
この環境でフォーマット未構築のため使わない（2026-05 から一度も動作せず）。

本番ビルド実測値（main `6e7a7c7`）: 11 ページ、letter（612×792pt、公開済み
preprint と同一）、`Missing character` 0（2 パス）、134,410 バイト。
`Overfull \hbox` 1 件（宣言表 D3 行の `N_robust_lifted_bounded`。等幅 1 語で
分割不能。最右列なので列衝突はしない。修正前の main は 4 件だった）。

## 書誌の一次資料照合（2026-07-30、管理役）

参照 8′ の書誌は repo 内文書からの転記ではなく、一次資料で照合済み。

| 項目 | 照合先 | 結果 |
|---|---|---|
| Dryad DOI `10.5061/dryad.t76hdr86j` | DataCite API | 実在。publisher Dryad、2024、rights `cc0-1.0`、第 1 著者 `Konno, Shunya`、`IsCitedBy 10.1126/science.adk7560` |
| 論文タイトル | Crossref API（`10.1126/science.adk7560`） | "Logical states for fault-tolerant quantum computation with propagating light" — 完全一致 |
| Science **383**, 289 (2024) | 同上 | volume 383 / page 289–293 / 2024 — 一致 |

CC0 であることは本文に書いていない（本線判断）。ライセンス主張を本文へ増やさず
Zenodo メタデータ側の `cites` に委ねる方針。CC0 は帰属を要求しないため、
引用を置いている現状は要求水準を上回る。

## 公開前の未解決事項

なし（2026-07-30 時点）。

## 投稿手順

zenodo.org → Upload → New upload → 上記を転記 → `note.pdf` を添付 → Publish。

UI の注意（実機準拠、`docs/2026-07-26-preprint-v2-correction-list--done.md` より）:

- **Version 欄**は `Recommended information` の中（デフォルトで折りたたみ）。
  展開すると Contributors / Keywords and subjects / Languages / Dates /
  **Version** / Publisher の順。Dates と Publisher の間に `v1` を入れる
- **`Dates` セクションは使わない。** これは受理日・収集日などを足す任意欄で、
  足すごとに Type の選択が要る。`2026-07-30` は別の必須欄
  **`Publication date`** に入れる（そちらに Type は無い）
- **`Add description` は押さない。** メインの Description 欄に abstract を
  貼るだけでよい（この欄に Type は無い）。`Add description` で追加ブロックを
  作った場合のみ **Type が必須**になり、未選択だと
  `The draft was not published. Record saved with validation feedback in
  Basic information` で弾かれる。今回は追加ブロック不要
  （preprint v2 では訂正要約を追加ブロックで書いたためこの罠を踏んだ。
  経緯は `docs/2026-07-26-preprint-v2-correction-list--done.md`）

発行された DOI は README・issue #71 に反映する。
