# Experiment 31 — Gate S′ prior-art survey: protocol (issue #137)

Status: adopted under orange's direction of 2026-08-03 ("proceed with
the natural next move", following the Gate T′ closure recorded on issue
#137). This protocol is written and committed **before** any search is
executed; the survey scope, query families, classification scheme, and
decision rules below are fixed here. Findings will live only in
`findings.md` (written after execution), whose §Classification table is
the **sole authoring location** for per-topic prior-art classifications.
This protocol contains no findings and cites no source with a content
claim.

## 0. What this survey can and cannot establish

A literature survey supports only **scope-bounded** statements: "within
the declared search scope, executed on the recorded date, prior art
covering topic X was / was not found". It can never establish novelty
absolutely. Whether Gate S′ closes, and what novelty-adjacent language
(if any) becomes available, is **orange's decision** on the survey
report; this survey proposes classifications and drafts candidate
language, nothing more. The repo-wide prohibition on novelty claims
stays in force throughout the survey and after it, until orange decides
otherwise.

Epistemic rules, fixed here:

- A content claim about a source ("paper P shows Y") may be recorded
  only if the cited text (at minimum the abstract; where load-bearing,
  the relevant section) was actually retrieved and read during this
  survey. Assistant background knowledge is NOT a permitted source —
  several of the K_ε note's §9 references postdate the assistant's
  knowledge cutoff, so everything is re-retrieved live.
- Negative results name the queries that produced them (a "not found"
  is meaningless without its scope).
- Search-engine coverage is imperfect and this is recorded as a
  standing limitation in the findings; no classification is stronger
  than the engines and dates behind it.

## 1. Surveyed claim topics

The topics below name the program's claim clusters by pointer (their
statements and statuses live only in the respective claim tables; this
survey does not restate or re-judge them — it asks only what the
literature already contains). The novelty-relevant composite is T2; the
others exist to locate the nearest neighboring literatures precisely.

- **T1** — two-mode stellar/Husimi/Bargmann zero sets intersected with
  a 3-sphere as links; census invariants (component count, core
  windings, linking matrix) for coherent / pure-Gaussian superpositions
  (exp24 claim table).
- **T2** — linking/knotting of phase-space zero sets used as an
  **obstruction to approximation by restricted dictionaries at fixed
  term budget** (the "topological K–ε obstruction": exp24 P3/P6-style
  statements plus the exp25 measured program).
- **T3** — quantitative isotopy stability of the zero link inside a
  fidelity ball, with explicit constants (exp28 claim table).
- **T4** — certified margins for a specific torus-knot target and a
  winding bound blocking it for a Gaussian dictionary at small budget
  (exp29 claim table).
- **T5** — the common-quadratic (common-squeezing) division dichotomy
  in two modes (exp30 claim table; the one-mode mechanism is already in
  the in-repo K_ε note and is NOT surveyed as if it were new).
- **T6** — Gaussian-unitary invariants of stellar zero-set structure
  (exp26 claim table).

## 2. Search scope

**Literature families** (the exp24 §7 minimum, plus the adjacent
families known to be nearby):

- F1: singularity theory — links of plane-curve singularities, Milnor
  fibrations, torus knots from `w1^p + w2^q` (expected: classical
  mathematics; the survey records the standard references actually
  retrieved).
- F2: structured light / optical vortices — knotted and linked nodal
  lines of complex scalar fields, vortex knots, experimental knotting.
- F3: stellar formalism and stellar rank — zeros of
  Bargmann/Husimi/stellar functions, (approximate) stellar rank,
  Gaussian rank and its lower-bound techniques.
- F4: phase-space zero topology in quantum states beyond one mode —
  Majorana constellations, zero manifolds of multimode Husimi
  functions, topology of phase-space distributions.
- F5: topological obstructions / invariants in quantum-state
  approximation and non-Gaussianity witnesses.
- F6: knotted structures in quantum wavefunctions and fields
  (nodal-line knots in wavefunctions, hopfions/skyrmions in optics and
  condensed matter) — the nearest physics neighborhood of T1.

**Engines and sources**: web search (general engine), arXiv listings
and abstract pages, publisher abstract pages where surfaced. Retrieval
via the session's search/fetch tools; every cited item records its
retrieval date (2026-08-03 unless noted) and locator (arXiv ID, DOI, or
URL).

**Query families** (declared; execution may add spelling variants and
follow references OUT of retrieved items, recorded as "citation-chase"
entries; it may not add new thematic families without a dated protocol
amendment):

- Q1 (F1): "Milnor fibration torus knot", "link of singularity w^p +
  w^q", "algebraic link 3-sphere".
- Q2 (F2): "optical vortex knot", "knotted nodal lines light",
  "linked vortex lines laser".
- Q3 (F3): "stellar rank", "stellar representation non-Gaussian",
  "approximate stellar rank", "Gaussian rank lower bound", "Bargmann
  function zeros quantum".
- Q4 (F4): "Husimi function zeros topology", "Majorana constellation
  two-mode", "phase space zeros multimode", "Husimi zero set
  manifold".
- Q5 (F5): "topological obstruction Gaussian approximation",
  "non-Gaussianity witness zeros", "topological invariant quantum
  state approximation".
- Q6 (F6): "knotted nodal lines quantum wavefunction", "hopfion
  optical field", "knots quantum optics phase space".
- Q7 (T2-specific composites): "linking number obstruction
  approximation", "knot invariant state approximation bound",
  "topological lower bound superposition rank".

**Stopping rule**: per query family, the first two result pages (or the
engine's returned set if smaller) are triaged by title/snippet;
items triaged as possibly relevant to any T-topic get their abstract
retrieved; an item whose abstract leaves a T2/T3/T4/T5 coverage
question open gets a deeper read of the relevant section. Citation
chases go one hop from retrieved items. The survey records every
triaged-in item and every abstract retrieved (including ones dismissed
after reading, with the dismissal reason).

## 3. Classification scheme (per topic, authored only in findings.md)

- **P (prior art)** — retrieved sources cover the topic's substance;
  the affected repo claims must then be presented as reproductions /
  applications, and any surface suggesting otherwise gets a correction
  便 (this is an outcome, not a halt; the correction list becomes part
  of the report).
- **A (adjacent)** — retrieved sources are near neighbors but a stated,
  checkable distinction separates them from the topic's substance; the
  distinction is recorded next to each cited source.
- **N (not found in scope)** — no retrieved source covers the topic's
  substance; the classification names the query families behind it.

## 4. Deliverables and process

1. This protocol (committed before any search).
2. `findings.md` — per-family retrieval log (item, locator, retrieval
   date, triage outcome, content notes only for read items) and the
   §Classification table (sole authoring location; one row per T-topic:
   classification, load-bearing citations, distinction notes).
3. A research-log pointer entry (no classification restatement).
4. Draft PR (base: dev), report-only independent review, stop pending
   verdict; Gate S′ close and any language decision are orange's.

## 5. Falsification / integrity conditions

- **G1**: a content claim about an unretrieved source, or a citation
  that cannot be re-resolved from its recorded locator, is a defect:
  the entry is struck and the incident recorded.
- **G2**: if execution needs a thematic family beyond F1–F6, the
  protocol gets a dated amendment BEFORE that family is searched.
- **G3**: a P-classification on T2–T5 triggers the correction-便 duty
  of §3 for every affected surface (tracked in the report).
