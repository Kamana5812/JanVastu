# Optional compatibility CLI. Build from the repository root:
# docker build -f ai-pipeline/pipelines/Dockerfile .
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY ai-pipeline/pipelines/main.py ./pipeline.py
CMD ["python", "pipeline.py"]
