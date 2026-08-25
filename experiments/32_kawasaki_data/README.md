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
