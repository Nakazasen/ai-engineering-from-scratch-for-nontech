"""
Redaction utilities to prevent secret leakage in logs and outputs.
"""
import re

# Simple regexes to catch common patterns. Should not over-redact normal text.
SECRET_PATTERNS = [
    re.compile(r'(?i)api_key[=\s]*["\']?([^"\'\s]+)["\']?'),
    re.compile(r'sk-[a-zA-Z0-9_-]{32,}'),
    re.compile(r'AIza[0-9A-Za-z_\-]{34,}'),
    re.compile(r'(?i)bearer\s+[a-zA-Z0-9_.-]+'),
    re.compile(r'(?i)key[=\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?')
]

def redact_secrets(text: str) -> str:
    if not isinstance(text, str):
        return text
    
    redacted_text = text
    for pattern in SECRET_PATTERNS:
        redacted_text = pattern.sub("[REDACTED_SECRET]", redacted_text)
    
    return redacted_text

def redact_dict(data: dict) -> dict:
    """Recursively redact secrets in a dictionary."""
    redacted = {}
    for k, v in data.items():
        if isinstance(v, str):
            redacted[k] = redact_secrets(v)
        elif isinstance(v, dict):
            redacted[k] = redact_dict(v)
        elif isinstance(v, list):
            redacted[k] = [redact_secrets(item) if isinstance(item, str) else item for item in v]
        else:
            redacted[k] = v
    return redacted
