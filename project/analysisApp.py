import io
import pandas as pd
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
from analysis.parser import get_details, get_resume_sections, read_pdf

st.title("resume screener")


def details_table(details):
    df = pd.DataFrame.from_dict(details, orient="index", columns=["value"])
    st.write(df)


def sections_table(sections):
    df = {key: "\n".join(sections[key]) for key in sections.keys()}
    df = df.style.set_properties(**{"white-space": "pre-wrap"})
    df = pd.DataFrame.from_dict(sections, orient="index", columns=["value"])
    st.table(df)


file = st.file_uploader("Upload PDF Resume", type="pdf")
if file:
    file_value = file.getvalue()
    pdf_viewer(file_value)
    with io.BytesIO(file_value) as f:
        text = read_pdf(f)
        details, text = get_details(text)
        details_table(details)
        resume_sections = get_resume_sections(text)
        sections_table(resume_sections)
