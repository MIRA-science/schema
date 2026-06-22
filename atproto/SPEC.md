# MIRA × AT Protocol binding — specification (DRAFT)

> Status: **DRAFT / proposal.** Derived by hand from [`../mira.yaml`](../mira.yaml).
> Canonical schema stays `mira.yaml`; this is a downstream binding. Nothing here is adopted.

## 1. Scope & goal

Bind the **public** MIRA / Discourse-Graphs node and edge types to AT Protocol **lexicons**
(`science.mira.*`) so that public discourse-graph records can be:

- **published** as signed, portable records in researchers' own repositories;
- **cited** by a stable, resolvable id (the AT-URI);
- **re-aggregated** by any indexer into a live "state of the field" view;
- **interoperable** with the wider ATProto ecosystem (Bluesky, [OXA](https://oxa.dev/articles/oxa-on-at-proto), etc.).

**Out of scope (for now):** private/unpublished nodes (ATProto "permissioned data" is still in
flight — see §9 Q6); replacing `mira.yaml` as canonical; a full XRPC query API. This binding covers
the *record* layer only.

This serves the [`inter-lab-user-story`](../../inter-lab-user-story/) directly: ATProto is a
concrete candidate answer to the transport / signing / identity questions in its **§10** open list,
and a substrate for rules **R1–R13** (push a result to a shared interface). It is an alternative or
complement to the KOI-net transport already being trialled.

> Per the schema repo's own README, the MIRA schema is meant to *stand alone* and each platform
> (incl. Discourse Graphs) inherits it. So this binding lives at the **MIRA** level
> (`science.mira.*`), and public DG nodes map through it — they do not get their own parallel
> namespace.

## 2. Why the shapes line up

| MIRA design principle | ATProto primitive it maps onto |
|---|---|
| "MIRA itself hosts nothing" | The protocol hosts nothing; records live in per-user PDS repos; indexers aggregate. |
| Signed, **citable** records | Repo records are signed; the **AT-URI** (`at://did/science.mira.claim/rkey`) is the citable id. |
| `creator` on every node | The **signing DID** is the author of every record in its repo — attribution is structural. |
| "Query the live graph … which claims are contested" | That is precisely an **AppView**: index the firehose, serve the aggregate. |
| Pointers, not payloads | Records are small JSON; big data is a URL via `defs#dataArtifact`. |
| One shared graph, many tools | A **lexicon** is a shared, versioned, multi-writer contract. |
| Relations reified with their own `creator` (`sampleData.json`) | A standalone `science.mira.relation` record, signed by its asserter. |

## 3. Node types → lexicons

`science.mira.*` = reverse-DNS of `mira.science` (MIRA controls the domain, so it owns the authority).

| `mira.yaml` class | Lexicon | Record key |
|---|---|---|
| `Question` | `science.mira.question` | `tid` |
| `Claim` | `science.mira.claim` | `tid` |
| `Evidence` | `science.mira.evidence` | `tid` |
| `Study` | `science.mira.study` | `tid` |
| `Protocol` | `science.mira.protocol` | `tid` |
| `Request` | `science.mira.request` | `tid` |
| `SourceDocument` | `science.mira.sourceDocument` | `tid` |
| `dgb:RelationInstance` | `science.mira.relation` | `tid` |

The `Argument` and `Activity` mixins are *not* their own records: `Argument` contributes the
`supports`/`opposes` fields to `claim` and `evidence`; `Activity` is the shared shape of `study` and
`protocol`.

## 4. Field mapping (the `NodeSchema` mixin)

Every node mixes in `NodeSchema` → `created`, `modified`, `creator`, `title`, `description`,
`has_container`. These are inlined on each record (idiomatic ATProto — records are self-contained):

| `NodeSchema` slot | Lexicon field | Notes |
|---|---|---|
| `dct:created` | `createdAt` (datetime, **required**) | Conventional ATProto record field. |
| `dct:modified` | `updatedAt` (datetime) | |
| `dct:title` | `title` (string) | The "CLM - …" style label. |
| `dgb:description` (string) | `description` (string) | Inline text form. |
| `dgb:description` (URI / `Item`) | `descriptionRef` (`defs#externalRef`) | Pointers-not-payloads form — content held off-PDS. |
| `creator` | **implicit = repo DID**; `attributedTo` (`defs#agent`) only when they differ | A curator importing a third party's claim sets `attributedTo` (DID **or** ORCID). |
| `has_container` | `container` (`defs#externalRef`) | |

`description` is modelled as *two* optional fields (`description` for the inline string, `descriptionRef`
for the URI form) rather than a union, because the inline-string case is overwhelmingly common and
should stay trivial to write. (Open question Q-desc in §9 if a single union is preferred.)

**`observationBase`** (range `prov:Entity` — the literal figure/blot/dataset) maps to
`defs#dataArtifact`: an external `uri` (preferred, large data) with an optional small PDS `blob`.

## 5. Edges — two representations

MIRA reifies *all* edges as `RelationInstance`s. ATProto gives a choice, and this binding uses a
**hybrid** (the central design decision; see Q1):

### 5a. Inline forward edges (the subject author owns the edge)

Stored as fields on the node record, as `defs#ref` (an AT-URI, optionally pinned with a `cid`):

| Record | Inlined edges (from `mira.yaml`) |
|---|---|
| `claim` | `addresses` → question · `supports` / `opposes` → claim |
| `evidence` | `observationStatement` → claim *(req.)* · `observationBase` → dataArtifact *(req.)* · `observationOriginActivity` → study · `isGroundedIn` → study · `sourceDocument` → sourceDocument · `supports` / `opposes` → claim |
| `study` | `follows` → protocol · `grounds` → evidence *(usually derived)* |
| `request` | `requestFor` → study · `requestTarget` → claim |
| `sourceDocument` | `describesActivity` → study · `externalRecord` → any (interop) |

`observationStatement` and `observationBase` are **required** on `evidence`, honoring the
cardinality-1 restriction the schema notes in comments (Q3 if the schema team wants them relaxed).

### 5b. Reified edges — `science.mira.relation` (anyone asserts an edge about records they don't own)

`{ source, destination, predicate }` + its own `createdAt`/`attributedTo` — a direct image of
`dgb:RelationInstance`. This is the **cross-lab** mechanism and the reason the binding is worth
doing: Lab B publishes "my evidence **opposes** Lab A's claim" into **B's own repo**, with no write
access to A. `predicate` is an open `knownValues` enum so the vocabulary can grow without a breaking
change.

### 5c. Inverse edges are never stored

`addressedBy`, `supportedBy`, `opposedBy`, `grounds` (vs `isGroundedIn`), `followedBy` are
**AppView-derived** — exactly as Bluesky stores `follow` once and computes followers. Half of the
schema's slots therefore disappear from the write model.

### 5d. Weak vs strong refs

`defs#ref` carries a required `uri` and an **optional** `cid`. No `cid` = weak ref (follow the
latest version of the target); `cid` present = strong ref (pin one immutable version — important when
a citation must not silently change underneath you). Default policy is Q2.

## 6. The AppView (where "the live graph of a field" comes from)

No central database. An indexer subscribes to the firehose / Jetstream, filters `science.mira.*`,
and:

1. normalizes **both** inline edges (5a) and `relation` records (5b) into one `RelationInstance` view;
2. computes inverses (5c);
3. answers the MIRA questions — *which claims are supported, which contested, which questions have no
   answering claim, which requests are open* — as graph queries over the aggregate.

Multiple AppViews can co-exist over the same records (the existing d3 viewer, an Obsidian sync,
`myst-plus-mira`). That is the "many tools, one graph" property, for free.

## 7. Interop seam

`sourceDocument.externalRecord` is an AT-URI to a richer record for the same work in **another**
lexicon — e.g. a [`pub.oxa.document`](https://oxa.dev/articles/oxa-on-at-proto). MIRA models the
*discourse graph* (claims/evidence/questions); OXA models the *document* (blocks/facets). They compose:
MIRA points at the document, OXA renders it. No competition.

## 8. Identity

Default author = the repo **DID**. Researchers who think in **ORCID** are bridged two ways: a
`did:web` rooted at an institutional/ORCID-linked domain, or `attributedTo.orcid` on the record when
the signer is a tool/curator rather than the scientist. Identity-bridging policy is Q7.

## 9. Open questions for the schema team (an RFC would settle these)

- **Q1 — Canonicalization of edges.** Hybrid (inline + reified) is drafted. Confirm it, and define the
  AppView **merge rule** when the same edge appears both inline and as a `relation` record (dedupe key?
  precedence? do both count as independent assertions for "contested"?).
- **Q2 — Default ref strength.** Weak (latest) or strong (cid-pinned) by default, and for which edges?
  Citation arguably wants strong; "addresses a question" arguably wants weak.
- **Q3 — Required cardinality on `evidence`.** Keep `observationStatement` + `observationBase`
  required (per the schema comments) or relax for drafts/partials?
- **Q4 — Lexicon governance.** Confirm `science.mira.*` authority (DNS under `mira.science`), the
  versioning policy (lexicon evolution is append-mostly / non-breaking), and who is the steward.
- **Q5 — Codegen vs hand-maintenance.** Generate the lexicons from `mira.yaml` (LinkML → lexicon) and
  wire it into the `Makefile`, so they can't drift. LinkML is *more* expressive than lexicon
  (inheritance, RDF semantics, SHACL) → the generator is lossy; agree what is dropped.
- **Q6 — Private / permissioned nodes.** Only public nodes are in scope now. Revisit when ATProto
  "permissioned data" lands. Keep `MIRA-transcripts`-class data off the network regardless.
- **Q7 — ORCID ↔ DID bridging.** Pick the supported path(s).
- **Q8 — `Request` fields.** The schema has no status/assignee/labels; the issue-tracker shape (and
  the `mira-board` REQ⇄GitHub-issue sync) will want them. Add to `mira.yaml` first, then here.
- **Q-desc — `description` shape.** Two optional fields (drafted) vs one union of string/`Item`/URI.

## 10. Non-goals

- Not canonical — `mira.yaml` is. This binding follows it.
- Not for private/unpublished science.
- Not an XRPC API yet (records only).
- Not adopted — see [`ROADMAP.md`](ROADMAP.md) for the path to propose it.

## 11. References

- AT Protocol lexicon spec — https://atproto.com/specs/lexicon
- ATProto Spring 2026 roadmap (IETF standardization in progress) — https://atproto.com/blog/2026-spring-roadmap
- OXA, scientific documents on ATProto — https://oxa.dev/articles/oxa-on-at-proto
- MIRA schema source — [`../mira.yaml`](../mira.yaml); sample data — [`../sampleData.json`](../sampleData.json)
- North-star user story — [`../../inter-lab-user-story/`](../../inter-lab-user-story/)
