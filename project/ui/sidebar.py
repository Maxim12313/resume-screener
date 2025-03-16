import streamlit as st
from rag.database import retrieve_resumes


@st.dialog("_______", width="large")
def view_resume(id: int):
    resume = retrieve_resumes([id])
    st.subheader(f"ID {id}")
    # TODO: make use pdf_viewer and make better data set with pdf access for viewing
    st.markdown(resume[0])
    st.html("<span class='big-dialog'></span>")


def popup():
    length = 165
    options = ["none"] + [f"ID {val + 1}" for val in range(length)]
    selected = st.selectbox("Search", options)
    if selected != "none":
        # TODO: find better solution
        id = int(selected[3:])
        if id != st.session_state.viewing_id:
            view_resume(id)
            st.session_state.viewing_id = id


def handle_sidebar():
    if "viewing_id" not in st.session_state:
        st.session_state.viewing_id = 0

    # https://discuss.streamlit.io/t/how-to-set-width-of-st-dialog-as-a-fraction-of-the-pages-width/78068/4
    st.markdown(
        """
    <style>
    div[data-testid="stDialog"] div[role="dialog"]:has(.big-dialog) {
        width: 80vw;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.title("Resumes Viewer")
        popup()
