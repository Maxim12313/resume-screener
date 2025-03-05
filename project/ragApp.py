import time
import streamlit as st
from dotenv import load_dotenv
from queryMaker import QueryMaker

st.title("Chat Bot")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

queryMaker = QueryMaker()


def respond(prompt):
    return queryMaker.query(prompt)


if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        res = respond(prompt)
        text = st.write_stream(res["text"])
        st.session_state.messages.append({"role": "assistant", "content": text})
