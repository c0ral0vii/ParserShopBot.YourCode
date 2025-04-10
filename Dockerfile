FROM python:3.13.2-slim



RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /bot
COPY . .

RUN pip install uv
RUN uv sync --no-cache

CMD ["python", "main.py"]