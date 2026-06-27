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
