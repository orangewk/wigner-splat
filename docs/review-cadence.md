# 固定 SHA レビューの cadence 規律(PR #158 研究ループ)

由来: QR5 v0.7 の一括執筆 → luna R1 受理不可(blocking 4 件、2026-08-09)の教訓と、
one-change packet 運用での捕捉実績(ν-chart 不連続を証明への焼き込み前に捕捉、2026-08-11)。
cadence は協力者(Sol 等)の自己評価や熱量ではなく、本文書の packet 規律で固定する。

## 粒度の基準

1 packet = **新しい数学的主張 1 個**、または**下流の証明が消費する interface 定義 1 個**。
目安 100–200 行。レビューアが主張のほぼ全数を機械検算(シンボリック/厳密演算/高精度数値)
できる規模を保つ。この規模を超える束は、束のまま出さず主張単位に切り直す。

## 固定 SHA レビューを要する変更

- 新しい statement の proof draft への昇格
- 下流が消費する chart / interface / 契約の定義・変更
- 主張の撤回と、それに伴う台帳(ledger)・status 表の書き換え
- 反例・witness の registry への追加

## レビュー不要(通常 commit でよい)変更

- 編集修正(文構造・リンク・誤字)
- 版履歴・review history の追記
- 受諾済み nonblocking minor の反映
- 生成ブロック・テストの機械的更新

## packet の種別

- **review packet**: 固定 SHA + gate 列挙 + PASS/BLOCKED 判定を求める。実装済み内容が対象。
- **consultation packet**: 設計段階の GO / REVISE / NO-GO を求める。証明の authoring location
  ではなく、採否は本線が実装 packet で確定する。

## レビューア独立性

- consultation で設計に関与したレビューアは、その実装 packet に対して完全独立ではない。
  主張が純代数で機械検証可能な場合は単独判定可、それ以外は第三者(luna 等)を併用する。
  レビュー comment に自己設計該当の有無を申告する。
- 判定には毎回「レビュー側で独立に新規作成した検算」を含める。検算を伴わない PASS は
  出さない(連続 PASS の儀式化のサイン)。
