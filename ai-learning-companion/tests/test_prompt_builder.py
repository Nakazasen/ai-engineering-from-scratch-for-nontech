import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('ai-learning-companion'))
from ai_tutor_proxy.prompt_builder import build_prompt
from ai_tutor_proxy.privacy import PrivacyMode

class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        self.chunks = [
            {"lesson_id": "L1", "heading": "H1", "text": "This is chunk 1."}
        ]
        self.context = {
            "track_id": "beginner",
            "current_lesson_id": "L1",
            "completed_lessons": ["L0"],
            "quiz_scores": {"L0": 100}
        }
        self.question = "What is chunk 1?"

    def test_local_only_mode(self):
        prompt = build_prompt(self.question, self.chunks, PrivacyMode.LOCAL_ONLY.value, self.context)
        self.assertNotIn("LEARNER CONTEXT", prompt)
        self.assertIn("RETRIEVED CURRICULUM CHUNKS:", prompt)
        self.assertIn("L1 - H1", prompt)
        self.assertIn(self.question, prompt)

    def test_public_curriculum_only_mode(self):
        prompt = build_prompt(self.question, self.chunks, PrivacyMode.PUBLIC_CURRICULUM_ONLY.value, self.context)
        self.assertNotIn("LEARNER CONTEXT", prompt)
        self.assertNotIn("beginner", prompt)
        self.assertIn("RETRIEVED CURRICULUM CHUNKS:", prompt)
        self.assertIn("L1 - H1", prompt)

    def test_learner_context_allowed_mode(self):
        prompt = build_prompt(self.question, self.chunks, PrivacyMode.LEARNER_CONTEXT_ALLOWED.value, self.context)
        self.assertIn("LEARNER CONTEXT:", prompt)
        self.assertIn("beginner", prompt)
        self.assertIn("RETRIEVED CURRICULUM CHUNKS:", prompt)
        
    def test_empty_chunks(self):
        prompt = build_prompt(self.question, [], PrivacyMode.PUBLIC_CURRICULUM_ONLY.value)
        self.assertIn("RETRIEVED CURRICULUM CHUNKS:", prompt)
        self.assertIn("None", prompt)

if __name__ == "__main__":
    unittest.main()
