from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

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
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)