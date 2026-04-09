# Codex Extraction Contract For `statement`

## Purpose

This document tells Codex when to emit a `statement` atom and how to fill its shared fields from source-side notes.

## Emit A `statement` Atom When

Emit a statement atom when the source expresses:

- a claim
- a conjecture
- an observation
- a question
- or a conceptual insight

Do not emit a statement atom when the source is primarily:

- defining a new concept
- assigning notation only
- recording local assumptions only
- documenting a computation or failed attempt as process material

## Shared Field Mapping

| Atom field | Extraction rule |
| --- | --- |
| `atom_id` | Use a stable semantic id with prefix `stmt:`. |
| `family` | Always `statement`. |
| `type` | Choose one of `proposition`, `conjecture`, `observation`, `question`, `insight`. |
| `body` | Preserve the mathematically essential statement text as the main canonical content field. Remove note-local conversational framing when it is not mathematically necessary. |
| `depends_on` | Add only atoms required to understand the statement. Use only `def:` or `stmt:` ids. |
| `bindings` | Add local symbol-to-definition assignments when the source says things like “Let $k$ be a field.” Each item must contain `notation` and a `def:` id in `refers_to`. |
| `supports` | Add atoms that provide evidence or justification. May reference any valid atom id. Do not use this field for final settlement of a question or conjecture. |
| `related_to` | Add meaningful but looser related atoms. May reference any valid atom id. |
| `answered_by` | Add later `stmt:` atoms that answer a question. Use `[]` when empty. |
| `resolved_by` | Add later `stmt:` atoms that positively settle a statement. Use `[]` when empty. |
| `refuted_by` | Add later `stmt:` atoms that negatively settle a statement. Use `[]` when empty. |
| `resolution_status` | Set to `open`, `answered`, `resolved`, or `refuted` so it agrees with the populated resolution links. |
| `references` | Add lightweight source handles. Each item must contain `kind` and `locator`. Use `[]` when no source handles are available. |

## Shared Extraction Procedure

1. Decide whether the source content is genuinely a statement atom rather than concept or process material.
2. Assign a stable `stmt:` id.
3. Classify the subtype by force of assertion:
   - `proposition` for assertive claim
   - `conjecture` for believed but unproven claim
   - `observation` for local or descriptive finding
   - `question` for inquiry or open problem
   - `insight` for heuristic or conceptual interpretation
4. Copy the mathematically essential statement text into `body`, preserving mathematical wording and LaTeX while removing note-local framing that does not change the meaning.
5. Populate `depends_on` only with conceptual prerequisites.
6. Populate `bindings` only when the source explicitly introduces a local symbol bound to a mathematical object.
7. Populate `supports` only with evidential or justificatory atoms.
8. Populate `related_to` only with looser meaningful connections.
9. Populate `answered_by`, `resolved_by`, and `refuted_by` only when later statements actually settle the current statement.
10. Set `resolution_status` so it agrees with the populated resolution links.
11. Add lightweight `references` for raw files, papers, books, notes, or web sources when available.
12. Use empty arrays when no relation or reference data is present.

## Theorem Labels

When the source uses theorem-like presentation labels such as theorem, lemma, or corollary:

- normalize to `type: proposition`
- do not add a separate canonical field for the label in this pass

## What Codex Must Not Infer

Codex must not:

- introduce a new definition inside a statement atom
- use `depends_on` as a bag of nearby references
- invent local bindings that the source does not actually introduce
- confuse evidential support with conceptual prerequisite
- confuse evidential support with logical resolution
- turn an interrogative question into a proposition
- normalize theorem, lemma, or corollary into separate canonical subtypes
