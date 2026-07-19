# Issue #48 Round 4 GPU実行記録

日付: 2026-07-19
状態: done
決定者: orange（Issue #48 comment 5013626313でhard lock）
実行担当: Codex session 019f6d8a
branch: feat/issue-48-round4-gpu

## 実行境界

- Round 3の3 checkpointとproduction Fisherを凍結再利用した。
- 再fit、新ノブ、BA、triangulation、splat更新は行っていない。
- fresh dataは元動画末尾のindex 216/244/272/300。
- 既開封のRound 3 held-out 4枚は判定に使っていない。

## 前提条件

- 元動画SHA-256は固定値4483e898...f7b9eと一致。
- lossless RGB PNG 4枚をheldout2-sealedへ隔離。
- COLMAP登録は4/4成功。
- train pose、intrinsics、point XYZは不変。

## 判定

- Gate B: pass。block-Fisher rho =
  0.36905 / 0.33663 / 0.37550、全seedで0.3以上。
- Gate B2: fail。ensemble sigma rho =
  0.57534 / 0.56690 / 0.54286で全seed blockを上回った。
- block Fisherはamplitude、J-norm、diagonal Fisherには全seedでstrictに勝った。
- 宣言済み反証文: この作業点でH^-1証明書は3-seed反復ensembleに勝てない。

判定外damping sweepは1e-4 -> 1e-6 -> 1e-8と弱めるほど全seedで相関が
上昇した。primary 1e-6は変更していない。

## 実測

- Gate elapsed: 113.2 / 84.3 / 93.8秒（seed 0/1/2）。
- peak VRAM: 0.959 / 0.965 / 0.951 GiB。
- shared ensemble render: 2.85秒、0.474 GiB。

## 成果物

- experiments/20_real_video_gpu/phase6_round4_result.json
- experiments/20_real_video_gpu/round4_certificate.png
- experiments/20_real_video_gpu/data/round4_manifest.json
- restartable local states: out/round4_*（Git非追跡）

## 運用所見

pytest対象テストはpass表示まで到達したが、Windowsでプロセス終了が2回
ハングした。二重起動せず対象PIDだけ停止し、最終的な構文・hard-lock定数は
固定CUDA環境で直接検証した。GPU runner自体は3 seedとも正常終了した。
