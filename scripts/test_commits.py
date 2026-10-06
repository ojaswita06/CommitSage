from src.commitsage.ingestion.github_loader import GitHubLoader


def main():
    loader = GitHubLoader()

    commits = loader.get_commits(
        "fastapi/fastapi",
        limit=3
    )

    print(f"Retrieved {len(commits)} commits")
    print("=" * 70)

    for i, commit in enumerate(commits, start=1):

        print(f"\nCommit {i}")
        print(f"SHA: {commit['sha']}")
        print(f"Author: {commit['author']}")
        print(f"Date: {commit['date']}")
        print(f"Message: {commit['message']}")
        print(f"URL: {commit['url']}")

        print("\nChanges:")
        print(f"Additions: {commit['total_additions']}")
        print(f"Deletions: {commit['total_deletions']}")

        print("\nChanged files:")

        for file in commit["files"]:
            print(f"  - {file['filename']}")
            print(f"    Status: {file['status']}")
            print(f"    Additions: {file['additions']}")
            print(f"    Deletions: {file['deletions']}")

            if file["patch"]:
                print("    Patch available: Yes")
            else:
                print("    Patch available: No")


if __name__ == "__main__":
    main()