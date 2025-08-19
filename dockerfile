# Базовий Python образ
FROM python:3.11-slim

# Робоча директорія всередині контейнера
WORKDIR /app

# Встановлюємо залежності системи
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо requirements
COPY requirements.txt /app/

# Ставимо залежності Python
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проекту
COPY . /app/

# Створюємо папку для статичних файлів
RUN mkdir -p /app/staticfiles

# Експортуємо порт (для локального тесту, Render і так підставить свій)
EXPOSE 8000

# Команда запуску (важливо: слухає PORT від Render)
CMD sh -c "gunicorn Mafia_sys.wsgi:application --bind 0.0.0.0:${PORT:-8000}"