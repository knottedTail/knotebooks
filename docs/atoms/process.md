# `process`

## Purpose

A `process` atom describes mathematical activity rather than final asserted content.

It belongs to:

- `family: process`
- `type: one of computation, attempt, failed_attempt, proof_idea, example, reference_note`

A process atom records how mathematical results are explored, tested, derived, or attempted. It must stay local, single-purpose, and small enough to be reused or linked. It must not be used as a container for a long undivided proof.

## Canonical Shape

```yaml
atom_id: proc:compute-commutator-el-with-f
family: process
type: computation
body: |
  Compute the commutator of $E^l$ with $F$ at the root of unity.
depends_on:
  - def:center
  - stmt:centrality-goal
produces:
  - stmt:commutator-el-f-vanishes
related_to: []
references:
  - kind: raw_file
    locator: raws/2026-04-08.tex
```

## Field Glossary

- `atom_id`
  - Stable identifier for the process atom
  - Must start with `proc:`
  - Should be semantic and should not include the creation date
- `body`
  - Main text of the local mathematical move
  - Must stay focused on one purpose
- `depends_on`
  - Earlier atoms required to understand or execute this step
  - May reference `def:`, `stmt:`, or `proc:` ids
- `produces`
  - Atoms directly yielded by this step
  - May reference any atom family
- `related_to`
  - Meaningful but non-strict links
  - May reference any atom family
- `references`
  - Lightweight source handles for raw files, papers, books, notes, or web sources
  - Each item must contain `kind` and `locator`

All array fields are required and use `[]` when empty.

## Shared Writing Guidance

### `body`

Good `body` values:

- describe one local mathematical move
- read as activity rather than final settled truth
- stay small enough to reuse or link

Bad `body` values:

- contain a whole proof
- merge several unrelated calculations
- state the final theorem as if it were process content

### `depends_on`

Use `depends_on` for atoms that the current process step genuinely requires.

Good:

- a computation depending on the relevant definition and setup statement
- an attempt depending on the conjecture it tries to prove
- a failed attempt depending on the attempt it refines

Bad:

- listing nearby atoms that are not needed
- using `related_to`-style thematic links as prerequisites

### `produces`

Use `produces` when the current step directly yields another atom.

Good:

- a computation producing an observation
- a proof idea producing one or more attempts
- an example producing a computation

Bad:

- using `produces` for vague relevance
- claiming to produce a final statement that is not actually present as a separate atom

### `related_to`

Use `related_to` for meaningful but non-strict connections.

Good:

- two analogous computations
- a failed attempt related to the successful strategy that replaced it

Bad:

- using `related_to` where `depends_on` or `produces` should be used

## Granularity Rule

A process atom should contain one local mathematical move.

Good process atoms:

- one computation
- one attempted reduction
- one failed argument
- one proof strategy
- one example check

Bad process atoms:

- a whole proof
- several unrelated calculations
- an entire page of mixed reasoning
- a complete argument with many distinct steps

If a proof feels too long for one atom, it must be split.

## Proof Decomposition Pattern

Typical decompositions include:

- `proof_idea -> attempt -> computation -> statement`
- `proof_idea -> attempt -> failed_attempt`
- `example -> computation -> observation`

The final mathematical conclusion should usually appear as a `statement` atom, not as a `process` atom.
