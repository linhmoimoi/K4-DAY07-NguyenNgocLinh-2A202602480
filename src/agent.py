from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.store.search(question, top_k=top_k)
        if not results:
            return "Không tìm thấy thông tin liên quan trong knowledge base."

        context_blocks: list[str] = []
        for index, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})
            source = (
                metadata.get("source_url")
                or metadata.get("source")
                or metadata.get("doc_id")
                or result.get("id", "unknown")
            )
            context_blocks.append(
                f"[{index}] source={source} score={result.get('score', 0.0):.4f}\n"
                f"{result.get('content', '')}"
            )

        prompt = (
            "Bạn là trợ lý hỏi đáp dựa trên tài liệu. "
            "Chỉ sử dụng thông tin trong CONTEXT để trả lời câu hỏi. "
            "Nếu CONTEXT không đủ thông tin, hãy nói rõ là không tìm thấy "
            "thông tin trong tài liệu; không được tự suy đoán. "
            "Khi trả lời, hãy trích dẫn số nguồn tương ứng như [1], [2].\n\n"
            f"QUESTION:\n{question}\n\n"
            "CONTEXT:\n"
            + "\n\n".join(context_blocks)
            + "\n\nANSWER:"
        )
        return self.llm_fn(prompt)
