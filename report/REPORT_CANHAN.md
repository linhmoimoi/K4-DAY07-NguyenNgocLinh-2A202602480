# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Ngọc Linh
**Nhóm:** G00
**Ngày:** 2026-09-20

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
Độ tương tự cosine cao nghĩa là hai vector embedding có hướng gần nhau, thường cho thấy hai đoạn văn có nội dung hoặc ý nghĩa gần nhau. Giá trị càng gần 1 thì mức tương đồng về hướng càng lớn; giá trị gần 0 hoặc âm cho thấy hai vector ít tương đồng hoặc ngược hướng.

**Ví dụ có độ tương tự CAO:**
- Câu A: Người mua có thể yêu cầu hoàn tiền trong bảy ngày.
- Câu B: Khách hàng được phép nhận lại tiền trong vòng một tuần.
- Tại sao tương đồng: Hai câu dùng từ khác nhau nhưng cùng diễn đạt quyền yêu cầu hoàn tiền trong một khoảng thời gian tương đương.

**Ví dụ có độ tương tự THẤP:**
- Câu A: Chính sách bảo hành áp dụng cho người bán.
- Câu B: Hà Nội có nhiều ngày nắng.
- Tại sao khác: Một câu nói về chính sách thương mại, câu còn lại nói về thời tiết nên chủ đề và ý nghĩa khác nhau.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
Cosine tập trung vào hướng của vector, phù hợp với việc so sánh ý nghĩa văn bản và ít bị ảnh hưởng bởi độ dài hoặc độ lớn tuyệt đối của embedding. Với embedding đã chuẩn hóa, cosine còn tương đương với dot product nên tìm kiếm đơn giản và hiệu quả.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
Phép tính theo công thức của bài: `ceil((10000 - 50) / (500 - 50)) = ceil(9950 / 450) = 23`.

Đối chiếu bằng `FixedSizeChunker(chunk_size=500, overlap=50)` trong repo cũng cho kết quả **23 chunks**.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
Khi `overlap=100`, số chunk là `ceil((10000 - 100) / (500 - 100)) = ceil(9900 / 400) = 25`, tức tăng từ 23 lên 25. Overlap lớn giúp giữ lại ngữ cảnh ở ranh giới giữa hai chunk, nhưng làm tăng số chunk, dung lượng lưu trữ và chi phí embedding/search.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
Hàm dùng regex `(?<=[.!?])(?:[ \t]+|\n+)` để tách tại vị trí sau dấu kết thúc câu, vì vậy dấu `.`, `!` hoặc `?` vẫn được giữ lại trong câu. Văn bản rỗng hoặc chỉ có khoảng trắng trả về `[]`, sau đó các câu được gom theo `max_sentences_per_chunk` và loại bỏ khoảng trắng thừa. Edge case còn hạn chế là chữ viết tắt như `TS.` hoặc số thập phân có thể bị hiểu nhầm là ranh giới câu.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
Thuật toán thử separator theo thứ tự ưu tiên `\n\n`, `\n`, `. `, khoảng trắng rồi đến ký tự; các mảnh nhỏ được gộp lại nhưng không vượt quá `chunk_size`. Base case là văn bản rỗng, văn bản đã nhỏ hơn hoặc bằng `chunk_size`, hoặc không còn separator; ở trường hợp cuối hàm fallback sang cắt cứng theo số ký tự để tránh đệ quy vô hạn. Cách này ưu tiên giữ nguyên đoạn và câu trước khi phải cắt nhỏ hơn.

**Chiến lược chunking cá nhân: Custom `HeadingChunker`**
Theo chiến lược đã thống nhất trong báo cáo nhóm, tôi chia tài liệu theo heading/section Markdown để mỗi chunk giữ được tiêu đề của mục chính sách. Nếu một section dài hơn `chunk_size`, phần nội dung được chia tiếp bằng `RecursiveChunker` và heading được lặp lại ở đầu mỗi chunk để giữ ngữ cảnh. Cách này phù hợp với tài liệu Shopee có cấu trúc mục rõ ràng; độ dài chunk có thể không đồng đều nên cần kiểm tra khi benchmark.

```python
import re

from src.chunking import RecursiveChunker


class HeadingChunker:
    def __init__(self, chunk_size: int = 500) -> None:
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []

        sections = re.split(r"(?m)(?=^#{1,6}\s+)", text.strip())
        chunks = []
        for section in sections:
            section = section.strip()
            if not section:
                continue
            if len(section) <= self.chunk_size:
                chunks.append(section)
                continue

            match = re.match(r"^(#{1,6}\s+[^\n]+)", section)
            heading = match.group(1) if match else ""
            body = section[match.end():].strip() if match else section
            body_limit = max(1, self.chunk_size - len(heading) - 1)
            pieces = RecursiveChunker(chunk_size=body_limit).chunk(body)
            chunks.extend(
                f"{heading}\n{piece}" if heading else piece
                for piece in pieces
            )
        return chunks
```

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
`add_documents` lưu mỗi `Document` thành một record in-memory, tạo embedding cho nội dung và sao chép metadata; việc chia chunk được thực hiện ở bên ngoài store. `search` tạo embedding cho query, tính dot product với các embedding đã lưu, sắp xếp score giảm dần và trả về tối đa `top_k` kết quả. Vì các embedder trong lab chuẩn hóa vector nên dot product tương đương cosine similarity.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
`search_with_filter` lọc trước theo tất cả cặp key/value trong `metadata_filter`, sau đó gửi đúng tập ứng viên vào cùng `_search_records`; cách này tránh việc các kết quả không phù hợp chiếm hết top-k. `delete_document` giữ lại những record có `metadata['doc_id']` khác doc_id cần xóa và trả về `True` nếu có ít nhất một record bị loại. Metadata được bổ sung `doc_id` và copy để việc xóa các chunk cùng một file vẫn truy vết được về tài liệu gốc.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
`answer` trước hết truy xuất top-k kết quả từ store. Mỗi chunk được đưa vào prompt với số thứ tự `[1]`, `[2]`, nguồn và score; prompt yêu cầu mô hình chỉ dùng CONTEXT, nói rõ khi không đủ thông tin và trích dẫn số nguồn khi trả lời. Nếu store rỗng, hàm trả về thông báo không tìm thấy thông tin và không gọi LLM không cần thiết.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
============================= test session starts =============================
collected 42 items
........................................................................ [100%]
42 passed in 0.06s
```

Lệnh chạy: `py -3.11 -m pytest tests/ -v`

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | A cat sits on the mat. | A feline rests on a rug. | cao | 0.024672 | Không |
| 2 | The return policy allows refunds within seven days. | The weather is sunny in Hanoi. | thấp | -0.240906 | Có |
| 3 | Python is a programming language. | Python is used to write software. | cao | 0.050174 | Không |
| 4 | Seller must provide warranty support. | Buyer asks for a refund. | thấp | 0.040280 | Có |
| 5 | The store filters documents by audience. | The search narrows results using metadata. | cao | 0.099903 | Không |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
Các cặp 1 và 3 có ý nghĩa khá gần nhau nhưng điểm thấp, trong khi một số cặp khác chủ đề vẫn có điểm dương. Điều này là có thể dự đoán vì lab đang dùng `MockEmbedder`: vector được tạo từ MD5 và số giả ngẫu nhiên xác định, không có khả năng hiểu ngữ nghĩa. Vì vậy kết quả này phù hợp để kiểm tra cấu trúc và công thức cosine, nhưng không nên dùng để kết luận chất lượng semantic retrieval.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá đã thống nhất trong nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. Dùng đúng các câu hỏi dưới đây để kết quả có thể so sánh với thành viên khác (xem `REPORT_NHOM.md`).

> **Trạng thái:** Nhóm đã thống nhất đủ 5 câu hỏi và câu trả lời chuẩn. Bảng dưới đây đã được cập nhật theo báo cáo nhóm; chưa có kết quả benchmark cá nhân cho cấu hình `HeadingChunker`, nên các ô kết quả đang để trống/chưa xác định. Câu 5 dùng bộ lọc metadata `{"audience": "seller"}` như yêu cầu trong báo cáo nhóm.

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Người mua có tối đa bao lâu để gửi yêu cầu trả hàng/hoàn tiền đối với đơn hàng thông thường và thực phẩm tươi sống hoặc đông lạnh? | Chưa chạy benchmark | — | Chưa xác định | — |
| 2 | Trong những trường hợp nào người mua có thể yêu cầu trả hàng/hoàn tiền? Hãy liệt kê ít nhất bốn trường hợp. | Chưa chạy benchmark | — | Chưa xác định | — |
| 3 | Shopee có hỗ trợ đổi sản phẩm trực tiếp không? Người mua nên làm gì nếu sản phẩm nhận được bị sai hoặc hư hỏng? | Chưa chạy benchmark | — | Chưa xác định | — |
| 4 | Sau khi Shopee chấp nhận hoàn tiền, người mua thanh toán khi nhận hàng có thể nhận tiền qua đâu và mất bao lâu? | Chưa chạy benchmark | — | Chưa xác định | — |
| 5 | Khi hệ thống ghi nhận đã trả hàng thành công nhưng Shop chưa nhận được hàng hoặc hàng hoàn gặp vấn đề, người bán phải phản hồi trong thời hạn bao lâu và thực hiện phản hồi ở đâu? (`metadata_filter={"audience": "seller"}`) | Chưa chạy benchmark | — | Chưa xác định | — |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** Chưa chạy benchmark / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
Chưa có dữ liệu demo hoặc kết quả benchmark chung trong báo cáo nhóm để ghi nhận. Sẽ bổ sung sau buổi demo hoặc khi nhóm hoàn thành so sánh kết quả các chiến lược.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | Chưa xác định / 10 |
| **Tổng phần cá nhân tạm tính** | **50 / 60, chờ benchmark** |
