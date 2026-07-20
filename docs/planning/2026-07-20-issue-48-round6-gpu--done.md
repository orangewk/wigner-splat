# Issue #48 Round 6 GPU execution record

Date: 2026-07-20
Status: done — did not finish at the pooled train PSNR prerequisite
Decision authority: orange approved Issue #48 comment 5017827938
Execution owner: Codex session 019f6d8a
Branch: feat/issue-48-round6-gpu

## Locked change from Round 5

Round 6 changed only the public-scene frame selection. Truck used the fixed
contiguous source block 113–136 and Train used 138–161. Positions 4/10/16/22
were sealed; only the remaining 20 images entered COLMAP and training. The
archives, estimator, fit recipe, seeds, damping, gates, and decomposition rules
remained locked to the Round 5 declaration.

## COLMAP outcome

The declared CUDA exhaustive recipe registered all 20/20 train images on its
first attempt for both scenes. Truck produced 10,537 points with mean
reprojection error 0.648 px; Train produced 8,934 points at 0.719 px. There was
no matcher or mapper rescue and no window movement. This passes the prerequisite
that stopped Round 5 and supports the diagnosis that the global-stride data
premise—not GPU availability—caused that DNF.

## Fit hard stop

The fixed 4000-step gsplat recipe was then run at fit seed 0 for each scene.

| Scene | Final pooled train PSNR | Required | Peak VRAM | Wall time |
|---|---:|---:|---:|---:|
| Truck | 24.305 dB | 25.000 dB | 1.282 GiB | 177.3 s |
| Train | 22.180 dB | 25.000 dB | 1.450 GiB | 180.5 s |

Both scenes are DNF. One failed fit seed is sufficient under the hard lock, so
seeds 1/2 were not run. Fisher, held-out pose registration, Gate B/B2, and the
ensemble decomposition were not started. Held-out images were not accessed by
COLMAP, training, or evaluation.

Truck reached a descriptive 24.969 dB at step 2999 before the fixed recipe's
later densification/pruning stages, but the preregistered decision point is the
final step 3999. Selecting the earlier checkpoint would be a post-hoc recipe
change and was not done.

## Scientific verdict

Round 6 repairs the Round 5 SfM failure but does not reach the declared public-
scene fit operating point. It therefore neither replicates nor rejects Gate B.
Any future attempt to alter the fit recipe, threshold, frame window, or
checkpoint selection requires a new declaration.

## Outputs

- `experiments/20_real_video_gpu/phase8_round6_result.json`
- `experiments/20_real_video_gpu/round6_dnf_certificate.png`
- `experiments/20_real_video_gpu/data/round6/{truck,train}/manifest.json`
- local ignored COLMAP and seed-0 fit outputs under
  `experiments/20_real_video_gpu/out/round6/`
