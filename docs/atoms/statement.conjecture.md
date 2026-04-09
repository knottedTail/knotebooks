# `statement.conjecture`

## Purpose

A `statement.conjecture` atom is an unproven statement believed to be true.

Use when:

- the statement is speculative
- the note expresses expectation or belief without proof

Examples:

- `The large center determines the Poisson structure.`
- `This construction should be equivalent to Hamiltonian reduction.`

## Guidance

- the body should remain assertive, but clearly speculative in force
- `supports` is especially useful for evidence from examples, computations, or earlier observations
- use `resolved_by` when a later statement establishes the conjecture
- use `refuted_by` when a later statement shows the conjecture fails
- `resolution_status` should normally be `open`, `resolved`, or `refuted`
