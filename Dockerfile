FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN python3 -m venv venv
RUN source "venv/bin/activate"
RUN pip install -r requirements.txt

COPY . /app

ENV PORT=8000
EXPOSE $PORT

