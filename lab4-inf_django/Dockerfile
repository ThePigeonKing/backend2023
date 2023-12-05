# Выбор базового образа с Python
FROM python:3.11

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файлов проекта в контейнер
COPY . /app/

# Установка Poetry
RUN pip install poetry

# Отключение виртуальных окружений для poetry (они не нужны в Docker)
RUN poetry config virtualenvs.create false

# Установка зависимостей через poetry
RUN poetry install --no-dev

# Указание команды для запуска приложения
# Здесь вам нужно указать команду для запуска вашего Django-приложения
CMD ["poetry", "run", "python3", "djangoinfire/manage.py", "runserver", "0.0.0.0:8001"]

