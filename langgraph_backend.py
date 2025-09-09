from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

import os
import sys

#add directory to path
sys.path.append(os.path.dirname(p=os.path.abspath(__file__)))

load_dotenv('.env')

llm = ChatOpenAI(model='gpt-4.1-mini-2025-04-14')

class ChatState(TypedDict):
	messages : Annotated[list[BaseMessage],add_messages]


def chat_node(state : ChatState):
	messages = state['messages']
	response = llm.invoke(messages)

	return {'messages':[response]}

#checkpointer
conn = sqlite3.connect(database = 'chatbot.db', check_same_thread=False)	#create sqlite database
checkpointer = SqliteSaver(conn= conn)

#build graph
graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):	#fetches checkpoint for all threads
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)