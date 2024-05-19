'''
Author: hibana2077 hibana2077@gmail.com
Date: 2024-05-17 21:46:09
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-05-19 21:09:15
FilePath: \llm-robotic-control\src\backend\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
import torch
import uvicorn
import io
import base64
import time
import requests

# Constants

MODEL_ID = "google/paligemma-3b-mix-224"
DEVICE = "cuda:0"
DTYPE = torch.bfloat16

# Load model

text_vision_model = PaliGemmaForConditionalGeneration.from_pretrained(
    MODEL_ID,
    torch_dtype=DTYPE,
    device_map=DEVICE,
    revision="bfloat16",
).eval()
processor = AutoProcessor.from_pretrained(MODEL_ID)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate")
def generate(text: str, image: str):# image in base64
    ts = time.time()
    # Convert base64 to image
    image = Image.open(io.BytesIO(base64.b64decode(image)))
    model_inputs = processor(text=text, images=image, return_tensors="pt").to(text_vision_model.device)
    input_len = model_inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = text_vision_model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
        generation = generation[0][input_len:]
        decoded = processor.decode(generation, skip_special_tokens=True)
    return {"generated_text": decoded, "time": time.time() - ts}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)