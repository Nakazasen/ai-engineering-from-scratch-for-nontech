# AI Learning Companion v0.4.1-pre Release Notes

## 1. Release status

* **Phân loại**: Internal pre-release / milestone closure.
* **Kết quả đánh giá audit**: `RELEASE_READY_WITH_WARNINGS`.

## 2. What this release contains

Phiên bản pre-release v0.4.1 này bao gồm các tính năng và cải tiến đã qua kiểm duyệt sau:
* **Ứng dụng Static local-first**: Ứng dụng AI Learning Companion chạy hoàn toàn cục bộ trên client-side.
* **20 thẻ bài học Non-tech demo**: Cung cấp nội dung giải thích trực quan, dễ hiểu bằng tiếng Việt cho 20 bài học demo.
* **Lesson Player**: Trình phát bài học tích hợp hướng dẫn từng bước.
* **Lưu tiến độ học tập bằng localStorage**: Lưu tiến độ (`completed`, `review`) trực tiếp trên trình duyệt của người dùng thông qua key `aiLearningCompanion.progress.v1`.
* **Placement Test & 3 Learning Tracks**: Bộ câu hỏi kiểm tra điểm xuất phát giúp đề xuất 1 trong 3 lộ trình học cá nhân hóa (Track A, B, C).
* **Gia sư local (Lexical search)**: Tính năng tìm kiếm từ khóa cục bộ và trả lời theo mẫu kèm trích dẫn nguồn cụ thể.
* **Local Tutor Index**: Bộ chỉ mục tìm kiếm lexical gồm 629 chunks dữ liệu.
* **Local AI Tutor Proxy (Optional)**: Proxy backend viết bằng Python nhằm xử lý kết nối AI Provider an toàn mà không cần nhập hay lưu API key tại browser client.
* **Provider Router**: Cơ chế định tuyến thác nước (waterfall) tự động chuyển đổi giữa Gemini, OpenAI-compatible, Mock provider (nếu bật), và cuối cùng là Local lexical fallback.
* **Chế độ bảo mật (Privacy Modes)**: Hỗ trợ 3 mức cấu hình bảo mật dữ liệu học tập:
  * `local_only` (Chỉ tìm kiếm local, không gửi dữ liệu ra ngoài).
  * `public_curriculum_only` (Chỉ gửi câu hỏi và ngữ cảnh bài học công khai ra AI).
  * `learner_context_allowed` (Gửi câu hỏi kèm theo thông tin tiến trình học tập tóm tắt).
* **Bảng điều khiển Gia sư AI local**: Panel tương tác trực quan ngay bên trong trang chi tiết bài học.
* **Harden UI & Fallback**:
  * Lưu giữ thông báo lỗi HTTP 500 thân thiện thay vì bị overwrite bởi message ngoại tuyến chung.
  * Đường dẫn smoke test mặc định không yêu cầu API key thực tế.
  * Bổ sung định nghĩa các CSS class bổ trợ (`.privacy-warning`, `.ai-tutor-actions`, `.ai-tutor-route`, `.ai-tutor-fallback`).
  * Cải thiện nội dung cảnh báo bảo mật trong README và SMOKE_TEST.

## 3. What this release does NOT contain

* **Không chứa đầy đủ 485 thẻ bài học**: Nội dung non-tech đầy đủ hiện chỉ khả dụng cho 20 bài học demo. Các bài học còn lại chỉ hiển thị khung sườn.
* **Không đạt chuẩn Production-grade**: Đây là bản phát hành pre-release thử nghiệm cục bộ, chưa tối ưu hóa cho môi trường production thực tế.
* **Không hỗ trợ triển khai Cloud**: Kiến trúc hiện tại phục vụ chạy local-first.
* **Không hỗ trợ Gia sư AI hoàn chỉnh cho toàn bộ curriculum**: Chất lượng câu trả lời từ AI phụ thuộc vào lượng ngữ cảnh bài học thực tế có trong local index.
* **Không thực hiện smoke test với real provider**: Luồng test mặc định chỉ kiểm thử với chế độ local hoặc mock key.
* **Không chứa hệ thống xác thực/CSDL backend**: Tiến trình học tập lưu hoàn toàn tại local storage trình duyệt, không có database hay user auth.
* **Không sử dụng Vector DB / RAG chuyên sâu**: Hệ thống sử dụng lexical search cơ bản làm nền tảng ngữ cảnh.

## 4. Safety and privacy posture

* **Thiết kế Local-first**: Mọi dữ liệu cá nhân của người học được giữ an toàn trên máy cục bộ.
* **Chế độ local_only không cần API key**: Người học hoàn toàn có thể sử dụng tính năng cơ bản mà không cần khóa AI nào.
* **Không lưu khóa API trên trình duyệt**: Ứng dụng không cung cấp bất kỳ ô nhập API key hay lưu trữ key nào trong `localStorage`/`sessionStorage` của trình duyệt. API key (nếu có để phục vụ advanced test) chỉ được khai báo trong biến môi trường hoặc tệp local config được gitignore ở proxy backend.
* **Bảo vệ dữ liệu học tập**:
  * Frontend không bao giờ gửi raw `localStorage`.
  * Không gửi đối tượng progress hoặc JSON bài học đầy đủ.
  * Ở chế độ gửi tiến trình học tập tóm tắt (`learner_context_allowed`), danh sách bài học và điểm số quiz được cắt ngắn (tối đa 20 mục gần nhất) và tối giản hóa thuộc tính trước khi gửi.

## 5. Validation evidence

Kết quả audit từ Codex GPT-5.5 R1 Final Release:
* **Git baseline**: Nhánh local `main` sạch sẽ và hoàn toàn đồng bộ với remote `origin/main` tại HEAD = `8097e45`.
* **Cú pháp JS**: File `app.js` được xác nhận không có lỗi cú pháp (`node -c`).
* **Unit tests**: 18 unit tests Python liên quan tới router, prompt builder, retrieval và privacy module đều vượt qua thành công.
* **Card validation**: Công cụ `validate_nontech_cards.py` kiểm tra thành công schema của 20 cards demo.
* **Index build**: Bộ chỉ mục lexical local được build chính xác và lưu trữ tại `local_tutor_index.demo.json` (629 chunks).
* **Phases scope**: Không phát hiện bất kỳ thay đổi ngoài ý muốn nào trong thư mục `phases/`.
* **Secret scan**: Xác nhận không tồn tại API key thực sự nào bị lộ trong codebase hoặc tài liệu hướng dẫn.

## 6. Known warnings

* **Tài liệu README**: Một số cụm từ về trạng thái v0.1 vẫn còn tồn tại và chưa cập nhật đồng bộ lên v0.4.1-pre trong các tệp hướng dẫn chính.
* **Wording "No AI API"**: Đọc lướt README có thể gây nhầm lẫn do tiêu đề chưa cập nhật kỹ việc bổ sung optional proxy UI, mặc dù các phần dưới đã giải thích rõ.
* **Độc lập kiểm thử giao diện**: Quá trình audit cuối cùng dựa trên phân tích mã nguồn và báo cáo smoke test trước đó chứ không chạy lại UI tự động hóa độc lập.
* **Giới hạn Proxy**: Proxy backend là phiên bản MVP cục bộ, có thiết lập CORS mở rộng cho localhost/127.0.0.1 và không tích hợp bảo mật sản xuất.
* **Tham số customAlertHtml**: Nhận chuỗi HTML thô và chỉ được thiết kế để hiển thị các chuỗi thông báo tĩnh, an toàn được định nghĩa sẵn trong ứng dụng.
* **Dữ liệu giả lập**: Các chuỗi khóa `sk-...` hoặc `AIza...` xuất hiện trong tệp test chỉ là dữ liệu mock mẫu, không được sử dụng làm cấu hình thực tế.

## 7. How to smoke test

### Khởi chạy Static App
```powershell
cd ai-learning-companion
python -m http.server 8000
```
Tru cập: `http://127.0.0.1:8000`

### Khởi chạy Proxy Backend
```powershell
$env:PYTHONPATH="ai-learning-companion"
py -m ai_tutor_proxy.server
```

### Chạy các lệnh kiểm thử và kiểm tra
```powershell
node -c ai-learning-companion/app.js
py -m unittest discover ai-learning-companion/tests -v
py ai-learning-companion/tools/validate_nontech_cards.py
py ai-learning-companion/tools/build_local_tutor_index.py
git diff --name-only -- phases
```

## 8. Next recommended step

```text
Do not open C5 until release notes are committed and the milestone is clean.
Recommended next gate: documentation commit for release notes, then tag/mark internal milestone if desired.
```
