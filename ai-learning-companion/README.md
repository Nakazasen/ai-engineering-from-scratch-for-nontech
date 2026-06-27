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

### Cách học bằng card tiếng Việt

1. App hiện thị danh sách các bài học.
2. Tìm các bài học có nhãn **Bản non-tech**. Đây là các bài học đã được đơn giản hóa cho người mới (Gate B1 hiện có 8 bài).
3. Click vào bài học, đọc các phần giải thích: Ý tưởng chính, Ẩn dụ đời thường, Ví dụ tối giản.
4. Làm phần **Kiểm tra hiểu (Quiz)** ở cuối bài để tự đánh giá kiến thức.

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
*(Hiện tại script này dùng template được soạn sẵn để tạo nội dung cho 8 bài học demo. Không gọi AI API).*

**3. Kiểm tra tính hợp lệ của dữ liệu thẻ (Schema Validation):**
```powershell
python ai-learning-companion/tools/validate_nontech_cards.py
```

### Tại sao B1 mới chỉ có 8 demo lessons?

Mục tiêu của Gate B1 là xây dựng hoàn chỉnh luồng UI/Data (hiển thị, quiz, validation) cho các bài học Non-tech mà không làm rủi ro hay phá vỡ curriculum gốc (485 lessons). Việc làm 8 bài giúp chứng minh MVP hoạt động trơn tru trước khi mở rộng (scale) lên toàn bộ repo, tránh tình trạng dịch máy kém chất lượng hoặc hallucination hàng loạt.
