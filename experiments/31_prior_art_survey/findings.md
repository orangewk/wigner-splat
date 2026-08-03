# Experiment 31 — Gate S′ prior-art survey: findings

Executed 2026-08-03 under the pre-committed `protocol.md` (`4fcac58`).
The §4 Classification table below is the **sole authoring location** for
per-topic prior-art classifications. Everything else here is retrieval
log and limitations. No novelty language is used or unlocked by this
document; Gate S′ decisions are orange's on this report.

## 1. Execution record and limitations

- **Retrieval channel.** The session's web-search tool only. Direct
  page fetches (arXiv abstract pages, `export.arxiv.org`, the
  Semantic Scholar API) were **blocked by the environment's network
  policy** — the egress proxy answered 403 to CONNECT for those hosts
  (denial logged by the proxy status endpoint during execution). Every
  content note below therefore reports what the search engine rendered
  from the cited page on 2026-08-03, not a first-hand read of the
  primary document. This weakens the evidence tier of each content
  note one step below the protocol's ideal (§0), and is recorded here
  as a standing limitation: before any outward-facing use of a
  load-bearing content claim, the primary source should be re-read
  through an unrestricted channel.
- **Engine shape.** The engine returns one condensed result set per
  query (not paginated result pages); the protocol's "first two result
  pages" stopping rule was executed as: triage of the full returned
  set per query, with 1–2 query variants per family. Eleven queries
  were executed in total (listed per family below, verbatim).
- **Date.** All retrievals 2026-08-03. Several load-bearing items
  postdate the assistant's knowledge cutoff; nothing below relies on
  background knowledge (protocol §0).

## 2. Retrieval log (by family)

### F3 — stellar formalism and rank (queries: "stellar rank quantum
optics zeros Bargmann function non-Gaussian"; "arXiv 2404.07115
Gaussian rank quantum states abstract chi decomposition")

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
  targeted queries (the abstract text surfaced on the second).
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
  (the note's Cottier–Chabaud line): approximate coherent-state rank;
  **analytical** lower bounds for squeezed states and finite Fock
  superpositions. Engine notes mention no topological technique.
- **arXiv:2507.23468** — "On the complex zeros of the wavefunction",
  Cerf, Wassner, Davis, Arzani, Chabaud: holomorphic extension of the
  (single-variable) position wavefunction, a Hudson-type theorem,
  Gaussian dynamics as classical motion of the zeros, single-quadrature
  non-Gaussianity detection. One variable; no links; no dictionary
  obstruction mentioned.
- **arXiv:2605.25862** — "Bargmann Zeros as a Diagnostic of the
  Tunneling Transition in Double-Well Quantum Systems": dynamical
  diagnostic use of (one-mode) Bargmann zeros. Triaged; not deepened
  (no topology-as-obstruction content in the rendered material).
- **arXiv:2504.10455** — "The stellar decomposition of Gaussian
  quantum states": surfaced during the HTFY query; triaged as
  F3-relevant bibliography, not deepened.

### F1 — singularity theory (query: "Milnor singular points complex
hypersurfaces link of singularity torus knot Brauner algebraic link
classification")

- **Milnor, "Singular Points of Complex Hypersurfaces" (1968)** and
  **Brauner (1928)**: links of plane-curve singularities; torus links
  as links of `x^p + y^q = 0`; algebraic links are iterated torus
  cables (engine-rendered from the Manifold Atlas page and related
  sources). Classical mathematics, as expected by exp24 §7: the
  trefoil-from-`w1^2, w2^3` mechanism the repo uses is **standard**.
- **arXiv:1611.02563** — "Knotted fields and explicit fibrations for
  lemniscate knots": Milnor-style explicit constructions bridging F1
  and F2. Triaged.

### F2 — optical vortex knots (queries: "knotted vortex lines optical
fields Leach Dennis Padgett isolated optical vortex knots nodal
lines"; "stability robustness knotted nodal lines perturbation optical
vortex knot structural stability quantitative bound")

- **Dennis, King, Jack, O'Holleran, Padgett, "Isolated optical vortex
  knots", Nature Physics 6, 118 (2010)**: knotted/linked zero
  (vortex) lines engineered in laser beams, following the
  **Berry–Dennis** theoretical constructions; algebraic-topology-based
  design with braided zeros embedded into propagating beams.
- **Berry–Dennis line ("Vortex knots in light", physics/0411121 and
  successors)**: design of knotted nodal lines in wave fields.
- **Stability neighborhood**: "Stability of optical knots in
  atmospheric turbulence" (Nat. Commun. 2025), "Topologically
  protected vortex knots and links" (Commun. Phys. 2022), nested
  vortex-knot coding (Nat. Commun. 2022): engine-rendered content is
  experimental/qualitative robustness of designed real-space knots
  under perturbations (e.g. turbulence altering superposition
  coefficients and topology at sufficient strength). No
  fidelity-ball / explicit-constant isotopy theorem for phase-space
  zero sets is mentioned in the rendered material.

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

- **Berry, "Knotted Zeros in the Quantum States of Hydrogen", Found.
  Phys. (2001)**: torus-knotted nodal lines in superpositions of
  degenerate hydrogen eigenfunctions (real 3-space; explicit recipes;
  trefoil needs `n >= 7`).
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
  zeros used to bound approximation). **No retrieved source uses a
  link/knot invariant of a state's phase-space zero set as a lower
  bound or obstruction for approximation by a restricted dictionary at
  fixed term budget.**

## 3. Citation-chase note

One-hop chases stayed within the families above (e.g. Berry–Dennis
from the Nature Physics item; Brauner/Milnor from the Manifold Atlas
page). No new thematic family was needed; G2 was not triggered.

## 4. Classification table (sole authoring location)

| Topic | Classification | Load-bearing near neighbors (locators above) | Recorded distinction |
| --- | --- | --- | --- |
| T1 | A | 2607.04007; Dennis et al. 2010 / Berry–Dennis; Berry 2001 / 1904.07229; 2605.15008 | nearest works treat one-mode stellar zeros as point configurations (braid monodromy of families), real-space nodal lines of fields/wavefunctions (designed constructions), or S² point constellations; none treats two-mode stellar zero sets ∩ S³ as links with a census (components, windings, linking matrix) |
| T2 | A | 2604.00766; 2410.23721 / 2404.07115; 2111.02391; 2305.10277 | the rank-lower-bound line is analytic (no topological technique in the rendered material); the topological items address different tasks; no retrieved source uses link/knot invariants of phase-space zeros as a restricted-dictionary, fixed-budget approximation obstruction |
| T3 | A | turbulence-stability line (Nat. Commun. 2025 etc.); 2607.04007 | retrieved stability work is experimental/qualitative for designed real-space knots; no fidelity-ball isotopy statement with explicit constants for phase-space zero links was found |
| T4 | A | Milnor 1968 / Brauner 1928; Berry 2001; 1611.02563 | torus-knot zero sets are classical and constructible in many systems; no retrieved source certifies margins for a torus-knot phase-space target against a Gaussian dictionary via a winding bound |
| T5 | A | in-repo K_ε note (one-mode mechanism; not external art); no external two-mode source retrieved | the common-vs-varying dichotomy in two modes was not found outside the in-repo line; the one-mode division mechanism is the note's own and is not claimed by this repo as new |
| T6 | A | 2607.04007 | nearest work is deformation monodromy of one-mode zero configurations; Gaussian-unitary invariance of multimode zero-set structure (exp26's object) is not covered in the rendered material |

No topic is classified P, so protocol G3 (correction duty) is not
triggered. No topic is classified N: every topic has genuine near
neighbors, and the honest reading of §3's scheme puts them all at A.

## 5. What this supports (drafts for orange; nothing adopted here)

Scope-bounded candidate language, for orange's Gate S′ decision only —
none of it is used anywhere in the repo by this survey:

- "Within a declared-scope literature search (2026-08-03; engines and
  limitations recorded), we did not find prior art treating two-mode
  stellar zero sets on the 3-sphere as links with census invariants,
  nor link/knot invariants of phase-space zeros used as a
  restricted-dictionary approximation obstruction; the nearest
  neighboring literatures are [the table's citations]."
- The survey equally supports *required attributions*: the
  trefoil-from-monomials mechanism is classical (Brauner/Milnor);
  knotted zero sets in physical fields and wavefunctions are an
  established, originally-designed literature (Berry–Dennis line);
  one-mode stellar-zero topology has contemporaneous active work
  (2607.04007), which any outward-facing text should cite and
  distinguish.

Per protocol §0, the fetch-level limitation of §1 means a primary-source
re-read is recommended before any outward-facing use.
