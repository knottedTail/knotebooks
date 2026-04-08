# `concept.definition`

## Purpose

A `concept.definition` atom introduces a mathematical object.

It belongs to:

- `family: concept`
- `type: definition`

A definition atom describes what an object is. It does not assert a theorem, record a failed attempt, or provide proof-style justification.

## Canonical Shape

```yaml
unit_id: def:2026-04-08-weight-profile
family: concept
type: definition
name: weight profile
body: |
  A weight profile is a finite tuple $(w_1, \dots, w_n)$ of integers
  attached to an object under study.
based_on: []
axiomatic: true
aliases: []
notation_ids: []
context_ids: []
tags:
  - algebra
related_unit_ids: []
confidence: 0.98
provenance:
  source_raw_file: raws/2026-04-08.tex
  source_date: 2026-04-08
  extracted_at: 2026-04-08T09:15:00Z
  extractor_version: codex-v1
```

## Field Glossary

- `unit_id`
  - Stable identifier for the definition atom
  - Must start with `def:`
- `name`
  - Canonical concept name
  - Must not include parameters such as "over `k`", "for fixed `n`", or similar local assumptions
- `body`
  - The actual definition text
  - Preserve LaTeX math and mathematical phrasing from the source when possible
- `based_on`
  - List of definition ids this definition depends on
  - Must contain only `def:` ids
  - Leave empty when there are no identified definition dependencies or when dependencies remain unresolved
- `axiomatic`
  - `true` if no meaningful dependencies were identified
  - `false` if the definition depends on earlier definitions or if dependency analysis is unresolved
- `aliases`
  - True synonyms only
  - Do not use for stricter variants, special cases, or contextual restatements
- `notation_ids`
  - Optional links to separate `concept.notation` atoms
- `context_ids`
  - Optional links to separate `concept.context` atoms

## Writing Guidance

### `name`

Good:

- `weight profile`
- `balanced weight profile`
- `admissible filtration`

Bad:

- `weight profile over k`
- `balanced weight profile for fixed rank n`
- `an admissible filtration`

### `body`

Good `body` values:

- define the object directly
- preserve mathematical notation from the source
- stay focused on the meaning of the object

Bad `body` values:

- include a proof sketch
- mix in evidence for a conjecture
- explain why a strategy failed
- only introduce notation without defining the object

### `based_on`

Use `based_on` only for prior definitions that the concept genuinely depends on.

Good:

- a balanced weight profile depends on weight profile
- an admissible filtration depends on filtration

Bad:

- listing every atom mentioned nearby in the note
- using statement or process atom ids
- using the atom's own `unit_id`

### `aliases`

Good aliases are interchangeable names.

Good:

- `zero-sum weight profile` as an alias for `balanced weight profile`

Bad:

- `semistable weight profile` if it adds extra conditions
- `balanced profile in rank 3` if it is only a local specialization

## What Is Not A Definition

Do not use `concept.definition` when the source material is really:

- a symbol assignment with no new object meaning: use `notation`
- a local assumption block: use `context`
- a claim about an object: use a `statement` atom
- a derivation, experiment, or exploratory step: use a `process` atom

## Source Mapping

In the current workflow, source notes may contain a LaTeX `definitionitem` block.

- block id maps to `unit_id`
- block title is an extraction hint for `name`
- block body maps to `body`
- explicit semantic references may populate `based_on`
- tags map to `tags`
- note metadata fills `provenance`

The source title is not stored as a canonical field in v1.

## Example Patterns

### Axiomatic Definition

Use this when the note introduces a new concept and no earlier definition dependencies have been identified.

### Dependent Definition

Use this when the concept explicitly refines or builds on earlier definitions.

### Definition With Linked Notation Or Context

Use this when notation or assumptions are important enough to stand as separate atoms and can be linked by id.
