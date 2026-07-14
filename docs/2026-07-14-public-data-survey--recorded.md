# 2026-07-14 公開 homodyne 実データ発掘サーベイ — 結果記録

状態: recorded(並走スカウトランナー [Sonnet] による調査 + 本セッションでの環境検証。**次のアクションは orange のローカル環境が必要** — 下記参照)
出所: [2026-07-13 方向性記録](2026-07-13-position-and-direction--recorded.md) の推奨②「公開データセットの発掘」の実施。実験装置なしで実データ検証(dreams #4「実データでの反証こそ最終試験」)に到達する 2 経路のうちの 1 つ。

---

## 結論(1段落)

オープンな「LO 位相タグ付きの生 homodyne quadrature ショットデータ」は**極めて希少**。15〜20 通りの検索(Zenodo / Dryad / figshare / OSF / Harvard Dataverse / GitHub / 論文 Data availability)で、確定的な発見は **1 件のみ**: **古澤研(東大)の Science 2024 GKP 論文の Dryad データセット**。cat / photon-subtracted / Fock 系の本命グループ(Lvovsky、DTU、LKB、Zavatta-Bellini、Yale 系)は該当実験を多数持つが**生データの一般公開例はゼロ** — この「非公開が常態」という構造的知見自体が、データ乞い型アウトリーチ(方向性記録 §5.1)の論拠になる。

## 最有力候補(唯一の確定発見)

**伝搬光 GKP 状態の生 quadrature データ — 古澤研**
- 論文: Konno, Asavanant, Hanamura, …, Furusawa, *"Logical states for fault-tolerant quantum computation with propagating light"*, **Science** 383, 289 (2024)。doi:10.1126/science.adk7560 / arXiv:2309.02306
- データ: Dryad **doi:10.5061/dryad.t76hdr86j** — https://datadryad.org/dataset/doi:10.5061/dryad.t76hdr86j
- 内容(検索インデックスからの引用): "quadrature values of generated states obtained by postprocessing of homodyne detector data collected via oscilloscope" — 損失補正なしのホモダイン測定による GKP 状態検証の生 quadrature 値
- 適合度: **高**。非ガウス状態 + 生ショット + 位相走査の可能性が高い。しかも GKP は dreams #7 の「スプラット表現がネイティブに合う」対象で、格子構造 = 符号付きガウス格子。BB† 側も squeezed-product ansatz(PR #36)が入った今、GKP 近似族を張る部品が揃っている
- 未確認事項(現物確認が必要): 位相数 × ショット数、検出効率の記載、ファイル形式、ライセンス(Dryad は原則 CC0)

## ⚠ 環境制約(本セッションで実測)

**この Claude Code 実行環境のネットワークポリシーは datadryad.org / zenodo.org への接続を遮断している**(agent proxy が CONNECT に 403、`recentRelayFailures` で確認)。したがって:
- スカウトランナーの探索で出た「403 Forbidden」の一部はサイト側 bot 対策ではなく**環境ポリシー由来**の可能性がある(= 上記以外にも見逃しがあり得る。ローカルブラウザでの Zenodo 再検索は価値あり)
- **ダウンロード検証はこの環境からは実行不可。orange のローカル環境での作業が必要**:
  1. https://datadryad.org/dataset/doi:10.5061/dryad.t76hdr86j をブラウザで開き、ファイル一覧・サイズ・README を確認
  2. 確認事項: (a) 位相タグの有無と位相数 (b) ショット数/位相 (c) 単位・規格化規約(真空分散 1/2 か 1 か) (d) 検出効率・電子ノイズの記載 (e) ライセンス
  3. 使えそうなら repo にローダ(`[(theta, samples)]` 形式へのアダプタ)を書く — 環境にデータを持ち込めばフィットはこちらで回せる

## 次点(要リクエスト系 — アウトリーチ素材)

| 相手 | 対象データ | 備考 |
|---|---|---|
| Zavatta & Bellini(INO-CNR) | 単一光子 Fock の homodyne 生データ(PRA 70, 053821, 2004 — 単一光子 Wigner 負性の歴史的実験) | 公開なし。論文記載の連絡先: bellini@ino.it |
| DTU(Andersen / Neergaard-Nielsen) | cat 状態系列 | 公開リポジトリなし。個別依頼 |
| LKB(Treps / Parigi) | 多モード squeezed | 同上 |
| Yale / Alice & Bob 系 | キャビティ displaced-parity 生データ | 公開例なし。測定モデルが違うためフォワードモデル差し替えが必要 |
| WilliamBidle/QST(GitHub) | コヒーレント状態の実測データ(README 言及、repo にはシミュのみ) | 著者に問い合わせれば入手可能性 |

副次: Zenodo 10803759 / 10810149(フォトン数分解検出器の POVM トモグラフィー)は homodyne ではないが、検出器較正・ノイズモデルの参考候補。

## 探索ログ

スカウトランナーが 20 件の検索クエリと空振りを記録済み(本記録の元レポート)。要旨: Zenodo/OSF/Dataverse 系は "quadrature" の数学ライブラリノイズが多い、GitHub の QST リポジトリはシミュレーションデータのみ、cavity 系 GKP の公開例なし。1 件、検索エンジンの AI 要約が実在しない Zenodo DOI を提示した疑いがあり(検証不能)、**要約経由の DOI は現物確認するまで信用しない**こと。

## 推奨アクション(優先順)

1. **orange のローカル作業**: Dryad GKP データセットの現物確認(上記チェックリスト)。使えるなら zip をこの環境に持ち込む(セッションへのファイル添付 or repo 外部ストレージ)
2. 使えると確認でき次第: ローダ + GKP ターゲットの参照実装(スプラットは格子とネイティブ整合、BB† は squeezed-product で近似族)— dreams #7 の前倒し
3. 並行: アウトリーチ計画(#18–#23)に「データ提供依頼」の型を追加(bellini@ino.it が最初の具体候補)。「非公開が常態」というサーベイ結果は依頼文の動機づけに使える
4. ローカルブラウザで Zenodo を再検索(環境ポリシーで見えていない可能性の潰し)
