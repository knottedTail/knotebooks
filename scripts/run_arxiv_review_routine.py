#!/usr/bin/env python3
"""Run the full arXiv review routine.

Workflow:
1. Process any unchecked review feedback already present in review/checked/.
2. Fetch today's arXiv snapshot.
3. Generate today's review into review/generated/.
4. Create today's checked copy if it does not already exist.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="arxiv_config.jsonc")
    parser.add_argument("--python", default=sys.executable)
    return parser.parse_args()


def run_step(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    args = parse_args()
    root = Path.cwd()

    run_step([args.python, str(root / "scripts/update_interest_profile.py")])
    run_step([args.python, str(root / "scripts/check_arxiv_updates.py"), "--config", args.config])
    run_step([args.python, str(root / "scripts/build_arxiv_review.py"), "--config", args.config])
    run_step([args.python, str(root / "scripts/prepare_arxiv_review_copy.py")])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
