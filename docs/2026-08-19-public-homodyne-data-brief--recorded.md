# 公開 homodyne / quadrature 実験データ候補

調査日: 2026-08-19 JST
用途: `wigner-splat` の実測データベンチマーク候補を本流へ共有するための要約。

## 候補一覧

| データ | 公開物の実体 | 実験データとしての確度 | `wigner-splat` への有用性 | 主な制約 |
|---|---|---|---|---|
| **Kawasaki et al. (2024)**  [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.9p8cz8wqn) | 位相別 `.mat` quadrature。各配列 1×5000。OPA pump power と追加損失の条件違いを含む。 | **A** — 一次資料が homodyne 測定による photon-subtracted state の quadrature data と明記。 | **高** — 既存 Konno データに近く、損失・高帯域 PSS・非ガウス性を比較できる。 | oscilloscope の raw trace ではなく、波束積分後の quadrature。 |
| **Endo et al. (2026)**  [論文](https://arxiv.org/abs/2606.24002) / [Zenodo DOI](https://doi.org/10.5281/zenodo.20640586) | TES pulse height と homodyne outcome の raw data。12 位相、光子数条件付き、論文記載で全体 10^8 超。 | **A** — 論文が raw data と解析コードの Zenodo 公開を明記。 | **非常に高** — n=2–4 の猫状態、Wigner negativity、ショット数・検出効率の検証に使える。 | Zenodo のファイル構成とライセンスは取得時に確認が必要。 |
| **Caron et al. (2026)**  [Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/MBDJEZ) | Figure 6 用 `Figure6.csv`。2 変数、16,338 観測値。大振幅 squeezed cat。 | **B** — 実験由来の Figure 6 データだが、完全 raw データではない。 | **高** — 大振幅猫状態と複数の Wigner 負領域のクロスチェックに使える。 | 論文の quadrature 数（16,339）と1件差。列の意味・単位は現物確認が必要。 |
| **Konno et al. (2024)**  [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.t76hdr86j) | 位相別 `quad_*.npy` 6ファイル。processed quadrature samples。 | **B** — homodyne oscilloscope data の後処理値であることを確認済み。 | **高** — 既存の GKP 回帰基準。 | 既存採用済み。GKP 固有の基準であり、猫状態ベンチマークではない。 |
| **Zhou et al. (2025)**  [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.s7h44j1n3) | 1–4D graph-state の raw oscilloscope homodyne trace。合計約 2.11 GB。 | **A** — probe / conjugate homodyne signals の実測 trace と明記。 | **中** — 多モード入力、共分散、Gaussian graph-state の検証に有用。 | Gaussian 状態が主対象で、猫状態・GKP negativity の直接ベンチマークではない。 |
| **Lopetegui et al. (2022)**  [Zenodo](https://zenodo.org/records/7307512) | 図再現データ・コード、および simulated homodyne detector data。 | **C** — 実測 raw homodyne データではない。 | **補助的** — Fisher information / steering の合成データ比較。 | 実測データ候補としては扱わない。 |
| **Gerrits et al. (2010)**  [NIST record](https://www.nist.gov/publications/generation-optical-schrodinger-cat-states-number-resolved-squeezed-photon-subtraction) | photon-subtracted cat の homodyne 実験データ。 | **D** — 実験データの存在は確認できるが、公開取得先は確認できない。 | **取得できれば高**。歴史的な猫状態対照。 | 著者への依頼が必要。公開データとしては数えない。 |

## 確度の定義

- **A**: 一次資料が、実験取得データまたは raw data と明記している。
- **B**: 実験由来だが、processed / figure-level データである。
- **C**: simulation、再構成結果、または図再現用データが中心である。
- **D**: 実験データは存在するが、公開取得できない。

## 要約

実測データとして優先すべき候補は Kawasaki と Endo である。Caron は小規模な squeezed-cat クロスチェック、Konno は GKP の既存基準、Zhou は Gaussian 多モード trace の補助候補と位置づける。Lopetegui は実測 raw データとして扱わず、Gerrits は公開データ候補に含めない。

詳細な調査根拠は [公開 homodyne / quadrature データ調査](2026-08-19-public-homodyne-data-survey--recorded.md) を参照。
