FROM python:3.12.4-slim

RUN apt-get install -y cron

WORKDIR /app

COPY /server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /server /app

COPY /.config /app/.config

RUN service cron start

RUN chmod +x .config/backend/entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "/app/.config/backend/entrypoint.sh" ]