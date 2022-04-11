FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add gcc python3-dev libc-dev libffi-dev firefox

COPY . /usr/src/screenshot
WORKDIR /usr/src/screenshot

RUN pip install -r requirements.txt
