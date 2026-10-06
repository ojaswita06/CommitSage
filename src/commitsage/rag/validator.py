import re
from typing import Any


class GroundingValidator:
    """
    Validates that generated answers reference only
    retrieved evidence items.
    """

    EVIDENCE_PATTERN = re.compile(r"\[E(\d+)\]")

    def validate(
        self,
        answer: str,
        documents: list[dict[str, Any]]
    ) -> dict[str, Any]:

        errors = []

        references = self.EVIDENCE_PATTERN.findall(answer)

        if not references:
            errors.append(
                "Answer does not contain any valid evidence references."
            )

            return {
                "valid": False,
                "errors": errors,
            }

        valid_ids = {
            str(index)
            for index in range(1, len(documents) + 1)
        }

        for reference in references:

            if reference not in valid_ids:

                errors.append(
                    f"Invalid evidence reference: [E{reference}]"
                )

        answer_lines = [
            line.strip()
            for line in answer.splitlines()
            if line.strip()
        ]

        for line in answer_lines:

            if line.startswith("[E"):

                if not self.EVIDENCE_PATTERN.search(line):

                    errors.append(
                        f"Claim has no valid evidence reference: {line}"
                    )

            elif line.startswith("-") or line.startswith("*"):

                if not self.EVIDENCE_PATTERN.search(line):

                    errors.append(
                        f"Bullet point has no evidence reference: {line}"
                    )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }