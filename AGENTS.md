# AGENTS.md

## Change Protocol

For any repository modification:

1. Inspect the current state before proposing changes.
2. Present a concrete plan before making changes.
3. Do not edit tracked files until the user explicitly approves the plan.
4. After approval, implement only the approved plan.
5. If the task changes materially after approval, stop and present a revised plan before continuing.
6. Before committing, create a dedicated branch for the work.
7. Agent-created branches should use the `codex/` prefix unless the user requests a different naming scheme.
8. Commit changes with a concise, descriptive commit message.
9. Do not include unrelated local changes in the branch commit.

## Merge Guidance

- Do not merge immediately after committing.
- Merge only after the approved plan is completed.
- Merge only after the relevant verification has passed, or any unverified items have been explicitly noted.
- Before merging, confirm the branch contains only changes related to the approved task.
- If the implemented work differs materially from the approved plan, stop and get approval before merging.
