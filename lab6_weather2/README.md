# Weather Django App

## Запуск Postgres
```
docker compose up -d
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