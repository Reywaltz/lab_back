FROM python:3.10

COPY . /app

WORKDIR /app

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install