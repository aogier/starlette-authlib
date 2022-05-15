ARG PYTHON_VERSION=3.10
FROM aogier/python-poetry:py${PYTHON_VERSION} as poetry

WORKDIR /srv
COPY . .

RUN set -x \
    && poetry config virtualenvs.create false \
    && poetry install

FROM poetry as test

RUN scripts/test

FROM poetry as release

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
