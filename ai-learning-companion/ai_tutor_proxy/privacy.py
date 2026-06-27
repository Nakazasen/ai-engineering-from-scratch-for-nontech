"""
Privacy modes for AI Tutor.
"""
from enum import Enum

class PrivacyMode(Enum):
    LOCAL_ONLY = "local_only"
    PUBLIC_CURRICULUM_ONLY = "public_curriculum_only"
    LEARNER_CONTEXT_ALLOWED = "learner_context_allowed"

def is_provider_call_allowed(mode: str) -> bool:
    allowed_modes = {
        PrivacyMode.PUBLIC_CURRICULUM_ONLY.value,
        PrivacyMode.LEARNER_CONTEXT_ALLOWED.value
    }
    return mode in allowed_modes

def is_learner_context_allowed(mode: str) -> bool:
    return mode == PrivacyMode.LEARNER_CONTEXT_ALLOWED.value

def normalize_privacy_mode(mode: str) -> str:
    valid_modes = {m.value for m in PrivacyMode}
    if mode in valid_modes:
        return mode
    return PrivacyMode.LOCAL_ONLY.value
