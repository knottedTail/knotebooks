# Codex Extraction Contract For `process.reference_note`

Emit `type: reference_note` when the source summarizes or records literature-derived mathematical content.

Use when:

- a note records a result or construction from a paper or book
- a literature block yields one or more canonical `def:` or `stmt:` atoms
- you need a companion provenance atom for a literature-derived definition

Do not use when:

- the source block is only the final canonical definition or proposition and no
  provenance note is needed
- the block is primarily an original local proof computation

Extraction notes:

- a `reference_note` may summarize one literature block while `produces` points to
  the `def:` and `stmt:` atoms extracted from that block
- keep the body provenance-focused rather than duplicating the full canonical
  statement texts
