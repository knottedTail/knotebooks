# knotebooks

`knotebooks` is an AI-assisted research system for mathematicians. It turns source-side daily notes into structured mathematical atoms that can be validated, indexed, searched, and reused downstream.

## Current Model

The canonical basic data unit in this repository is an `atom`.

Atoms are organized into three families:

- `concept`: `definition`, `notation`, `context`
- `statement`: `proposition`, `conjecture`, `observation`, `question`, `insight`
- `process`: `computation`, `attempt`, `failed_attempt`, `proof_idea`, `example`, `reference_note`

This first documentation pass defines the shared atom contract and the first fully specified atom type: `concept.definition`.

## Documentation

- [Project overview](docs/project_overview.md)
- [Atom ontology](docs/ontology.md)
- [Human spec for `concept.definition`](docs/atoms/concept.definition.md)
- [Codex extraction contract for `concept.definition`](docs/codex/concept.definition.md)

## Schemas And Fixtures

- [Base atom schema](schemas/atom.schema.yaml)
- [`concept.definition` schema](schemas/concept.definition.schema.yaml)
- [Example definition atoms](schemas/examples/)

## Repository Function

- define schemas for structured research atoms
- support extraction from raw notes into canonical atom files
- preserve provenance from source notes to derived atoms
- validate canonical atoms
- index structured data for retrieval
- support search and reuse over the structured layer

## Storage Model

- Canonical atoms live under `derived/units/<family>/<type>/<unit_id>.yaml`
- The first canonical path established in this pass is `derived/units/concept/definition/<unit_id>.yaml`
- Embeddings and search-ready text belong to a separate derived index, not to canonical atom files
- Source-side daily notes remain the human-authored origin; the current repository includes LaTeX note templates under `templates/`
