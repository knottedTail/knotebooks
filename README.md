# knotebooks

`knotebooks` is an AI-assisted research system for mathematicians. It turns source-side daily notes into structured mathematical atoms that can be validated, indexed, searched, and reused downstream.

## Current Model

The canonical basic data entity in this repository is an `atom`.

Atoms are organized into three families:

- `concept`: `definition`, `notation`, `context`
- `statement`: `proposition`, `conjecture`, `observation`, `question`, `insight`
- `process`: `computation`, `attempt`, `failed_attempt`, `proof_idea`, `example`, `reference_note`

This documentation pass defines the shared atom contract, fully specifies `concept.definition`, and implements the `statement` family.

## Documentation

- [Project overview](docs/project_overview.md)
- [Atom ontology](docs/ontology.md)
- [Human spec for `concept.definition`](docs/atoms/concept.definition.md)
- [Human spec for `statement`](docs/atoms/statement.md)
- [Codex extraction contract for `concept.definition`](docs/codex/concept.definition.md)
- [Codex extraction contract for `statement`](docs/codex/statement.md)

## Schemas

- [Base atom schema](schemas/atom.schema.yaml)
- [`concept.definition` schema](schemas/concept.definition.schema.yaml)
- [Shared `statement` schema](schemas/statement.schema.yaml)

## Canonical Atoms

- [Definition atoms](derived/atoms/concept/definition/)
- [Statement atoms](derived/atoms/statement/)

## Repository Function

- define schemas for structured research atoms
- support extraction from raw notes into canonical atom files
- validate canonical atoms
- index structured data for retrieval
- support search and reuse over the structured layer

## Storage Model

- Canonical atoms live under `derived/atoms/<family>/<type>/<atom_id>.yaml`
- The first canonical path established in this pass is `derived/atoms/concept/definition/<atom_id>.yaml`
- Statement atoms live under `derived/atoms/statement/<type>/<atom_id>.yaml`
- In this model, the filename should exactly match `atom_id`, with only the `.yaml` extension added
- In v1, a `concept.definition` atom stores only semantic definition data
- In v1, a `statement` atom stores `body`, `depends_on`, `bindings`, `supports`, `related_to`, explicit resolution links, `resolution_status`, and lightweight `references` in addition to the shared atom fields
- Duplicate definition names are allowed; practical disambiguation comes from `atom_id`, `based_on`, and the opening sentence of `body`
- Theorem, lemma, and corollary are treated as source-side labels and normalize to `type: proposition`
- Embeddings and search-ready text belong to a separate derived index, not to canonical atom files
- Source-side daily notes remain the human-authored origin; the current repository includes LaTeX note templates under `templates/`
