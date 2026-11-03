from datetime import date
from pathlib import Path
import json
import pytest
from src.catalog import load_catalog, get_article


def test_sample_dataset_has_valid_unique_official_urls():
    records = load_catalog()
    assert len(records) == 10
    assert records[0]["published"] == "2026-10-01"
    assert len({r["id"] for r in records}) == 10
    assert all(r["url"].startswith("https://") for r in records)
    assert all(date.fromisoformat(r["published"]) <= date(2026, 10, 10) for r in records)


def test_lookup():
    articles = load_catalog()
    assert get_article("N05", articles)["topic"] == "Quality Management"
    assert get_article("DOES_NOT_EXIST", articles) is None


def test_reject_duplicate_ids(tmp_path):
    records = load_catalog()
    records[1]["id"] = records[0]["id"]
    f = tmp_path / "duplicate.json"
    f.write_text(json.dumps(records), encoding="utf-8")
    with pytest.raises(ValueError, match="Duplicate"):
        load_catalog(f)


def test_reject_external_host(tmp_path):
    records = load_catalog()
    records[0]["url"] = "https://evil.example/phish"
    f = tmp_path / "bad.json"
    f.write_text(json.dumps(records), encoding="utf-8")
    with pytest.raises(ValueError, match="official ISO"):
        load_catalog(f)
