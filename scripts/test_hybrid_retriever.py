import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.processing.chunker import chunk_commit_document
from src.commitsage.processing.document_builder import build_commit_document

from src.commitsage.retrieval.hybrid_retriever import HybridRetriever
from src.commitsage.retrieval.reranker import Reranker

from src.commitsage.rag.citations import group_evidence_by_commit
from src.commitsage.rag.prompt import build_rag_prompt
from src.commitsage.rag.generator import LLMGenerator


def load_documents():
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

    print("Loading repository history...")

    documents = load_documents()

    print(f"Prepared {len(documents)} chunks")


    print("\nInitializing hybrid retriever...")

    retriever = HybridRetriever(documents)

    query = input(
        "\nAsk CommitSage a question: "
    ).strip()

    if not query:
        print("Question cannot be empty.")
        return

    print("\nRetrieving relevant repository history...")

    retrieved_documents = retriever.search(
        query,
        top_k=10
    )

    print(
        f"Retrieved {len(retrieved_documents)} candidates."
    )

    print("\nReranking candidates...")

    reranker = Reranker()

    reranked_documents = reranker.rerank(
        query,
        retrieved_documents,
        top_k=5
    )

    print(
        f"Selected {len(reranked_documents)} chunks."
    )

    evidence = group_evidence_by_commit(
        reranked_documents
    )

    print(
        f"Grouped into {len(evidence)} commit-level evidence items."
    )

    prompt = build_rag_prompt(
        query=query,
        documents=evidence
    )


    print("\nGenerating answer with local Qwen model...")
    print("-" * 70)

    generator = LLMGenerator()

    answer = generator.generate(prompt)


    print("\nCommitSage Answer")
    print("=" * 70)

    print(answer)

    print("\n" + "=" * 70)
    print("CommitSage pipeline completed successfully.")


if __name__ == "__main__":
    main()