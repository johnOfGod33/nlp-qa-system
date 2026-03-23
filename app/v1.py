import streamlit as st

from prediction import predict
from utils import extract_text

def render():
    st.title("NLP Question Answering")
    st.caption("Provide a context or upload a document, then ask a question.")

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
            "Upload a PDF document",
            type=["pdf"],
            help="Supported format: PDF only",
        )
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            context = extract_text(file_bytes, uploaded_file.type)
            with st.expander("Extracted text preview", expanded=False):
                st.text(context[:2000] + ("…" if len(context) > 2000 else ""))

    st.divider()

    question = st.text_input(
        "Your Question",
        placeholder="What would you like to know about the context?",
    )

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        ask = st.button("Get Answer", type="primary", use_container_width=True)

    if ask:
        if not context.strip():
            st.warning("Please provide a context first (paste text or upload a document).")
        elif not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                answer, score, was_truncated = predict(question, context)

            if was_truncated:
                st.info(
                    "The document exceeded the model's token limit and was automatically truncated. "
                    "For best results, keep the relevant passage concise."
                )

            score_pct = f"{score * 100:.1f}%"
            st.subheader("Answer")
            st.write(answer)
            st.caption(f"Confidence: {score_pct}")


if __name__ == "__main__":
    st.set_page_config(page_title="NLP Q&A System", page_icon="🔍", layout="centered")
    render()
