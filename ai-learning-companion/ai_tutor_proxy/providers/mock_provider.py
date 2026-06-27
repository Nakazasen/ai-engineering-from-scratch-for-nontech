"""
Mock Provider for testing.
"""
import os
import time
from .base import TutorProvider, TutorProviderResult

class MockProvider(TutorProvider):
    def __init__(self):
        super().__init__(provider_id="mock", display_name="Mock Provider")
        self.explicitly_enabled = False

    def check_availability(self) -> bool:
        if self.explicitly_enabled:
            return True
        return os.environ.get("ALC_ENABLE_MOCK_PROVIDER") == "1"

    def answer(self, prompt: str) -> TutorProviderResult:
        start_time = time.time()
        
        # Deterministic simulation based on prompt content
        if "sim_timeout" in prompt:
            return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model="mock_model",
                error_type="timeout",
                error_message_redacted="Simulated timeout",
                latency_ms=int((time.time() - start_time) * 1000)
            )
        elif "sim_auth_error" in prompt:
            return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model="mock_model",
                error_type="auth",
                error_message_redacted="Simulated auth error",
                latency_ms=int((time.time() - start_time) * 1000)
            )
        elif "sim_rate_limit" in prompt:
            return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model="mock_model",
                error_type="rate_limit",
                error_message_redacted="Simulated rate limit",
                latency_ms=int((time.time() - start_time) * 1000)
            )
        elif "sim_network_error" in prompt:
             return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model="mock_model",
                error_type="network",
                error_message_redacted="Simulated network error",
                latency_ms=int((time.time() - start_time) * 1000)
            )

        return TutorProviderResult(
            status="success",
            answer_text="Đây là câu trả lời mock từ AI Tutor. Dựa trên nội dung bài học, ...",
            provider_id=self.provider_id,
            model="mock_model",
            latency_ms=int((time.time() - start_time) * 1000)
        )
