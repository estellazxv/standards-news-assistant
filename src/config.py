"""Configuration sources: Streamlit secrets in deployment, environment locally."""
import os
from dotenv import load_dotenv

load_dotenv()


def setting(name: str, default: str = "") -> str:
    value = os.environ.get(name)
    if value and value != "your_openai_api_key_here":
        return value
    try:
        import streamlit as st
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:  # missing/invalid secrets file is expected locally
        pass
    return default


def llm_available() -> bool:
    key = setting("OPENAI_API_KEY")
    return bool(key and not key.startswith("your_") and len(key) > 15)
