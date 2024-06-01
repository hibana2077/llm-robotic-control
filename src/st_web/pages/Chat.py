import streamlit as st
import requests
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from audiorecorder import audiorecorder
import os
import yaml
"""
Workflow:
語音輸入 website
語音到文字轉換 api
指令解析 api
視覺識別 api
動作計劃 api
執行與即時反饋迴圈：
    執行計劃動作
    持續捕捉視覺資料
    根據視覺資料調整動作
    檢查是否達到目標
確認和結束
"""


st.title("Voice Robot Control")

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.export().read())  

    # To save audio to a file, use pydub export method:
    audio.export("audio.wav", format="wav")

    # To get audio properties, use pydub AudioSegment properties:
    st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")