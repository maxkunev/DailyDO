FROM python:3.13-slim

WORKDIR /app/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pybabel compile -d bot/locales -D messages

COPY docker/backend/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]



