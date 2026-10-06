from typing import Any

from src.commitsage.retrieval.bm25_retriever import BM25Retriever
from src.commitsage.retrieval.vector_store import VectorStore


class HybridRetriever:
    """
    Combines semantic vector retrieval with BM25 keyword retrieval.
    """

    def __init__(
        self,
        documents: list[dict[str, Any]]
    ):
        self.documents = documents

        self.bm25_retriever = BM25Retriever(
            documents
        )

        self.vector_store = VectorStore()

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[dict[str, Any]]:
        """
        Retrieve documents using both semantic and
        keyword-based retrieval, then combine their rankings.
        """

        vector_results = self.vector_store.search(
            query,
            top_k=top_k
        )

        bm25_results = self.bm25_retriever.search(
            query,
            top_k=top_k
        )

        scores = {}

        documents_by_id = {}

        # Process semantic results
        for rank, document in enumerate(
            vector_results["documents"][0]
        ):
            metadata = vector_results["metadatas"][0][rank]

            document_id = (
                f"{metadata['commit_sha']}_"
                f"{metadata['chunk_index']}"
            )

            documents_by_id[document_id] = {
                "content": document,
                "metadata": metadata,
            }

            scores.setdefault(document_id, 0.0)

            # Reciprocal Rank Fusion
            scores[document_id] += 1 / (60 + rank + 1)

        # Process BM25 results
        for rank, document in enumerate(bm25_results):

            metadata = document["metadata"]

            document_id = (
                f"{metadata['commit_sha']}_"
                f"{metadata['chunk_index']}"
            )

            documents_by_id[document_id] = {
                "content": document["content"],
                "metadata": metadata,
            }

            scores.setdefault(document_id, 0.0)

            scores[document_id] += 1 / (60 + rank + 1)

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True
        )

        results = []

        for document_id in ranked_ids[:top_k]:

            result = documents_by_id[document_id].copy()

            result["hybrid_score"] = scores[
                document_id
            ]

            results.append(result)

        return results