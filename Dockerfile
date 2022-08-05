"""If you see this message, that's mean Dockerfile does not work for now. I'm so sorry"""
FROM python:3.10.4-slim-buster
LABEL maintainer='vasylenkokatrine@gmail.com'

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt

COPY . .
