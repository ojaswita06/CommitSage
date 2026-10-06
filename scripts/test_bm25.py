import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.processing.chunker import chunk_commit_document
from src.commitsage.processing.document_builder import build_commit_document
from src.commitsage.retrieval.bm25_retriever import BM25Retriever


def main():
    input_file = RAW_DATA_DIR / "commits.json"

    with open(input_file, "r", encoding="utf-8") as file:
        commits = json.load(file)

    documents = []

    for commit in commits[:10]:
        document = build_commit_document(
            commit,
            repository="fastapi/fastapi"
        )

        chunks = chunk_commit_document(
            document,
            max_chars=3000
        )

        documents.extend(chunks)

    print(f"Prepared {len(documents)} chunks")

    retriever = BM25Retriever(documents)

    results = retriever.search(
        "dependency updates",
        top_k=5
    )

    print("\nBM25 Search Results")
    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("-" * 70)

        print(result["content"][:500])

        print("\nScore:")
        print(result["score"])

        print("\nMetadata:")
        print(f"Commit: {result['metadata']['commit_sha']}")
        print(f"Author: {result['metadata']['author']}")
        print(f"Date: {result['metadata']['date']}")


if __name__ == "__main__":
    main()