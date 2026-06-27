"""
OpenAI-Compatible Provider using urllib.request.
"""
import os
import json
import time
import urllib.request
import urllib.error
from .base import TutorProvider, TutorProviderResult
from ..redaction import redact_secrets

class OpenAICompatibleProvider(TutorProvider):
    def __init__(self):
        super().__init__(provider_id="openai_compatible", display_name="OpenAI Compatible")
        self.api_key = os.environ.get("ALC_OPENAI_COMPATIBLE_API_KEY")
        self.base_url = os.environ.get("ALC_OPENAI_COMPATIBLE_BASE_URL")
        self.model = os.environ.get("ALC_OPENAI_COMPATIBLE_MODEL", "gpt-3.5-turbo")

    def check_availability(self) -> bool:
        return bool(self.api_key and self.base_url)

    def answer(self, prompt: str) -> TutorProviderResult:
        if not self.check_availability():
             return TutorProviderResult(
                status="error",
                provider_id=self.provider_id,
                model=self.model,
                error_type="auth",
                error_message_redacted="Missing API key or Base URL",
            )
        
        url = self.base_url
        if not url.endswith('/'):
            url += '/'
        url += "chat/completions"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                try:
                    answer_text = result['choices'][0]['message']['content']
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
