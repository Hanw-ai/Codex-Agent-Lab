"""Planning abstractions for coding-agent repairs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class RepairContext:
    """Observable state available to the repair planner."""

    task_id: str
    description: str
    target_file: str
    source_code: str
    test_output: str


@dataclass
class RepairPlan:
    """A concrete source-code repair proposed by a planner."""

    explanation: str
    old_text: str
    new_text: str


class RepairPlanner(Protocol):
    """Interface for coding-agent repair planners."""

    def plan(self, context: RepairContext) -> RepairPlan:
        """Produce a repair plan from the current observation."""
        ...


class RuleBasedPlanner:
    """Deterministic baseline planner for reproducible agent evaluation."""

    def plan(self, context: RepairContext) -> RepairPlan:
        """Generate a repair plan from source code and test evidence."""

        source = context.source_code

        buggy_subtract = """def subtract(a: float, b: float) -> float:
    \"\"\"Return the difference between two numbers.\"\"\"
    return a + b
"""

        fixed_subtract = """def subtract(a: float, b: float) -> float:
    \"\"\"Return the difference between two numbers.\"\"\"
    return a - b
"""

        if buggy_subtract in source:
            return RepairPlan(
                explanation=(
                    "The subtract function incorrectly performs addition; "
                    "replace its implementation with subtraction."
                ),
                old_text=buggy_subtract,
                new_text=fixed_subtract,
            )

        if (
            "def normalize_username" in source
            and "return username" in source
        ):
            return RepairPlan(
                explanation=(
                    "Username normalization must trim surrounding whitespace "
                    "and convert text to lowercase."
                ),
                old_text="return username",
                new_text="return username.strip().lower()",
            )

        if "return list(set(items))" in source:
            return RepairPlan(
                explanation=(
                    "Using set removes duplicates but does not preserve "
                    "the required input order."
                ),
                old_text="return list(set(items))",
                new_text="return list(dict.fromkeys(items))",
            )

        raise ValueError(
            "Planner could not determine a repair from the observed state."
        )