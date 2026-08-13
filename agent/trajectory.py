"""Trajectory logging utilities for coding-agent runs."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class TrajectoryStep:
    """One observable step in a coding-agent trajectory."""

    iteration: int
    action: str
    target_file: str
    success: bool
    observation: str


class TrajectoryLogger:
    """Collect and persist coding-agent trajectory steps."""

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        self.steps: list[TrajectoryStep] = []

    def add_step(
        self,
        iteration: int,
        action: str,
        target_file: str,
        success: bool,
        observation: str,
    ) -> None:
        """Append one step to the trajectory."""

        self.steps.append(
            TrajectoryStep(
                iteration=iteration,
                action=action,
                target_file=target_file,
                success=success,
                observation=observation,
            )
        )

    def save(self, output_path: str | Path) -> None:
        """Write the trajectory to a JSON file."""

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "task_id": self.task_id,
            "steps": [
                asdict(step)
                for step in self.steps
            ],
        }

        path.write_text(
            json.dumps(
                payload,
                indent=2,
            ),
            encoding="utf-8",
        )
