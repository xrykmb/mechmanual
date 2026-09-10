from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .parse import load_sections
from .search import search_sections


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mechmanual", description="Search equipment maintenance manuals.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("version", help="Print package version")
    search = sub.add_parser("search", help="Keyword search over local manuals")
    search.add_argument("query", help="Search text, e.g. 润滑")
    search.add_argument("--manuals", default="examples/manuals", help="Directory of .md / .txt manuals")
    search.add_argument("-k", type=int, default=5, help="Max hits")
    args = parser.parse_args(argv)

    if args.command == "version":
        print(__version__)
        return 0

    root = Path(args.manuals)
    if not root.is_dir():
        print(f"manual directory not found: {root}")
        return 2
    hits = search_sections(args.query, load_sections(root), limit=args.k)
    if not hits:
        print("no hits")
        return 1
    for hit in hits:
        print(f"[{hit.score}] {hit.section.title}  ({hit.section.source})")
        preview = hit.section.text.replace("\n", " ")[:160]
        print(f"    {preview}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
