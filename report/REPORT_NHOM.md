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

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| | FixedSizeChunker (`fixed_size`) | | | |
| | SentenceChunker (`by_sentences`) | | | |
| | RecursiveChunker (`recursive`) | | | |

### Chiến lược của từng thành viên

Mỗi thành viên thử một chiến lược riêng trên cùng corpus và cùng bộ 5 benchmark query.

**Đặng Văn Thái Anh**
- **Loại chiến lược:** `SentenceChunker` (`max_sentences_per_chunk=3`)
- **Mô tả & lý do chọn cho chủ đề này:** Gom ba câu hoàn chỉnh vào mỗi chunk để giữ mạch diễn đạt của các quy định và hướng dẫn Shopee. Cách này dễ đọc, nhưng độ dài chunk không đồng đều và một mục chính sách dài có thể bị tách khỏi tiêu đề.
- **Code snippet (nếu custom):** Không áp dụng — dùng `SentenceChunker` có sẵn.

**Nguyễn Lê Ngọc Bảo**
- **Loại chiến lược:** `FixedSizeChunker` (`chunk_size=500`, `overlap=50`)
- **Mô tả & lý do chọn cho chủ đề này:** Chia văn bản thành các chunk có kích thước ổn định, thuận tiện kiểm soát số lượng và so sánh retrieval. Overlap giúp giữ một phần ngữ cảnh ở ranh giới, nhưng chunk vẫn có thể cắt ngang câu hoặc tiêu đề.
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

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Đặng Văn Thái Anh | `SentenceChunker` (3 câu/chunk) | Chờ benchmark | Giữ ranh giới câu, chunk dễ đọc | Độ dài không đồng đều; có thể mất liên kết với heading |
| Nguyễn Lê Ngọc Bảo | `FixedSizeChunker` (500, overlap 50) | Chờ benchmark | Kích thước ổn định; overlap giữ ngữ cảnh ở biên | Có thể cắt ngang câu/mục; overlap tạo nội dung lặp |
| Lê Thị Châm Anh | `RecursiveChunker` (500) | Chờ benchmark | Ưu tiên tách theo đoạn/dòng trước khi cắt nhỏ | Không nhất thiết giữ nguyên ranh giới heading/section |
| Nguyễn Ngọc Linh | Custom `HeadingChunker` (heading + recursive fallback) | Chờ benchmark | Giữ tiêu đề/mục chính sách trong ngữ cảnh | Chunk có thể dài/ngắn khác nhau; section dài cần chia tiếp |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> *Viết 2-3 câu — đây là phần được đánh giá cao nhất (khả năng suy nghĩ & giải thích):*

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

*Vị trí hiện ghi theo tài liệu và tiêu đề mục; bổ sung ID chunk sau khi chốt cấu hình chia chunk dùng cho benchmark.*

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> *Viết 2-3 câu:*

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> *Liệt kê 2-3 ý:*

**Bài học rút ra khi so sánh trong nhóm:**
> *Viết 2-3 câu — cùng tài liệu nhưng chiến lược khác nhau dẫn tới khác biệt gì?*

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | / 10 |
| Thiết kế chiến lược (Strategy Design) | / 15 |
| Chất lượng truy xuất (Retrieval Quality) | / 10 |
| Thuyết trình (Demo) | / 5 |
| **Tổng phần nhóm** | **/ 40** |
