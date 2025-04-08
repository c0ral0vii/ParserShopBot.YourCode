FROM python:3.13.2-slim

WORKDIR /bot
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]