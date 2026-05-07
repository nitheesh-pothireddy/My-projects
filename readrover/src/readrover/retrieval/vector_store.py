"""Thin Chroma wrapper.

We isolate Chroma access here so we can swap it (pgvector, FAISS, Qdrant) later
without touching agent code.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import chromadb
from chromadb.utils import embedding_functions

from readrover.config import settings

if TYPE_CHECKING:
    from readrover.graph import Chunk


class VectorStore:
    """Per-question Chroma collection backed by sentence-transformers embeddings."""

    def __init__(self, collection: str) -> None:
        self._client = chromadb.PersistentClient(path=settings.chroma_path)
        self._embed = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )
        self._collection = self._client.get_or_create_collection(
            name=str(collection),
            embedding_function=self._embed,
            metadata={"hnsw:space": "cosine"},
        )

    # -- writes --

    def add_chunks(self, chunks: list["Chunk"]) -> None:
        """Embed and store chunks. Skips empty inputs."""
        if not chunks:
            return
        ids = [f"{c.paper_id}::{i}" for i, c in enumerate(chunks)]
        documents = [c.text for c in chunks]
        metadatas = [{"paper_id": c.paper_id, "page": c.page or -1} for c in chunks]
        self._collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    # -- reads --

    def query(self, text: str, k: int = 8) -> list[dict]:
        """Return top-k chunks (text + metadata) for a query string."""
        result = self._collection.query(query_texts=[text], n_results=k)
        return [
            {"id": _id, "text": _doc, "metadata": _meta}
            for _id, _doc, _meta in zip(
                result["ids"][0],
                result["documents"][0],
                result["metadatas"][0],
                strict=True,
            )
        ]
