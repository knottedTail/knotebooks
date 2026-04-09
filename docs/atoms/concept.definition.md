# `concept.definition`

## Purpose

A `concept.definition` atom introduces a mathematical object.

It belongs to:

- `family: concept`
- `type: definition`

A definition atom describes what an object is. It does not assert a theorem, record a failed attempt, or provide proof-style justification.

## Canonical Shape

```yaml
atom_id: def:field
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

- `atom_id`
  - Stable identifier for the definition atom
  - Must start with `def:`
  - Should be semantic and should not include the creation date
- `name`
  - Canonical concept name
  - Duplicate `name` values are allowed
  - Must come from explicit source wording rather than model-supplied expansion
  - Must not include parameters such as "over `k`", "for fixed `n`", or similar local assumptions
- `body`
  - The actual definition text
  - Preserve LaTeX math and mathematical phrasing from the source when possible
  - When `name` is ambiguous, the opening sentence must state the sense immediately
- `based_on`
  - List of definition ids this definition depends on
  - Must contain only `def:` ids
  - Leave empty when there are no identified definition dependencies or when dependencies remain unresolved
  - For ambiguous repeated `name` values, this is the main mathematical source of disambiguation when such a basis exists
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
- `U_q(\\mathfrak{g})` when the source names the object only by that notation

Bad:

- `vector space over k`
- `associative algebra over a field`
- `an admissible filtration`
- a guessed expansion of source notation that does not appear in the source

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
- start with an ambiguous sentence when `name` is duplicated elsewhere

### `based_on`

Use `based_on` only for prior definitions that the concept genuinely depends on.

Good:

- a vector space depends on field
- an associative algebra depends on field and vector space

Bad:

- listing every atom mentioned nearby in the note
- using notation or context ids
- using statement or process atom ids
- using the atom's own `atom_id`
- using it as an unprincipled bag of nearby concepts rather than a mathematically prior basis

### Duplicate Names

Duplicate `name` values are allowed.

When a name is ambiguous:

- `atom_id` should carry the distinguishing sense
- `based_on` should carry the mathematically prior definition basis when such a basis exists
- the opening sentence of `body` should disambiguate immediately

Good:

- `atom_id: def:associativity-binary-operation`
- `name: associativity`
- `based_on: [def:binary-operation]`
- opening sentence: `Associativity of a binary operation is the property that ...`

Bad:

- two atoms with `name: associativity` and the same `based_on`, unless they are intentionally separate formulations and reviewed as such
- `atom_id: def:associativity` when the sense is ambiguous
- opening sentence: `Associativity is the property that ...` when the sense is not already obvious

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

- block id maps to `atom_id`
- block title is an extraction hint for `name`
- block body maps to `body`
- explicit semantic references may populate `based_on`

The source title is not stored as a canonical field in v1.

When a definition atom is stored as a YAML file, the filename should exactly match `atom_id`, with `.yaml` appended.

## Example Patterns

### Axiomatic Definition

Use this when the note introduces a new concept and no earlier definition dependencies have been identified.

### Dependent Definition

Use this when the concept explicitly refines or builds on earlier definitions.

### Multi-Dependency Definition

Use this when a concept genuinely depends on more than one prior definition, such as an associative algebra depending on both field and vector space.

### Repeated-Name Definition

Use this when the lexical name is reused across nearby concepts, but the mathematically prior basis in `based_on` distinguishes the senses.
