from src.catalog import load_catalog
from src.llm import answer_question, expand_query, summarise_text


def test_answer_prompt_uses_only_original_notes_and_ids(monkeypatch):
    from src import llm
    recorded = {}

    def fake_completion(system, user, max_tokens=700):
        recorded["system"] = system
        recorded["user"] = user
        return {"answer": "Based on the note, a new edition was published.",
                "supporting_ids": ["N05", "FAKE_ID"]}

    monkeypatch.setattr(llm, "_completion", fake_completion)
    article = next(x for x in load_catalog() if x["id"] == "N05")
    result = answer_question("What does this mean?", [article])
    assert "independent_editorial_note" in recorded["user"]
    assert article["url"] not in recorded["user"]
    assert article["title"] not in recorded["user"]
    assert result["supporting_ids"] == ["N05"]


def test_query_expansion_validates_output(monkeypatch):
    from src import llm
    monkeypatch.setattr(llm, "_completion", lambda *_args, **_kwargs: {
        "keywords": ["quality management", "ISO 9001", "!!!", 314, "supply chains"]})
    result = expand_query("what is new about quality?")
    assert "quality management" in result
    assert "supply chains" in result
    assert "!!!" not in result


def test_summary_returns_bounded_key_points(monkeypatch):
    from src import llm
    monkeypatch.setattr(llm, "_completion", lambda *_args, **_kwargs: {
        "summary": "Brief overview", "key_points": ["one", "two", "three", "four", "five"],
        "why_it_matters": "Potential relevance", "limitations": "This is a short note"})
    output = summarise_text("x" * 200, "Quick overview", "editorial brief")
    assert len(output["key_points"]) == 4
    assert output["limitations"] == "This is a short note"
