import re

import streamlit as st

from src.commitsage.rag.pipeline import CommitSagePipeline


st.set_page_config(
    page_title="CommitSage",
    page_icon="🔎",
    layout="wide",
)


@st.cache_resource
def load_pipeline():
    return CommitSagePipeline()


def format_answer(answer: str) -> str:
    answer = re.sub(
        r"\[E\d+\]\s*",
        "",
        answer,
    )

    answer = re.sub(
        r"\(commit:\s*[a-f0-9]{7},\s*https?://[^\s)]+\)",
        "",
        answer,
    )

    return answer.strip()


def extract_evidence_ids(answer: str) -> list[str]:
    return re.findall(
        r"\[E(\d+)\]",
        answer,
    )


st.title("CommitSage")

st.caption(
    "GitHub Repository History Assistant"
)

st.write(
    "Ask questions about repository history and get "
    "evidence-grounded answers with verifiable commit citations."
)

st.divider()


with st.spinner("Loading CommitSage..."):
    pipeline = load_pipeline()


query = st.text_input(
    "Ask a question",
    placeholder=(
        "What changed in commit "
        "c03a416427418c2e891aa62c28a4045d2fd29e14?"
    ),
)


if st.button(
    "Ask CommitSage",
    type="primary",
):

    if not query.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching repository history and generating answer..."
        ):

            result = pipeline.answer_question(
                query.strip()
            )

        answer = result["answer"]
        evidence = result["evidence"]
        validation = result["validation"]

        evidence_ids = extract_evidence_ids(answer)

        st.subheader("Answer")

        st.markdown(
            format_answer(answer)
        )

        if validation["valid"]:

            st.success(
                "Grounding validation passed."
            )

        else:

            st.warning(
                "The generated answer could not be "
                "fully verified against the retrieved evidence."
            )

        if evidence_ids:

            st.caption(
                "Evidence used: "
                + ", ".join(
                    f"E{evidence_id}"
                    for evidence_id in evidence_ids
                )
            )

        st.divider()

        st.subheader("Sources")

        shown_evidence = set()

        for evidence_id in evidence_ids:

            evidence_index = int(evidence_id) - 1

            if evidence_index < 0:
                continue

            if evidence_index >= len(evidence):
                continue

            if evidence_index in shown_evidence:
                continue

            shown_evidence.add(evidence_index)

            item = evidence[evidence_index]
            metadata = item["metadata"]

            commit_sha = metadata.get(
                "commit_sha",
                "",
            )

            repository = metadata.get(
                "repository",
                "fastapi/fastapi",
            )

            author = metadata.get(
                "author",
                "Unknown",
            )

            date = metadata.get(
                "date",
                "Unknown",
            )

            commit_url = (
                f"https://github.com/"
                f"{repository}/commit/"
                f"{commit_sha}"
            )

            content = item["content"]

            additions = len(
                re.findall(
                    r"^\+(?!\+\+)",
                    content,
                    re.MULTILINE,
                )
            )

            deletions = len(
                re.findall(
                    r"^-(?!--)",
                    content,
                    re.MULTILINE,
                )
            )

            commit_message = "Commit details"

            message_match = re.search(
                r"Commit message:\s*\n(.+)",
                content,
            )

            if message_match:
                commit_message = (
                    message_match.group(1).strip()
                )

            with st.container(border=True):

                st.markdown(
                    f"**E{evidence_id} · "
                    f"Commit `{commit_sha[:7]}`**"
                )

                st.caption(
                    f"Author: {author}  •  Date: {date}"
                )

                st.markdown(
                    f"**Commit message:** {commit_message}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Additions",
                        additions,
                    )

                with col2:
                    st.metric(
                        "Deletions",
                        deletions,
                    )

                with col3:
                    st.link_button(
                        "View commit",
                        commit_url,
                    )

                with st.expander(
                    "View full repository evidence"
                ):

                    st.code(
                        content,
                        language="text",
                    )


if not query.strip():
    st.info(
        "Example: Ask about a specific commit, "
        "file change, translation, or repository history."
    )