# syntax=docker/dockerfile:1.2
FROM python:latest
# put you docker configuration here
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]