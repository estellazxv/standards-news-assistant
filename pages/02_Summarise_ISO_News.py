"""Use case 2: source-aware summarisation without processing copyrighted ISO text."""
import streamlit as st
from src.catalog import load_catalog, get_article
from src.config import llm_available
from src.llm import summarise_text
from src.security import validate_user_text
from src.ui import site_intro

articles = load_catalog()
site_intro("Get to the key points, faster.",
           "Summarise independent editorial briefs, or provide text you are authorised to process with AI.")
st.warning("**Copyright safeguard:** This app does not retrieve, store or send ISO's online article text "
           "to an LLM. ISO's current terms restrict the use of its content for AI. "
           "Read the original article at ISO; only upload other text if you have explicit permission for AI use.")

index = {a["id"]: i for i, a in enumerate(articles)}
initial_id = st.session_state.get("selected_article_id", articles[0]["id"])
selected_index = index.get(initial_id, 0)
selected = st.selectbox("Choose a news article", options=articles, index=selected_index,
                        format_func=lambda a: f"{a['published']} · {a['title']}")
st.session_state["selected_article_id"] = selected["id"]
st.markdown(f"### {selected['title']}")
st.caption(f"Published {selected['published']} · {selected['topic']} · Reference {selected['id']}")
st.link_button("Read the complete original at ISO ↗", selected["url"])

with st.expander("View the independent editorial brief used by this demonstration", expanded=True):
    st.write(selected["editorial_brief"])
    st.caption("This is an independently authored short factual briefing, not the ISO article itself.")

st.markdown("### Prepare an AI summary")
source_choice = st.radio("Material to summarise", [
    "Independent editorial brief (default demo)",
    "Text I am authorised to use with AI",
], index=0)

content = selected["editorial_brief"]
provenance = "independently written editorial brief"
confirm_rights = True
if source_choice.startswith("Text I am"):
    content = st.text_area("Paste authorised text (maximum 14,000 characters)",
                           height=210, placeholder="Paste text that you have the right to use with an AI service...")
    confirm_rights = st.checkbox(
        "I confirm that I have permission to submit this text to an external AI service, "
        "and that its sensitivity is suitable for that service.")
    provenance = "user-provided authorised text"

detail = st.segmented_control("Summary format", ["Quick overview", "Detailed overview", "For standards professionals"],
                              default="Quick overview")
if st.button("Generate AI summary", type="primary", use_container_width=True,
             disabled=not llm_available()):
    try:
        safe_text = validate_user_text(content)
        if len(safe_text) < 60:
            st.error("Provide at least 60 characters of informative material for a meaningful summary.")
        elif not confirm_rights:
            st.error("Please confirm you are authorised to use this material with AI.")
        else:
            with st.spinner("Summarising the permitted text…"):
                result = summarise_text(safe_text, detail or "Quick overview", provenance)
            st.session_state["last_summary"] = {
                "article_id": selected["id"], "format": detail, "source_choice": source_choice,
                "result": result, "source_url": selected["url"],
            }
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error("The AI request failed. Check the API key, model access and network connection.")

if not llm_available():
    st.info("AI summarisation requires OPENAI_API_KEY, configured in .env locally or Streamlit Cloud Secrets.")

saved = st.session_state.get("last_summary")
if saved and saved["article_id"] == selected["id"] and saved["source_choice"] == source_choice:
    r = saved["result"]
    st.markdown("### Generated summary")
    st.info("AI-generated from " + ("independently written editorial notes." if source_choice.startswith("Independent") else "user-authorised text."))
    st.write(r["summary"])
    st.markdown("#### Key points")
    for point in r["key_points"]:
        st.markdown("- " + point)
    st.markdown("#### Why this may matter")
    st.write(r["why_it_matters"])
    st.markdown("#### Limitations")
    st.write(r["limitations"])
    st.link_button("Check the original ISO news article ↗", selected["url"])
    export_text = "\n".join([
        "Standards News Assistant - Demonstration Summary", selected["title"],
        "Source: " + selected["url"], "Material: " + saved["source_choice"], "",
        "SUMMARY", r["summary"], "", "KEY POINTS",
        *["- " + x for x in r["key_points"]], "", "WHY IT MATTERS",
        r["why_it_matters"], "", "LIMITATIONS", r["limitations"],
        "", "POC only; do not use for actual decisions.",
    ])
    st.download_button("Download summary (.txt)", data=export_text,
                       file_name=f"standards_summary_{selected['id']}.txt", mime="text/plain")
