'''
Author: hibana2077 hibana2077@gmail.com
Date: 2024-05-08 14:05:18
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-06-07 13:27:08
FilePath: \llm-robotic-control\src\st_web\pages\Chat.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import streamlit as st
import requests
import json
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
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN", "sk-")

os.environ["OPENAI_API_KEY"] = OPENAI_TOKEN

st.title("Robot Control Chat")

def init_chat_history() -> ChatPromptTemplate:
    if 'chat_history' not in st.session_state:
        template = ChatPromptTemplate.from_messages([# Need to change the messages to guide LLM reactivity
            ('system', "You are an AI Assistant, helping the user control a robotic arm. The user will instruct you, and you will use the RoboticArmOperation tool to create a schedule. Please break down the steps as much as possible."),
        ])
        st.session_state['chat_history'] = template
    else:
        template = st.session_state['chat_history']
    return template

chat_tmp = init_chat_history()
llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0).bind_tools([RoboticArmOperation])
user_input = st.chat_input("Say something")
chain = chat_tmp | llm | JsonOutputToolsParser()

if user_input:
    with st.status("Thinking..."):
        chat_tmp.append(HumanMessage(user_input))
        response = chain.invoke({})
        chat_tmp.append(AIMessage(str(response)))
        st.session_state['chat_history'] = chat_tmp

for message in st.session_state['chat_history'].messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.json(message.content)
    
if st.button("Submit Task"):
    st.success("Task submitted")
    # send task to backend (str format)
    last_edit_task:str = chat_tmp.messages[-1].content
    payload = {
        "task": last_edit_task
    }
    response = requests.post(f"http://{BACKEND_HOST}/task", json=payload)
    st.write(response.json())