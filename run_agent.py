"""Run a coding task with the executable coding agent."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from agent.coding_agent import CodingAgent


def main() -> None:
    """Load a task, run the agent, and save its trajectory."""

    repo_root = Path(__file__).parent.resolve()

    if len(sys.argv) > 1:
        task_path = repo_root / sys.argv[1]
    else:
        task_path = repo_root / "tasks" / "task_001.json"

    if not task_path.exists():
        raise FileNotFoundError(
            f"Task file does not exist: {task_path}"
        )

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
        test_command=task["test_command"],
    )

    result = agent.solve(
        target_file=task["target_file"],
        description=task["description"],
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
