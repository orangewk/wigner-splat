# Issue #48 Round 3 GPU 移行・再検証計画

日付: 2026-07-17
状態: in progress（orange 承認 2026-07-17、Phase 0–2 完了 2026-07-18）
担当: Codex session `019f6d8a`
branch: `feat/issue-48-round3-gpu`
## 実行状況

- Phase 0: PR #59 merge、生動画取得・同一性確認まで完了。
- Phase 1: RTX 5070 上で gsplat forward/backward/optimizer smoke 合格。
- Phase 2: lossless RGB 24枚を train 20 / held-out-sealed 4へ分離し、train-only COLMAP が 20/20 images、4,567 points、0.695 px で成立。
- 公開記録上の不履行: 本計画は実走前に orange 承認済みだったが、Issue #48 への同文投稿を Phase 2 前に失念した。Gate 学習前の 2026-07-18 に遅延公開として訂正し、事前投稿とは扱わない。
- 訂正記録: https://github.com/orangewk/wigner-splat/issues/48#issuecomment-5008571914

## 目的と完了条件

CPU 自作レンダラで反証された Phase 1 の後を引き継ぎ、RTX 5070 上の本物の静的 3DGS 作業点で、delta-method 型証明書が held-out 残差を順位づけできるかを再検証する。

Round 3(a) の完了条件は、結果の成否ではなく次を満たして判定を記録すること:

1. フル解像度 RGB、COLMAP pose、gsplat で train-only fit を3 seeds実行する。
2. 全 seed の pooled train PSNR が 25 dB 以上の場合だけ held-out を開封する hard stop を保つ。
3. Gate B（Spearman ρ >= 0.3、全 seed）と Gate B2（既存3対照への全 seed 一貫上積み）を事前宣言どおり判定する。
4. DNF・反証・支持のいずれでも、コード、設定、version、ログ、issue #48、`docs/research-log.md` を一致させる。

Round 3(b) の残差ベース bias 項は、(a) の判定後に別計画として扱う。今回の実装へ混ぜない。

## 現在地と境界

- PR #59 は open。Phase 1 資産と handoff は同 PR branch 上にあり、Round 3 実装は PR #59 の main へのマージ後に開始する。
- PR #59 のレビュー対応は元セッションの担当。こちらから変更しない。
- 次の実験番号は、open PR #61 の `19_thermal_gate` を考慮して `experiments/20_real_video_gpu/` とする。
- 生動画 `IMG_3899.mov` は手元の標準フォルダに見つからず、orange からの再提供が必要。原本は commit しない。
- 量子コア線、issue #47/#43/#45、動的 4DGS Phase 2 は対象外。

## 採用方針

### 学習スタック

`gsplat` を直接使い、公式 `examples/simple_trainer.py` の COLMAP trainer を固定 commit で利用・薄く適応する。Nerfstudio 全体は採用しない。

理由:

- gsplat は公式に COLMAP capture trainer、PyTorch bindings、packed rasterization、sparse gradient を提供する。
- Nerfstudio は Windows を fragile と明記し、Round 3 に不要な tiny-cuda-nn/viewer 等の依存が増える。
- 原版 Graphdeco 3DGS は基準実装として重要だが、公式記載で paper-quality は 24 GB VRAM が目安。12 GB と証明書研究には gsplat の方が制御しやすい。

依存は floating `main` にせず、環境 smoke が通った gsplat commit SHA、PyTorch、CUDA、COLMAP を manifest に固定する。

### 初期環境候補

- Windows native / Python 3.10 の隔離 venv
- PyTorch 2.11.0 + cu128
- CUDA Toolkit 12.8 系 + Visual Studio 2022 C++ Build Tools
- gsplat source build（公開 wheel index は PyTorch 2.4 / CUDA 12.4 までで、sm_120 用には使えない）
- COLMAP 4.1.0 の公式 Windows CUDA build

現在の driver 576.88 は CUDA 12.9 runtime を認識するが、PyTorch 2.12 の CUDA 13 wheel が要求する Windows driver 580.88 に届かない。そのため、driver 更新を先行させず cu128 を第一候補にする。

## 実装前に固定するプロトコル

issue #48 に以下を投稿してから実データを走らせる。

1. `t in [1.0, 7.0)`、4 fps、24 frames、1920x1080 RGB。
2. held-out の相対位置は 4/10/16/22 のまま。
3. COLMAP の初期 reconstruction は train 20 frames だけで作る。
4. held-out pose は hard stop 通過後に、train reconstruction を固定した別コピー上で登録し、学習済み splat は更新しない。
5. train PSNR は従来どおり全 train frame/channel の pooled MSE から算出する。色補正後 metric は主要判定に使わない。
6. Gate B は RGB residual を pixel 単位の L2 norm に集約する。証明書と各対照も pixel scalar に揃える。
7. appearance embedding、held-out fine-tuning、人物 mask は使わない。SH は標準 view-dependent appearance として許可する。
8. OOM 時の解像度低下は行わない。packed mode、画像の CPU 保持、densification 上限を train-only で試し、12 GB の壁を実測したら cloud 移行を orange が判断する。

held-out を COLMAP に最初から渡すと画像特徴が train reconstruction に混入し、既存の「hard stop 後ろで初開封」という契約を破るため、この分離を新たに明文化する。

## フェーズ別手順

### Phase 0: 前提の確定

1. PR #59 の merge と main 取り込みを確認する。
2. orange から `IMG_3899.mov` のローカルパス提供を受ける。
3. 原本の SHA-256、ffprobe metadata、抽出コマンドを manifest に記録する。
4. 上記プロトコルを issue #48 へ事前宣言する。

停止条件: PR #59 未マージ、生動画なし、またはプロトコル未承認。

### Phase 1: GPU 環境 smoke

1. 隔離 venv と build toolchain を用意する。
2. `torch.cuda.is_available()`、device name、compute capability `(12, 0)` を記録する。
3. gsplat の小シーンで forward、backward、1 optimizer step、render 保存を検収する。
4. COLMAP の version と GPU feature extraction を検収する。
5. package/driver/compiler/version manifest を保存する。

停止条件: sm_120 build 不成立、勾配不一致、または最小 smoke の CUDA error。

### Phase 2: train-only data と COLMAP

1. ffmpeg で24枚を lossless RGB 抽出し、train/held-out manifest を生成する。
2. held-out 4枚は別ディレクトリへ隔離し、通常の train loader から到達不能にする。
3. train 20枚だけで COLMAP reconstruction を作る。
4. registered image 数、reprojection error、camera trajectory、sparse point 数を記録する。

停止条件: train 20枚だけで安定した reconstruction が成立しない。追加フレーム使用や matcher 変更は、held-out を触る前に再宣言する。

### Phase 3: gsplat train adapter

1. upstream trainer の設定・checkpoint・metric を再現可能な wrapper に固定する。
2. seed 0 の train-only pilot で VRAM peak と PSNR trajectory を観察する。
3. train 情報だけでレシピを固定し、seeds 0/1/2 を checkpoint 対応で実行する。
4. 全 seed の primary fit が 25 dB を超えなければ DNF を記録して終了する。

主要設定は DefaultStrategy、SH degree 3、appearance optimization off、full resolution。12 GB 対策は `packed=True` と画像 CPU 保持から始める。

### Phase 4: 証明書 feasibility spike

大規模実装前に、少数 splat・低解像度の scene で以下を照合する。

1. PyTorch の exact Jacobian から作る per-splat Gauss-Newton block を基準値にする。
2. 本番候補の block Fisher 実装を基準値と比較する。
3. `J_rho^T (H_i + eps I)^-1 J_rho` の pixel map と、振幅・`||J||`・diagonal-H 対照を比較する。
4. damping、block parameterization、chunking に対する不変性/収束性をテストする。

本番候補は、PUP 3D-GS の per-Gaussian block Fisher（mean + scale）と FisherRF の diagonal Fisher を参照する。ただし PUP の CUDA kernel を無批判に移植せず、gsplat 上で exact reference と一致する最小実装を先に作る。

停止条件: fused gsplat 上で検証可能な block Fisher/pushforward が得られない。ランダム推定や custom CUDA へ切り替える場合は、それ自体を科学的変数として issue #48 で再宣言する。

### Phase 5: hard stop と Gate B/B2

1. Phase 3 の checkpoint を読み、train PSNR だけを先に集計する。
2. hard stop 通過後にだけ held-out ディレクトリを開く。
3. train reconstruction のコピーに held-out pose を登録する。
4. splat を固定して residual、証明書、3対照を計算する。
5. 3 seeds の Gate B/B2 を判定し、図と machine-readable result を保存する。
6. hard-stop 回帰テストで DNF 経路が held-out loader/registrator を呼ばないことを保証する。

### Phase 6: 記録と判断

1. 実行ログ、version manifest、設定、図、checkpoint 取扱いを整理する。
2. issue #48 と `docs/research-log.md` に同じ数値・同じ claim scope を記録する。
3. 結果にかかわらず Round 3(a) を閉じる。
4. 残差ベース PPU と Bayesian 3DGS を比較対象にした Round 3(b) 計画を別途提案する。

## テストと検収

- CPU tiny-scene unit tests: PSNR、split manifest、hard stop、seed/config serialization。
- GPU tests: gsplat forward/backward、checkpoint round-trip、exact-vs-block Fisher small-scene comparison。
- protocol test: DNF では held-out path access を罠で検知し、ゼロ回であること。
- data test: 24 frame の時刻/index/hash、train 20 + held-out 4、重複なし。
- scientific output test: issue 記載値、JSON、ログ、図の再集計一致。

## リスクと担当判断

- HIGH — block Fisher の実装可能性。Phase 4 を独立 stop にして先に潰す。担当: Codex が提案、orange が近似変更を承認。
- HIGH — 25 dB が局所動体・露出変化を含む静的モデルで届かない可能性。届かなければ DNF が正しい結果。閾値は動かさない。
- HIGH — 12 GB OOM。解像度を落とさず、実測後に orange が cloud 移行を決める。
- MEDIUM — Windows source build。cu128 + VS2022 を固定し、Nerfstudio 全体を避けて依存面を減らす。
- MEDIUM — train-only COLMAP が20枚で成立しない可能性。held-out 開封前の再宣言でのみ取得条件を変更する。
- MEDIUM — GPU 非決定性。seed、commit、driver、設定、VRAM を記録し、判定単位は3 runsの事前規約を維持する。

複雑度: 高。

## 調査した一次資料

- gsplat official docs/repository: https://docs.gsplat.studio/main/ / https://github.com/nerfstudio-project/gsplat
- Graphdeco reference 3DGS: https://github.com/graphdeco-inria/gaussian-splatting
- Nerfstudio Splatfacto/Windows notes: https://docs.nerf.studio/nerfology/methods/splat.html / https://docs.nerf.studio/quickstart/installation.html
- COLMAP official repository/releases: https://github.com/colmap/colmap / https://github.com/colmap/colmap/releases
- NVIDIA CUDA 12.8 release notes (SM_120): https://docs.nvidia.com/cuda/archive/12.8.0/cuda-toolkit-release-notes/index.html
- PyTorch version matrix: https://pytorch.org/get-started/previous-versions/
- FisherRF (ECCV 2024): https://arxiv.org/abs/2311.17874 / https://github.com/JiangWenPL/FisherRF
- PUP 3D-GS (CVPR 2025): https://openaccess.thecvf.com/content/CVPR2025/html/Hanson_PUP_3D-GS_Principled_Uncertainty_Pruning_for_3D_Gaussian_Splatting_CVPR_2025_paper.html
- Predictive Photometric Uncertainty (ECCV 2026): https://arxiv.org/abs/2603.22786
- Rendering-Aware Bayesian 3DGS (2026 preprint): https://arxiv.org/abs/2607.05522

## 承認記録

2026-07-17 に orange が本計画を承認した。一括実装はせず、まず Phase 0–1（前提確定 + GPU smoke）だけを実施して結果を報告する。Phase 2 以降は smoke 結果と生動画の提供を受けて次の確認へ進む。

承認直後の再確認では PR #59 は open、生動画 `IMG_3899.mov` は既定のローカルフォルダに見つからなかったため、Phase 0 の停止条件に従って環境変更前で待機する。
