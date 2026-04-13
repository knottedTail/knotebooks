#!/usr/bin/env python3
"""Fetch recent arXiv metadata for configured categories.

This script reads category settings from a JSON config file, fetches recent
entries from the official arXiv Atom API, optionally refreshes a local copy of
the official arXiv category taxonomy, and writes a day-named JSON snapshot
under ``derived/arxiv/``.

Storage behavior:
  - The main output is ``derived/arxiv/YYYY-MM-DD.json``.
  - Re-running the script on the same day updates the same file.
  - Entries are merged by base arXiv identifier, keeping the record with the
    newest ``updated`` timestamp.
  - A small ``derived/arxiv/state.json`` file stores run metadata.
  - ``derived/arxiv/category_taxonomy.json`` stores the locally cached list of
    official arXiv subject categories such as ``math.QA`` and ``math.GT``.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen
import xml.etree.ElementTree as ET


ARXIV_API_URL = "https://export.arxiv.org/api/query"
ARXIV_TAXONOMY_URL = "https://arxiv.org/category_taxonomy"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


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


# Stored category-taxonomy fields.
TAXONOMY_FIELD_DOCS = {
    "id": "Category identifier such as math.QA or cs.AI.",
    "name": "Human-readable category name.",
    "group": "Top-level arXiv group heading, such as Mathematics or Computer Science.",
    "archive": "Archive identifier when present, such as math or cs.",
    "archive_name": "Human-readable archive name when present.",
    "description": "Category description text from the official taxonomy page when present.",
}


@dataclass
class Config:
    categories: list[str]
    max_results: int
    sort_by: str
    sort_order: str
    refresh_taxonomy: bool


class TaxonomyHTMLParser(HTMLParser):
    """Extract category metadata from https://arxiv.org/category_taxonomy.

    The taxonomy page is structured as top-level groups (``<h2>``), optional
    archive headings (``<h3>``), and category headings (``<h4>``) followed by
    description paragraphs. This parser records those relationships and emits a
    flat category list that is straightforward to serialize as JSON.
    """

    def __init__(self) -> None:
        super().__init__()
        self.categories: list[dict[str, str | None]] = []
        self._capture_tag: str | None = None
        self._buffer: list[str] = []
        self._current_group: str | None = None
        self._current_archive_name: str | None = None
        self._current_archive: str | None = None
        self._current_category: dict[str, str | None] | None = None
        self._skip_h3_hint = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"h2", "h3", "h4", "p"}:
            self._capture_tag = tag
            self._buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag != self._capture_tag:
            return

        text = " ".join("".join(self._buffer).split()).strip()
        self._capture_tag = None
        self._buffer = []
        if not text:
            return

        if tag == "h2":
            if text in {"Classification guide", "Group Name", "quick links"}:
                return
            self._current_group = text
            self._current_archive = None
            self._current_archive_name = None
            self._skip_h3_hint = False
            return

        if tag == "h3":
            if text.startswith("Archive Name"):
                self._skip_h3_hint = True
                return
            archive_name, archive_id = parse_archive_heading(text)
            self._current_archive_name = archive_name
            self._current_archive = archive_id
            return

        if tag == "h4":
            if text == "Category Name (Category ID)" or self._current_group is None:
                return
            category_id, category_name = parse_category_heading(text)
            if category_id is None:
                return
            inferred_archive = self._current_archive or category_id.split(".", 1)[0]
            if self._current_archive is None and self._skip_h3_hint:
                self._current_archive = inferred_archive
                self._current_archive_name = self._current_group
            self._current_category = {
                "id": category_id,
                "name": category_name,
                "group": self._current_group,
                "archive": inferred_archive,
                "archive_name": self._current_archive_name,
                "description": "",
            }
            self.categories.append(self._current_category)
            return

        if tag == "p" and self._current_category is not None:
            description = self._current_category["description"] or ""
            self._current_category["description"] = (description + " " + text).strip()

    def handle_data(self, data: str) -> None:
        if self._capture_tag is not None:
            self._buffer.append(data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default="arxiv_config.json",
        help="Path to the JSON config file. Default: %(default)s",
    )
    parser.add_argument(
        "--output-dir",
        default="derived/arxiv",
        help="Directory for JSON outputs. Default: %(default)s",
    )
    parser.add_argument(
        "--skip-taxonomy-refresh",
        action="store_true",
        help="Do not refresh category_taxonomy.json during this run.",
    )
    return parser.parse_args()


def load_config(path: Path) -> Config:
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)

    categories = raw.get("categories", [])
    if not isinstance(categories, list) or not categories or not all(isinstance(item, str) for item in categories):
        raise ValueError("Config field 'categories' must be a non-empty list of strings.")

    max_results = int(raw.get("max_results", 100))
    if max_results <= 0:
        raise ValueError("Config field 'max_results' must be positive.")

    sort_by = str(raw.get("sort_by", "lastUpdatedDate"))
    if sort_by not in {"relevance", "lastUpdatedDate", "submittedDate"}:
        raise ValueError("Config field 'sort_by' must be one of relevance, lastUpdatedDate, submittedDate.")

    sort_order = str(raw.get("sort_order", "descending"))
    if sort_order not in {"ascending", "descending"}:
        raise ValueError("Config field 'sort_order' must be 'ascending' or 'descending'.")

    refresh_taxonomy = bool(raw.get("refresh_taxonomy", True))
    return Config(
        categories=categories,
        max_results=max_results,
        sort_by=sort_by,
        sort_order=sort_order,
        refresh_taxonomy=refresh_taxonomy,
    )


def fetch_url(url: str) -> str:
    with urlopen(url) as response:  # nosec B310 - this tool intentionally fetches official arXiv URLs
        return response.read().decode("utf-8")


def build_query(categories: list[str]) -> str:
    return " OR ".join(f"cat:{category}" for category in categories)


def parse_entry(entry: ET.Element) -> dict[str, Any]:
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

    return {
        "arxiv_id": arxiv_id,
        "versioned_id": versioned_id,
        "title": clean_text(text_or_none(entry.find("atom:title", ATOM_NS))),
        "summary": clean_text(text_or_none(entry.find("atom:summary", ATOM_NS))),
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
    return [parse_entry(entry) for entry in root.findall("atom:entry", ATOM_NS)]


def fetch_taxonomy() -> list[dict[str, str | None]]:
    parser = TaxonomyHTMLParser()
    parser.feed(fetch_url(ARXIV_TAXONOMY_URL))
    parser.close()
    return sorted(parser.categories, key=lambda item: item["id"] or "")


def parse_archive_heading(text: str) -> tuple[str | None, str | None]:
    if "(" in text and text.endswith(")"):
        name, archive = text.rsplit("(", 1)
        return name.strip(), archive[:-1].strip()
    return text.strip(), None


def parse_category_heading(text: str) -> tuple[str | None, str | None]:
    # Taxonomy headings use "math.QA (Quantum Algebra)".
    if "(" in text and text.endswith(")"):
        category_id, category_name = text.split("(", 1)
        return category_id.strip(), category_name[:-1].strip()
    return None, None


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


def validate_categories(config_categories: list[str], taxonomy_categories: list[dict[str, str | None]]) -> list[str]:
    known = {item["id"] for item in taxonomy_categories if item.get("id")}
    return sorted(category for category in config_categories if category not in known)


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
    snapshot_path = output_dir / f"{now.date().isoformat()}.json"
    state_path = output_dir / "state.json"
    taxonomy_path = output_dir / "category_taxonomy.json"

    taxonomy_categories: list[dict[str, str | None]] = []
    taxonomy_refreshed = False
    if config.refresh_taxonomy and not args.skip_taxonomy_refresh:
        taxonomy_categories = fetch_taxonomy()
        taxonomy_payload = {
            "fetched_at": now.isoformat(),
            "source_url": ARXIV_TAXONOMY_URL,
            "field_docs": TAXONOMY_FIELD_DOCS,
            "categories": taxonomy_categories,
        }
        write_json(taxonomy_path, taxonomy_payload)
        taxonomy_refreshed = True
    elif taxonomy_path.exists():
        cached_taxonomy = load_existing_snapshot(taxonomy_path) or {}
        taxonomy_categories = list(cached_taxonomy.get("categories", []))

    unknown_categories = validate_categories(config.categories, taxonomy_categories) if taxonomy_categories else []

    entries = fetch_recent_entries(config)
    existing_snapshot = load_existing_snapshot(snapshot_path) or {}
    merged_entries = merge_entries(list(existing_snapshot.get("entries", [])), entries)

    snapshot_payload = {
        "date": now.date().isoformat(),
        "fetched_at": now.isoformat(),
        "source_url": ARXIV_API_URL,
        "query": {
            "categories": config.categories,
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
        "taxonomy_path": str(taxonomy_path),
        "taxonomy_refreshed": taxonomy_refreshed,
        "category_count": len(config.categories),
        "entry_count": len(merged_entries),
        "unknown_categories": unknown_categories,
    }
    write_json(state_path, state_payload)

    print(f"Wrote snapshot: {snapshot_path}")
    print(f"Wrote state: {state_path}")
    if taxonomy_refreshed:
        print(f"Wrote taxonomy: {taxonomy_path}")
    if unknown_categories:
        print("Warning: unknown configured categories:", ", ".join(unknown_categories), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
