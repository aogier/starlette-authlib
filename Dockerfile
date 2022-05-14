ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim-bullseye as poetry

RUN set -x; apt-get update \
    && apt-get install -y curl \
    && curl \
        -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
        | python -

WORKDIR /srv
COPY . .

RUN set -x; . $HOME/.poetry/env \
    && poetry config virtualenvs.create false \
    && poetry install

FROM poetry as test

RUN scripts/test

FROM poetry as publish

ARG PYPI_TOKEN

RUN set -x; echo poetry publish --build -u __token__ -p XX
