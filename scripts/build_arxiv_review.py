#!/usr/bin/env python3
"""Build a Markdown arXiv review checklist from a daily snapshot."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def strip_jsonc_comments(text: str) -> str:
    pattern = r'"(?:\\.|[^"\\])*"|//.*'

    def replacer(match: re.Match[str]) -> str:
        token = match.group(0)
        return "" if token.startswith("//") else token

    return re.sub(pattern, replacer, text)


@dataclass
class ReviewConfig:
    review_top_n: int
    review_high_score: float
    review_mid_score: float
    category_weights: dict[str, float]
    keyword_weights: dict[str, float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="arxiv_config.jsonc")
    parser.add_argument("--snapshot", help="Path to the day snapshot JSON file.")
    parser.add_argument("--profile", default="derived/arxiv/interest_profile.json")
    parser.add_argument("--output-dir", default="derived/arxiv/review/generated")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def load_jsonc(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.loads(strip_jsonc_comments(handle.read()))


def load_review_config(path: Path) -> ReviewConfig:
    raw = load_jsonc(path)
    return ReviewConfig(
        review_top_n=int(raw.get("review_top_n", 20)),
        review_high_score=float(raw.get("review_high_score", 10.0)),
        review_mid_score=float(raw.get("review_mid_score", 4.0)),
        category_weights={str(k): float(v) for k, v in raw.get("category_weights", {}).items()},
        keyword_weights={str(k): float(v) for k, v in raw.get("keyword_weights", {}).items()},
    )


def ensure_profile(path: Path, config: ReviewConfig) -> dict[str, Any]:
    if path.exists():
        return load_json(path)

    payload = {
        "category_weights": config.category_weights,
        "keyword_weights": config.keyword_weights,
        "history": {
            "positive_count": 0,
            "negative_count": 0,
            "last_review_path": None,
        },
        "processed_review_files": [],
        "updated_at": datetime.now().astimezone().isoformat(),
    }
    write_json(path, payload)
    return payload


def score_entry(entry: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    categories = [str(item) for item in entry.get("categories", [])]
    title = str(entry.get("title", ""))
    summary = str(entry.get("summary") or "")
    category_weights = profile.get("category_weights", {})
    keyword_weights = profile.get("keyword_weights", {})

    matched_categories = [cat for cat in categories if cat in category_weights]
    matched_keywords: list[str] = []
    score = 0.0

    for category in matched_categories:
        score += float(category_weights[category])

    title_lower = title.casefold()
    summary_lower = summary.casefold()
    for keyword, weight in keyword_weights.items():
        key_lower = keyword.casefold()
        keyword_score = 0.0
        if key_lower in title_lower:
            keyword_score += float(weight)
        elif key_lower in summary_lower:
            keyword_score += float(weight) * 0.5
        if keyword_score > 0:
            matched_keywords.append(keyword)
            score += keyword_score

    return {
        "score": round(score, 3),
        "matched_categories": matched_categories,
        "matched_keywords": matched_keywords,
    }


def build_review_markdown(
    review_date: str,
    will_entries: list[dict[str, Any]],
    will_matches: list[dict[str, Any]],
    might_entries: list[dict[str, Any]],
    might_matches: list[dict[str, Any]],
) -> str:
    lines = [
        f"# arXiv Review {review_date}",
        "",
        "Check a box if the paper is interesting to you.",
        "",
    ]

    def append_section(header: str, entries: list[dict[str, Any]], matches: list[dict[str, Any]]) -> None:
        lines.extend([f"## {header}", ""])
        if not entries:
            lines.extend(["No papers in this section today.", "", "---", ""])
            return

        for entry, match in zip(entries, matches, strict=True):
            categories = ", ".join(entry.get("categories", [])) or "None"
            keywords = ", ".join(match["matched_keywords"]) or "None"
            abstract = clean_single_line(entry.get("summary")) or "No abstract stored."
            metadata = {
                "arxiv_id": entry.get("arxiv_id"),
                "versioned_id": entry.get("versioned_id"),
                "score": match["score"],
                "matched_categories": match["matched_categories"],
                "matched_keywords": match["matched_keywords"],
            }
            lines.extend(
                [
                    f"### [ ] {entry.get('title', 'Untitled paper')}",
                    "",
                    f"**Categories:** {categories}  ",
                    f"**Keywords:** {keywords}",
                    "",
                    "**Abstract**  ",
                    abstract,
                    "",
                    f"<!-- {json.dumps(metadata, ensure_ascii=False)} -->",
                    "",
                    "---",
                    "",
                ]
            )

    append_section("Strong Matches", will_entries, will_matches)
    append_section("Possible Matches", might_entries, might_matches)

    return "\n".join(lines).rstrip() + "\n"


def clean_single_line(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def default_snapshot_path() -> Path:
    today = datetime.now().date().isoformat()
    return Path("derived/arxiv") / f"{today}.json"


def main() -> int:
    args = parse_args()
    snapshot_path = Path(args.snapshot) if args.snapshot else default_snapshot_path()
    config = load_review_config(Path(args.config))
    profile = ensure_profile(Path(args.profile), config)
    snapshot = load_json(snapshot_path)
    entries = list(snapshot.get("entries", []))

    scored_pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for entry in entries:
        match = score_entry(entry, profile)
        if match["score"] >= config.review_mid_score:
            scored_pairs.append((entry, match))

    scored_pairs.sort(key=lambda pair: (pair[1]["score"], pair[0].get("updated", "")), reverse=True)
    scored_pairs = scored_pairs[: config.review_top_n]
    will_pairs = [pair for pair in scored_pairs if pair[1]["score"] >= config.review_high_score]
    might_pairs = [pair for pair in scored_pairs if config.review_mid_score <= pair[1]["score"] < config.review_high_score]
    will_entries = [entry for entry, _ in will_pairs]
    will_matches = [match for _, match in will_pairs]
    might_entries = [entry for entry, _ in might_pairs]
    might_matches = [match for _, match in might_pairs]

    review_date = str(snapshot.get("date") or snapshot_path.stem)
    output_path = Path(args.output_dir) / f"{review_date}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_review_markdown(review_date, will_entries, will_matches, might_entries, might_matches),
        encoding="utf-8",
    )

    print(f"Wrote interest profile: {args.profile}")
    print(f"Wrote review: {output_path}")
    print(f"Selected papers: {len(scored_pairs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
