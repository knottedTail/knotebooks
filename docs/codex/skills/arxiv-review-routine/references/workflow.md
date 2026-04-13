# Workflow Reference

## Daily routine

1. Review any files in `derived/arxiv/review/checked/` that have not yet been processed.
2. Apply their checkbox feedback to `derived/arxiv/interest_profile.json`.
3. Fetch today's arXiv snapshot.
4. Generate today's review in `derived/arxiv/review/generated/`.
5. Copy today's generated review into `derived/arxiv/review/checked/` if the checked copy is missing.

## Folder layout

- `derived/arxiv/YYYY-MM-DD.json`
  Daily arXiv metadata snapshot.
- `derived/arxiv/review/generated/YYYY-MM-DD.md`
  Generated shortlist.
- `derived/arxiv/review/checked/YYYY-MM-DD.md`
  User-annotated shortlist.
- `derived/arxiv/feedback/YYYY-MM-DD.json`
  Parsed checkbox feedback.
- `derived/arxiv/interest_profile.json`
  Learned weights and processed review-file history.

## Expected manual behavior

- Edit only files in `derived/arxiv/review/checked/`.
- Leave files in `derived/arxiv/review/generated/` untouched.
- After checking boxes, run the routine again so the checked file is incorporated before generating the next review.
