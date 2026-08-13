"""Run a coding task with the executable coding agent."""

from __future__ import annotations

import json
from pathlib import Path

from agent.coding_agent import CodingAgent


def load_task(task_path: str | Path) -> dict:
    """Load a coding task from JSON."""

    path = Path(task_path)

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    """Run the first coding-agent task."""

    task = load_task("tasks/task_001.json")

    print(f"Task: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Target: {task['target_file']}")
    print()

    agent = CodingAgent(task["workspace"])

    result = agent.solve(
        target_file=task["target_file"],
        max_iterations=task["max_iterations"],
    )

    print()
    print("=== Agent Result ===")
    print(f"Success: {result.success}")
    print(f"Iterations: {result.iterations}")
    print(f"Message: {result.message}")


if __name__ == "__main__":
    main()
