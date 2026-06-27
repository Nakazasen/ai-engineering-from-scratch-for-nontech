"""Validate non-tech cards JSON data.

Run from repository root:
    python ai-learning-companion/tools/validate_nontech_cards.py
"""
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "lesson_id", "source_doc_path", "generated_at", "review_status", 
    "audience_level", "title_vi", "plain_language_summary_vi", 
    "why_it_matters_vi", "daily_life_analogy_vi", "mental_model_vi", 
    "minimal_example_vi", "real_app_use_vi", "common_misunderstandings_vi", 
    "source_citations", "check_questions"
]

def get_repo_root():
    return Path(__file__).resolve().parents[2]

def main():
    repo_root = get_repo_root()
    data_dir = repo_root / "ai-learning-companion" / "data"
    cards_file = data_dir / "nontech-cards" / "cards.demo.json"
    demo_lessons_file = data_dir / "demo_lessons.json"
    lessons_file = data_dir / "lessons.json"

    if not cards_file.exists():
        print(f"FAIL: {cards_file} does not exist.")
        return 1

    with open(cards_file, "r", encoding="utf-8") as f:
        cards_data = json.load(f).get("cards", [])

    if not (5 <= len(cards_data) <= 20):
        print(f"FAIL: Expected 5-20 cards, found {len(cards_data)}.")
        return 1

    with open(demo_lessons_file, "r", encoding="utf-8") as f:
        demo_lessons = json.load(f).get("demo_lessons", [])

    with open(lessons_file, "r", encoding="utf-8") as f:
        all_lessons = [item["id"] for item in json.load(f).get("lessons", [])]

    seen_ids = set()
    errors = []

    for idx, card in enumerate(cards_data):
        lesson_id = card.get("lesson_id")
        
        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in card:
                errors.append(f"Card {idx} ({lesson_id}) missing required field: {field}")
            elif not card[field]: # Empty string/list check
                errors.append(f"Card {idx} ({lesson_id}) has empty required field: {field}")

        # Check duplicates
        if lesson_id in seen_ids:
            errors.append(f"Duplicate lesson_id found: {lesson_id}")
        seen_ids.add(lesson_id)

        # Check against lessons.json
        if lesson_id not in all_lessons:
            errors.append(f"Card lesson_id {lesson_id} not found in lessons.json")

        # Check against demo_lessons.json exact match
        if lesson_id not in demo_lessons:
            errors.append(f"Card lesson_id {lesson_id} not found in demo_lessons.json")

        # Check source_doc_path exists
        doc_path = repo_root / card.get("source_doc_path", "")
        if not doc_path.exists():
            errors.append(f"Source doc path does not exist for {lesson_id}: {doc_path}")

        # Check questions
        questions = card.get("check_questions", [])
        if len(questions) != 3:
            errors.append(f"Card {lesson_id} has {len(questions)} questions. Expected 3.")
        else:
            for q_idx, q in enumerate(questions):
                if "question" not in q or "options" not in q or "correct" not in q or "explanation" not in q:
                    errors.append(f"Card {lesson_id} question {q_idx} missing required sub-fields.")
                else:
                    options = q["options"]
                    if not isinstance(options, list):
                        errors.append(f"Card {lesson_id} question {q_idx} options must be a list.")
                    elif not (3 <= len(options) <= 4):
                        errors.append(f"Card {lesson_id} question {q_idx} options length must be 3 or 4.")
                    
                    correct = q["correct"]
                    if type(correct) is not int:
                        errors.append(f"Card {lesson_id} question {q_idx} correct must be an integer.")
                    elif isinstance(options, list) and not (0 <= correct < len(options)):
                        errors.append(f"Card {lesson_id} question {q_idx} correct index is out of range.")

        # Check citations
        citations = card.get("source_citations", [])
        if len(citations) < 1:
            errors.append(f"Card {lesson_id} has no source citations.")
        else:
            for c_idx, c in enumerate(citations):
                quote = c.get("quote", "")
                if len(quote) > 200:
                    errors.append(f"Card {lesson_id} citation {c_idx} quote is too long ({len(quote)} chars). Expected < 200.")

    # Check exact match reverse (all demo lessons have cards)
    for dl in demo_lessons:
        if dl not in seen_ids:
            errors.append(f"Lesson {dl} in demo_lessons.json is missing a card.")

    if errors:
        print("FAIL: Validation errors found:")
        for err in errors:
            print(f" - {err}")
        return 1

    print(f"PASS: Validated {len(cards_data)} non-tech cards successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
