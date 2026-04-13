#!/usr/bin/env python3
"""Copy a generated arXiv review into the checked folder if needed."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="Review date in YYYY-MM-DD format. Defaults to today.")
    parser.add_argument("--generated-dir", default="derived/arxiv/review/generated")
    parser.add_argument("--checked-dir", default="derived/arxiv/review/checked")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    review_date = args.date or datetime.now().date().isoformat()
    source_path = Path(args.generated_dir) / f"{review_date}.md"
    target_path = Path(args.checked_dir) / f"{review_date}.md"

    if not source_path.exists():
        raise SystemExit(f"Generated review not found: {source_path}")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists():
        print(f"Checked review already exists: {target_path}")
        return 0

    shutil.copyfile(source_path, target_path)
    print(f"Copied review to: {target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
