import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "build_arxiv_review.py"


def make_entry(
    arxiv_id: str,
    versioned_id: str,
    title: str,
    *,
    categories: list[str] | None = None,
    updated: str = "2026-01-02T00:00:00Z",
) -> dict[str, object]:
    return {
        "arxiv_id": arxiv_id,
        "versioned_id": versioned_id,
        "title": title,
        "authors": ["Test Author"],
        "categories": categories or ["math.QA"],
        "abs_url": f"http://arxiv.org/abs/{versioned_id}",
        "summary": "Test abstract.",
        "updated": updated,
    }


class BuildArxivReviewTests(unittest.TestCase):
    maxDiff = None

    def run_builder(
        self,
        current_date: str,
        current_entries: list[dict[str, object]],
        *,
        history_snapshots: dict[str, list[dict[str, object]]] | None = None,
        review_top_n: int = 20,
    ) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            snapshots_dir = root / "snapshots"
            output_dir = root / "output"
            config_path = root / "config.json"
            profile_path = root / "profile.json"
            current_snapshot_path = snapshots_dir / f"{current_date}.json"

            snapshots_dir.mkdir(parents=True, exist_ok=True)
            output_dir.mkdir(parents=True, exist_ok=True)

            config_path.write_text(
                json.dumps(
                    {
                        "include_review_summary": True,
                        "review_top_n": review_top_n,
                        "review_high_score": 10.0,
                        "review_mid_score": 4.0,
                        "category_weights": {"math.QA": 5.0},
                        "keyword_weights": {},
                    }
                ),
                encoding="utf-8",
            )
            profile_path.write_text(
                json.dumps(
                    {
                        "category_weights": {"math.QA": 5.0},
                        "keyword_weights": {},
                        "history": {
                            "positive_count": 0,
                            "negative_count": 0,
                            "last_review_path": None,
                        },
                        "processed_review_files": [],
                        "updated_at": "2026-01-01T00:00:00+00:00",
                    }
                ),
                encoding="utf-8",
            )

            for snapshot_date, entries in (history_snapshots or {}).items():
                (snapshots_dir / f"{snapshot_date}.json").write_text(
                    json.dumps({"date": snapshot_date, "entries": entries}),
                    encoding="utf-8",
                )

            current_snapshot_path.write_text(
                json.dumps({"date": current_date, "entries": current_entries}),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--config",
                    str(config_path),
                    "--snapshot",
                    str(current_snapshot_path),
                    "--profile",
                    str(profile_path),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=str(REPO_ROOT),
                check=True,
                capture_output=True,
                text=True,
            )

            return (output_dir / f"{current_date}.md").read_text(encoding="utf-8")

    def test_exact_duplicate_version_is_suppressed(self) -> None:
        markdown = self.run_builder(
            "2026-01-02",
            [
                make_entry("1234.5678", "1234.5678v1", "Repeated Paper"),
                make_entry("9999.0001", "9999.0001v1", "Fresh Paper"),
            ],
            history_snapshots={
                "2026-01-01": [make_entry("1234.5678", "1234.5678v1", "Repeated Paper")]
            },
        )

        self.assertNotIn("Repeated Paper", markdown)
        self.assertIn("Fresh Paper", markdown)

    def test_newer_version_of_seen_arxiv_id_is_kept_as_update(self) -> None:
        markdown = self.run_builder(
            "2026-01-02",
            [make_entry("1234.5678", "1234.5678v2", "Revised Paper")],
            history_snapshots={
                "2026-01-01": [make_entry("1234.5678", "1234.5678v1", "Revised Paper")]
            },
        )

        self.assertIn("Revised Paper [Update]", markdown)
        self.assertIn('"is_update": true', markdown)
        self.assertIn('"previous_versioned_ids": ["1234.5678v1"]', markdown)

    def test_fresh_paper_without_history_appears_without_update_label(self) -> None:
        markdown = self.run_builder(
            "2026-01-02",
            [make_entry("7777.0001", "7777.0001v1", "Brand New Paper")],
        )

        self.assertIn("Brand New Paper", markdown)
        self.assertNotIn("Brand New Paper [Update]", markdown)
        self.assertIn('"is_update": false', markdown)

    def test_duplicate_suppression_happens_before_top_n_trimming(self) -> None:
        markdown = self.run_builder(
            "2026-01-02",
            [
                make_entry("1111.0001", "1111.0001v1", "Duplicate Candidate", updated="2026-01-02T03:00:00Z"),
                make_entry("2222.0001", "2222.0001v1", "Fresh Candidate One", updated="2026-01-02T02:00:00Z"),
                make_entry("3333.0001", "3333.0001v1", "Fresh Candidate Two", updated="2026-01-02T01:00:00Z"),
            ],
            history_snapshots={
                "2026-01-01": [make_entry("1111.0001", "1111.0001v1", "Duplicate Candidate")]
            },
            review_top_n=2,
        )

        self.assertNotIn("Duplicate Candidate", markdown)
        self.assertIn("Fresh Candidate One", markdown)
        self.assertIn("Fresh Candidate Two", markdown)

    def test_current_snapshot_is_not_treated_as_history(self) -> None:
        markdown = self.run_builder(
            "2026-01-02",
            [make_entry("5555.0001", "5555.0001v1", "Current Day Paper")],
            history_snapshots={
                "2026-01-03": [make_entry("5555.0001", "5555.0001v1", "Future Snapshot Paper")]
            },
        )

        self.assertIn("Current Day Paper", markdown)
        self.assertNotIn("Current Day Paper [Update]", markdown)


if __name__ == "__main__":
    unittest.main()
