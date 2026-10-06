from typing import Any


def group_evidence_by_commit(
    documents: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Group multiple chunks belonging to the same commit
    into a single evidence item.
    """

    grouped = {}

    for document in documents:

        metadata = document["metadata"]
        commit_sha = metadata["commit_sha"]

        if commit_sha not in grouped:

            grouped[commit_sha] = {
                "content": [],
                "metadata": metadata,
            }

        grouped[commit_sha]["content"].append(
            document["content"]
        )

    results = []

    for commit_sha, evidence in grouped.items():

        results.append({
            "content": "\n\n".join(
                evidence["content"]
            ),
            "metadata": evidence["metadata"],
        })

    return results