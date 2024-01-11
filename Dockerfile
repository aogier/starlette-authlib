ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION} as base

WORKDIR /srv
COPY . .

# hadolint ignore=DL3042,DL3013
RUN set -x \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

FROM base as test

ARG PYTHON_VERSION=3.10

RUN if [ $PYTHON_VERSION != 3.7 ] \
    ;then \
        poetry run \
            pre-commit run \
                -a --show-diff-on-failure \
    ;fi \
    && poetry run \
        pytest \
            --ignore venv \
            -W ignore::DeprecationWarning \
            --cov-report=xml \
            --cov=starlette_authlib \
            --cov=tests \
            --cov-fail-under=100 \
            --cov-report=term-missing

FROM base as release

ARG PYPI_TOKEN
ARG CODECOV_TOKEN
ARG GIT_SHA

COPY --from=test /srv/coverage.xml .

RUN set -x \
    && poetry publish --build \
        --username __token__ \
        --password $PYPI_TOKEN \
    && codecov \
        --token $CODECOV_TOKEN \
        --commit $GIT_SHA
