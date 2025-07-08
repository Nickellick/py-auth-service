# Dockerfile

# pull the official docker image
FROM python:3.13-slim AS builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry==2.1.3

WORKDIR /app

COPY pyproject.toml .

RUN poetry install --no-root && poetry export --without-hashes --format requirements.txt --output requirements.txt

FROM python:3.13-slim AS executor
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY --from=builder /app/requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
