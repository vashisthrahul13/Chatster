import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "thread-1"}}

user_input = st.chat_input("Type here")

if user_input:
    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)

    # render full conversation from LangGraph
    for msg in response["messages"]:
        role = "user" if msg.type == "human" else "assistant"
        with st.chat_message(role):
            st.text(msg.content)