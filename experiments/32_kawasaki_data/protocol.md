# Experiment 32 — Kawasaki homodyne external-data protocol

状態: **pre-data-values / packet 1**

固定日: 2026-08-24 JST

Issue: #180

本 packet は取得契約・loader・後続解析の事前固定だけを扱う。2026-08-24 の
固定時点で確認した source metadata の範囲は `source_manifest.json` に記録した。
quadrature 値、統計量、分布、fit 結果は確認していない。

## 1. Packet 1 の gate

1. `source_manifest.json` を source metadata の唯一の authoring location とする。
2. raw file は repository 外へ取得し、byte size と SHA-256 が一致したものだけを読む。
3. schema-only 検証は `scipy.io.whosmat` を使い、quadrature array を load しない。
4. value loader は stored phase label を radian へ変換するだけで、位相shift、値のrescale、
   offset subtraction、loss/efficiency correctionを行わない。
5. synthetic MAT fixture で checksum、schema、位相、無変換を検査する。

この5条件のいずれかが失敗した場合、後続 fit packet へ進まない。

## 2. source fact routing / scope table

この表は source fact を再記述せず、唯一の authoring location と解釈境界を対応づける。

| ID | 対象 | authoring location | このprotocolでの境界 |
|---|---|---|---|
| K32-D1 | 公開物の同一性 | `source_manifest.json.source` / `.files` | source identityだけを消費し、状態の意味を推論しない。 |
| K32-D2 | MAT schema | `source_manifest.json.expected_mat_schema` | schema-only観察を分布観察として扱わない。 |
| K32-D3 | series provenance | `source_manifest.json.series_record` | manifestに記録されたsource-supported部分と推論部分を混ぜない。 |
| K32-D4 | 位相 | `source_manifest.json.convention_record.phase_mapping` / `.phase_sign_identifiability` | loaderはH1だけを実装する。fitはH1/H2を固定armとして両方実行し、parity仮定をarm省略や規約選択に使わない。 |
| K32-D5 | quadrature単位 | `source_manifest.json.convention_record.quadrature_scale` | loaderはprimary ruleだけを実装し、別解釈は§3の固定armに限定する。 |
| K32-D6 | added loss | `source_manifest.json.convention_record.additional_loss` | source conditionとfit parameterを別fieldで保持する。 |
| K32-N1 | model比較 | 本文 §3–5 | 次packetまでnot run。現packetから性能・物理状態の結論を出さない。 |

## 3. 後続 pump-series packet（まだ実行しない）

- 対象: `series=pump_power` の4条件。
- `01mW` は development condition。fitコードのsmokeとtrain-only convergence確認に使う。
- `03/10/25mW` は validation conditions。01mWでコードとscheduleを固定するまで値を読まない。
- 各位相内で80/20 split。reshuffle seedsは0と1。
- convention armは次の2×2直積を全条件へ適用し、結果を見て選ばない。

  | axis | primary | fixed sensitivity |
  |---|---|---|
  | quadrature scale | stored value | 全sampleを`sqrt(2)`倍 |
  | phase interpretation | H1 | H2: stored phaseは維持し、stored phaseが180度以上のsampleだけ符号反転 |

  4 armすべてを同じsplit、model、scheduleでfitする。
- manifestのparity recordは、H1/H2が一致し得る理論上の説明にだけ使う。両armの一致を
  parity symmetryの証明やH1の選択に使わず、同recordを理由にH2を省略しない。
  逆に、両armの不一致はparity破れの証拠ではない。母集団がparity対称でも有限標本の
  揺らぎでfitとCIはずれ、0境界付近では分類が反転し得るためである。各armのCI値そのものを
  分類と併記し、`phase-convention-dependent` は保守的なrobustness flagとしてだけ使う。
- article phaseからstored phaseへのglobal `-60 deg` shiftも独立armにしない。現在のBB† familyは
  `alpha, xi`のglobal rotationによる再parameterizationに閉じ、fixed-cutoff MLEのFock空間も
  位相回転に閉じる。共通x binsも角度非依存なので、有限最適化による差は位相規約でなく
  init sensitivityとして扱う。
- primary physical modelは exp18 と同一の mixed BB† `R=4,K=4`、fitted `eta`、
  `iters=500`、`lr=0.05`、`eta0=0.8`、init seeds `{0,1,2}`、train NLL選択。
- opponentは fixed MLE `n_max=16`。matched-dof対照として fixed `n_max=10` も報告する。
  cutoffをtest NLLで選択しない。MLE histogram binsは80。
- metricはheld-out per-sample NLL。既 fitted model間のpaired bootstrapは
  `B=2000, seed=123` とする。

各 condition / reshuffle の `BB† R4K4 - MLE16` CIを、上端<0ならdescriptive win、
下端>0ならdescriptive loss、それ以外はunresolvedと機械分類する。これは条件付きCIであり、
model選択や複数条件を含むconfirmatory inferenceではない。primaryからscale軸だけを変えて
分類が変わる場合は `unit-convention-dependent`、phase軸だけを変えて分類が変わる場合は
`phase-convention-dependent` とする。両軸のinteractionも4 arm表から報告し、いずれかが
convention-dependentなら外部妥当性のheadlineを作らない。分類以外の報告量もarm間で
畳み込まず、§5のarm-indexed result surfaceで差を個別に示す。

## 4. 後続 loss-series packet（pump packetから分離）

`series=post_psa_loss_tolerance` は、同一生成状態へ既知state lossを加えた系列として
扱わない。目的はPSA後measurement-chain degradationに対する再構成の頑健性記述に限定する。
manifestの `post_psa_loss_db` と fitted `eta` は別列に置き、同値変換や校正値比較をしない。
全conditionで§3と同じ2×2 convention armを実行し、convention-dependentな場合は
規約を限定しないmeasurement-chain robustnessのheadlineを作らない。

## 5. result surface

後続runnerは測定値と判定入力をJSONへ書き、READMEの結果blockはJSONから生成する。
runnerやREADME proseへ結論文字列を手書きしない。result tableは
`source_file × series × condition × reshuffle_seed × scale_arm × phase_arm × model` の
1行1claimとし、最低限次の列を持つ。

| 列 | 内容 |
|---|---|
| `source_file`, `series` | manifestで一意なsource identityとseries provenance |
| `condition`, `reshuffle_seed` | source conditionとsplit identity |
| `scale_arm`, `phase_arm` | scale規約とH1/H2を別列で明示 |
| `model`, `mode_count` | model identityと、そのarmで報告するmode count |
| `fitted_eta`, `train_nll`, `test_nll` | arm-indexed point estimates |
| `delta_nll_vs_mle16`, `ci_low`, `ci_high` | 勝敗の測定値とCI値そのもの |
| `classification` | CIから機械生成したwin / loss / unresolved |
| `convention_status`, `epistemic_status` | 規約依存性とclaimの限定 |

result-surface status語彙の唯一のauthoring locationを次の表とする。`convention_status`は単一値、
`epistemic_status`は必要なtagを並べるJSON arrayとし、runnerは表外の値を拒否する。

| field | allowed values |
|---|---|
| `convention_status` | `convention-stable`; `unit-convention-dependent`; `phase-convention-dependent`; `unit-and-phase-convention-dependent`; `arm-specific-difference` |
| `epistemic_status` | `descriptive-conditional-ci`; `source-assignment-inferred`; `convention-conditional`; `unresolved` |

mode countを含む全報告量を4 armごとに出力し、H1/H2やscaleの値を単一point estimateへ
集約しない。convention comparison tableも報告量ごとに1行とし、H1/H2の値、数値なら差、
categoricalなら一致/不一致を保持する。分類の不一致は`phase-convention-dependent`、それ以外の
差は`arm-specific-difference`とし、その量に関するheadlineは両armを包含するrangeまたは
両armで共通に成立する記述に限定する。
