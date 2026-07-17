# ハンドオフ: 応用線(issue #48)の GPU 環境移行 — round 3 準備

日付: 2026-07-16 / 状態: ready(移行先セッションの最初の読み物)
対象: 本線「6 秒動画 → 信頼度アノテーション付き 4DGS」(issue #48)
書き手: 応用線セッション(branch `claude/repository-research-track-a-flxtz9`)

---

## 1. なぜ移行するか

Phase 1(実動画・静的)を CPU-only コンテナの自作 NumPy スタック
(K=250・等方性・96×54)で完走した結果、**証明書の検証に必要な
フィット品質(25 dB 級)にこの環境では原理的に届かない**ことが
確定した。round 2 の Gate B 反証(下記)の正直な読みは「18 dB では
残差がバイアス(モデル不整合)支配で、分散型証明書には測るものが
ない」。容量ギャップは自作レンダラの増強ではなく、**GPU 環境 +
本物のスタック(PyTorch + gsplat)への乗り換え**で閉じる。
orange の決定: ローカル RTX 5070(12 GB)で開始、VRAM の壁に実際に
当たったら cloud GPU を検討。

## 2. 現在地(2026-07-16 時点の確定結果)

- **Phase 0(合成・静的)= 完了、PR #54 マージ済み。**
  delta-method 証明書 σ_pred² = J_ρᵀ(H+εI)⁻¹J_ρ が inverse-crime
  合成で Gate A 合格(Spearman +0.909/+0.863/+0.763、バー 0.3)。
  ただし制御群(振幅・‖J‖・diag-H)への一貫した上回りはなし →
  「H⁻¹ 帰属は主張しない」に結論を絞った(research-log 参照)。
- **Phase 1(実動画・静的)= round 1 前提条件 DNF → round 2 で
  前提クリア → Gate B 反証。PR #59(オープン、Sol 再レビュー待ち)。**
  - round 1: 加算レンダラは 17.85 dB で頭打ち(宣言フロア 18 dB)。
    held-out 未開封のまま DNF 記録。診断: 遮蔽。
  - round 2: α 合成レンダラ(composite.py)で全 seed 18.08/18.16/
    18.21 dB — 遮蔽診断は確証。held-out 初開封、Gate B は
    **+0.029/+0.026/+0.026(バー 0.3)で全 seed 不合格**。
    Gate B2 も不合格(‖J‖ 制御 +0.26〜+0.28 が全 seed で勝つ。
    diag-H(≈FisherRF 相当)は +0.05 止まり)。ブラー ablation も
    バー未達。事前宣言した反証条件どおり記録済み。
  - 教訓(round 3 の設計に直結): 分散型証明書はバイアス支配の
    作業点では機能しない。対角 Fisher 近似はさらに弱い。

## 3. リポジトリ内の資産(全部コミット済み)

| 何 | どこ |
|---|---|
| Phase 0 コード + テスト | `experiments/15_video_conf/`, `tests/test_gauss3d.py` |
| Phase 1 レンダラ(加算/合成)・ジョイントフィット | `experiments/16_real_video/{splatvid,composite,jointfit}.py` |
| Phase 1 プロトコルランナー(hard stop 実装込み) | `experiments/16_real_video/run.py`, `tests/test_{splatvid,composite}.py` |
| round 1 再現スクリプト | `experiments/16_real_video/tune.py` + `out_tuning_round1.log` |
| round 2 判定ログ・証明書図 | `experiments/16_real_video/out_run.log`, `heldout_certificate.png` |
| フィット済みチェックポイント(seed×ブランチ) | `experiments/16_real_video/checkpoints/*.npz` |
| データ(縮小版のみ) | `experiments/16_real_video/data/carousel_frames.npz` + `README.md`(来歴) |
| 経緯の一次記録 | `docs/research-log.md`(exp15/exp16 = 16_real_video の各エントリ) |
| 宣言・報告の場 | issue #48(全宣言・全結果)、PR #54(マージ)、PR #59(オープン) |

## 4. ⚠️ 移行時の罠(必読)

1. **生動画はリポジトリにない。** コミット済みは 96×54(フィット用)
   と 192×108(図用)のグレースケール npz のみ。GPU round はフル
   解像度(1920×1080)が前提なので、**orange が新環境に
   IMG_3899.mov(10.3 s, HEVC, 30 fps)を再アップロードする必要が
   ある**。窓の定義は t∈[1,7) の 6 秒(data/README.md に記録)。
   held-out フレームの相対位置(24 フレーム中 4/10/16/22)は
   フレームレートを変える場合は issue #48 で再宣言すること。
2. **RTX 5070 は Blackwell(sm_120)。** PyTorch は CUDA 12.8 以降の
   ビルド、gsplat は新しめのバージョンを掴むこと(古いビルドは
   5000 番台でコンパイル不能の既知問題)。
3. **実験番号の衝突。**「experiment 16」は量子線
   (`experiments/16_exp11_seeds`)と応用線
   (`experiments/16_real_video`)で番号が重複している。新実験は
   ディレクトリ番号を最新の連番から取り、research-log に
   ディレクトリ名を併記する。
4. **PR #59 はマージ前。** 移行後に Sol のレビューが来たら、この
   ブランチ(`claude/repository-research-track-a-flxtz9`)で対応する
   (round 3 は別ブランチで)。
5. **データのライセンス表記は orange の決定待ち**(data/README.md に
   仮置きの権利注記あり)。

## 5. Round 3 計画(宣言ドラフト — 走らせる前に issue #48 で確定)

**問い**: 分散型証明書(delta-method)は、バイアスが十分小さい
高品質フィット(25 dB 級以上)なら実動画の held-out 残差と相関するか。

**段取り**(a→b の順で、対立ではなく順番):

1. **(a) 作業点の移動**: gsplat(または 4DGaussians)+ COLMAP で
   carousel 動画のフル解像度・静的 3DGS フィット。自作レンダラは
   使わない(役目終了)。目標 train PSNR ≥ 25 dB を新しい前提条件
   (hard stop)として宣言。
2. **Gate B 再挑戦**: 同じ構造 — held-out 4 フレーム、
   Spearman(σ_pred, |residual|) ≥ 0.3 全 seed、制御群(振幅・‖J‖・
   diag-H)への一貫した上回り(B2)。**バーは 0.3 のまま動かさない**。
3. **H の近似が新しい科学的変数**: 本家規模(10⁵〜10⁶ splat)では
   フル H⁻¹ は不可能。ブロック対角(splat 単位)から始め、必要なら
   低ランク補正。「どの近似で証明書が生き残るか」自体を記録する。
   exp16 の知見: 対角近似は弱い(+0.05)。
4. **(b) バイアス項**: (a) が通っても通らなくても、分散項 + 残差
   ベース項の二項構成を設計する。比較対象・必読:
   arXiv:2603.22786(post-hoc 残差ベース不確かさ)、
   FisherRF(ECCV 2024、diag Fisher)、arXiv:2607.05522。
5. Phase 2(動的 4DGS)はその後。参照設計: 4DGaussians
   (変形場)/ fudan-zvg 4DGS(ネイティブ 4D)。ポーズは COLMAP
   既知扱いに切り替え(exp16 の自作ジョイントポーズ推定は GPU 環境
   では不要 — 4DGT ですらポーズ外部前提)。

**変えないもの(ethos)**: gate・反証条件は走らせる前に issue で宣言。
held-out はランナーの hard stop の後ろに置く(exp16 run.py の構造を
踏襲)。DNF も反証もそのまま記録。事後リスコープ禁止。

## 6. 環境セットアップ(新セッション最初の 30 分)

```
# 前提: RTX 5070 / driver は CUDA 12.8+ 対応
pip install torch --index-url https://download.pytorch.org/whl/cu128
pip install gsplat  # ビルドに nvcc が要る。sm_120 対応版であること
# COLMAP: apt / conda / 公式バイナリのどれでも
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

検収: gsplat 付属の簡単なシーンが学習・レンダできること。その後
IMG_3899.mov からフル解像度フレームを抽出し、COLMAP でポーズを取り、
round 3 の宣言を issue #48 に書いてから走らせる。

## 7. この線の外(触らない)

量子コア線(#39/#40/#42 完了、#41 以降)は別セッション・別ブランチ。
issue #47(ケージ設計)・#43(アウトリーチ、送信禁止)・#45(Sol の
線)はこのハンドオフの対象外。
