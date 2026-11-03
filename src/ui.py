"""Shared Streamlit interface helpers."""
import streamlit as st
from src.config import llm_available

NOTICE = """**IMPORTANT NOTICE:** This web application is developed as a proof-of-concept prototype. The information provided here is **NOT intended for actual usage** and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

**Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**

Always consult with qualified professionals for accurate and personalised advice."""


def site_intro(title: str, subtitle: str):
    st.markdown(f'<div class="eyebrow">AI CHAMPIONS BOOTCAMP · PROJECT TYPE 1</div>', unsafe_allow_html=True)
    st.title(title)
    st.caption(subtitle)


def disclaimer():
    with st.expander("⚠️ Important notice — proof-of-concept disclaimer", expanded=True):
        st.markdown(NOTICE)


def llm_status():
    if llm_available():
        st.sidebar.success("AI features ready", icon="✅")
    else:
        st.sidebar.warning("Add OPENAI_API_KEY to enable AI features", icon="🔑")


def article_card(article: dict, show_score: bool = False):
    with st.container(border=True):
        st.markdown(f"#### {article['title']}")
        st.caption(f"{article['published']} · {article['topic']} · {article['id']}")
        st.write(article["editorial_brief"][:320] + ("…" if len(article["editorial_brief"]) > 320 else ""))
        c1, c2 = st.columns([1, 1])
        with c1:
            st.link_button("Read original at ISO ↗", article["url"], use_container_width=True)
        with c2:
            if st.button("Summarise this news", key=f"sum_{article['id']}", use_container_width=True):
                st.session_state["selected_article_id"] = article["id"]
                st.switch_page("pages/02_Summarise_ISO_News.py")
        if show_score:
            st.caption(f"Retrieval relevance score: {article.get('score', 0):.2f} · not a measure of accuracy")
