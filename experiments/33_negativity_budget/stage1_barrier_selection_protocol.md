# 負性予算 sweep Stage 1 barrier-selection packet

状態: **global train-only coefficient selection / pre-data-values**

Issue: #140

依存: Stage 1 candidate cellとfixed-schedule candidate runner。

本packetはbarrier係数の候補と選択規則を、GKP quadrature値を読む前に固定する。
一つの係数を全beta・全reshuffleで共有する。beta/seed/reshuffle cellの構築、artifact、
test評価、Stage 2 beta選択、科学的判定は扱わない。

## 1. authoring locationと候補

barrier係数候補、admissibility、選択規則、返却interfaceは本文書を唯一のauthoring
locationとする。objectiveと単一candidate runは既存protocolを参照し、再定義しない。

| 項目 | 固定値 / 意味 |
| --- | --- |
| 候補lambda | `0`と`10^k (k = -1, ..., 12)`（昇順） |
| 入力 | orchestration packetが返すcanonical 30-cell列 |
| schedule | 各setup・各lambdaで既存の100 accepted-step runner |
| 共有範囲 | 入力された全cellに一つのglobal lambda |

`beta = 0`のexp18一致検算は後続orchestrationの責任であり、係数選択へ混ぜない。
selectorは同じcell/setup objectを全lambdaで再利用し、lambdaごとの再初期化やdata差し替えを
許さない。入力cell identityとsetup objectの重複、およびcanonical 30-cell集合・順序との差を
拒否する。実験で使う集合と順序は`stage1_orchestration_protocol.md`を参照し、本protocolで
再定義しない。

各lambdaについて入力された全setupを入力順に実行してから次のlambdaへ進む。最初の隣接
global-admissible pairが揃った時点で停止し、それより大きい候補は実行しない。候補範囲を
データ閲覧後に拡張しない。`10^12`までに選択不能ならtestを読まず、新しいreviewed
protocolを発行する。

## 2. terminal grid diagnostic

各runの最後にcommitされたstateを、setupが所有するtrain由来gridで再評価する。

- 全grid densityの有限性
- strict nonpositive点数（`p <= 0`、toleranceなし）
- nonfinite点数
- finite点があればその最小density
- runner status、terminal train NLL、terminal eta

clip、floor、許容差による符号変更を行わない。runがdeclared numerical stopを返した場合も
最後のcommit stateを診断するが、admissibleにはしない。予期しない例外はstatusへ丸めず
伝播する。

一つのcell/lambda assessmentがadmissibleである条件は、runner statusが`completed`で、
nonpositive点とnonfinite点がともに0であること。lambda全体のadmissibilityは、入力された
**全cell**のassessmentがadmissibleであること。

## 3. global selection

候補を昇順に隣接pairとして走査し、両方がglobal-admissibleである最初のpairの下端を選ぶ。
上側の一点は次の宣言候補でもgrid positivityが再現することの感度確認である。正の下端では
一桁強い係数、下端`0`では最初の正のcontrolに相当する。

例: `1`と`10`が最初のadmissible pairなら選択値は`1`。単独でadmissibleな候補や、最後の
`10^12`だけがadmissibleな場合は選ばない。該当pairがなければstatus
`no_stable_admissible_pair`、selected weightは`None`とし、test評価前に停止する。

train NLLとetaは診断として残すが選択条件に使わない。係数をfitの良さへ合わせず、completion
とstrict grid positivityだけで決める。per-beta / per-reshuffleの別係数は返さない。

## 4. result interface

`Stage1BarrierSelection`は実行済みprefixの全assessment、status、selected weightを返す。
assessment順はlambda昇順、その中でcell入力順とする。各assessmentはsetupの入力順、cell
identity（dataset、reshuffle、beta、init seed）、lambda、candidate run、grid点数、invalid点数、
最小densityを持つ。attempted weights、admissibility、global-admissible weightsは保存値でなく
保持dataから計算する。

各assessmentはcell identityを保持し、`Stage1CandidateRun`のcell identityおよび呼出し時の
barrier weightが自身のidentity/lambdaと一致することをresult境界で検査する。これによりrunと
別cellまたは別lambdaの誤結合を拒否する。本packetはin-memory selectionまでを扱い、artifactへの
変換は後続packetで別に固定する。

resultはin-memory recordであり、artifact schema、test metric、invalid-rate verdict、Stage 2
beta点、解釈文を持たない。

## 5. gates

1. 候補列が固定15点で、各候補について全setupを実行し、最初のstable pairで停止する。
2. 同一cell/setup objectを候補間で再利用し、空入力・`beta = 0`・identity/object重複を拒否する。
3. nonpositiveとnonfinite densityを別々に数え、strict positivityだけをadmissibleにする。
4. numerical stopはgridが正でもadmissibleにしない。
5. 全cellに共通する最初の隣接admissible pairの下端だけを選ぶ。
6. 孤立点または`10^12`までpairなしではselected weightを返さない。
7. resultへtest data、artifact、Stage 2選択、科学的verdictが混入しない。

## 6. implementation choice

一般のconstrained optimizerへの置換は、本issueが固定したexp18-aligned optimizerを変更する。
このpacketは既存optimizerを保ち、train-onlyの係数感度を明示的に測る。

- SciPy `trust-constr`: <https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustconstr.html>
- NLopt augmented Lagrangian: <https://nlopt.readthedocs.io/en/stable/NLopt_Algorithms/>
- JAXopt constrained optimization: <https://jaxopt.github.io/stable/constrained.html>
- Optax backtracking line search: <https://optax.readthedocs.io/en/latest/api/generated/optax.scale_by_backtracking_linesearch.html>
