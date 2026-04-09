# Codex Extraction Contract For `statement.conjecture`

Emit `type: conjecture` when the source presents a statement believed to be true but not yet proven.

Use when:

- the note signals expectation, belief, or plausible truth
- the source presents evidence without proof

Do not use when:

- the note states the claim as established fact: use `proposition`
- the note merely asks whether the claim holds: use `question`

Extraction notes:

- use `resolved_by` when a later statement establishes the conjecture
- use `refuted_by` when a later statement shows the conjecture fails
- do not use `answered_by` for conjectures
