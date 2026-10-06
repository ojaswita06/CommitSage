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


class CommitSagePipeline:
    """
    End-to-end CommitSage RAG pipeline.
    """

    def __init__(self):

        self.documents = self._load_documents()

        self.retriever = HybridRetriever(
            self.documents
        )

        self.reranker = Reranker()

        self.generator = LLMGenerator()

        self.validator = GroundingValidator()

    def _load_documents(self):
        """
        Load repository commits, build commit documents,
        and split them into chunks.
        """

        input_file = RAW_DATA_DIR / "commits.json"

        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as file:

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

    def answer_question(self, query: str):

        retrieved_documents = self.retriever.search(
            query,
            top_k=10
        )

        reranked_documents = self.reranker.rerank(
            query,
            retrieved_documents,
            top_k=5
        )

        evidence = group_evidence_by_commit(
            reranked_documents
        )

        prompt = build_rag_prompt(
            query=query,
            documents=evidence
        )

        answer = self.generator.generate(
            prompt
        )

        validation = self.validator.validate(
            answer=answer,
            documents=evidence
        )

        cited_answer = add_citations(
            answer,
            evidence
        )

        return {
            "answer": answer,
            "cited_answer": cited_answer,
            "evidence": evidence,
            "validation": validation,
        }