from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUPPORTED = {".md", ".txt"}


@dataclass(frozen=True)
class Section:
    """One heading block from a manual file."""

    source: str
    title: str
    text: str


def load_sections(manual_dir: Path) -> list[Section]:
    """Split markdown-like manuals on ATX headings (## )."""
    sections: list[Section] = []
    for path in sorted(manual_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        current_title = path.stem
        buffer: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                _flush(sections, path, current_title, buffer)
                current_title = line[3:].strip()
                buffer = []
            else:
                buffer.append(line)
        _flush(sections, path, current_title, buffer)
    return sections


def _flush(sections: list[Section], path: Path, title: str, buffer: list[str]) -> None:
    text = "\n".join(buffer).strip()
    if text:
        sections.append(Section(source=str(path), title=title, text=text))
