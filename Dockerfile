FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
 apt-get install -y --no-install-recommends \
 gcc \
 && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
COPY src/ ./src/


RUN mkdir -p data


RUN pip install --no-cache-dir -r requirements.txt


ENV PYTHONPATH=/app


CMD ["python", "src/scraper.py"]
