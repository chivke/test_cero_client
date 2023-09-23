FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY ./.docker/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./.docker/start_test /start_test
RUN sed -i 's/\r$//g' /start_test
RUN chmod +x /start_test

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
