# Codex Extraction Contract For `concept.definition`

## Purpose

This document tells Codex when to emit a `concept.definition` atom and how to fill its fields from source-side notes.

## Emit A `concept.definition` Atom When

Emit a definition atom when the source introduces what a mathematical object is.

Typical signals:

- "A ... is ..."
- "We define ... to be ..."
- "Call ... a ... if ..."

Do not emit a definition atom when the block is primarily:

- symbol assignment only
- local assumptions only
- a theorem-like claim
- a question
- a computation, attempt, or proof fragment

## Field Mapping

| Atom field | Extraction rule |
| --- | --- |
| `atom_id` | Use a stable semantic id. For this atom type it must start with `def:` and should not encode the creation date. |
| `family` | Always `concept`. |
| `type` | Always `definition`. |
| `name` | Extract the canonical concept name, not the local title verbatim when the title contains parameters or assumptions. Duplicate names are allowed. |
| `body` | Preserve the defining text as a single LaTeX-preserving text field. When `name` is ambiguous, the opening sentence must disambiguate immediately. |
| `based_on` | Add only explicit or clearly necessary definition dependencies. Use only `def:` ids. For ambiguous repeated names, this is the main mathematical source of disambiguation when such a basis exists. |
| `axiomatic` | Set to `true` only when no meaningful dependencies were identified. |
| `aliases` | Add only true synonyms found in the source or clearly equivalent surrounding text. |

## Extraction Procedure

1. Identify whether the source block truly defines an object.
2. Keep or normalize the source semantic id as `atom_id`, removing date text when present.
3. Rewrite the displayed source title into a canonical `name` when needed. Duplicate `name` values are allowed.
4. If the name is ambiguous, make `atom_id` sense-bearing rather than generic.
5. Copy the defining text into `body`, preserving LaTeX math and mathematical wording.
6. If the name is ambiguous, make the opening sentence of `body` identify the sense immediately.
7. Add `based_on` only for definition dependencies, not for every referenced atom.
8. For ambiguous repeated names, use `based_on` to capture the mathematically prior basis whenever such a basis exists.
9. Decide `axiomatic` from the dependency picture:
   - `true` when no meaningful definition dependencies were identified
   - `false` when dependencies exist
   - `false` when dependencies may exist but remain unresolved
10. Add `aliases` only when the source provides a true synonym.

## When To Leave `based_on` Empty

Leave `based_on: []` in either of these cases:

- the definition is treated as axiomatic in the current extraction context
- the dependency picture is still unresolved

Then set:

- `axiomatic: true` for the first case
- `axiomatic: false` for the second case

## What Codex Must Not Infer

Codex must not:

- invent hidden dependencies just because related concepts exist in the same note
- copy local assumptions like "over `k`" into the canonical `name`
- assume `name` must be globally unique
- turn notation-only material into a definition
- move proof, evidence, or strategy text into `body`
- create notation or context links inside `concept.definition`
- leave an ambiguous repeated name unexplained in both `atom_id` and the opening sentence of `body`
- silently normalize away mathematical LaTeX in `body`

## Validator Semantics

Schema validation remains unchanged, but future semantic validation should:

- reject self-reference in `based_on`
- reject non-`def:` ids in `based_on`
- warn when two definition atoms share the same `name` and the same `based_on` set
- warn when duplicate `name` occurs with a generic `atom_id`
- warn when duplicate `name` occurs with empty `based_on` and the opening sentence of `body` does not disambiguate the sense

## Current Source Mapping

The current source-side authoring format uses LaTeX `definitionitem` blocks.

- `\begin{definitionitem}{<id>}{<title>}{<tags>}` provides the id, title hint, and tags
- the block contents provide the definition text
- explicit references such as `\defref{...}` may support `based_on` when they indicate true definition dependencies

The source title is not a canonical stored field in `concept.definition` v1.

When writing the canonical YAML file, use `<atom_id>.yaml` as the filename.
