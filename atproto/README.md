# MIRA × AT Protocol — lexicon draft (`science.mira.*`)

> **Status: DRAFT / PROPOSAL. Not adopted, not published, not on the network.**
> Hand-authored on the local branch `atproto-lexicon-draft`. Nothing here is canonical.

This folder sketches an [AT Protocol](https://atproto.com) **lexicon** binding for the MIRA
discourse-graph schema, so that the **public** parts of a MIRA / Discourse Graphs graph can be
published as signed, citable records in the broader ATProto ecosystem (the network behind Bluesky,
[OXA](https://oxa.dev/articles/oxa-on-at-proto), Frontpage, etc.) and re-aggregated by anyone.

The canonical schema remains [`../mira.yaml`](../mira.yaml) (LinkML). These lexicons are a
**downstream binding** of it — the same relationship `mira.shacl` / `mira.ttl` / `mira.jsonld` have,
except this one is hand-drafted for now rather than generated (see [`ROADMAP.md`](ROADMAP.md), codegen
milestone).

## Contents

| File | What |
|------|------|
| [`SPEC.md`](SPEC.md) | The binding: every node & edge → lexicon, the design decisions, and the **open questions for the schema team**. |
| [`ROADMAP.md`](ROADMAP.md) | Proposed phases **and the governance path** (schema-team discussion → issue/RFC → PR). |
| `lexicons/science/mira/*.json` | The nine draft lexicons (7 node types + `defs` + `relation`). |
| `examples/*.json` | Sample record **instances** (not lexicons), mirroring `../sampleData.json`. |

## The record types

`science.mira.*` is the reverse-DNS of `mira.science`, the domain MIRA controls.

| Lexicon | MIRA class (`mira.yaml`) |
|---------|--------------------------|
| `science.mira.question` | `Question` |
| `science.mira.claim` | `Claim` |
| `science.mira.evidence` | `Evidence` |
| `science.mira.study` | `Study` |
| `science.mira.protocol` | `Protocol` |
| `science.mira.request` | `Request` |
| `science.mira.sourceDocument` | `SourceDocument` |
| `science.mira.relation` | `dgb:RelationInstance` (reified edge) |
| `science.mira.defs` | shared `ref` / `externalRef` / `dataArtifact` / `agent` defs |

## In one paragraph

A MIRA node becomes a record in its author's personal repo; its **AT-URI** is the citable id; the
**signing DID** is the creator (no `creator` field needed). Forward edges the author owns are inlined
on the node; anyone can assert an edge about records they don't own via a standalone
`science.mira.relation` record (this is exactly how MIRA already reifies relations, and how Bluesky
likes/follows work). Inverse edges are not stored — an **AppView** indexing the firehose derives them
and answers "which claims are supported, which contested, which questions unanswered." Raw data
(figures, datasets) stays a URL via `dataArtifact` — pointers, not payloads.

See [`SPEC.md`](SPEC.md) for the full mapping and the decisions a schema-team RFC would need to settle.
