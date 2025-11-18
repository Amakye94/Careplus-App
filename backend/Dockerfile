# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy backend code
COPY . /app/backend

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
