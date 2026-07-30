# Zenodo 投稿メタデータ（準備稿 — orange が投稿フォームに貼る用）

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
- **Related identifiers**:
  - `is supplement to` → doi:10.5281/zenodo.21457048（preprint concept DOI。
    常に最新版を指す）
  - `is supplemented by` → https://github.com/orangewk/wigner-splat（repository）
  - `cites` → doi:10.5061/dryad.t76hdr86j（Konno et al. GKP dataset。
    本文の参照 8′ と対応。#132 で追加済み）
- **Communities**: （任意）quantum-physics 系があれば
- **Notes 欄**: 特記なし

## 添付ファイル

`note.pdf`（本書と同じディレクトリに配置予定）。

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

- Version 欄は `Recommended information` の中、Dates と Publisher の間
- Description を追加したら **Type の選択が必須**。空だと Publish が
  validation で弾かれる

発行された DOI は README・issue #71 に反映する。
