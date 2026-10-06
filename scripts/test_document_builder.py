import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.processing.document_builder import build_commit_document


def main():
    input_file = RAW_DATA_DIR / "commits.json"

    with open(input_file, "r", encoding="utf-8") as file:
        commits = json.load(file)

    document = build_commit_document(
        commits[0],
        repository="fastapi/fastapi"
    )

    print("Document created successfully!")
    print("=" * 70)

    print("\nCONTENT")
    print("-" * 70)
    print(document["content"])

    print("\nMETADATA")
    print("-" * 70)

    for key, value in document["metadata"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()