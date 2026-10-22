# Signed splat の対消滅から Gaussian jet へ — 応用アイデア記録

日付: 2026-08-08  
status: **proposed（アイデア記録。実装・有効性・novelty は未確立）**  
関連: PR #158 / Issue #89 / Experiment 22

## 0. 一言

正の Gaussian splat と負の Gaussian splat は、同位置・同形なら消滅する。位置差を \(h\) に縮めながら係数を \(1/h\) で拡大すると、極限には何も残らないのではなく Gaussian の方向微分が残る。三項なら二階微分が残る。

\[
\frac{G(x+h)-G(x)}{h}\to G'(x),\qquad
\frac{G(x+h)-2G(x)+G(x-h)}{h^2}\to G''(x).
\]

これは PR #158 の閉包候補に現れる \(P(x)e^{q(x)}\)（衝突した Gaussian 原子から生じる jet）を、splat 表現として可視化・利用する案である。

## 1. 既存成果との距離

### 1.1 Experiment 22 で既にできていること

[Issue #89 signed-splat demo](2026-07-20-issue-89-signed-splat-demo--done.md) と
[Experiment 22](../../experiments/22_signed_splat_demo/README.md) は、学習済み CC0 3DGS を用いて以下を高精細動画化済み。

- **eraser**: 3D 球内の元 splat の opacity を減衰させ、背面を露出する。
- **dark-flashlight**: 52 個の負 Gaussian からなる 2D signed field を、通常レンダリング後の画像へ減算する。
- **annihilation**: 移動する負コピーを別途レンダリングして RGB を減算し、接触時には元 splat の opacity をフェードアウトする。

したがって、既存成果は「負の寄与で消す／暗くする／対消滅を見せる」という**表現デモ**までは到達済みである。

### 1.2 まだ実装していないこと

既存実装は、負の opacity を持つ3D primitiveを alpha compositingへ直接投入していない。

- eraser は正 opacity のマスク減衰。
- dark-flashlight は screen-space の post-render signed field。
- annihilation は正レンダリングと負コピーの RGB 差分 + 正 opacity の消去。

よって、PR #158 の数学が扱う「線形結合した Gaussian 原子が衝突し、正規化極限で (P e^q) を生む」現象とはまだ別物である。見た目の距離は近いが、表現・極限・誤差保証の距離は残る。

### 1.3 先行 NegGS との距離

NegGS (Kasymov et al., arXiv:2405.18163) は negative Gaussian を負の色として導入し、Diff-Gaussian により高周波要素、急な色変化、影の表現改善を報告している。したがって「負の Gaussian を3DGSに入れる」だけでは新規主張にできない。

本案の差分候補は次の三点。

1. splat の**衝突極限**を derivative/jet primitive として扱う。
2. 近接した正負クラスタを一つの (P e^q) primitive へ圧縮する。
3. K2 型不等式により、局所的に消えたクラスタが別区間で爆発しないための認証を検討する。

いずれも現時点では応用仮説であり、先行調査と実証が必要。

## 2. 応用候補

### A. Differential splat（境界・法線・曲率 primitive）

二項衝突を一次 Gaussian jet、三項衝突を二次 Gaussian jet として直接レンダリングする。

- 一次 jet: 符号の異なる二葉。エッジ、法線方向、薄い境界。
- 二次 jet: 中央と外側で符号が変わる。曲率、リッジ、薄い殻。
- 高次 jet: 細部や振動を少数 primitive で表す候補。

### B. Signed-splat 圧縮

ほぼ相殺する近接 splat 群を削除するのではなく、低次 jet primitive へ置換する。

候補評価量:

- 元クラスタと jet 置換の画面誤差
- primitive 数と描画時間
- 視点変更時の誤差
- 衝突距離 \(h\) に対する収束率
- K2 型上界と実測 worst-case の差

### C. Cancellation certificate

小さい観測領域 (J) で残差が小さいことだけを理由に splat を prune すると、別領域 (I) で大きな残差が現れる恐れがある。K2 は二次位相二項和について

\[
\sup_I|F|\le 300\varepsilon^{-2}e^{A+\Lambda\varepsilon}\sup_J|F|
\]

を与える。ray 上の加法的 signed field に特殊化できれば、相殺クラスタの安全な削除・jet 化を認証する候補になる。

注意: 標準3DGSの visibility/transmittance を含む alpha compositing は線形和ではない。適用対象は signed feature buffer、radiance residual、optical-depth residual 等の線形段に限定して設計する必要がある。

### D. 「負の光」の次段階

既存 dark-flashlight は画像上の減算効果であり、物理的な負の光を主張しない。次段階は二系統に分ける。

- **表現系**: signed radiance residual を3D空間に置き、視点を変えても一貫した暗部投影になるか検証する。
- **波動系**: 負の係数を位相差 \(\pi\) と読み替え、複素 Gaussian beam の破壊的干渉として扱う。こちらは「負のエネルギー」ではなく、通常の波の位相相殺なので物理的意味を持つ。

PR #158 の複素二次位相 K2 に近いのは後者。

## 3. 最小実験案（未承認・未実装）

1. 1D/2D の加法的 renderer で \(+G/h\) と \(-G(\cdot-h)/h\) を表示。
2. \(h\to0\) で解析的な \(G'\) へ収束するか、L²・sup 誤差を測る。
3. 三項 \((1,-2,1)/h^2\) と \(G''\) も同様に測る。
4. 既存 cactus scene の別 signed buffer 上で jet primitive を投影する。
5. 通常3DGS画像への合成は最後に行い、alpha/transmittance 本体とは分離する。

この順なら既存動画・GPU rendererを再利用しつつ、最初から負 opacity の非線形問題へ入らずに済む。

## 4. 外向けの物語

> 正の splat と負の splat は重なると消える。  
> しかし、ほんの少しずれて衝突すると、境界や曲率という「形の微分」を残す。  
> wigner-splat は、この対消滅の残り方を Gaussian jet として捉え、どこまで少数の primitive で複雑な形・波・量子状態を表せるか調べる。

公開時に分離する主張:

- **実演済み**: eraser / dark-flashlight / annihilation の動画表現。
- **数学ドラフトあり**: 二項二次位相 K2 と \(c=2\) の弱増大度評価。
- **未実証の応用仮説**: jet splat 圧縮、K2によるpruning認証、物理波動への適用。
- **未完成**: 一般 \(c\) の閉包定理、半直線状態の発散結論。

## 5. 概念図

gpt-image-2 用の原文プロンプトは orange の指定後に固定する。生成前に枚数・比率・出力先を確認し、原文を編集せず渡す。

予定配置: `experiments/22_signed_splat_demo/media/signed-splat-jet-concept.png`

## 6. 参照

- [K2 独立ドラフト](../2026-08-08-quadratic-phase-turan-K2.md)
- [閉包定理ドラフト](../2026-08-02-gaussian-border-rank-closure--wip.md)
- [研究状況](../2026-08-08-closure-research-status.md)
- [Experiment 22 README](../../experiments/22_signed_splat_demo/README.md)
- NegGS: https://arxiv.org/abs/2405.18163
