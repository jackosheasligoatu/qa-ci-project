FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pages ./pages
COPY tests ./tests
COPY utils ./utils

CMD ["pytest", "-v", "tests/"]
