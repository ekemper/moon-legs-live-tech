# Piano Practice App backend: FastAPI + Uvicorn
# SuperCollider runs on host; set SC_HOST=host.docker.internal when using Docker.

FROM python:3.12-slim

# Non-root user
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --shell /bin/sh --create-home app
WORKDIR /app

# Dependencies (build from repo root: docker build -f backend/Dockerfile .)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application (backend + data; sc_programs stay on host)
COPY backend /app/backend
COPY data /app/data

# Ensure data dir writable for device_configs.json
RUN chown -R app:app /app

USER app
EXPOSE 8765

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8765"]
