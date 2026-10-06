import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.processing.chunker import chunk_commit_document
from src.commitsage.processing.document_builder import build_commit_document
from src.commitsage.rag.citations import group_evidence_by_commit


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
            max_chars=1000
        )

        documents.extend(chunks)

    print(f"Original chunks: {len(documents)}")

    grouped = group_evidence_by_commit(
        documents
    )

    print(f"Grouped commits: {len(grouped)}")

    print("\nGrouped Evidence")
    print("=" * 70)

    for i, evidence in enumerate(
        grouped,
        start=1
    ):

        print(f"\nEvidence {i}")
        print("-" * 70)

        print(
            f"Commit: "
            f"{evidence['metadata']['commit_sha']}"
        )

        print(
            f"Content length: "
            f"{len(evidence['content'])}"
        )

        print(
            f"Author: "
            f"{evidence['metadata']['author']}"
        )


if __name__ == "__main__":
    main()