FROM python:3.9-slim

# Establish the working directory
WORKDIR /app

# Set the Python path so the governor module is discoverable
ENV PYTHONPATH=/app

# Install dependencies first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all PhD project folders (governor, agents, harness, etc.)
COPY . .

# Launch the GMD Hub using the dynamic PORT provided by GCP
CMD ["sh", "-c", "uvicorn governor.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
