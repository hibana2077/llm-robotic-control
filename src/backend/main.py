'''
Author: hibana2077 hibana2077@gmail.com
Date: 2024-05-17 21:46:09
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-06-01 16:34:05
FilePath: \llm-robotic-control\src\backend\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from transformers import AutoModelForSpeechSeq2Seq, pipeline
from PIL import Image
import redis
import torch
import os
import uvicorn
import io
import base64
import time
import requests

# Environment variables

HOST = os.getenv("HOST", "127.0.0.1")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Constants

MODEL_ID = "google/paligemma-3b-mix-224"
WHISPER_MODEL_ID = "openai/whisper-large-v3"
DEVICE = "cuda:0"
DTYPE = torch.bfloat16
WHISPER_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

# Connect to Redis

redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

# Load model

text_vision_model = PaliGemmaForConditionalGeneration.from_pretrained(
    MODEL_ID,
    torch_dtype=DTYPE,
    device_map=DEVICE,
    revision="bfloat16",
).eval()
whisper_model = AutoModelForSpeechSeq2Seq.from_pretrained(
    WHISPER_MODEL_ID, torch_dtype=WHISPER_DTYPE, low_cpu_mem_usage=True, use_safetensors=True
)
whisper_model.to(DEVICE)

# Load processor
audio_processor = AutoProcessor.from_pretrained(WHISPER_MODEL_ID)
text_vision_processor = AutoProcessor.from_pretrained(MODEL_ID)

# define pipeline
whisper_pipeline = pipeline(
    "automatic-speech-recognition",
    model=whisper_model,
    tokenizer=audio_processor.tokenizer,
    feature_extractor=audio_processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=WHISPER_DTYPE,
    device=DEVICE,
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/generate")
async def generate(data: dict):
    ts = time.time()
    text:str = data["text"]
    image:str = data["image"]
    # Convert base64 to image
    image = Image.open(io.BytesIO(base64.b64decode(image)))
    model_inputs = text_vision_processor(text=text, images=image, return_tensors="pt").to(text_vision_model.device)
    input_len = model_inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = text_vision_model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
        generation = generation[0][input_len:]
        decoded = text_vision_processor.decode(generation, skip_special_tokens=True)
    return {"generated_text": decoded, "time": time.time() - ts}

@app.post("/whisper")
async def whisper(file: UploadFile = File(...)):
    ts = time.time()
    # save file to temp location
    with open("temp.wav", "wb") as f:
        f.write(file.file.read())
    # load file and run whisper pipeline
    result = whisper_pipeline(f"temp_{ts}.wav", generate_kwargs={"task": "translate"})
    # remove temp file
    os.remove("temp.wav")
    return {"translate": result, "time": time.time() - ts}

@app.post("/exp_data_recorder")
async def exp_data_recorder(data: dict):
    print(data)
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8000)