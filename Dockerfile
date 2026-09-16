FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY backend/pyproject.toml backend/uv.lock ./

RUN uv sync --locked

COPY backend/ .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "Workshop.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
