FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY env.json /app/env.json

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
