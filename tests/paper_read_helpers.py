from __future__ import annotations

import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from mw_paper_sources import QUALITY_DIMENSIONS, quality_gate, sha256_file, write_read_context  # noqa: E402


def write_read_fixture(
    workspace: Path,
    *,
    paper_id: str,
    locator: str,
    source_fingerprint: str,
    source_format: str = "html",
    statuses: dict[str, str] | None = None,
) -> str:
    workspace.mkdir(parents=True, exist_ok=True)
    selected_statuses = statuses or {
        "text": "pass",
        "structure": "pass",
        "equations": "not_applicable",
        "figures": "not_applicable",
        "tables": "not_applicable",
    }
    dimensions = {
        name: {
            "status": selected_statuses[name],
            "score": 100 if selected_statuses[name] in {"pass", "not_applicable"} else 50,
            "metrics": {"fixture": True},
            "evidence": [f"Fixture evidence for {name}."],
        }
        for name in QUALITY_DIMENSIONS
    }
    gate, blocking = quality_gate(dimensions)
    report = {
        "parse_quality_schema": 1,
        "source": {
            "locator": locator,
            "resolved_locator": locator,
            "format": source_format,
            "fingerprint": source_fingerprint,
            "raw_artifact": f"source.{source_format}",
            "normalized_artifact": "source.md",
        },
        "dimensions": dimensions,
        "gate": gate,
        "blocking_dimensions": blocking,
        "acquisition_attempts": [{"format": source_format, "locator": locator, "result": "selected"}],
    }
    locator_value = "html#S1" if source_format == "html" else "pdf:p1"
    (workspace / f"source.{source_format}").write_bytes(
        b"<html>fixture</html>" if source_format == "html" else b"%PDF-fixture"
    )
    (workspace / "source.md").write_text(
        f"<!-- mary-normalized-source:v1 -->\n<!-- locator: {locator_value} -->\nFixture source.\n",
        encoding="utf-8",
    )
    (workspace / "parse-quality.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    context = write_read_context(workspace, paper_id, locator)
    degraded = [name for name in QUALITY_DIMENSIONS if selected_statuses[name] == "degraded"]
    claim = {"text": "Evidence-backed fixture claim.", "locators": [locator_value]}
    ledger = {
        "paper_notes_schema": 1,
        "paper_id": paper_id,
        "source": context["source"],
        "bibliography": {
            "title": "Fixture Paper",
            "authors": ["Fixture Author"],
            "year": "2026",
            "venue": "Fixture Venue",
        },
        "research": {
            "background": claim,
            "problem": claim,
            "contributions": [claim],
            "method": claim,
            "experiments": claim,
            "limitations": claim,
            "conclusions": claim,
        },
        "section_ledger": [
            {"section": "Fixture Section", "locators": [locator_value], "findings": ["Fixture finding."]}
        ],
        "parse_quality": context["parse_quality"],
        "uncertainties": [
            {
                "question": "Which details remain uncertain?",
                "why_unresolved": "The fixture preserves an explicit uncertainty contract.",
                "impact": "The uncertainty must be checked before downstream claims are trusted.",
                "locators": [locator_value],
                "quality_dimensions": degraded,
            }
        ],
    }
    notes = "<!-- mary-paper-notes:v1 -->\n```json\n" + json.dumps(ledger, ensure_ascii=False, indent=2) + "\n```\n"
    (workspace / "paper-notes.md").write_text(notes, encoding="utf-8")
    return sha256_file(workspace / "paper-notes.md")
