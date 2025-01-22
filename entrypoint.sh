#!/bin/bash

# Установка значений по умолчанию
POSTGRES_DB=${POSTGRES_DB:-mydatabase}
POSTGRES_USER=${POSTGRES_USER:-myuser}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-mypassword}
POSTGRES_HOST=${POSTGRES_HOST:-db}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

# Ожидание подключения к PostgreSQL
echo "Ожидание подключения к PostgreSQL на $POSTGRES_HOST:$POSTGRES_PORT..."
timeout=240
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))
    if [ $timeout -le 0 ]; then
        echo "Ошибка: PostgreSQL не подключился в течение заданного времени."
        exit 1
    fi
done

echo "PostgreSQL подключен. Проверяем существование базы данных..."
DB_EXIST=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -tc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'" | xargs)
if [ "$DB_EXIST" != "1" ]; then
    echo "База данных $POSTGRES_DB не найдена. Создаём..."
    PGPASSWORD=$POSTGRES_PASSWORD createdb -h $POSTGRES_HOST -U $POSTGRES_USER $POSTGRES_DB
else
    echo "База данных $POSTGRES_DB уже существует."
fi

# Применение миграций
echo "Применение миграций..."
python manage.py makemigrations
python manage.py migrate

# Загрузка фикстур
echo "Загрузка фикстур..."
python manage.py loaddata dishes.json orders.json order_dishes.json revenue.json

# Запуск сервера
echo "Запуск сервера Django..."
exec "$@"  # Передаем управление в следующую команду
