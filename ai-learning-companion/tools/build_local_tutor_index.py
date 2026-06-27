"""Build a deterministic local tutor search index for the companion app."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

TRACK_NAMES = {
    "work_ai_user": "Track A: AI User Manh",
    "workflow_operator": "Track B: AI Workflow Operator",
    "ai_engineer_from_scratch": "Track C: AI Engineer Tu Nen Tang",
}

CARD_FIELDS = [
    ("summary", "plain_language_summary_vi", ["tom tat", "khai niem", "giai thich"]),
    ("why", "why_it_matters_vi", ["vi sao", "ly do", "quan trong"]),
    ("analogy", "daily_life_analogy_vi", ["an du", "vi du doi thuong", "non-tech"]),
    ("mental_model", "mental_model_vi", ["mo hinh tu duy", "mental model", "hieu nhanh"]),
    ("minimal_example", "minimal_example_vi", ["vi du", "toi gian", "example"]),
    ("real_app", "real_app_use_vi", ["ung dung", "cong viec", "app that"]),
]

BASE_KEYWORDS = {
    "rag": ["rag", "retrieval", "truy xuat", "tai lieu", "hoi dap", "nguon"],
    "prompt": ["prompt", "prompting", "cau lenh", "viet lenh", "prompt engineering"],
    "api": ["api", "api key", "key", "mat khau", "token", "bao mat"],
    "transformer": ["transformer", "attention", "chu y", "mo hinh ngon ngu"],
    "embedding": ["embedding", "vector", "bieu dien so", "nhung"],
    "nontech": ["khong biet code", "non-tech", "nguoi moi", "beginner"],
}


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = str(value).strip()
        if clean and clean.lower() not in seen:
            seen.add(clean.lower())
            result.append(clean)
    return result


def track_ids_for_lesson(lesson_id: str, tracks: dict[str, Any]) -> list[str]:
    return sorted(track_id for track_id, track in tracks.items() if lesson_id in track.get("lessons", []))


def keywords_for_text(*parts: str) -> list[str]:
    text = " ".join(part for part in parts if part).lower()
    keywords: list[str] = []
    for trigger, terms in BASE_KEYWORDS.items():
        if trigger in text or any(term in text for term in terms):
            keywords.extend(terms)
    keywords.extend(re.findall(r"[\wÀ-ỹ-]{3,}", text, flags=re.UNICODE)[:24])
    return unique(keywords)


def make_chunk(**kwargs: Any) -> dict[str, Any]:
    kwargs["keywords"] = unique(kwargs.get("keywords", []))
    kwargs["text"] = str(kwargs.get("text", "")).strip()
    kwargs["title"] = str(kwargs.get("title", "")).strip()
    return kwargs


def build_index(repo_root: Path) -> dict[str, Any]:
    data_dir = repo_root / "ai-learning-companion" / "data"
    lessons_data = read_json(data_dir / "lessons.json")
    demo_data = read_json(data_dir / "demo_lessons.json")
    cards_data = read_json(data_dir / "nontech-cards" / "cards.demo.json")
    tracks = read_json(data_dir / "learning_tracks.json")
    placement_questions = read_json(data_dir / "placement_questions.json")

    lessons = lessons_data.get("lessons", [])
    lesson_map = {lesson["id"]: lesson for lesson in lessons}
    demo_ids = set(demo_data.get("demo_lessons", []))
    chunks: list[dict[str, Any]] = []
    warnings: list[str] = []

    for card in sorted(cards_data.get("cards", []), key=lambda item: item["lesson_id"]):
        lesson_id = card["lesson_id"]
        if lesson_id not in lesson_map:
            warnings.append(f"Card lesson does not exist in lessons.json: {lesson_id}")
            continue
        if lesson_id not in demo_ids:
            warnings.append(f"Card lesson is not in demo_lessons.json: {lesson_id}")
            continue
        lesson = lesson_map[lesson_id]
        title = card.get("title_vi") or lesson.get("title") or lesson_id
        source_path = card.get("source_doc_path") or lesson.get("doc_path") or ""
        track_ids = track_ids_for_lesson(lesson_id, tracks)
        base_keywords = keywords_for_text(title, lesson_id, lesson.get("title", ""))
        for section, field, extra_keywords in CARD_FIELDS:
            text = card.get(field, "")
            if text:
                chunks.append(make_chunk(
                    audience_level=card.get("audience_level", "nontech_beginner"),
                    chunk_id=f"nontech_card:{lesson_id}:{section}",
                    citation_label=f"{title} · {section.replace('_', ' ')}",
                    keywords=base_keywords + extra_keywords + keywords_for_text(text),
                    lesson_id=lesson_id,
                    section=field,
                    source_path=source_path,
                    source_type="nontech_card",
                    text=text,
                    title=title,
                    track_ids=track_ids,
                ))
        misunderstandings = card.get("common_misunderstandings_vi") or []
        if misunderstandings:
            text = " ".join(misunderstandings)
            chunks.append(make_chunk(
                audience_level=card.get("audience_level", "nontech_beginner"),
                chunk_id=f"nontech_card:{lesson_id}:misunderstandings",
                citation_label=f"{title} · hiểu sai thường gặp",
                keywords=base_keywords + ["hiểu sai", "nhầm lẫn", "cảnh báo"] + keywords_for_text(text),
                lesson_id=lesson_id,
                section="common_misunderstandings_vi",
                source_path=source_path,
                source_type="nontech_card",
                text=text,
                title=title,
                track_ids=track_ids,
            ))

    for lesson in sorted(lessons, key=lambda item: item["id"]):
        headings = " ".join(h.get("text", "") for h in lesson.get("headings", []))
        text = f"{lesson.get('title', '')}. {lesson.get('id', '')}. Headings: {headings}"
        chunks.append(make_chunk(
            audience_level="all",
            chunk_id=f"lesson_metadata:{lesson['id']}",
            citation_label=f"{lesson.get('title', lesson['id'])} · metadata",
            keywords=keywords_for_text(text, lesson.get("doc_path", "")),
            lesson_id=lesson["id"],
            section="lesson_metadata",
            source_path=lesson.get("doc_path", ""),
            source_type="lesson_metadata",
            text=text,
            title=lesson.get("title", lesson["id"]),
            track_ids=track_ids_for_lesson(lesson["id"], tracks),
        ))

    for track_id, track in sorted(tracks.items()):
        lessons_text = ", ".join(track.get("lessons", []))
        text = f"{TRACK_NAMES.get(track_id, track_id)}. {track.get('description', '')} Lessons: {lessons_text}"
        chunks.append(make_chunk(
            audience_level="nontech_beginner",
            chunk_id=f"track:{track_id}",
            citation_label=f"{TRACK_NAMES.get(track_id, track_id)} · learning track",
            keywords=keywords_for_text(track_id, text) + ["track", "lộ trình", "học gì tiếp"],
            lesson_id=None,
            section=track_id,
            source_path="ai-learning-companion/data/learning_tracks.json",
            source_type="track",
            text=text,
            title=TRACK_NAMES.get(track_id, track_id),
            track_ids=[track_id],
        ))

    placement_text = " ".join(q.get("text", "") + " " + " ".join(opt.get("text", "") for opt in q.get("options", [])) for q in placement_questions)
    chunks.append(make_chunk(
        audience_level="nontech_beginner",
        chunk_id="placement:questions",
        citation_label="Placement Test · câu hỏi điểm bắt đầu",
        keywords=keywords_for_text(placement_text) + ["placement", "kiểm tra", "bắt đầu", "không biết code"],
        lesson_id=None,
        section="placement_questions",
        source_path="ai-learning-companion/data/placement_questions.json",
        source_type="placement",
        text=placement_text,
        title="Kiểm tra điểm bắt đầu",
        track_ids=sorted(tracks.keys()),
    ))

    chunks.sort(key=lambda item: item["chunk_id"])
    return {
        "chunk_count": len(chunks),
        "chunks": chunks,
        "generated_at": "1970-01-01T00:00:00+00:00",
        "schema_version": 1,
        "source_files": [
            "ai-learning-companion/data/lessons.json",
            "ai-learning-companion/data/demo_lessons.json",
            "ai-learning-companion/data/nontech-cards/cards.demo.json",
            "ai-learning-companion/data/learning_tracks.json",
            "ai-learning-companion/data/placement_questions.json",
        ],
        "warnings": warnings,
    }


def validate_index(index: dict[str, Any], repo_root: Path) -> None:
    lessons_data = read_json(repo_root / "ai-learning-companion" / "data" / "lessons.json")
    lesson_ids = {lesson["id"] for lesson in lessons_data.get("lessons", [])}
    assert index["schema_version"] == 1
    assert index["chunk_count"] == len(index["chunks"])
    seen: set[str] = set()
    for chunk in index["chunks"]:
        assert chunk["chunk_id"] not in seen, chunk["chunk_id"]
        seen.add(chunk["chunk_id"])
        assert chunk["source_type"] in {"lesson_metadata", "nontech_card", "track", "placement"}
        assert chunk["title"] and chunk["text"] and chunk["source_path"] and chunk["citation_label"]
        if chunk["lesson_id"] is not None:
            assert chunk["lesson_id"] in lesson_ids, chunk["lesson_id"]


def main() -> int:
    repo_root = repo_root_from_script()
    output_path = repo_root / "ai-learning-companion" / "data" / "local_tutor_index.demo.json"
    index = build_index(repo_root)
    validate_index(index, repo_root)
    output_path.write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {index['chunk_count']} local tutor chunks to {output_path}")
    for warning in index["warnings"]:
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
