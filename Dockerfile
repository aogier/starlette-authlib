ARG PYTHON_VERSION=3.14
FROM python:${PYTHON_VERSION} AS base

WORKDIR /srv
COPY . .

# hadolint ignore=DL3042,DL3013
RUN set -x \
    && pip install uv \
    && uv sync

FROM base AS test

ARG PYTHON_VERSION=3.10

RUN uv run pre-commit run -a --show-diff-on-failure \
    && uv run \
          pytest \
          --ignore venv \
          -W ignore::DeprecationWarning \
          --cov-report=xml \
          --cov=starlette_authlib \
          --cov=tests \
          --cov-fail-under=100 \
          --cov-report=term-missing

FROM base AS release

ARG PYPI_TOKEN
ARG CODECOV_TOKEN
ARG GIT_SHA

COPY --from=test /srv/coverage.xml .

RUN set -x \
    && uv build \
    && uv publish \
        --token $PYPI_TOKEN \
    && uv run codecov \
        --token $CODECOV_TOKEN \
        --commit $GIT_SHA
