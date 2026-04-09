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
  The center of $A$ is a subalgebra.
depends_on:
  - def:associative-algebra
bindings:
  - notation: A
    refers_to: def:associative-algebra
supports: []
related_to:
  - def:associative-algebra
answered_by: []
resolved_by: []
refuted_by: []
resolution_status: open
references:
  - kind: raw_file
    locator: raws/2026-04-08.tex
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
- `bindings`
  - Lightweight local symbol-to-definition assignments used by the statement
  - Each item must contain `notation` and `refers_to`
  - `refers_to` must be a `def:` id
- `supports`
  - Atoms that provide evidence or justification
  - May reference any atom family
  - Typical supports are process atoms, examples, or earlier arguments
- `related_to`
  - Atoms with meaningful but looser thematic or heuristic relation
  - May reference any atom family
- `answered_by`
  - Later statement atoms that answer a question
  - Must contain only `stmt:` ids
- `resolved_by`
  - Later statement atoms that positively settle a statement
  - Must contain only `stmt:` ids
- `refuted_by`
  - Later statement atoms that negatively settle a statement
  - Must contain only `stmt:` ids
- `resolution_status`
  - Current resolution state of the statement
  - One of `open`, `answered`, `resolved`, `refuted`
- `references`
  - Lightweight source handles for raw files, papers, books, notes, or web sources
  - Each item must contain `kind` and `locator`

All relation arrays are required and use `[]` when empty.

## Shared Writing Guidance

### `body`

Good `body` values:

- clearly read as a proposition, conjecture, observation, question, or insight
- refer to mathematical objects without redefining them
- stay focused on one main statement
- keep only mathematically essential content
- keep scope qualifiers only when they materially change the claim

Bad `body` values:

- introduce a new concept definition
- introduce notation with no statement content
- mix several unrelated claims into one atom
- include note-local framing such as "in the examples under consideration" when that framing does not change the mathematical content

### `depends_on`

Use `depends_on` for atoms required to understand the statement.

Good:

- a proposition about associative algebras depends on `def:associative-algebra`
- a conjecture refining an earlier claim depends on both a definition and a prior statement

Bad:

- adding every nearby atom whether needed or not
- using process-only evidence atoms as if they were conceptual prerequisites
- using ids outside `def:` and `stmt:`

### `bindings`

Use `bindings` for local setup such as “Let $k$ be a field” or “Let $A$ be an associative algebra.”

Good:

- `notation: k`, `refers_to: def:field`
- `notation: A`, `refers_to: def:associative-algebra`

Bad:

- using `bindings` for claims or evidence
- using non-`def:` ids in `refers_to`
- treating `bindings` as a replacement for `depends_on`

### `supports`

Use `supports` for evidence, justification, examples, or prior arguments.

Good:

- a computation atom supporting an observation
- a previous proposition supporting an insight or conjecture

Bad:

- using `supports` for atoms that are actually prerequisites
- using `supports` to mean that a question has been answered or a conjecture has been settled
- using it as a vague replacement for `related_to`

### `related_to`

Use `related_to` for looser but still meaningful connections.

Good:

- a conceptual insight related to a proposition and a definition
- a question related to a nearby conjecture

Bad:

- encoding strict dependency in `related_to` when `depends_on` should be used
- populating it with arbitrary nearby atoms

### Resolution Fields

Use resolution fields for later statements that settle an earlier statement.

Good:

- a question with `answered_by` pointing to a later proposition
- a conjecture with `resolved_by` pointing to a later proposition
- a conjecture with `refuted_by` pointing to a later statement showing the claim fails

Bad:

- using `supports` instead of a resolution field for final settlement
- populating more than one resolution link field without a strong reason
- using non-`stmt:` ids in resolution links

### `references`

Use `references` for lightweight source handles, not for logical structure.

Good:

- a raw note path such as `raws/2026-04-08.tex`
- a paper handle such as `arXiv:1234.5678`

Bad:

- treating a reference as proof or support by itself
- replacing `depends_on` or `supports` with source handles

## Statement Labels

Canonical statement subtypes are:

- `proposition`
- `conjecture`
- `observation`
- `question`
- `insight`

When a source note uses labels such as theorem, lemma, or corollary, normalize them to `type: proposition`.
