# Zenodo 投稿メタデータ(準備稿 — orange が投稿フォームに貼る用)

- **Upload type**: Publication → Preprint
- **Title**: Compact physical Gaussian-ket models for homodyne quantum-state tomography
- **Authors**: orangewk
- **Description** (アブストラクトをそのまま):
  Continuous-variable quantum-state tomography usually reconstructs a truncated
  Fock-basis density matrix. We study a compact alternative: finite mixtures of
  displaced, squeezed Gaussian kets whose ρ = BB† construction is positive
  semidefinite by construction, fitted by per-sample homodyne likelihood with
  closed-form gradients, and composed with physical loss and noise channels. On
  the public propagating-light GKP dataset of Konno et al. (Science 2024), a
  rank-4 model with 92 real parameters matches the empirical full-rank
  maximum-likelihood frontier (255 parameters) at confidence-interval resolution
  on held-out likelihood. On a synthetic thermal-noise target that we prove lies
  outside the model family — no detection efficiency and no finite rank
  reproduces it exactly — the channel-composed model fitted blind exceeds a
  full-rank MLE run under the pre-declared 900-second baseline budget, a verdict
  that holds across all five pre-declared seed and noise configurations. We do
  not claim a universally superior method: comparisons on real data reuse
  observations across splits, the strongest baseline is test-selected, and the
  blind result covers one target class. The contribution is a compact,
  physically constrained model family together with a fully falsification-first
  research record — negative results, superseded scorings, and pre-declared
  protocols are all preserved in the accompanying repository.
- **License**: CC-BY-4.0 (本文 PDF。コードは repo 側 MIT のまま — 別物なので混同しない)
- **Keywords**: continuous-variable quantum tomography; homodyne tomography;
  Wigner function; Gaussian representations; quantum optics; Gaussian splatting;
  GKP states
- **Related identifiers**:
  - `is supplemented by` → https://github.com/orangewk/wigner-splat (repository)
  - `is supplemented by` → doi:10.5281/zenodo.21387212 (archived software release v0.1.0)
  - `cites` → doi:10.5061/dryad.t76hdr86j (Konno et al. GKP dataset)
- **Communities**: (任意) quantum-physics 系があれば
- **Notes 欄**: AI assistance statement は PDF の Acknowledgements に記載済み

手順: zenodo.org → Upload → New upload → 上記を転記 → preprint.pdf を添付 →
Publish。発行された DOI を README / #69 / #70(アウトリーチ文面)に反映する。
