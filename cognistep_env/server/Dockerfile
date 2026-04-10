# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (cache optimization)
# NOTE: Build context should be cognistep_env/ (one level above server/)
COPY server/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full cognistep_env package (needed so 'server' can import siblings)
COPY __init__.py ./cognistep_env/__init__.py
COPY client.py ./cognistep_env/client.py
COPY models.py ./cognistep_env/models.py
COPY server/ ./cognistep_env/server/

# Make cognistep_env importable
RUN echo "" > /app/cognistep_env/__init__.py || true

# Expose port
EXPOSE 8000

# Start server — run from /app so 'cognistep_env.server.app' resolves
CMD ["uvicorn", "cognistep_env.server.app:app", "--host", "0.0.0.0", "--port", "8000"]