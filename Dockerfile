FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
 apt-get install -y --no-install-recommends \
 gcc \
 && rm -rf /var/lib/apt/lists/*

# 接收建構參數
ARG ENV=development

COPY requirements.txt .
COPY src/ ./src/
COPY config/ ./config/

RUN mkdir -p data

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
ENV ENV=${ENV}

CMD ["python", "src/scraper.py"]
