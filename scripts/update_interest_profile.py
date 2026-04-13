#!/usr/bin/env python3
"""Update the arXiv interest profile from a checked Markdown review file."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


REVIEW_ITEM_PATTERN = re.compile(
    r"^- \[(?P<checked>[ xX])\] (?P<title>.+?)\n"
    r"  Categories: (?P<categories>.*?)\n"
    r"  Keywords: (?P<keywords>.*?)\n"
    r"  Abstract: (?P<abstract>.*?)\n\n"
    r"  <!-- (?P<meta>\{.*?\}) -->",
    re.MULTILINE | re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", required=True, help="Path to the Markdown review file.")
    parser.add_argument("--profile", default="derived/arxiv/interest_profile.json")
    parser.add_argument("--feedback-dir", default="derived/arxiv/feedback")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def clamp(value: float, minimum: float = -2.0, maximum: float = 8.0) -> float:
    return max(minimum, min(value, maximum))


def parse_review(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    items: list[dict[str, Any]] = []
    for match in REVIEW_ITEM_PATTERN.finditer(text):
        metadata = json.loads(match.group("meta"))
        categories = [part.strip() for part in match.group("categories").split(",") if part.strip() and part.strip() != "None"]
        keywords = [part.strip() for part in match.group("keywords").split(",") if part.strip() and part.strip() != "None"]
        items.append(
            {
                "title": match.group("title").strip(),
                "interested": match.group("checked").lower() == "x",
                "categories": categories,
                "keywords": keywords,
                "metadata": metadata,
            }
        )
    return items


def update_profile(profile: dict[str, Any], review_items: list[dict[str, Any]], review_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    category_weights = {str(k): float(v) for k, v in profile.get("category_weights", {}).items()}
    keyword_weights = {str(k): float(v) for k, v in profile.get("keyword_weights", {}).items()}
    positive_count = int(profile.get("history", {}).get("positive_count", 0))
    negative_count = int(profile.get("history", {}).get("negative_count", 0))

    feedback_items: list[dict[str, Any]] = []
    for item in review_items:
        interested = bool(item["interested"])
        category_delta = 0.4 if interested else -0.1
        keyword_delta = 0.3 if interested else -0.1
        matched_categories = [str(value) for value in item["metadata"].get("matched_categories", item["categories"])]
        matched_keywords = [str(value) for value in item["metadata"].get("matched_keywords", item["keywords"])]
        for category in matched_categories:
            category_weights[category] = round(clamp(category_weights.get(category, 0.0) + category_delta), 3)
        for keyword in matched_keywords:
            keyword_weights[keyword] = round(clamp(keyword_weights.get(keyword, 0.0) + keyword_delta), 3)
        if interested:
            positive_count += 1
        else:
            negative_count += 1
        feedback_items.append(
            {
                "title": item["title"],
                "interested": interested,
                "categories": item["categories"],
                "keywords": item["keywords"],
                "metadata": item["metadata"],
            }
        )

    updated_at = datetime.now().astimezone().isoformat()
    profile_payload = {
        "category_weights": dict(sorted(category_weights.items())),
        "keyword_weights": dict(sorted(keyword_weights.items())),
        "history": {
            "positive_count": positive_count,
            "negative_count": negative_count,
            "last_review_path": str(review_path),
        },
        "updated_at": updated_at,
    }
    feedback_payload = {
        "review_path": str(review_path),
        "reviewed_at": updated_at,
        "items": feedback_items,
    }
    return profile_payload, feedback_payload


def main() -> int:
    args = parse_args()
    review_path = Path(args.review)
    profile_path = Path(args.profile)
    feedback_dir = Path(args.feedback_dir)

    profile = load_json(profile_path)
    review_items = parse_review(review_path)
    profile_payload, feedback_payload = update_profile(profile, review_items, review_path)

    write_json(profile_path, profile_payload)
    feedback_path = feedback_dir / f"{review_path.stem}.json"
    write_json(feedback_path, feedback_payload)

    print(f"Wrote updated profile: {profile_path}")
    print(f"Wrote feedback: {feedback_path}")
    print(f"Processed items: {len(review_items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
