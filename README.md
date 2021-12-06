# Nautilus Librarian

[![Lint Code Base](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/linter.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/linter.yml)
[![Test](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/test.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/test.yml)
[![Publish Docker image](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml)
[![Publish to PyPI](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-pypi.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-pypi.yml)

A Python Console application to handle media libraries like Git and [Dvc](https://github.com/iterative/dvc).

## Install

Requirements:

- Libvips
- Python 3.9

Install Python Package:

```shell
pip install nautilus-librarian
```

Example commands:

```shell
nautilus-librarian [OPTIONS] COMMAND [ARGS]...
nautilus-librarian --help
nautilus-librarian namecodes --help
nautilus-librarian namecodes validate-filename 000000-32.600.2.tif
```

You can also use the docker image from DockerHub registry:

```shell
docker run --rm -it nautiluscyberneering/librarian [OPTIONS] COMMAND [ARGS]...
docker run --rm -it nautiluscyberneering/librarian --help
```

Or the docker image from GitHub registry:

```shell
docker run --rm -it ghcr.io/nautilus-cyberneering/librarian [OPTIONS] COMMAND [ARGS]...
docker run --rm -it ghcr.io/nautilus-cyberneering/librarian --help
```

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

With [MegaLinter](https://megalinter.github.io/latest/mega-linter-runner/#local-installation):

Install:

```
```

Run:

```
npx mega-linter-runner
```

For Dockerfile:

We are using GitHub Action [super-linter](https://github.com/marketplace/actions/super-linter). If you want to check the `Dockerfile` linting before pushing, you can do it with:

```shell
docker run --rm -i hadolint/hadolint < Dockerfile
```

Run super-linter locally with [act](https://github.com/nektos/act):

```shell
act -W .github/workflows/linter.yml -j build
```
