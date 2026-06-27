"""
Prompt Builder for the AI Tutor.
"""
from typing import List, Dict, Any
from .privacy import is_learner_context_allowed

SYSTEM_PROMPT = """You are a Vietnamese AI tutor for non-technical learners.
Answer only from the provided curriculum context.
If the context does not contain enough information, you must say: "Chưa đủ dữ liệu trong bộ bài demo để trả lời chắc chắn."
Use simple Vietnamese.
Cite sources by lesson_id/source/heading.
Do not invent lesson content.
Do not ask for API keys or secrets."""

def build_prompt(
    question: str,
    chunks: List[Dict[str, Any]],
    privacy_mode: str,
    learner_context: Dict[str, Any] = None
) -> str:
    prompt_parts = [SYSTEM_PROMPT, "\n"]
    
    if learner_context and is_learner_context_allowed(privacy_mode):
        prompt_parts.append("LEARNER CONTEXT:")
        # We only serialize a simplified summary, not raw objects
        summary = {
            "track_id": learner_context.get("track_id"),
            "current_lesson_id": learner_context.get("current_lesson_id"),
            "completed_lessons": learner_context.get("completed_lessons", []),
            "quiz_scores": learner_context.get("quiz_scores", {})
        }
        prompt_parts.append(str(summary))
        prompt_parts.append("\n")

    prompt_parts.append("RETRIEVED CURRICULUM CHUNKS:")
    if not chunks:
        prompt_parts.append("None")
    else:
        for i, chunk in enumerate(chunks):
            lesson_id = chunk.get("lesson_id", "unknown")
            heading = chunk.get("heading", "unknown")
            text = chunk.get("text", "")
            prompt_parts.append(f"[{i+1}] Source: {lesson_id} - {heading}\n{text}")
    
    prompt_parts.append("\nUSER QUESTION:")
    prompt_parts.append(question)
    
    prompt_parts.append("\nREQUIRED OUTPUT:\n- Short answer in Vietnamese\n- Why it matters\n- Source citations")
    
    return "\n".join(prompt_parts)
