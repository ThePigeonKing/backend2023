FROM python:3.11

RUN pip install poetry

WORKDIR /usr/src/app

COPY pyproject.toml ./

# CMD ["sleep", "10000"]

# RUN poetry config virtualenvs.create true \
#   && poetry install --no-interaction --no-ansi

RUN pip install django django-bootstrap5 psycopg2-binary

COPY ./djangoinfire/ /usr/src/app/

COPY ./wait_for_it.sh ./migrate_run.sh ./


CMD ["./wait_for_it.sh", "postgres:5432", "--", "./migrate_run.sh"]