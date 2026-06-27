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
4. **Luồng học:** Đọc các phần được thiết kế riêng cho người non-tech (Mục tiêu, Vì sao cần hiểu, Ẩn dụ đời thường, Ví dụ tối giản...).
5. **Làm bài kiểm tra (Quiz):** Ở cuối bài, hãy nộp bài kiểm tra. Nếu đạt 3/3 điểm, bài học sẽ tự động được đánh dấu ✅ Đã hiểu. Nếu chưa đạt, hãy làm theo gợi ý ⚠️ Cần ôn lại.
6. **Xem tiến độ:** Bảng "Tiến độ học tập" trên cùng sẽ đếm số bài bạn đã học trong track hiện tại.
7. **Xoá tiến độ (nếu muốn):** Bạn có thể bấm "Xóa tiến độ" để làm mới toàn bộ kết quả học và kết quả kiểm tra điểm bắt đầu của mình. Mọi tiến độ được lưu hoàn toàn cục bộ trên trình duyệt (không gửi ra ngoài).

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

## Giới hạn hiện tại

- Mới có 8 demo lessons được làm nội dung non-tech. Các learning track hiện cũng chỉ mapping vào 8 lesson này.
- Local Tutor là tìm kiếm lexical + template answer, chưa phải RAG/LLM thật.
- Hoàn toàn chưa tích hợp AI API (giữ an toàn, offline-first).
