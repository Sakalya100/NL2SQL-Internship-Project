import mysql.connector
import streamlit as st
import openai
from openai import OpenAI
from utils import *
import os
from streamlit_chat import message
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

st.title("Natural Language to SQL Chatbot")
model="gpt-3.5-turbo"

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            responses = get_chatgpt_response(conversation_string,query)
            # st.write(responses)
        st.session_state.requests.append(query)
        st.session_state.responses.append(responses["Result"]) 
        with st.expander("Show Messages"):
            st.write(conversation_string)
with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
        