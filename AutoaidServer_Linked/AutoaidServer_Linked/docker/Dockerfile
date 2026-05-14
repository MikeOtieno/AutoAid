
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential gcc git ffmpeg libsndfile1     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY autoaid /app/autoaid
COPY ml /app/ml

RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

WORKDIR /app/autoaid

EXPOSE 8000
