import re
from typing import Any


def add_citations(
    answer: str,
    documents: list[dict[str, Any]]
) -> str:
    """
    Replace evidence references such as [E1] with
    deterministic commit citations.

    The LLM chooses the evidence ID.
    Python supplies the actual commit metadata.
    """

    evidence_map = {}

    for index, document in enumerate(
        documents,
        start=1
    ):

        metadata = document["metadata"]

        sha = metadata.get("commit_sha")
        repository = metadata.get(
            "repository",
            "fastapi/fastapi"
        )

        url = metadata.get("url")

        if not url and sha:
            url = (
                f"https://github.com/"
                f"{repository}/commit/{sha}"
            )

        evidence_map[f"E{index}"] = {
            "sha": sha,
            "url": url,
        }

    def replace_reference(match):

        evidence_id = match.group(1)

        evidence = evidence_map.get(
            f"E{evidence_id}"
        )

        if not evidence:
            return match.group(0)

        sha = evidence["sha"]
        url = evidence["url"]

        if not sha:
            return match.group(0)

        short_sha = sha[:7]

        if url:
            return (
                f"[E{evidence_id}] "
                f"(commit: {short_sha}, {url})"
            )

        return (
            f"[E{evidence_id}] "
            f"(commit: {short_sha})"
        )

    return re.sub(
        r"\[E(\d+)\]",
        replace_reference,
        answer
    )