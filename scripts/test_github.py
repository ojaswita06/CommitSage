from src.commitsage.ingestion.github_loader import GitHubLoader


def main():
    loader = GitHubLoader()

    repository = loader.get_repository_info("tiangolo/fastapi")

    print("GitHub connection successful!")
    print("-" * 50)

    for key, value in repository.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()