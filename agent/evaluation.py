"""Evaluation utilities for coding-agent trajectories."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TaskEvaluation:
    """Evaluation summary for one coding-agent task."""

    task_id: str
    success: bool
    iterations: int
    trajectory_length: int


@dataclass
class EvaluationSummary:
    """Aggregate evaluation metrics across multiple tasks."""

    total_tasks: int
    successful_tasks: int
    success_rate: float
    average_iterations: float
    average_trajectory_length: float


def evaluate_trajectory(path: str | Path) -> TaskEvaluation:
    """Evaluate one saved coding-agent trajectory."""

    trajectory_path = Path(path)

    data = json.loads(
        trajectory_path.read_text(encoding="utf-8")
    )

    steps = data["steps"]

    successful = bool(
        steps
        and steps[-1]["action"] == "run_tests_after_repair"
        and steps[-1]["success"] is True
    )

    iterations = max(
        (step["iteration"] for step in steps),
        default=0,
    )

    return TaskEvaluation(
        task_id=data["task_id"],
        success=successful,
        iterations=iterations,
        trajectory_length=len(steps),
    )


def summarize_evaluations(
    evaluations: list[TaskEvaluation],
) -> EvaluationSummary:
    """Aggregate evaluation metrics across coding-agent tasks."""

    if not evaluations:
        return EvaluationSummary(
            total_tasks=0,
            successful_tasks=0,
            success_rate=0.0,
            average_iterations=0.0,
            average_trajectory_length=0.0,
        )

    total_tasks = len(evaluations)

    successful_tasks = sum(
        evaluation.success
        for evaluation in evaluations
    )

    return EvaluationSummary(
        total_tasks=total_tasks,
        successful_tasks=successful_tasks,
        success_rate=successful_tasks / total_tasks,
        average_iterations=sum(
            evaluation.iterations
            for evaluation in evaluations
        ) / total_tasks,
        average_trajectory_length=sum(
            evaluation.trajectory_length
            for evaluation in evaluations
        ) / total_tasks,
    )
