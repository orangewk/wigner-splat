# Experiment 31 — Gate S′ prior-art survey: findings

Executed 2026-08-03 under the pre-committed `protocol.md` (`4fcac58`);
revised the same day after round 1 of the independent review (PR #168)
— every revision below carries a dated note. The §4 Classification
table below is the **sole authoring location** for per-topic prior-art
classifications; nothing outside its rows (in this file, the research
log, or the PR body) authors or restates a classification. Everything
else here is retrieval log, incident record, and limitations. No
novelty language is used or unlocked by this document; Gate S′
decisions are orange's on this report.

## 1. Execution record and incident record

- **Retrieval channel.** The session's web-search tool only. Direct
  page fetches were blocked by the environment's network policy at
  initial execution, and re-verified blocked during the round-1 fix
  (2026-08-03): the egress proxy denies CONNECT for every host probed
  — arxiv.org, export.arxiv.org, api.openalex.org, api.crossref.org,
  doi.org, quantum-journal.org, www.nature.com, link.springer.com,
  api.semanticscholar.org, inspirehep.net, www.osti.gov (HTTP 403 at
  the CONNECT stage in each case; a control fetch of example.com was
  denied identically, so the denial is policy-wide, not host-specific).
  Every content note below therefore reports what the search engine
  rendered from the cited page on 2026-08-03, not a first-hand read of
  the primary document.
- **G1 incident record (added 2026-08-03, round 1 of the PR #168
  review).** The initial version of this file framed the above as a
  "standing limitation" with a re-read recommendation. The round-1
  review correctly rejected that framing: protocol §0 pre-commits that
  a content claim about a source may be recorded only if at minimum
  its abstract (and, where load-bearing, the relevant section) was
  actually retrieved and read, and the project rules do not admit
  engine-rendered material as the source. Under that reading the §0
  condition was **not met** by any content note in §2, and G1 is
  treated as **fired** for this file as a whole: the incident is
  recorded here, the content notes below stand as *engine-tier,
  provisional* records (kept for auditability rather than struck
  individually), and the §4 rows are **provisional — not final — until
  every load-bearing citation is re-read from its primary source**
  (abstract at minimum; relevant section where load-bearing). A source
  that cannot be so re-read must then be removed from the load-bearing
  basis of its row. The primary-tier re-read requires an execution
  environment whose network policy permits fetching the scholarly
  hosts above; that environment change is orange's decision and is
  pending.
- **Locator caveat (round 1).** DOIs, ISBNs, and URLs recorded below
  were themselves surfaced by the search engine on 2026-08-03;
  in-session resolution of these locators could not be verified (same
  egress denial), so locator verification is part of the pending
  primary-tier re-read. The round-1 reviewer's independent environment
  did resolve arXiv:2607.04007, arXiv:2604.00766, and arXiv:2507.23468
  from their recorded locators.
- **Engine shape.** The engine returns one condensed result set per
  query (not paginated result pages); the protocol's "first two result
  pages" stopping rule was executed as: triage of the full returned
  set per query, with 1–2 query variants per family. Eleven queries
  were executed initially; the round-1 fix (same day) added three
  in-family variant queries (recorded under F3 in §2 — protocol §2
  permits spelling/variant additions within declared families) and a
  set of bibliographic locator lookups (§2a) that resolved locators
  for already-triaged items and triaged in no new thematic material.
- **Date.** All retrievals 2026-08-03. Several load-bearing items
  postdate the assistant's knowledge cutoff; nothing below relies on
  background knowledge (protocol §0).

## 2. Retrieval log (by family)

### F3 — stellar formalism and rank

Queries (initial): "stellar rank quantum optics zeros Bargmann
function non-Gaussian"; "arXiv 2404.07115 Gaussian rank quantum states
abstract chi decomposition". Queries (round-1 additions, Q3/Q5
variants, 2026-08-03): "common squeezing superposition of Gaussian
states approximation stellar function common quadratic factor";
"squeezed cat state approximation Gaussian rank lower bound shared
squeezing factor divides"; "two-mode squeezed superposition
approximation obstruction Gaussian dictionary common quadratic
dichotomy fidelity constant"; plus one item-directed abstract query
("Lower Bounds on Coherent State Rank Cottier Chabaud multimode core
states approximate coherent rank abstract").

- **arXiv:2607.04007** — "Stellar Braid Monodromy of Finite-Rank
  Non-Gaussian Photonic States", A. Coatanhay, A. Drémeau (announced
  2026-07; 42 pp). Engine-rendered abstract: for finite-stellar-rank
  states, after splitting off a zero-free Gaussian factor, the
  non-Gaussian structure sits in a finite stellar divisor; the paper
  introduces a **topological refinement of stellar rank for regular
  parameterized families** by tracking the motion of the divisor's
  zeros under deformations and recording the **braid monodromy** (the
  regular stratum is biholomorphic to an unordered configuration
  space; its fundamental group is the Artin braid group); concrete
  laboratories are finite-Fock families; the invariant is
  post-tomographic and complements scalar non-Gaussianity
  diagnostics. Content notes as rendered: zeros are a **finite point
  configuration** (single-variable divisor), the invariant is attached
  to **loops/families of states**, and no approximation bound,
  dictionary, or budget statement is mentioned. Retrieved via two
  targeted queries (the abstract text surfaced on the second). The
  round-1 review's independent primary check reports the paper
  restricts itself to pure single-mode states, finite stellar rank,
  and regular families, and excludes multimode zero varieties and
  isolated-state approximation obstructions from scope — consistent
  with this note; to be re-confirmed at the primary-tier re-read.
- **arXiv:1907.11009** — "Stellar representation of non-Gaussian
  quantum states" (Chabaud et al.): the stellar hierarchy; rank-`n`
  states need `n` creation operators plus Gaussian unitaries; finite
  rank iff finitely many Husimi zeros. (Also the in-repo note's
  foundation; triaged for completeness.)
- **arXiv:2410.23721** — "Assessing non-Gaussian quantum state
  conversion with the stellar rank" (Hahn, Garnier, Ferrini, Ferraro,
  Chabaud): approximate stellar rank, fidelity-ball template. In-repo
  reference of the K_ε note; retrieval confirms the bibliographic
  identity.
- **arXiv:2404.07115** — "Classical simulation and quantum resource
  theory of non-Gaussian optics", Hahn, Takagi, Ferrini, Yamasaki
  (Quantum 9, 1881 (2025)): resource-theoretic treatment, optimal
  decompositions for CV-computing states (the note's "HTFY" χ line).
- **arXiv:2604.00766** — "Lower Bounds on Coherent State Rank"
  (Cottier, Chabaud). Engine-rendered notes (initial query):
  approximate coherent-state rank; **analytical** lower bounds for
  squeezed states and finite Fock superpositions; no topological
  technique mentioned. *Round-1 addition (item-directed query,
  2026-08-03):* the engine-rendered abstract material further states
  the paper gives **lower bounds on the approximate coherent-state
  rank of multimode bosonic states, including finite superpositions of
  multimode core states** (alongside a single-mode
  low-rank-approximation technique) — i.e. its *outcome* overlaps the
  multimode approximate-rank territory even though its technique is
  analytic. Recorded so the corresponding §4 distinction reflects the
  outcome overlap, not only the technique difference. (The round-1
  review independently verified this against the primary abstract and
  relevant sections; to be re-confirmed at the primary-tier re-read.)
- **arXiv:2507.23468** — "On the complex zeros of the wavefunction",
  Cerf, Wassner, Davis, Arzani, Chabaud: holomorphic extension of the
  (single-variable) position wavefunction, a Hudson-type theorem,
  Gaussian dynamics as classical motion of the zeros,
  single-quadrature non-Gaussianity detection. One variable; no links;
  no dictionary obstruction mentioned.
- **arXiv:2605.25862** — "Bargmann Zeros as a Diagnostic of the
  Tunneling Transition in Double-Well Quantum Systems": dynamical
  diagnostic use of (one-mode) Bargmann zeros. Triaged; not deepened
  (no topology-as-obstruction content in the rendered material).
- **arXiv:2504.10455** — "The stellar decomposition of Gaussian
  quantum states": surfaced during the HTFY query; triaged as
  F3-relevant bibliography, not deepened.
- **arXiv:2607.02427** — "Optimal stellar rank approximation of
  squeezed cat states with photon catalysis" (Nauth, Walk, Datta,
  Busch, Eisert, Benson, Kögler; announced 2026-07). *Round-1
  addition:* triaged in by the round-1 variant queries as directly
  relevant to the exp30 topic pointer (T5). Engine-rendered notes:
  photon catalysis between low-number Fock states and squeezed states
  generates squeezed coherent-state superpositions; the stellar-rank
  formalism characterizes the non-Gaussian complexity of inputs and
  outputs; cat states are approximated by squeezing a finite Fock
  superposition; and **the stellar fidelity for approximating squeezed
  cat states is invariant under the squeezing operator and thus
  independent of the cat squeezing** — a one-mode statement that
  approximation fidelity is unchanged by a squeezing factor common to
  target and ansatz. One mode; no two-mode statement and no
  common-vs-varying dichotomy in the rendered material.
- *Round-1 variant queries also surfaced, triaged and not deepened:*
  **arXiv:2506.17437** ("Nonlinear squeezing of superpositions of
  quadrature eigenstates" — witness/measure line) and
  **arXiv:2603.15258** ("Gaussian superpositions for bosonic
  encodings" — encodings built from Gaussian superpositions;
  pure-Gaussian fidelity via first and second moments). The two-mode
  composite variant query returned no source treating a
  common-vs-varying quadratic dichotomy or a dictionary-obstruction
  statement for two-mode superpositions (nearest returns: a two-mode
  coherent-superposed teleportation channel, arXiv:2607.01786, and the
  encodings item above).

### F1 — singularity theory (query: "Milnor singular points complex
hypersurfaces link of singularity torus knot Brauner algebraic link
classification")

- **Milnor, "Singular Points of Complex Hypersurfaces"**, Annals of
  Mathematics Studies 61, Princeton University Press, 1968. Locators
  (round 1, engine-surfaced from the publisher's and bibliographic
  pages): ISBN 9780691080659 (print); ISBN 9781400881819 (publisher
  e-edition,
  `press.princeton.edu/books/ebook/9781400881819/singular-points-of-complex-hypersurfaces-am-61-volume-61`).
- **Brauner, "Zur Geometrie der Funktionen zweier komplexer
  Veränderlicher" (II: Das Verhalten der Funktionen in der Umgebung
  ihrer Verzweigungsstellen)**, Abh. Math. Sem. Univ. Hamburg 6, 1–55
  (1928). Locator (round 1, engine-surfaced from the Springer journal
  page): doi:10.1007/BF02940600.
- **Manifold Atlas, "Links of singular points of complex
  hypersurfaces"** — URL locator (round 1):
  `http://www.map.mpim-bonn.mpg.de/Links_of_singular_points_of_complex_hypersurfaces`.
  The engine-rendered chase origin for both items above: links of
  plane-curve singularities; torus links as links of `x^p + y^q = 0`;
  algebraic links are iterated torus cables. Classical mathematics, as
  expected by exp24 §7: the trefoil-from-`w1^2, w2^3` mechanism the
  repo uses is **standard**.
- **arXiv:1611.02563** — "Knotted fields and explicit fibrations for
  lemniscate knots": Milnor-style explicit constructions bridging F1
  and F2. Triaged.

### F2 — optical vortex knots (queries: "knotted vortex lines optical
fields Leach Dennis Padgett isolated optical vortex knots nodal
lines"; "stability robustness knotted nodal lines perturbation optical
vortex knot structural stability quantitative bound")

- **Dennis, King, Jack, O'Holleran, Padgett, "Isolated optical vortex
  knots"**, Nature Physics 6, 118–121 (2010); doi:10.1038/nphys1504
  (locator round 1): knotted/linked zero (vortex) lines engineered in
  laser beams; algebraic-topology-based design with braided zeros
  embedded into propagating beams.
- **Leach, Dennis, Courtial, Padgett, "Vortex knots in light"**, New
  J. Phys. 7, 55 (2005); arXiv:physics/0411121;
  doi:10.1088/1367-2630/7/1/055. *Correction (round 1, 2026-08-03):*
  the initial log lumped this as a "Berry–Dennis line ('Vortex knots
  in light', physics/0411121 and successors)" — an item-level
  miscitation: physics/0411121 is the Leach et al. paper, whose
  engine-rendered description says its vortex loop/link/knot
  constructions follow the theoretical model of Berry and Dennis. The
  Berry–Dennis theory papers themselves were not separately retrieved
  and are therefore not cited as items here; the attribution reaches
  them through this paper's own rendered description.
- Stability neighborhood — itemized in round 1 (previously one grouped
  citation, which was unauditable):
  - **Pires, Tsvetkov, Barati Sedeh, Chandra, Litchinitser,
    "Stability of optical knots in atmospheric turbulence"**, Nat.
    Commun. 16, 3001 (2025); doi:10.1038/s41467-025-57827-1.
    Engine-rendered: the knots' topological invariant is preserved in
    the weak-turbulence regime and can fail to be conserved under
    stronger turbulence despite their topological nature, with
    transitions occurring through reconnection events.
  - **Annala, Zamora-Zamora, Möttönen, "Topologically protected
    vortex knots and links"**, Commun. Phys. 5, 309 (2022);
    doi:10.1038/s42005-022-01071-2; arXiv:2204.03612. *Correction
    (round 1):* the initial grouped note described the whole trio as
    "experimental/qualitative"; the engine-rendered description of
    this item is **theoretical** — knots/links of non-Abelian vortices
    (Bose–Einstein condensates, liquid crystals) that cannot be
    dissolved by local reconnections and strand crossings — a
    protection mechanism, not a fidelity-ball statement.
  - **"High capacity topological coding based on nested vortex knots
    and links"**, Nat. Commun. 13 (2022);
    doi:10.1038/s41467-022-30381-w. Engine-rendered: designed nested
    vortex knots/links used for high-capacity coding. (The engine did
    not render the author list; the DOI is the locator.)
  - In none of the three does the rendered material state a
    fidelity-ball / explicit-constant isotopy theorem for phase-space
    zero sets.

### F4 — phase-space zero topology beyond one mode (queries: "two-mode
Husimi function zero set link 3-sphere Hopf link quantum state
topology"; "Majorana constellation stellar representation topology
multimode phase space zeros invariant")

- **arXiv:2605.15008** — "Majorana Constellations: A Geometric Lens on
  Multipartite Entanglement and Geometric Phases": spin-system Husimi
  zeros as **point constellations on S²**; entanglement measures and
  geometric phases from constellation geometry. Finite point sets on a
  2-sphere, not curves/links in `S^3`; no approximation-budget
  statement in the rendered material.
- **arXiv:1101.3564** — "Entangled topological features of light":
  vortex Hopf links in modal superpositions of light (real space).
  Triaged.
- The two-mode query returned **no** source treating zero sets of
  two-mode phase-space functions intersected with a 3-sphere as links.

### F6 — knotted quantum wavefunctions (query: "Berry knotted zeros
quantum states hydrogen nodal lines wavefunction knots")

- **Berry, "Knotted Zeros in the Quantum States of Hydrogen"**, Found.
  Phys. 31, 659–667 (2001); doi:10.1023/A:1017521126923 (locator
  round 1): torus-knotted nodal lines in superpositions of degenerate
  hydrogen eigenfunctions (real 3-space; explicit recipes; trefoil
  needs `n >= 7`).
- **arXiv:1904.07229** — Kauffman, Lomonaco, "Quantum knots and
  knotted zeros": every smooth knot arises as the zero set of some
  classifying map; realizations in hydrogen and harmonic-oscillator
  systems. Construction-oriented.
- **arXiv:2312.09619** — "Topological atom optics and beyond with
  knotted quantum wavefunctions" (BEC realizations). Triaged.

### F5 / T2-composites (queries: "topological obstruction approximation
quantum state Gaussian superposition rank lower bound linking number";
"linking number zeros Q function witness lower bound number Gaussian
terms multimode obstruction approximation"; "knot link invariant
phase-space zeros obstruction quantum state approximation stellar rank
topology")

- **arXiv:2111.02391** — "Topologically driven no-superposing theorem
  with a tight error bound" (Quantum, 2025): topology used for a no-go
  on superposing unknown states — different task; dismissed for T2
  with that reason.
- **arXiv:2305.10277** — "Quadratic Lower bounds on the Approximate
  Stabilizer Rank": discrete-variable analogue (stabilizer rank);
  non-topological techniques; dismissed for T2 (analogy only).
- The second composite query surfaced only signal-processing
  "Gaussian Q-function" material (dismissed: unrelated homonym); the
  third surfaced TQFT/knot-invariant material about entanglement and
  quantum computation (dismissed for T2: invariants OF knots computed
  BY quantum theories, not knot invariants of a state's phase-space
  zeros used to bound approximation). Across the three F5 queries, no
  returned source uses a link/knot invariant of a state's phase-space
  zero set as a lower bound or obstruction for approximation by a
  restricted dictionary at fixed term budget.

### 2a. Locator lookups (round 1, 2026-08-03)

Engine queries used solely to resolve bibliographic locators for
already-triaged items (no new thematic material; G2 untouched), listed
verbatim for auditability: "Brauner 1928 Abhandlungen mathematischen
Seminar Hamburg Geometrie Funktionen zweier komplexen Veränderlichen
doi"; "Milnor 'Singular Points of Complex Hypersurfaces' Annals of
Mathematics Studies 61 Princeton 1968 doi ISBN"; "Dennis King Jack
O'Holleran Padgett 'Isolated optical vortex knots' Nature Physics 2010
doi"; "Berry 'Knotted zeros in the quantum states of hydrogen'
Foundations of Physics 2001 doi"; "'Stability of optical knots'
atmospheric turbulence Nature Communications 2025 doi";
"'topologically protected' vortex knots links Communications Physics
2022 doi optical"; "Manifold Atlas algebraic link of singularity torus
knot iterated torus cables page"; "arXiv physics/0411121 Berry Dennis
knotted vortex light title"; "Manifold Atlas links of singularities
algebraic knots" (domain-restricted to `map.mpim-bonn.mpg.de`).

## 3. Citation-chase note

One-hop chases stayed within the families above: Brauner and Milnor
were reached from the Manifold Atlas page (URL locator in §2); the
Berry–Dennis attribution is carried inside the Leach et al. item's own
rendered description and was not chased to the theory papers (recorded
in §2). No new thematic family was needed; G2 was not triggered.

## 4. Classification table (sole authoring location)

*Status note (2026-08-03, added in round 1 of the PR #168 review):*
the rows below are **provisional** pending the primary-tier
re-verification required by the §1 incident record; until that
completes they support no outward-facing use. Round-1 revisions to
individual rows (one load-bearing basis substituted because protocol
§3 does not admit an in-repo pointer as load-bearing basis;
re-itemized citations; one extended distinction) are recorded in the
row cells themselves and in §2's dated notes.

| Topic | Classification | Load-bearing near neighbors (locators in §2) | Recorded distinction |
| --- | --- | --- | --- |
| T1 | A | 2607.04007; Dennis et al. 2010; Leach et al. 2005; Berry 2001 / 1904.07229; 2605.15008 | nearest works treat one-mode stellar zeros as point configurations (braid monodromy of families), real-space nodal lines of fields/wavefunctions (designed constructions), or S² point constellations; none treats two-mode stellar zero sets ∩ S³ as links with a census (components, windings, linking matrix) |
| T2 | A | 2604.00766; 2410.23721 / 2404.07115; 2111.02391; 2305.10277 | the rank-lower-bound line's technique is analytic (no topological technique in the rendered material) **and its outcome overlaps directly in the multimode territory** — 2604.00766 gives approximate coherent-state-rank lower bounds for multimode states, including finite superpositions of multimode core states (§2 round-1 note) — while no retrieved source uses link/knot invariants of phase-space zeros as a restricted-dictionary, fixed-budget approximation obstruction; the retrieved topological items address different tasks; any outward-facing distinction must state the outcome overlap, not only "analytic/non-topological" |
| T3 | A | Pires et al. 2025; Annala et al. 2022; nested-coding item (doi:10.1038/s41467-022-30381-w); 2607.04007 | retrieved stability work is either experimental robustness of designed real-space knots under turbulence or theoretical protection of non-Abelian vortex links against reconnection; neither is a fidelity-ball isotopy statement with explicit constants for phase-space zero links |
| T4 | A | Milnor 1968 / Brauner 1928; Berry 2001; 1611.02563 | torus-knot zero sets are classical and constructible in many systems; no retrieved source certifies margins for a torus-knot phase-space target against a Gaussian dictionary via a winding bound |
| T5 | A | 2607.02427 | the retrieved neighbor is one-mode: stellar approximation fidelity invariant under a squeezing operator common to target and ansatz (engine-rendered; §2 round-1 entry) — the nearest external statement of a common-factor mechanism; the two-mode common-vs-varying quadratic dichotomy with uniform transfer of certified constants (exp30's object) was not covered by any retrieved source (variant queries recorded in §2); the in-repo K_ε note's one-mode mechanism is context only and is no longer cited as load-bearing (round-1 revision) |
| T6 | A | 2607.04007 | nearest work is deformation monodromy of one-mode zero configurations; Gaussian-unitary invariance of multimode zero-set structure (exp26's object) is not covered in the rendered material |

Whether protocol G3's correction duty fires is read off the
Classification column above; it is not separately authored in prose
here or on any other surface.

## 5. What this supports (pointers only; nothing adopted here)

Candidate language for orange's Gate S′ decision is **generated from
the §4 table rather than authored here**: protocol §3 fixes, per
classification value, the statement form a row supports, and protocol
§0 fixes the scope-bounded template (declared scope, engines,
retrieval dates, and — since round 1 — the §1 incident record and its
pending resolution as explicit conditions). Substituting a §4 row into
those forms yields that topic's candidate sentence; this document
deliberately performs no substitution, and no such sentence is adopted
anywhere by this survey. The survey equally records attribution
duties: the §2 content notes for F1, F2, and F3 name the works (with
locators) that any outward-facing text should cite and distinguish per
the corresponding §4 rows.

Everything above is additionally conditional on the §1 incident's
resolution: until the primary-tier re-read completes, the §4 rows are
provisional and support no outward-facing language at all.
