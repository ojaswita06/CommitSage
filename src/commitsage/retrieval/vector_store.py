from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

from src.commitsage.config import (
    VECTORSTORE_DIR,
    settings,
)


class VectorStore:
    """
    Handles embedding generation and storage in ChromaDB.
    """

    def __init__(self):
        self.embedding_model = SentenceTransformer(
            settings.embedding_model
        )

        self.client = chromadb.PersistentClient(
            path=str(VECTORSTORE_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name
        )

    def add_documents(
        self,
        documents: list[dict[str, Any]]
    ) -> None:
        """
        Generate embeddings and store documents in ChromaDB.
        """

        if not documents:
            return

        texts = [
            document["content"]
            for document in documents
        ]

        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True
        ).tolist()

        ids = [
            (
                f"{document['metadata']['commit_sha']}"
                f"_chunk_{document['metadata']['chunk_index']}"
            )
            for document in documents
        ]

        metadatas = [
            document["metadata"]
            for document in documents
        ]

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> dict:
        """
        Search ChromaDB using semantic similarity.
        """

        query_embedding = self.embedding_model.encode(
            [query]
        ).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
        )

        return results