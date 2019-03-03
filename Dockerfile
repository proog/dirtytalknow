FROM python:3.7-slim

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

COPY normalcommenter ./normalcommenter

ENTRYPOINT [ "python", "-m", "normalcommenter" ]
