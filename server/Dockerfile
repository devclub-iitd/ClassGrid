FROM python:3.12.4-slim

WORKDIR /backend

COPY /server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /server /backend

RUN chmod +x /backend/entrypoint.sh

EXPOSE 8000

# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

ENTRYPOINT [ "/backend/entrypoint.sh" ]