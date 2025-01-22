# Официальный образ Python
FROM python:3.12-slim-bullseye

# Переменные окружения для Python
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

# Устанавливаею рабочую директорию
WORKDIR /cafe_order_system

# Настройка временной зоны UTC
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone

# Системные зависимости (для сборки и PostgreSQL клиента)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копирую файл с зависимостями (requirements.txt) в контейнер
COPY requirements.txt .

# Устанавка Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Все файлы проекта копируются в контейнер
COPY . .

# Исполняемым скрипт entrypoint.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Порт для Django
EXPOSE 8000

# Устанавливаю entrypoint для запуска сервера Django
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Команда для запуска Django-сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
