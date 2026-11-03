"""Reproducible hybrid ranking: metadata TF-IDF + editorial-brief embeddings."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.llm import embed_texts


def _lexical_text(article: dict) -> str:
    # ISO title is used only in local deterministic keyword matching.
    return " ".join([article["title"], article["topic"],
                     " ".join(article["tags"]), article["editorial_brief"]])


def lexical_scores(query: str, articles: list[dict]) -> np.ndarray:
    if not query.strip() or not articles:
        return np.zeros(len(articles))
    docs = [_lexical_text(x) for x in articles] + [query]
    try:
        matrix = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True).fit_transform(docs)
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    except ValueError:
        scores = np.zeros(len(articles))
    return np.asarray(scores)


def rank_articles(query: str, articles: list[dict], enriched_query: str = "",
                  semantic: bool = False, precomputed: list[list[float]] | None = None,
                  limit: int = 10) -> list[dict]:
    """Returns copies enriched with score. Falls back to local search on API failures."""
    if not articles:
        return []
    if not query.strip():
        return [dict(item, score=1.0) for item in articles[:limit]]
    lexical = lexical_scores(query + " " + enriched_query, articles)
    score = lexical.copy()
    if semantic:
        try:
            docs = precomputed if precomputed is not None else embed_texts([x["editorial_brief"] for x in articles])
            query_emb = embed_texts([query])[0]
            sem = cosine_similarity([query_emb], docs).ravel()
            sem = np.clip((sem - 0.12) / 0.88, 0.0, 1.0)
            score = 0.55 * sem + 0.45 * lexical
        except Exception:
            score = lexical
    ranked = [dict(article, score=float(score[i])) for i, article in enumerate(articles)]
    ranked.sort(key=lambda x: (x["score"], x["published"]), reverse=True)
    # Threshold prevents unrelated answers when keyword-only matching fails.
    return [a for a in ranked if a["score"] > 0.025][:limit]
