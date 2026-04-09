# Codex Extraction Contract For `statement.question`

Emit `type: question` when the source is explicitly asking something mathematically unknown or unclear.

Use when:

- the note is interrogative
- the note expresses an open problem or unresolved issue

Do not use when:

- the statement already asserts an answer or expectation: use another statement subtype

Extraction notes:

- prefer `answered_by` for later `stmt:` atoms that answer the question
- set `resolution_status` to `answered` only when `answered_by` is populated
