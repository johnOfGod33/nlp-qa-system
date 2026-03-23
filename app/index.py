import streamlit as st
from v1 import render as render_v1


def render_v2_placeholder():
    st.title("NLP Q&A - V2")
    st.info("V2 page placeholder. Implement your new V2 UI here.")


st.set_page_config(page_title="NLP Q&A System", page_icon="🔍", layout="centered")

page = st.sidebar.radio("Pages", ["V1", "V2"], index=0)

if page == "V1":
    render_v1()
else:
    render_v2_placeholder()
