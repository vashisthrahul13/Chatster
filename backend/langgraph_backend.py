from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition

from tools.basic_tools import search_tool,calculator,get_stock_price
from tools.sql_db import query_db
# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_core.tools import tool

import requests
from dotenv import load_dotenv
import sqlite3

import os
import sys

#-------0. Add directory to path and load env variables-------
# Go one step back to the base folder
base_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..",'..'))

# Construct the .env path
env_path = os.path.join(base_dir, ".env")

load_dotenv(env_path)

#------1.LLM---------------------
llm = ChatOpenAI(model='gpt-4.1-mini-2025-04-14')

#------2.Tools---------------------
tools = [search_tool,calculator,get_stock_price,query_db]

# Bind LLM and Tools
llm_wtih_tools = llm.bind_tools(tools)


# -------3. State---------------------------
class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

# ---------4. Nodes -----------------------------
def chat_node(state : ChatState):
    messages = state['messages']
    response = llm_wtih_tools.invoke(messages)

    return {'messages':[response]}

tool_node = ToolNode(tools=tools)

#------------ 5. Checkpointer ---------------------
db_path = os.path.join(base_dir, "data", "chatbot.db")
conn = sqlite3.connect(database = db_path, check_same_thread=False)	#create sqlite database
checkpointer = SqliteSaver(conn= conn)

#--------------6. Graph ---------------------------
graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)

graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot = graph.compile(checkpointer=checkpointer)


# ---------7. Helper function to get all threads and sent to frontend --------------
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):	#fetches checkpoint for all threads
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)