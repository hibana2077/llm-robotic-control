import streamlit as st
import requests

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