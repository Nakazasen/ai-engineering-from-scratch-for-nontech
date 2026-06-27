"""
Gemini Provider using urllib.request.
"""
import os
import json
import time
import urllib.request
import urllib.error
from .base import TutorProvider, TutorProviderResult
from ..redaction import redact_secrets

class GeminiProvider(TutorProvider):
    def __init__(self):
        super().__init__(provider_id="gemini", display_name="Gemini AI")
        self.api_key = os.environ.get("ALC_GEMINI_API_KEY")
        self.model = os.environ.get("ALC_GEMINI_MODEL", "gemini-1.5-flash")

    def check_availability(self) -> bool:
        return bool(self.api_key)

    def answer(self, prompt: str) -> TutorProviderResult:
        if not self.api_key:
             return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model=self.model,
                error_type="auth",
                error_message_redacted="Missing API key",
            )
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                try:
                    answer_text = result['candidates'][0]['content']['parts'][0]['text']
                    return TutorProviderResult(
                        status="success",
                        answer_text=answer_text,
                        provider_id=self.provider_id,
                        model=self.model,
                        latency_ms=int((time.time() - start_time) * 1000)
                    )
                except (KeyError, IndexError) as e:
                    return TutorProviderResult(
                        status="error",
                        provider_id=self.provider_id,
                        model=self.model,
                        error_type="bad_response",
                        error_message_redacted=f"Failed to parse response: {str(e)}",
                        latency_ms=int((time.time() - start_time) * 1000)
                    )

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            redacted_body = redact_secrets(error_body)
            error_type = "provider_error"
            if e.code in (401, 403):
                error_type = "auth"
            elif e.code == 429:
                error_type = "rate_limit"
            elif e.code >= 500:
                error_type = "server_error"

            return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model=self.model,
                error_type=error_type,
                error_message_redacted=f"HTTP {e.code}: {redacted_body}",
                latency_ms=int((time.time() - start_time) * 1000)
            )
        except urllib.error.URLError as e:
            return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model=self.model,
                error_type="network",
                error_message_redacted=f"Network Error: {redact_secrets(str(e.reason))}",
                latency_ms=int((time.time() - start_time) * 1000)
            )
        except TimeoutError:
            return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model=self.model,
                error_type="timeout",
                error_message_redacted="Request timed out",
                latency_ms=int((time.time() - start_time) * 1000)
            )
        except Exception as e:
             return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model=self.model,
                error_type="unknown",
                error_message_redacted=f"Unknown Error: {redact_secrets(str(e))}",
                latency_ms=int((time.time() - start_time) * 1000)
            )
