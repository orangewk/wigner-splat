# Agent provenance 再発明評価

- 状態: done（再発明評価と旧pilot停止の記録）
- 評価日: 2026-08-02
- 処置指示者: orange（private task instruction。GitHub投稿者identityだけでは本人性を証明しない）
- 後継設計の採否: proposed / pending
- GitHub側の停止記録: [Issue #146 comment](https://github.com/orangewk/wigner-splat/issues/146#issuecomment-5154361100)
- GitHub側の設計状態: [Issue #152 comment](https://github.com/orangewk/wigner-splat/issues/152#issuecomment-5154360704)（`DesignReviewPending`）
- 再設計Issue: [#152](https://github.com/orangewk/wigner-splat/issues/152)
- 前段監査: [`2026-08-01-sebastian-drift-audit--done.md`](2026-08-01-sebastian-drift-audit--done.md)
- 評価対象: [Issue #143](https://github.com/orangewk/wigner-splat/issues/143)、[Issue #146](https://github.com/orangewk/wigner-splat/issues/146)、[PR #147](https://github.com/orangewk/wigner-splat/pull/147)

## 結論

GitHubが既に持つagent実行境界、write gate、run記録を、手書きYAMLと運用規則で再構成し始めていた。設計上の重複は大きい。ただし独自service、DB、checkerの実装前に発見しており、コード上のsunk costは小さい。

この文書の`done`は、再発明評価を記録し、手書きprovenance pilotのTask 2 / 3を停止したことだけを表す。gh-awまたは後継設計を採用したという意味ではない。private task instructionは処置の由来として記録するが、第三者がGitHubだけからorange本人の承認を検証できるprimary decision URLは存在しない。この限界を埋めるための自己申告フィールドは追加しない。

セバスチャン監査、科学研究固有のauthority matrix、`verification` / `validation` / `decision`の区別、`agmsg`のlocal配送用途は再発明ではない。今後はGitHub-native control planeと科学policyを分離する。

## 重複していた部分

現行設計はactorとrun、委譲経路、exact SHAとartifact scope、author / reviewer / decision ownerの分離、stale review、cloud runnerの成果提出、task状態遷移、GitHub writeの前段gateを手動recordで表現した。

[GitHub Agentic Workflows](https://github.github.com/gh-aw/)はCopilot、Claude Code、Codex、Gemini等をGitHub Actions内で動かし、agentへread-only tokenを渡し、secretを隔離し、writeを[Safe Outputs](https://github.github.com/gh-aw/reference/safe-outputs/)の別jobへ分離する。許可operation、件数、対象file、review eventをpolicyで制限できる。agent execution、GitHub mutation、run auditの基盤をproject側で再実装しない。

GitHub Copilot cloud agentは、agent author、task開始者のco-author、verified commit、session logへのlinkをGitHub上に残す。[Managing agent sessions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents)で追跡できる。第三者engineで同等の情報が残るかはpilotで実測する。

## 再発明ではなかった部分

### セバスチャン監査

自己検収、誤検算の伝播、reviewer結果の再裁定、brief作成とacceptance判定の集中は実際のfailureである。基盤をGitHub-nativeへ移しても責務分離の必要性は消えない。

### 科学的authority

GitHubは、reviewerがspec作成者から科学的に独立しているか、再現確認と科学的妥当性確認の違い、計算経路の独立性、HOLD解除に必要な証拠、研究路線や公開claimのdecision ownerを判定しない。これらはproject policyとして残す。

### agmsg

`agmsg`はユーザーglobalなlocal配送路として残す。task URL、SHA、run ref、request / status / receiptを配送し、GitHubが保持するactor情報やclaim本文を複写しない。

## pilotの到達点と限界

Issue #143は、legacy recordからtaskとcommitは復元できるが、actor ancestry、review対象bytes、decision主体は復元できないことを示した。この診断は有効である。

PR #147は、正直なrunnerがactivity stampを記録すれば作業関係を読めることを示した。しかしGitHub上のauthor、review comment投稿者、decision記録者はすべて`orangewk`であり、Lunaの結果は正式なGitHub reviewではなくcommentへの転記だった。authorizationやpersonhoodの証明ではない。

現行文書もactivity stampを敵対的ななりすましに対するsecurity boundaryとしていなかったため、虚偽の達成ではない。ただし保証に対して記録量が大きく、Task 2 / 3を同じ方法で反復する価値は低い。

## 調査上の失敗

A2A、Ably、Entra Agent ID、SPIFFE等を調べた一方、durable recordとしてGitHubを選んだ時点で最も近いGitHub Agentic Workflows、Safe Outputs、Copilot session provenanceを先に評価しなかった。製品カテゴリの選び方が不適切だった。

## 処置

1. Issue #146 Task 2 / 3の手書きprovenance pilotを停止する（[GitHub側のcanonical pause record](https://github.com/orangewk/wigner-splat/issues/146#issuecomment-5154361100)）。
2. 独自schema、checker、identity service、relay、approval署名基盤を実装しない。
3. [Issue #152](https://github.com/orangewk/wigner-splat/issues/152)でGitHub-native capability mappingと低リスクpilotを行う。
4. GitHubが自動記録するfieldは手書きしない。
5. custom policyは科学的独立性とauthorityに限定する。
6. Public Previewのため、実測前に全面採用しない。

## 総括

重い車輪を設計し、手動模型を一周させた段階で既製基盤を発見した。監査と要件発見は残し、実行・来歴基盤はGitHub-nativeを第一候補として再設計する。
