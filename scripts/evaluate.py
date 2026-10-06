import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.processing.chunker import chunk_commit_document
from src.commitsage.processing.document_builder import build_commit_document

from src.commitsage.retrieval.hybrid_retriever import HybridRetriever
from src.commitsage.retrieval.reranker import Reranker

from src.commitsage.rag.citations import group_evidence_by_commit
from src.commitsage.rag.prompt import build_rag_prompt
from src.commitsage.rag.generator import LLMGenerator
from src.commitsage.rag.validator import GroundingValidator
from src.commitsage.rag.citation_formatter import add_citations


EVALUATION_FILE = "data/evaluation/evaluation_questions.json"


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


def load_questions():
    """
    Load evaluation questions.
    """

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    print("=" * 70)
    print("CommitSage Evaluation")
    print("=" * 70)

    print("\nLoading repository history...")

    documents = load_documents()

    print(
        f"Prepared {len(documents)} chunks."
    )

    print("\nInitializing retriever...")

    retriever = HybridRetriever(
        documents
    )

    print("\nInitializing reranker...")

    reranker = Reranker()

    print("\nInitializing generator...")

    generator = LLMGenerator()

    validator = GroundingValidator()

    questions = load_questions()

    retrieval_passed = 0
    grounding_passed = 0
    citation_passed = 0

    results = []

    print(
        f"\nRunning {len(questions)} evaluation cases..."
    )

    print("=" * 70)

    for index, test_case in enumerate(
        questions,
        start=1
    ):

        question_id = test_case["id"]
        question = test_case["question"]
        expected_commit = test_case["expected_commit"]

        print(
            f"\n[{question_id}] {question}"
        )

        retrieved_documents = retriever.search(
            question,
            top_k=10
        )

        reranked_documents = reranker.rerank(
            question,
            retrieved_documents,
            top_k=5
        )

        evidence = group_evidence_by_commit(
            reranked_documents
        )

        retrieved_commits = [
            item["metadata"].get("commit_sha")
            for item in evidence
        ]

        retrieval_ok = (
            expected_commit in retrieved_commits
        )

        if retrieval_ok:
            retrieval_passed += 1

        prompt = build_rag_prompt(
            query=question,
            documents=evidence
        )

        answer = generator.generate(
            prompt
        )

        validation = validator.validate(
            answer=answer,
            documents=evidence
        )

        grounding_ok = validation["valid"]

        if grounding_ok:
            grounding_passed += 1

        cited_answer = add_citations(
            answer,
            evidence
        )

        citation_ok = (
            "[E" in answer
            and "commit:" in cited_answer
        )

        if citation_ok:
            citation_passed += 1

        results.append(
            {
                "id": question_id,
                "question": question,
                "expected_commit": expected_commit,
                "retrieved_commits": retrieved_commits,
                "retrieval_pass": retrieval_ok,
                "grounding_pass": grounding_ok,
                "citation_pass": citation_ok,
                "answer": answer,
                "cited_answer": cited_answer,
                "validation_errors": validation["errors"],
            }
        )

        print(
            f"  Retrieval: "
            f"{'PASS' if retrieval_ok else 'FAIL'}"
        )

        print(
            f"  Grounding: "
            f"{'PASS' if grounding_ok else 'FAIL'}"
        )

        print(
            f"  Citation: "
            f"{'PASS' if citation_ok else 'FAIL'}"
        )

    total = len(questions)

    print("\n")
    print("=" * 70)
    print("Evaluation Summary")
    print("=" * 70)

    print(
        f"\nRetrieval Accuracy: "
        f"{retrieval_passed}/{total} "
        f"({retrieval_passed / total * 100:.1f}%)"
    )

    print(
        f"Grounding Pass Rate: "
        f"{grounding_passed}/{total} "
        f"({grounding_passed / total * 100:.1f}%)"
    )

    print(
        f"Citation Pass Rate: "
        f"{citation_passed}/{total} "
        f"({citation_passed / total * 100:.1f}%)"
    )

    output_file = (
        "data/evaluation/evaluation_results.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "total_questions": total,
                "retrieval_passed": retrieval_passed,
                "grounding_passed": grounding_passed,
                "citation_passed": citation_passed,
                "retrieval_accuracy":
                    retrieval_passed / total,
                "grounding_pass_rate":
                    grounding_passed / total,
                "citation_pass_rate":
                    citation_passed / total,
                "results": results,
            },
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nDetailed results saved to:"
        f"\n{output_file}"
    )

    print(
        "\nCommitSage evaluation completed."
    )


if __name__ == "__main__":
    main()