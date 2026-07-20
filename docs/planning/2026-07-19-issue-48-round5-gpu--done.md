# Issue #48 Round 5 GPU execution record

Date: 2026-07-19
Status: done — did not finish at the COLMAP prerequisite
Decision authority: orange approved Issue #48 comment 5014598454
Execution owner: Codex session 019f6d8a
Branch: feat/issue-48-round5-gpu

## Locked scope

Round 5 was intended to replicate Gate B on independent public scenes and
decompose the Round 4 ensemble advantage. The official Tanks and Temples Truck
and Train image sets were pinned, with 24 native-resolution frames selected by
source index = position * floor(total source frames / 24). Positions
4/10/16/22 were sealed. Only the other 20 were supplied to COLMAP.

The shared-ensemble reuse guard was implemented before scene execution. It
checks heldout names, fit seeds, ddof, every map SHA-256, and the corresponding
map metadata before reuse.

## Data

Truck archive: 380,210,369 bytes, SHA-256
9ae9ebe8...872439cc2, 251 frames, stride 10.

Train archive: 201,581,296 bytes, SHA-256
542bb34a...d8894367, 301 frames, stride 12.

Both official image sets contain native 1920x1080 JPEGs. Download and frame
hashes are recorded in the committed manifests. The official terms page's
Copyright section states CC BY 4.0, while its License Grant section separately
limits use to non-commercial scientific research and prohibits third-party
redistribution without prior written permission. Both statements are recorded
in the Round 5 data README and manifests; this run is research use.

## COLMAP outcome

The first attempt inherited the video-oriented sequential matcher. CUDA SIFT
and matching completed, but Truck registered 11/20 and Train 3/20 images.

Before any fit or held-out computation, Issue #48 comment 5014845453 recorded
an operational correction to exhaustive matching for globally spaced image-set
frames. Failed outputs were preserved. With CUDA exhaustive matching, Truck
registered 15/20 and Train 2/20. The runner requires 20/20, so both scenes are
DNF.

Observed wall times were 17.7/19.2 seconds for sequential Truck/Train and
10.9/6.5 seconds for exhaustive Truck/Train. The jobs were too short for a
synchronized peak-VRAM sample; CUDA use is explicit in COLMAP logs. No unrelated
process was stopped.

## Scientific verdict

No gsplat fit was started. The pooled-train-PSNR hard stop, production Fisher,
sealed pose registration, Gate B/B2, and ensemble decomposition were not
evaluated. Sealed images were not read by the training or evaluation pipeline.

This DNF neither replicates nor rejects Gate B. It establishes that the locked
24-frame global stride is too sparse for the required complete SfM prerequisite
on these two official image sets under the declared pipeline. Further COLMAP
parameter rescue would be post-hoc protocol exploration and was not attempted.

## Outputs

- experiments/20_real_video_gpu/phase7_round5_result.json
- experiments/20_real_video_gpu/round5_dnf_certificate.png
- experiments/20_real_video_gpu/data/round5/{truck,train}/manifest.json
- experiments/20_real_video_gpu/data/round5/README.md
- local preserved attempts: experiments/20_real_video_gpu/out/round5/
