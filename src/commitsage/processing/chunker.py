from typing import Any


def chunk_commit_document(
    document: dict[str, Any],
    max_chars: int = 3000
) -> list[dict[str, Any]]:
    """
    Split a commit document into meaningful chunks while
    preserving commit context and metadata.
    """

    content = document["content"]
    metadata = document["metadata"]

    if len(content) <= max_chars:
        return [
            {
                "content": content,
                "metadata": {
                    **metadata,
                    "chunk_index": 0,
                    "total_chunks": 1,
                },
            }
        ]

    lines = content.splitlines()

    # Keep the commit identity/context in every chunk.
    header_lines = []
    body_lines = []

    in_body = False

    for line in lines:
        if line.startswith("Changed files:"):
            in_body = True

        if in_body:
            body_lines.append(line)
        else:
            header_lines.append(line)

    header = "\n".join(header_lines)

    chunks = []
    current_lines = []
    current_length = len(header) + 2

    for line in body_lines:

        line_length = len(line) + 1

        if (
            current_lines
            and current_length + line_length > max_chars
        ):
            chunks.append(
                header
                + "\n\n"
                + "\n".join(current_lines)
            )

            current_lines = []
            current_length = len(header) + 2

        current_lines.append(line)
        current_length += line_length

    if current_lines:
        chunks.append(
            header
            + "\n\n"
            + "\n".join(current_lines)
        )

    total_chunks = len(chunks)

    return [
        {
            "content": chunk,
            "metadata": {
                **metadata,
                "chunk_index": index,
                "total_chunks": total_chunks,
            },
        }
        for index, chunk in enumerate(chunks)
    ]