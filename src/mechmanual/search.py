from __future__ import annotations

from dataclasses import dataclass

from .parse import Section


@dataclass(frozen=True)
class Hit:
    section: Section
    score: int


def search_sections(query: str, sections: list[Section], *, limit: int = 5) -> list[Hit]:
    """Score a section by how many query tokens appear in title+body."""
    tokens = [part.lower() for part in query.split() if part.strip()]
    if not tokens:
        return []
    hits: list[Hit] = []
    for section in sections:
        blob = f"{section.title}\n{section.text}".lower()
        score = sum(blob.count(token) for token in tokens)
        if score > 0:
            hits.append(Hit(section=section, score=score))
    hits.sort(key=lambda item: item.score, reverse=True)
    return hits[:limit]
