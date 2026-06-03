from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


TEXT_EXTENSIONS = {
    ".bash",
    ".cfg",
    ".conf",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

TEXT_FILENAMES = {
    "Dockerfile",
    "Makefile",
    "Procfile",
    "requirements.txt",
    "SKILL.md",
    "README",
    "README.md",
}

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "reports",
}


@dataclass(frozen=True)
class TextFile:
    path: Path
    relpath: str
    content: str
    lines: List[str]
    sha256: str


def is_probably_text(path: Path) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_EXTENSIONS


def iter_project_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def load_text_files(root: Path, max_bytes: int = 2_000_000) -> List[TextFile]:
    files: List[TextFile] = []
    root = root.resolve()
    for path in iter_project_files(root):
        if not is_probably_text(path):
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if len(raw) > max_bytes:
            continue
        digest = hashlib.sha256(raw).hexdigest()
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                content = raw.decode("latin-1")
            except UnicodeDecodeError:
                continue
        try:
            relpath = str(path.resolve().relative_to(root))
        except ValueError:
            relpath = str(path)
        files.append(TextFile(path=path, relpath=relpath, content=content, lines=content.splitlines(), sha256=digest))
    return files


def file_hashes(root: Path) -> List[dict]:
    root = root.resolve()
    hashes = []
    for path in iter_project_files(root):
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        try:
            relpath = str(path.resolve().relative_to(root))
        except ValueError:
            relpath = str(path)
        hashes.append({"path": relpath, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
    return hashes
