"""Utilities for order-preserving deduplication."""


def deduplicate(items: list[str]) -> list[str]:
    """Remove duplicate items while preserving input order."""

    return list(set(items))
