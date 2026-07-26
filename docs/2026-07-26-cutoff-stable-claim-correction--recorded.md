# 2026-07-26 「cutoff-stable」主張の訂正

状態: recorded（訂正の実施記録。公開済み preprint の扱いのみ orange 判断待ち）

## 何が誤りだったか

Route B の best-found 残差について、リポジトリ全体で

> approach the target to 1–2×10⁻³ in 1 − F (**cutoff-stable** best-found values)

と書いていた。実測（`results_routeB.json` squeezed 系列、seed 3 本の best を
(n_score, K) ごとに集計）はこうである:

| n_score | K=2 | K=4 | K=8 |
|---|---|---|---|
| 8 | 2.50e-3 | 1.60e-3 | 1.36e-3 |
| 10 | 3.21e-3 | 2.20e-3 | 1.98e-3 |
| 12 | 3.44e-3 | 2.37e-3 | 2.17e-3 |

採点最大カットオフ n=12 で **≈2–3×10⁻³**、しかも**全 K でカットオフとともに単調増加**している。
数値レンジが違うだけでなく、「cutoff-stable」という安定性の主張自体が偽である。

定性的な結論（"the boundary is thin"、および Route B が上界であって下界ではないこと）は
変わらない。変わるのは引用すべき数値と、安定性を主張してよいかどうかである。

## 根本原因

`experiments/20_noninclusion/routeB.py` の判定出力が、この文言を**ハードコードで印字していた**。
系列が単調増加していても "and are cutoff-stable" が必ず出る構造で、計算された判定ではなく
無条件の宣言だった。README・preprint の文言はここから流れている。

## 実施した訂正

- `README.md` / `README.ja.md` — PR #106（最大採点カットオフでの値と微増中である旨へ）
- `experiments/20_noninclusion/routeB.py` — 判定を計算に変更。カットオフ系列の傾向
  （increasing / decreasing / non-monotone）を実データから判定して印字し、`ruling.cutoff_trend`
  として JSON にも残す。安定性の主張は削除
- `docs/preprint/2026-07-preprint--wip.md` — 同趣旨へ修正
- `docs/kepsilon-note/note.md` — §7.3 に引用ポリシーとして既に反映済み
  （カットオフ系列を常に併記、headline は最大採点カットオフ、"cutoff-stable" は使わない、
  圧縮レンジ "1–2×10⁻³" はリポジトリ全体で deprecated）

## 触っていないもの

`experiments/20_noninclusion/out_routeB*.log` は**当時の主張の記録**であり書き換えない。
何をいつ主張していたかの証拠性が失われるため。

## 未決（orange 判断）

`docs/preprint/preprint.md` は Zenodo にアーカイブ済みで DOI が振られており、
旧文言のまま公開されている。さらにその DOI を貼ったアウトリーチメールが送信済みである。

訂正版を concept DOI 配下の新バージョンとして出すかどうかは orange の判断。
旧版は残る（それが正しい）。
