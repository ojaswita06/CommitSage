import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.processing.document_builder import build_commit_document
from src.commitsage.processing.chunker import chunk_commit_document


def main():
    input_file = RAW_DATA_DIR / "commits.json"

    with open(input_file, "r", encoding="utf-8") as file:
        commits = json.load(file)

    document = build_commit_document(
        commits[0],
        repository="fastapi/fastapi"
    )

    chunks = chunk_commit_document(
        document,
        max_chars=1000
    )

    print(f"Original document length: {len(document['content'])}")
    print(f"Number of chunks: {len(chunks)}")
    print("=" * 70)

    for i, chunk in enumerate(chunks):
        print(f"\nCHUNK {i}")
        print("-" * 70)
        print(chunk["content"])

        print("\nMetadata:")
        print(f"Commit SHA: {chunk['metadata']['commit_sha']}")
        print(f"Chunk index: {chunk['metadata']['chunk_index']}")
        print(f"Total chunks: {chunk['metadata']['total_chunks']}")


if __name__ == "__main__":
    main()