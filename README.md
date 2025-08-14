# FastAPI Blog

A simple blog backend made with FastAPI + MongoDB

## Tech Stack

- Python (≥ 3.10)
- FastAPI
- MongoDB
- Beanie
- Pydantic

## Environment Variables

```txt
PROJECT_NAME=
STACK_NAME=

MONGO_SERVER=
MONGO_PORT=
MONGO_DB=
MONGO_USER=
MONGO_PASSWORD=

DOCKER_IMAGE_BACKEND=
```

## Setup

- Docker build

```bash
docker build -t fastapi-blog-backend:latest .
```

- Docker compose

```bash
docker compose up
```
