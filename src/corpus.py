"""Load the Shopee policy corpus stored under the project's data directory."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .chunking import RecursiveChunker
from .models import Document


PROJECT_ROOT = Path(__file__).resolve().parent.parent
POLICY_DIRECTORY_NAME = "chinh-sach-tmdt"
REQUIRED_POLICY_METADATA = {
    "doc_id",
    "source_url",
    "retrieved_at",
    "document_version",
    "audience",
}
VALID_AUDIENCES = {"buyer", "seller", "both"}
FRONT_MATTER_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$")


def _policy_directory(data_dir: str | Path | None = None) -> Path:
    """Find the policy directory in either supported project data layout."""
    if data_dir is None:
        roots = [PROJECT_ROOT / "data", PROJECT_ROOT / "data" / "data"]
    else:
        supplied = Path(data_dir).expanduser()
        if not supplied.is_absolute():
            supplied = PROJECT_ROOT / supplied
        roots = [supplied]

    candidates: list[Path] = []
    for root in roots:
        if root.name == POLICY_DIRECTORY_NAME:
            candidates.append(root)
        candidates.extend(
            [root / POLICY_DIRECTORY_NAME, root / "data" / POLICY_DIRECTORY_NAME]
        )

    for candidate in candidates:
        if candidate.is_dir() and any(candidate.glob("*.md")):
            return candidate

    checked = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Could not find a policy corpus directory. Checked: {checked}")


def _parse_front_matter(text: str, source: Path) -> tuple[dict[str, str], str]:
    """Read the simple key/value YAML front matter used by this corpus."""
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Markdown file is missing YAML front matter: {source}")

    try:
        closing_index = next(
            index for index in range(1, len(lines)) if lines[index].strip() == "---"
        )
    except StopIteration as error:
        raise ValueError(f"Unclosed YAML front matter in {source}") from error

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:closing_index], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = FRONT_MATTER_LINE.match(line)
        if not match:
            raise ValueError(f"Invalid front matter at {source}:{line_number}")
        key, raw_value = match.groups()
        value: Any = raw_value
        if raw_value.startswith('"'):
            try:
                value = json.loads(raw_value)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid quoted metadata at {source}:{line_number}") from error
        elif raw_value.startswith("'") and raw_value.endswith("'"):
            value = raw_value[1:-1].replace("''", "'")
        metadata[key] = str(value).strip()

    content = "\n".join(lines[closing_index + 1 :]).strip()
    return metadata, content


def load_policy_documents(data_dir: str | Path | None = None) -> list[Document]:
    """Load policy Markdown files and preserve their front matter as metadata.

    ``data_dir`` may be the policy directory itself, the project ``data``
    directory, or the nested ``data/data`` directory. If omitted, the project
    data folders are searched automatically.
    """
    policy_dir = _policy_directory(data_dir)
    documents: list[Document] = []
    seen_document_ids: set[str] = set()

    for path in sorted(policy_dir.glob("*.md")):
        metadata, content = _parse_front_matter(path.read_text(encoding="utf-8-sig"), path)
        missing = {
            key for key in REQUIRED_POLICY_METADATA if not metadata.get(key, "").strip()
        }
        if missing:
            raise ValueError(f"{path} is missing metadata: {', '.join(sorted(missing))}")
        if metadata["audience"] not in VALID_AUDIENCES:
            raise ValueError(
                f"Invalid audience {metadata['audience']!r} in {path}; "
                f"expected one of {', '.join(sorted(VALID_AUDIENCES))}"
            )
        if not content:
            raise ValueError(f"Policy document is empty: {path}")
        if metadata["doc_id"] in seen_document_ids:
            raise ValueError(f"Duplicate doc_id {metadata['doc_id']!r} in {path}")
        seen_document_ids.add(metadata["doc_id"])

        try:
            source = path.relative_to(PROJECT_ROOT).as_posix()
        except ValueError:
            source = path.as_posix()
        metadata["source"] = source
        metadata["extension"] = path.suffix.lower()
        documents.append(Document(id=metadata["doc_id"], content=content, metadata=metadata))

    if not documents:
        raise FileNotFoundError(f"No Markdown policy documents found in {policy_dir}")
    return documents


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunker: RecursiveChunker | None = None,
) -> list[Document]:
    """Split documents while carrying source and audience metadata to each chunk."""
    splitter = chunker or RecursiveChunker(chunk_size=chunk_size)
    chunked_documents: list[Document] = []

    for document in documents:
        chunks = splitter.chunk(document.content)
        for index, content in enumerate(chunks, start=1):
            metadata = dict(document.metadata)
            metadata["chunk_index"] = index
            metadata["chunk_count"] = len(chunks)
            chunked_documents.append(
                Document(
                    id=f"{document.id}#chunk-{index:04d}",
                    content=content,
                    metadata=metadata,
                )
            )
    return chunked_documents
