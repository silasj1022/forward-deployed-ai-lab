"""Optional vector-database adapters.

These classes are deliberately small: the reference runtime stays credential-free,
while the interfaces show how Chroma or Qdrant can replace BM25 without changing
the orchestrator.
"""

from __future__ import annotations

from typing import Any, cast


class ChromaVectorAdapter:
    def __init__(
        self, collection_name: str = "fdai_knowledge", persist_directory: str = ".chroma"
    ) -> None:
        import chromadb  # type: ignore[import-not-found]

        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(collection_name)

    def upsert(
        self, *, ids: list[str], documents: list[str], metadatas: list[dict[str, Any]]
    ) -> None:
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    def query(self, text: str, top_k: int = 3) -> dict[str, Any]:
        result = self.collection.query(query_texts=[text], n_results=top_k)
        return cast(dict[str, Any], result)


class QdrantVectorAdapter:
    def __init__(self, url: str, collection_name: str, api_key: str | None = None) -> None:
        from qdrant_client import QdrantClient  # type: ignore[import-not-found]

        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name
