"""
Base classes for Tutor Providers.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time

class TutorProviderResult:
    def __init__(
        self,
        status: str,
        answer_text: str = "",
        provider_id: str = "",
        model: str = "",
        error_type: str = "",
        error_message_redacted: str = "",
        latency_ms: int = 0
    ):
        self.status = status # 'success' or 'error'
        self.answer_text = answer_text
        self.provider_id = provider_id
        self.model = model
        self.error_type = error_type
        self.error_message_redacted = error_message_redacted
        self.latency_ms = latency_ms
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "answer_text": self.answer_text,
            "provider_id": self.provider_id,
            "model": self.model,
            "error_type": self.error_type,
            "error_message_redacted": self.error_message_redacted,
            "latency_ms": self.latency_ms
        }

class TutorProvider(ABC):
    def __init__(self, provider_id: str, display_name: str):
        self.provider_id = provider_id
        self.display_name = display_name
        self.is_disabled = False
        self.cooldown_until = 0.0

    def is_available(self) -> bool:
        if self.is_disabled:
            return False
        if time.time() < self.cooldown_until:
            return False
        return self.check_availability()

    @abstractmethod
    def check_availability(self) -> bool:
        """Provider specific availability check (e.g. checking env vars)"""
        pass

    @abstractmethod
    def answer(self, prompt: str) -> TutorProviderResult:
        """Call the provider and return a result"""
        pass

    def apply_cooldown(self, seconds: int):
        self.cooldown_until = time.time() + seconds

    def disable(self):
        self.is_disabled = True
