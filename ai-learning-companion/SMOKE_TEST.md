# AI Learning Companion MVP v0.1 Smoke Test

Manual checklist only. Do not treat this as an automated test script.

## Setup

- [ ] From repo root, confirm no unexpected changes:
  ```powershell
  git status --short
  git diff --name-only -- phases
  ```
- [ ] Start a local static server:
  ```powershell
  cd ai-learning-companion
  python -m http.server 8000
  ```
- [ ] Open `http://localhost:8000` in a browser.

## B1 — non-tech cards

- [ ] Confirm the app renders the lesson list.
- [ ] Open a lesson with the `Bản non-tech` badge.
- [ ] Confirm the non-tech lesson card shows summary, why it matters, analogy,
      mental model, example, real-app use, misunderstandings, and citations.

## B2 — quiz and progress

- [ ] Submit a quiz answer set.
- [ ] Confirm quiz feedback appears.
- [ ] Confirm progress changes to `Đã hiểu` or `Cần ôn`.
- [ ] Refresh the page and confirm progress is retained by browser localStorage.

## B3 — placement and tracks

- [ ] Click `Kiểm tra điểm bắt đầu`.
- [ ] Complete all placement questions.
- [ ] Confirm one of the 3 tracks is recommended.
- [ ] Confirm the dashboard changes to track-aware progress and next lesson.

## B4 — Local Tutor

Run these tutor queries and confirm each confident answer includes a local source
or citation path:

- [ ] `rag`
- [ ] `prompt`
- [ ] `api key`
- [ ] `không biết code`
- [ ] `transformer`
- [ ] nonsense query such as `xyz vô nghĩa` returns a no-data fallback.

## Missing-index fallback

- [ ] Temporarily rename `data/local_tutor_index.demo.json` outside git.
- [ ] Refresh the app.
- [ ] Confirm the app does not crash and displays a missing local tutor index
      fallback while other sections still render.
- [ ] Restore `data/local_tutor_index.demo.json`.

## C3/C4 — Local AI Tutor Proxy (Optional)

- [ ] Copy `ai_tutor_proxy/provider_config.example.json` to `ai_tutor_proxy/provider_config.local.json`.
- [ ] Add dummy API keys to the local config (e.g. `mock_key` or `dummy_value`) to verify the mock provider configuration.
- [ ] Do **NOT** use or configure real API keys for normal release smoke testing. Testing real provider calls is an optional advanced manual test only.
- [ ] Start the proxy: `python -m ai_tutor_proxy.server`
- [ ] Test via cURL that the proxy falls back safely when keys are missing or invalid:
  ```bash
  curl -X POST http://127.0.0.1:8080/api/tutor/ask -H "Content-Type: application/json" -d '{"question": "AI là gì?", "privacy_mode": "public_curriculum_only"}'
  ```
- [ ] Verify the response includes citations, does not leak API keys, and has the correct `privacy_mode`.

## C4 — Local AI Tutor Proxy UI

Required checks:
- [ ] Static app opens at http://127.0.0.1:8000
- [ ] Existing Gia sư local still works with proxy stopped
- [ ] Lesson detail shows Gia sư AI local panel
- [ ] Default privacy mode is local_only
- [ ] No API key input exists in browser
- [ ] Browser localStorage/sessionStorage does not contain API key/provider config
- [ ] Proxy stopped: AI Tutor panel shows fallback message and local lexical answer
- [ ] Proxy running: local_only returns local_lexical
- [ ] public_curriculum_only without keys does not crash
- [ ] learner_context_allowed sends summary only
- [ ] raw localStorage is not sent
- [ ] full state.progress is not sent
- [ ] full lesson/card JSON is not sent
- [ ] no phases diff
- [ ] tests pass
## C5 — Buổi học hôm nay

- [ ] Static app opens.
- [ ] Daily plan panel ("Buổi học hôm nay") is visible.
- [ ] Before placement test (or after progress reset): panel recommends a safe beginner lesson (e.g. "Cài đặt môi trường học").
- [ ] After placement test: panel recommends the next uncompleted lesson from the recommended track.
- [ ] Recommended next lesson button opens the correct lesson.
- [ ] If you complete a quiz and fail (getting "review" status), that lesson appears under the "Ôn lại" card.
- [ ] The "Ôn bài cần xem lại" button opens the correct lesson to review.
- [ ] The tutor suggestion card displays a question based on the recommended lesson.
- [ ] Clicking "Điền câu hỏi" fills the question in the global "Gia sư local" textarea and scrolls down to it without auto-submitting.
- [ ] Existing Gia sư local search still works.
- [ ] Existing Gia sư AI local panel still works/falls back safely.
- [ ] No API keys are used or leaked.

## Final scope check

- [ ] Stop the local server.
- [ ] Confirm no generated churn is staged or left dirty:
  ```powershell
  git status --short
  git diff --name-only -- phases
  ```
- [ ] If `data/lessons.json` changed only by `generated_at`, revert it before
      any unrelated commit:
  ```powershell
  git checkout -- ai-learning-companion/data/lessons.json
  ```
