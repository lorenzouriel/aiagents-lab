FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry==1.8.5 && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./
RUN poetry install --only=main --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
