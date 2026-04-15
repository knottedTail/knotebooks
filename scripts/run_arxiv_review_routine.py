#!/usr/bin/env python3
"""Run the arXiv review routine with optional manual fetch handoff.

Workflow:
1. Process any unchecked review feedback already present in review/checked/.
2. Attempt to fetch today's arXiv snapshot.
3. If the fetch fails, stop and hand off the exact fetch command to the user.
4. Generate today's review into review/generated/ after a successful fetch.

Manual step after this script:
- Copy the generated review into review/checked/ when ready to annotate it.
- Stage `derived/arxiv/snapshots/YYYY-MM-DD.json`,
  `derived/arxiv/review/generated/YYYY-MM-DD.md`, and `derived/arxiv/state.json`,
  then commit them with a concise message on a dedicated `codex/...` branch.
- Merge that branch into `main` only if it contains only those routine-output files
  and the merge is conflict-free. Otherwise stop for manual follow-up.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


FETCH_HANDOFF_EXIT_CODE = 20


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "phase",
        nargs="?",
        choices=("full", "prepare", "finalize"),
        default="full",
        help="Routine phase to run. Default: %(default)s",
    )
    parser.add_argument("--config", default="arxiv_config.jsonc")
    parser.add_argument("--python", default=sys.executable)
    return parser.parse_args()


def run_step(name: str, cmd: list[str]) -> None:
    rendered = shlex.join(cmd)
    print(f"[start] {name}: {rendered}", flush=True)
    started_at = time.monotonic()
    subprocess.run(cmd, check=True)
    elapsed = time.monotonic() - started_at
    print(f"[done] {name}: {elapsed:.1f}s", flush=True)


def manual_fetch_command(root: Path, config: str) -> str:
    return f"cd {shlex.quote(str(root))} && python3 scripts/check_arxiv_updates.py --config {shlex.quote(config)}"


def finalize_command(root: Path, args: argparse.Namespace) -> str:
    return shlex.join(
        [
            args.python,
            str(root / "scripts/run_arxiv_review_routine.py"),
            "finalize",
            "--config",
            args.config,
        ]
    )


def expected_snapshot_path(root: Path) -> Path:
    return root / "derived/arxiv/snapshots" / f"{datetime.now().date().isoformat()}.json"


def expected_state_path(root: Path) -> Path:
    return root / "derived/arxiv/state.json"


def expected_review_source_path(root: Path) -> Path:
    return root / "derived/arxiv/review/source" / f"{datetime.now().date().isoformat()}.json"


def load_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def cleanup_review_source(root: Path) -> None:
    source_path = expected_review_source_path(root)
    if source_path.exists():
        source_path.unlink()

    source_dir = source_path.parent
    if source_dir.exists() and not any(source_dir.iterdir()):
        source_dir.rmdir()


def validate_fetch_outputs(root: Path, config: str) -> None:
    snapshot_path = expected_snapshot_path(root)
    state_path = expected_state_path(root)
    missing_paths = [path for path in (snapshot_path, state_path) if not path.exists()]
    fetch_cmd = manual_fetch_command(root, config)
    if missing_paths:
        missing_text = ", ".join(str(path) for path in missing_paths)
        raise SystemExit(
            "Cannot finalize arXiv review because the manual fetch outputs are missing: "
            f"{missing_text}\n"
            "This usually means the fetch command was not run yet, or it was run in a different checkout. "
            f"Run exactly:\n{fetch_cmd}"
        )

    state_payload = load_json(state_path)
    expected_snapshot_ref = str(snapshot_path.relative_to(root))
    state_snapshot_ref = str(state_payload.get("last_snapshot_path") or "")
    if state_snapshot_ref != expected_snapshot_ref:
        raise SystemExit(
            "Cannot finalize arXiv review because derived/arxiv/state.json points to "
            f"{state_snapshot_ref!r} instead of {expected_snapshot_ref!r}.\n"
            "This usually means the fetch command wrote files in another checkout or produced stale state. "
            f"Run exactly:\n{fetch_cmd}"
        )


def run_prepare(root: Path, args: argparse.Namespace) -> int:
    run_step("update_interest_profile", [args.python, str(root / "scripts/update_interest_profile.py")])
    print("\nPreparation is complete. Run this command in your normal terminal, then return here and report that you finished:\n")
    print(manual_fetch_command(root, args.config), flush=True)
    return 0


def run_finalize(root: Path, args: argparse.Namespace) -> int:
    validate_fetch_outputs(root, args.config)
    run_step("build_arxiv_review", [args.python, str(root / "scripts/build_arxiv_review.py"), "--config", args.config])
    cleanup_review_source(root)
    return 0


def print_fetch_handoff(root: Path, args: argparse.Namespace) -> None:
    print("\nAutomatic fetch failed. Run this command in your normal terminal from the same worktree:\n")
    print(manual_fetch_command(root, args.config))
    print("\nAfter it succeeds, return here, tell Codex the fetch is done, and run:\n")
    print(finalize_command(root, args), flush=True)


def run_full(root: Path, args: argparse.Namespace) -> int:
    run_step("update_interest_profile", [args.python, str(root / "scripts/update_interest_profile.py")])
    try:
        run_step("check_arxiv_updates", [args.python, str(root / "scripts/check_arxiv_updates.py"), "--config", args.config])
    except subprocess.CalledProcessError:
        print_fetch_handoff(root, args)
        return FETCH_HANDOFF_EXIT_CODE
    run_step("build_arxiv_review", [args.python, str(root / "scripts/build_arxiv_review.py"), "--config", args.config])
    cleanup_review_source(root)
    return 0


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    if args.phase == "prepare":
        return run_prepare(root, args)
    if args.phase == "finalize":
        return run_finalize(root, args)
    return run_full(root, args)


if __name__ == "__main__":
    raise SystemExit(main())
