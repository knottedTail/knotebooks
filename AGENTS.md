# AGENTS.md

## Change Protocol

For any repository modification:

1. Inspect the current state before proposing changes.
2. Present a concrete plan before making changes.
3. After approval, implement only the approved plan.
4. If the task changes materially after approval, stop and present a revised plan before continuing.
5. At the start of any new repo task that is likely to lead to tracked-file changes, check whether the current branch is appropriate for that task.
6. If the current branch belongs to an unrelated task, create or switch to a proper dedicated branch immediately, even if the work is still at the planning stage.
7. A new thread does not justify reusing an unrelated branch; branch choice must follow task scope, not thread history.
8. Agent-created branches should use the `codex/` prefix unless the user requests a different naming scheme.
9.  Before committing, confirm you are already on the proper dedicated work branch.
10. After applying an approved repo modification, commit the relevant changes immediately.
11. Commit changes with a concise, descriptive commit message.
12. Do not include unrelated local changes in the branch commit.
13. Do not modify any files in resources/.

### Daily Routine Exception

- The established daily arXiv review routine may update its expected tracked output files without requiring a new per-run approval each day.
- This exception applies only to routine output files under `derived/arxiv/` that are produced by the approved arXiv workflow.
- This exception does not apply to source-code changes, skill/instruction changes, files in `resources/`, or any tracked files outside the routine's expected output scope.

## Merge Guidance

- Do not merge immediately after committing.
- Merge only after the approved plan is completed.
- Merge only after the relevant verification has passed, or any unverified items have been explicitly noted.
- Before merging, confirm the branch contains only changes related to the approved task.
- If the implemented work differs materially from the approved plan, stop and get approval before merging.
