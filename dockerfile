FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Важливо: використовуємо sh -c для правильної обробки змінної PORT
CMD sh -c "python manage.py runserver 0.0.0.0:${PORT:-8000}"