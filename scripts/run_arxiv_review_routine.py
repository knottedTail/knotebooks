#!/usr/bin/env python3
"""Run the arXiv review routine up to generated review creation.

Workflow:
1. Process any unchecked review feedback already present in review/checked/.
2. Fetch today's arXiv snapshot.
3. Generate today's review into review/generated/.

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
import shlex
import subprocess
import sys
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
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


def main() -> int:
    args = parse_args()
    root = Path.cwd()

    run_step("update_interest_profile", [args.python, str(root / "scripts/update_interest_profile.py")])
    run_step("check_arxiv_updates", [args.python, str(root / "scripts/check_arxiv_updates.py"), "--config", args.config])
    run_step("build_arxiv_review", [args.python, str(root / "scripts/build_arxiv_review.py"), "--config", args.config])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
