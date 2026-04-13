# Workflow Reference

## Daily routine

1. Review any files in `derived/arxiv/review/checked/` that have not yet been processed.
2. Apply their checkbox feedback to `derived/arxiv/interest_profile.json`.
3. Fetch today's arXiv snapshot.
4. Generate today's review in `derived/arxiv/review/generated/`.
5. Manually copy today's generated review into `derived/arxiv/review/checked/` when you are ready to review it.
6. Remove the generated review after the checked file exists.
7. Stage `derived/arxiv/snapshots/YYYY-MM-DD.json`, `derived/arxiv/category_taxonomy.json`, `derived/arxiv/review/generated/YYYY-MM-DD.md`, and `derived/arxiv/state.json`, then commit them on a dedicated `codex/...` branch.
8. Merge that branch into `main` only if the branch contains only those routine-output files and the merge is conflict-free.
9. Otherwise stop and leave manual follow-up for the user instead of merging.

## Folder layout

- `derived/arxiv/snapshots/YYYY-MM-DD.json`
  Daily arXiv metadata snapshot.
- `derived/arxiv/review/generated/YYYY-MM-DD.md`
  Generated shortlist. This is temporary and can be deleted after a checked copy exists.
- `derived/arxiv/review/checked/YYYY-MM-DD.md`
  User-annotated shortlist.
- `derived/arxiv/feedback/YYYY-MM-DD.json`
  Parsed checkbox feedback.
- `derived/arxiv/interest_profile.json`
  Learned weights and processed review-file history.

## Expected manual behavior

- Edit only files in `derived/arxiv/review/checked/`.
- Leave files in `derived/arxiv/review/generated/` untouched.
- Copy from `generated/` to `checked/` deliberately; this keeps the transition from system output to user annotation explicit.
- After `checked/YYYY-MM-DD.md` exists, `generated/YYYY-MM-DD.md` can be removed.
- After checking boxes, run the routine again so the checked file is incorporated before generating the next review.
- When saving routine outputs, stage only the daily snapshot, category taxonomy, generated review file, and `derived/arxiv/state.json`.
- Only merge the routine branch when it stays limited to those files and `main` can be merged cleanly.
