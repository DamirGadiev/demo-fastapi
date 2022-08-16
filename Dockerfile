FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
WORKDIR ./app

COPY requirements.txt .
COPY /app/templates /app/
RUN pip install -r requirements.txt
