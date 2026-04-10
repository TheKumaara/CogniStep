# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
# Build context is cognistep_env/ so server/requirements.txt is accessible
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full package so relative imports work inside the container
# cognistep_env/__init__.py, client.py, models.py are siblings of server/
COPY __init__.py ./cognistep_env/__init__.py
COPY client.py   ./cognistep_env/client.py
COPY models.py   ./cognistep_env/models.py
COPY server/     ./cognistep_env/server/

# Expose port
EXPOSE 8000

# Run from /app so Python sees cognistep_env as a top-level package
# app.py's relative imports (from ..models) resolve correctly this way
CMD ["uvicorn", "cognistep_env.server.app:app", "--host", "0.0.0.0", "--port", "8000"]