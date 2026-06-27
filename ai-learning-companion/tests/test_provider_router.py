import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('ai-learning-companion'))
from unittest.mock import patch, MagicMock
from ai_tutor_proxy.provider_router import TutorProviderRouter
from ai_tutor_proxy.providers.base import TutorProviderResult

class TestProviderRouter(unittest.TestCase):
    def setUp(self):
        self.router = TutorProviderRouter()
        # Disable gemini and openai to force mock provider
        self.router.providers[0].check_availability = lambda: False
        self.router.providers[1].check_availability = lambda: False
        # Explicitly enable MockProvider for testing
        self.router.providers[2].explicitly_enabled = True

    @patch('ai_tutor_proxy.provider_router.retrieve_top_chunks')
    def test_local_only_mode(self, mock_retrieve):
        mock_retrieve.return_value = [{"title": "T1", "heading": "H1", "text": "Content", "lesson_id": "L1"}]
        result = self.router.route_request("Hello", "local_only")
        
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["provider_id"], "local_lexical")
        self.assertIn("Dựa trên nội dung tìm kiếm cục bộ", result["answer_text"])
        self.assertEqual(len(result["route_log"]), 1)
        self.assertEqual(result["route_log"][0]["reason"], "privacy_mode_blocked")

    @patch('ai_tutor_proxy.provider_router.retrieve_top_chunks')
    def test_invalid_privacy_mode(self, mock_retrieve):
        mock_retrieve.return_value = [{"title": "T1", "heading": "H1", "text": "Content", "lesson_id": "L1"}]
        result = self.router.route_request("Hello", "invalid_or_empty_mode")
        
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["provider_id"], "local_lexical")
        self.assertIn("Dựa trên nội dung tìm kiếm cục bộ", result["answer_text"])
        self.assertEqual(len(result["route_log"]), 1)
        self.assertEqual(result["route_log"][0]["reason"], "privacy_mode_blocked")

    @patch('ai_tutor_proxy.provider_router.retrieve_top_chunks')
    def test_insufficient_evidence(self, mock_retrieve):
        mock_retrieve.return_value = []
        result = self.router.route_request("Hello", "public_curriculum_only")
        
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["provider_id"], "local_lexical")
        self.assertIn("Chưa đủ dữ liệu", result["answer_text"])
        self.assertEqual(len(result["route_log"]), 1)
        self.assertEqual(result["route_log"][0]["reason"], "insufficient_evidence")

    @patch('ai_tutor_proxy.provider_router.retrieve_top_chunks')
    def test_mock_success(self, mock_retrieve):
        mock_retrieve.return_value = [{"title": "T1", "heading": "H1", "text": "Content", "lesson_id": "L1"}]
        result = self.router.route_request("Hello", "public_curriculum_only")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["provider_id"], "mock")
        self.assertIn("Đây là câu trả lời mock", result["answer_text"])
        self.assertEqual(result["citations"], ["L1"])

    @patch('ai_tutor_proxy.provider_router.retrieve_top_chunks')
    def test_mock_auth_error_fallback(self, mock_retrieve):
        mock_retrieve.return_value = [{"title": "T1", "heading": "H1", "text": "Content", "lesson_id": "L1"}]
        # The prompt "sim_auth_error" will make mock provider return an auth error.
        # Since it's the only available provider, the router will exhaust providers and fallback to local.
        result = self.router.route_request("sim_auth_error", "public_curriculum_only")
        
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["provider_id"], "local_lexical")
        self.assertTrue(self.router.providers[2].is_disabled) # auth error should disable the provider
        self.assertEqual(len(result["route_log"]), 1)
        self.assertEqual(result["route_log"][0]["error_type"], "auth")

    @patch('ai_tutor_proxy.provider_router.retrieve_top_chunks')
    def test_mock_timeout_cooldown(self, mock_retrieve):
        mock_retrieve.return_value = [{"title": "T1", "heading": "H1", "text": "Content", "lesson_id": "L1"}]
        
        result = self.router.route_request("sim_timeout", "public_curriculum_only")
        
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["provider_id"], "local_lexical")
        self.assertFalse(self.router.providers[2].is_disabled)
        self.assertFalse(self.router.providers[2].is_available()) # Should be in cooldown

if __name__ == "__main__":
    unittest.main()
