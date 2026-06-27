# AI Tutor Proxy

This is a local Python proxy for the AI Learning Companion. It provides an AI-backed Tutor without exposing API keys to the browser, maintaining strict privacy controls.

## Features
- **Waterfall Routing:** Falls back automatically if a provider fails (e.g. Gemini -> OpenAI Compatible -> Local Lexical).
- **Privacy Gated:** Supports `local_only`, `public_curriculum_only` (default), and `learner_context_allowed`.
- **Secret Redaction:** Automatically scrubs API keys and tokens from logs and error messages.
- **Local Fallback:** Always falls back to local lexical search if no AI providers are available or if offline.

## Setup

1. Copy the example config:
   ```bash
   cp provider_config.example.json provider_config.local.json
   ```
   *Note: `*.local.json` is ignored by git.*
2. Add your API keys to `provider_config.local.json` or set them as environment variables (e.g. `ALC_GEMINI_API_KEY`).

## Running the Server

Start the proxy server (requires Python 3 stdlib only):
```bash
python -m ai_tutor_proxy.server
```
The server will start on port 8080.

## Manual Smoke Test (CURL)

You can test the server locally:
```bash
curl -X POST http://127.0.0.1:8080/api/tutor/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "AI là gì?", "privacy_mode": "public_curriculum_only"}'
```
