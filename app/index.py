import streamlit as st
from v1 import render as render_v1

st.set_page_config(page_title="NLP Q&A System", page_icon="🔍", layout="centered")

render_v1()
