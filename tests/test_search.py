from src.catalog import load_catalog
from src.search import rank_articles, lexical_scores

ARTICLES = load_catalog()


def test_empty_query_browses_newest_first():
    results = rank_articles("", ARTICLES)
    assert len(results) == len(ARTICLES)
    assert results[0]["id"] == "N01"


def test_quality_management_finds_iso9001():
    ids = [x["id"] for x in rank_articles("ISO 9001 quality management", ARTICLES)]
    assert ids and ids[0] == "N05"


def test_digital_credentials_finds_digital_identity():
    ids = [x["id"] for x in rank_articles("mobile driving licence digital identity", ARTICLES)]
    assert ids and ids[0] == "N07"


def test_unrelated_query_does_not_generate_invented_results():
    assert rank_articles("quasar platypus nebula", ARTICLES) == []


def test_lexical_scores_match_catalogue_length():
    assert len(lexical_scores("resilience", ARTICLES)) == len(ARTICLES)


def test_semantic_falls_back_if_embedding_fails(monkeypatch):
    def fail(_):
        raise RuntimeError("down")
    monkeypatch.setattr("src.search.embed_texts", fail)
    ranked = rank_articles("ISO 9001", ARTICLES, semantic=True)
    assert ranked and ranked[0]["id"] == "N05"
