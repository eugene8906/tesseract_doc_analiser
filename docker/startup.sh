#!/bin/bash

# Ожидание запуска базы данных
#echo "Waiting for PostgreSQL to start..."
#
#while ! nc -z $DB_HOST $DB_PORT; do
#  sleep 1
#done
#
#echo "PostgreSQL started"

# Применение миграций
echo "Applying migrations..."
python manage.py migrate

# Запуск сервера
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:7000
