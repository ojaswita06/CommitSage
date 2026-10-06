import json

from src.commitsage.config import RAW_DATA_DIR
from src.commitsage.ingestion.github_loader import GitHubLoader


def main():
    repository_name = "fastapi/fastapi"

    print("Starting GitHub repository ingestion...")
    print(f"Repository: {repository_name}")

    loader = GitHubLoader()

    commits = loader.get_commits(
        repository_name,
        limit=100
    )

    output_file = RAW_DATA_DIR / "commits.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(commits, file, indent=2, ensure_ascii=False)

    print("-" * 60)
    print(f"Retrieved {len(commits)} commits")
    print(f"Saved to: {output_file}")
    print("Ingestion completed successfully!")


if __name__ == "__main__":
    main()