FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up your working directory and install Poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi \
    && poetry cache clear . --all --no-interaction

# Copy the rest of your application code
COPY . .

# 포트 노출
EXPOSE 8080

# FastAPI 앱 실행
ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
