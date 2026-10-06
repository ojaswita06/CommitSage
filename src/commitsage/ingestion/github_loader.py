from github import Github
from github.Repository import Repository

from src.commitsage.config import settings


class GitHubLoader:
    """
    Handles communication with the GitHub API.
    """

    def __init__(self, token: str | None = None):
        self.token = token or settings.github_token

        if not self.token:
            raise ValueError(
                "GitHub token not found. "
                "Add GITHUB_TOKEN to your .env file."
            )

        self.github = Github(self.token)

    def get_repository(self, repository_name: str) -> Repository:
        """
        Load a GitHub repository.

        Example:
            repository_name = "tiangolo/fastapi"
        """

        return self.github.get_repo(repository_name)

    def get_repository_info(self, repository_name: str) -> dict:
        """
        Return basic repository information.
        """

        repo = self.get_repository(repository_name)

        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "url": repo.html_url,
            "default_branch": repo.default_branch,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language,
        }

    def get_commits(self, repository_name: str, limit: int = 100) -> list:
        """
        Retrieve detailed commits from a GitHub repository.
        """

        repo = self.get_repository(repository_name)

        commits = []

        for commit in repo.get_commits():

            changed_files = []

            for file in commit.files:
                changed_files.append({
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch,
                })

            commits.append({
                "sha": commit.sha,
                "message": commit.commit.message,
                "author": (
                    commit.author.login
                    if commit.author
                    else commit.commit.author.name
                ),
                "date": commit.commit.author.date.isoformat(),
                "url": commit.html_url,
                "files": changed_files,
                "total_additions": commit.stats.additions,
                "total_deletions": commit.stats.deletions,
            })

            if len(commits) >= limit:
                break

        return commits