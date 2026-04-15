# Workflow Reference

## Daily routine

1. Review any files in `derived/arxiv/review/checked/` that have not yet been processed.
2. Apply their checkbox feedback to `derived/arxiv/interest_profile.json`.
3. Run the routine prepare phase so the automation updates local state and prints the exact manual fetch command for the current worktree.
4. Run the printed fetch command in that same worktree from a normal terminal session.
5. Return to the same thread and run the routine finalize phase.
6. Generate today's review in `derived/arxiv/review/generated/`.
7. Manually copy today's generated review into `derived/arxiv/review/checked/` when you are ready to review it.
8. Remove the generated review after the checked file exists.
9. Stage `derived/arxiv/snapshots/YYYY-MM-DD.json`, `derived/arxiv/review/generated/YYYY-MM-DD.md`, and `derived/arxiv/state.json`, then commit them on a dedicated `codex/...` branch.
10. Merge that branch into `main` only if the branch contains only those routine-output files and the merge is conflict-free.
11. Otherwise stop and leave manual follow-up for the user instead of merging.

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
- When the automation pauses after prepare, run the exact fetch command it printed. Do not substitute another checkout path.
- Copy from `generated/` to `checked/` deliberately; this keeps the transition from system output to user annotation explicit.
- After `checked/YYYY-MM-DD.md` exists, `generated/YYYY-MM-DD.md` can be removed.
- After checking boxes, run the routine again so the checked file is incorporated before generating the next review.
- When saving routine outputs, stage only the daily snapshot, generated review file, and `derived/arxiv/state.json`.
- Only merge the routine branch when it stays limited to those files and `main` can be merged cleanly.
