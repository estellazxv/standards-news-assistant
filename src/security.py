"""Basic POC authentication and bounded input checks. Not enterprise-grade IAM."""
import hmac
import re

MAX_QUERY_LENGTH = 400
MAX_AUTHORIZED_TEXT = 14000


def validate_query(value: str) -> str:
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", value or "").strip()
    if len(value) > MAX_QUERY_LENGTH:
        raise ValueError(f"Please keep your question within {MAX_QUERY_LENGTH} characters.")
    return value


def validate_user_text(value: str) -> str:
    value = (value or "").strip()
    if len(value) > MAX_AUTHORIZED_TEXT:
        raise ValueError(f"Text is too long. Limit: {MAX_AUTHORIZED_TEXT:,} characters.")
    return value


def password_matches(provided: str, expected: str) -> bool:
    return bool(expected) and hmac.compare_digest(
        provided.encode("utf-8"), expected.encode("utf-8")
    )
