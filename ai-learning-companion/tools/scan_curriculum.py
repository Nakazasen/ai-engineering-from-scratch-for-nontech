"""Scan curriculum lessons into a deterministic JSON index.

Run from the repository root:
    python ai-learning-companion/tools/scan_curriculum.py
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

METADATA_KEYS = ("Type", "Languages", "Prerequisites", "Time")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
METADATA_RE = re.compile(r"^\*\*(Type|Languages|Prerequisites|Time):\*\*\s*(.*?)\s*$")


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def relative_posix(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def split_list(value: str) -> list[str]:
    if not value or value.strip().lower() in {"none", "n/a", "na", "-"}:
        return []
    return [item.strip() for item in re.split(r",|;", value) if item.strip()]


def parse_markdown(markdown: str) -> tuple[str, dict[str, str], list[dict[str, object]]]:
    title = "Untitled lesson"
    metadata = {key: "" for key in METADATA_KEYS}
    headings: list[dict[str, object]] = []

    for line in markdown.splitlines():
        heading_match = HEADING_RE.match(line)
        if heading_match:
            text = heading_match.group(2).strip().strip("#").strip()
            level = len(heading_match.group(1))
            headings.append({"level": level, "text": text})
            if level == 1 and title == "Untitled lesson":
                title = text
            continue

        metadata_match = METADATA_RE.match(line)
        if metadata_match:
            metadata[metadata_match.group(1)] = metadata_match.group(2).strip()

    return title, metadata, headings


def find_code_files(lesson_dir: Path, repo_root: Path) -> list[str]:
    code_dir = lesson_dir / "code"
    if not code_dir.exists() or not code_dir.is_dir():
        return []
    return sorted(
        relative_posix(path, repo_root)
        for path in code_dir.rglob("*")
        if path.is_file()
    )


def lesson_from_doc(doc_path: Path, repo_root: Path) -> dict[str, object]:
    lesson_dir = doc_path.parents[1]
    phase_dir = lesson_dir.parent
    markdown = doc_path.read_text(encoding="utf-8")
    title, metadata, headings = parse_markdown(markdown)

    phase = phase_dir.name
    lesson = lesson_dir.name
    return {
        "id": f"{phase}/{lesson}",
        "phase": phase,
        "lesson": lesson,
        "title": title,
        "doc_path": relative_posix(doc_path, repo_root),
        "time": metadata["Time"],
        "type": metadata["Type"],
        "languages": split_list(metadata["Languages"]),
        "prerequisites": split_list(metadata["Prerequisites"]),
        "headings": headings,
        "code_files": find_code_files(lesson_dir, repo_root),
    }


def discover_lesson_docs(phases_dir: Path) -> Iterable[Path]:
    return sorted(phases_dir.glob("**/docs/en.md"), key=lambda path: path.as_posix())


def build_index(repo_root: Path) -> dict[str, object]:
    warnings: list[str] = []
    phases_dir = repo_root / "phases"
    lessons: list[dict[str, object]] = []

    if not phases_dir.exists():
        warnings.append("Directory 'phases' was not found. Generated an empty lesson index.")
    else:
        doc_paths = list(discover_lesson_docs(phases_dir))
        if not doc_paths:
            warnings.append("No lesson docs matching 'phases/**/docs/en.md' were found.")
        for doc_path in doc_paths:
            lessons.append(lesson_from_doc(doc_path, repo_root))

    lessons.sort(key=lambda lesson: str(lesson["doc_path"]))
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo_root.resolve()),
        "lesson_count": len(lessons),
        "warnings": warnings,
        "lessons": lessons,
    }


def write_index(index: dict[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan curriculum lessons into lessons.json")
    parser.add_argument("--repo-root", type=Path, default=repo_root_from_script())
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root_from_script() / "ai-learning-companion" / "data" / "lessons.json",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output_path = args.output.resolve()
    index = build_index(repo_root)
    write_index(index, output_path)
    print(f"Wrote {index['lesson_count']} lessons to {output_path}")
    for warning in index["warnings"]:
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
