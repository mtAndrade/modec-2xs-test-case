ARG environment

FROM python:3.8.6-slim-buster as base

WORKDIR /srv/app

ADD . /srv/app

RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    make \
    git \
    gcc \
    ssh \
    libc-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

RUN \
    pip install --upgrade pip; \
    pip install pipenv;

RUN make install

CMD make start
