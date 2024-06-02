'''
Author: hibana2077 hibana2077@gmail.com
Date: 2024-06-02 21:35:59
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-06-02 21:51:18
FilePath: \llm-robotic-control\src\st_web\pages\Task.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import streamlit as st
import translators as ts
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

# Load task from backend

# According to the action in the task, send control signals to database and robotic arm will get the signals from database

# Wait for the robotic arm to complete the action (loop until the action is completed(sleep for 1 second))

# Check the scene after the action is completed (use vision model to check the scene's description is the same as expected_image_description)

# If the scene is not the same as expected_image_description, determine should need human help or more additional actions

# need human: shut down the robotic arm and send a message to the user to ask for help

# need more actions: ask vision model to provide the next action and send the action to the robotic arm

# If the scene is the same as expected_image_description, go to the next action

# exit the action loop when all actions are completed