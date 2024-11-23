FROM python:3.10.12

RUN apt-get update \
    && apt-get install -y python3-dev libc-dev gcc musl-dev

WORKDIR /app

RUN pip install --upgrade pip setuptools

RUN pip install gunicorn

ADD ./requirements.txt /app/

RUN pip install -r requirements.txt
