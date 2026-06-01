import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "ai-learning-companion" / "tools" / "scan_curriculum.py"
spec = importlib.util.spec_from_file_location("scan_curriculum", MODULE_PATH)
scan_curriculum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan_curriculum)


def test_parse_title_from_markdown_sample():
    title, metadata, headings = scan_curriculum.parse_markdown("# My Lesson\n\n## Build It\n")

    assert title == "My Lesson"
    assert headings == [{"level": 1, "text": "My Lesson"}, {"level": 2, "text": "Build It"}]


def test_parse_metadata_fields():
    markdown = """# Metadata Lesson

**Type:** Build
**Languages:** Python, TypeScript
**Prerequisites:** 00-setup, 01-math
**Time:** ~45 minutes
"""

    title, metadata, headings = scan_curriculum.parse_markdown(markdown)

    assert title == "Metadata Lesson"
    assert metadata["Type"] == "Build"
    assert scan_curriculum.split_list(metadata["Languages"]) == ["Python", "TypeScript"]
    assert scan_curriculum.split_list(metadata["Prerequisites"]) == ["00-setup", "01-math"]
    assert metadata["Time"] == "~45 minutes"


def test_scanner_does_not_crash_without_phases(tmp_path):
    index = scan_curriculum.build_index(tmp_path)

    assert index["lesson_count"] == 0
    assert index["lessons"] == []
    assert index["warnings"]


def test_output_lessons_are_sorted_deterministically(tmp_path):
    first = tmp_path / "phases" / "00-phase" / "02-b" / "docs"
    second = tmp_path / "phases" / "00-phase" / "01-a" / "docs"
    first.mkdir(parents=True)
    second.mkdir(parents=True)
    (first / "en.md").write_text("# B Lesson\n", encoding="utf-8")
    (second / "en.md").write_text("# A Lesson\n", encoding="utf-8")

    index = scan_curriculum.build_index(tmp_path)

    assert [lesson["id"] for lesson in index["lessons"]] == ["00-phase/01-a", "00-phase/02-b"]
