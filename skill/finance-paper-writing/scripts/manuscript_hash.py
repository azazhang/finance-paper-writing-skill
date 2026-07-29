from __future__ import annotations

import hashlib
import re
from pathlib import Path


TEX_DEPENDENCY_PATTERN = re.compile(
    r"\\(?:input|include|subfile)\s*\{([^}]+)\}"
)


def strip_tex_comments(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        output: list[str] = []
        backslashes = 0
        for character in line:
            if character == "%" and backslashes % 2 == 0:
                break
            output.append(character)
            if character == "\\":
                backslashes += 1
            else:
                backslashes = 0
        cleaned.append("".join(output))
    return "\n".join(cleaned)


def manuscript_entries(manuscript: Path) -> list[tuple[Path, bool]]:
    manuscript = manuscript.expanduser().resolve()
    if manuscript.suffix.lower() != ".tex":
        return [(manuscript, manuscript.is_file())]

    entries: list[tuple[Path, bool]] = []
    visited: set[Path] = set()

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in visited:
            return
        visited.add(path)
        exists = path.is_file()
        entries.append((path, exists))
        if not exists:
            return
        text = strip_tex_comments(
            path.read_text(encoding="utf-8", errors="replace")
        )
        for match in TEX_DEPENDENCY_PATTERN.finditer(text):
            dependency = (path.parent / match.group(1).strip()).resolve()
            if not dependency.suffix:
                dependency = dependency.with_suffix(".tex")
            visit(dependency)

    visit(manuscript)
    return sorted(entries, key=lambda item: str(item[0]))


def manuscript_files(manuscript: Path) -> list[Path]:
    return [path for path, exists in manuscript_entries(manuscript) if exists]


def manuscript_sha256(manuscript: Path) -> str:
    manuscript = manuscript.expanduser().resolve()
    if not manuscript.is_file():
        raise FileNotFoundError(manuscript)

    digest = hashlib.sha256()
    for path, exists in manuscript_entries(manuscript):
        digest.update(str(path).encode("utf-8"))
        digest.update(b"\0")
        if exists:
            digest.update(path.read_bytes())
        else:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return digest.hexdigest()
