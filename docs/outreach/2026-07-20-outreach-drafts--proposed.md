# アウトリーチ文面ドラフト(#70)— 全件 orange 承認待ち、送信禁止

状態: proposed。**この文書の存在は送信許可を意味しない。** 宛先ごとに
orange の明示承認(宛先・文面・送信経路)を得てから送る。送信記録は
issue #70 にコメントで残す。

差出人名義: Wataru Kawashima(ORCID 0009-0002-7713-5547)。
共通リンク: preprint doi:10.5281/zenodo.21457049 / repo
https://github.com/orangewk/wigner-splat

方針: 過大主張なし(README と同じ規律)。各通とも「なぜあなたに」を
1 文で明示。長さは 120–250 語(読了 1 分)。返信がなくても失うものは
ない設計(具体的で小さい ask を 1 つだけ)。

---

## 1. Konno / Asavanant / Furusawa グループ(GKP データ所有者)

目的: データ利用の報告と謝意(礼儀として最優先)+ held-out セッションの
有無を尋ねる(#41 の preregistered confirmation への最短路)。

Subject: Your public GKP homodyne dataset — a reanalysis, with thanks

> Dear Dr. Konno and colleagues,
>
> I am writing to thank you for making the raw homodyne data from your
> Science 2024 propagating-light GKP work publicly available on Dryad.
> I have used it as the real-data benchmark in a small research project
> on compact, physically constrained tomography models, and it is the
> only public raw homodyne dataset my survey could find — its existence
> materially changed what the project could test.
>
> The result that may interest you: a rank-4 mixture of displaced,
> squeezed Gaussian kets (ρ = BB†, 92 real parameters) matches a
> full-rank MLE frontier (255 parameters) at confidence-interval
> resolution on held-out per-sample likelihood on your data. The
> analysis is exploratory (data splits reuse the same observations),
> and the preprint states its limits explicitly:
> https://doi.org/10.5281/zenodo.21457049 (code and full research log:
> https://github.com/orangewk/wigner-splat).
>
> One question, if it is not too much trouble: do additional measurement
> sessions of the same or similar states exist that could serve as a
> genuinely held-out set? A preregistered confirmation on fresh data is
> the natural next step for this line, and your group is the shortest
> path to it. Any guidance — including "no" — would be appreciated.
>
> With thanks and best regards,
> Wataru Kawashima (independent researcher; ORCID 0009-0002-7713-5547)

## 2. I. Strandberg(最近接の方法論)

目的: 技術フィードバック依頼(+ 将来の arXiv endorsement の種)。

Subject: Physically constrained homodyne tomography — a small preprint you may find familiar

> Dear Dr. Strandberg,
>
> Your 2022 paper on simple, reliable continuous-variable tomography
> with convex optimization is the closest methodological neighbor to a
> small project I have just written up, so I wanted to share it with
> you directly.
>
> The project fits finite mixtures of displaced, squeezed Gaussian kets
> (ρ = BB†, PSD by construction) by per-sample homodyne likelihood with
> closed-form gradients, composed with physical loss channels. On the
> public GKP dataset of Konno et al. it ties a full-rank MLE frontier at
> CI resolution with ~1/3 the parameters; on a synthetic thermal target
> it records one instance of blind held-out performance above a
> full-rank MLE run under a pre-declared 900-second baseline budget, on
> a target provably outside the model family — the
> preprint is deliberately explicit about scope limits and negative
> results: https://doi.org/10.5281/zenodo.21457049
> (code: https://github.com/orangewk/wigner-splat).
>
> If you have 15 minutes for it, the single question I would most value
> your view on: does the non-inclusion argument in §3.3 (no detection
> efficiency and no finite rank reproduces the thermal target) look
> sound to you, and is it stated at the right strength?
>
> Best regards,
> Wataru Kawashima (independent researcher; ORCID 0009-0002-7713-5547)

## 3. Gaikwad / Kockum グループ(gradient-descent tomography)

目的: 隣接ラインへの共有 + ベンチマーク観点のフィードバック。

Subject: Gradient-based physical tomography — an adjacent preprint

> Dear Dr. Gaikwad and colleagues,
>
> Your recent Quantum Science and Technology paper on gradient-descent
> quantum state tomography is directly adjacent to a project I have
> just released, so I wanted to share it.
>
> It takes the physically-constrained-optimization route in the
> continuous-variable setting: finite mixtures of displaced, squeezed
> Gaussian kets (ρ = BB†), per-sample homodyne likelihood, closed-form
> gradients, physical loss channels. Results on the public GKP dataset
> of Konno et al. and on a synthetic out-of-family gate are in the
> preprint, with scope limits stated inline:
> https://doi.org/10.5281/zenodo.21457049
> (code: https://github.com/orangewk/wigner-splat).
>
> If anything there is useful to your benchmarking — or if you see a
> comparison we should run against your methods — I would be glad to
> hear it.
>
> Best regards,
> Wataru Kawashima (independent researcher; ORCID 0009-0002-7713-5547)

## 4. R2-Gaussian / X²-Gaussian 著者(Zha / Yu ら)

目的: 系譜への報告(彼らの機構を量子逆問題に移植した話)。CV 業界なので
トーンをやや軽く。

Subject: Your Gaussian-splatting tomography, ported to quantum state reconstruction

> Dear authors of R2-Gaussian and X²-Gaussian,
>
> A note of appreciation from an unexpected direction: your
> differentiable Radon splatting line was the starting point of a
> project that applies the same idea to quantum homodyne tomography —
> where a camera view becomes a local-oscillator phase and the rendered
> projection becomes a measured quadrature histogram, and where Gaussian
> mixtures must carry *signed* weights to express Wigner negativity.
>
> The signed-splat track and its limits (a signed mixture is not a
> quantum state; we document where that fails), plus a physically
> constrained successor model, are written up here:
> https://doi.org/10.5281/zenodo.21457049
> (code: https://github.com/orangewk/wigner-splat).
>
> No ask beyond sharing it — the lineage section credits your work, and
> I thought you might enjoy seeing the mechanism in a different physics.
>
> Best regards,
> Wataru Kawashima (independent researcher; ORCID 0009-0002-7713-5547)

## 5. Tosca / Ciuti グループ(multi-Gaussian phase-space)

目的: Gaussian 表現系譜への共有 + 表現論の観点のフィードバック。

Subject: Multi-Gaussian representations meet homodyne tomography — a short preprint

> Dear Dr. Tosca and colleagues,
>
> Your work on variational multi-Gaussian phase-space dynamics is part
> of the lineage of a small tomography project I have just released,
> and one discussion point in it may interest you specifically: the
> number of Gaussian components a state needs (in a signed mixture or a
> BB† ket mixture) as a possible continuous-variable analogue of
> stabilizer rank. It is flagged as speculative — one paragraph, no
> results claimed — but your group is among the few who would have an
> informed opinion on whether it is worth developing.
>
> The preprint (with the empirical results on public GKP homodyne data
> that motivate the question):
> https://doi.org/10.5281/zenodo.21457049
> (code: https://github.com/orangewk/wigner-splat).
>
> Best regards,
> Wataru Kawashima (independent researcher; ORCID 0009-0002-7713-5547)

---

## 送信メモ(承認後に確定)

- 宛先アドレスは各論文の corresponding author 欄から取得(この文書には
  記載しない — 公開リポジトリのため)
- 送信経路: orange のメールアカウントから手動送信を推奨(なりすまし
  回避・返信の受け口)
- 順序推奨: 1(Konno、礼儀)→ 2(Strandberg、最近接)→ 3–5 は同時で可
- 各送信後、issue #70 に「宛先(所属のみ)・日付・文面 rev」を記録
