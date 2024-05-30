FROM ubuntu:22.04

RUN apt update && apt install -y \
    git \
    cmake \
    python3 \
    python3-pip \
    g++ \
    gcc

RUN apt-get install python3-opencv -y

RUN pip3 install fastapi

WORKDIR /app

COPY . .

CMD ["python3", "main.py"]