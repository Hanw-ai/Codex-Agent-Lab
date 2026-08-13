"""Run a coding task with the executable coding agent."""

from __future__ import annotations

import json
from pathlib import Path

from agent.coding_agent import CodingAgent


def main() -> None:
    """Load a task, run the agent, and save its trajectory."""

    repo_root = Path(__file__).parent.resolve()

    task_path = repo_root / "tasks" / "task_001.json"

    task = json.loads(
        task_path.read_text(encoding="utf-8")
    )

    print(f"Task: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Target: {task['target_file']}")

    workspace_path = repo_root / task["workspace"]

    agent = CodingAgent(
        workspace=workspace_path,
        task_id=task["task_id"],
    )

    result = agent.solve(
        target_file=task["target_file"],
        max_iterations=task["max_iterations"],
    )

    output_path = (
        repo_root
        / "outputs"
        / f"{task['task_id']}_trajectory.json"
    )

    agent.trajectory.save(output_path)

    print("\n=== Agent Result ===")
    print(f"Success: {result.success}")
    print(f"Iterations: {result.iterations}")
    print(f"Message: {result.message}")
    print(f"Trajectory: {output_path}")


if __name__ == "__main__":
    main()
