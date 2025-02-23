import io
import pdfplumber
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
from parser import get_details, get_resume_sections, read_pdf

st.title("thing")
st.title("resume screener")

file = st.file_uploader("Upload PDF Resume", type="pdf")
if file:
    file_value = file.getvalue()
    pdf_viewer(file_value)
    with io.BytesIO(file_value) as f:
        text = read_pdf(f)
        st.write(text)
