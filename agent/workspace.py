"""Workspace tools for reading and modifying coding-agent files."""

from __future__ import annotations

from pathlib import Path


class WorkspaceManager:
    """Provide controlled file access inside an agent workspace."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()

        if not self.root.exists():
            raise FileNotFoundError(
                f"Workspace does not exist: {self.root}"
            )

    def _resolve_path(self, relative_path: str | Path) -> Path:
        """Resolve a path and prevent access outside the workspace."""

        path = (self.root / relative_path).resolve()

        if path != self.root and self.root not in path.parents:
            raise ValueError(
                f"Path escapes workspace: {relative_path}"
            )

        return path

    def list_files(self) -> list[str]:
        """Return all files in the workspace."""

        return sorted(
            str(path.relative_to(self.root))
            for path in self.root.rglob("*")
            if path.is_file()
        )

    def read_file(self, relative_path: str | Path) -> str:
        """Read a UTF-8 text file from the workspace."""

        path = self._resolve_path(relative_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"File does not exist: {relative_path}"
            )

        return path.read_text(encoding="utf-8")

    def write_file(
        self,
        relative_path: str | Path,
        content: str,
    ) -> None:
        """Write UTF-8 text to a file inside the workspace."""

        path = self._resolve_path(relative_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )
