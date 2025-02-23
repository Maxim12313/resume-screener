from streamlit_pdf_viewer import pdf_viewer
import streamlit as st

st.title("resume screener")

file = st.file_uploader("Upload PDF Resume", type="pdf")
if file:
    file_value = file.getvalue()
    pdf_viewer(file_value)
