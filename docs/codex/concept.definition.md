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
| `unit_id` | Use the source semantic id. For this atom type it must start with `def:`. |
| `family` | Always `concept`. |
| `type` | Always `definition`. |
| `name` | Extract the canonical concept name, not the local title verbatim when the title contains parameters or assumptions. |
| `body` | Preserve the defining text as a single LaTeX-preserving text field. |
| `based_on` | Add only explicit or clearly necessary definition dependencies. Use only `def:` ids. |
| `axiomatic` | Set to `true` only when no meaningful dependencies were identified. |
| `aliases` | Add only true synonyms found in the source or clearly equivalent surrounding text. |
| `notation_ids` | Add only when separate notation atoms already exist or are extracted in the same pass. |
| `context_ids` | Add only when separate context atoms already exist or are extracted in the same pass. |
| `tags` | Carry over source tags when they are present and meaningful. |
| `related_unit_ids` | Use for untyped cross-links that matter but are not typed definition dependencies. |
| `confidence` | Use when extraction is uncertain; omit when confidence is not being recorded. |
| `provenance` | Always populate from the source note and extraction run metadata. |

## Extraction Procedure

1. Identify whether the source block truly defines an object.
2. Keep the source semantic id as `unit_id`.
3. Rewrite the displayed source title into a canonical `name` when needed.
4. Copy the defining text into `body`, preserving LaTeX math and mathematical wording.
5. Add `based_on` only for definition dependencies, not for every referenced atom.
6. Decide `axiomatic` from the dependency picture:
   - `true` when no meaningful definition dependencies were identified
   - `false` when dependencies exist
   - `false` when dependencies may exist but remain unresolved
7. Add `notation_ids` or `context_ids` only when those are genuinely separate atoms.
8. Fill provenance last and do not omit it.

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
- turn notation-only material into a definition
- move proof, evidence, or strategy text into `body`
- create `notation_ids` or `context_ids` unless those atoms are actually present or being extracted
- silently normalize away mathematical LaTeX in `body`

## Current Source Mapping

The current source-side authoring format uses LaTeX `definitionitem` blocks.

- `\begin{definitionitem}{<id>}{<title>}{<tags>}` provides the id, title hint, and tags
- the block contents provide the definition text
- explicit references such as `\defref{...}` may support `based_on` when they indicate true definition dependencies

The source title is not a canonical stored field in `concept.definition` v1.
