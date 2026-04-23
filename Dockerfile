
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

#cmd for local/manual run only
#CMD ["python", "-m", "pipelines.runner"]