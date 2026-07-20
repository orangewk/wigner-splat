# Issue #89 signed-splat demo — done

## Authority and fixed contract

orangeが2026-07-20にGOし、同日「公開済み・学習済み・美麗・精細度に問題がない
3DGSを探し、追加学習なしで3効果を完成させる」と契約を再確認した。
Codex session `019f6d8a` がデータ探索、GPU描画、視覚QA、PR反映を担当した。

## Final public material

steam studio / 3D SCAN STUDIO irisのCC0サボテンPLYを採用した。

- source: https://note.com/steam_studio/n/ne9736d94f162
- capture: Nikon Z7II、8256×5504、427 photos
- model: Postshot、25k steps、1,935,120 splats、SH degree 3
- PLY: 456,689,798 bytes
- SHA-256: `0d747af95e3e9d55837a1e3aa6a4ed7dc6222866e0ba8cda928e211f7e8888c1`
- GPU training: なし

大容量PLYはcommitしない。CC0派生動画3本は合計約1.4MBのためPRに含める。

## Implementation decisions

- `gpu_renderer.py`: Postshot/INRIA binary PLYの全Gaussian属性を読む。
- `gsplat` CUDA rasterizer: 異方性scale、quaternion、SH degree 3、antialiasingを使用。
- `eraser`: カメラ側3D球内の正splatsを相殺し、取得済み背面を露出。
- `dark-flashlight`: 52個のnegative Gaussianによる減光ビーム。
- `annihilation`: サボテンと遮蔽由来の小片を負コピーとの接触で相殺し、鉢は保持。
- CUDA依存は実行時に遅延importし、PLY loaderのCIテストはCPUだけで実行可能。
- 既存CPU rendererはlegacy fallbackとして残すが、正式成果物には使わない。

## Superseded path

初版の`cakewalk/splat-data/garden.splat`＋固定screen-space footprint CPU rendererは
正式成果物から外した。gardenの個別licenseが不明確だったことに加え、異方性scale、
quaternion、SHを無視する描画が精細度契約を満たさなかったためである。
自作MOVへの切替・再学習案も撤回した。

## Validation

- targeted pytest: `6 passed in 0.21s`（最終再実行）
- full pytest: CPU稼働を継続したまま304秒でtimeout。元processはtimeoutで終了し、二重起動なし
- GPU: NVIDIA GeForce RTX 5070
- videos: 3本とも960×960、12 fps、96 frames、8.000秒、H.264 yuv420p
- visual QA: 各動画1・4・7秒、annihilation最終frame
- committed artifacts:
  - `media/cc0-cactus-eraser.mp4`
  - `media/cc0-cactus-dark-flashlight.mp4`
  - `media/cc0-cactus-annihilation.mp4`

結果・hash・再現条件は`experiments/22_signed_splat_demo/demo_result.json`に記録した。
