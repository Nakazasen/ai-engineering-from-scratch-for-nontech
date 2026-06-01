# AI Engineering Companion — 80/20 Non-Tech Edition

Phase A tạo một companion app tĩnh để người non-tech xem lộ trình học AI Engineering từ repo curriculum hiện có.

## Chạy scanner

Từ root repo:

```powershell
python ai-learning-companion/tools/scan_curriculum.py
```

Lệnh này đọc read-only từ `phases/**/docs/en.md` và tạo:

```text
ai-learning-companion/data/lessons.json
```

## Mở giao diện

```powershell
cd ai-learning-companion
python -m http.server 8000
```

Sau đó mở trình duyệt tại:

```text
http://localhost:8000
```

## Phase A làm gì?

- Quét danh sách bài học từ `phases/`.
- Trích xuất title, phase, lesson folder, metadata, headings và code files.
- Hiển thị dashboard tiếng Việt.
- Hiển thị lộ trình 12 tuần cho người non-tech.
- Cho phép tìm kiếm, lọc phase và click xem chi tiết lesson.

## Phase A chưa làm gì?

- Chưa gọi AI API.
- Chưa tạo nội dung giải thích 5 khối “Học kiểu non-tech”.
- Chưa thay đổi nội dung lesson gốc trong `phases/`.
- Chưa cần API key.

## Khi nào dùng Phase B?

Sau khi bạn review UI local, Phase B có thể thêm:

- Tạo giải thích “nói như người thường” cho từng lesson.
- Index nội dung sâu hơn từ code và glossary.
- RAG local hoặc AI API tùy lựa chọn.
