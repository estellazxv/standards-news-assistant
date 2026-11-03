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
├── main.py                    # Auth, theme, 4-page navigation
├── pages/
│   ├── 01_Search_ISO_News.py  # Search / query chain / answer generation
│   ├── 02_Summarise_ISO_News.py
│   ├── 03_About_Us.py         # Mandatory documentation
│   └── 04_Methodology.py      # Mandatory documentation + 2 flowcharts
├── src/
│   ├── catalog.py             # Validate and load data
│   ├── config.py              # Environment and Streamlit Secrets
│   ├── llm.py                 # LLM prompts, embeddings, structured outputs
│   ├── search.py              # TF-IDF + optional semantic ranker
│   ├── security.py            # Password and input checks
│   └── ui.py                  # Common UI and disclaimer
├── data/
│   └── iso_news_catalog.json  # 10 links + original editorial notes
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example   # Safe placeholders only
├── tests/                     # Automated unit tests
├── .env.example               # Safe placeholders only
├── requirements.txt
├── TEST_PLAN.md
├── SUBMISSION_TEXT.md
├── run_windows.bat
└── README.md
```

## Quick start (Windows, VS Code)

### 1. Extract and open folder

Unzip the project. In VS Code, select **File → Open Folder** and choose `standards_news_assistant`.

### 2. Create a virtual environment

Open **Terminal → New Terminal** and run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell activation is blocked, use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

Or use `.venv\Scripts\python.exe` instead of `python` in the commands that follow.

### 3. Add local settings

Copy `.env.example` to `.env` in the project root, then replace placeholders with:

```ini
OPENAI_API_KEY=your_real_openai_api_key
APP_PASSWORD=your_own_strong_password
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

**Do not** share, email, upload to LaunchPad, or commit the `.env` file. OpenAI API access requires a separate API key, a supported model and API billing. Having a ChatGPT subscription alone does not automatically provide API credentials.

### 4. Run the app

```powershell
python -m streamlit run main.py
```

Open the local URL printed by Streamlit, generally <http://localhost:8501>. Enter your app password.

`run_windows.bat` is also included for opening an already-configured environment on Windows.

### 5. Run automated tests

```powershell
python -m pip install pytest
python -m pytest -q
```

## Deploy online for bootcamp grading

You need to perform these account-authorised steps (they cannot be completed by producing Python files alone):

1. Create a **private GitHub repository** and upload the *project source files* (not `.env`, private passwords, or API keys). Confirm `.gitignore` excludes secrets. Check GitHub/Streamlit deployment permissions and agency-approved data handling.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) and choose **Create app → Deploy a public app from GitHub**. Point it at your repo and set **Main file path** to `main.py`. Community Cloud availability and private-repository access depend on your account.
3. Under **App settings → Secrets**, add:

   ```toml
   APP_PASSWORD = "replace_with_your_strong_private_password"
   OPENAI_API_KEY = "replace_with_your_openai_api_key"
   OPENAI_MODEL = "gpt-4o-mini"
   EMBEDDING_MODEL = "text-embedding-3-small"
   ```

4. Deploy, then test the external HTTPS URL in an incognito/private browser window: log in, search, summarise, browse both documentation pages and open each flowchart.
5. **Submit the live URL and the app password** in LaunchPad under your project's **Proposed Solution**. Include the title, short description, tag `agency` and team members. **Do not submit your OpenAI API key.**
6. Review the source/data classification and platform approval requirements before any external hosting; no sensitive agency data should be used for this POC.

A live URL **cannot be generated by this ZIP alone**; you must deploy it to a hosting account. You do not need to submit the source code unless requested by assessors.

## Two demonstration workflows

**Search workflow:**

```text
User question → input bounds → optional LLM query reformulation
  → local TF-IDF on news catalogue + optional embeddings on original editorial notes
  → rank articles → show source links → optional LLM answer from selected notes
```

**Summary workflow:**

```text
Select news reference → choose original editorial note / authorised text
  → confirm rights (if user-provided) → validate length → LLM JSON summary
  → render points + caveats → download text → check original ISO link
```

## Key architecture decisions

- ISO reference metadata (title/date/source URL) remains on the local search/display side. Prompts and embedding requests contain only user questions and originally authored editorial material, never original ISO article content.
- Search works without an API key, via scikit-learn TF-IDF.
- AI enhancements use `text-embedding-3-small` and `gpt-4o-mini` by default (configurable).
- Model calls are deliberately *not* agentic open-ended web crawlers. That removes the risk of an autonomous tool fetching copyrighted pages or malicious URLs.
- Authentication uses a session password and constant-time comparison, but is **POC-only**. Stronger authentication, abuse controls and monitoring would be required for wider use.
- OpenAI API processing occurs on servers controlled by the API provider; only submit material approved for that service and classification.
- The catalogue is **manually selected and static** as of **10 October 2026**. It does not imply comprehensive ISO coverage.

## Troubleshooting

| Problem | Likely fix |
|---|---|
| `App password not configured` | Add a non-placeholder `APP_PASSWORD` to `.env` or Streamlit Cloud Secrets |
| `ModuleNotFoundError` | Activate `.venv` and run `python -m pip install -r requirements.txt` |
| Search works but AI is disabled | Set a valid `OPENAI_API_KEY` in secrets |
| OpenAI error | Check account billing, model availability, credentials, network and request limits |
| Flowchart doesn't render | Install requirements including `graphviz` and restart the app |
| News link changed | Update link in `data/iso_news_catalog.json` after independent verification |
| Some results do not match | This is a 10-item POC; simplify query or disable semantic search for deterministic matching |

## Testing, submissions and licensing

`TEST_PLAN.md` includes automated and manual verification cases. `SUBMISSION_TEXT.md` provides text you can paste into LaunchPad. This student POC's code is written for this assignment. The ten news references link to ISO's own website and do not grant any rights to republish its content.
