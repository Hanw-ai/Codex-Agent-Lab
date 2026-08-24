"""Aggregate evaluation runner for coding-agent trajectories."""

from __future__ import annotations

from pathlib import Path

from agent.evaluation import (
    evaluate_trajectory,
    summarize_evaluations,
)

TRAJECTORY_PATHS = [
    Path("outputs/task_001_trajectory.json"),
    Path("outputs/task_002_trajectory.json"),
    Path("outputs/task_003_trajectory.json"),
]
