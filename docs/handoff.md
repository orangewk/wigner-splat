# handoff - Next session work order

> 更新: 2026-07-09（issue #8 物理性の調査を完了した回）
> 前回の作業指示（exp06 回収）は完了済み。以下は現在地と次の作業。

## 0. まず読む
1. `README.md`（3つの反証判定 + issue #8 判定＝物理性 tension の節）
2. `docs/research-log.md`、`docs/three-mode-plan.md`
3. この handoff の「Where things stand」

## 1. セットアップ
```
pip install numpy matplotlib pytest    # 実際は venv 必須（下記 gotcha 参照）
python -m pytest tests/ -q -m "not slow"   # ~71 passed 想定（slow は 15分の MLE budget test 等）
```
- **venv 必須**: この環境の pip は `PIP_REQUIRE_VIRTUALENV` でグローバル install を拒否する。`python -m venv .venv` → `.venv/Scripts/python.exe -m pip install numpy matplotlib pytest`。
- pytest 依存は numpy 2.2.6 / matplotlib 3.10.9 / pytest 9.1.1。

## 2. FIRST TASK — 未マージ PR の確認とマージ
- **PR #12** `fix(exp08): diagnose_1mode の grid 演算子基底の虚部欠落を修正`。`fock.wigner_from_rho` を非 Hermitian `|m><n|` に流用して虚部を落としていたバグ。Hermitian/i-Hermitian 分解で修正。
- **PR #13** `feat(exp08): 少数 shape パラメータ PSD polish — #8 3モード tension を firm`。#8 の shape-polish 判定 + conftest docstring 訂正 + 本 handoff。
- どちらも main へ。CI は無いので内容レビューのみ。マージ後に merged branch を削除、`git worktree prune`。

## 3. Where things stand（2026-07-09）

### スケーリング梯子（確定、変更なし）
1モード: MLE 2倍速勝ち（利得なし）｜ 2モード: fidelity 互角（20シード p=0.121）・splat 7.4倍速｜ 3モード: seed42 で splat が両勝ち（F 0.756 vs 0.676-DNF、15s vs 901s）。

### issue #8 物理性 — 調査完了、判定確定
splat 出力の ρ は PSD 保証がない（Wigner 負性=正しい、固有値負性=非物理は別物）。閉形式 Fock 射影 `wigner_splat/fock_project.py:rho_from_splat`（1/2/3モード、cat1 一致 4.4e-9・cat3 trace が既知打切上限 0.99321 と厳密一致で検証済み）で ρ を materialize し、フィット中に PSD ペナルティを課して反証条件（(a) ΔF>−0.03 かつ (b) 射影後 min_eig≥−1e−9）を実測:
- **1モード（full-param polish + 射影）**: negativity 0.070→0.007 を安く削り λ=5〜50 で両立 → **解決可能**。
- **3モード（exp06 seed42、weight-only polish）**: 物理化で fidelity 0.75→0.4 崩壊、全 λ 不合格。
- **3モード（shape+weight polish、3 global ノブ）**: weight-only より改善（proj F 0.49 vs 0.38）だが ΔF −0.26 で桁違い不合格。
- **判定**: 3モードでは **fidelity 優位と PSD 物理性が robust な tension**。weight-only の交絡でなく本質的（shape 自由度でも救えず）。exp06 の3モード勝ちは**少なくとも一部が非物理な Wigner-overlap score 由来**。ただし **full 28-param/splat FD は計算非現実的で未検証**（趨勢から救済見込みは薄い）。

### issue #8 続報 — ρ=BB† 実装済み、tension 解消（このベンチマーク、2026-07-11）
`wigner_splat/bbdag.py`（1モード）/`bbdagM.py`（多モード coherent-product ket）を実装。状態を組んで
マージナルを導出（p_θ=|ψ_θ|²/Z）→ 構成的に物理。同一指標で3モード再対戦: **BB†(物理) F 0.9501/0.9434/0.9332
(seed 42/1/2) が 符号付き splat(非物理) 0.756/0.741/0.624 を上回る**。NLL(fit)<NLL(真) より F~0.95 は
データ限界 ceiling。判定: この cat では physicality はボトルネックでない（負性は不要だった）。
**scope**: BB† ansatz はターゲット族を含む（target-aligned）→「一般に無コスト」は未主張。
図: `experiments/08_positivity/issue8_resolution.png`。実験: `bbdag_prototype_1mode.py`/`bbdag_3mode.py`/
`bbdag_3mode_robustness.py`/`figure_issue8.py`。

### 次にやる価値（優先順）
1. **BB† の firm-up（#8 を「このベンチマーク」から広げる）** — (a) 族外ターゲット（squeezed cat・非等振幅・
   mixed・損失チャネル）で BB† が splat を上回るか、(b) train/test split で held-out 比較（「負性=noise-fitting」
   を言えるようにする）、(c) **解析勾配**（現状 FD で ~300-1600s、splat 15s に対し大幅に遅い→速度優位の回収）、
   (d) 多モード squeeze の一般化。oracle fairness review 由来。
2. **#6 もつれコスト予想の理論化**（exp05: R ~ k、Gabor フレーム理論で下界 → 短い note/preprint）。
3. **#4 実データ**（検出効率 eta + ガウス暗ノイズ = フォワードモデルへの1回のガウス畳み込み。公開 homodyne データで MLE と再対戦）。
4. follow-up（小）: 3モード shape polish を full-param 近くまで広げられれば #8 の最後の caveat が閉じる（現状 3ノブ止まり、計算コスト大）。

## 4. Gotcha / 運用注意（今回の教訓）

### マルチセッションと worktree（重要）
- **共有チェックアウトで複数セッションが同時に pytest を回すとデッドロックする**（2026-07-09 に2時間ハング）。真因: `C:/dev/wigner-splat` を Claude と Codex が共有し、両者が pytest を並行起動（一方 .venv、一方 system Python）。片方が 0 CPU でブロック。
- **対処**: セッションごとに `git worktree` で分離（各自の `.pytest_cache`/`__pycache__`/collection になる）。`AGENTS.md`: 「ハングして見えても2本目の pytest を起動せず、まず元プロセスを kill/診断」。
- `conftest.py` の BLAS スレッド pin は**再現性/oversubscription 回避**であり、このハングの対策ではない（BLAS 仮説は非再現。docstring に明記済み）。
- 2 セッション以上は **worktree 必須**（プロジェクト/グローバル CLAUDE.md のルール）。後付けで stash すると別セッションの未コミット編集を巻き込む（今回 diagnose 修正で発生、PR #12 で回収）。

### 実装委譲の癖
- Sonnet subagent は「背景実行を残して verdict 未報告のまま完了」しがち。委譲後は成果物（コミット有無・実験ログ）を必ず自分で確認し、未報告なら実験スクリプトを自分で回して verdict を取る。
- oracle（`codex exec -m gpt-5.5`）は数式導出・framing の de-risk に有効だった（閉形式 Fock 写像、#8 の scope 精密化、conftest 判断）。

## 5. Module map（更新）
states/2/3・forward/fit（1D）・forward2f/fit2f・forward3f/fit3f（full-cov 3-mode winner）・fock（Fock tools、cat2/cat3）・mle/mle2/mle3・data2/data3・**fock_project（splat→Fock ρ 閉形式射影 + psd_penalty/psd_report、#8）**・**fit.fit_psd（1モード full-param PSD polish）/ fit3f.fit3f_psd（3モード weight-only）/ fit3f.fit3f_shape_psd（3モード shape+weight、identify_stripes/apply_shape_knobs）**・experiments/01-08（08 = positivity）・conftest.py（BLAS pin）・AGENTS.md（pytest 運用ルール）。
