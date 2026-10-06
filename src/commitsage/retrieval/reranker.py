from typing import Any

from sentence_transformers import CrossEncoder

from src.commitsage.config import settings


class Reranker:
    """
    Reranks retrieved documents using a cross-encoder.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: list[dict[str, Any]],
        top_k: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Rerank documents according to their relevance to the query.
        """

        if not documents:
            return []

        pairs = [
            [query, document["content"]]
            for document in documents
        ]

        scores = self.model.predict(pairs)

        ranked_documents = []

        for document, score in zip(
            documents,
            scores
        ):
            result = document.copy()

            result["rerank_score"] = float(score)

            ranked_documents.append(result)

        ranked_documents.sort(
            key=lambda document: document["rerank_score"],
            reverse=True
        )

        if top_k is not None:
            ranked_documents = ranked_documents[:top_k]

        return ranked_documents