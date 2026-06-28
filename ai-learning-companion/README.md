# AI Engineering Companion — 80/20 Non-Tech Edition

App tĩnh để người non-tech học AI Engineering từ repo curriculum hiện có thông qua ngôn ngữ đơn giản, trực quan.

## Dành cho Người học (Learner)

Bạn không cần biết code để bắt đầu.

### Cách mở app local

Từ terminal, chạy:

```powershell
cd ai-learning-companion
python -m http.server 8000
```

Sau đó mở trình duyệt tại `http://localhost:8000`.

### Cách học

1. **Hỏi gia sư local:** Nhập câu hỏi tiếng Việt như “Tôi không hiểu RAG là gì” hoặc “API key nguy hiểm ở đâu”. Gia sư chỉ tìm trong dữ liệu local, không gọi AI API và luôn hiển thị nguồn.
2. **Làm kiểm tra điểm bắt đầu:** Bấm nút **"Kiểm tra điểm bắt đầu"** để làm bài đánh giá nhỏ. Hệ thống sẽ gợi ý 1 trong 3 lộ trình (track) phù hợp nhất với bạn:
   - **Track A (AI User Mạnh)**: Dành cho ứng dụng công việc trực tiếp (Prompting, RAG).
   - **Track B (AI Workflow Operator)**: Dành cho việc tự động hóa và kết nối API.
   - **Track C (AI Engineer Từ Nền Tảng)**: Đi sâu vào cốt lõi toán học và nguyên lý Machine Learning.
   *(Lưu ý: Nếu có nhiều track trùng điểm, hệ thống ưu tiên theo thứ tự Track A > Track B > Track C).*
3. **Học theo track:** Bấm **"Bắt đầu track của tôi"** hoặc **"Học tiếp theo track"** để học tuần tự các bài được thiết kế cho mục tiêu của bạn.
4. **Buổi học hôm nay:** Sử dụng bảng **"Buổi học hôm nay"** để xem bài học đề xuất tiếp theo, bài cần ôn (nếu có bài bị đánh giá ⚠️ Cần ôn, kèm thông tin chi tiết về điểm số lần làm gần nhất), và điền nhanh câu hỏi gợi ý cho Gia sư local. Toàn bộ tiến trình này hoạt động hoàn toàn offline cục bộ.
5. **Luồng học:** Đọc các phần được thiết kế riêng cho người non-tech (Mục tiêu, Vì sao cần hiểu, Ẩn dụ đời thường, Ví dụ tối giản...).
6. **Làm bài kiểm tra (Quiz):** Ở cuối bài, hãy nộp bài kiểm tra. Nếu đạt 3/3 điểm, bài học sẽ tự động được đánh dấu ✅ Đã hiểu. Nếu chưa đạt, hãy làm theo gợi ý ⚠️ Cần ôn lại (ứng dụng hiển thị chi tiết các câu sai, đáp án đúng, giải thích nguyên nhân và đề xuất câu hỏi cho Gia sư). Bạn có thể bấm nút **"Làm lại"** để đặt bài học về trạng thái đang học và xóa lịch sử kiểm tra của riêng bài đó.
7. **Xem tiến độ và Đánh giá chặng:** Bảng "Tiến độ học tập" trên cùng sẽ đếm số bài bạn đã học trong track hiện tại, kèm chỉ báo **Đánh giá chặng** hiển thị trạng thái chuẩn bị (Chưa sẵn sàng, Ôn lại trước, hoặc Sẵn sàng kiểm tra nhỏ khi hoàn thành >= 3 bài và không có bài cần ôn).
8. **Xoá tiến độ (nếu muốn):** Bạn có thể bấm "Xóa tiến độ" để làm mới toàn bộ kết quả học và kết quả kiểm tra điểm bắt đầu của mình. Mọi tiến độ được lưu hoàn toàn cục bộ trên trình duyệt (không gửi ra ngoài).

## Dành cho Maintainer

### Cách chạy công cụ

Từ root repo:

**1. Quét danh sách bài học gốc (cập nhật data/lessons.json):**
```powershell
python ai-learning-companion/tools/scan_curriculum.py
```

**2. Tạo thẻ Non-tech (cards.demo.json):**
```powershell
python ai-learning-companion/tools/generate_nontech_cards.py
```

**3. Kiểm tra tính hợp lệ của dữ liệu thẻ (Schema Validation):**
```powershell
python ai-learning-companion/tools/validate_nontech_cards.py
```

**4. Tạo chỉ mục Gia sư local (Local Tutor Index):**
```powershell
python ai-learning-companion/tools/build_local_tutor_index.py
```

### Kiến trúc lưu trữ (Gate B2, B3 & B4)

Gate B2/B3 sử dụng **`localStorage`** (key: `aiLearningCompanion.progress.v1`) để lưu tiến độ của người học tại client-side. KHÔNG cần backend, KHÔNG cần cơ sở dữ liệu. Dữ liệu sẽ mất nếu người dùng xóa dữ liệu trình duyệt hoặc nhấn "Xóa tiến độ".

Gate B4 thêm **Local Tutor** bằng lexical retrieval trên file `data/local_tutor_index.demo.json`. Đây không phải chatbot AI/LLM: app chỉ khớp từ khóa trong dữ liệu local và trả lời bằng template có nguồn trích dẫn. Nếu không đủ dữ liệu, app nói rõ: “Chưa đủ dữ liệu trong local index”.

Schema progress bao gồm:
- `learner_profile`: Lưu kết quả placement test, recommended_track.
- `last_opened_lesson_id`: ID bài học mở gần nhất.
- `lessons`: Lưu trạng thái `completed`, `review` và lịch sử làm quiz.

Các file cấu hình Data mới:
- `data/placement_questions.json`: Câu hỏi đánh giá và điểm map với các track.
- `data/learning_tracks.json`: 3 lộ trình học và danh sách lesson ID tương ứng.
- `data/local_tutor_index.demo.json`: Chỉ mục lexical local cho Gia sư local.

## MVP v0.1 current state

### What is real

- Static browser/local-server app.
- 20 reviewed non-tech demo lesson cards.
- Lesson player and quiz flow.
- Browser-local progress memory via `localStorage` key `aiLearningCompanion.progress.v1`.
- Vietnamese placement test and 3 learning tracks.
- Track-aware dashboard.
- Local Tutor using lexical/template search over local JSON with citations.
- Local tutor index with 629 chunks.
- Citation/source display for lesson cards and tutor answers.
- Learner progress stays in the browser and is not sent outside the local app.

### What is not implemented yet

- No AI chatbot.
- No AI API.
- No backend/database/auth.
- No vector DB.
- No real generative RAG.
- No full 485-lesson non-tech card coverage.
- Local Tutor is lexical/template search, so answer quality depends on keyword overlap.

### Known limitations

- Full non-tech explanations exist only for the 20 demo lessons.
- The curriculum index scans 485 lessons, but companion cards are not scaled to all lessons yet.
- Local Tutor can cite lesson metadata broadly, but rich plain-language explanations come from the 20 demo cards.
- Running `scan_curriculum.py` updates `data/lessons.json` `generated_at`; revert that file if only timestamp changes before unrelated commits.

### Optional Local AI Tutor Proxy (C3/C4 MVP)

An optional local Python proxy is available to enable AI provider integration without exposing API keys in the browser. 

The **Gia sư local** feature in the frontend app works entirely offline without this proxy. However, to use the in-lesson **Gia sư AI local**, you must start the proxy.

To start the proxy:
```powershell
$env:PYTHONPATH="ai-learning-companion"
python -m ai_tutor_proxy.server
```
The server will run on port 8080. 

Note: You do **not** need API keys to use the `local_only` privacy mode, and normal release smoke tests should be run without configuring real API keys.
If you want to use real AI providers for optional advanced testing:
1. Copy `ai_tutor_proxy/provider_config.example.json` to `ai_tutor_proxy/provider_config.local.json`.
2. Edit your keys in `provider_config.local.json`.
3. Never paste your API keys into the browser. API keys must only remain in local configuration or environment variables.
