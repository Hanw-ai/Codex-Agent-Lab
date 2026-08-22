"""Minimal executable coding agent for deterministic repair tasks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.executor import CommandExecutor
from agent.planner import RepairContext, RepairPlan, RepairPlanner, RuleBasedPlanner
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
        planner: RepairPlanner | None = None,
    ) -> None:
        self.workspace = WorkspaceManager(workspace)
        self.executor = CommandExecutor(workspace)
        self.task_id = task_id
        self.trajectory = TrajectoryLogger(task_id)
        self.planner = planner or RuleBasedPlanner()
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

    def apply_plan(
        self,
        relative_path: str,
        plan: RepairPlan,
    ) -> None:
        """Apply a planner-generated source-code repair."""

        content = self.workspace.read_file(relative_path)

        if plan.old_text not in content:
            raise ValueError(
                f"Planner patch target was not found in {relative_path}."
            )

        updated = content.replace(
            plan.old_text,
            plan.new_text,
            1,
        )

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

    def execute_tests(self):
        """Run the task-specific test command and return the full result."""

        result = self.executor.run(
            self.test_command
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result

    def run_tests(self) -> bool:
        """Run the task-specific tests and return whether they pass."""

        return self.execute_tests().success

    def solve(
        self,
        target_file: str,
        description: str = "",
        max_iterations: int = 3,
    ) -> AgentResult:
        """Inspect, plan, repair, and verify a coding task."""

        for iteration in range(1, max_iterations + 1):
            source_code = self.inspect_file(target_file)

            self.trajectory.add_step(
                iteration=iteration,
                action="inspect_source",
                target_file=target_file,
                success=True,
                observation=f"Inspected source file: {target_file}.",
            )

            test_result = self.execute_tests()
            tests_passed = test_result.success

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

            test_output = "\n".join(
                part
                for part in (
                    test_result.stdout,
                    test_result.stderr,
                )
                if part
            )

            context = RepairContext(
                task_id=self.task_id,
                description=description,
                target_file=target_file,
                source_code=source_code,
                test_output=test_output,
            )

            plan = self.planner.plan(context)

            self.trajectory.add_step(
                iteration=iteration,
                action="generate_repair_plan",
                target_file=target_file,
                success=True,
                observation=plan.explanation,
            )

            self.apply_plan(
                target_file,
                plan,
            )

            self.trajectory.add_step(
                iteration=iteration,
                action="apply_patch",
                target_file=target_file,
                success=True,
                observation=f"Applied planner patch to {target_file}.",
            )

            verification_result = self.execute_tests()
            tests_passed = verification_result.success

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
                    message="Planner-driven repair succeeded.",
                )

        return AgentResult(
            success=False,
            iterations=max_iterations,
            message="Repair budget exhausted.",
        )
