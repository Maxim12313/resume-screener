import json
import streamlit as st
from typing import List, Dict
from rag.queryMaker import QueryMaker


queryMaker = QueryMaker()


def render_top(top_k: List[Dict], relevant: List[Dict], key):
    # Store expanded state only if not already present

    with st.expander("Retrival Details", expanded=True):
        options1 = dict(
            {
                # f"ID {record['source_id']} | Score: {round(record['score'], 3)}": record
                f"ID {record['source_id']}": record
                for record in top_k
            }
        )

        options2 = dict(
            {
                # f"ID {record['source_id']} | Score: {round(record['score'], 3)}": record
                f"ID {record['source_id']}": record
                for record in relevant
            }
        )

        res = st.toggle("Relevant/All", key="c" + str(key))
        selected = None
        if res:
            selected = st.selectbox(
                "Select a retrieved resume:", list(options1.keys()), key="a" + str(key)
            )
        else:
            selected = st.selectbox(
                "Select a retrieved resume:", list(options2.keys()), key="b" + str(key)
            )

        record = options1[selected]  # options2 subset options1
        with st.container(height=400):
            st.markdown(record["resume"])


def dummy_respond():
    def gen():
        yield "\n[5]\n"

    return {
        "text": gen,
        "top_k": [
            {"resume": "hi", "score": 0.5, "source_id": 5},
        ],
    }


def respond(prompt):
    convo = st.session_state.messages[:-1]  # just not last which is curr
    prev_relevant = (
        convo[-1]["relevant"] if len(convo) and "relevant" in convo[-1] else []
    )

    convo = [{"role": record["role"], "content": record["content"]} for record in convo]
    return queryMaker.query(prompt, prev_relevant, convo)
    # return dummy_respond()


def chat_logic(prompt):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    res = respond(prompt)
    with st.chat_message("assistant"):
        text = st.write_stream(res["text"])

    key = len(st.session_state.messages)
    relevant_ids = set(json.loads(text.split("\n")[-2]))
    relevant = [
        record for record in res["top_k"] if record["source_id"] in relevant_ids
    ]
    render_top(res["top_k"], relevant, key)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": text,
            "top_k": res["top_k"],
            "key": key,
            "relevant": relevant,
        }
    )


def render_chat():
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                render_top(msg["top_k"], msg["relevant"], i)


# use this component
def handle_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    render_chat()

    if prompt := st.chat_input("Try me!"):
        chat_logic(prompt)
