# 公開された実測 homodyne / quadrature データ調査

状態: recorded
調査日: 2026-08-19 JST
対象: `wigner-splat` の連続変数量子状態トモグラフィー。符号付きガウス混合、物理的 Gaussian-ket / BB† モデル、homodyne データへのフィットを想定する。

## 結論

現在の導入優先順位は次のとおりとする。

1. **Kawasaki et al. の Dryad データ**（`10.5061/dryad.9p8cz8wqn`）を最初の追加データにする。公式 README が `.mat` の変数名、位相、ショット数、単位、実験条件を定義しており、既存の Konno データと同じ `[(theta, samples)]` 形式へ変換しやすい。
2. **Endo et al. の 2026 年 Zenodo raw data**（`10.5281/zenodo.20640586`）を、取得可能性とライセンスを確認したうえで次の主ベンチマークにする。論文は、光子数識別用 TES の pulse height と homodyne 結果の組、12 位相、n=2–4 の大規模実測データを含む raw data と明記している。規模と物理的非ガウス性の点では最も強いが、Kawasaki よりローダーとストリーミング処理が重い。
3. **Caron et al. の Figure 6 データ**（`10.57745/MBDJEZ`）を、小規模な大振幅 squeezed cat のクロスチェックに使う。公開ファイルは `Figure6.csv` で、Data Gouv のメタデータ上は 2 変数・16,338 観測値。ただし、論文の「16,339 quadrature measurements」と 1 件の差があり、列名・位相・単位はダウンロード後に確認する。
4. 既存の **Konno et al. の GKP データ**（`10.5061/dryad.t76hdr86j`）を共通の回帰基準として維持する。新規データの性能を比較する際、データ形式だけでなく、GKP の格子構造に対する既存実験の再現性も守る。
5. **Zhou et al. の graph-state Dryad データ**（`10.5061/dryad.s7h44j1n3`）は、多モード・生 oscilloscope trace のテスト用に有用。ただし Gaussian graph state が主対象であり、Wigner negativity や猫状態の out-of-family ベンチマークには使わない。

Lopetegui、Parker、Fletcher、Gerrits は、homodyne または CV tomography と関係するが、今回の「公開された光学系の実測 raw quadrature」要件にはそのまま合わない。特に Lopetegui と Parker は、公開物の中心がシミュレーションまたは解析コードである。Gerrits の猫状態データは、後続論文が「公開されておらず、著者への合理的な依頼で取得」と記載している。

## 判定基準

「実測 raw」と「図を再現するためのデータ」を区別する。採用判定は次の順序で行う。

| 判定項目 | 採用条件 |
|---|---|
| 実験性 | 実験で取得した homodyne / quadrature 値である。シミュレーションだけのデータは除外する。 |
| 入力適合性 | 位相タグ付きの 1 次元 quadrature sample、または明確な変換規則を持つ多モード sample である。 |
| 物理メタデータ | `hbar` 規約、真空分散、位相定義、検出効率・損失、条件変数が追跡できる。 |
| 再現性 | DOI、バージョン、元ファイルの checksum、ライセンス、変換手順を記録できる。 |
| 研究価値 | GKP、非ガウス性、損失、rank、位相数、ショット数のいずれかを既存実験の外へ広げる。 |

## 候補の比較

| 候補 | 公開物の実体 | `wigner-splat` への適合 | ライセンス／注意 | 推奨用途 |
|---|---|---|---|---|
| Konno et al. (2024) | Dryad の `quad_*.npy` 6 ファイル。位相は `0, ±30, ±60, -90` 度。各配列は homodyne 信号を波束形状で積分した processed quadrature event。 | **A**。既存 `experiments/12_gkp_data/run.py` が `[(theta_rad, samples)]` に変換済み。 | Dryad のデータは CC0 方針。元 README と DOI を保持する。 | GKP 回帰基準、rank・loss・検出効率の比較。 |
| Kawasaki et al. (2024) | Dryad に `.mat` 11 ファイル。ファイル名は `quad_01GHz_xxmW_yydB.mat`。各 MATLAB 変数は `pzzdeg` 形式、1×5000、各点が quadrature event。`hbar=1/2` の無次元単位。 | **A**。位相と条件がファイル／変数名に現れ、単一モードの位相別 sample に直接落とせる。 | Dryad のデータは CC0 方針。再配布時は個別 DOI とデータ引用を併記する。 | 最初の追加実測。ポンプ強度・追加損失・高帯域 PSS の比較。 |
| Endo et al. (2026) | 論文が Zenodo に simulation/analysis code と raw data を公開。TES pulse height と homodyne outcome のペアを保存し、n=2,3,4 などへ offline 分類。12 位相、各位相約 8×10^6、全体 10^8 超と記載。 | **A- / B+**。sample 抽出後は適合するが、TES 条件付きデータ、巨大ファイル、位相・光子数メタデータの扱いが必要。 | Zenodo record のライセンスとファイル一覧は取得時に確認するまで未確定。確認前に repo へコピー／再配布しない。 | 最重要の非ガウス raw ベンチマーク。n=2→4、ショット数、negativity、検出効率の外挿。 |
| Caron et al. (2026) | Recherche Data Gouv の `Figure6.csv`。2 変数、16,338 観測値、公開ファイル。Figure 6 用の実験データ。論文は 16,339 quadrature measurements と記載。 | **B+**。CSV は小さく扱いやすいが、列の意味と位相の紐付けを現物確認する必要がある。 | Etalab Open License 2.0（CC-BY 2.0 と互換）。データ引用を残す。 | 大振幅 squeezed cat、3 つの負領域、単一条件での再構成クロスチェック。 |
| Zhou et al. (2025) | Dryad に 1–4D graph-state の CSV zip、合計約 2.11 GB。raw oscilloscope trace、probe / conjugate homodyne の 2 列、任意で trigger 列、サンプリング設定などの補助メタデータ。 | **B**。既存の単一モード位相別 sample ではなく、多モードの同時信号と drive 条件からの前処理が必要。 | Dryad のデータは CC0 方針。大容量のため repo には置かない。 | Gaussian graph-state、共分散、raw trace、マルチモード入力境界の検証。 |
| Lopetegui et al. (2022) | Zenodo の図再現データ・コードと、論文末尾で使った simulated homodyne detector data。`Homodyne_data_analysis.zip` は 7.0 GB。 | **C**。公開ページ自身が simulated data を含むと説明し、論文も実験データではなく rejection sampling による realistic simulation と記載。 | CC BY 4.0。 | Fisher-information / steering 指標の合成データ比較。実測 raw の代用にはしない。 |
| Fletcher et al. (2019) | Zenodo の 19.1 MB zip。solitary electron の energy-time tomography の図を生成するデータ。 | **C**。CV tomography だが光学 homodyne ではなく、時間依存障壁の transmission と inverse Radon reconstruction。 | CC BY 4.0。 | 異なる物理系への手法移植・Radon 入力境界の参考。 |
| Gerrits et al. (2010) | NIST の論文説明では 1087 homodyne measurements による photon-subtracted cat。 | **D**。Bayesian 論文は、データは公開されておらず著者への reasonable request で取得可能と記載。 | 公開ライセンスを確認できない。 | 取得依頼の候補。公開データとしては数えない。 |
| Parker et al. (2020) | Dryad の Mathematica notebook。cat-state entanglement swapping の密度行列・fidelity・success probability を生成するコード。 | **D**。実験 shot data ではなくモデル計算。 | 個別のコードライセンスを確認できない。Dryad のデータ用 CC0 方針をコードへ自動適用しない。 | 損失・非理想 homodyne の forward model 参考。 |

## 候補ごとの確認結果

### Kawasaki et al. — 最初に追加する実測データ

Dryad の公式ページは、状態を squeezed light から photon subtraction で生成した PSS と説明している。PSS は Schrödinger cat の近似であり、追加損失を変えて tomography 結果を比較する構成である。ファイル名の `xxmW` は OPA pump power、`yydB` は追加損失を表す。各 `.mat` は複数の `pzzdeg` 配列を持ち、各配列は 5000 個の quadrature event である。

この構造は Konno のローダーに最も近い。追加するアダプタの責務は、MATLAB 配列を読み、`pzzdeg` の `zz` を位相として `[(theta_rad, samples)]` に正規化し、ファイル名から `pump_mW` と `loss_dB` をメタデータへ保存することだけでよい。README の `hbar=1/2` 表記を repo の真空分散規約と同一視せず、vacuum calibration と論文の定義を照合してから数値変換を決める。位相の符号反転、単位変換、損失補正はローダー内で暗黙に行わず、論文・README に明記された規約として実験設定に記録する。

### Endo et al. — 最も価値が高いが、まず取得検証する raw data

論文は、10 ps temporal mode の pulsed homodyne、5 MHz pump repetition、TES の photon-number-resolved heralding を組み合わせた実験を報告する。n=2,3,4 の状態について Wigner negativity が測定され、論文の Data and materials availability は raw data と解析コードの Zenodo DOI を指定している。

このデータは Kawasaki と異なり、quadrature だけを単純に位相別ファイルから読むとは限らない。TES pulse height と homodyne outcome をペアで保持し、後処理の photon-number discrimination を再現する必要がある。したがって導入順は次の二段階にする。

1. Zenodo record のファイル一覧、ライセンス、README、checksum、ストレージ形式を取得する。
2. 全 raw data を repo に入れず、n=2 の小さい検証 slice を一時領域に展開し、12 位相の `[(theta_rad, samples)]` を生成してから n=3/4 と大規模 streaming へ進む。

論文にある `α_eff`、homodyne efficiency、TES efficiency は「真値」としてフィットへ固定しない。まずは、未補正 measured PDF の held-out NLL、条件別の marginal、rank/loss model の比較を行う。効率を fit する場合は、実験校正値との比較を別の表で記録する。

### Caron et al. — 小規模な squeezed-cat クロスチェック

Data Gouv のデータセットは Figure 6 に対応する `Figure6.csv` 一つからなり、ファイルメタデータは 2 変数・16,338 観測値・600 KB と記載する。ライセンスは Etalab Open License 2.0 である。

論文は 16,339 quadrature measurements を用いた QST と述べるため、リポジトリの観測値数との差を導入時のデータ整合性チェックにする。現物 CSV のヘッダー、欠損値、位相列の分布、quadrature 列の規格化、Figure 6(a)–(c) のどの補正状態に対応するかを確認し、確認できない場合は「再構成済み Figure 6 用データ」として使い、raw homodyne と呼ばない。

### Zhou et al. — Gaussian の多モード raw trace

Zhou の Dryad データは、probe と conjugate の homodyne signals を含む oscilloscope trace と、sampling rate、vertical scale、shot 数、record length などの補助ファイルを公開している。1–4 次元 graph state の各 drive 条件と shot が整理されているため、raw signal → calibration → covariance の一貫性を検査する教材としては非常に良い。

一方、対象状態は Gaussian graph state であり、単一モードの猫状態や GKP negativity の検証には直結しない。`wigner-splat` の多モード入力契約を拡張するときの前処理・メタデータ設計に限定して使う。

## `wigner-splat` への取り込み契約

既存の実験12が使う単一モード契約を共通形式とする。

```text
data = [(theta_rad: float, samples: ndarray[shot]), ...]
```

各データセットに対して、sample とは別に次の provenance envelope を保存する。

```text
source_doi
source_url
source_version_or_publication_date
source_file
source_sha256
raw_or_processed
state_family
condition                 # pump, loss, photon number, drive, etc.
phase_definition
quadrature_convention     # hbar, vacuum variance, sign convention
detector_efficiency
additional_loss
license
transform_description
```

ローダーと実験の境界は次のとおりにする。

- ローダーはファイル形式、位相の単位、配列形状、欠損値、checksum を扱う。
- 物理補正（loss、efficiency、electronic noise、offset subtraction）はローダーへ埋め込まない。
- 実験スクリプトが、未補正データと補正モデルを明示的に比較する。
- 元データは repo にコピーせず、取得 manifest と再現可能な download 手順を保存する。大規模 raw data は特に Git 管理しない。
- 変換後の sample 数、位相数、平均、分散、最小最大、vacuum calibration を検証ログへ出力する。結論文はこのログから生成する。

## 実験12–21への適用案

| 実験群 | 実測データでの使い方 |
|---|---|
| 12–14 GKP baseline / efficiency / rank | Konno を固定基準にし、Kawasaki の PSS を同じ single-mode pipeline に通す。Konno の GKP 専用結論と、PSS の猫近似に対する結論を混ぜない。 |
| 17 loss control | Kawasaki の追加損失系列（0–20 dB）を同一 pump 条件の loss sweep として使う。データ由来の損失と fit した `eta` を別フィールドにする。 |
| 18 GKP saturation | Konno の格子構造を主結果とし、Endo / Caron を「GKPそのものではない非ガウス資源」の saturation・negativity 対照にする。猫から GKP への生成能力をデータだけから主張しない。 |
| 19–21 out-of-family / thermal・noise 対照 | Caron の大振幅 squeezed cat、Endo の n=2–4 条件、Zhou の Gaussian graph-state を分けて使う。Lopetegui の simulated data はこの対照に追加できるが、実測結果の行へ入れない。 |

各実験で、実測データに未知の状態真値はない。主指標は fixed train/test split の held-out per-sample NLL と phase-wise marginal overlay とする。論文に再構成済み density matrix がある場合は二次的な cross-check とし、そこから raw data の fidelity を逆算したことにはしない。

## 取得前チェックリスト

1. DOI の version と公開日を記録する。
2. README、データファイル一覧、ライセンス、checksum を保存する。
3. 配列／列の意味を現物ファイルから確認する。検索スニペットや論文図だけから列の意味を推定しない。
4. `hbar`、vacuum variance、quadrature sign、phase origin を記録する。
5. raw、processed quadrature、figure-only、simulation を分類する。
6. まず 1 条件・1 位相の小さい slice で loader smoke test を行う。
7. 全条件を対象に shot 数、位相数、欠損、重複、分散、外れ値を確認する。
8. 取得した外部データを repo にコミットする場合は、ライセンスとデータ引用を先に確認する。特に Endo の Zenodo record はこの調査時点でライセンス未確認である。

## 一次資料

- Konno et al., [Dryad: Propagating Gottesman–Kitaev–Preskill states encoded in an optical oscillator](https://datadryad.org/dataset/doi:10.5061/dryad.t76hdr86j), DOI `10.5061/dryad.t76hdr86j`.
- Kawasaki et al., [Dryad: High-rate generation and state tomography of non-Gaussian quantum states](https://datadryad.org/dataset/doi:10.5061/dryad.9p8cz8wqn), DOI `10.5061/dryad.9p8cz8wqn`; [Nature Communications article](https://www.nature.com/articles/s41467-024-53408-w), DOI `10.1038/s41467-024-53408-w`.
- Endo et al., [arXiv: Picosecond Schrödinger cat states for ultrafast optical quantum processing](https://arxiv.org/abs/2606.24002), raw data DOI `10.5281/zenodo.20640586`.
- Caron et al., [Recherche Data Gouv dataset](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/MBDJEZ), DOI `10.57745/MBDJEZ`; [arXiv:2601.09672](https://arxiv.org/abs/2601.09672).
- Zhou et al., [Dryad: Generation of reconfigurable hypercubic graph states in 1–4 dimensions](https://datadryad.org/dataset/doi:10.5061/dryad.s7h44j1n3), DOI `10.5061/dryad.s7h44j1n3`.
- Lopetegui et al., [Zenodo figure data](https://zenodo.org/records/7307512), DOI `10.5281/zenodo.7307512`; [PRX Quantum article](https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.3.030347).
- Fletcher et al., [Zenodo dataset](https://zenodo.org/records/3533120), DOI `10.5281/zenodo.3533120`; [Nature Communications article](https://doi.org/10.1038/s41467-019-13222-1).
- Chapman et al., [Bayesian homodyne and heterodyne tomography](https://doi.org/10.1364/OE.456597), DOI `10.1364/OE.456597`.
- Gerrits et al., [NIST publication record](https://www.nist.gov/publications/generation-optical-schrodinger-cat-states-number-resolved-squeezed-photon-subtraction).
- Parker, [Dryad: Photonic hybrid state entanglement swapping using cat state superpositions](https://datadryad.org/dataset/doi:10.5061/dryad.05qfttf0c), DOI `10.5061/dryad.05qfttf0c`.
- Dryad, [How to reuse Dryad data](https://v3.datadryad.org/help/guides/reuse)（CC0 のデータ方針）。
