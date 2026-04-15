#!/usr/bin/env python3
"""Fetch recent arXiv metadata for configured categories.

This script reads category settings from a JSON config file, fetches recent
entries from the official arXiv Atom API, and writes a day-named JSON snapshot
under ``derived/arxiv/snapshots/``.

Storage behavior:
  - The main output is ``derived/arxiv/snapshots/YYYY-MM-DD.json``.
  - Re-running the script on the same day updates the same file.
  - Entries are merged by base arXiv identifier, keeping the record with the
    newest ``updated`` timestamp.
  - A small ``derived/arxiv/state.json`` file stores run metadata.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
DEFAULT_USER_AGENT = "knotebooks-arxiv-fetcher/1.0 (+https://arxiv.org/help/api/)"
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_RETRY_COUNT = 4
DEFAULT_RETRY_DELAY_SECONDS = 3.0


# Stored entry fields.
# Each key here is intentionally documented so the output JSON is easy to reuse.
ENTRY_FIELD_DOCS = {
    "arxiv_id": "Base arXiv identifier without version suffix, for example 2501.01234.",
    "versioned_id": "Identifier including version suffix when available, for example 2501.01234v2.",
    "title": "Paper title from the Atom entry.",
    "summary": "Paper abstract from the Atom entry.",
    "authors": "Ordered list of author display names.",
    "affiliations": "Unique list of affiliations exposed by arXiv author records, when present.",
    "categories": "All category identifiers attached to the entry, such as math.QA or math.GT.",
    "primary_category": "Primary arXiv category identifier, when present.",
    "published": "Original publication timestamp for the entry in ISO 8601 format.",
    "updated": "Most recent update timestamp for the retrieved entry in ISO 8601 format.",
    "comment": "Author comment field, when present.",
    "journal_ref": "Journal reference field, when present.",
    "doi": "DOI field, when present.",
    "abs_url": "Canonical arXiv abstract URL for the entry.",
    "pdf_url": "Direct arXiv PDF URL when exposed by the feed.",
}


@dataclass
class Config:
    categories: list[str]
    include_summary: bool
    max_results: int
    sort_by: str
    sort_order: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default="arxiv_config.jsonc",
        help="Path to the JSON config file. Default: %(default)s",
    )
    parser.add_argument(
        "--output-dir",
        default="derived/arxiv/snapshots",
        help="Directory for JSON outputs. Default: %(default)s",
    )
    return parser.parse_args()


def load_config(path: Path) -> Config:
    with path.open("r", encoding="utf-8") as handle:
        raw = json.loads(strip_jsonc_comments(handle.read()))

    categories = raw.get("categories", [])
    if not isinstance(categories, list) or not categories or not all(isinstance(item, str) for item in categories):
        raise ValueError("Config field 'categories' must be a non-empty list of strings.")

    include_summary = bool(raw.get("include_summary", True))
    max_results = int(raw.get("max_results", 100))
    if max_results <= 0:
        raise ValueError("Config field 'max_results' must be positive.")

    sort_by = str(raw.get("sort_by", "lastUpdatedDate"))
    if sort_by not in {"relevance", "lastUpdatedDate", "submittedDate"}:
        raise ValueError("Config field 'sort_by' must be one of relevance, lastUpdatedDate, submittedDate.")

    sort_order = str(raw.get("sort_order", "descending"))
    if sort_order not in {"ascending", "descending"}:
        raise ValueError("Config field 'sort_order' must be 'ascending' or 'descending'.")

    return Config(
        categories=categories,
        include_summary=include_summary,
        max_results=max_results,
        sort_by=sort_by,
        sort_order=sort_order,
    )


def fetch_url(url: str) -> str:
    request = Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
    last_error: Exception | None = None

    for attempt in range(DEFAULT_RETRY_COUNT):
        try:
            with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:  # nosec B310 - this tool intentionally fetches official arXiv URLs
                return response.read().decode("utf-8")
        except HTTPError as exc:
            last_error = exc
            if exc.code == 429 and attempt < DEFAULT_RETRY_COUNT - 1:
                delay = retry_delay_seconds(exc, attempt)
                time.sleep(delay)
                continue
            raise
        except (TimeoutError, URLError) as exc:
            last_error = exc
            if attempt < DEFAULT_RETRY_COUNT - 1:
                time.sleep(DEFAULT_RETRY_DELAY_SECONDS * (attempt + 1))
                continue
            raise

    if last_error is not None:
        raise last_error
    raise RuntimeError("fetch_url failed without raising an explicit error")


def retry_delay_seconds(error: HTTPError, attempt: int) -> float:
    retry_after = error.headers.get("Retry-After")
    if retry_after:
        try:
            return max(float(retry_after), 1.0)
        except ValueError:
            pass
    return DEFAULT_RETRY_DELAY_SECONDS * (attempt + 1)


def strip_jsonc_comments(text: str) -> str:
    """Remove // comments while leaving quoted strings intact."""

    pattern = r'"(?:\\.|[^"\\])*"|//.*'

    def replacer(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.startswith("//"):
            return ""
        return token

    return re.sub(pattern, replacer, text)


def build_query(categories: list[str]) -> str:
    return " OR ".join(f"cat:{category}" for category in categories)


def parse_entry(entry: ET.Element, include_summary: bool) -> dict[str, Any]:
    entry_id_text = text_or_none(entry.find("atom:id", ATOM_NS)) or ""
    versioned_id = entry_id_text.rsplit("/", 1)[-1]
    arxiv_id = versioned_id.split("v", 1)[0]
    categories = [node.attrib["term"] for node in entry.findall("atom:category", ATOM_NS) if "term" in node.attrib]

    authors: list[str] = []
    affiliations: list[str] = []
    for author in entry.findall("atom:author", ATOM_NS):
        name = text_or_none(author.find("atom:name", ATOM_NS))
        if name:
            authors.append(name)
        affiliation = text_or_none(author.find("arxiv:affiliation", ATOM_NS))
        if affiliation and affiliation not in affiliations:
            affiliations.append(affiliation)

    pdf_url = None
    for link in entry.findall("atom:link", ATOM_NS):
        href = link.attrib.get("href")
        title = link.attrib.get("title")
        if href and title == "pdf":
            pdf_url = href
            break

    primary_category = None
    primary = entry.find("arxiv:primary_category", ATOM_NS)
    if primary is not None:
        primary_category = primary.attrib.get("term")

    payload = {
        "arxiv_id": arxiv_id,
        "versioned_id": versioned_id,
        "title": clean_text(text_or_none(entry.find("atom:title", ATOM_NS))),
        "authors": authors,
        "affiliations": affiliations,
        "categories": categories,
        "primary_category": primary_category,
        "published": text_or_none(entry.find("atom:published", ATOM_NS)),
        "updated": text_or_none(entry.find("atom:updated", ATOM_NS)),
        "comment": text_or_none(entry.find("arxiv:comment", ATOM_NS)),
        "journal_ref": text_or_none(entry.find("arxiv:journal_ref", ATOM_NS)),
        "doi": text_or_none(entry.find("arxiv:doi", ATOM_NS)),
        "abs_url": entry_id_text,
        "pdf_url": pdf_url,
    }
    if include_summary:
        payload["summary"] = clean_text(text_or_none(entry.find("atom:summary", ATOM_NS)))
    return payload


def fetch_recent_entries(config: Config) -> list[dict[str, Any]]:
    params = {
        "search_query": build_query(config.categories),
        "start": 0,
        "max_results": config.max_results,
        "sortBy": config.sort_by,
        "sortOrder": config.sort_order,
    }
    feed = fetch_url(f"{ARXIV_API_URL}?{urlencode(params)}")
    root = ET.fromstring(feed)
    return [parse_entry(entry, config.include_summary) for entry in root.findall("atom:entry", ATOM_NS)]
def text_or_none(node: ET.Element | None) -> str | None:
    if node is None or node.text is None:
        return None
    value = node.text.strip()
    return value or None


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    return " ".join(value.split())


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_existing_snapshot(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def choose_newer_entry(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    left_updated = parse_timestamp(left.get("updated"))
    right_updated = parse_timestamp(right.get("updated"))
    if right_updated >= left_updated:
        return right
    return left


def parse_timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        return datetime.min.replace(tzinfo=UTC)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=UTC)


def merge_entries(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for entry in existing + incoming:
        key = str(entry.get("arxiv_id") or entry.get("versioned_id"))
        if key in merged:
            merged[key] = choose_newer_entry(merged[key], entry)
        else:
            merged[key] = entry
    return sorted(
        merged.values(),
        key=lambda item: (
            parse_timestamp(item.get("updated")),
            str(item.get("arxiv_id", "")),
        ),
        reverse=True,
    )
def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    output_dir = Path(args.output_dir)
    ensure_output_dir(output_dir)

    try:
        config = load_config(config_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Failed to load config: {exc}", file=sys.stderr)
        return 1

    now = datetime.now().astimezone()
    derived_dir = output_dir.parent
    snapshot_path = output_dir / f"{now.date().isoformat()}.json"
    state_path = derived_dir / "state.json"

    try:
        entries = fetch_recent_entries(config)
    except (HTTPError, TimeoutError, URLError) as exc:
        state_payload = {
            "last_run_at": now.isoformat(),
            "last_success_at": None,
            "last_snapshot_path": str(snapshot_path),
            "config_path": str(config_path),
            "category_count": len(config.categories),
            "entry_count": 0,
            "last_error": str(exc),
        }
        write_json(state_path, state_payload)
        print(f"Fetch failed after retries: {exc}", file=sys.stderr)
        return 1

    existing_snapshot = load_existing_snapshot(snapshot_path) or {}
    merged_entries = merge_entries(list(existing_snapshot.get("entries", [])), entries)

    snapshot_payload = {
        "date": now.date().isoformat(),
        "fetched_at": now.isoformat(),
        "source_url": ARXIV_API_URL,
        "query": {
            "categories": config.categories,
            "include_summary": config.include_summary,
            "max_results": config.max_results,
            "sort_by": config.sort_by,
            "sort_order": config.sort_order,
        },
        "field_docs": ENTRY_FIELD_DOCS,
        "entries": merged_entries,
    }
    write_json(snapshot_path, snapshot_payload)

    state_payload = {
        "last_run_at": now.isoformat(),
        "last_success_at": now.isoformat(),
        "last_snapshot_path": str(snapshot_path),
        "config_path": str(config_path),
        "category_count": len(config.categories),
        "entry_count": len(merged_entries),
        "last_error": None,
    }
    write_json(state_path, state_payload)

    print(f"Wrote snapshot: {snapshot_path}")
    print(f"Wrote state: {state_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
