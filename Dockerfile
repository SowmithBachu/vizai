FROM python:3.11-slim


WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libc6-dev \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static


EXPOSE 5000

ENV FLASK_APP=app_flask.py
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app_flask:app"]

