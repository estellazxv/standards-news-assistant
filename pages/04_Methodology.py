"""Mandatory Project Type 1 technical methodology and flowcharts."""
import streamlit as st
from src.ui import site_intro

site_intro("Methodology", "Architecture, retrieval logic, LLM chains, safeguards and testing")
st.markdown("""
## Technical stack
This Python application follows the notebook pattern of separating Streamlit UI pages from reusable `src/` helper functions. It uses Streamlit for multipage navigation; OpenAI Chat Completions for prompt-controlled JSON responses; OpenAI embeddings for semantic comparisons; NumPy and scikit-learn for ranking; and a local JSON source catalogue. The app is deployed through GitHub and Streamlit Community Cloud, with credentials in deployment Secrets.

**Data flow and boundary:** ISO-hosted news articles are *not downloaded or passed to AI*. Display metadata and ISO links are kept distinct from independently authored editorial notes. Model calls receive only the user's question, independent notes, or material the user confirms is authorised for AI processing.

## Use case 1 — Search ISO News
""")
st.graphviz_chart(r"""
digraph Search {
  rankdir=TB;
  graph [bgcolor="transparent", nodesep=0.40, ranksep=0.43];
  node [shape=box, style="rounded,filled", fillcolor="#edf3fd", color="#b5caed", fontname="Arial"];
  edge [color="#4869a6"];
  A [label="Enter question / keyword"];
  B [label="Validate input length"];
  C [label="Optional LLM extracts query concepts\n(user query ONLY)"];
  D [label="Read fixed catalogue:\nmetadata + independent notes"];
  E [label="TF-IDF rank against local fields"];
  F [label="Optional embedding similarity\n(independent notes ONLY)"];
  G [label="Combine scores and apply topic filter"];
  H [label="Show results, dates and original URLs"];
  I [label="Optional LLM answer from top\nindependent notes with source IDs"];
  A -> B -> C -> E;
  D -> E;
  D -> F;
  C -> F;
  E -> G;
  F -> G;
  G -> H -> I;
}
""", use_container_width=True)
st.markdown("""
**Search pipeline details:**
1. The query is cleaned and limited to 400 characters. No blank query means browse in date order.
2. If AI is enabled, a first LLM prompt expands the **user's wording only** into 3–8 relevant concepts (e.g. "carbon" → "emissions", "GHG"). The model has no tools or access to ISO webpages.
3. A local TF-IDF search computes keyword relevance across reference metadata and editorial notes. No model receives the ISO reference titles.
4. Where enabled, embeddings compare the query with **independent editorial notes only**. The result is combined with the keyword ranking (55% semantic, 45% lexical). Failed API requests fall back to local keyword search.
5. Users see selected matching articles with dates, topic tags, and links to original ISO pages.
6. On demand, another LLM prompt answers a question from the top five original editorial notes; article IDs are checked against the retrieved items before source links are shown.

**Prompt chain:** query → LLM concept extraction → embedding-based retrieval + local TF-IDF → grounded answer generation. This implements prompt chaining and a restricted retrieval tool workflow. It is not an autonomous browsing agent.

## Use case 2 — Summarise ISO News
""")
st.graphviz_chart(r"""
digraph Summarise {
  rankdir=TB;
  graph [bgcolor="transparent", nodesep=0.40, ranksep=0.43];
  node [shape=box, style="rounded,filled", fillcolor="#edf3fd", color="#b5caed", fontname="Arial"];
  edge [color="#4869a6"];
  A [label="Select ISO News reference"];
  B [label="Display source link and\nindependent editorial brief"];
  C [label="Choose independently authored brief\nOR authorised user-provided text"];
  D [label="For user text: rights confirmation\nand sensitivity check"];
  E [label="Validate content length and format"];
  F [label="LLM summarises permitted content\nwith restrictive system instructions"];
  G [label="Parse structured JSON output"];
  H [label="Display summary, points,\nimplications and limitations"];
  I [label="Download text + verify at original ISO URL"];
  A -> B -> C -> D -> E -> F -> G -> H -> I;
}
""", use_container_width=True)
st.markdown("""
**Summary pipeline details:** The selected article determines only which reference link and **independently authored** briefing to present. Users may alternatively provide material suitable for an external AI service, with explicit confirmation of permission. After input checks, the model returns JSON containing `summary`, `key_points`, `why_it_matters`, and `limitations`. Returned arrays are bounded and strings checked before being displayed. The user can download a text summary and click through to the actual ISO news page. **The app does not claim to have processed the full original ISO article.**

## Prompt engineering approach
- **System role separation:** The model is instructed to use only permitted data, never follow instructions embedded in source material, and avoid unsupported details.
- **Prompt chaining:** Different model prompts perform specific tasks: query reformulation, retrieval and optional short-answer synthesis, and summary generation.
- **Restricted tool usage:** The `embed_texts()` wrapper is the only retrieval-related AI tool. There is no live browser tool, file-writing tool, arbitrary URL fetcher or code-execution tool available to the model.
- **JSON outputs and validation:** Required JSON schemas reduce uncontrolled formatting; returned source IDs are constrained to retrieved items.
- **Low-variation generation:** `temperature=0` promotes consistent demonstrations (not a guarantee of correctness).
- **Source separation:** Official link metadata stays outside model inputs; independently authored editorial notes can be passed for processing.

## Safeguards and limitations
| Risk | Mitigation |
|---|---|
| Copyright and unlicensed ISO content | No page scraping or model submission of ISO-hosted news content |
| Prompt injection | Untrusted inputs are delimited as data; no model tool execution; no secrets included in prompts |
| Hallucination | Retrieval-grounded prompts and explicit limitations; user can open original source |
| Excessive cost or misuse | Authentication, query length caps, maximum article count, bounded output tokens |
| API service outage | Search remains functional in keyword-only mode; summarisation reports API failure |
| Sensitive data exposure | Text permission/sensitivity confirmation, explicit no-confidential-data guidance |
| Retrieval bias | The 10-item collection is declared incomplete and fixed as of October 2026 |

A simple application password is sufficient for an assessor POC, but this does **not** substitute for enterprise identity management, per-user quotas, DLP or audited authorisation. Client-side and prompt-only protections cannot guarantee resistance to all attacks.

## Testing and evaluation
`pytest` covers catalogue validation, local retrieval, input limits, passwords and unrelated queries. Manual end-to-end testing additionally checks navigation, password gating, search terms from multiple topics, API errors, summary JSON, provenance notices, links, and mobile layout. The project includes a `TEST_PLAN.md` with examples and expected results. End-to-end LLM outputs require configured API access and should be assessed for factual support, not just fluency.

## Key scripts
| File | Role |
|---|---|
| `main.py` | Authentication, common UI, navigation |
| `pages/01_Search_ISO_News.py` | Search interface and ranked results |
| `pages/02_Summarise_ISO_News.py` | Summary interface and text export |
| `src/catalog.py` | Validates the local source catalogue |
| `src/search.py` | TF-IDF and optional semantic ranking |
| `src/llm.py` | Prompt chain, OpenAI client, structured outputs |
| `src/security.py` | Input bounds and password comparison |
| `data/iso_news_catalog.json` | Verified links and independent editorial notes |

### Source and technical references
[ISO copyright conditions](https://www.iso.org/copyright.html) · [Streamlit multipage navigation](https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation) · [OpenAI embedding API](https://developers.openai.com/api/reference/python/resources/embeddings/methods/create)
""")
