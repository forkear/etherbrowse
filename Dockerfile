ARG APP_IMAGE=python:3.10.5-slim-buster

FROM $APP_IMAGE AS base

FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt


RUN pip install --prefix=/install -r /requirements.txt

FROM base
ENV FLASK_APP app.py
WORKDIR /project
COPY --from=builder /install /usr/local
ADD . /project

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]