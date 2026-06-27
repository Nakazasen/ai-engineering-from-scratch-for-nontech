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

1. **Bắt đầu học:** Trên giao diện, bấm nút **"Học bài đầu tiên"** tại bảng Tiến độ học tập.
2. **Luồng học:** Đọc các phần được thiết kế riêng cho người non-tech (Mục tiêu, Vì sao cần hiểu, Ẩn dụ đời thường, Ví dụ tối giản...).
3. **Làm bài kiểm tra (Quiz):** Ở cuối bài, hãy nộp bài kiểm tra. Nếu đạt 3/3 điểm, bài học sẽ tự động được đánh dấu ✅ Đã hiểu. Nếu chưa đạt, hãy làm theo gợi ý ⚠️ Cần ôn lại.
4. **Xem tiến độ:** Bảng "Tiến độ học tập" trên cùng sẽ tự động đếm số bài bạn đã học và cần ôn. 
5. **Xoá tiến độ (nếu muốn):** Bạn có thể bấm "Xóa tiến độ" để làm mới toàn bộ kết quả học của mình.

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

### Kiến trúc lưu trữ (Gate B2)

Gate B2 sử dụng **`localStorage`** (key: `aiLearningCompanion.progress.v1`) để lưu tiến độ của người học tại client-side. KHÔNG cần backend, KHÔNG cần cơ sở dữ liệu. Dữ liệu sẽ mất nếu người dùng xóa dữ liệu trình duyệt hoặc nhấn "Xóa tiến độ".

## Giới hạn hiện tại

- Mới có 8 demo lessons được làm nội dung non-tech.
- Chưa có bài kiểm tra xếp lớp (placement test).
- Chưa có RAG/tutor nội bộ hỗ trợ giải đáp.
- Hoàn toàn chưa tích hợp AI API (giữ an toàn, offline-first).
