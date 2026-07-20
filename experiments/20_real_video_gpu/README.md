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

Production train Fisher は seed ごとに実行し、各 train view 完了後に
`out/production_fisher_seed*/fisher_state.pt` を更新する。再実行は次の未完 view
から再開する。smoke 実測は55.2万 splats・1920×1080・1 view×2 probesで
1.34秒、peak VRAM 0.683 GiB。held-out path は構築・列挙しない。

```powershell
.venv\Scripts\python.exe experiments\20_real_video_gpu\build_production_fisher.py `
  --fit-seed 0
```

## Held-out Gate B/B2

3 seed の production Fisher 完了後にだけ held-out 4枚を開封した。GPU SIFT と
GPU exhaustive matching の後、`image_registrator` で固定train modelへposeだけを
登録した。BA・triangulation・splat更新は行わず、train 20 pose、camera intrinsics、
4,567 pointのXYZが不変であることを検証した。

```powershell
.venv\Scripts\python.exe experiments\20_real_video_gpu\register_heldout_poses.py `
  --colmap .venv\tools\colmap-4.0.4\bin\colmap.exe `
  --output experiments\20_real_video_gpu\out\heldout_registration_v2

.venv\Scripts\python.exe experiments\20_real_video_gpu\run_gate_b.py --fit-seed 0
.venv\Scripts\python.exe experiments\20_real_video_gpu\summarize_gate_b.py
```

256 probes/view の block-Fisher Spearman は `0.3343 / 0.3324 / 0.3351` で、
固定閾値0.3を全seedで超えたため Gate B は通過した。一方、`||J||` controlは
`0.4025 / 0.3984 / 0.4009`、diagonal-Fisherは
`0.3783 / 0.3660 / 0.3778` と全seedでblockを上回り、Gate B2は不通過。
高品質fitではpredictive sensitivityと残差の相関が回復するが、block Fisher固有の
優位性は示されない。結果は `phase5_gate_b_result.json`、図は
`heldout_certificate.png`。
## Round 4 fresh-view replication

Issue #48 comment 5013626313 の hard lock に従い、未使用の動画末尾 frame
index 216/244/272/300 を heldout2-sealed へ lossless 抽出した。4/4 pose が
凍結 train COLMAP model のコピーへ登録され、train pose、camera intrinsics、
point XYZ は不変だった。再fit、BA、triangulation、splat更新は行っていない。

```powershell
.venv\Scripts\python.exe experiments\20_real_video_gpu\prepare_round4_data.py `
  --video C:\path\to\IMG_3899.MOV
.venv\Scripts\python.exe experiments\20_real_video_gpu\register_round4_poses.py `
  --colmap .venv\tools\colmap-4.0.4\bin\colmap.exe
.venv\Scripts\python.exe experiments\20_real_video_gpu\run_round4_gate.py `
  --fit-seed 0 --build-shared-ensemble
.venv\Scripts\python.exe experiments\20_real_video_gpu\run_round4_gate.py --fit-seed 1
.venv\Scripts\python.exe experiments\20_real_video_gpu\run_round4_gate.py --fit-seed 2
.venv\Scripts\python.exe experiments\20_real_video_gpu\summarize_round4.py
```

主系 block-Fisher は fresh data でも 0.3690 / 0.3366 / 0.3755 で Gate B を
全seed通過し、今回は amplitude、H=I ||J||、diagonal-Fisher の全てを
全seedで上回った。しかし3 fit-seed共有の不偏 ensemble sigma は
0.5753 / 0.5669 / 0.5429 でblockを全seed上回り、Gate B2は不通過。
hard lockどおり「H^-1証明書はこの作業点で力ずくの反復に勝てない」と読む。
damping感度は判定外で、1e-4 -> 1e-6 -> 1e-8 と弱めるほど全seedで相関が
上がったが、primaryは1e-6から変更しない。結果は
phase6_round4_result.json、図はround4_certificate.png。

## Round 5 independent public scenes

Issue #48 comment 5014598454 で hard lock した公開データ検証。公式 Tanks and
Temples の Truck/Train image set から、全フレーム数を N として
position * floor(N/24) の24枚を native 1920x1080で固定した。positions
4/10/16/22 は heldout-sealed、残り20枚だけをCOLMAPへ渡した。

共有ensemble artifactには heldout names、fit seeds、ddof、各map SHA-256と
内部metadataの一致を要求するreuse guardを事前実装した。データ取得・hash・
attributionは data/round5/README.md と各scene manifestを参照。

動画向けsequential matchingはTruck 11/20、Train 3/20登録だった。fit前に
Issue comment 5014845453へ運用修正を記録し、失敗出力を保持したままCUDA
exhaustive matchingを別出力で試したが、Truck 15/20、Train 2/20だった。
20/20を完了条件としたため両scene DNF。

gsplat、train PSNR hard stop、Fisher、sealed pose登録、Gate B/B2、ensemble
分解は未実行である。このDNFはGate Bの再現も棄却も意味しない。宣言24枚の
global strideでは必要な完全SfMへ到達しなかった、という前提条件の結果である。
集計は phase7_round5_result.json、図は round5_dnf_certificate.png。

## Round 6 contiguous public-scene blocks

Issue #48 comment 5017827938 の hard lock に従い、Round 5 と同じ Truck / Train
アーカイブから中央固定の連続24枚を使用した。Truckはsource 113–136、Trainは
138–161、sealed positionsは4/10/16/22で不変。CUDA exhaustive COLMAPは両scene
とも最初の試行でtrain 20/20を登録し、Round 5のSfM前提DNFを解消した。

次のpooled train PSNR前提は、固定4000-step recipeのseed 0でTruck 24.305 dB、
Train 22.180 dBとなり、25 dB床を両sceneとも未達。1 seedの未達でDNFが確定する
ためseeds 1/2、Fisher、held-out登録、Gate B/B2、ensemble分解は実行していない。
held-outはCOLMAP・fit・評価から未アクセス。集計は
phase8_round6_result.json、図はround6_dnf_certificate.png。
