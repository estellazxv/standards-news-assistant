"""Use case 1: search curated ISO News references with optional LLM assistance."""
import streamlit as st
from src.catalog import load_catalog
from src.config import llm_available
from src.llm import expand_query, answer_question, embed_texts
from src.search import rank_articles
from src.security import validate_query
from src.ui import site_intro, disclaimer, article_card


@st.cache_data(ttl=86400, show_spinner=False)
def cached_editorial_embeddings(editorial_notes: tuple[str, ...], model: str) -> list[list[float]]:
    # Model is part of the cache key. No ISO title, URL or article body is embedded.
    return embed_texts(list(editorial_notes))


articles = load_catalog()
site_intro("Find the standards news that matters.",
           "Search a fixed, curated directory of public ISO News links. AI works only on independent editorial notes.")
disclaimer()

st.info("**Data scope:** 10 selected news links, dated September 2025–October 2026. "
        "Not a live ISO feed. Original ISO articles are accessed on ISO's own website. "
        "Search answers are based on independently authored editorial notes, not full ISO articles.")

m1, m2, m3 = st.columns(3)
m1.metric("Curated articles", len(articles))
m2.metric("Topics covered", len(set(a["topic"] for a in articles)))
m3.metric("Latest entry", articles[0]["published"])
st.markdown("### Search the collection")

suggested = ["ISO 9001 quality management", "climate and sustainability", "digital identity standards"]
s_cols = st.columns(3)
for col, q in zip(s_cols, suggested):
    with col:
        if st.button(q, key="suggest_" + q, use_container_width=True):
            st.session_state["search_query"] = q
            st.session_state["query_input"] = q
            st.session_state.pop("expanded_query", None)
            st.rerun()

if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""
with st.form("news_search_form"):
    st.text_input("Enter a keyword or a question", key="query_input",
                  placeholder="e.g. What recent updates relate to sustainability?")
    options = ["All topics"] + sorted({x["topic"] for x in articles})
    chosen_topic = st.selectbox("Topic filter", options)
    advanced = st.checkbox("Use AI-assisted semantic search (requires API key)",
                           value=llm_available(), disabled=not llm_available())
    submitted = st.form_submit_button("Search news", type="primary", use_container_width=True)

if submitted:
    try:
        st.session_state["search_query"] = validate_query(st.session_state["query_input"])
        st.session_state["expanded_query"] = ""
        if advanced and st.session_state["search_query"]:
            try:
                with st.spinner("Understanding your search intent…"):
                    st.session_state["expanded_query"] = expand_query(st.session_state["search_query"])
            except Exception:
                st.warning("Query expansion is unavailable; continuing with the original keywords.")
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

query = st.session_state.get("search_query", "")
filtered = [x for x in articles if chosen_topic == "All topics" or x["topic"] == chosen_topic]
semantic_on = bool(query and advanced and llm_available())
embeddings = None
if semantic_on and filtered:
    try:
        with st.spinner("Comparing query with curated editorial notes…"):
            from src.config import setting
            embeddings = cached_editorial_embeddings(tuple(a["editorial_brief"] for a in filtered),
                                                     setting("EMBEDDING_MODEL", "text-embedding-3-small"))
    except Exception:
        st.warning("Semantic search could not be completed; using local keyword search instead.")
        semantic_on = False
results = rank_articles(query, filtered, st.session_state.get("expanded_query", ""),
                        semantic=semantic_on, precomputed=embeddings)
st.markdown(f"### {'Browse recent news' if not query else 'Search results'}")
st.caption(f"Showing {len(results)} of {len(filtered)} available in the selected topic.")
if not results:
    st.info("No matches in this small collection. Try simpler keywords or browse all topics.")
else:
    for record in results:
        article_card(record, show_score=bool(query))

if query and results:
    st.markdown("### Ask a question about these results")
    st.caption("A second LLM step can synthesise only the independent notes for the top matching articles.")
    if not llm_available():
        st.info("Set OPENAI_API_KEY in Streamlit Secrets to activate grounded AI answers.")
    elif st.button("Generate grounded answer", type="secondary"):
        try:
            with st.spinner("Preparing a source-grounded answer…"):
                response = answer_question(query, results[:5])
            st.markdown("#### AI answer")
            st.write(response["answer"])
            references = set(response.get("supporting_ids", []))
            if references:
                st.markdown("**Editorial-note sources:**")
                for item in results[:5]:
                    if item["id"] in references:
                        st.markdown(f"- {item['id']} · [{item['title']}]({item['url']})")
            st.caption("Check the original links. The AI does not read the original ISO pages.")
        except Exception:
            st.error("AI answer could not be generated. Check API settings, network connectivity and model access.")
