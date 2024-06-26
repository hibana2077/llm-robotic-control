'''
Author: hibana2077 hibana2077@gmail.com
Date: 2024-06-02 21:35:59
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-06-07 13:11:02
FilePath: \llm-robotic-control\src\st_web\pages\Task.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import streamlit as st
import requests
import json
import os
import yaml
import time
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

def need_human_intervention(current_scene, expected_scene):
    # 根據實際情況定義何時需要人工干預
    # 此處僅為示例
    return current_scene != expected_scene

def get_next_action_from_vision_model():
    # 請求視覺模型提供下一步行動
    # 此處需要實現與視覺模型的接口
    next_action = requests.get(f"http://{BACKEND_HOST}/get_next_action").json()
    return next_action

# Load task from backend

tasks_list = requests.get(f"http://{BACKEND_HOST}/get_tasks").json()

# Display the tasks in a selectbox

selected_task_index = st.selectbox("Select a task", range(len(tasks_list)), index=None, placeholder="Select a task")

# Display the selected task

if selected_task_index is not None:
    selected_task = tasks_list[selected_task_index]
    st.json(selected_task)

# Execute button
if st.button("Execute Task"):
    # send task to backend (str format)
    payload = {
        "task": selected_task
    }
    response = requests.post(f"http://{BACKEND_HOST}/remove_task", json=payload)
    if response.status_code == 200:st.success("Task will be executed")
    else:st.error("Task could not be executed")

# Turn the task into a json object

task = json.loads(selected_task)[0]

# According to the action in the task, send control signals to database and robotic arm, arm will get the signals from database

# Wait for the robotic arm to complete the action (loop until the action is completed(sleep for 1 second))

# Check the scene after the action is completed (use vision model to check the scene's description is the same as expected_image_description)

# If the scene is not the same as expected_image_description, determine should need human help or more additional actions

# need human: shut down the robotic arm and send a message to the user to ask for help

# need more actions: ask vision model to provide the next action and send the action to the robotic arm

# If the scene is the same as expected_image_description, go to the next action

# exit the action loop when all actions are completed

# 根據任務中的行動指示，向數據庫發送控制信號
for action in task['tasks']:
    # 向數據庫發送控制信號（假設已實現的接口）
    response = requests.post(f"http://{BACKEND_HOST}/send_signal", json=action['action'])
    if response.status_code == 200:
        st.success("Control signals sent to the robotic arm.")
    else:
        st.error("Failed to send control signals.")
    
    # 等待機械手臂完成動作
    action_completed = False
    while not action_completed:
        time.sleep(1)
        # 檢查機械手臂是否完成動作（此處需要與實際硬體接口對接）
        status = requests.get(f"http://{BACKEND_HOST}/check_status").json()
        if status['status'] == "completed":
            action_completed = True
    
    # 使用視覺模型檢查動作後的場景
    current_scene_description = requests.get(f"http://{BACKEND_HOST}/get_scene_description").json()['description']

    # 如果場景與預期描述不符，決定是否需要人工幫助或進行其他行動
    if current_scene_description != action['expected_image_description']:
        if need_human_intervention(current_scene_description, action['expected_image_description']):
            # 需要人工幫助
            st.error("Human intervention required. Please assist.")
            break
        else:
            # 需要更多行動，從視覺模型獲取下一個行動
            next_action = get_next_action_from_vision_model()
            continue  # 循環執行下一個行動
    else:
        st.success("Action completed as expected.")
        continue  # 轉到下一個行動

# 所有動作完成
st.success("All actions have been completed.")