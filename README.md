# Standards News Assistant 📰

**AI Champions Bootcamp 2026 · Project Type 1 · Agency-level proof-of-concept**

A deployable, password-protected, multi-page Streamlit app demonstrating:

1. **Search ISO News:** Browse 10 verified ISO News references using local keyword search; optionally use an LLM to expand natural-language queries and embeddings to rank independently authored editorials. Generate short grounded answers from these editorials.
2. **Summarise ISO News:** Select a news reference, read an independently authored editorial brief, and generate an AI summary with key points, relevance and limitations; or submit text you are explicitly authorised to use with AI.
3. **About Us:** Project scope, objectives, users, source data and functionality.
4. **Methodology:** Two separate process flowcharts, LLM chain, technical architecture, safeguards and tests.

## IMPORTANT: Legal and source-data boundary

ISO's online copyright conditions (verified 10 October 2026) state that, except for applicable ISO Open Data material, ISO content must not be used to prompt or otherwise enable AI without appropriate permission. See <https://www.iso.org/copyright.html>. **This application does not automatically scrape, store, republish, embed or summarise original ISO webpages.** It uses official links/titles/dates for local discovery and separately authored editorial fact briefs for the AI demo. An AI summary of the editorial brief is **not** a summary made from the full original article. To expand the project to article-level AI summarisation, obtain relevant permissions or find a suitable licensed source.

This approach preserves a functional AI POC while respecting the declared source restrictions. The app is NOT a production information service, is NOT a complete or live ISO news feed, and MUST NOT be relied upon for decisions.

## Project files

```text
standards_news_assistant/
├── main.py
├── pages/
│   ├── 01_Search_ISO_News.py
│   ├── 02_Summarise_ISO_News.py
│   ├── 03_About_Us.py
│   └── 04_Methodology.py
├── src/
│   ├── catalog.py
│   ├── config.py
│   ├── llm.py
│   ├── search.py
│   ├── security.py
│   └── ui.py
├── data/
│   └── iso_news_catalog.json
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── tests/
├── .env.example
├── requirements.txt
├── TEST_PLAN.md
├── SUBMISSION_TEXT.md
├── run_windows.bat
└── README.md
```
