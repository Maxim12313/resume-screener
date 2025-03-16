import io
import pandas as pd
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
from analysis.parser import get_details, get_resume_sections, read_pdf
from analysis.knn import ResumeKNN

st.title("resume screener")


def write_table(df, title):
    st.title(title)
    df = df.style.set_properties(**{"white-space": "pre-wrap"})
    st.table(df)


def details_table(details):
    df = pd.DataFrame.from_dict(details, orient="index", columns=["value"])
    write_table(df, "details")


def sections_table(sections):
    sections = {key: "\n".join(sections[key]) for key in sections.keys()}
    df = pd.DataFrame.from_dict(sections, orient="index", columns=["value"])
    write_table(df, "sections")


def knn_results(sections):
    knn = ResumeKNN()
    labels = knn.get_categories()

    excluded = set(["education", "phone", "email", "name", "gpa"])

    text = ""
    for key in sections:
        if key in excluded:
            continue
        text += "".join(x for x in sections[key])

    pred = knn.predict(text)[0]
    st.write(f"Your skill is best suited to {pred}")

    pred_prob = knn.predict_proba(text)[0]
    probs = [(labels[i], pred_prob[i]) for i in range(len(labels))]
    table = pd.DataFrame(probs, columns=["Occupation", "Probability"])
    table.sort_values("Probability", inplace=True, ascending=False)
    table.reset_index(inplace=True, drop=True)
    st.table(table)


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
        knn_results(resume_sections)
