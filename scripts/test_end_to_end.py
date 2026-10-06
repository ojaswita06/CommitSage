import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.processing.chunker import chunk_commit_document
from src.commitsage.processing.document_builder import build_commit_document
from src.commitsage.rag.citation_formatter import add_citations
from src.commitsage.retrieval.hybrid_retriever import HybridRetriever
from src.commitsage.retrieval.reranker import Reranker

from src.commitsage.rag.citations import group_evidence_by_commit
from src.commitsage.rag.prompt import build_rag_prompt
from src.commitsage.rag.generator import LLMGenerator
from src.commitsage.rag.validator import GroundingValidator


def load_documents():
    """
    Load repository commits, build commit documents,
    and split them into chunks.
    """

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

    return documents


def main():

    print("Initializing CommitSage...")
    print("-" * 70)

    print("\nLoading repository history...")

    documents = load_documents()

    print(
        f"Prepared {len(documents)} chunks."
    )


    print("\nInitializing hybrid retriever...")

    retriever = HybridRetriever(
        documents
    )


    query = input(
        "\nAsk CommitSage a question: "
    ).strip()

    if not query:

        print(
            "Question cannot be empty."
        )

        return


    print(
        "\nRetrieving relevant repository history..."
    )

    retrieved_documents = retriever.search(
        query,
        top_k=10
    )

    print(
        f"Retrieved {len(retrieved_documents)} candidates."
    )

    print(
        "\nReranking candidates..."
    )

    reranker = Reranker()

    reranked_documents = reranker.rerank(
        query,
        retrieved_documents,
        top_k=5
    )

    print(
        f"Selected {len(reranked_documents)} relevant chunks."
    )


    evidence = group_evidence_by_commit(
        reranked_documents
    )

    print(
        f"Grouped into {len(evidence)} "
        "commit-level evidence items."
    )

    print("\nRetrieved Evidence")
    print("=" * 70)

    for index, item in enumerate(
        evidence,
        start=1
    ):

        metadata = item["metadata"]

        print(
            f"\nEvidence {index}"
        )

        print(
            "-" * 70
        )

        print(
            f"Commit SHA: "
            f"{metadata.get('commit_sha')}"
        )

        print(
            f"Author: "
            f"{metadata.get('author')}"
        )

        print(
            f"Date: "
            f"{metadata.get('date')}"
        )

        print(
            f"Source: "
            f"{metadata.get('url')}"
        )

        print("\nContent:")

        print(
            item["content"][:1500]
        )


    prompt = build_rag_prompt(
        query=query,
        documents=evidence
    )


    print(
        "\nGenerating answer with local Qwen model..."
    )

    print(
        "-" * 70
    )

    generator = LLMGenerator()

    answer = generator.generate(
        prompt
    )

    print(
        "\nValidating answer grounding..."
    )

    validator = GroundingValidator()

    validation = validator.validate(
        answer=answer,
        documents=evidence
    )

    print(
        "\nCommitSage Answer"
    )

    print(
        "=" * 70
    )

    if validation["valid"]:

        cited_answer = add_citations(
            answer,
            evidence
        )

        print(cited_answer)

        print(
            "\nGrounding Validation: PASSED"
        )

    else:

        print(
            "The generated answer could not be fully "
            "verified against the retrieved evidence."
        )

        print(
            "\nGrounding Validation: FAILED"
        )

        print(
            "\nValidation Issues:"
        )

        for error in validation["errors"]:

            print(
                f"- {error}"
            )


    print(
        "\n" + "=" * 70
    )

    print(
        "CommitSage pipeline completed successfully."
    )


if __name__ == "__main__":
    main()