# LaunchPad proposed solution — ready to adapt

**Project title:** Standards News Assistant

**Project type (Submission Tag):** agency

**Project description:**

The Standards News Assistant is a proof-of-concept Streamlit web application that helps users find and understand developments related to ISO standards. It has two primary use cases. In *Search ISO News*, users search a curated catalogue of ISO News references using keywords or natural-language questions. Search results include publication dates, subject categories and links to the original articles. With an API key, the application demonstrates query expansion, semantic ranking over independently prepared editorial notes, and a short source-grounded answer. In *Summarise ISO News*, users select a referenced article and obtain an AI summary of a separately authored editorial briefing; they may also supply text they are authorised to use with AI. Summaries include key points, potential relevance and limitations, together with a link to the original source.

The prototype is restricted to a fixed sample of 10 ISO News references and does not scrape or send copyrighted ISO webpage text to an AI model. It includes password protection, source attribution, prompt-injection safeguards, and mandatory *About Us* and *Methodology* pages. The methodology page contains separate flowcharts for the search and summarisation use cases. The application is solely for demonstration and evaluation and must not be relied upon for operational decisions.

**Streamlit URL:** [PASTE YOUR DEPLOYED HTTPS URL HERE]

**App password for assessors:** [PASTE YOUR DEMO PASSWORD HERE - NOT YOUR OPENAI API KEY]

**Team members:** [ADD NAME(S)]

**Project repository / code:** [OPTIONAL - ADD PRIVATE SOURCE REPOSITORY ONLY IF REQUESTED]

**Note for presentation:** The original proposed solution envisaged automatic full-article summarisation. ISO's current website terms restrict AI use of its published material without permission. This POC instead demonstrates AI summarisation on independently written editorial briefs and separately authorised text while leaving original article access on ISO's website. The distinction is deliberately explained to assessors in the app.
