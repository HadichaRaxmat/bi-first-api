FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app/

# Открываем порт
EXPOSE 8000

# Запуск Gunicorn
CMD ["gunicorn", "be-first.wsgi:application", "--bind", "0.0.0.0:8000"]
