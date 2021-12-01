FROM  python:3.9 AS builder

    # Pip
ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=${PYTHONPATH}:${PWD} \
    # Poetry
    POETRY_HOME="/opt/poetry"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN mkdir /app
WORKDIR /app

# Install Poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && poetry config virtualenvs.create false

# Install dependencies
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-root

COPY ./src /app

ENTRYPOINT ["python", "-m", "nautilus_librarian"]

