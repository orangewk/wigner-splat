# Experiment 32 — Kawasaki homodyne data contract

Issue #180 packet 1。原本の分担と非スコープは `protocol.md` §1–2 を参照する。

## 取得

manifestに記録した直リンクを表示する。

```powershell
python experiments\32_kawasaki_data\kawasaki_data.py urls
```

表示されたURL、またはmanifestの `source.dataset_page` から全fileをrepository外の
directoryへ保存する。期限付きS3 redirect URLは再現不能なので記録・再利用しない。

## schema-only検証

次のコマンドはsize、SHA-256、MAT変数名、shape、classだけを検証し、quadrature arrayを
loadしない。

```powershell
python experiments\32_kawasaki_data\kawasaki_data.py verify --data-dir C:\data\kawasaki-2024
```

後続packetで値のloadが承認された場合だけ、同じコマンドへ `--load-values` を加える。
その場合もloaderは統計量を出力せず、位相shift・値rescale・物理補正を行わない。

## テスト

```powershell
python -m pytest tests\test_kawasaki_data.py tests\test_kawasaki_pump_series.py -q
```

テストはsynthetic MATだけを使用し、公開raw fileへアクセスしない。

## pump-series実行gate

`pump_series_plan.json` が数値scheduleの唯一のauthoring locationで、runnerはplan外の
model・arm・判定語彙を受け付けない。まず01mWだけをtiny budgetで配線確認する。

```powershell
python experiments\32_kawasaki_data\run_pump_series.py smoke `
  --data-dir C:\data\kawasaki-2024 `
  --output C:\temp\kawasaki-pump-smoke.json
```

次にclean worktreeの固定SHAで01mWのtrain-only development gateを実行する。

```powershell
python experiments\32_kawasaki_data\run_pump_series.py development `
  --data-dir C:\data\kawasaki-2024 `
  --checkpoint-dir C:\temp\kawasaki-pump-checkpoints `
  --output experiments\32_kawasaki_data\pump_development.json
```

checkpointは1 seed×1 armごとに書かれ、同じplan・runner・git SHAで再実行した場合だけ
再利用される。

validation conditionは、passing development artifactを含むfixed SHAの独立review recordが
揃うまでrunner自身が拒否する。artifact内のclean execution SHAはreviewed SHAの祖先であり、
plan・runner・manifestのgit blobが両SHAで同一、artifact自体がreviewed SHAにcommitされた
blobとbyte一致することも検証する。review recordにはreviewed SHA、development execution
SHA、4 artifact/input SHA-256、tracked artifact path、PASS review URLが必要である。tracked
textのhashとblob比較はWindows checkoutのCRLF差を意味差にしないようLF正規化後に行う。
PASS後の全条件実行は、fit単位のcheckpoint directoryを必須にする。

```powershell
python experiments\32_kawasaki_data\run_pump_series.py execute `
  --data-dir C:\data\kawasaki-2024 `
  --development-artifact experiments\32_kawasaki_data\pump_development.json `
  --review-record C:\temp\kawasaki-pump-review.json `
  --checkpoint-dir C:\temp\kawasaki-pump-execute-checkpoints `
  --output C:\temp\kawasaki-pump-result.json
```

BB-daggerはsource×split×arm×init seed、MLEはsource×split×arm×modelごとに保存する。
再利用時はplan・runner・manifest・reviewed SHA・development artifact・review recordと
source/split/arm/model identityを照合する。さらにBB stateからtrain NLLを再計算し、MLEの
密度行列はshape・finite・Hermitian・trace・PSDに加え、同じtrain splitから再計算したNLLを
検証する。したがって中断後も、検証済みのfitだけを再利用して続行できる。

## pump-series結果

[`pump_results.json`](pump_results.json) が数値結果の唯一のauthoring locationである。
以下は `pump_result_summary.py` が同artifactから生成し、専用policy testがartifactとの
一致を検査する。表は4 convention armを畳み込まず、splitごとの分類をそのまま示す。

<!-- generated-block: do not edit (written by pump_result_summary.py from pump_results.json) -->
- Artifact identity: normalized SHA-256 `4279a3dda0c08caf3b3466bb7fa2843468534a6c44680362278cb28dc25f83fe`; execution code SHA `1571886893cb5137cee83147c500dc389d8edd3b`.
- Arm-indexed primary classifications: win 7; loss 0; unresolved 25 (total 32).
- Convention-stable condition/seed groups: 3 of 8; classified win among them: 0 of 3.

| pump condition | reshuffle seed | stored/H1 | stored/H2 | sqrt2/H1 | sqrt2/H2 | convention status |
| --- | ---: | --- | --- | --- | --- | --- |
| 1 mW (source assignment inferred) | 0 | unresolved | unresolved | win | win | unit-convention-dependent |
| 1 mW (source assignment inferred) | 1 | unresolved | unresolved | unresolved | win | unit-and-phase-convention-dependent |
| 3 mW | 0 | win | unresolved | unresolved | unresolved | unit-and-phase-convention-dependent |
| 3 mW | 1 | unresolved | unresolved | unresolved | unresolved | convention-stable |
| 10 mW | 0 | win | unresolved | unresolved | unresolved | unit-and-phase-convention-dependent |
| 10 mW | 1 | win | win | unresolved | unresolved | unit-convention-dependent |
| 25 mW | 0 | unresolved | unresolved | unresolved | unresolved | convention-stable |
| 25 mW | 1 | unresolved | unresolved | unresolved | unresolved | convention-stable |

- Conditions classified win in all four convention arms and both reshuffle seeds: **none**.
<!-- generated-block: end -->

`unresolved` や `loss` 非検出は、同等性・非劣性・model同一性を意味しない。各行は
事前固定したfit、split、arm、paired-bootstrap CIに条件づく記述結果であり、詳しい
解釈境界とstatus語彙は [`protocol.md`](protocol.md) §3・§5を参照する。

生成blockの再現・検査だけならraw MATを読まない。

```powershell
python experiments\32_kawasaki_data\pump_result_summary.py
```

artifactを正当に更新したpacketでは、固定SHA review後に次を実行してblockを再生成する。

```powershell
python experiments\32_kawasaki_data\pump_result_summary.py --write
```
