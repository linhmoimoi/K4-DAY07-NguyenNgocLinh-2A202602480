# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** G00
**Thành viên:** Đặng Văn Thái Anh, Nguyễn Lê Ngọc Bảo, Lê Thị Châm Anh, Nguyễn Ngọc Linh
**Ngày:** 20/09/2026

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Chính sách thương mại điện tử Shopee: trả hàng, hoàn tiền, bảo hành và quy trình xử lý dành cho người mua/người bán.

**Tại sao nhóm chọn chủ đề này?**
> Bộ tài liệu lấy từ Trung tâm trợ giúp Shopee, bao phủ cả quy định, hướng dẫn thao tác, ngoại lệ và quy trình phía người bán nên phù hợp với câu hỏi thực tế. Metadata `audience` cho phép đánh giá việc lọc kết quả theo người mua hoặc người bán, còn `category` giúp phân biệt nhóm chủ đề khi truy xuất.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự nội dung | Metadata đã gán |
|---|--------------|--------------------|----------------------|------------------:|-----------------|
| 1 | Chính sách bảo hành cho sản phẩm mua tại Shopee | [Shopee Help Center (79046)](https://help.shopee.vn/portal/4/article/79046-%5BQuy%20%C4%91%E1%BB%8Bnh%5D%20Ch%C3%ADnh%20s%C3%A1ch%20b%E1%BA%A3o%20h%C3%A0nh%20cho%20s%E1%BA%A3n%20ph%E1%BA%A9m%20mua%20t%E1%BA%A1i%20Shopee) | 2026-09-20 / not-stated | 4.421 | `audience=buyer`; `category=warranty-policy`; `language=vi` |
| 2 | Chính sách Trả hàng và Hoàn tiền | [Shopee Help Center (77251)](https://help.shopee.vn/portal/4/article/77251-CH%C3%8DNH%20S%C3%81CH%20TR%E1%BA%A2%20H%C3%80NG%20V%C3%80%20HO%C3%80N%20TI%E1%BB%80N) | 2026-09-20 / not-stated | 19.609 | `audience=both`; `category=returns-policy`; `language=vi` |
| 3 | Hướng dẫn gửi yêu cầu Trả hàng/Hoàn tiền | [Shopee Help Center (79233)](https://help.shopee.vn/portal/4/article/79233-%5BTr%E1%BA%A3%20h%C3%A0ng%2F%20Ho%C3%A0n%20ti%E1%BB%81n%5D%20H%C6%B0%E1%BB%9Bng%20d%E1%BA%ABn%20g%C6%B0%CC%89i%20y%C3%AAu%20c%E1%BA%A7u%20Tr%E1%BA%A3%20h%C3%A0ng%2F%20Ho%C3%A0n%20ti%E1%BB%81n) | 2026-09-20 / not-stated | 2.518 | `audience=buyer`; `category=returns-process`; `language=vi` |
| 4 | Các phương thức gửi hàng hoàn trả và phí hoàn trả | [Shopee Help Center (189477)](https://help.shopee.vn/portal/4/article/189477-%5BTr%E1%BA%A3%20h%C3%A0ng%2F%20Ho%C3%A0n%20ti%E1%BB%81n%5D%20C%C3%A1c%20ph%C6%B0%C6%A1ng%20th%E1%BB%A9c%20g%E1%BB%ADi%20h%C3%A0ng%20ho%C3%A0n%20tr%E1%BA%A3%20v%C3%A0%20ph%C3%AD%20ho%C3%A0n%20tr%E1%BA%A3) | 2026-09-20 / not-stated | 5.930 | `audience=buyer`; `category=returns-logistics`; `language=vi` |
| 5 | Quản lý đơn trả hàng hoàn tiền (Kênh Quản Lý người bán) | [Shopee Help Center (102521)](https://help.shopee.vn/portal/1/article/102521-Qu%E1%BA%A3n%20l%C3%BD%20%C4%91%C6%A1n%20tr%E1%BA%A3%20h%C3%A0ng%20ho%C3%A0n%20ti%E1%BB%81n) | 2026-09-20 / not-stated | 3.867 | `audience=seller`; `category=returns-process`; `language=vi` |
| 6 | Những quy định chung về Trả hàng/Hoàn tiền | [Shopee Help Center (188931)](https://help.shopee.vn/portal/4/article/188931-%5BTr%E1%BA%A3%20h%C3%A0ng%2FHo%C3%A0n%20ti%E1%BB%81n%5D%20Nh%E1%BB%AFng%20quy%20%C4%91%E1%BB%8Bnh%20chung%20v%E1%BB%81%20Tr%E1%BA%A3%20h%C3%A0ng%2F%20Ho%C3%A0n%20ti%E1%BB%81n%20c%E1%BB%A7a%20Shopee) | 2026-09-20 / not-stated | 6.318 | `audience=buyer`; `category=returns-policy`; `language=vi` |
| 7 | Quy trình Shopee xử lý yêu cầu Trả hàng/Hoàn tiền | [Shopee Help Center (190242)](https://help.shopee.vn/portal/4/article/190242-%5BTr%E1%BA%A3%20h%C3%A0ng%2F%20Ho%C3%A0n%20ti%E1%BB%81n%5D%20Quy%20tr%C3%ACnh%20Shopee%20x%E1%BB%AD%20l%C3%BD%20y%C3%AAu%20c%E1%BA%A7u%20Tr%E1%BA%A3%20h%C3%A0ng%2F%20Ho%C3%A0n%20ti%E1%BB%81n) | 2026-09-20 / not-stated | 8.111 | `audience=both`; `category=returns-process`; `language=vi` |
| 8 | Sản phẩm hạn chế trả hàng là gì | [Shopee Help Center (79465)](https://help.shopee.vn/portal/4/article/79465-%5BTr%E1%BA%A3%20h%C3%A0ng%2F%20Ho%C3%A0n%20ti%E1%BB%81n%5D%20S%E1%BA%A3n%20ph%E1%BA%A9m%20h%E1%BA%A1n%20ch%E1%BA%BF%20tr%E1%BA%A3%20h%C3%A0ng%20l%C3%A0%20g%C3%AC%3F) | 2026-09-20 / not-stated | 1.463 | `audience=buyer`; `category=returns-exceptions`; `language=vi` |
| 9 | Thời gian nhận tiền hoàn và cách kiểm tra tiền hoàn | [Shopee Help Center (189473)](https://help.shopee.vn/portal/4/article/189473-%5BTr%E1%BA%A3%20h%C3%A0ng%2F%20Ho%C3%A0n%20ti%E1%BB%81n%5D%20Th%E1%BB%9Di%20gian%20nh%E1%BA%ADn%20ti%E1%BB%81n%20ho%C3%A0n%20v%C3%A0%20c%C3%A1ch%20ki%E1%BB%83m%20tra%20ti%E1%BB%81n%20ho%C3%A0n) | 2026-09-20 / not-stated | 3.898 | `audience=buyer`; `category=refund-timeline`; `language=vi` |
| 10 | Những điều cần biết về Trả hàng do Đổi ý/không còn nhu cầu | [Shopee Help Center (204305)](https://help.shopee.vn/portal/4/article/204305-Nh%E1%BB%AFng%20%C4%91i%E1%BB%81u%20c%E1%BA%A7n%20bi%E1%BA%BFt%20v%E1%BB%81%20Tr%E1%BA%A3%20h%C3%A0ng%20do%20%22%C4%90%E1%BB%95i%20%C3%BD%2Fkh%C3%B4ng%20c%C3%B2n%20nhu%20c%E1%BA%A7u%22) | 2026-09-20 / not-stated | 7.371 | `audience=buyer`; `category=returns-exceptions`; `language=vi` |

*Số ký tự được tính trên phần nội dung Markdown sau front matter; chưa tính metadata.*

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) gồm các bài chính sách công khai từ Trung tâm trợ giúp Shopee; không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Cả 10 tài liệu đều có `source_url`, `retrieved_at`, `document_version` trong metadata; `document_version` hiện ghi `not-stated`.
- [x] Trường `audience` có đủ ba giá trị `buyer`, `seller` và `both`, nhờ đó có thể kiểm tra tác động thực tế của `metadata_filter` thay vì chỉ lưu metadata để mô tả.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | Chuỗi | `thoi-gian-nhan-tien-hoan` | Định danh duy nhất để truy nguồn, quản lý và xóa tài liệu. |
| `title` | Chuỗi | `Thời gian nhận tiền hoàn và cách kiểm tra tiền hoàn` | Nhận diện nội dung và bổ sung tiêu đề vào ngữ cảnh truy xuất. |
| `audience` | Enum: `buyer` / `seller` / `both` | `seller` | Lọc tài liệu theo đối tượng; tài liệu `both` dùng được cho cả hai phía. |
| `category` | Chuỗi | `refund-timeline` | Giới hạn kết quả theo nhóm chủ đề như chính sách, quy trình hoặc ngoại lệ. |
| `language` | Chuỗi | `vi` | Lọc theo ngôn ngữ của câu hỏi và tài liệu. |
| `source_url` | URL | `https://help.shopee.vn/...` | Truy ngược nguồn và dẫn chứng câu trả lời. |
| `retrieved_at` | Ngày ISO 8601 | `2026-09-20` | Biết thời điểm thu thập để đánh giá độ mới của dữ liệu. |
| `document_version` | Chuỗi | `not-stated` | Theo dõi phiên bản hoặc ngày hiệu lực khi nguồn công bố thông tin này. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare(chunk_size=500)` trên phần nội dung sau front matter của ba tài liệu đại diện trong corpus hiện tại:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Đánh giá ngữ cảnh |
|-----------|----------|-------------:|------------------:|-------------------|
| `quy-dinh-chung-tra-hang-hoan-tien.md` (6.318 ký tự) | FixedSizeChunker (`fixed_size`) | 13 | 486,0 | Có thể cắt giữa điều khoản |
|  | SentenceChunker (`by_sentences`, 3 câu/chunk) | 10 | 626,8 | Giữ câu nhưng chunk dài không đồng đều |
|  | RecursiveChunker (`recursive`) | 15 | 417,6 | Ưu tiên ranh giới đoạn, vẫn có thể tách khỏi heading |
| `thoi-gian-nhan-tien-hoan.md` (3.898 ký tự, có bảng) | FixedSizeChunker | 8 | 487,2 | Có thể cắt giữa hàng hoặc cột bảng |
|  | SentenceChunker | 4 | 972,0 | Gom nhiều nội dung vì cấu trúc bảng ít dấu kết thúc câu |
|  | RecursiveChunker | 10 | 386,1 | Tách theo dòng tốt hơn nhưng vẫn có thể xé bảng dài |
| `chinh-sach-tra-hang-hoan-tien.md` (19.609 ký tự) | FixedSizeChunker | 40 | 490,2 | Kích thước ổn định nhưng nhiều chunk cạnh tranh top-k |
|  | SentenceChunker | 43 | 453,3 | Không cắt giữa câu nhưng có thể mất liên kết với heading |
|  | RecursiveChunker | 62 | 313,7 | Nhiều chunk nhỏ do tài liệu có nhiều xuống dòng |

**Nhận xét baseline:**
> Ba chiến lược có sẵn chưa khai thác trực tiếp cấu trúc heading Markdown của tài liệu Shopee. `SentenceChunker` giữ ranh giới câu nhưng xử lý bảng kém; `FixedSizeChunker` dễ cắt ngang ý; còn `RecursiveChunker` bảo toàn đoạn tốt hơn nhưng sinh nhiều chunk nhỏ trên tài liệu dài. Đây là cơ sở để nhóm thử `HeadingChunker`, trong đó heading được gắn lại vào từng mảnh con khi section vượt quá giới hạn.

### Chiến lược của từng thành viên

Mỗi thành viên thử một chiến lược riêng trên cùng corpus và cùng bộ 5 benchmark query.

**Đặng Văn Thái Anh**
- **Loại chiến lược:** `SentenceChunker` (`max_sentences_per_chunk=3`)
- **Mô tả & lý do chọn cho chủ đề này:** Gom ba câu hoàn chỉnh vào mỗi chunk để giữ mạch diễn đạt của các quy định và hướng dẫn Shopee. Cách này dễ đọc, nhưng độ dài chunk không đồng đều và một mục chính sách dài có thể bị tách khỏi tiêu đề.
- **Code snippet (nếu custom):** Không áp dụng — dùng `SentenceChunker` có sẵn.

**Nguyễn Lê Ngọc Bảo**
- **Loại chiến lược:** `FixedSizeChunker` (`chunk_size=500`, `overlap=80`)
- **Mô tả & lý do chọn cho chủ đề này:** Chia văn bản thành các chunk có kích thước ổn định, thuận tiện kiểm soát số lượng và so sánh retrieval. Overlap 80 ký tự giữ thêm ngữ cảnh ở ranh giới, nhưng chunk vẫn có thể cắt ngang câu hoặc tiêu đề và tạo nội dung lặp.
- **Code snippet (nếu custom):** Không áp dụng — dùng `FixedSizeChunker` có sẵn.

**Lê Thị Châm Anh**
- **Loại chiến lược:** `RecursiveChunker` (`chunk_size=500`)
- **Mô tả & lý do chọn cho chủ đề này:** Thử tách theo ranh giới lớn như đoạn và dòng trước, rồi mới dùng dấu câu hoặc khoảng trắng khi cần. Chiến lược này có thể giữ cấu trúc văn bản tốt hơn cắt ký tự cố định, nhưng không đảm bảo mỗi chunk tương ứng trọn vẹn với một mục chính sách.
- **Code snippet (nếu custom):** Không áp dụng — dùng `RecursiveChunker` có sẵn.

**Nguyễn Ngọc Linh**
- **Loại chiến lược:** Custom `HeadingChunker` — chia theo heading/section Markdown, dùng `RecursiveChunker` cho mục quá dài.
- **Mô tả & lý do chọn cho chủ đề này:** Các tài liệu Shopee có tiêu đề và mục đánh số; giữ heading trong chunk giúp nhận biết quy định thuộc phần nào và truy nguồn dễ hơn. Với section dài hơn giới hạn, chunker tiếp tục chia nhỏ phần nội dung nhưng lặp lại heading để giữ ngữ cảnh; cần kiểm tra các chunk này không vượt quá kích thước mục tiêu.
- **Code snippet (nếu custom):**
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

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Embedding | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|-----------|----------------------|-----------|----------|
| Đặng Văn Thái Anh | `SentenceChunker` (3 câu/chunk) | `MockEmbedder` | 2 / 10 theo bản đính kèm | Giữ ranh giới câu, chunk dễ đọc | Độ dài không đồng đều; có thể mất liên kết với heading |
| Nguyễn Lê Ngọc Bảo | `FixedSizeChunker` (500, overlap 80) | MiniLM đa ngôn ngữ | 3 / 10 | Kích thước ổn định; overlap giữ ngữ cảnh ở biên | Có thể cắt ngang câu/mục; overlap tạo nội dung lặp |
| Lê Thị Châm Anh | `RecursiveChunker` (500) | TF-IDF word + bigram | 4 / 10 theo kết quả riêng | Ưu tiên tách theo đoạn/dòng; Q1 và Q4 truy xuất được thông tin liên quan | Không nhất thiết giữ heading; danh sách dài vẫn bị trải qua nhiều chunk |
| Nguyễn Ngọc Linh | Custom `HeadingChunker` (heading + recursive fallback, 500) | MiniLM đa ngôn ngữ | 2 / 10 | Giữ tiêu đề/mục chính sách trong ngữ cảnh | Một số section dài và các chunk lặp heading cạnh tranh top-3 |

**Benchmark FixedSizeChunker:** JSON nhóm cung cấp ghi nhận model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (local), `top_k=3`, `chunk_size=500`, `overlap=80` và **149 chunks**.

**Benchmark Nguyễn Ngọc Linh:** Chạy ngày 2026-09-20 trên corpus hiện có bằng cùng model local và `top_k=3`; `HeadingChunker(chunk_size=500)` tạo **186 chunks**. Điểm được tính theo vị trí tài liệu chuẩn trong top-3 và các cụm nội dung cần có từ đáp án chuẩn; chi tiết ở mục 3.

> **Lưu ý khi so sánh:** Chạy lại `FixedSizeChunker(500, overlap=80)` từ mã nguồn hiện tại tạo 155 chunks và không tái lập được ID chunk top-3 trong JSON đã cung cấp. Vì vậy điểm giữa hai lượt benchmark hiện chỉ mang tính tham khảo cho tới khi thống nhất lại runner/cấu hình FixedSize.

> Bốn kết quả trên còn dùng backend embedding khác nhau. Chênh lệch điểm phản ánh đồng thời tác động của chunking và embedding, nên chưa thể quy toàn bộ khác biệt cho riêng chiến lược chunking.

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> Điểm quan sát cao nhất hiện tại là **4/10** của `RecursiveChunker + TF-IDF`, trong khi `FixedSizeChunker + MiniLM` đạt **3/10** và `HeadingChunker + MiniLM` đạt **2/10**. Tuy nhiên các lượt chạy chưa dùng cùng backend và runner, vì vậy chưa thể kết luận `RecursiveChunker` tốt nhất chỉ từ điểm tổng. Về thiết kế dữ liệu, `HeadingChunker` vẫn phù hợp với tài liệu chính sách có cấu trúc mục rõ ràng; bước tiếp theo cần chạy cả bốn chunker trên cùng MiniLM, cùng corpus và cùng tiêu chí chấm để chọn chiến lược thắng một cách công bằng.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Người mua có tối đa bao lâu để gửi yêu cầu trả hàng/hoàn tiền đối với đơn hàng thông thường và thực phẩm tươi sống hoặc đông lạnh? | Với đơn hàng thông thường, thời hạn là **15 ngày** kể từ khi đơn hàng được cập nhật “Giao hàng thành công”. Với thực phẩm tươi sống hoặc đông lạnh, thời hạn là **24 giờ**, trừ trường hợp khiếu nại “Chưa nhận được hàng”. | `quy-dinh-chung-tra-hang-hoan-tien.md` — mục **1.2. Thời gian tối đa để gửi yêu cầu trả hàng hoàn tiền cho Shopee** |
| 2 | Trong những trường hợp nào người mua có thể yêu cầu trả hàng/hoàn tiền? Hãy liệt kê ít nhất bốn trường hợp. | Có thể yêu cầu khi chưa nhận được hàng; nhận thiếu hàng, phụ kiện hoặc quà tặng; nhận sai sản phẩm; hàng bị bể vỡ, hư hỏng hoặc rò rỉ; hàng lỗi/không hoạt động; hoặc sản phẩm khác rõ ràng so với mô tả. | `quy-dinh-chung-tra-hang-hoan-tien.md` — mục **1.3. Lý do Trả hàng/Hoàn tiền** |
| 3 | Shopee có hỗ trợ đổi sản phẩm trực tiếp không? Người mua nên làm gì nếu sản phẩm nhận được bị sai hoặc hư hỏng? | Shopee **chưa hỗ trợ yêu cầu đổi hàng**. Người mua có thể từ chối nhận khi được đồng kiểm hoặc gửi yêu cầu **Trả hàng/Hoàn tiền** sau khi nhận hàng và trong thời hạn quy định. | `quy-dinh-chung-tra-hang-hoan-tien.md` — mục **1.1. Nguyên tắc chung** |
| 4 | Sau khi Shopee chấp nhận hoàn tiền, người mua thanh toán khi nhận hàng có thể nhận tiền qua đâu và mất bao lâu? | Tiền có thể được hoàn vào **Ví ShopeePay trong 24 giờ**, nếu ví hoạt động bình thường; hoặc vào **tài khoản ngân hàng mặc định đã liên kết trong 2 ngày làm việc**, tùy ngân hàng. | `thoi-gian-nhan-tien-hoan.md` — bảng **Phương thức hoàn tiền và thời gian hoàn tiền** |
| 5 | Khi hệ thống ghi nhận đã trả hàng thành công nhưng Shop chưa nhận được hàng hoặc hàng hoàn gặp vấn đề, người bán phải phản hồi trong thời hạn bao lâu và thực hiện phản hồi ở đâu? | Người bán phải phản hồi trong vòng **2 ngày**, tính từ ngày hệ thống cập nhật trả hàng thành công. Vào **Kênh Quản Lý Shop → Trả hàng/Hoàn tiền → Cần phản hồi → Phản hồi đến Shopee**; hệ thống điều hướng sang Kênh Người Bán để hoàn tất phản hồi. | `quan-ly-don-tra-hang-nguoi-ban.md` — mục **C. Hướng dẫn Phản hồi đến Shopee khi chưa nhận được hàng hoàn hoặc hàng hoàn gặp vấn đề**; `metadata_filter={"audience": "seller"}` |

*Trong bảng so sánh bên dưới, ID của FixedSize lấy từ JSON đã cung cấp; ID của Heading lấy từ lượt benchmark hiện tại. ID thay đổi theo chiến lược và cấu hình chunking.*

### Tổng hợp chất lượng truy xuất của nhóm

> Benchmark chấm theo hạng của tài liệu chuẩn trong top-3 và kiểm tra các cụm bắt buộc trong context: **2 điểm** nếu tài liệu chuẩn hạng 1 và context đủ đáp án, **1 điểm** nếu tài liệu chuẩn hạng 2–3 và context đủ đáp án, **0 điểm** nếu không tìm thấy tài liệu chuẩn hoặc context thiếu cụm bắt buộc. Đây là phép kiểm tra độ bao phủ context, không phải câu trả lời do LLM tạo. Bảng so sánh dưới đây gồm benchmark `FixedSizeChunker` đã cung cấp và lượt `HeadingChunker` của Nguyễn Ngọc Linh; kết luận xếp hạng vẫn tạm thời do lưu ý về khả năng tái lập ở mục 2.

#### Tổng hợp các kết quả hiện có

| Chiến lược | Embedding | Q1 | Q2 | Q3 | Q4 | Q5 | Tổng |
|---|---|:---:|:---:|:---:|:---:|:---:|---:|
| `SentenceChunker(max=3)` | Mock | 0 | 0 | 0 | 0 | 2 | **2/10** |
| `FixedSizeChunker(500, overlap=80)` | MiniLM đa ngôn ngữ | 1 | 0 | 0 | 0 | 2 | **3/10** |
| `RecursiveChunker(500)` | TF-IDF word + bigram | 2 | 0 | 0 | 1 | 1 | **4/10** |
| `HeadingChunker(500)` | MiniLM đa ngôn ngữ | 1 | 0 | 0 | 0 | 1 | **2/10** |

> Bảng này tổng hợp các lượt chạy đã có, nhưng không phải thí nghiệm chỉ thay một biến vì backend embedding chưa đồng nhất. Repo hiện lưu kết quả chi tiết của Heading; kết quả FixedSize đến từ JSON đã cung cấp, còn Sentence và Recursive được bổ sung từ báo cáo đính kèm/kết quả riêng của thành viên. Cần đưa toàn bộ runner và output vào repo trước khi chạy lại phép so sánh cuối cùng.

#### So sánh chi tiết FixedSize và Heading trên MiniLM

| # | Câu hỏi | `FixedSizeChunker` (500, overlap 80) | `HeadingChunker` (500) — Nguyễn Ngọc Linh |
|---|---------|--------------------------------------|-----------------------------------------|
| 1 | Thời hạn gửi yêu cầu trả hàng/hoàn tiền | Gold chunk `quy-dinh-chung-tra-hang-hoan-tien#1` hạng 2; context đủ; **1 / 2**. Top-1 `chinh-sach-tra-hang-hoan-tien#7` (0.8594). | Gold chunk `quy-dinh-chung-tra-hang-hoan-tien#3` hạng 2; context đủ; **1 / 2**. Top-1 `chinh-sach-tra-hang-hoan-tien#11` (0.8171). |
| 2 | Các trường hợp được yêu cầu trả hàng/hoàn tiền | Gold chunk `quy-dinh-chung-tra-hang-hoan-tien#4` hạng 2; context thiếu “bể vỡ”; **0 / 2**. Top-1 `chinh-sach-tra-hang-hoan-tien#5` (0.6943). | Tài liệu chuẩn không vào top-3; context thiếu nhiều trường hợp; **0 / 2**. Top-1 `chinh-sach-tra-hang-hoan-tien#12` (0.6502). |
| 3 | Đổi sản phẩm trực tiếp và cách xử lý khi nhận sai/hỏng | Tài liệu chuẩn không vào top-3; **0 / 2**. Top-1 `tra-hang-do-doi-y#3` (0.8297). | Tài liệu chuẩn không vào top-3; **0 / 2**. Top-1 `tra-hang-do-doi-y#20` (0.7649). |
| 4 | Kênh và thời gian hoàn tiền cho đơn thanh toán khi nhận hàng | Gold chunk `thoi-gian-nhan-tien-hoan#4` hạng 2; context thiếu “2 ngày làm việc”; **0 / 2**. Top-1 `huong-dan-gui-yeu-cau-tra-hang#4` (0.8345). | Gold chunk `thoi-gian-nhan-tien-hoan#7` hạng 2; context thiếu phương thức và mốc “2 ngày làm việc”; **0 / 2**. Top-1 `huong-dan-gui-yeu-cau-tra-hang#6` (0.7936). |
| 5 | Người bán phản hồi khi chưa nhận được hàng hoàn/hàng có vấn đề | Có lọc: gold chunk `quan-ly-don-tra-hang-nguoi-ban#5` hạng 1, context đủ; **2 / 2**. Không lọc: **0 / 2**. | Có lọc: gold chunk `quan-ly-don-tra-hang-nguoi-ban#6` hạng 2, context có “2 ngày” và “Phản hồi đến Shopee”; **1 / 2**. Không lọc trả về cùng top-3 và cũng **1 / 2**. |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> Tác động phụ thuộc chiến lược: với FixedSize, lọc `audience=seller` tăng câu 5 từ **0 / 2** lên **2 / 2**. Với HeadingChunker, top-3 câu 5 giống nhau khi bật/tắt filter và cả hai lượt đạt **1 / 2**; bộ lọc không cải thiện kết quả vì tài liệu `audience=both` vẫn được xem là phù hợp với `seller`. Tổng lượt HeadingChunker là **2 / 10**; cần đồng bộ lại cách chạy FixedSize và benchmark thêm các chiến lược còn lại trước khi kết luận chiến lược tốt nhất.

#### Phân tích lỗi chung

- **Q2 — câu hỏi dạng danh sách:** thông tin cần trả lời trải qua nhiều dòng hoặc nhiều chunk; top-3 thường đúng chủ đề nhưng không chứa đủ bốn trường hợp.
- **Q3 — ý phủ định:** các tài liệu về “đổi ý” hoặc hàng hư hỏng có độ tương tự từ vựng cao, trong khi chunk chứa kết luận “chưa hỗ trợ đổi hàng” không lọt top-3.
- **Q4 — các mốc thời gian gần nhau:** chunk nói về thời gian xử lý yêu cầu cạnh tranh với chunk nói về thời gian nhận tiền; retrieval dễ lấy đúng chủ đề nhưng sai loại thời gian.
- **Q5 — tác động của metadata:** filter giúp rõ rệt với FixedSize nhưng không đổi kết quả của Heading, cho thấy hiệu quả lọc phụ thuộc vào phân bố chunk và cách `audience=both` được xử lý.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> 1. **Backend embedding và chunking phải được kiểm soát cùng lúc.** Điểm hiện có dao động từ 2–4/10, nhưng các thành viên chưa dùng cùng backend nên không thể quy toàn bộ chênh lệch cho chunker. Benchmark tiếp theo cần cố định MiniLM, corpus, `top_k` và cách chấm, chỉ thay chunker.
>
> 2. **Hai failure case chung là danh sách dài và ý phủ định.** Q2 thất bại vì các lý do trả hàng bị phân tán qua nhiều chunk; Q3 thất bại vì tài liệu “Trả hàng do Đổi ý” có từ vựng gần câu hỏi, làm chìm chunk chứa câu “chưa hỗ trợ đổi hàng”.
>
> 3. **Metadata filter không bảo đảm cải thiện trong mọi chiến lược.** Filter `audience=seller` giúp FixedSize ở Q5, nhưng không đổi top-3 của HeadingChunker vì store coi `audience=both` là phù hợp với truy vấn seller. Do đó phải đánh giá filter bằng A/B thay vì mặc định xem filter luôn tốt hơn.

**Bài học rút ra khi so sánh trong nhóm:**
> Cùng corpus nhưng cách chia khác nhau làm thay đổi số lượng ứng viên, mức độ đầy đủ của mỗi chunk và khả năng một tài liệu dài chiếm nhiều vị trí top-k. `FixedSizeChunker` ổn định về kích thước nhưng dễ cắt ngang ý; `SentenceChunker` giữ câu nhưng không phù hợp với bảng; `RecursiveChunker` giữ đoạn tốt hơn nhưng sinh nhiều chunk nhỏ; `HeadingChunker` giữ cấu trúc mục nhưng việc lặp heading khiến nhiều chunk cùng chủ đề có điểm gần nhau. Kết quả cho thấy độ mạch lạc của chunk và chất lượng embedding đều ảnh hưởng trực tiếp đến retrieval.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ dùng một benchmark runner duy nhất và cùng MiniLM cho cả bốn chiến lược, đồng thời lưu corpus hash, số chunk theo file và kết quả top-3 để bảo đảm tái lập. Với `HeadingChunker`, nhóm sẽ bỏ các chunk chỉ có tiêu đề, giữ heading khi fallback và thêm xử lý riêng cho bảng/danh sách. Cuối cùng, nhóm sẽ thử giới hạn số chunk trên mỗi tài liệu hoặc reranking để tài liệu dài không chiếm toàn bộ top-k.

---

## Tự Đánh Giá (Phần Nhóm)

> Điểm dưới đây là tự đánh giá dựa trên minh chứng hiện có. Điểm chất lượng truy xuất lấy theo kết quả benchmark cao nhất đã ghi nhận, không cộng thêm điểm thiết kế chiến lược vào tiêu chí retrieval.

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | **10 / 10** — 10 tài liệu công khai, đủ provenance và metadata bắt buộc |
| Thiết kế chiến lược (Strategy Design) | **15 / 15** — có baseline, bốn chiến lược, custom chunker và phân tích giới hạn |
| Chất lượng truy xuất (Retrieval Quality) | **4 / 10** — kết quả cao nhất hiện tại là `RecursiveChunker + TF-IDF` đạt 4/10 |
| Thuyết trình (Demo) | **5 / 5** — đã có insight, failure case, A/B metadata và hướng cải tiến cụ thể |
| **Tổng phần nhóm** | **34 / 40** |
