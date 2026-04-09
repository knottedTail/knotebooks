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
| `body` | Preserve the statement text as the main canonical content field. |
| `depends_on` | Add only atoms required to understand the statement. Use only `def:` or `stmt:` ids. |
| `supports` | Add atoms that provide evidence or justification. May reference any valid atom id. |
| `related_to` | Add meaningful but looser related atoms. May reference any valid atom id. |

## Shared Extraction Procedure

1. Decide whether the source content is genuinely a statement atom rather than concept or process material.
2. Assign a stable `stmt:` id.
3. Classify the subtype by force of assertion:
   - `proposition` for assertive claim
   - `conjecture` for believed but unproven claim
   - `observation` for local or descriptive finding
   - `question` for inquiry or open problem
   - `insight` for heuristic or conceptual interpretation
4. Copy the main statement text into `body`, preserving mathematical wording and LaTeX.
5. Populate `depends_on` only with conceptual prerequisites.
6. Populate `supports` only with evidential or justificatory atoms.
7. Populate `related_to` only with looser meaningful connections.
8. Use empty arrays when no relation data is present.

## Theorem Labels

When the source uses theorem-like presentation labels such as theorem, lemma, or corollary:

- normalize to `type: proposition`
- do not add a separate canonical field for the label in this pass

## What Codex Must Not Infer

Codex must not:

- introduce a new definition inside a statement atom
- use `depends_on` as a bag of nearby references
- confuse evidential support with conceptual prerequisite
- turn an interrogative question into a proposition
- normalize theorem, lemma, or corollary into separate canonical subtypes
