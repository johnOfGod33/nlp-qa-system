import streamlit as st

from prediction import predict
from utils import extract_text


def _questions_from_input(raw: str) -> list[str]:
    return [q.strip() for q in raw.split("?") if q.strip()]


def render():
    st.title("NLP Question Answering")
    st.caption(
        "Provide a context or upload a document, then ask one or more questions "
        "(separate them with ?)."
    )

    tab_text, tab_doc = st.tabs(["Paste Text", "Upload Document"])

    context = ""

    with tab_text:
        context_input = st.text_area(
            "Context / Passage",
            height=200,
            placeholder="Paste your context or passage here…",
        )
        if context_input:
            context = context_input

    with tab_doc:
        uploaded_file = st.file_uploader(
            "Upload a document",
            type=["pdf", "txt"],
            help="Supported formats: PDF, plain text (.txt)",
        )
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            context = extract_text(
                file_bytes, uploaded_file.type, filename=uploaded_file.name
            )
            with st.expander("Extracted text preview", expanded=False):
                st.text(context[:2000] + ("…" if len(context) > 2000 else ""))

    st.divider()

    question_input = st.text_area(
        "Your question(s)",
        height=140,
        placeholder="What is the name of the project? What is Koffi's job? …",
        help="Use ? between questions. A final ? is optional on the last one.",
    )

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        ask = st.button("Get Answer", type="primary", use_container_width=True)

    if ask:
        questions = _questions_from_input(question_input)
        if not context.strip():
            st.warning("Please provide a context first (paste text or upload a document).")
        elif not questions:
            st.warning("Please enter at least one question.")
        else:
            with st.spinner("Thinking..."):
                results = []
                for q in questions:
                    answer, score, was_truncated = predict(q, context)
                    results.append((q, answer, score, was_truncated))

            any_truncated = any(r[3] for r in results)
            if any_truncated:
                st.info(
                    "The document exceeded the model's token limit and was automatically truncated. "
                    "For best results, keep the relevant passage concise."
                )

            st.subheader("Answer" if len(results) == 1 else "Answers")
            for i, (q, answer, score, _) in enumerate(results, start=1):
                if len(results) > 1:
                    st.markdown(f"**Question {i}:** {q}?")
                score_pct = f"{score * 100:.1f}%"
                st.write(answer)
                st.caption(f"Confidence: {score_pct}")
                if len(results) > 1 and i < len(results):
                    st.divider()


if __name__ == "__main__":
    st.set_page_config(page_title="NLP Q&A System", page_icon="🔍", layout="centered")
    render()
