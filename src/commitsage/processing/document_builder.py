from typing import Any


def build_commit_document(
    commit: dict[str, Any],
    repository: str
) -> dict[str, Any]:
    """
    Convert a raw GitHub commit into a RAG-ready document.
    """

    lines = [
        f"Repository: {repository}",
        f"Commit SHA: {commit['sha']}",
        f"Author: {commit['author']}",
        f"Date: {commit['date']}",
        "",
        "Commit message:",
        commit["message"],
        "",
        "Changed files:",
    ]

    for file in commit["files"]:
        lines.extend([
            f"- {file['filename']}",
            f"  Status: {file['status']}",
            f"  Additions: {file['additions']}",
            f"  Deletions: {file['deletions']}",
        ])

        if file["patch"]:
            lines.extend([
                "  Patch:",
                file["patch"],
            ])

        lines.append("")

    lines.extend([
        f"Total additions: {commit['total_additions']}",
        f"Total deletions: {commit['total_deletions']}",
        "",
        f"Commit URL: {commit['url']}",
    ])

    content = "\n".join(lines)

    metadata = {
        "source_type": "commit",
        "repository": repository,
        "commit_sha": commit["sha"],
        "author": commit["author"],
        "date": commit["date"],
        "url": commit["url"],
    }

    return {
        "content": content,
        "metadata": metadata,
    }