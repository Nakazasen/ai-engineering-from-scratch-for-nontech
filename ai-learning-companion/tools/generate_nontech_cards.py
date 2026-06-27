"""Generate deterministic non-tech cards for MVP Gate B1.

Run from repository root:
    python ai-learning-companion/tools/generate_nontech_cards.py
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

def get_repo_root():
    return Path(__file__).resolve().parents[2]

def get_demo_cards_content():
    return {
        "00-setup-and-tooling/01-dev-environment": {
            "title_vi": "Cài đặt môi trường học",
            "plain_language_summary_vi": "Thiết lập các công cụ cơ bản trên máy tính của bạn để sẵn sàng viết và chạy code AI.",
            "why_it_matters_vi": "Giống như xây nhà cần có móng, học AI cần một máy tính được cài đặt đúng các phần mềm (Python, VS Code, Git) để mọi thứ chạy mượt mà.",
            "daily_life_analogy_vi": "Tưởng tượng bạn chuẩn bị nấu một món ăn phức tạp. Việc cài môi trường giống như mua đủ nồi niêu xoong chảo và sắp xếp gọn gàng vào bếp trước khi bắt đầu thái rau thái thịt.",
            "mental_model_vi": "Môi trường dev = Hệ điều hành + Ngôn ngữ lập trình (Python) + Công cụ quản lý gói (pip) + Trình soạn thảo (VS Code).",
            "minimal_example_vi": "Cài đặt Python và chạy dòng lệnh `print('Hello AI')` đầu tiên.",
            "real_app_use_vi": "Bất kỳ dự án AI nào cũng bắt đầu bằng việc cài đặt môi trường để đảm bảo code chạy được trên máy của tất cả mọi người trong team.",
            "common_misunderstandings_vi": [
                "Cài xong phần mềm là AI tự chạy (Thực ra bạn vẫn phải viết code).",
                "Chỉ cần cài một lần là xong mãi mãi (Các thư viện AI cập nhật rất nhanh, bạn sẽ thường xuyên phải cập nhật môi trường)."
            ],
            "check_questions": [
                {
                    "question": "Vì sao cần cài đặt môi trường lập trình trước khi học AI?",
                    "options": [
                        "Để máy tính tự động viết code AI",
                        "Để có sẵn các công cụ (Python, editor) giúp viết và chạy code dễ dàng",
                        "Để tải game về máy",
                        "Để tăng tốc độ wifi"
                    ],
                    "correct": 1,
                    "explanation": "Môi trường lập trình cung cấp các công cụ cần thiết (như trình biên dịch, thư viện) để bạn có thể ra lệnh cho máy tính thông qua code."
                },
                {
                    "question": "Thành phần nào KHÔNG thường có trong môi trường phát triển cơ bản?",
                    "options": [
                        "Ngôn ngữ lập trình (VD: Python)",
                        "Trình soạn thảo code (VD: VS Code)",
                        "Phần mềm chỉnh sửa video",
                        "Công cụ quản lý phiên bản (VD: Git)"
                    ],
                    "correct": 2,
                    "explanation": "Phần mềm chỉnh sửa video không cần thiết cho việc lập trình AI cơ bản."
                },
                {
                    "question": "Ví dụ nào so sánh đúng nhất về việc thiết lập môi trường?",
                    "options": [
                        "Trang bị đồ nghề và bàn làm việc trước khi sửa xe",
                        "Chạy xe ra ngoài đường",
                        "Đi mua xe mới",
                        "Sửa bánh xe bị thủng"
                    ],
                    "correct": 0,
                    "explanation": "Thiết lập môi trường là bước chuẩn bị công cụ và không gian làm việc (đồ nghề, bàn) trước khi thực sự làm việc (sửa xe/viết code)."
                }
            ],
            "source_citations": [
                {"heading": "Tooling", "quote": "The foundation of all your AI engineering."}
            ]
        },
        "00-setup-and-tooling/04-apis-and-keys": {
            "title_vi": "API và Key kết nối",
            "plain_language_summary_vi": "Cách ứng dụng của bạn nói chuyện với các mô hình AI lớn thông qua API và bảo mật 'chìa khóa' của bạn.",
            "why_it_matters_vi": "Các mô hình mạnh nhất như GPT-4 hay Claude thường chạy trên máy chủ của OpenAI/Anthropic. Bạn cần API key để chứng minh mình là ai khi yêu cầu họ xử lý dữ liệu.",
            "daily_life_analogy_vi": "API key giống như thẻ thành viên phòng gym. Mỗi lần bạn muốn vào tập (gọi API), bạn phải quẹt thẻ (gửi key). Nếu để rơi thẻ, người khác có thể nhặt được và vào tập miễn phí (bạn phải trả tiền).",
            "mental_model_vi": "API = Cửa sổ giao tiếp. API Key = Mật khẩu đi kèm mỗi yêu cầu.",
            "minimal_example_vi": "Sử dụng file `.env` để lưu trữ `OPENAI_API_KEY` một cách an toàn mà không bị tải lên mạng.",
            "real_app_use_vi": "Mọi ứng dụng chat AI, phân tích văn bản hay tạo ảnh đều gọi API và cần quản lý key an toàn.",
            "common_misunderstandings_vi": [
                "API key là miễn phí (Đa số đều tính phí theo lượt dùng).",
                "Có thể dán trực tiếp API key vào code để chạy cho tiện (Tuyệt đối không, vì nếu đưa code lên mạng, người khác sẽ lấy cắp key của bạn)."
            ],
            "check_questions": [
                {
                    "question": "API Key trong AI có vai trò gì?",
                    "options": [
                        "Làm cho model AI thông minh hơn",
                        "Như một mật khẩu để xác thực và thanh toán khi bạn gọi các dịch vụ AI",
                        "Để mã hóa dữ liệu của bạn",
                        "Là một loại tiền điện tử"
                    ],
                    "correct": 1,
                    "explanation": "API Key dùng để nhận diện tài khoản của bạn, cho phép dịch vụ (như OpenAI) biết ai đang sử dụng và tính phí hợp lý."
                },
                {
                    "question": "Lỗi bảo mật nghiêm trọng nhất khi dùng API Key là gì?",
                    "options": [
                        "Quên không lưu lại key",
                        "Tạo quá nhiều key",
                        "Viết thẳng key vào file code và tải lên mạng công khai (VD: GitHub)",
                        "Chia sẻ key cho đồng nghiệp qua tin nhắn an toàn"
                    ],
                    "correct": 2,
                    "explanation": "Đưa API key lên mạng công khai (hardcode) khiến ai cũng có thể dùng key của bạn, dẫn đến việc bạn phải trả số tiền khổng lồ."
                },
                {
                    "question": "Cách an toàn nhất để lưu API key trong dự án là?",
                    "options": [
                        "Dùng file biến môi trường (.env) và không đưa file này lên mạng",
                        "Lưu trong file .txt bình thường",
                        "Viết thẳng vào file main.py",
                        "Ghi ra giấy nhớ"
                    ],
                    "correct": 0,
                    "explanation": "File .env được thiết kế để giữ các biến môi trường (như API key) ở máy tính cục bộ và thường được cấu hình để Git bỏ qua (không đưa lên mạng)."
                }
            ],
            "source_citations": [
                {"heading": "Safety first", "quote": "Never commit your API keys."}
            ]
        },
        "01-math-foundations/01-linear-algebra-intuition": {
            "title_vi": "Trực giác Đại số Tuyến tính",
            "plain_language_summary_vi": "Hiểu cách máy tính biến mọi thứ (chữ, ảnh, âm thanh) thành các danh sách số (vector) để tính toán.",
            "why_it_matters_vi": "Máy tính không hiểu chữ hay hình ảnh, chúng chỉ giỏi cộng trừ nhân chia. Đại số tuyến tính cung cấp cách dịch thế giới thực sang ngôn ngữ toán học mà AI có thể xử lý cực nhanh.",
            "daily_life_analogy_vi": "Giống như việc đánh giá một chiếc điện thoại qua các điểm số: [Thiết kế: 8, Pin: 9, Camera: 7]. Một danh sách điểm số như vậy chính là một 'vector' mô tả điện thoại đó.",
            "mental_model_vi": "Vector = Một danh sách các con số. Ma trận = Một bảng gồm nhiều vector. Tính toán AI = Xoay, nhân, và cộng các bảng số này.",
            "minimal_example_vi": "Từ 'vua' được biểu diễn bằng vector `[0.9, 0.1, 0.5]`, 'hoàng hậu' là `[0.9, 0.8, 0.5]`. Máy có thể tính toán sự tương đồng giữa chúng.",
            "real_app_use_vi": "Mọi công cụ tìm kiếm, hệ thống gợi ý phim (Netflix), và các mô hình ngôn ngữ (GPT) đều chạy bằng phép nhân ma trận khổng lồ ở bên dưới.",
            "common_misunderstandings_vi": [
                "Phải siêu giỏi toán mới làm được AI (Bạn chỉ cần hiểu khái niệm, máy tính sẽ tính hộ bạn).",
                "Vector chỉ là mũi tên trong hình học (Trong AI, nó chủ yếu là danh sách các con số)."
            ],
            "check_questions": [
                {
                    "question": "Trong bối cảnh AI, 'Vector' thường được hiểu đơn giản là gì?",
                    "options": [
                        "Một mũi tên chỉ hướng",
                        "Một danh sách các con số dùng để đại diện cho một đối tượng (từ, ảnh...)",
                        "Một thuật toán học máy",
                        "Một loại dữ liệu chỉ có Đúng/Sai"
                    ],
                    "correct": 1,
                    "explanation": "Mặc dù trong hình học vector là mũi tên, trong AI/lập trình, vector thực chất là một danh sách (mảng) các con số, ví dụ [0.2, -1.5, 3.4]."
                },
                {
                    "question": "Tại sao AI cần biến văn bản hoặc hình ảnh thành số?",
                    "options": [
                        "Vì máy tính chỉ tính toán được với các con số",
                        "Để tiết kiệm dung lượng lưu trữ",
                        "Để bảo mật thông tin",
                        "Để người dùng không đọc được"
                    ],
                    "correct": 0,
                    "explanation": "Bản chất của các mô hình học máy là các phương trình toán học khổng lồ, chúng chỉ hoạt động bằng cách thực hiện các phép tính trên số liệu."
                },
                {
                    "question": "Nếu vector của 'Chó' là [1, 0] và 'Mèo' là [0.9, 0.1], điều này ngụ ý gì?",
                    "options": [
                        "Chó lớn hơn Mèo",
                        "Chó và Mèo có chung nhiều đặc điểm (vector gần nhau trong không gian)",
                        "Chó ăn thịt Mèo",
                        "Đây là dữ liệu lỗi"
                    ],
                    "correct": 1,
                    "explanation": "Trong không gian vector, các vật thể có ý nghĩa tương đồng thường được gán các danh sách số gần giống nhau để máy tính dễ so sánh."
                }
            ],
            "source_citations": [
                {"heading": "Intuition", "quote": "A vector is just a list of numbers."}
            ]
        },
        "02-ml-fundamentals/01-what-is-machine-learning": {
            "title_vi": "Machine Learning là gì?",
            "plain_language_summary_vi": "Thay vì lập trình các quy tắc (ví dụ: NẾU có từ 'xổ số' THÌ là thư rác), ta cho máy xem ví dụ để nó tự tìm ra quy tắc.",
            "why_it_matters_vi": "Nhiều vấn đề (như nhận diện khuôn mặt hay dịch ngôn ngữ) quá phức tạp để con người viết hết tất cả các quy tắc IF/ELSE. ML giải quyết điều này bằng cách học từ dữ liệu.",
            "daily_life_analogy_vi": "Cách bạn dạy một đứa trẻ phân biệt chó và mèo. Bạn không đưa cho trẻ một danh sách các đặc điểm sinh học, bạn chỉ cần chỉ vào nhiều con chó và nói 'Đây là chó', chỉ vào mèo và nói 'Đây là mèo'. Trẻ sẽ tự rút ra quy luật nhận biết.",
            "mental_model_vi": "Lập trình truyền thống: Dữ liệu + Quy tắc = Kết quả. Machine Learning: Dữ liệu + Kết quả = Quy tắc (Model).",
            "minimal_example_vi": "Cung cấp cho máy hàng ngàn email đã được gắn nhãn 'Spam' hoặc 'Bình thường'. Máy tạo ra một 'Model' (quy tắc) để tự nhận diện email mới.",
            "real_app_use_vi": "Lọc thư rác, gợi ý sản phẩm trên Shopee/Tiki, dự đoán thời tiết, xe tự lái.",
            "common_misunderstandings_vi": [
                "Machine Learning tự nghĩ ra kiến thức mới (Nó chỉ tìm các pattern/quy luật có sẵn trong dữ liệu mà bạn cung cấp).",
                "Model ML luôn luôn đúng 100% (Chúng hoạt động dựa trên xác suất và có thể sai số)."
            ],
            "check_questions": [
                {
                    "question": "Sự khác biệt cốt lõi giữa Lập trình truyền thống và Machine Learning là gì?",
                    "options": [
                        "Lập trình truyền thống dùng Python, ML dùng C++",
                        "Lập trình truyền thống tạo ra quy tắc từ người dùng, ML tự học quy tắc từ dữ liệu",
                        "ML luôn chạy nhanh hơn Lập trình truyền thống",
                        "ML không cần dữ liệu đầu vào"
                    ],
                    "correct": 1,
                    "explanation": "Trong ML, thay vì bạn viết luật IF/ELSE, bạn cung cấp dữ liệu và kết quả mong muốn, máy sẽ tự tìm ra luật."
                },
                {
                    "question": "Thuật ngữ 'Model' (Mô hình) trong Machine Learning có nghĩa là?",
                    "options": [
                        "Một chương trình 3D",
                        "Tập hợp các quy tắc/mẫu (patterns) mà máy tính đã học được từ dữ liệu",
                        "Một loại cơ sở dữ liệu",
                        "Máy chủ chạy ứng dụng"
                    ],
                    "correct": 1,
                    "explanation": "Model là 'não bộ' chứa những gì máy đã học, dùng để đưa ra dự đoán cho dữ liệu mới."
                },
                {
                    "question": "Yếu tố nào quan trọng nhất để một hệ thống Machine Learning hoạt động tốt?",
                    "options": [
                        "Máy tính phải cực đắt tiền",
                        "Giao diện đẹp mắt",
                        "Dữ liệu đầu vào đủ nhiều và chất lượng cao",
                        "Mạng internet tốc độ cao"
                    ],
                    "correct": 2,
                    "explanation": "Dữ liệu là nhiên liệu của ML. Dữ liệu rác sẽ sinh ra mô hình rác (Garbage In, Garbage Out)."
                }
            ],
            "source_citations": [
                {"heading": "The Paradigm Shift", "quote": "Data + Output -> Rules"}
            ]
        },
        "05-nlp-foundations-to-advanced/01-text-processing": {
            "title_vi": "Xử lý văn bản (Text Processing)",
            "plain_language_summary_vi": "Cách băm nhỏ và chuẩn hóa văn bản con người thành các mẩu nhỏ (tokens) để máy tính dễ dàng xử lý.",
            "why_it_matters_vi": "Máy không đọc văn bản như người. Nếu bạn đưa câu 'Tôi thích AI!' cho máy, nó không biết phân chia từ ngữ hay xử lý dấu chấm than thế nào. Xử lý văn bản giúp làm sạch và cấu trúc hóa ngôn ngữ.",
            "daily_life_analogy_vi": "Giống như việc nhặt rau trước khi nấu ăn. Bạn phải nhặt bỏ rễ, rửa sạch, cắt thành từng khúc vừa ăn. Xử lý văn bản (cắt từ, bỏ dấu câu thừa, chuyển chữ thường) chính là bước 'sơ chế' dữ liệu.",
            "mental_model_vi": "Văn bản thô -> Làm sạch (Xóa ký tự lạ, chuyển chữ thường) -> Tokenization (Cắt thành các từ/âm tiết nhỏ).",
            "minimal_example_vi": "Câu 'Hello, World!!!' -> Làm sạch: 'hello world' -> Cắt từ (Tokenize): ['hello', 'world'].",
            "real_app_use_vi": "Mọi chatbot, công cụ tìm kiếm Google, hay hệ thống dịch tự động đều phải có bước xử lý văn bản ở ngoài cùng.",
            "common_misunderstandings_vi": [
                "1 Token luôn luôn là 1 từ (Đôi khi token có thể là 1 ký tự, hoặc 1 cụm từ, tùy cách chia).",
                "Chữ hoa chữ thường không quan trọng (Với nhiều hệ thống cũ, 'Apple' (công ty) và 'apple' (quả táo) bị gộp làm một nếu không xử lý cẩn thận)."
            ],
            "check_questions": [
                {
                    "question": "Mục đích chính của bước Xử lý văn bản là gì?",
                    "options": [
                        "Dịch văn bản sang ngôn ngữ khác",
                        "Làm sạch và chia nhỏ văn bản thành định dạng máy tính dễ học hơn",
                        "Tạo ra các câu trả lời tự động",
                        "Sửa lỗi chính tả cho người dùng"
                    ],
                    "correct": 1,
                    "explanation": "Nó là quá trình 'sơ chế' dữ liệu thô thành các khối gọn gàng, đồng nhất (tokens) để model đọc được."
                },
                {
                    "question": "Tokenization là quá trình gì?",
                    "options": [
                        "Bảo mật dữ liệu bằng mã thông báo",
                        "Cắt một câu dài thành các mẩu nhỏ (tokens) như từ hoặc chữ cái",
                        "Tính toán xác suất của các từ",
                        "Lưu trữ văn bản vào cơ sở dữ liệu"
                    ],
                    "correct": 1,
                    "explanation": "Tokenization (mã hóa chuỗi) là thao tác băm nhỏ văn bản, giúp máy có một 'từ điển' giới hạn để ánh xạ sang số."
                },
                {
                    "question": "Việc chuyển đổi tất cả văn bản thành chữ thường (lowercase) có lợi ích gì trong các mô hình đơn giản?",
                    "options": [
                        "Làm văn bản đẹp hơn",
                        "Máy tính chạy nhanh hơn",
                        "Giảm kích thước từ điển vì 'Word' và 'word' được coi là giống nhau",
                        "Giúp dịch thuật chính xác hơn"
                    ],
                    "correct": 2,
                    "explanation": "Nó giúp giảm độ phức tạp của dữ liệu, tiết kiệm bộ nhớ cho từ điển (vocabulary)."
                }
            ],
            "source_citations": [
                {"heading": "Text pre-processing", "quote": "Tokenization is breaking text into units."}
            ]
        },
        "07-transformers-deep-dive/01-why-transformers": {
            "title_vi": "Vì sao lại là Transformers?",
            "plain_language_summary_vi": "Kiến trúc mang tính cách mạng giúp AI có thể chú ý đến mối quan hệ giữa các từ trong câu dù chúng cách xa nhau, mở ra kỷ nguyên của LLMs.",
            "why_it_matters_vi": "Trước Transformer, AI đọc từng từ một theo thứ tự, rất chậm và hay quên các từ ở đầu câu dài. Transformer cho phép đọc song song mọi từ cùng lúc và tự 'đánh giá' mức độ liên quan giữa chúng.",
            "daily_life_analogy_vi": "Các AI cũ giống như người đọc sách bằng cách soi kính lúp từng chữ một từ trái qua phải. Transformer giống như người có thể nhìn lướt cả một trang sách cùng lúc, và ngay lập tức biết những chữ nào có liên hệ mật thiết với nhau.",
            "mental_model_vi": "Transformer = Attention (Chú ý). Nó hỏi: 'Khi tôi xử lý từ này, tôi nên tập trung bao nhiêu % vào các từ khác trong câu?'",
            "minimal_example_vi": "Trong câu 'Ngân hàng đang bờ sông', từ 'ngân hàng' sẽ liên kết mạnh với từ 'bờ sông' để máy tính hiểu đây là bãi đất ven sông chứ không phải nơi gửi tiền.",
            "real_app_use_vi": "Kiến trúc lõi của ChatGPT (GPT có chữ T là Transformer), Google Translate hiện đại, và hầu hết mọi AI xử lý ngôn ngữ hiện nay.",
            "common_misunderstandings_vi": [
                "Transformer là tên của một model cụ thể (Thực ra nó là một *kiến trúc* dùng để xây dựng hàng ngàn model khác nhau).",
                "Transformer hiểu ngôn ngữ như con người (Nó chỉ tính toán xác suất liên quan giữa các token rất giỏi)."
            ],
            "check_questions": [
                {
                    "question": "Hạn chế lớn nhất của các mô hình trước Transformer (như RNN) là gì?",
                    "options": [
                        "Không thể xử lý hình ảnh",
                        "Quá đắt đỏ để chạy",
                        "Đọc dữ liệu tuần tự từng từ nên chậm và hay 'quên' ngữ cảnh ở đầu câu dài",
                        "Chỉ hiểu được tiếng Anh"
                    ],
                    "correct": 2,
                    "explanation": "RNN (Recurrent Neural Networks) xử lý chuỗi tuần tự, gây ra hiện tượng nghẽn cổ chai và giảm trí nhớ với văn bản dài."
                },
                {
                    "question": "Cơ chế 'Tự chú ý' (Self-Attention) trong Transformer làm nhiệm vụ gì?",
                    "options": [
                        "Giúp máy tính không bị mất kết nối mạng",
                        "Đánh giá xem một từ trong câu có liên quan (chú ý) tới các từ khác ở mức độ nào",
                        "Tự động gửi email cảnh báo",
                        "Sửa lỗi chính tả người dùng"
                    ],
                    "correct": 1,
                    "explanation": "Self-attention giúp model hiểu được ngữ cảnh động của từ. VD: từ 'đường' trong 'hạt đường' khác 'con đường' nhờ nhìn vào các từ xung quanh."
                },
                {
                    "question": "Vì sao Transformer train (huấn luyện) nhanh hơn các mô hình ngôn ngữ cũ?",
                    "options": [
                        "Vì nó bỏ qua các bước kiểm tra lỗi",
                        "Vì mã nguồn của nó ngắn hơn",
                        "Vì nó có thể xử lý tất cả các từ trong một câu cùng một lúc (tính toán song song)",
                        "Vì nó dùng dữ liệu ít hơn"
                    ],
                    "correct": 2,
                    "explanation": "Nhờ loại bỏ sự phụ thuộc tuần tự, Transformer có thể tận dụng tối đa sức mạnh tính toán song song của các card đồ họa (GPU)."
                }
            ],
            "source_citations": [
                {"heading": "The Attention Bottleneck", "quote": "Attention is all you need."}
            ]
        },
        "11-llm-engineering/01-prompt-engineering": {
            "title_vi": "Kỹ sư Prompt (Prompt Engineering)",
            "plain_language_summary_vi": "Nghệ thuật và khoa học trong việc viết hướng dẫn rõ ràng để ép mô hình AI sinh ra kết quả chính xác, đúng định dạng bạn cần.",
            "why_it_matters_vi": "AI rất thông minh nhưng cũng rất dễ đoán mò hoặc trả lời lan man. Một câu prompt tốt là ranh giới giữa một công cụ vô dụng và một trợ lý đắc lực.",
            "daily_life_analogy_vi": "Giống như giao việc cho một thực tập sinh xuất sắc nhưng chưa có kinh nghiệm. Nếu bạn bảo 'Viết cho tôi cái email', họ sẽ bối rối. Nếu bạn bảo 'Viết email cho sếp, độ dài 3 câu, tông giọng lịch sự, báo cáo tiến độ dự án X', kết quả sẽ hoàn hảo ngay.",
            "mental_model_vi": "Prompt = Vai trò + Ngữ cảnh + Nhiệm vụ + Định dạng đầu ra mong muốn.",
            "minimal_example_vi": "Thay vì 'Dịch câu này', hãy dùng 'Bạn là một dịch giả chuyên nghiệp. Hãy dịch câu sau sang tiếng Việt. Trả về đúng kết quả dịch, không thêm lời chào: [văn bản].'",
            "real_app_use_vi": "Trong các ứng dụng thực tế (System Prompt), prompt bị giấu phía sau để định hình tính cách và cách xử lý của ứng dụng mà người dùng không nhìn thấy.",
            "common_misunderstandings_vi": [
                "Prompt là các câu 'thần chú' bí mật (Thực ra prompt tốt chỉ là giao tiếp rõ ràng và rành mạch).",
                "Cần một prompt siêu dài cho mọi thứ (Đôi khi cung cấp ví dụ mẫu (few-shot) tốt hơn là giải thích dài dòng)."
            ],
            "check_questions": [
                {
                    "question": "Đâu là một câu lệnh (prompt) tốt nhất cho AI?",
                    "options": [
                        "Tóm tắt bài này đi",
                        "Hãy đọc bài viết sau, tóm tắt lại thành 3 gạch đầu dòng, ngôn ngữ dễ hiểu cho học sinh cấp 2.",
                        "Làm thế nào để tóm tắt một bài viết?",
                        "Tóm tắt"
                    ],
                    "correct": 1,
                    "explanation": "Prompt tốt cung cấp đủ: hành động (tóm tắt), định dạng (3 gạch đầu dòng), và đối tượng/tông giọng (học sinh cấp 2)."
                },
                {
                    "question": "Kỹ thuật 'Few-shot prompting' là gì?",
                    "options": [
                        "Bảo AI trả lời thật ngắn",
                        "Dùng ít từ nhất có thể trong prompt",
                        "Đưa ra một vài ví dụ Mẫu trong prompt để AI bắt chước theo quy luật",
                        "Bắn một vài phát súng"
                    ],
                    "correct": 2,
                    "explanation": "Việc cung cấp 1-3 ví dụ (Input -> Output) giúp AI hiểu chính xác định dạng và logic bạn muốn mà không cần giải thích bằng lời quá dài."
                },
                {
                    "question": "Lỗi 'Hallucination' (Ảo giác) của LLM thường xuất hiện khi nào?",
                    "options": [
                        "Khi máy tính bị quá nhiệt",
                        "Khi Prompt quá chung chung hoặc yêu cầu thông tin AI không biết",
                        "Khi dùng sai ngôn ngữ",
                        "Khi AI không có kết nối internet"
                    ],
                    "correct": 1,
                    "explanation": "Khi thiếu ngữ cảnh rõ ràng, AI sẽ có xu hướng đoán mò và bịa ra câu trả lời có vẻ hợp lý nhưng sai sự thật."
                }
            ],
            "source_citations": [
                {"heading": "Prompt Fundamentals", "quote": "Clear instructions are better than clever ones."}
            ]
        },
        "11-llm-engineering/06-rag": {
            "title_vi": "RAG (Tạo văn bản dựa trên tìm kiếm)",
            "plain_language_summary_vi": "Kết hợp khả năng tìm kiếm tài liệu nội bộ với khả năng đọc hiểu của AI để trả lời câu hỏi bằng thông tin chính xác, cập nhật.",
            "why_it_matters_vi": "ChatGPT không biết quy chế công ty bạn hay số liệu hôm qua. Để AI trả lời đúng về dữ liệu đóng/cập nhật, ta phải tìm tài liệu đưa cho AI đọc trước khi nó trả lời.",
            "daily_life_analogy_vi": "Thay vì bắt sinh viên (AI) vào phòng thi và phải nhớ mọi thứ trong đầu (Dễ bịa bậy), RAG cho phép sinh viên mang theo sách giáo khoa (Tài liệu nội bộ). Khi có câu hỏi, sinh viên lật đúng trang sách, đọc và tóm tắt lại câu trả lời.",
            "mental_model_vi": "RAG = Retriever (Tìm kiếm văn bản liên quan) + Generator (LLM đọc văn bản đó để tóm tắt trả lời).",
            "minimal_example_vi": "User hỏi: 'Quy trình xin nghỉ phép?'. Hệ thống tìm file `hr_policy.pdf`, lấy đoạn 'Nghỉ phép báo trước 3 ngày'. Đưa đoạn đó + câu hỏi cho LLM. LLM trả lời: 'Theo chính sách, bạn cần báo trước 3 ngày'.",
            "real_app_use_vi": "Chatbot tư vấn luật, bot tra cứu tài liệu nội bộ doanh nghiệp, hệ thống chăm sóc khách hàng dựa trên FAQ.",
            "common_misunderstandings_vi": [
                "Phải 'huấn luyện lại' (fine-tune) model bằng dữ liệu nội bộ (Không cần, RAG chỉ 'nhét' tài liệu vào prompt ở thời gian thực, rẻ và dễ hơn nhiều).",
                "RAG không bao giờ nói dối (Nó vẫn có thể bịa nếu tài liệu tìm được không liên quan hoặc prompt bảo nó được đoán)."
            ],
            "check_questions": [
                {
                    "question": "Chữ RAG viết tắt của thuật ngữ nào?",
                    "options": [
                        "Random Access Generation",
                        "Retrieval-Augmented Generation",
                        "Real AI Graph",
                        "Robotic Auto Generator"
                    ],
                    "correct": 1,
                    "explanation": "Retrieval (Tìm kiếm) - Augmented (Tăng cường) - Generation (Tạo sinh). Sinh văn bản được tăng cường bởi dữ liệu tìm kiếm."
                },
                {
                    "question": "Khi nào thì một doanh nghiệp nên dùng RAG thay vì dùng ChatGPT thông thường?",
                    "options": [
                        "Khi muốn dịch văn bản",
                        "Khi cần AI trả lời các câu hỏi dựa trên dữ liệu nội bộ, bảo mật và cập nhật liên tục của công ty",
                        "Khi muốn vẽ tranh",
                        "Khi muốn AI giải toán"
                    ],
                    "correct": 1,
                    "explanation": "RAG giải quyết điểm yếu lớn nhất của LLM là không có thông tin cá nhân/nội bộ hoặc thông tin mới nhất sau ngày huấn luyện."
                },
                {
                    "question": "Thành phần 'Retriever' trong hệ thống RAG làm nhiệm vụ gì?",
                    "options": [
                        "Sinh ra câu trả lời cuối cùng",
                        "Sửa lỗi chính tả",
                        "Tìm kiếm và trích xuất các đoạn tài liệu có liên quan nhất tới câu hỏi của người dùng",
                        "Kiểm tra xem người dùng có đăng nhập chưa"
                    ],
                    "correct": 2,
                    "explanation": "Giống như thủ thư, Retriever có nhiệm vụ lục lọi kho tài liệu để mang đúng trang tài liệu cần thiết đưa cho LLM (Generator) đọc."
                }
            ],
            "source_citations": [
                {"heading": "What is RAG?", "quote": "Search context, then generate."}
            ]
        }
    }


def main():
    repo_root = get_repo_root()
    data_dir = repo_root / "ai-learning-companion" / "data"
    demo_lessons_file = data_dir / "demo_lessons.json"
    cards_out_file = data_dir / "nontech-cards" / "cards.demo.json"

    if not demo_lessons_file.exists():
        print(f"Error: {demo_lessons_file} not found.")
        return 1

    with open(demo_lessons_file, "r", encoding="utf-8") as f:
        demo_lessons = json.load(f).get("demo_lessons", [])

    content_map = get_demo_cards_content()
    cards = []

    for lesson_id in demo_lessons:
        doc_path = repo_root / "phases" / lesson_id / "docs" / "en.md"
        if not doc_path.exists():
            print(f"Error: Source document for {lesson_id} not found at {doc_path}")
            return 1
            
        rel_doc_path = f"phases/{lesson_id}/docs/en.md"
        
        if lesson_id not in content_map:
            print(f"Error: No demo content mapped for {lesson_id}")
            return 1
            
        card_content = content_map[lesson_id]
        
        card = {
            "lesson_id": lesson_id,
            "source_doc_path": rel_doc_path,
            "generated_at": "2026-06-27T00:00:00+00:00",
            "review_status": "reviewed",
            "audience_level": "nontech_beginner",
            "title_vi": card_content["title_vi"],
            "plain_language_summary_vi": card_content["plain_language_summary_vi"],
            "why_it_matters_vi": card_content["why_it_matters_vi"],
            "daily_life_analogy_vi": card_content["daily_life_analogy_vi"],
            "mental_model_vi": card_content["mental_model_vi"],
            "minimal_example_vi": card_content["minimal_example_vi"],
            "real_app_use_vi": card_content["real_app_use_vi"],
            "common_misunderstandings_vi": card_content["common_misunderstandings_vi"],
            "source_citations": card_content["source_citations"],
            "check_questions": card_content["check_questions"]
        }
        cards.append(card)

    cards_out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cards_out_file, "w", encoding="utf-8") as f:
        json.dump({"cards": cards}, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {len(cards)} non-tech cards to {cards_out_file.relative_to(repo_root)}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
