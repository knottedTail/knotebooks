# `concept.definition`

## Purpose

A `concept.definition` atom introduces a mathematical object.

It belongs to:

- `family: concept`
- `type: definition`

A definition atom describes what an object is. It does not assert a theorem, record a failed attempt, or provide proof-style justification.

## Canonical Shape

```yaml
unit_id: def:2026-04-08-field
family: concept
type: definition
name: field
body: |
  A field is a set $F$ equipped with two binary operations, called addition
  and multiplication, such that $(F, +)$ is an abelian group, multiplication
  is associative and commutative on $F \setminus \{0\}$, and multiplication
  distributes over addition.
based_on: []
axiomatic: true
aliases: []
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

## Writing Guidance

### `name`

Good:

- `field`
- `vector space`
- `associative algebra`

Bad:

- `vector space over k`
- `associative algebra over a field`
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

- a vector space depends on field
- an associative algebra depends on field and vector space

Bad:

- listing every atom mentioned nearby in the note
- using notation or context ids
- using statement or process atom ids
- using the atom's own `unit_id`

### `aliases`

Good aliases are interchangeable names.

Good:

- `linear space` as an alias for `vector space`

Bad:

- `finite-dimensional vector space` if it adds extra conditions
- `associative algebra over k` if it is only a local specialization

## What Is Not A Definition

Do not use `concept.definition` when the source material is really:

- a symbol assignment with no new object meaning: use `notation`
- a local assumption block: use `context`
- a claim about an object: use a `statement` atom
- a derivation, experiment, or exploratory step: use a `process` atom

Even if notation or context atoms exist elsewhere in the ontology later, they are not part of the `concept.definition` data structure.

## Source Mapping

In the current workflow, source notes may contain a LaTeX `definitionitem` block.

- block id maps to `unit_id`
- block title is an extraction hint for `name`
- block body maps to `body`
- explicit semantic references may populate `based_on`

The source title is not stored as a canonical field in v1.

## Example Patterns

### Axiomatic Definition

Use this when the note introduces a new concept and no earlier definition dependencies have been identified.

### Dependent Definition

Use this when the concept explicitly refines or builds on earlier definitions.

### Multi-Dependency Definition

Use this when a concept genuinely depends on more than one prior definition, such as an associative algebra depending on both field and vector space.
