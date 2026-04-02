# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (cache optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all server files
COPY . .

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]