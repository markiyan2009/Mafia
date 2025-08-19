# Використаємо офіційний Python образ
FROM python:3.11-slim

# Встановимо робочу директорію
WORKDIR /app

# Вимикаємо кеш python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо проєкт
COPY . .

# Збираємо статичні файли (якщо є)
RUN python manage.py collectstatic --noinput

# Запускаємо через gunicorn
CMD gunicorn Mafia.wsgi:application --bind 0.0.0.0:$PORT