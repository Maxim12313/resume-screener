from typing import List
import streamlit as st
from ui.chat import handle_chat
from ui.sidebar import handle_sidebar


st.title("Resume Screener Chat")

handle_chat()
handle_sidebar()
