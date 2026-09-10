from pathlib import Path

from mechmanual.cli import main
from mechmanual.parse import load_sections
from mechmanual.search import search_sections


def test_search_hits_lubrication_section(tmp_path: Path) -> None:
    path = tmp_path / "pump.md"
    path.write_text("## 润滑\n每 2000 小时补脂。\n## 其它\n无关内容。\n", encoding="utf-8")
    hits = search_sections("润滑 小时", load_sections(tmp_path), limit=3)
    assert hits
    assert hits[0].section.title == "润滑"


def test_cli_search_sample_manual() -> None:
    assert main(["search", "轴承过热", "--manuals", "examples/manuals"]) == 0
