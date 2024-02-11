# yayd

### Запуск базы данных
```
docker compose up -d
```

### Запуск сервера
``` bash
poetry install 

# или так
poetry run python3 djangoinfire/manage.py migrate
poetry run python3 djangoinfire/manage.py runserver

# или так 
poetry shell
python djangoinfire/manage.py migrate
python djangoinfire/manage.py runserver
```