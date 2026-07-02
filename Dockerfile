FROM python:3.12
WORKDIR /app

RUN python -m pip install --upgrade pip

COPY pyproject.toml uv.lock ./

RUN pip install .

COPY . .
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]