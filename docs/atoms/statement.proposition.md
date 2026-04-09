# `statement.proposition`

## Purpose

A `statement.proposition` atom is a mathematically assertive claim intended to be true or false.

Use when:

- the note presents a definite claim
- the statement is intended to be provable

Examples:

- `In a group, the identity element is unique.`
- `The center of an associative algebra is a subalgebra.`

## Guidance

- the body should read as a claim, not a question or heuristic
- theorem, lemma, and corollary normalize to this subtype
- `depends_on` should list the definitions and prior statements needed to understand the claim
- canonical proposition bodies should be concise and free of note-local staging language
