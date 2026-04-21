FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY tests ./tests

COPY utils ./utils

COPY run_all.py .

CMD ["python", "run_all.py"]
