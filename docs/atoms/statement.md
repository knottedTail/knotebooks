# `statement`

## Purpose

A `statement` atom describes an assertion, question, observation, or conceptual insight about mathematical objects.

It belongs to:

- `family: statement`
- `type: one of proposition, conjecture, observation, question, insight`

A statement atom expresses content that can be asserted, conjectured, observed, questioned, or conceptually suggested. It must not introduce a new definition, notation, or context block.

## Canonical Shape

```yaml
atom_id: stmt:center-subalgebra
family: statement
type: proposition
body: |
  The center of an associative algebra is a subalgebra.
depends_on:
  - def:associative-algebra
supports: []
related_to:
  - def:associative-algebra
```

## Field Glossary

- `atom_id`
  - Stable identifier for the statement atom
  - Must start with `stmt:`
  - Should be semantic and should not include the creation date
- `body`
  - Main statement text
  - Must be self-contained enough to interpret as a statement atom
- `depends_on`
  - Atoms required to understand the statement
  - Must contain only `def:` or `stmt:` ids
- `supports`
  - Atoms that provide evidence or justification
  - May reference any atom family
  - Typical supports are process atoms, examples, or earlier arguments
- `related_to`
  - Atoms with meaningful but looser thematic or heuristic relation
  - May reference any atom family

All three relation arrays are required and use `[]` when empty.

## Shared Writing Guidance

### `body`

Good `body` values:

- clearly read as a proposition, conjecture, observation, question, or insight
- refer to mathematical objects without redefining them
- stay focused on one main statement

Bad `body` values:

- introduce a new concept definition
- introduce notation with no statement content
- mix several unrelated claims into one atom

### `depends_on`

Use `depends_on` for atoms required to understand the statement.

Good:

- a proposition about associative algebras depends on `def:associative-algebra`
- a conjecture refining an earlier claim depends on both a definition and a prior statement

Bad:

- adding every nearby atom whether needed or not
- using process-only evidence atoms as if they were conceptual prerequisites
- using ids outside `def:` and `stmt:`

### `supports`

Use `supports` for evidence, justification, examples, or prior arguments.

Good:

- a computation atom supporting an observation
- a previous proposition supporting an insight or conjecture

Bad:

- using `supports` for atoms that are actually prerequisites
- using it as a vague replacement for `related_to`

### `related_to`

Use `related_to` for looser but still meaningful connections.

Good:

- a conceptual insight related to a proposition and a definition
- a question related to a nearby conjecture

Bad:

- encoding strict dependency in `related_to` when `depends_on` should be used
- populating it with arbitrary nearby atoms

## Statement Labels

Canonical statement subtypes are:

- `proposition`
- `conjecture`
- `observation`
- `question`
- `insight`

When a source note uses labels such as theorem, lemma, or corollary, normalize them to `type: proposition`.
