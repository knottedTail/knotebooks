# Codex Extraction Contract For `process`

## Purpose

This document tells Codex when to emit a `process` atom and how to fill its shared fields from source-side notes.

## Emit A `process` Atom When

Emit a process atom when the source records mathematical activity such as:

- a computation
- an attempt
- a failed attempt
- a proof strategy
- a concrete example used for testing
- a literature-derived note

Do not emit a process atom when the source is primarily:

- defining a new concept
- stating a final proposition, conjecture, observation, question, or insight
- introducing notation only

## Shared Field Mapping

| Atom field | Extraction rule |
| --- | --- |
| `atom_id` | Use a stable semantic id with prefix `proc:`. |
| `family` | Always `process`. |
| `type` | Choose one of `computation`, `attempt`, `failed_attempt`, `proof_idea`, `example`, `reference_note`. |
| `body` | Preserve the local mathematical move as the main canonical content field. |
| `depends_on` | Add atoms required to understand or execute the step. |
| `produces` | Add atoms directly yielded by the step. |
| `related_to` | Add meaningful but looser related atoms. |
| `references` | Add lightweight source handles. Each item must contain `kind` and `locator`. Use `[]` when no source handles are available. |

## Shared Extraction Procedure

1. Decide whether the source content is genuinely process material rather than concept or statement material.
2. Assign a stable `proc:` id.
3. Classify the subtype by activity:
   - `computation` for explicit calculation or derivation
   - `attempt` for a trial step toward a goal
   - `failed_attempt` for a trial step that breaks
   - `proof_idea` for strategic route
   - `example` for a concrete mathematical instance
   - `reference_note` for literature-derived content
4. Copy the local mathematical move into `body`.
5. Populate `depends_on` only with genuinely required earlier atoms.
6. Populate `produces` only with atoms directly yielded by the current step.
7. Populate `related_to` only with looser meaningful connections.
8. Add lightweight `references` for raw files, papers, books, notes, or web sources when available.
9. Use empty arrays when no relation or reference data is present.

## What Codex Must Not Infer

Codex must not:

- turn a whole proof into one process atom
- invent missing intermediate steps not present in the source
- turn a final settled claim into process content when it should be a statement atom
- use `produces` for vague thematic similarity
