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
python -m pytest tests\test_kawasaki_data.py -q
```

テストはsynthetic MATだけを使用し、公開raw fileへアクセスしない。
