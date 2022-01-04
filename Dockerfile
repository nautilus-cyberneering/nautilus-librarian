FROM nautiluscyberneering/librarian-system-dockerfile:v1.0.0 AS builder

WORKDIR /app

    # Python
ENV PYTHONPATH=${PYTHONPATH}:/app:/app/src \
    # Poetry
    POETRY_HOME="/opt/poetry"

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && poetry config virtualenvs.create false

# Install libvips
RUN rm -rf /var/lib/apt/lists/* \
    apt-get update \
	&& apt-get install -y  --no-install-recommends "libvips-dev>=8.12.1"

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-root

COPY . /app

ENTRYPOINT ["python", "-m", "nautilus_librarian"]

