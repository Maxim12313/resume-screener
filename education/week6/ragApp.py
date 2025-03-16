import random
import time
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


st.title("Chat Bot")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def respond():
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ],
        stream=True,
    )
    return stream


if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = st.write_stream(respond())
        st.session_state.messages.append({"role": "assistant", "content": response})
