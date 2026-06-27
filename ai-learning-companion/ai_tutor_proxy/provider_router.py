"""
Provider Router for AI Tutor.
"""
from typing import List, Dict, Any
from .providers.base import TutorProvider, TutorProviderResult
from .providers.mock_provider import MockProvider
from .providers.gemini_provider import GeminiProvider
from .providers.openai_compatible_provider import OpenAICompatibleProvider
from .privacy import is_provider_call_allowed
from .retrieval import retrieve_top_chunks
from .prompt_builder import build_prompt

class TutorProviderRouter:
    def __init__(self):
        # Ordered list of providers for waterfall fallback
        self.providers: List[TutorProvider] = [
            GeminiProvider(),
            OpenAICompatibleProvider(),
            MockProvider()
        ]
        self.max_attempts_total = 3

    def get_local_lexical_fallback(self, chunks: List[Dict[str, Any]]) -> TutorProviderResult:
        """Fallback to local lexical search"""
        if not chunks:
            return TutorProviderResult(
                status="fallback",
                answer_text="Chưa đủ dữ liệu trong bộ bài demo để trả lời chắc chắn.",
                provider_id="local_lexical"
            )
        
        # Build a simple answer from the top chunk
        top_chunk = chunks[0]
        title = top_chunk.get("title", "")
        heading = top_chunk.get("heading", "")
        text = top_chunk.get("text", "")
        lesson_id = top_chunk.get("lesson_id", "")
        
        answer_text = f"Dựa trên nội dung tìm kiếm cục bộ ({title} - {heading}):\n\n{text}"
        
        return TutorProviderResult(
            status="fallback",
            answer_text=answer_text,
            provider_id="local_lexical",
            model="lexical_search"
        )

    def route_request(self, question: str, privacy_mode: str, learner_context: Dict[str, Any] = None) -> TutorProviderResult:
        route_log = []
        
        from .privacy import normalize_privacy_mode
        privacy_mode = normalize_privacy_mode(privacy_mode)
        
        # 1. Retrieve chunks
        chunks = retrieve_top_chunks(question)
        
        # 2. Check privacy mode
        if not is_provider_call_allowed(privacy_mode):
            fallback_res = self.get_local_lexical_fallback(chunks)
            route_log.append({
                "provider_id": "local_lexical",
                "status": "success",
                "reason": "privacy_mode_blocked"
            })
            result_dict = fallback_res.to_dict()
            result_dict["route_log"] = route_log
            return result_dict

        # 3. Check evidence
        if not chunks:
            fallback_res = self.get_local_lexical_fallback([])
            route_log.append({
                "provider_id": "local_lexical",
                "status": "success",
                "reason": "insufficient_evidence"
            })
            result_dict = fallback_res.to_dict()
            result_dict["route_log"] = route_log
            return result_dict

        # 4. Build prompt
        prompt = build_prompt(question, chunks, privacy_mode, learner_context)
        
        # 5. Waterfall routing
        attempts = 0
        
        for provider in self.providers:
            if attempts >= self.max_attempts_total:
                break
                
            if not provider.is_available():
                continue
                
            attempts += 1
            result = provider.answer(prompt)
            
            log_entry = {
                "provider_id": result.provider_id,
                "model": result.model,
                "status": result.status,
                "latency_ms": result.latency_ms
            }

            if result.status == "success":
                route_log.append(log_entry)
                result_dict = result.to_dict()
                result_dict["route_log"] = route_log
                # Extract citations from chunks for the final response
                result_dict["citations"] = [c.get("lesson_id") for c in chunks if c.get("lesson_id")]
                return result_dict
            else:
                log_entry["error_type"] = result.error_type
                log_entry["error_message_redacted"] = result.error_message_redacted
                route_log.append(log_entry)
                
                # Handle error types
                if result.error_type == "auth":
                    provider.disable()
                elif result.error_type in ["rate_limit", "timeout", "network", "server_error"]:
                    provider.apply_cooldown(60) # 60 seconds cooldown

        # 6. All providers failed or exhausted attempts
        fallback_res = self.get_local_lexical_fallback(chunks)
        result_dict = fallback_res.to_dict()
        result_dict["route_log"] = route_log
        return result_dict
