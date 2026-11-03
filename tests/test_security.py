import pytest
from src.security import validate_query, validate_user_text, password_matches


def test_clean_query_control_characters():
    assert validate_query("  what is\x00 ISO 9001  ") == "what is ISO 9001"


def test_query_input_limit():
    with pytest.raises(ValueError, match="400"):
        validate_query("A" * 401)


def test_user_text_max_length():
    with pytest.raises(ValueError, match="14,000"):
        validate_user_text("X" * 14001)


def test_password_comparison():
    assert password_matches("correct", "correct")
    assert not password_matches("wrong", "correct")
    assert not password_matches("", "")
