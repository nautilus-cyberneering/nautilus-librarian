# Librarian System Dependencies

[![Lint Code Base](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/linter.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/linter.yml) [![Publish Docker image](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml)

A Python Console application to handle media libraries like Git and [Dvc](https://github.com/iterative/dvc).

## Lint

### Dockerfile

We are using GitHub Action [super-linter](https://github.com/marketplace/actions/super-linter). If you want to check the `Dockerfile` linting before pushing, you can do it with:

```shell
docker run --rm -i hadolint/hadolint < Dockerfile
```

## Run

Build:

```shell
docker build -t librarian .
```

Run:

```shell
docker run --rm -it librarian [OPTIONS] COMMAND [ARGS]...
docker run --rm -it librarian --help
```
