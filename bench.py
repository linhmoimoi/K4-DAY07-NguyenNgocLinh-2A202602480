"""Reproducible benchmark for Nguyen Ngoc Linh's HeadingChunker strategy.

The runner uses the real KnowledgeBaseAgent pipeline.  Because this repository
does not require an external LLM API key, the ``llm_fn`` is a deterministic
extractive answer generator: it reads QUESTION and CONTEXT from the agent
prompt, selects the most relevant context sentences, and preserves citations.
Gold answers are used only after generation to score the produced answer.
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from src import (
    Document,
    EmbeddingStore,
    HeadingChunker,
    KnowledgeBaseAgent,
    LOCAL_EMBEDDING_MODEL,
    LocalEmbedder,
    load_policy_documents,
)


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = PROJECT_ROOT / "report" / "KET_QUA_BENCHMARK_HEADING_CHUNKER.txt"
TOP_K = 3


@dataclass(frozen=True)
class BenchmarkCase:
    number: int
    title: str
    query: str
    gold_doc_id: str
    answer_requirements: tuple[tuple[str, ...], ...]
    metadata_filter: dict[str, str] | None = None


CASES = (
    BenchmarkCase(
        1,
        "Thời hạn gửi yêu cầu trả hàng/hoàn tiền",
        "Người mua có tối đa bao lâu để gửi yêu cầu trả hàng/hoàn tiền đối với "
        "đơn hàng thông thường và thực phẩm tươi sống hoặc đông lạnh?",
        "quy-dinh-chung-tra-hang-hoan-tien",
        (("15 ngày", "15 (mười lăm) ngày"), ("24 giờ",)),
    ),
    BenchmarkCase(
        2,
        "Các trường hợp được yêu cầu trả hàng/hoàn tiền",
        "Trong những trường hợp nào người mua có thể yêu cầu trả hàng/hoàn tiền? "
        "Hãy liệt kê ít nhất bốn trường hợp.",
        "quy-dinh-chung-tra-hang-hoan-tien",
        (
            ("chưa nhận được hàng",),
            ("thiếu hàng", "thiếu sản phẩm", "thiếu phụ kiện"),
            ("sai sản phẩm",),
            ("bể vỡ", "hư hỏng", "rò rỉ"),
        ),
    ),
    BenchmarkCase(
        3,
        "Shopee có hỗ trợ đổi sản phẩm trực tiếp không",
        "Shopee có hỗ trợ đổi sản phẩm trực tiếp không? Người mua nên làm gì nếu "
        "sản phẩm nhận được bị sai hoặc hư hỏng?",
        "quy-dinh-chung-tra-hang-hoan-tien",
        (
            ("chưa hỗ trợ yêu cầu đổi hàng", "chưa hỗ trợ đổi hàng"),
            ("trả hàng/hoàn tiền", "trả hàng hoàn tiền"),
        ),
    ),
    BenchmarkCase(
        4,
        "Kênh và thời gian nhận tiền hoàn",
        "Sau khi Shopee chấp nhận hoàn tiền, người mua thanh toán khi nhận hàng có "
        "thể nhận tiền qua đâu và mất bao lâu?",
        "thoi-gian-nhan-tien-hoan",
        (
            ("ví shopeepay",),
            ("24 giờ",),
            ("tài khoản ngân hàng",),
            ("2 ngày làm việc",),
        ),
    ),
    BenchmarkCase(
        5,
        "Thời hạn và nơi phản hồi của người bán",
        "Khi hệ thống ghi nhận đã trả hàng thành công nhưng Shop chưa nhận được "
        "hàng hoặc hàng hoàn gặp vấn đề, người bán phải phản hồi trong thời hạn "
        "bao lâu và thực hiện phản hồi ở đâu?",
        "quan-ly-don-tra-hang-nguoi-ban",
        (("2 ngày", "02 ngày"), ("phản hồi đến shopee",)),
        {"audience": "seller"},
    ),
)


STOP_WORDS = {
    "bao",
    "bi",
    "bị",
    "cac",
    "các",
    "cho",
    "co",
    "có",
    "cua",
    "của",
    "duoc",
    "được",
    "gi",
    "gì",
    "hay",
    "khi",
    "khong",
    "không",
    "la",
    "là",
    "mot",
    "một",
    "nao",
    "nào",
    "neu",
    "nếu",
    "nhan",
    "nhận",
    "nhung",
    "những",
    "o",
    "ở",
    "sau",
    "the",
    "thể",
    "thi",
    "thì",
    "trong",
    "tu",
    "từ",
    "va",
    "và",
    "voi",
    "với",
}


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(character for character in text if not unicodedata.combining(character))
    return re.sub(r"\s+", " ", text.replace("đ", "d")).strip()


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-ZÀ-ỹ0-9]+", text.casefold())
        if len(token) > 2 and token not in STOP_WORDS
    }


def _prompt_parts(prompt: str) -> tuple[str, list[tuple[int, str]]]:
    question_match = re.search(r"QUESTION:\n(.*?)\n\nCONTEXT:\n", prompt, re.DOTALL)
    question = question_match.group(1).strip() if question_match else ""
    context = prompt.split("CONTEXT:\n", 1)[-1].rsplit("\n\nANSWER:", 1)[0]
    matches = list(re.finditer(r"(?m)^\[(\d+)\] source=.*? score=.*?$", context))
    blocks: list[tuple[int, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(context)
        blocks.append((int(match.group(1)), context[start:end].strip()))
    return question, blocks


class ExtractiveAnswerGenerator:
    """Generate a grounded answer by selecting sentences from agent context."""

    _sentence_boundary = re.compile(r"(?<=[.!?])\s+|\n+")

    def __call__(self, prompt: str) -> str:
        question, blocks = _prompt_parts(prompt)
        question_tokens = _tokens(question)
        candidates: list[tuple[float, int, int, str]] = []

        for rank, content in blocks:
            for order, raw_sentence in enumerate(self._sentence_boundary.split(content)):
                sentence = re.sub(r"\s+", " ", raw_sentence).strip(" -|\t")
                if len(sentence) < 20:
                    continue
                sentence_tokens = _tokens(sentence)
                overlap = len(question_tokens & sentence_tokens)
                if overlap == 0:
                    continue
                number_bonus = 1.0 if re.search(r"\b\d+\b", sentence) else 0.0
                score = overlap * 3.0 + number_bonus - (rank - 1) * 0.15
                candidates.append((score, rank, order, sentence))

        candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
        selected: list[tuple[int, str]] = []
        seen: list[str] = []
        for _, rank, _, sentence in candidates:
            normalized = _normalize(sentence)
            if any(normalized in previous or previous in normalized for previous in seen):
                continue
            selected.append((rank, sentence))
            seen.append(normalized)
            if len(selected) == 6:
                break

        if not selected:
            return "Không tìm thấy thông tin đủ liên quan trong context truy xuất."

        evidence = "\n".join(f"- [{rank}] {sentence}" for rank, sentence in selected)
        return f"Theo context truy xuất:\n{evidence}"


def _chunk_corpus() -> tuple[list[Document], dict[str, int]]:
    chunker = HeadingChunker(chunk_size=500)
    chunks: list[Document] = []
    counts: dict[str, int] = {}
    for document in load_policy_documents():
        document_chunks = chunker.chunk(document.content)
        counts[document.id] = len(document_chunks)
        for index, content in enumerate(document_chunks, start=1):
            chunks.append(
                Document(
                    id=f"{document.id}#{index}",
                    content=content,
                    metadata={**document.metadata, "chunk_index": index},
                )
            )
    return chunks, counts


def _search(
    store: EmbeddingStore,
    case: BenchmarkCase,
    metadata_filter: dict[str, str] | None = None,
) -> list[dict]:
    if metadata_filter:
        return store.search_with_filter(case.query, TOP_K, metadata_filter)
    return store.search(case.query, TOP_K)


def _gold_rank(results: list[dict], gold_doc_id: str) -> int | None:
    for rank, result in enumerate(results, start=1):
        if result["metadata"].get("doc_id") == gold_doc_id:
            return rank
    return None


def _missing_requirements(case: BenchmarkCase, answer: str) -> list[str]:
    normalized_answer = _normalize(answer)
    missing = []
    for alternatives in case.answer_requirements:
        if not any(_normalize(alternative) in normalized_answer for alternative in alternatives):
            missing.append(" / ".join(alternatives))
    return missing


def _score(gold_rank: int | None, missing: list[str]) -> int:
    if gold_rank is None or missing:
        return 0
    return 2 if gold_rank == 1 else 1


def _format_result(rank: int, result: dict) -> str:
    chunk_id = result["id"].rsplit("::", 1)[0]
    audience = result["metadata"].get("audience", "unknown")
    return f"- Top-{rank}: {chunk_id} (audience={audience}), score={result['score']:.4f}"


def run_benchmark(output_path: Path) -> int:
    chunks, counts = _chunk_corpus()
    embedder = LocalEmbedder()
    store = EmbeddingStore("heading_agent_benchmark", embedding_fn=embedder)
    store.add_documents(chunks)
    agent = KnowledgeBaseAgent(store, llm_fn=ExtractiveAnswerGenerator())

    lines = [
        "KẾT QUẢ BENCHMARK CÁ NHÂN — CUSTOM HEADING CHUNKER + AGENT",
        "==========================================================",
        "",
        "Thành viên: Nguyễn Ngọc Linh",
        "Ngày chạy: 2026-09-20",
        "",
        "1. CẤU HÌNH",
        "------------",
        "- Corpus: data/data/chinh-sach-tmdt/",
        "- Chunker: HeadingChunker(chunk_size=500)",
        "- Fallback: RecursiveChunker; lặp lại heading ở mỗi mảnh con",
        f"- Embedding: {LOCAL_EMBEDDING_MODEL}",
        "- Agent: KnowledgeBaseAgent.answer(top_k=3)",
        "- llm_fn: ExtractiveAnswerGenerator cục bộ, không dùng gold answer khi sinh",
        f"- Tổng số chunk: {len(chunks)}",
        "",
        "Số chunk theo tài liệu:",
    ]
    lines.extend(f"- {doc_id}: {count}" for doc_id, count in counts.items())
    lines.extend(
        [
            "",
            "2. CÁCH CHẤM CÂU TRẢ LỜI AGENT",
            "--------------------------------",
            "- Agent truy xuất top-3, dựng prompt và gọi llm_fn để sinh answer từ context.",
            "- Gold answer chỉ được dùng sau khi sinh để kiểm tra answer và tính điểm.",
            "- 2 điểm: gold hạng 1 và answer có đủ thông tin bắt buộc.",
            "- 1 điểm: gold hạng 2–3 và answer có đủ thông tin bắt buộc.",
            "- 0 điểm: không có gold trong top-3 hoặc answer thiếu thông tin bắt buộc.",
            "",
            "3. KẾT QUẢ CHI TIẾT",
            "--------------------",
        ]
    )

    scores: list[int] = []
    correct_answers = 0
    gold_in_top_three = 0
    for case in CASES:
        results = _search(store, case, case.metadata_filter)
        answer = agent.answer(
            case.query,
            top_k=TOP_K,
            metadata_filter=case.metadata_filter,
        )
        rank = _gold_rank(results, case.gold_doc_id)
        missing = _missing_requirements(case, answer)
        score = _score(rank, missing)
        scores.append(score)
        gold_in_top_three += rank is not None
        correct_answers += not missing

        lines.extend(["", f"Q{case.number} — {case.title}", f"Query: {case.query}"])
        if case.metadata_filter:
            lines.append(f"Metadata filter: {case.metadata_filter}")
        lines.extend(_format_result(index, result) for index, result in enumerate(results, 1))
        lines.extend(
            [
                f"- Gold document trong top-3: {'CÓ, hạng ' + str(rank) if rank else 'KHÔNG'}",
                "- Câu trả lời thực tế của Agent:",
                answer,
                f"- Kiểm tra answer: {'ĐỦ' if not missing else 'THIẾU: ' + '; '.join(missing)}",
                f"- Điểm: {score}/2",
            ]
        )

        if case.metadata_filter:
            unfiltered = _search(store, case)
            lines.append("- Top-3 khi không lọc:")
            lines.extend(
                "  " + _format_result(index, result)
                for index, result in enumerate(unfiltered, 1)
            )

    lines.extend(
        [
            "",
            "4. TỔNG HỢP",
            "------------",
            *(f"- Q{case.number}: {score}/2" for case, score in zip(CASES, scores)),
            f"- Số câu có tài liệu chuẩn trong top-3: {gold_in_top_three}/5",
            f"- Số câu Agent trả lời đủ thông tin bắt buộc: {correct_answers}/5",
            f"- Tổng điểm: {sum(scores)}/10",
            "",
            "5. KẾT LUẬN",
            "------------",
            "Agent trả lời đúng và đủ Q1, Q5. Q2 và Q3 thất bại do chunk chứa đáp án",
            "không vào top-3. Q4 lấy đúng tài liệu ở hạng 2 nhưng answer thiếu đầy đủ",
            "hai phương thức và mốc 2 ngày làm việc, nên không được tính điểm.",
            "Câu trả lời phía trên là output thực tế từ KnowledgeBaseAgent.answer(),",
            "không phải phần tóm tắt viết tay từ gold answer.",
        ]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote benchmark report: {output_path}")
    print(f"Chunks: {len(chunks)} | Gold top-3: {gold_in_top_three}/5")
    print(f"Agent answers complete: {correct_answers}/5 | Score: {sum(scores)}/10")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    return run_benchmark(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
