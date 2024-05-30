'''
Author: hibana2077 hibana2077@gmail.com
Date: 2024-05-20 01:00:06
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-05-30 20:40:55
FilePath: \llm-robotic-control\src\rp2040\main.py
Description: api server to get real time image
'''
from fastapi import FastAPI
import cv2 as cv
import base64
import uvicorn
import os

HOST = os.getenv("HOST", "127.0.0.1")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/image")
async def get_image():
    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    ret, buffer = cv.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8000)