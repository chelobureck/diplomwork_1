#!/bin/bash
set -e

echo "--> Проверка подключения к базе данных..."

if [ "$DATABASE" = "postgres" ]
then
    echo "Ожидание базы данных PostgreSQL ($DB_HOST:$DB_PORT)..."
    
    if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ]; then
        echo "Ошибка: Переменные DB_HOST или DB_PORT не заданы!"
        exit 1
    fi

    while ! timeout 1 bash -c "cat < /dev/null > /dev/tcp/$DB_HOST/$DB_PORT" 2>/dev/null; do
      echo "База данных еще не доступна, ждем..."
      sleep 1
    done
    
    echo "База данных PostgreSQL запущена и доступна!"
    
    # СЮДА: Автоматически запускаем миграции прямо перед стартом сервера
    echo "--> Накатываем миграции..."
    python manage.py migrate
fi

exec "$@"