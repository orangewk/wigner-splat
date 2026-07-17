# Experiment 20 — real-video GPU round 3

Issue #48 の静的実写 round 3。フル解像度 RGB、train-only COLMAP、
`gsplat` によって、25 dB 級の作業点へ移れるかを検証する。

## Data boundary

- 元動画の frame index は experiment 16 の `src_indices` を継承する。
- 24枚中、位置 4/10/16/22 は `data/heldout-sealed/` へ隔離する。
- COLMAP と学習は `data/train/` の20枚だけを入力にする。
- held-out は train PSNR hard stop 通過まで loader / COLMAP に渡さない。
- フル解像度PNGとCOLMAP生成物はローカル成果物で、Gitには含めない。
- `data/manifest.json` が動画・フレーム hash と split の SoT である。
- 提供原本は実測20,130,116 bytes / H.264。旧READMEの「12 MB / HEVC」と metadataは異なるが、24個の既存縮小フレームとの内容照合で同一素材と確認した。

## Prepare

```powershell
.venv\Scripts\python.exe experiments\20_real_video_gpu\prepare_data.py `
  --video C:\path\to\IMG_3899.MOV
```


COLMAPの再現実行:

```powershell
.venv\Scripts\python.exe experiments\20_real_video_gpu\run_colmap.py `
  --colmap .venv\tools\colmap-4.0.4\bin\colmap.exe
```

COLMAP 4.1.0公式CUDA版はCUDA 13.2 buildのため、driver 576.88ではGPU初期化できない。CUDA 12.9 + sm_120の公式4.0.4 assetを固定して使う。