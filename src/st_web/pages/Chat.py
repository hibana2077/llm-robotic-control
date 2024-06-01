import streamlit as st
import translators as ts
import requests
import os
import yaml
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from cus_obj import Action, Task, RoboticArmOperation

BACKEND_HOST = os.getenv("BACKEND_HOST", "localhost")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
TRANSLATOR_PROVIDER = os.getenv("TRANSLATOR_PROVIDER", "google")

st.title("Robot Control Chat")

def init_chat_history() -> ChatPromptTemplate:
    if 'chat_history' not in st.session_state:
        template = ChatPromptTemplate.from_messages([# Need to change the messages to guide LLM reactivity
            ('system', "You are an AI Assistant, helping the user to control a robotic arm."),
            ('system', "You can help the user to control the robotic arm to complete a task."),
        ])
        st.session_state['chat_history'] = template
    else:
        template = st.session_state['chat_history']
    return template

chat_tmp = init_chat_history()
llm = ChatOpenAI(model=OPENAI_MODEL)
user_input = st.chat_input("Say something")
chain = chat_tmp | llm | StrOutputParser()

if user_input:
    with st.status("Thinking..."):
        chat_tmp.append(HumanMessage(ts.translate_text(user_input, translator=TRANSLATOR_PROVIDER, to_language="en")))
        response = chain.invoke({})
        chat_tmp.append(AIMessage(response))
        st.session_state['chat_history'] = chat_tmp

if len(st.session_state['chat_history'].messages) == 1:
    st.html("<p align='center'><h3>Start a conversation with the AI Robot Control Assistant!</h3></p>")

for message in st.session_state['chat_history'].messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(ts.translate_text(message.content, translator=TRANSLATOR_PROVIDER, to_language="zh-TW"))
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(ts.translate_text(message.content, translator=TRANSLATOR_PROVIDER, to_language="zh-TW"))