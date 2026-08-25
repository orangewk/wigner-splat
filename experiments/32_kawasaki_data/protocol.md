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

## 3. pump-series packet

- 数値schedule、condition分担、model、split、arm、判定語彙の唯一のmachine-readable
  authoring locationを `pump_series_plan.json` とする。本節はその意図と解釈境界だけを記す。
- 同planのdevelopment conditionはfitコードのsmokeとtrain-only convergence確認だけに使う。
- validation conditionsはdevelopment gate通過後、runner・plan・development artifactを含む
  fixed SHAの独立reviewがPASSするまで値を読まない。development artifactの生成SHAは
  reviewed SHAの祖先とし、plan・runner・manifestのblob同一性、reviewed SHAに含まれる
  artifact blob、外部review recordのSHA/pathをrunnerが照合する。
- 同planの2×2 convention armを全条件へ適用し、結果を見て選ばない。

  | axis | primary | fixed sensitivity |
  |---|---|---|
  | quadrature scale | `arms.scale[0]` | `arms.scale[1]` |
  | phase interpretation | `arms.phase[0]` | `arms.phase[1]` |

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
- physical model、fixed MLE opponent、matched-dof対照、histogram、optimizer、init、metric、
  bootstrapの値はplanの `models` と `primary_comparison` をそのまま消費する。runner側の
  fallback値やtest NLLによるcutoff選択を認めない。

各 condition / reshuffle のplan指定primary comparisonを同planのruleで機械分類する。
これは条件付きCIであり、
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
| `convention_status`, `epistemic_status` | classificationの規約依存性とclaimの限定 |

result-surface statusの語彙と付与条件の唯一のauthoring locationを次の表とする。
classificationを `C(scale_arm, phase_arm)` と書き、
`scale_dep = (C(stored,H1) != C(sqrt2,H1)) or (C(stored,H2) != C(sqrt2,H2))`、
`phase_dep = (C(stored,H1) != C(stored,H2)) or (C(sqrt2,H1) != C(sqrt2,H2))`
として機械計算する。`convention_status`はclassificationだけに付く単一値、
`comparison_status`はclassification以外の報告量ごとにcomparison tableへ付く単一値、
`epistemic_status`は必要なtagを並べるJSON arrayとする。runnerは表外の値を拒否する。

| field / tag | 付与条件 |
|---|---|
| `convention_status=convention-stable` | `not scale_dep and not phase_dep`。4 armのclassificationが同一。 |
| `convention_status=unit-convention-dependent` | `scale_dep and not phase_dep`。scale軸だけでclassificationが変わる。 |
| `convention_status=phase-convention-dependent` | `not scale_dep and phase_dep`。phase軸だけでclassificationが変わる。 |
| `convention_status=unit-and-phase-convention-dependent` | `scale_dep and phase_dep`。両単軸の変化と、単軸primary contrastは不変でも対角armだけが変わるinteraction-only caseを含む。 |
| `comparison_status=same-across-arms` | classification以外の当該報告量が4 armで同一。 |
| `comparison_status=arm-specific-difference` | classification以外の当該報告量が1 arm以上で異なる。 |
| `epistemic_status+=descriptive-conditional-ci` | fixed fitted modelsのdelta / CI / classificationを含む全result rowに付ける。confirmatory inferenceではないことを示す。 |
| `epistemic_status+=source-assignment-inferred` | `files[*].series_assignment == inferred` のsource_fileにだけ付ける。 |
| `epistemic_status+=convention-conditional` | 単一のscale / phase armに条件づけられた全result rowに付ける。 |
| `epistemic_status+=unresolved` | 当該rowの`classification == unresolved`の場合だけ付ける。他のepistemic tagと併存する。 |

mode countを含む全報告量を4 armごとに出力し、H1/H2やscaleの値を単一point estimateへ
集約しない。convention comparison tableも報告量ごとに1行とし、H1/H2の値、数値なら差、
categoricalなら一致/不一致を保持する。分類の不一致は`phase-convention-dependent`、それ以外の
差は`comparison_status=arm-specific-difference`とし、その量に関するheadlineは両armを包含するrangeまたは
両armで共通に成立する記述に限定する。
