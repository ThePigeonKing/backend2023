FROM python:3.11

RUN pip install poetry

WORKDIR /usr/src/

COPY pyproject.toml /usr/src/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./weather_app /usr/src/app

# RUN "poetry run python3 app/manage.py makemigrations"
RUN poetry run python3 app/manage.py migrate

CMD ["poetry", "run", "python3", "app/manage.py", "runserver", "0.0.0.0:8000"]