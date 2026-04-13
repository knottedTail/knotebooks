---
name: writing-feedback
description: Review, critique, and polish English writing, including daily logs, diary-style notes, research logs, mathematical writing, proof sketches, and expository prose. Use when Codex should read writing from repo-relative paths such as resources/raws/... and produce structured feedback with grammar corrections, style guidance, mathematical-writing critique when relevant, and a polished rewrite saved to derived/writing-feedback/... as a Markdown file.
---

# Writing Feedback

Provide careful, teacher-like feedback on the user's writing while preserving meaning, intent, and voice.

Treat this skill as both an English-writing coach and a mathematical-writing reviewer. Adapt the review to the genre: informal logs should stay natural, while formal exposition should become precise and polished.

## Workflow

1. Identify the source text.
2. Classify the writing genre.
3. Review the text for language and structure.
4. Review mathematical writing quality when relevant.
5. Produce a structured feedback file in Markdown.

## Step 1: Identify the source text

- Prefer reading the user's target file directly when they mention a path under `resources/raws/`.
- If the user provides text inline, review that text directly.
- Do not modify the source file.
- If multiple files are mentioned, review only the ones the user asked for.
- Resolve paths relative to the repository root.

## Step 2: Classify the writing genre

Classify the input before critiquing it:

- `daily-log`: short progress report, rough notes, or status update
- `diary-style`: reflective writing, personal tone, mixed with technical comments
- `math-research-log`: research progress with definitions, questions, computations, proof ideas, or conjectures
- `formal-math-writing`: theorem, lemma, proof, definition, exposition, or paper-style prose
- `general-english-writing`: non-mathematical prose such as emails, summaries, reflective writing, or planning notes

Use the genre to set the standard:

- For `daily-log` and `diary-style`, improve grammar, readability, and organization without over-formalizing the voice.
- For `math-research-log`, preserve exploratory tone but make statements, notation, and reasoning easier to follow.
- For `formal-math-writing`, prioritize precision, consistency, concision, and mathematical rigor.
- For `general-english-writing`, prioritize naturalness, clarity, tone, and structure.

## Step 3: Review language and writing quality

Always check the following:

- grammar, spelling, article usage, singular/plural agreement, tense consistency
- awkward phrasing, unnatural collocations, and unclear pronoun references
- sentence flow, paragraph coherence, and transitions
- concision and repetition
- register and tone for the genre

When giving grammar feedback:

- quote the problematic phrase or sentence
- explain the issue briefly
- suggest a natural correction

When giving style feedback:

- explain why the original sounds awkward, vague, too informal, or too wordy
- prefer revisions that sound natural in academic English
- preserve the author's intended meaning

## Step 4: Review mathematical writing quality

Apply this section only when the text contains mathematical content.

Check for:

- undefined notation or symbols introduced without context
- inconsistent notation or naming
- ambiguous claims
- unsupported logical jumps
- weak distinction between intuition, claim, and proof
- unclear statement scope, assumptions, or quantifiers
- overloaded sentences that mix several mathematical ideas at once
- imprecise references such as "this", "it", or "the structure" when the referent is unclear

Critique mathematical writing, not the mathematics itself, unless a mathematical error is obvious from the text.

If the math meaning is uncertain:

- do not silently rewrite it into a stronger or different claim
- mark the passage as ambiguous
- offer one safe rewrite and, if useful, one note about what needs clarification

## Step 5: Produce the feedback file

Write the output as Markdown by default.

Save feedback to:

- source under `resources/raws/...`
- output under `derived/writing-feedback/...`

Mirror the relative source path and append `-feedback.md` to the stem.

Examples:

- `resources/raws/logs/today.md` -> `derived/writing-feedback/logs/today-feedback.md`
- `resources/raws/2026/apr/note.tex` -> `derived/writing-feedback/2026/apr/note-feedback.md`

Create parent directories as needed.

## Output format

Use this section order unless the user asks for a different format.

### 1. Overview

Give a short summary of the writing's strengths and main improvement areas.

### 2. Grammar Corrections

For each correction, present the original and polished sentences in a highly contrasting left-aligned layout, and highlight the changed word or phrase in both sentences with bold markup.

Use this exact structure:

```md
<div align="left"><strong>Original</strong></div>

<div align="left">[original sentence with the changed phrase in **bold**]</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">[polished sentence with the revised phrase in **bold**]</div>

> **Reason**
> [brief explanation]

<br>
<br>
```

Leave the extra `<br>` spacing between correction items so each pair is visibly separated.

Highlight only the part that changed, not the whole sentence, unless the entire sentence had to be rewritten.

### 3. Style and English Feedback

Explain:

- what sounds unnatural or unclear
- how to make the writing more idiomatic or formal
- how to improve paragraph and sentence flow

### 4. Mathematical Writing Feedback

Include this section only if the text contains mathematical content.

Comment on:

- precision
- notation
- logical flow
- statement clarity
- exposition quality

### 5. Polished Revision

Provide a revised version of the full text.

Rules for the revision:

- preserve the meaning and level of certainty
- preserve exploratory tone for logs when appropriate
- improve clarity and grammar
- split overloaded sentences when helpful
- do not invent new mathematical claims

### 6. Next-Time Checklist

End with a short checklist of repeatable writing habits tailored to the sample.

## File-writing guidance

- Default to Markdown output.
- Use plain headings and bullet lists, except that the `Grammar Corrections` section should use left-aligned HTML blocks plus a callout-style `Reason` block for contrast.
- Include the source file path near the top of the feedback file.
- If the source is LaTeX, keep inline math readable in Markdown.
- Do not convert the entire feedback file to LaTeX unless the user explicitly asks.

## References

- Read [references/review-rubric.md](references/review-rubric.md) for the evaluation rubric.
- Read [references/genre-guidance.md](references/genre-guidance.md) when deciding how formal the feedback should be.
- Read [references/output-template.md](references/output-template.md) when drafting the feedback file structure.
