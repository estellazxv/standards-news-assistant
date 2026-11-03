"""Validated curated collection; does not scrape or cache ISO webpages."""
import json
from pathlib import Path
from datetime import date
from urllib.parse import urlparse

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "iso_news_catalog.json"


def load_catalog(path: Path = DATA_FILE) -> list[dict]:
    records = json.loads(path.read_text(encoding="utf-8"))
    ids = set()
    for item in records:
        expected = ("id", "title", "published", "url", "topic", "tags", "editorial_brief")
        if not all(item.get(field) for field in expected):
            raise ValueError(f"Incomplete record: {item.get('id', 'unknown')}")
        if item["id"] in ids:
            raise ValueError("Duplicate article ID")
        ids.add(item["id"])
        date.fromisoformat(item["published"])
        if urlparse(item["url"]).hostname not in ("www.iso.org", "committee.iso.org"):
            raise ValueError("Catalogue links must lead to the official ISO websites")
        if len(item["editorial_brief"]) > 3500:
            raise ValueError("Editorial brief exceeds expected length")
    return sorted(records, key=lambda a: a["published"], reverse=True)


def get_article(article_id: str, articles: list[dict]) -> dict | None:
    return next((a for a in articles if a["id"] == article_id), None)
