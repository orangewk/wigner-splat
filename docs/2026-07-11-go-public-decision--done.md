# wigner-splat 公開判断記録

日付: 2026-07-11
状態: 公開準備完了。可視性の変更と GitHub 設定は orange が判断・実施する。

## 判断の前提

`wigner-splat` は、符号付き異方性ガウス混合を homodyne 測定データに
フィットし、Wigner 関数を再構成する予備的な研究プロトタイプである。
README に記録した測定条件・実験範囲を越えて、一般的な優位性や
論文級の確立済み成果としては扱わない。

公開する場合も、成功した結果だけでなく、反証条件、未検証項目、
失敗した物理化手法を同じ重さで残す。公開は主張を強めるためではなく、
コード、実験条件、限界を検証可能にするために行う。

## 既知の物理性 caveat（Issue #8）

符号付きガウス混合が表す Wigner 関数は、対応する密度演算子
ρ が正定値（ρ ⪰ 0）になる保証を持たない。Wigner 負性は物理状態でも
生じる一方、任意の符号付き混合が物理状態に対応するわけではない。

実験08では、1モードは full-parameter PSD polish と事後射影により、
品質低下の反証条件と PSD 条件を両立できた。一方、3モードでは
weight-only と少数の shape parameter による物理化の双方で品質が大きく
低下し、現行の fidelity 優位と PSD 物理性の間に強い tension が残った。
3モードの full 28-parameter/splat による物理化は未検証である。
したがって、現状の3モード値は厳密な物理状態の fidelity ではなく
Wigner overlap score を含む予備的結果として提示する。

## 公開前に確認・整備した事項

- 2026-07-11 の gitleaks 全履歴スキャン（43 commits）は 0 leaks。
- 認証ファイルが tracked されていないことを確認済み。
- README と research log から private 親リポへのリンク・固有名を除去。
- PR、push、手動実行、週次実行の gitleaks workflow を追加。
- MIT License と最小構成の `CITATION.cff` を追加。
- GitHub Actions の週次 Dependabot 更新を追加。

これらは公開時の事故リスクを下げるための準備であり、研究結果の
妥当性や一般化可能性を追加で保証するものではない。

## orange が GitHub 上で手作業する設定

可視性を Public に変更する最終判断と同時に、orange が次を確認・設定する。

1. Secret Scanning を有効化する。
2. Push Protection を有効化する。
3. `main` への直接変更を防ぐ branch protection を設定する。

可視性変更そのもの、および上記 GitHub 設定はこの実装の範囲外とする。
