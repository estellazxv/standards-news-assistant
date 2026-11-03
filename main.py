"""Single entrypoint; use `streamlit run main.py`.

Pages remain inaccessible until the password has been provided successfully.
"""
import streamlit as st
from src.config import setting
from src.security import password_matches
from src.ui import llm_status, NOTICE

st.set_page_config(page_title="Standards News Assistant", page_icon="📰", layout="wide",
                   initial_sidebar_state="expanded")
st.markdown("""
<style>
.block-container {max-width: 1150px; padding-top: 2rem; padding-bottom: 3rem}
h1 {font-weight: 800 !important; letter-spacing: -.03em}
h2, h3 {letter-spacing: -.018em}
.eyebrow {color: #1d4ed8; font-size: .72rem; font-weight: 750; letter-spacing: .11em;
          margin-bottom: .7rem}
div[data-testid="stMetric"] {border:1px solid #e0e8f7; border-radius:12px;
    background: white; padding: 1rem}
div[data-testid="stContainer"] {border-radius:12px}
</style>
""", unsafe_allow_html=True)

expected_password = setting("APP_PASSWORD")
if not expected_password or expected_password == "replace_with_a_strong_password":
    st.error(
        "App password not configured. Add APP_PASSWORD to your .env or Streamlit Secrets.")
    st.info("See README.md for secure setup. Never hardcode or commit credentials.")
    st.stop()
if not st.session_state.get("authenticated", False):
    st.title("📰 Standards News Assistant")
    st.markdown("### Private proof-of-concept")
    st.info("Enter the demo password provided by the project team.")
    with st.expander("Important notice: prototype only"):
        st.markdown(NOTICE)
    with st.form("login_form"):
        password = st.text_input("Application password", type="password")
        login = st.form_submit_button("Access application", type="primary")
    if login:
        if password_matches(password, expected_password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

with st.sidebar:
    st.markdown("## 📰 Standards News")
    st.caption("ISO news discovery · curated proof-of-concept")
    llm_status()
    if st.button("Sign out", use_container_width=True):
        st.session_state.clear()
        st.rerun()

navigation = st.navigation({
    "APPLICATION": [
        st.Page("pages/01_Search_ISO_News.py",
                title="Search ISO News", icon="🔎", default=True),
        st.Page("pages/02_Summarise_ISO_News.py",
                title="Summarise ISO News", icon="📝"),
    ],
    "PROJECT DOCUMENTATION": [
        st.Page("pages/03_About_Us.py", title="About Us", icon="ℹ️"),
        st.Page("pages/04_Methodology.py", title="Methodology", icon="🧭"),
    ],
})
navigation.run()
