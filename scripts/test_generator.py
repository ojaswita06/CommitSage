from src.commitsage.rag.generator import LLMGenerator
from src.commitsage.rag.prompt import build_rag_prompt


def main():
    generator = LLMGenerator()

    documents = [
        {
            "content": """
Repository: fastapi/fastapi

Commit message:
Updated dependency versions in the project configuration.

Changed files:
- pyproject.toml
- uv.lock

The dependency versions were updated to newer releases.
""",
            "metadata": {
                "repository": "fastapi/fastapi",
                "commit_sha": "example123",
                "author": "test-user",
                "date": "2026-10-05",
                "url": "https://github.com/fastapi/fastapi/commit/example123",
            },
        }
    ]

    query = "What changed in this commit?"

    prompt = build_rag_prompt(
        query=query,
        documents=documents,
    )

    print("Sending prompt to LLM...")
    print("-" * 70)

    answer = generator.generate(prompt)

    print("\nCommitSage Answer")
    print("=" * 70)
    print(answer)


if __name__ == "__main__":
    main()