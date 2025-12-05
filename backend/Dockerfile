FROM python:3.12-slim

WORKDIR /app

# Copy ONLY requirements first (better caching)
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Now copy the full backend source code
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#FROM python:3.12-slim

#WORKDIR /app

#COPY backend/ /app/backend/
#COPY backend/requirements.txt /app/requirements.txt

#RUN pip install --no-cache-dir -r /app/requirements.txt

#EXPOSE 8000
#
#CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
