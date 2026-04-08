# Atom Ontology

## Purpose

This document is the normative cross-type contract for `knotebooks` atoms. It defines the shared atom envelope, the current family/type ontology, id conventions, storage rules, and the boundary between canonical atoms and derived search data.

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
Shared fields are intentionally minimal in v1. Richer semantic fields such as `name`, `body`, `based_on`, `axiomatic`, and `aliases` belong in atom-specific schemas.

## Id Conventions

`unit_id` is the canonical stable identifier for an atom.

- Shape: `<prefix>:<slug>`
- Prefix identifies the atom type family contract
- Slug is human-readable, semantic, and should remain stable once published
- `unit_id` should not encode the date when the atom was created
- This pass makes `def:` normative for `concept.definition`
- Other prefixes may exist in source notes already, but they are not yet canonical until their atom specs are defined

Examples:

- `def:field`
- `def:vector-space`

## Storage Rules

Canonical atoms are stored as one YAML file per atom under `derived/units/`.

- Layout: `derived/units/<family>/<type>/<unit_id>.yaml`
- First concrete path in this pass: `derived/units/concept/definition/<unit_id>.yaml`
- The filename should exactly equal `unit_id`, with `.yaml` appended
- Canonical atom files are meant for inspection, schema validation, diff review, and downstream indexing

## Validation Layers

Validation happens in two layers.

- Schema validation checks shape, required fields, enums, and type-safe references
- Semantic validation checks cross-field rules that plain JSON Schema cannot express well

Examples of semantic rules that need validator support later:

- a definition must not list itself in `based_on`
- `name` must stay parameter-free even if the source title includes local assumptions
- `concept.definition` should remain a definition-only structure with no notation or context links

## Search Boundary

Canonical atoms are not the same thing as the search index.

- canonical atom files preserve source-faithful semantic content
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
