# Weather Django App

## Запуск Postgres
```
docker compose up -d
```
или без компоуза
```
docker run -d \
  --name mypostgresdb \
  -e POSTGRES_DB=yourdbname \
  -e POSTGRES_USER=yourdbuser \
  -e POSTGRES_PASSWORD=yourdbpassword \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:13
```

## Добавить API ключ
```
export API_KEY=<your key here>
```

## Запустить сервер
```
poetry install
poetry run python3 main_weather/manage.py migrate
poetry run python3 main_weather/manage.py runserver
```