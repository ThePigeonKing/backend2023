# Weather Django App

## Запуск

Через докер:
```
# в файл .env внесите свой API ключ (см. env.example)
docker compose up
```

Ручной режим:
```
# сначал экспортируйте переменную окружения
export APIKEY=<KEY HERE>
poetry install
poetry run python3 weather_app/manage.py migrate
poetry run python3 weather_app/manage.py runserver
```