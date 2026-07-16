# Birth-field image demo

exp02 の教訓(「分裂は親の符号を保存する。最適化そのものは重みをゼロ通過させて符号を変えられる」)を、量子トモグラフィの文脈を知らない読者向けに **画像フィッティング**として可視化するデモ。issue #46 案④の第一号成果物。

## なにを見せるか

ターゲットはこのリポジトリの主役 — 猫状態(α=2)の Wigner 関数を「ただの符号つき画像」として扱い、符号つき 2D ガウススプラットでフィットする。同一予算(iteration・スプラット数・seed)で densification 規則だけを変えて比較:

- `split`: 勾配蓄積が最大のスプラットを長軸方向に半分ずつへ分裂(3DGS 流ベースライン。分裂は符号を保存する — `split_one` を直接テスト)
- `birth`: **birth field**(仮想新規スプラットの重みに関する損失勾配の閉形式 = 残差のカーネル平滑化)の |最大| 点に、場の符号で新スプラットを産む
- `birth_pos` / `birth_zero`: 帰属 ablation — 配置・スケールは `birth` と同一で、初期重みだけ「正固定」/「ゼロ」

## 実行

```
python demos/birthfield_image/run.py   # リポジトリのルートから、~15 分
```

依存: コアモジュール `birthfield2d.py` は **numpy のみ**。`run.py`(資産生成)は追加で matplotlib・Pillow と、ターゲット生成にリポジトリの `wigner_splat.fock` を使う。

## 出力の読み方

- `birthfield_demo.gif` — 5 面: ①ターゲット ②現在の再構成 ③スプラット地図(青=正、赤=負の輪郭)④birth field(次の一手が光る地図)⑤損失曲線(縦の赤線 = birth 事象)。**③の同一時点の状態に ④・② が揃えてある**(post-update で再レンダリング)
- `comparison.png` — 損失曲線(split 青 / birth 赤 / ablation 橙・緑、各 3 seeds)+ 最終画像の並置
- `out_run.log` — committed log(科学表記の生の数値、宣言済み判定つき)

## 主張のスコープ(正直コーナー)

- 「split では負が永遠に得られない」は**この目的関数では偽**(最適化は重みをゼロ通過できる)。成り立つのは「分裂そのものは符号を保存する」まで
- **headline は 1000 updates の共通固定予算時点**(全方式 K=10)の paired(同一 seed)比。4000 iter の結果は一度きりの補助記録、GIF は固定 seed の完成イメージ(比較証拠ではない)
- ablation が分離したのは**初期符号のみ**(配置・初期スケール・生成方式は birth 変種間で共通、split とは異なる)。支持される結論は「符号注入は主因ではない」+「**複合** birth 規則がこの split baseline に勝つ」まで — 配置**単独**への帰属は別の scale/position ablation が必要で、ここでは主張しない
- 集計は paired(同一 seed 比の中央値)。プール別中央値の比は使わない
- ここで示すのは 2D 画像フィッティング上の原理可視化であり、本物の 3D パイプラインでの新規視点合成品質の改善は**主張しない**(それは issue #48 のスコープ)

検証: `python -m pytest tests/test_birthfield2d.py`(FD 勾配一致、birth field = 解析的 dL/dw、符号保存、負スプラット birth の実証)
