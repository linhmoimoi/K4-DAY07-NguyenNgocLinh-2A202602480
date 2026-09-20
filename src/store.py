from __future__ import annotations

from typing import Any, Callable

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    This lab deliberately uses an in-memory store.  The embedding_fn
    parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

    def _make_record(self, doc: Document) -> dict[str, Any]:
        metadata = dict(doc.metadata)
        metadata.setdefault("doc_id", doc.id.split("#", 1)[0])

        record = {
            "id": f"{doc.id}::{self._next_index}",
            "content": doc.content,
            "metadata": metadata,
            "embedding": self._embedding_fn(doc.content),
        }
        self._next_index += 1
        return record

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        if top_k <= 0 or not records:
            return []

        query_embedding = self._embedding_fn(query)
        scored: list[dict[str, Any]] = []
        for record in records:
            # Embeddings in this project are normalized, so dot product is
            # equivalent to cosine similarity and avoids extra work here.
            score = _dot(query_embedding, record["embedding"])
            result = {
                key: value
                for key, value in record.items()
                if key != "embedding"
            }
            result["metadata"] = dict(record["metadata"])
            result["score"] = score
            scored.append(result)

        scored.sort(key=lambda result: result["score"], reverse=True)
        return scored[:top_k]

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.

        Chunking happens outside the store.  Each Document supplied here is
        stored as one record.
        """
        for doc in docs:
            self._store.append(self._make_record(doc))

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        Compute the dot product of the query embedding against all stored
        embeddings and return the highest-scoring records.
        """
        return self._search_records(query, self._store, top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        First filter stored chunks by metadata_filter, then run similarity search.
        """
        if not metadata_filter:
            candidates = self._store
        else:
            candidates = [
                record
                for record in self._store
                if all(
                    self._metadata_matches(record["metadata"], key, expected_value)
                    for key, expected_value in metadata_filter.items()
                )
            ]
        return self._search_records(query, candidates, top_k)

    @staticmethod
    def _metadata_matches(metadata: dict[str, Any], key: str, expected_value: Any) -> bool:
        actual_value = metadata.get(key)
        if actual_value == expected_value:
            return True
        # A policy marked "both" applies to either audience-specific query.
        return (
            key == "audience"
            and isinstance(expected_value, str)
            and expected_value in {"buyer", "seller"}
            and actual_value == "both"
        )

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        original_size = len(self._store)
        self._store = [
            record
            for record in self._store
            if record["metadata"].get("doc_id") != doc_id
        ]
        return len(self._store) < original_size
