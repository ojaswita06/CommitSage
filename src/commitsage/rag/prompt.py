from typing import Any


def build_rag_prompt(
    query: str,
    documents: list[dict[str, Any]]
) -> str:

    evidence_sections = []

    for index, document in enumerate(documents, start=1):

        metadata = document["metadata"]

        evidence_sections.append(
            f"""
[E{index}]

Commit SHA:
{metadata.get("commit_sha")}

Repository:
{metadata.get("repository")}

Author:
{metadata.get("author")}

Date:
{metadata.get("date")}

Commit information:
{document["content"]}
"""
        )

    evidence = "\n".join(evidence_sections)

    prompt = f"""
You are CommitSage, a repository-history evidence summarizer.

USER QUESTION:
{query}

REPOSITORY EVIDENCE:
{evidence}

Your task is to summarize ONLY the changes explicitly shown
in the repository evidence.

STRICT RULES:

1. Use ONLY information explicitly present in the evidence.

2. Do not use outside knowledge.

3. Do not explain or interpret the changes.

4. Do not infer motivations or reasons.

5. Do not invent information.

6. Do not invent commit SHAs.

7. Do not invent PR numbers.

8. Do not invent file names.

9. Do not combine information between evidence items unless
   the evidence explicitly connects them.

10. Every statement must be associated with exactly one
    evidence identifier such as [E1], [E2], or [E3].

11. Use the evidence identifier that directly supports the statement.

12. If the evidence does not answer the question, say:

The available repository history does not provide enough
evidence to answer this question.

13. If the question asks why something changed and no explicit
reason is present, say:

The available repository history does not establish
the exact reason.

14. Keep the answer concise.

15. Use bullet points.

16. Do NOT write commit SHAs in your answer.

17. Do NOT write PR links in your answer.

18. Do NOT add a conclusion.

19. Do NOT ask a follow-up question.

20. Output ONLY the answer.

Example format:

[E1] Updated the release notes with a translation entry for tr.

[E2] Updated the release notes with a translation entry for hi.

FINAL ANSWER:
"""

    return prompt