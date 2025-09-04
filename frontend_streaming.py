import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}


#create conversation history in session_state
if 'message_history' not in st.session_state:
	st.session_state['message_history'] = []


#load existing conversation history and display
for message in st.session_state['message_history']:
	with st.chat_message(name = message['role']):
		st.text(message['content'])


#get user input
user_input = st.chat_input('Type here')

if user_input:

	#add the message in message history and display
	st.session_state['message_history'].append({'role':'user','content':user_input})
	with st.chat_message(name = 'user'):
		st.text(user_input)

	#add ai response
	with st.chat_message(name='assistant'):

		ai_message = st.write_stream(message_chunk.content for message_chunk,metadata in chatbot.stream(input={'messages':[HumanMessage(content=user_input)]},
		config=CONFIG,
		stream_mode='messages'))

	st.session_state['message_history'].append({'role':'assistant','content':ai_message})