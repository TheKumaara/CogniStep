FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt pyproject.toml ./
COPY cognistep_env/ ./cognistep_env/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "cognistep_env.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
