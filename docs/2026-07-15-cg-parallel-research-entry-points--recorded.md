# 2026-07-15 CG 並走研究と「白馬の騎士」になれる入口

- 状態: recorded / quick survey（方針決定ではない）
- 依頼: orange — CG / Gaussian Splatting の激戦区で何が進み、wigner-splat がどこから入れるかを記録する
- 判断: Codex — 2026-07-15 時点の一次資料とリポジトリ成果から暫定順位を付けた
- 実装判断: 未決定。既存の [issue #45](https://github.com/orangewk/wigner-splat/issues/45) が本命仮説の検証計画

## 結論

**最も「白馬の騎士」らしく登場できる舞台は、通常の RGB 3DGS 高速化ではなく、部分コヒーレントな wave / holographic Gaussian Splatting の対話編集である。**

先行研究は、Gaussian scene を coherent hologram に変えるところまでは急速に進んだ。[Gaussian Wave Splatting](https://arxiv.org/abs/2505.06582) は閉形式変換と CUDA、[Complex-Valued Holographic Radiance Fields](https://arxiv.org/abs/2506.08350) は複素 Gaussian の学習と伝搬を実現している。一方、実機に近い部分コヒーレンス、speckle、焦点・絞り変更を、品質予算つきで対話速度に乗せる統合 UX はまだ狙い目に見える。

wigner-splat の横入り材料は、PR #44 までに検証した低ランク物理表現 `rho = B B^H` を coherence matrix に読み替えることにある。

```text
J = B B^H
I(p) = g(p)^H J g(p) = ||B^H g(p)||^2
```

一般の primitive 間相互作用 `O(K^2)` を、実効 coherence rank `R` が小さい領域で `O(RK)` に落とす。`B B^H` は強度の非負性を構成的に保ち、rank を quality / FPS knob にできる。低ランク分解そのものは既知なので、新規性候補は **learnable Gaussian basis + PSD coherence + analytic propagation + adaptive rank + interactive / foveated UX** の組合せである。

## 登場シーン

既存 wave splatting の scene をそのまま読み、焦点面・絞り・coherence を動かす。speckle と defocus が連続的に変化し、フレーム予算に合わせて rank が自動調整される。

見せ場は「さらに速い静止画」ではない。**coherent CGH の高速フォワード変換を、実機条件を触れる光学エディタへ変える**ことである。量子トモグラフィー由来の `B B^H` が、CG 側では「物理的に壊れない coherence editor」になる、という越境物語も明瞭。

成功条件は issue #45 の Gate B/C に集約される。

- 非自明な partial-coherence 条件で、full pairwise / Monte Carlo /既存 mode propagation より明瞭な速度・メモリ差が出る
- focus / aperture / coherence の変更が待ち時間でなく連続操作になる
- rank truncation error が見た目と物理量の双方で予測可能

必要 rank が常に `K` 近く、occlusion が支配し、既存 mode 法と同等以下ならこの舞台から降りる。

## 他の戦線との順位

### 2位 — signed birth / birth–death densification

このリポの「残差逆投影の極値へ、改善符号を持つ Gaussian を誕生させる」仕組みは、局所 split より global な functional-gradient / matching-pursuit 型として逆輸出できる可能性がある。量子・CT・CG を貫く理論テーマとしては最も面白い。

ただし「未解決の荒野」ではない。[SteepGS](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_Steepest_Descent_Density_Control_for_Compact_3D_Gaussian_Splatting_CVPR_2025_paper.html) は saddle point からの split を最適化理論で説明し約50% compact 化、[GS^2](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_GS2_Graph-based_Spatial_Distribution_Optimization_for_Compact_3D_Gaussian_Splatting_CVPR_2026_paper.html) は ELBO 型の adaptive densification、[Difference-of-Gaussian primitive](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Prune_Wisely_Reconstruct_Sharply_Compact_3D_Gaussian_Splatting_via_Adaptive_CVPR_2026_paper.html) は正負密度、[EDGS](https://openaccess.thecvf.com/content/CVPR2026/html/Kotovenko_EDGS_Eliminating_Densification_for_Efficient_Convergence_of_3DGS_CVPR_2026_paper.html) は densification 自体の廃止を攻めている。

したがって登場条件は厳しい。単なる新しい heuristic ではなく、**global residual birth と death を一つの目的関数から導き、primitive budget・単調改善・multi-view occlusion のいずれかを保証し、SteepGS 等に実測で勝つ**必要がある。当面は issue #45 の adaptive rank を支える技術、または独立した比較研究として扱うのが妥当。

### 3位 — 不確定性原理から導く anti-aliasing / LOD

Gaussian の空間幅と周波数幅を Gabor–Heisenberg の制約として扱い、view scale ごとの最小 footprint、culling、LOD error を一つの式から出せれば理論的な入口になる。ただし [3D Gabor Splatting](https://arxiv.org/abs/2504.11003) など周波数表現側も進んでいる。説明の言い換えだけでは弱く、既存 filter より良い誤差境界または自動予算配分が必要。現状は「騎士の理論武器」であって舞台そのものではない。

### 4位以下 — mobile / console、4D editing、sorting-free renderer

- mobile / console は大きな市場だが、独自の入口ではなく配備先。[Portals](https://openaccess.thecvf.com/content/CVPR2026W/ReGen4D/html/Tunick_Portals_Persistent_Editable_4D_Spatial_World_Models_on_Edge_Devices_CVPRW_2026_paper.html) は iPhone 上の editable 4D world と 60 fps をすでに示している。issue #45 が成立した後の foveated rank 配備先としては有望。
- 4D editing は canonical scene + deformation、時間整合、編集伝播の競争が激しい。[Catalyst4D](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Catalyst4D_High-Fidelity_3D-to-4D_Scene_Editing_via_Dynamic_Propagation_CVPR_2026_paper.html) などに対し、現リポは概念的並走に留まる。
- sorting-free rasterization は alpha compositing の順序依存を解く別問題。[StochasticSplats](https://openaccess.thecvf.com/content/ICCV2025/html/Kheradmand_StochasticSplats_Stochastic_Rasterization_for_Sorting-Free_3D_Gaussian_Splatting_ICCV_2025_paper.html) は unbiased Monte Carlo で sorting を外し4倍超を報告した。加算的な Radon 投影や `B B^H` は、通常の occlusion を自動では解かない。

## 推奨

最初の一手は新規実装ではなく、issue #45 Phase 0/1 の前に **実効 coherence rank が小さくなる条件の紙上・小規模数値監査**を行うこと。ここが成立すれば、white-knight story は次の一文になる。

> Gaussian Wave Splatting が高速な hologram を作れるようになった。その次に必要な、実機の coherence と speckle を触れる速度で編集する層を、量子状態の低ランク物理表現から持ってきた。

成立しなければ、CG への主入口を無理に作らず、signed birth を SteepGS 系と正面比較する理論課題へ戻す。

## 調査限界

これは 2026-07-15 の quick scan であり、網羅的 systematic review ではない。特に partial-coherence renderer と global functional-gradient densification については、実装着手前に引用ネットワークと公開コードを追加確認する。
