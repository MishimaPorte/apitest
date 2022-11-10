# syntax=docker/dockerfile:1
FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/src

CMD ["python", "main.py"]
