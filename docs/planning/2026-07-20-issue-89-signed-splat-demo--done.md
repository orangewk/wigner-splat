# Issue #89 signed-splat demo — done

## Authority and scope

orange が 2026-07-20 に GO。Codex session `019f6d8a` が担当した。
確認的検証や GPU 再学習ではなく、既存 3D Gaussian scene に負の寄与を後処理で
加える表現デモを対象とした。追加候補（干渉縞・存在つまみ）は実装していない。

## Implementation decisions

- 32-byte `.splat` と gsplat test `.npz` を読み込む dependency-light CPU renderer。
- `eraser`: 3D球内で source splat と同位置の負コピーを相殺する。inpaintingしない。
- `dark-flashlight`: 44個の低振幅 negative Gaussian で sweep する減光ビームを作る。
- `annihilation`: 中央領域の負コピーを右から接近させ、接触時に正側を相殺する。
- NumPy / Pillow / ffmpeg のみ。raw RGB を ffmpeg stdin へ流し、中間frameを作らない。
- 出力済みファイルは既定で上書き拒否する。

## Prior-work boundary

NegGS は negative Gaussian 自体と再構成用途の先行。GaussianEditor は Gaussian
RoI とtext instructionによる局所編集、Point'n Moveは object removal/manipulation
と露出領域inpaintingの先行。本作の差分は、学習改善ではなく時間変化する符号付き
表現操作であり、既存法への優越は主張しない。

## Local material and license boundary

ローカル検証に `cakewalk/splat-data/garden.splat` を使用した。

- bytes: `186,713,088`
- SHA-256: `f85efae49d16cf17756290a4f6d9dea71c324639b7f53119920630389f2b59aa`
- camera: 同作者 WebGL viewer `main.js` の camera 0 を転記

upstream model card は「様々な出典・様々なライセンス」とだけ記し、garden file と
元素材licenseの対応を示さない。Issue本文の「動画公開は出典明記でOK」は一次資料から
確認できなかったため、scene と動画はcommit・公開しない。公開版は自作scan等、権利が
明確なsceneへの差し替えが必要。

## Local representative videos

共通 recipe: 2,000,000 splats / 1296×840 / 12 fps / 96 frames / 8.000 s /
H.264 yuv420p。ファイル本体は `out/` にあり、gitignore対象。

- eraser: 1,794,195 bytes, wall 81.732 s,
  SHA-256 `0a55fb0f66934525b3197fa789c0b03be2d221ed0adfcdff5b496db13d1971bc`
- dark-flashlight v2: 1,490,389 bytes, wall 4.082 s,
  SHA-256 `bfec3b36eb150d627aec742d4fe6301b42beca1c5d2ec869a130204d231978c1`
- annihilation: 13,583,664 bytes, wall 113.686 s,
  SHA-256 `2084ff259b75dfc9b3d241134d7581a6505a2c6fceaf357d94cdf838aa8aeb18`

1 / 4 / 7秒frameで視覚QA。初版の闇ビームはfoliage上で弱すぎたため、negative
particle weightを `-0.055` から `-0.12` へ強めてv2を採用した。

## Validation and operational record

- targeted pytest: `4 passed in 0.15s`
- ffprobe: 全3本 1296×840 / 12 fps / 96 frames / 8.000 s
- AST parse / direct `.splat` decode / exact signed cancellation check: pass
- `garden.splat` hashはHugging Face Xet pointer記載値と一致

sandbox内pytestはテスト本体が `3 passed` に到達後、終了処理で2回hangした。
二重起動せず、各元process treeだけを診断・停止した。権限付きかつthird-party plugin
autoload無効で再実行すると正常終了し、fixture 1件のnear-plane前提を修正後4件pass。

## Remaining action

公開可能な自作sceneを受領後、同じCLIで3本を再生成して動画を公開成果物へ昇格する。
現時点の完了範囲は、再現可能なコード、ローカル表現検証、権利境界の記録まで。
