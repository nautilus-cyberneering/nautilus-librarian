# Nautilus Librarian

[![Lint Code Base](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/linter.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/linter.yml) [![Publish Docker image](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml)

A Python Console application to handle media libraries like Git and [Dvc](https://github.com/iterative/dvc).

## Development

### Run

With docker:

Build:

```shell
./bin/docker/build.sh
```

Run pre-built docker image:

```shell
./bin/docker/run.sh [OPTIONS] COMMAND [ARGS]...
./bin/docker/run.sh --help
```

Run mounting current repo:

```shell
./bin/docker/run-dev.sh [OPTIONS] COMMAND [ARGS]...
./bin/docker/run-dev.sh --help
```

With Poetry:

```shell
poetry install
poetry run nautilus-librarian [OPTIONS] COMMAND [ARGS]...
poetry run nautilus-librarian --help
```

> NOTE: With Poetry, you have to install the [Librarian system dependencies](https://github.com/Nautilus-Cyberneering/librarian-system-dockerfile).

### Testing

With docker:

```shell
./bin/docker/test.sh
```

With Poetry:

```shell
poetry shell
pytest
```

or:

```shell
poetry run pytest --cov
```

### Linting

For Dockerfile:

We are using GitHub Action [super-linter](https://github.com/marketplace/actions/super-linter). If you want to check the `Dockerfile` linting before pushing, you can do it with:

```shell
docker run --rm -i hadolint/hadolint < Dockerfile
```
