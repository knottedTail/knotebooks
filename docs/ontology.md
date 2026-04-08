# Atom Ontology

## Purpose

This document is the normative cross-type contract for `knotebooks` atoms. It defines the shared atom envelope, the current family/type ontology, id conventions, storage rules, provenance rules, and the boundary between canonical atoms and derived search data.

## Atom Families

Atoms are grouped into three families.

- `concept`
  - `definition`
  - `notation`
  - `context`
- `statement`
  - `proposition`
  - `conjecture`
  - `observation`
  - `question`
  - `insight`
- `process`
  - `computation`
  - `attempt`
  - `failed_attempt`
  - `proof_idea`
  - `example`
  - `reference_note`

Only `concept.definition` is fully specified in this pass. Other types are recognized by the ontology but still need dedicated type specs.

## Shared Atom Envelope

Every canonical atom must provide the following shared fields.

| Field | Status | Meaning |
| --- | --- | --- |
| `unit_id` | required | Stable atom identifier |
| `family` | required | One of `concept`, `statement`, `process` |
| `type` | required | Atom subtype within the family |
| `provenance` | required | Source-note and extraction metadata |
| `tags` | optional | Human or extraction tags |
| `related_unit_ids` | optional | Untyped cross-links to other atoms |
| `confidence` | optional | Extraction confidence in the range `[0, 1]` |

Shared fields are intentionally small. Richer relationships such as `based_on`, `notation_ids`, or `context_ids` belong in atom-specific schemas.

## Provenance Contract

Every canonical atom must preserve:

- `source_raw_file`
- `source_date`
- `extracted_at`
- `extractor_version`

Provenance is part of the canonical atom and is not optional, even when extraction is manual.

## Id Conventions

`unit_id` is the canonical stable identifier for an atom.

- Shape: `<prefix>:<slug>`
- Prefix identifies the atom type family contract
- Slug is human-readable and should remain stable once published
- This pass makes `def:` normative for `concept.definition`
- Other prefixes may exist in source notes already, but they are not yet canonical until their atom specs are defined

Examples:

- `def:2026-04-08-weight-profile`
- `def:2026-04-08-balanced-weight-profile`

## Storage Rules

Canonical atoms are stored as one YAML file per atom under `derived/units/`.

- Layout: `derived/units/<family>/<type>/<unit_id>.yaml`
- First concrete path in this pass: `derived/units/concept/definition/<unit_id>.yaml`
- Canonical atom files are meant for inspection, schema validation, diff review, and downstream indexing

## Validation Layers

Validation happens in two layers.

- Schema validation checks shape, required fields, enums, and type-safe references
- Semantic validation checks cross-field rules that plain JSON Schema cannot express well

Examples of semantic rules that need validator support later:

- a definition must not list itself in `based_on`
- `name` must stay parameter-free even if the source title includes local assumptions
- typed link fields should reference atoms of the expected type

## Search Boundary

Canonical atoms are not the same thing as the search index.

- canonical atom files preserve source-faithful content and provenance
- embedding text, vector indexes, and retrieval-oriented expansions belong in a separate derived index layer
- downstream search should operate on the derived structured layer, not on ad hoc parsing of source prose

## Source Mapping Boundary

Source notes remain the human-authored origin. The repository currently includes LaTeX daily-note templates that define source-side blocks such as `definitionitem`.

Source-side fields and canonical atom fields are not always identical.

- source titles may help extraction but are not automatically canonical fields
- atom-specific specs decide which source-side cues become canonical data
- this pass defines that a `definitionitem` title is a hint for `concept.definition.name`, not a stored `title` field

## Note On Statement Labels

The current ontology recognizes `proposition` as the canonical statement type in this family pass. Presentation labels such as theorem, lemma, or corollary may later be modeled as refinements or display labels when the statement family is specified in detail.
