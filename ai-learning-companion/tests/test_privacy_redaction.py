import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('ai-learning-companion'))
from ai_tutor_proxy.privacy import PrivacyMode, is_provider_call_allowed, is_learner_context_allowed, normalize_privacy_mode
from ai_tutor_proxy.redaction import redact_secrets

class TestPrivacyAndRedaction(unittest.TestCase):
    def test_privacy_modes(self):
        self.assertFalse(is_provider_call_allowed(PrivacyMode.LOCAL_ONLY.value))
        self.assertTrue(is_provider_call_allowed(PrivacyMode.PUBLIC_CURRICULUM_ONLY.value))
        self.assertTrue(is_provider_call_allowed(PrivacyMode.LEARNER_CONTEXT_ALLOWED.value))
        
        # Test unknown/invalid privacy modes return False
        self.assertFalse(is_provider_call_allowed("invalid_mode"))
        self.assertFalse(is_provider_call_allowed(""))
        
        self.assertFalse(is_learner_context_allowed(PrivacyMode.LOCAL_ONLY.value))
        self.assertFalse(is_learner_context_allowed(PrivacyMode.PUBLIC_CURRICULUM_ONLY.value))
        self.assertTrue(is_learner_context_allowed(PrivacyMode.LEARNER_CONTEXT_ALLOWED.value))

    def test_normalize_privacy_mode(self):
        self.assertEqual(normalize_privacy_mode(PrivacyMode.LOCAL_ONLY.value), "local_only")
        self.assertEqual(normalize_privacy_mode(PrivacyMode.PUBLIC_CURRICULUM_ONLY.value), "public_curriculum_only")
        self.assertEqual(normalize_privacy_mode(PrivacyMode.LEARNER_CONTEXT_ALLOWED.value), "learner_context_allowed")
        # Normalization of invalid modes
        self.assertEqual(normalize_privacy_mode("invalid_mode"), "local_only")
        self.assertEqual(normalize_privacy_mode(""), "local_only")
        self.assertEqual(normalize_privacy_mode(None), "local_only")

    def test_redact_secrets(self):
        cases = [
            ("Here is my key: API_KEY=abc1234567890", "Here is my key: [REDACTED_SECRET]"),
            ("token sk-1234567890abcdef1234567890abcdef here", "token [REDACTED_SECRET] here"),
            ("google AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6 here", "google [REDACTED_SECRET] here"),
            ("Bearer my_token.123", "[REDACTED_SECRET]"),
            ("This is a safe text.", "This is a safe text."),
            ("key='1234567890abcdef1234'", "[REDACTED_SECRET]")
        ]
        
        for text, expected in cases:
            self.assertEqual(redact_secrets(text), expected)

if __name__ == "__main__":
    unittest.main()
