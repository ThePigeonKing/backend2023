FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /code

COPY pyproject.toml /code

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /code/

CMD ["sleep", "10000"]
# RUN poetry run python3 main_weather/manage.py migrate

# CMD ["poetry", "run", "python3", "main_weather/manage.py", "runserver", "0.0.0.0:8000"]