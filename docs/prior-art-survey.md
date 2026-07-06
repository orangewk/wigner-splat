# 3DGS × 量子論 研究プログラム — 先行研究サーベイ

- Status: survey report / done
- Date: 2026-07-06
- 対象: [ポジションペーパー](2026-07-06-3dgs-quantum-program--position.md)のテーマA(§2 トモグラフィー)、B(§3 Wave Splatting)、C(§4 不確定性)の「サーベイ未了事項」
- 手法: マルチエージェント調査(検索7角度 → 候補39件をURL/タイトルで重複除去 → 上位18件を一次ソース精読・closeness採点 → closeness≥6の候補に懐疑派/擁護派/中立の3票による敵対的先取り判定 → 統合)。担当エージェントは全て sonnet。
- 統計: 検索角度 7 / ユニーク候補 39 / 精読 18 / 近接候補(closeness≥6) 4 / 先取り判定(2票以上) 0

---

## 1. 結論サマリ

**テーマA — Gaussian Splatting for Quantum State Tomography: 新規性あり**

homodyne測定データからのトモグラフィー再構成、符号付き(負重み可)異方性Gaussian混合によるWigner負性の表現、3DGS流の微分可能Radon変換フォワードモデル+勾配駆動の適応的densification/pruning、という3要素を同時に満たす先行研究は候補中に存在しない。最も近いのは分類学的に離れた2系統である。ひとつは同じ問題設定(古典的X線CTの微分可能Radon変換+3DGS的密度制御)を持つが量子性・符号付き重みが皆無の [R2-Gaussian](https://arxiv.org/abs/2405.20693)(closeness 6, preemptVotes 0/3)。もうひとつは符号付き(複素重み)異方性Gaussian混合でWigner負性を表現するが、既知の解析的状態を対象とした閉形式の表現論であり、測定データからの逆問題ではない [Kenfack et al. 2004](https://arxiv.org/abs/physics/0304029)(closeness 3)、および自動微分による複素中心Gaussian混合をWignerダイナミクスに用いる [Tosca et al. 2025](https://arxiv.org/abs/2507.14076)(closeness 3)。この2系統を「データからの逆問題」×「符号付き表現」×「3DGS的densification/pruning」という3点の交差として結合する点にテーマAの核心的noveltyが残っている。

**テーマB — Wave Gaussian Splatting: 要ピボット**

「3DGS由来のGaussianプリミティブを複素振幅(振幅+位相)に拡張し、強度でなく振幅を合成してCGH等コヒーレント撮像に適用する」という中核アイデア自体は、2025年に複数の独立研究がほぼ同時に到達しており、テーマBが単独で主張できる新規性の幅はかなり狭くなっている。特に [Complex-Valued Holographic Radiance Fields](https://arxiv.org/abs/2506.08350)(closeness 6, preemptVotes 1/3)は3DGS類似の複素値Gaussianプリミティブをマルチビュー画像から共同最適化し、角スペクトル法で伝搬させて複素ホログラムを合成する、というテーマBの核心とほぼ同型の枠組みをすでに実現している。加えて [Gaussian Wave Splatting](https://arxiv.org/abs/2505.06582)(closeness 6)、[Random-phase Wave Splatting](https://arxiv.org/abs/2508.17480)(closeness 7、ただし重複エントリで4とも記載—要検証)、[Complex-Valued 2D Gaussian Representation for CGH](https://arxiv.org/abs/2511.15022)(closeness 4)、[GSRF](https://arxiv.org/abs/2502.01826)(closeness 3, RF版)、[GSH](https://arxiv.org/abs/2509.20774)(closeness 3, レンズレスホログラフィー版)が同じ方向性を様々な角度から埋めている。厳密な閾値(closeness≥8またはpreempts=true)には該当しないが、密集度が高く、素朴な「複素振幅Gaussian splatting for CGH」という主張のままでは差分がほぼ消えている。生き残る新規性は「exact Gaussian-beam/ABCD行列伝搬による閉形式パイプラインの維持」「CGH以外(OCT・デジタルホログラフィー・スペックル)への一般化」「非コヒーレント3DGSを厳密な極限として回収する理論的統一」の3点に絞られており、主張の再構成(ピボット)が必要である。

**テーマC — Anti-aliasing in 3DGS as an uncertainty principle: 新規性あり(ただし要追加調査)**

本サーベイの候補にはテーマCに該当する先行研究が一件も含まれていない。少なくとも今回のサーチ範囲では、Mip-Splatting等の3DGSアンチエイリアシング手法とGabor–Heisenberg位置-周波数不確定性原理を明示的に接続した公表研究は見つかっていない。これは強い「クリア」の証拠ではなく「この検索では発見されなかった」ことを意味する点に注意。信号処理・ウェーブレット・ガボール限界に関する既存文献(3DGS文脈に限らない一般論)を対象に追加調査してから最終判断することを推奨する。

---

## 2. テーマ別詳細

### テーマA

| 論文名(年) | 何をしたか | closeness | preemptVotes | 残る差分 |
|---|---|---|---|---|
| [R2-Gaussian: Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction](https://arxiv.org/abs/2405.20693) (2024) | 3DGSプリミティブ+微分可能X線Radon投影+3DGS流densification/pruningでスパースビューCT再構成。積分バイアスを補正する「rectification」を提案。 | 6 | 0/3 | 量子状態・homodyneデータ・Wigner/Husimi再構成に一切触れず。密度は非負の物理減衰係数で、符号付き(負)重みの概念が皆無、むしろ正値化バイアスを補正する真逆の設計思想。3DGS-for-Radon-tomographyという「機構」の直接的先例だが、「量子状態への応用」と「Wigner負性を表す符号付き重み」という核心クレームは未着手。 |
| [X²-Gaussian: 4D Radiative Gaussian Splatting for Continuous-time Tomographic Reconstruction](https://arxiv.org/abs/2503.21779) (2025) | R2-Gaussian系列を4D(動的)CTに拡張、時空間デコーダで呼吸周期を自己教師あり学習。 | 3 | — | 古典的X線CT・非負密度のまま。符号付きGaussian・量子性は皆無。 |
| [Optimal representations of quantum states by gaussians in phase space](https://arxiv.org/abs/physics/0304029) (2004) | 既知の量子状態を最少数の複素重み付き(符号付き)異方性Gaussianの和として位相空間に表現する2段階最適化アルゴリズム。 | 3 | — | 対象は既知の解析的状態であり、homodyneデータからの逆問題ではない。微分可能フォワード投影による当てはめも、勾配駆動のsplitting/pruningも存在しない。「符号付き異方性Gaussian混合でWigner負性を表す」表現論の直接的先行例として引用必須。 |
| [Efficient Variational Dynamics of Open Quantum Bosonic Systems via Automatic Differentiation](https://arxiv.org/abs/2507.14076) (2025) | 複素中心Gaussian混合(Variational Multi-Gaussian)でWigner関数を表現し、変分運動方程式を自動微分で解いて開放量子系ダイナミクスをシミュレート。cat状態の負の干渉縞を再現。 | 3 | — | 逆問題ではなくフォワードシミュレーション。densification/pruning皆無。符号付き重みでWigner負性を表す点のみ重なる。 |
| [Simple, reliable and noise-resilient CV QST with convex optimization](https://arxiv.org/abs/2202.11584) (2022) | homodyne/heterodyneデータから凸最適化(SDP)でFock基底密度行列を再構成。 | 3 | — | Gaussian混合表現ではない。「homodyneデータからの再構成」という問題設定のみ共通。 |
| [Gradient-descent methods for fast quantum state tomography](https://arxiv.org/html/2503.04526v1) (2025) | 密度行列を物理制約を保つパラメータ化のもとで勾配降下最適化、CV系でWigner関数出力まで実証。 | 3 | — | 表現は密度行列。Gaussianプリミティブ・符号付き重み・Radon型フォワードモデル・densification不在。 |
| [Witnessing negativity of Wigner function from homodyne measurements](https://arxiv.org/abs/1306.0508) (2013) | パターン関数でcat状態忠実度を推定しWigner負性をワンポイント証明。 | 1 | — | スカラーの負性ウィットネス。関連性は低い。 |
| [Gradient-Descent Quantum Process Tomography by Learning Kraus Operators](https://link.aps.org/pdf/10.1103/PhysRevLett.130.150402) (2023) | Kraus演算子のStiefel多様体上制約付き勾配降下。 | 2 | — | プロセストモグラフィー。位相空間・Gaussian・符号付き重み皆無。 |
| [Efficient factored gradient descent algorithm for quantum state tomography](https://link.aps.org/doi/10.1103/PhysRevResearch.6.033034) (2024) | ρ=TT†分解による多量子ビット状態トモグラフィーの高速勾配降下。 | 2 | — | 離散変数。Gaussian混合概念が皆無。 |
| [Neural networks for detecting multimode Wigner-negativity](https://arxiv.org/pdf/2003.03343) (2020) | NNでhomodyne型データから多モードWigner負性の有無を直接分類。 | 2 | — | 再構成せず分類のみ。 |
| [Experimental quantum homodyne tomography via machine learning](https://opg.optica.org/optica/fulltext.cfm?uri=optica-7-5-448&id=431506) (2020) | 制限ボルツマンマシンで実験homodyneデータから状態再構成。 | 2 | — | NN生成モデルでありGaussian混合ではない。 |

**生き残る新規性:** 「homodyneデータ(測定)からの逆問題」「符号付き異方性Gaussian混合表現(Wigner負性=負スプラット)」「3DGS流の微分可能フォワード投影+勾配駆動densification/pruning」の3点をすべて満たす研究は存在しない。R2-Gaussianが機構を、Kenfack (2004) とTosca et al. (2025) が表現を、それぞれ別領域で先取りしているに過ぎない。

**主張文言の調整案:** 「3DGS機構を量子トモグラフィーに初めて導入する」という素朴な言い方は避け、「3DGS-for-Radon-tomography機構(R2-Gaussian, X²-Gaussian)と、符号付きGaussian混合によるWigner負性表現(Kenfack 2004, Tosca 2025)という2つの独立した先行系譜を統合し、実測homodyneデータからの逆問題として初めて結合する」という形で差分を明示すべき。また、負性を保ったまま物理的制約(正規化・周辺分布整合)を課す最適化上の課題が新規の技術的困難であることも明記する。

### テーマB

| 論文名(年) | 何をしたか | closeness | preemptVotes | 残る差分 |
|---|---|---|---|---|
| [Complex-Valued Holographic Radiance Fields](https://arxiv.org/abs/2506.08350) (2025) | 3DGS類似の複素値(振幅+位相)Gaussianプリミティブをマルチビュー画像から共同最適化。深度平面へ投影し角スペクトル法(FFT)で伝搬して複素ホログラム合成、最後にのみ強度化。30〜10,000倍高速化。 | 6 | 1/3 | 伝搬が角スペクトル法(離散深度平面・FFT)であり、exact Gaussian-beam/ABCD行列伝搬による閉形式パイプラインではない。非コヒーレント3DGSの厳密極限回収なし。応用はCGH/新規視点合成限定。**ただし中核アイデアはほぼ同一で、最も脅威度が高い先行研究。** |
| [Gaussian Wave Splatting for CGH](https://arxiv.org/abs/2505.06582) (2025, SIGGRAPH) | 既存3DGS/2DGSシーンをGaussian-to-hologram閉形式変換+Fourier領域近似でホログラムに変換。 | 6 | 0/3 | 学習済みシーンからの一方向フォワード変換であり、複素振幅・位相を一次パラメータとするEnd-to-End最適化表現ではない。 |
| [Random-phase Wave Splatting of Translucent Primitives](https://arxiv.org/abs/2508.17480) (2025) | GWSをランダム位相プリミティブ+時間多重alphaブレンディングで拡張。近眼ディスプレイ向けCGH。 | 7(重複エントリで4とも — 要検証) | 0/3 | 既存GWSの改良。ABCD伝搬・非コヒーレント極限・OCT等への一般化は主張せず。 |
| [Complex-Valued 2D Gaussian Representation for CGH](https://arxiv.org/abs/2511.15022) (2025) | ホログラム平面上の複素値2D Gaussian+微分可能ラスタライザ+自由空間伝搬でEnd-to-End最適化。 | 4 | — | 3Dシーン表現ではなく2Dホログラム面上の表現。 |
| [Gaussian Splatting Holography (GSH)](https://arxiv.org/abs/2509.20774) (2025) | 2D Gaussianスプラットで複素光場を圧縮表現し、レンズレスホログラフィー位相回復。 | 3 | — | 単一平面の複素場パラメータ化。3DGSパイプライン不使用。 |
| [GSRF: Complex-Valued 3D Gaussian Splatting for RF](https://arxiv.org/abs/2502.01826) (2025, NeurIPS) | 複素値3D Gaussian+複素レイトレーシングでRF信号合成。 | 3 | — | RF帯域。ただし「複素値3DGS+波動伝搬」の発想が他モダリティでも既出である証左。 |

**生き残る新規性(3点に限定):** (1) exact Gaussian-beam/ABCD行列伝搬による閉形式パイプラインの維持(既存はすべてFFT/角スペクトル/自由空間の数値近似)。(2) 非コヒーレント3DGSを厳密な数学的極限として導出する統一理論(未実証)。(3) CGH以外のコヒーレント撮像モダリティ(OCT、デジタルホログラフィー、スペックル)への一般化(未着手)。これらが実証できなければテーマBは競合と差別化困難。

### テーマC

候補に該当エントリなし。3DGSのアンチエイリアシング(Mip-Splattingの最小スプラットサイズ/3D平滑化フィルタ)とGabor–Heisenberg不確定性原理を明示的に接続した公表研究は、今回のサーチでは一件も見つからなかった。ただし「見つからなかった」ことに基づく消極的結論であり、(a) Mip-Splatting原論文と引用ネットワークでのGabor/Heisenberg/uncertainty/time-frequencyキーワード共起の確認、(b) 信号処理・光学分野での「アンチエイリアシングフィルタ設計と不確定性原理」の一般論の確認、を経てから最終判断すべき。

---

## 3. 検証メモ(未検証・情報が食い違う候補)

- **アクセス不可(アブストラクト等の二次情報のみで評価):** [Tosca et al. 2025](https://arxiv.org/abs/2507.14076)、[Strandberg 2022](https://arxiv.org/abs/2202.11584)、[Kraus QPT 2023](https://link.aps.org/pdf/10.1103/PhysRevLett.130.150402)、[factored GD QST 2024](https://link.aps.org/doi/10.1103/PhysRevResearch.6.033034)、[Tiunov et al. 2020](https://opg.optica.org/optica/fulltext.cfm?uri=optica-7-5-448&id=431506)、[RPWS](https://arxiv.org/abs/2508.17480) の一方のエントリ
- **3票が割れた候補:** [Complex-Valued Holographic Radiance Fields](https://arxiv.org/abs/2506.08350) は1票が「先取りしている」と判定。少数意見(「ABCD行列という差分は実装上の変種に過ぎない可能性」)は無視すべきでない
- **重複・矛盾エントリ:** [arxiv.org/abs/2508.17480](https://arxiv.org/abs/2508.17480) に対し closeness 7/accessible:true と closeness 4/accessible:false の二重評価が存在。一次資料で再確認しテーマBの最終判断に反映すべき
- **テーマC:** 候補ゼロは「未調査」の可能性を否定できず、追加調査完了までは暫定判定

---

## 4. 推奨アクション

**テーマA:** (1) 主張を「2系譜の初の統合」として再定式化。(2) Related Work に R2-Gaussian / X²-Gaussian(機構)、Kenfack 2004 / Tosca 2025(表現)、Strandberg 2022 / Gaikwad 2025(homodyne最適化)を必ず引用。(3) 負重みスプラットへの物理制約(正規化・周辺分布整合)を新規の技術的困難として明記。

**テーマB:** (1) 広い主張は取り下げ、Complex-Valued Holographic Radiance Fields を正面から引用・対比。(2) 核心主張をABCD厳密伝搬・非コヒーレント極限理論・多モダリティ一般化の3点に絞る。(3) 近接研究との機構差を表形式で明示。(4) RPWSの重複エントリ矛盾を一次資料で解消。

**テーマC:** 執筆前に追加サーチ(Mip-Splatting引用ネットワーク+信号処理一般論)。クリアなら最も確度の高い新規性を持つテーマとなる。

**着手順序:** テーマA最優先(差分明確・追加検証少)。テーマCは追加サーチ後すぐ着手可能、並行調査が効率的。テーマBはピボット3点の実装・実証の見通しが立つまで保留し優先順位は最後。
