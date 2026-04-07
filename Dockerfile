FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Ensure the root is in the Python path
ENV PYTHONPATH=/app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files [cite: 263-265]
COPY . .

# Run uvicorn using the module path
CMD ["sh", "-c", "uvicorn governor.main:app --host 0.0.0.0 --port ${PORT:-8080}"]