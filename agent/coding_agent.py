"""Minimal executable coding agent for deterministic repair tasks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.executor import CommandExecutor
from agent.workspace import WorkspaceManager


@dataclass
class AgentResult:
    """Result produced by a coding-agent run."""

    success: bool
    iterations: int
    message: str


class CodingAgent:
    """A minimal coding agent that can inspect, edit, and test code."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = WorkspaceManager(workspace)
        self.executor = CommandExecutor(workspace)

    def inspect_file(self, relative_path: str) -> str:
        """Read a file from the workspace."""

        return self.workspace.read_file(relative_path)

    def repair_subtract_bug(self, relative_path: str) -> None:
        """Repair the known subtraction bug in the calculator task."""

        content = self.workspace.read_file(relative_path)

        old = """def subtract(a: float, b: float) -> float:
    \"\"\"Return the difference between two numbers.\"\"\"
    return a + b
"""

        new = """def subtract(a: float, b: float) -> float:
    \"\"\"Return the difference between two numbers.\"\"\"
    return a - b
"""

        if old not in content:
            raise ValueError(
                "Expected buggy subtract implementation was not found."
            )

        updated = content.replace(old, new)

        self.workspace.write_file(
            relative_path,
            updated,
        )

    def run_tests(self) -> bool:
        """Run pytest inside the workspace."""

        result = self.executor.run(
            ["python", "-m", "pytest", "-q"]
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result.success

    def solve(
        self,
        target_file: str,
        max_iterations: int = 3,
    ) -> AgentResult:
        """Attempt to repair the task until tests pass."""

        for iteration in range(1, max_iterations + 1):

            if self.run_tests():
                return AgentResult(
                    success=True,
                    iterations=iteration - 1,
                    message="Tests already pass.",
                )

            self.repair_subtract_bug(target_file)

            if self.run_tests():
                return AgentResult(
                    success=True,
                    iterations=iteration,
                    message="Repair succeeded.",
                )

        return AgentResult(
            success=False,
            iterations=max_iterations,
            message="Repair budget exhausted.",
        )
