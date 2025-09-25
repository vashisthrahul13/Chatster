import streamlit as st
from backend.langgraph_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid


# **************************************** utility functions *************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def reset_chat():
    
    #generate new thread id
    thread_id = generate_thread_id()

    #add thread id to session state
    st.session_state['thread_id'] = thread_id

    #add the conversation thread_id to list of all thread ids
    add_thread(thread_id)

    #clear session chat history
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config = {'configurable':{'thread_id':thread_id}})

    return state.values.get('messages')


# ******************************Session Setup ***********************
#create conversation history in session_state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

#generate new thread_id for converstaion
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

#list to store all chat ids
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI *********************************
st.sidebar.title('Chatster')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.subheader('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:

    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        if messages is not None:
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    role='user'
                else:
                    role='assistant'
                temp_messages.append({'role': role, 'content': msg.content})

            st.session_state['message_history'] = temp_messages
        else:
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
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

     # first add the message to message_history
    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    # yield only assistant tokens
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})