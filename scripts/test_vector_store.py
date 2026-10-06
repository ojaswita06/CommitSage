import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.processing.chunker import chunk_commit_document
from src.commitsage.processing.document_builder import build_commit_document
from src.commitsage.retrieval.vector_store import VectorStore


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

    vector_store = VectorStore()

    vector_store.add_documents(documents)

    print("Documents successfully added to ChromaDB!")

    results = vector_store.search(
        "dependency updates",
        top_k=5
    )

    print("\nSearch results")
    print("=" * 70)

    for i, document in enumerate(
        results["documents"][0],
        start=1
    ):
        print(f"\nResult {i}")
        print("-" * 70)
        print(document[:500])

        metadata = results["metadatas"][0][i - 1]

        print("\nMetadata:")
        print(f"Commit: {metadata['commit_sha']}")
        print(f"Author: {metadata['author']}")
        print(f"Date: {metadata['date']}")


if __name__ == "__main__":
    main()