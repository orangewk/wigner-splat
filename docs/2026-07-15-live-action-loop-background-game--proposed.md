# 実写ループ背景＋3Dキャラクター ゲーム試作構想

- 日付: 2026-07-15
- 状態: proposed（構想整理。実装決定ではない）
- 依頼・体験目標: orange
- 技術的な整理・暫定推奨: Codex
- 対象: 固定〜小さな視差を持つ実写背景を編集・ループ再生し、既存のリグ付き3Dキャラクターを配置するゲーム

## 1. 目指す体験

実写映像を単なる平面動画として見せるのではなく、前景・中景・背景と奥行きを持つ「生きている舞台」にする。その中へ既存のpolygon、rig、motionを持つ3Dキャラクターを置き、実写物体の前後を移動させる。

背景は自然にループする。カメラは最初は固定でよいが、後から小さな揺れ・パン・視差を追加できる余地を残す。制作時の重い処理は許容し、低価格ハードでは軽い再生処理だけを行う。

## 2. 基本方針

初期試作は full 4D Gaussian Splatting を前提にしない。中心は **looping video plate + depth + layers + proxy geometry** とし、Gaussian Splatting は視差や奥行き破綻を補う拡張手段として使う。

これにより、映像デコードを端末の専用ハードウェアへ任せ、リアルタイム負荷を3Dキャラクター、遮蔽、影、少量の追加表現へ集中できる。

## 3. 表現の段階

| 段階 | 背景表現 | カメラ自由度 | 用途 |
|---|---|---|---|
| 0 | ループ動画1枚 | 固定 | 最小試作、演出確認 |
| 1 | 前景・中景・背景の動画層 + depth / depth mesh | 固定〜小さな移動 | キャラとの遮蔽、軽い視差 |
| 2 | 静的3DGS + 局所的な動画層／animated splat | 小範囲の移動 | 実写空間らしい奥行き |
| 3 | full 4DGS | 自由視点 | 将来研究。初期スコープ外 |

段階0から順番に価値を検証し、必要な場合だけ次へ進む。

## 4. ランタイムの構成

- **背景plate**: ループする実写動画
- **depth / mask**: キャラクターを実写物体の前後に正しく合成する
- **3Dキャラクター**: polygon + rig + animationを正本として維持する
- **proxy geometry**: 地面、壁、衝突、navmesh、遮蔽判定に使う非表示mesh
- **shadow catcher**: キャラクターの接地影を実写背景へ馴染ませる
- **仕上げ**: fog、color grading、被写界深度、grain等を実写と3Dへ共通適用する
- **任意のGS層**: 小さなカメラ移動、穴埋め、局所VFXが必要になった時だけ追加する

## 5. 制作フロー案

1. 実写クリップを読み込む
2. 使用区間を選び、開始・終了が自然につながるループを作る
3. カメラ、depth、前景mask、地面を推定・手直しする
4. 不要物の消去、色調整、背景補完を行う
5. collision / navmesh / shadow catcher用proxyを作る
6. 既存3Dキャラクターとmotionを読み込む
7. 遮蔽、足の接地、影、画角、色、fogを合わせる
8. 対象端末向けに動画・depth・mask・proxy・scene metadataを出力する

エディタの一文UXは次の通り。

> 実写動画を入れ、ループを決め、奥行きを直し、3Dキャラを置くと、実写の中を歩くゲーム背景として出力できる。

## 6. 編集範囲

### 初期から扱う

- ループ区間の指定と継ぎ目の調整
- crop、mask、不要領域の消去
- 前景・背景の層分け
- depthと地面の修正
- 色、fog、grain等の馴染ませ
- キャラクター・カメラ・proxyの配置

### 後から検討する

- 多視点で一貫した物体除去・生成
- 動く物体の形状変更
- 自由視点の長時間4D背景
- 動的な実写背景への完全なrelighting
- runtimeでの生成編集

## 7. キャラクターをGS化するか

初期段階ではGS化しない。polygon + rigを保つ方が、animation、表情、collision、LOD、動的照明、ゲームロジックを扱いやすい。

将来、見た目だけをGaussianへ変換する場合も、骨格meshはanimationとcollisionの正本として残す。GS化は性能対策ではなく、実写背景との質感統一や特殊演出として評価する。

## 8. Gaussian Splattingを使う場所

GSが有効なのは次の場合に限る。

- 固定背景から少しカメラを動かしたい
- depth meshでは露出する隠れ面を補いたい
- 実写空間の複雑な細部をmesh化せず保持したい
- dissolve、煙、記憶の変形等の局所VFXを作りたい

単に固定背景を再生するだけなら、動画plateの方が安価で安定する。GSを採用すること自体を目的にしない。

## 9. wigner-splatから将来持ち込めるもの

- **周期的な残差splat**: 静的背景との差分だけを短い周期表現として保持する
- **birth / prune**: 動いている場所へだけGaussian予算を割り当てる
- **低ランク時間表現**: ループを少数の時間modeへ圧縮する
- **反証可能な評価**: 映像品質、遮蔽、loop seam、frame time、memoryを同時に測る

これは初期MVPの前提ではない。段階1で動画層の限界が確認された場合の研究拡張とする。

## 10. 最小試作

- 5〜15秒の実写ループ1本
- 固定カメラ、必要ならごく小さな揺れのみ
- 一室または短い屋外区間
- 既存3Dキャラクター1体と歩行motion
- キャラクターが実写前景の後ろを一度通る
- 地面proxy、collision、接地影
- 対象となる低価格端末で安定30 fps

### 合格条件

- ループの継ぎ目が通常プレイ中に目立たない
- キャラクターの前後関係と足の接地が破綻しない
- 実写と3Dの色・粒状感・fogが同じ画として見える
- 30 fps、peak memory、配布サイズを記録できる
- 背景を動画1枚にしたbaselineより、depth / layer追加の価値が見える

### 中止・縮小条件

- depth / maskの手修正コストが背景制作の価値を上回る
- 小さなカメラ移動が体験に寄与しない
- GS層が動画plateより重いだけで、視差や編集性を改善しない
- 実写と3Dの不一致が技術でなくアート制作量に支配される

## 11. 現在の技術との位置関係

- [Instruct-4DGS](https://openaccess.thecvf.com/content/CVPR2025/html/Kwon_Efficient_Dynamic_Scene_Editing_via_4D_Gaussian-based_Static-Dynamic_Separation_CVPR_2025_paper.html): 静的Gaussianと変形場を分離した4D scene編集。制作時編集の先行例。
- [Portals](https://openaccess.thecvf.com/content/CVPR2026W/ReGen4D/html/Tunick_Portals_Persistent_Editable_4D_Spatial_World_Models_on_Edge_Devices_CVPRW_2026_paper.html): edge device上のlayered spatial world、depth・stencil・VFX統合の近接例。
- [PlayCanvas Engine](https://github.com/playcanvas/engine) / [splat-transform](https://github.com/playcanvas/splat-transform): GS、通常mesh、physics、LOD、圧縮、collision proxyを組み合わせる実装基盤候補。

既存研究は自由視点4D再構成を強く追っている。本構想はそこへ競争するのではなく、**固定背景で十分なゲームに、実写の奥行き・ループ・3Dキャラ統合を低コストで提供する制作道具**へ焦点を置く。

## 12. 未決定事項

- 最初の対象端末とengine
- 入力映像を固定撮影にするか、軽いカメラ移動を含めるか
- loop生成を手動中心にするか半自動化するか
- depth / maskの生成手段と手直しUI
- 既存キャラクターassetの想定format
- 背景編集を専用ツールにするかengine editor内へ置くか

これらは実装着手前にorangeが決定する。
