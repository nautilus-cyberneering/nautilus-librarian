# Development

## Run

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

## Testing

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

## Linting

With [MegaLinter](https://megalinter.github.io/latest/mega-linter-runner/#local-installation):

Install:

```shell
npm install mega-linter-runner -g
```

Run with the auto fix:

```shell
mega-linter-runner --fix
```

## Releases

We use [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). To publish a new release, you only new to create the tag (for example, `v1.3.0`) and push it to [GitHub](https://github.com/Nautilus-Cyberneering/librarian/tags).
