from deduplicate import deduplicate


def test_deduplicate_preserves_order() -> None:
    assert deduplicate(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]


def test_deduplicate_removes_duplicates() -> None:
    assert deduplicate(["x", "x", "y", "y", "z"]) == ["x", "y", "z"]


def test_deduplicate_empty_input() -> None:
    assert deduplicate([]) == []
    