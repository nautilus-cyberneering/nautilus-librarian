# Nautilus Librarian

[![Lint Code Base](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/linter.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/linter.yml) [![Publish Docker image](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml)

A Python Console application to handle media libraries like Git and [Dvc](https://github.com/iterative/dvc).

## Run

### With docker

Build:

```shell
./bin/build.sh
```

Run:

```shell
docker run --rm -it nautilus-librarian [OPTIONS] COMMAND [ARGS]...
docker run --rm -it nautilus-librarian --help
```

Run for development:

```shell
./bin/run.sh [OPTIONS] COMMAND [ARGS]...
./bin/run.sh --help
```

### With Poetry

```shell
poetry install
poetry run nautilus-librarian --help
```

## Testing

With Poetry:

```shell
poetry shell
pytest
```

## Lint

### Dockerfile

We are using GitHub Action [super-linter](https://github.com/marketplace/actions/super-linter). If you want to check the `Dockerfile` linting before pushing, you can do it with:

```shell
docker run --rm -i hadolint/hadolint < Dockerfile
```
