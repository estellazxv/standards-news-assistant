"""Mandatory Project Type 1 documentation: project scope and data provenance."""
import streamlit as st
from src.catalog import load_catalog
from src.ui import site_intro

site_intro("About Us", "Project scope, objectives, intended users, sources and functions")
st.markdown("""
## The problem
ISO publishes developments related to standards, technical work and international cooperation. Reading many individual articles is time-consuming when a user wants to understand only the subjects relevant to their work.

## Our proposed solution
**Standards News Assistant** is a password-protected Streamlit proof-of-concept focused exclusively on ISO News. It demonstrates two complementary tasks: finding relevant news using keyword or natural-language queries, and generating shorter descriptions of authorised supporting material. The original ISO article remains one click away.

## Objectives
1. Reduce time spent finding articles among a selected ISO News collection.
2. Demonstrate how an LLM can interpret a user query and provide contextual results rather than exact-word matching alone.
3. Show how AI can create useful summaries **when the text is authorised for AI processing**.
4. Preserve traceability through dates, news titles, original links and clear disclosure of information limitations.

## Intended users
Standards officers, standards-development professionals, policy researchers and anyone exploring how to track international standards developments. The current project is a prototype for assessor demonstrations, not a production information service.

## Scope and out-of-scope
**Included:** 10 selectively curated public ISO News references, a local search index, optional query expansion, semantic ranking, source-grounded answers based on independently authored editorial briefs, AI summarisation of such briefs, and user-supplied authorised text.

**Excluded:** other standards bodies, automatic live scraping, the contents of paid ISO standards, full ISO article extraction, production decision support, confidential documents and unrestricted public use.

## Data sources and provenance
- **Official ISO News webpages** provide bibliographic reference metadata such as titles, dates and source links. These are displayed for discovery and processed by local, deterministic keyword matching. The app does not send this ISO-hosted content to an LLM.
- **Original editorial briefs** in `data/iso_news_catalog.json` are independently authored, concise factual notes about the selected news events. These notes, rather than copies of ISO articles, are used for the optional AI search and summarisation demonstrations.
- **User-supplied authorised text** is processed only after a confirmation of permission and suitability for the external AI service. Text is used for the current request and is not intentionally persisted to the app's dataset.
- The catalogue is a **fixed snapshot assembled on 10 October 2026**, not a claim to index all ISO publications or provide live updates.

## Features at a glance
| Feature | Implementation | Why it is useful |
|---|---|---|
| ISO News discovery | Search, date, topic filtering, original links | Find likely relevant items quickly |
| Natural-language interpretation | LLM query expansion | Recognises concepts beyond literal terms |
| Semantic retrieval | OpenAI embeddings on independent editorial notes | Finds conceptually related news |
| Grounded questions | Short answers restricted to selected editorial notes | Rapid understanding with traceable references |
| Summary generator | Prompt-based extraction with JSON structure | Consistent key takeaways and limitations |
| Privacy and security | Password, secret management, bounded inputs | Reduces exposure in a demo environment |
| Methodology page | Two process flowcharts and implementation notes | Transparent and assessable technical design |

## Copyright, AI and responsible use
ISO states that its online materials are protected and, except for applicable ISO Open Data material, cannot be used for AI systems without appropriate permission. Accordingly, this prototype **does not scrape ISO articles or use copied ISO news text as model input**. The independent briefs are shorter editorial accounts and are not substitutes for the original articles. Obtain any necessary rights or a separately licensed dataset before developing direct full-article AI summarisation.

[ISO copyright conditions](https://www.iso.org/copyright.html) · [ISO News](https://www.iso.org/news.html)

## What would be improved beyond the POC?
With a suitable content licence and agency approval: larger news coverage, scheduled authorised content ingestion, durable vector storage, improved relevance evaluation, stronger authentication, access logging and user interviews. These are not implemented in the current prototype.
""")
st.caption(f"Current sample size: {len(load_catalog())} curated references · Prepared for AI Champions Bootcamp Project Type 1")
