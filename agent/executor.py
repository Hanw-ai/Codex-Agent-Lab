"""Utilities for executing commands inside a coding-agent workspace."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass
class ExecutionResult:
    """Structured result returned after executing a command."""

    command: list[str]
    return_code: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        """Return True when the command exits successfully."""
        return self.return_code == 0


class CommandExecutor:
    """Execute shell commands inside a controlled workspace."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()

        if not self.workspace.exists():
            raise FileNotFoundError(
                f"Workspace does not exist: {self.workspace}"
            )

    def run(
        self,
        command: Sequence[str],
        timeout: int = 30,
    ) -> ExecutionResult:
        """Run a command and capture its output."""

        command_list = list(command)

        try:
            completed = subprocess.run(
                command_list,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            return ExecutionResult(
                command=command_list,
                return_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )

        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(
                command=command_list,
                return_code=124,
                stdout=exc.stdout or "",
                stderr=exc.stderr or f"Command timed out after {timeout}s",
            )
