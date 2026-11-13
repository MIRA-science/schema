# Example graphs

Validation fixtures beyond `sampleData.json`. `make validate_examples` (also run by `make validate_data`) validates every `*.jsonld` file here against `mira.shacl`.

The examples refer to the context in this repository (`../mira.jsonld`), not to the published URL. Validation then tests the working copy's context, so a change to the context is checked in the same pull request, and these checks don't depend on the context URL being reachable. A clean build still downloads `dg_base.ttl` for the ontology.

## research-survey.jsonld

A source-derived fixture with an illustrative review scenario, from a desk-research project outside the life sciences: a landscape survey of research tooling carried out largely by LLM agents with web search, then partly fact-checked. 39 nodes: 3 Questions, 8 Claims, 8 Evidence nodes, 5 Studies, 2 SourceDocuments (one unreferenced), 1 Request, 3 UserAccounts, and 9 reified `supports`/`opposes` RelationInstances, each with its own `creator`.

What comes from the actual survey:

- Each Study is a real agent run (a scan or the fact-check).
- Each Evidence title quotes, verbatim, a passage from that run's output.
- The `opposes` relation and the superseded version claim record a real correction made by the fact-check.

What was constructed to exercise the schema:

- Claim wording and grouping were written for the fixture, from the survey's conclusions.
- One claim (`c-typst-active`) still depends on the superseded claim, on purpose.
- The Request stands for an open decision.
- The account names (`human:lead`, `agent:…`) are placeholders.

Each Study's creator is the agent account that ran it, so the graph also shows how much of the evidence is model-generated: 7 of the 8 Evidence nodes.
