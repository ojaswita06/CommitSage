from typing import Any

from rank_bm25 import BM25Okapi


class BM25Retriever:
    """
    Keyword-based retrieval using BM25.
    """

    def __init__(
        self,
        documents: list[dict[str, Any]]
    ):
        self.documents = documents

        tokenized_documents = [
            document["content"].lower().split()
            for document in documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[dict[str, Any]]:
        """
        Retrieve documents using keyword matching.
        """

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indices[:top_k]:
            results.append({
                "content": self.documents[index]["content"],
                "metadata": self.documents[index]["metadata"],
                "score": float(scores[index]),
            })

        return results