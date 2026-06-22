# MIRA × AT Protocol — proposed roadmap

> Status: **PROPOSED. Nothing here has been carried out** beyond the draft in this folder.
> No lexicons published, no infrastructure stood up, no PR opened, nothing pushed.

## A. How this gets introduced into MIRA (the governance path)

The draft is deliberately a *spike on a local branch*, not a fait accompli. The schema is a shared
contract (`mira.yaml` ripples to every project in the workspace), so the binding should enter through
discussion, not a surprise PR.

| Step | What | Where | Output |
|------|------|-------|--------|
| **0. Spike** *(done)* | Hand-draft lexicons + spec + this roadmap on local branch `atproto-lexicon-draft`. Kept local. | `schema/atproto/` | This folder. |
| **1. Schema-team discussion** | Raise at a schema sync (async is fine): frame as *"an ATProto binding for the **public** discourse-graph nodes,"* not a schema change. Get buy-in on scope, on the `science.mira.*` authority (we control `mira.science`), and on whether this complements or competes with KOI-net. Loop in the **Discourse Graphs** team, since public DG nodes map through it. | Meeting / Slack / `MIRA-science` discussion | A go/no-go on "worth an RFC?" |
| **2. Issue / RFC** | Open an issue in `MIRA-science/schema` titled e.g. *"RFC: AT Protocol lexicon binding for public DG nodes."* Summarize §2 of the SPEC, link the **open questions Q1–Q8**, and cross-link the [`inter-lab-user-story` §10](../../inter-lab-user-story/) transport/identity items this would close. Solicit decisions on Q1 (edge canonicalization), Q2 (ref strength), Q4 (governance), Q5 (codegen). | GitHub issue (RFC) | Resolved design questions; recorded decision. |
| **3. PR** | If accepted in principle, open a PR adding `schema/atproto/` (lexicons + spec), reviewed against the repo's README/AGENTS conventions. Cite the resolved RFC questions in the PR description. | `MIRA-science/schema` PR | `atproto/` merged to `main` as an accepted-draft binding. |
| **4. Codegen** | Replace the hand-drafted lexicons with ones **generated from `mira.yaml`** (LinkML → lexicon), wired into the `Makefile` alongside the SHACL/TTL/JSON-LD targets, so the binding can't drift from canonical. (Resolves Q5.) | `MIRA-science/schema` PR | `make` emits `atproto/lexicons/**`. |
| **5. Reference PoC** | Stand up a minimal end-to-end proof: write a slice of the demo graph into a PDS, run a Jetstream consumer that rebuilds the graph, render it in the **existing d3 viewer** (`matsulab-MIRA-graph-data`). Proves "host-nothing + emergent aggregated graph" on real infra. | New repo / `matsulab-MIRA-graph-data` | A working demo; evidence for or against adoption. |
| **6. Publish** | Only once stable: make `science.mira.*` **resolvable** (lexicon resolution via `mira.science` DNS / `com.atproto.lexicon.schema`), so third parties can validate and build AppViews. This is the irreversible, outward-facing step — gated on 1–5. | DNS + `mira.science` | Lexicons live on the network. |

**Decision gates:** Step 3 is gated on Q1/Q2/Q4 from the RFC; Step 4 on Q5; Step 6 on Q4 governance
+ a stable schema (lexicon evolution is append-mostly, so publishing pins us).

## B. Technical milestones (independent of governance)

- **M0 — Draft binding** *(this folder).* Nine lexicons, spec, examples.
- **M1 — Validation.** Run the drafts through the ATProto lexicon validator / `@atproto/lex` codegen;
  hand-write a few real records (extend `examples/`); confirm round-trip against `sampleData.json`.
- **M2 — Codegen.** LinkML→lexicon generator (Step 4). Source of truth stays `mira.yaml`.
- **M3 — PoC AppView.** PDS write + Jetstream consumer + d3 viewer (Step 5).
- **M4 — Interop.** Demonstrate `sourceDocument.externalRecord` pointing at a real `pub.oxa.document`;
  verify a generic ATProto indexer can see MIRA records on the firehose.
- **M5 — Publish + AppView service** (Step 6) — only if M3/M4 justify it.

## C. Risks / what would kill it

- **Adoption tax** — researchers need DIDs; ORCID bridging (Q7) is unproven friction.
- **Two schema languages** — without M2 codegen, the lexicons rot relative to `mira.yaml`.
- **Indexer cost** — a live field graph means running a Jetstream consumer + AppView indefinitely.
- **Premature publish** — Step 6 is hard to walk back (records and lexicons get cached/indexed network-wide); do not publish before the schema is stable.
- **Maybe KOI-net is enough** — if the only requirement is signed federation among a few known labs,
  this is heavier than needed. The deciding factor is the stated goal: **interop with the broader
  ATProto ecosystem** (which this delivers and KOI-net does not).

## D. Not being done yet

To be explicit, none of the following has happened: no push, no issue/RFC filed, no PR, no lexicons
published, no DNS changes, no PDS/AppView running. Step 0 only.
