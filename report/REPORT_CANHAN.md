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

Phần này trình bày cách tôi triển khai các thành phần chính trong gói `src` và chiến lược chunking cá nhân.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
Hàm dùng regex `(?<=[.!?])(?:[ \t]+|\n+)` để tách tại vị trí sau dấu kết thúc câu, vì vậy dấu `.`, `!` hoặc `?` vẫn được giữ lại trong câu. Văn bản rỗng hoặc chỉ có khoảng trắng trả về `[]`, sau đó các câu được gom theo `max_sentences_per_chunk` và loại bỏ khoảng trắng thừa. Edge case còn hạn chế là chữ viết tắt như `TS.` hoặc số thập phân có thể bị hiểu nhầm là ranh giới câu.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
Thuật toán thử separator theo thứ tự ưu tiên `\n\n`, `\n`, `. `, khoảng trắng rồi đến ký tự; các mảnh nhỏ được gộp lại nhưng không vượt quá `chunk_size`. Base case là văn bản rỗng, văn bản đã nhỏ hơn hoặc bằng `chunk_size`, hoặc không còn separator; ở trường hợp cuối hàm fallback sang cắt cứng theo số ký tự để tránh đệ quy vô hạn. Cách này ưu tiên giữ nguyên đoạn và câu trước khi phải cắt nhỏ hơn.

**Chiến lược chunking cá nhân: Custom `HeadingChunker`**
Theo chiến lược đã thống nhất trong báo cáo nhóm, tôi chia tài liệu theo heading/section Markdown để mỗi chunk giữ được tiêu đề của mục chính sách. Nếu một section dài hơn `chunk_size`, phần nội dung được chia tiếp bằng `RecursiveChunker` và heading được lặp lại ở đầu mỗi chunk để giữ ngữ cảnh. Cách này phù hợp với tài liệu Shopee có cấu trúc mục rõ ràng; độ dài chunk có thể không đồng đều nên cần kiểm tra khi benchmark.

Trong benchmark thực tế với `chunk_size=500`, chiến lược này tạo 186 chunks. Heading giúp giữ dấu vết của mục chính sách, nhưng các section dài tạo nhiều chunk lặp lại cùng heading và cạnh tranh vị trí trong top-3. Phiên bản chạy được được đặt trong `src/chunking.py`; runner `bench.py` dùng chính lớp này để tái lập benchmark.

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

Các điểm trong mục này được tính bằng `MockEmbedder`; benchmark retrieval ở mục 5 dùng model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` nên hai nhóm điểm không được so sánh trực tiếp.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Tôi chạy 5 câu hỏi chung của nhóm bằng `HeadingChunker(chunk_size=500)`, model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` và `top_k=3`. Corpus sau khi chia gồm 186 chunks. Mỗi câu hỏi được gọi qua `KnowledgeBaseAgent.answer()`; Agent truy xuất top-3, dựng prompt và gọi `ExtractiveAnswerGenerator` cục bộ để sinh câu trả lời trực tiếp từ context kèm citation. Bộ sinh không nhận gold answer; gold chỉ được dùng sau khi sinh để kiểm tra độ đầy đủ và tính điểm. Cách chạy này không cần API key và có thể tái lập bằng `py -3.11 bench.py`.

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Score | Đánh giá top-3 | Câu trả lời thực tế của Agent (tóm tắt) |
|---|-------|--------------------------------|------:|------------------|-----------------------------------------|
| 1 | Người mua có tối đa bao lâu để gửi yêu cầu trả hàng/hoàn tiền đối với đơn hàng thông thường và thực phẩm tươi sống hoặc đông lạnh? | `chinh-sach-tra-hang-hoan-tien#11`: thời hạn 15 ngày | 0.8171 | Có — gold `quy-dinh-chung-tra-hang-hoan-tien#3` ở hạng 2 | Agent trích được 15 ngày cho đơn thông thường và 24 giờ cho thực phẩm tươi sống/đông lạnh `[1][2]`; answer đủ, **1/2 điểm** |
| 2 | Trong những trường hợp nào người mua có thể yêu cầu trả hàng/hoàn tiền? Hãy liệt kê ít nhất bốn trường hợp. | `chinh-sach-tra-hang-hoan-tien#12`: hỗ trợ sau thời hạn trả hàng | 0.6502 | Không — tài liệu chuẩn không vào top-3 | Agent chỉ nêu các trường hợp hoàn tiền một phần/không cần trả hàng; thiếu nhận thiếu, sai, bể vỡ hoặc hư hỏng; **0/2 điểm** |
| 3 | Shopee có hỗ trợ đổi sản phẩm trực tiếp không? Người mua nên làm gì nếu sản phẩm nhận được bị sai hoặc hư hỏng? | `tra-hang-do-doi-y#20`: bao bì và phụ kiện khi trả hàng | 0.7649 | Không — tài liệu chuẩn không vào top-3 | Agent nêu một số trường hợp “đổi ý”, giao sai và hư hỏng nhưng không trả lời kết luận “chưa hỗ trợ đổi hàng” và hướng xử lý; **0/2 điểm** |
| 4 | Sau khi Shopee chấp nhận hoàn tiền, người mua thanh toán khi nhận hàng có thể nhận tiền qua đâu và mất bao lâu? | `huong-dan-gui-yeu-cau-tra-hang#6`: thời gian hoàn tiền 1–14 ngày làm việc | 0.7936 | Có một phần — gold `thoi-gian-nhan-tien-hoan#7` ở hạng 2 | Agent trả lời mốc chung 1–14 ngày và dẫn tới bảng, nhưng thiếu Ví ShopeePay/24 giờ và tài khoản ngân hàng/2 ngày làm việc; **0/2 điểm** |
| 5 | Khi hệ thống ghi nhận đã trả hàng thành công nhưng Shop chưa nhận được hàng hoặc hàng hoàn gặp vấn đề, người bán phải phản hồi trong thời hạn bao lâu và thực hiện phản hồi ở đâu? (`metadata_filter={"audience": "seller"}`) | `chinh-sach-tra-hang-hoan-tien#33`: người bán phản hồi trong 02 ngày | 0.7263 | Có — gold `quan-ly-don-tra-hang-nguoi-ban#6` ở hạng 2 | Agent trích được thời hạn 02 ngày và phần “Phản hồi đến Shopee” trên Kênh Quản Lý Shop `[1][2][3]`; answer đủ, **1/2 điểm** |

**Kết quả tổng hợp:**

- Tài liệu chuẩn xuất hiện trong top-3 ở **3/5 câu**: Q1, Q4 và Q5.
- Câu trả lời thực tế của Agent đủ thông tin bắt buộc ở **2/5 câu**: Q1 và Q5.
- Tổng điểm retrieval: **2/10**.
- Runner tái lập: `bench.py`; output đầy đủ gồm top-3, answer và citation được lưu tại `report/KET_QUA_BENCHMARK_HEADING_CHUNKER.txt`.

**Lọc bằng metadata:** Ở Q5, `metadata_filter={"audience": "seller"}` trả về cùng top-3 và cùng score như khi không lọc. Bộ lọc chưa cải thiện thứ hạng vì chunk top-1 có `audience="both"` và vẫn được xem là phù hợp với truy vấn dành cho người bán.

**Điều hay nhất tôi học được từ kết quả của các thành viên khác:**
Điểm quan sát cao nhất của nhóm là 4/10 với `RecursiveChunker + TF-IDF`, nhưng các thành viên chưa dùng cùng embedding backend nên chưa thể quy khác biệt điểm hoàn toàn cho chunker. Bài học quan trọng nhất là phải cố định corpus, embedding, runner, `top_k` và cách chấm khi so sánh chiến lược. Q2 cho thấy danh sách dài dễ bị phân mảnh qua nhiều chunk; Q3 cho thấy truy vấn có từ “đổi” dễ bị kéo sang tài liệu “đổi ý” dù thiếu câu phủ định cần thiết. Nếu cải thiện `HeadingChunker`, tôi sẽ loại các chunk chỉ có heading, xử lý riêng bảng/danh sách và thêm reranking hoặc giới hạn số chunk từ cùng một tài liệu để giảm cạnh tranh trong top-3.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 2 / 10 |
| **Tổng phần cá nhân** | **52 / 60** |
