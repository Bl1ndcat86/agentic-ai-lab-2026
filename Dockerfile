FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire project structure
COPY . .
# Use the PORT environment variable provided by Cloud Run
CMD ["sh", "-c", "uvicorn governor.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
