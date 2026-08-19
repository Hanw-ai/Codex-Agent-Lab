"""Minimal executable coding agent for deterministic repair tasks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.executor import CommandExecutor
from agent.trajectory import TrajectoryLogger
from agent.workspace import WorkspaceManager


@dataclass
class AgentResult:
    """Result produced by a coding-agent run."""

    success: bool
    iterations: int
    message: str


class CodingAgent:
    """A minimal coding agent that can inspect, edit, and test code."""

    def __init__(
        self,
        workspace: str | Path,
        task_id: str = "unknown_task",
        test_command: list[str] | None = None,
    ) -> None:
        self.workspace = WorkspaceManager(workspace)
        self.executor = CommandExecutor(workspace)
        self.trajectory = TrajectoryLogger(task_id)
        self.test_command = test_command or [
            "python",
            "-m",
            "pytest",
            "-q",
        ]

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

    def repair_username_normalization(
        self,
        relative_path: str,
    ) -> None:
        """Repair username normalization logic."""

        content = self.workspace.read_file(relative_path)

        old = """def normalize_username(username: str) -> str:
    \"\"\"Normalize a username for consistent storage.\"\"\"

    return username
"""

        new = """def normalize_username(username: str) -> str:
    \"\"\"Normalize a username for consistent storage.\"\"\"

    return username.strip().lower()
"""

        if old not in content:
            raise ValueError(
                "Expected buggy username implementation was not found."
            )

        updated = content.replace(old, new)

        self.workspace.write_file(
            relative_path,
            updated,
        )

    def repair_file(self, relative_path: str) -> None:
        """Select a repair strategy for the target file."""

        if relative_path == "calculator.py":
            self.repair_subtract_bug(relative_path)
            return

        if relative_path == "username.py":
            self.repair_username_normalization(relative_path)
            return

        raise ValueError(
            f"No repair strategy available for: {relative_path}"
        )

    def run_tests(self) -> bool:
        """Run pytest inside the workspace."""

        result = self.executor.run(
            self.test_command
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
    
            tests_passed = self.run_tests()
    
            self.trajectory.add_step(
                iteration=iteration,
                action="run_tests_before_repair",
                target_file=target_file,
                success=tests_passed,
                observation=(
                    "Tests passed before repair."
                    if tests_passed
                    else "Tests failed before repair."
                ),
            )
    
            if tests_passed:
                return AgentResult(
                    success=True,
                    iterations=iteration - 1,
                    message="Tests already pass.",
                )
    
            self.repair_file(target_file)
    
            self.trajectory.add_step(
                iteration=iteration,
                action="repair_file",
                target_file=target_file,
                success=True,
                observation=f"Applied repair to {target_file}.",
            )
    
            tests_passed = self.run_tests()
    
            self.trajectory.add_step(
                iteration=iteration,
                action="run_tests_after_repair",
                target_file=target_file,
                success=tests_passed,
                observation=(
                    "Tests passed after repair."
                    if tests_passed
                    else "Tests still failed after repair."
                ),
            )
    
            if tests_passed:
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
