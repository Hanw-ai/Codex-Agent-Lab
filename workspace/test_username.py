"""Tests for username normalization."""


from username import normalize_username


def test_normalize_username_removes_whitespace() -> None:
    assert normalize_username("  Alice  ") == "alice"


def test_normalize_username_lowercases() -> None:
    assert normalize_username("BOB") == "bob"


def test_normalize_username_preserves_internal_characters() -> None:
    assert normalize_username("  User_123  ") == "user_123"
