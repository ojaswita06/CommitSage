# CommitSage

## GitHub Repository History Assistant

CommitSage is a Retrieval-Augmented Generation (RAG) system that helps developers understand GitHub repository history by answering questions about past commits using retrieved repository evidence.

Instead of relying only on an LLM's internal knowledge, CommitSage retrieves relevant commit history, reranks the results, and generates answers grounded in that evidence with deterministic commit-level citations.

---

## Problem

Understanding why code changed can require searching through many commits, commit messages, and large diffs.

Typical questions include:

* What changed in this commit?
* Which file was modified?
* Which translation was added?
* What repository does this commit belong to?
* What information is available about a particular change?

CommitSage provides a conversational interface for querying repository history while keeping the generated responses grounded in retrieved evidence.

---

## Features

* GitHub repository commit ingestion
* Commit-level document construction
* Document chunking for large commits
* Semantic retrieval using ChromaDB
* Keyword retrieval using BM25
* Hybrid retrieval using Reciprocal Rank Fusion
* Cross-encoder reranking
* Commit-level evidence grouping
* Local LLM generation using Ollama and Qwen 2.5 3B
* Grounding validation
* Deterministic commit citations
* Streamlit web interface
* Evaluation pipeline for retrieval, grounding, and citation accuracy

---

## Architecture

```text
GitHub Repository
       │
       ▼
GitHub API Ingestion
       │
       ▼
Commit Documents
       │
       ▼
Chunking
       │
       ├───────────────┐
       ▼               ▼
   ChromaDB           BM25
 Semantic Search   Keyword Search
       │               │
       └───────┬───────┘
               ▼
       Reciprocal Rank Fusion
               │
               ▼
       Cross-Encoder Reranker
               │
               ▼
       Commit-Level Evidence
               │
               ▼
        Grounded Prompt
               │
               ▼
          Qwen 2.5 3B
          via Ollama
               │
               ▼
       Grounding Validator
               │
               ▼
    Deterministic Citations
               │
               ▼
        Streamlit Interface
```

---

## Tech Stack

| Component         | Technology             |
| ----------------- | ---------------------- |
| Language          | Python                 |
| Repository Data   | GitHub API             |
| Vector Database   | ChromaDB               |
| Embeddings        | Sentence Transformers  |
| Keyword Retrieval | BM25                   |
| Hybrid Retrieval  | Reciprocal Rank Fusion |
| Reranking         | Cross-Encoder          |
| LLM               | Qwen 2.5 3B            |
| Local LLM Runtime | Ollama                 |
| Frontend          | Streamlit              |

---

## Project Structure

```text
CommitSage/
│
├── app.py
│
├── data/
│   ├── raw/
│   │   └── commits.json
│   └── evaluation/
│       └── evaluation_questions.json
│
├── scripts/
│   ├── ingest_repository.py
│   ├── evaluate.py
│   ├── test_end_to_end.py
│   ├── test_bm25.py
│   ├── test_chunker.py
│   ├── test_citations.py
│   ├── test_commits.py
│   ├── test_config.py
│   ├── test_document_builder.py
│   ├── test_generator.py
│   ├── test_github.py
│   ├── test_hybrid_retriever.py
│   ├── test_prompt.py
│   ├── test_reranker.py
│   └── test_vector_store.py
│
├── src/
│   └── commitsage/
│       ├── config.py
│       │
│       ├── ingestion/
│       │   └── github_loader.py
│       │
│       ├── processing/
│       │   ├── chunker.py
│       │   └── document_builder.py
│       │
│       ├── rag/
│       │   ├── citations.py
│       │   ├── citation_formatter.py
│       │   ├── generator.py
│       │   ├── pipeline.py
│       │   ├── prompt.py
│       │   └── validator.py
│       │
│       └── retrieval/
│           ├── bm25_retriever.py
│           ├── hybrid_retriever.py
│           ├── reranker.py
│           └── vector_store.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd CommitSage
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

CommitSage uses a loca
