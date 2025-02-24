FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
 apt-get install -y --no-install-recommends \
 gcc \
 && rm -rf /var/lib/apt/lists/*

ARG ENV=production

COPY requirements.txt .
COPY src/ ./src/
COPY config/ ./config/

RUN mkdir -p data

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
ENV ENV=${ENV}

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
 CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "src/scraper.py"]
