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

## Train-only gsplat

固定commitのupstream `examples/simple_trainer.py`をadapter経由で呼ぶ。
20枚すべてを学習へ投入し、画像はCPU RAMへcache、評価は全frame/channelの
pooled MSEからPSNRを算出する。`heldout-sealed/` は列挙もloaderへの引き渡しも
行わない。COLMAPのradial undistortionは使うが、有効ROI cropは行わず
1920x1080 canvasを維持する。

```powershell
.venv\Scripts\python.exe experiments\20_real_video_gpu\train_gsplat.py `
  --seed 0 --steps 4000 --eval-every 250 --run-name seed0_fixed_4000
```

seed 0 / 3000-step pilotは25.976 dB、peak VRAM 0.955 GiBで通過した。ただし
SH昇格間隔ではdegree 2までだったため、固定3-seed recipeは4000 stepとする。
pilotの集計値は `phase3_pilot_result.json`。

## Fisher feasibility spike

held-out に触れない完全合成の tiny scene（2 views、2 splats、8×6 RGB）で、
PUP と共通の per-splat block `[mean(3), log-scale(3)]` を検証する。exact は
PyTorch の全画像 Jacobian から、候補は scalar RGB output ごとの VJP 外積累積
から作る。回転・opacity・色は固定する。

```powershell
.venv\Scripts\python.exe experiments\20_real_video_gpu\phase4_fisher_spike.py
```

chunk 1/7/64 の候補 block は exact block と最大相対誤差 `6.94e-9` で一致した。
log-scale と activated-scale の座標変換では damping metric も変換し、score map
の相対誤差は `4.40e-7`。damping `1e-8` 対 `1e-10` の map 変化は
`7.25e-5` まで収束した。振幅、density-gradient norm、diagonal Fisher、block
Fisher の4 mapと全数値は `phase4_fisher_result.json` に保存する。

この pass が保証するのは fused gsplat 上の scalar-output VJP 実装だけである。
PUP の patch-summed 近似、custom CUDA Fisher kernel、held-out ranking は未検証。
設計参照は [gsplat](https://github.com/nerfstudio-project/gsplat)、
[PUP 3D-GS](https://github.com/j-alex-hanson/gaussian-splatting-pup)、
[FisherRF](https://github.com/JiangWenPL/FisherRF)。

## Randomized matrix-free Fisher

Phase 4b は Issue #48 comments `5011474178` / `5011480536` で実行前に
固定した Rademacher estimator を検証する。train block は 512 output-VJPs、
pixel predictive variance は block 逆共分散方向の256二側中央差分 JVPs。

```powershell
.venv\Scripts\python.exe experiments\20_real_video_gpu\phase4b_randomized_fisher.py
```

3 estimator seeds の 512-probe Fisher 相対 Frobenius 誤差は
`0.0930 / 0.0813 / 0.0498`、256-probe score の exact map との Spearman は
`0.9975 / 0.9986 / 0.9984`、nRMSE は `0.0474 / 0.0256 / 0.0417`。
中央差分 JVP の最大 nL2 は `0.00727`、16→256 probes の median nRMSE 比は
`0.342`。事前 gate を全項目で通過したため、production は estimator seed
`314159`、Fisher 512、score 256 に固定する。結果は
`phase4b_randomized_fisher_result.json`。
