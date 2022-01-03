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
pip install poetry poetry-dynamic-versioning
poetry install
poetry run nautilus-librarian [OPTIONS] COMMAND [ARGS]...
poetry run nautilus-librarian --help
```

> NOTE: With Poetry, you have to install the [Librarian system dependencies](https://github.com/Nautilus-Cyberneering/librarian-system-dockerfile).

## Build

```shell
pip install poetry poetry-dynamic-versioning
poetry install
poetry build
```

You should have the package in the `dist` folder.

You can install the package locally with:

```shell
pip install --user --force-reinstall dist/nautilus_librarian-0.2.1.post2.dev0+871cb83-py3-none-any.whl
```

Where `0.2.1.post2.dev0+871cb83` is the package version. You can get the package version with: `poetry version`.
Remember to exit from your poetry Python environment. If you open the wheel file (zip) you will find the version in
the `nautilus_librarian/_version.py` file:

```text
...
__version__: str = "0.2.1.post2.dev0+871cb83"
...
```

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

Some useful test commands:

Run only one test (`-k`) with no capture (`-s`):

```shell
pytest -s -k "test_app"
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

## Run workflows locally

You can use [act](https://github.com/nektos/act) to run workflows locally. For example:

```shell
act -W ./.github/workflows/test-gold-images-processing-workflow.yml -j build
```

With that command, you can run the `build` job in the `test-gold-images-processing-workflow.yml` workflow.

## Releases

We use [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). To publish a new release, you only new to
create the tag (for example, `v1.3.0`) and push it to [GitHub](https://github.com/Nautilus-Cyberneering/nautilus-librarian/tags).

```shell
git tag v1.3.0
git push origin v1.3.0
```

## Commits

We are using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Security

The application uses a lot of console commands. Commands that use arguments taken from user input could be a potential security risk. Please review the rules to avoid command injection before adding a new console command.

If you want to know more about command injection please read the links below.

The basic rules to follow when you add a new console command are:

1. Always try to use an internal Python API (if it exists) instead of running an OS command.
2. Try to use a high-level wrapper instead of executing a command: `gpg_connect_agent(...)`, `git(...)`, `dvc(...)`, `gpg(...)`.
3. Do not pass user-controlled input (if possible). If you need it, consider using validation before passing values. If you expect a file path, check if the file exists. If you expect an email, validate the email, etcetera.
4. Do not use "shell" if not needed. Consider using `execute_console_command` instead of `execute_shell_command`.
5. Do not use "f-string" with `execute_console_command` and `execute_shell_command`. Consider using placeholders in the command string and passing variables values as keyword arguments. Those functions use the function `shlex.quote(..)` to scape the values. For example:

```python
execute_console_command(
    "dvc remote add -d {remote_name} {remote_dir}",
    remote_name=remote_name,
    remote_dir=remote_dir,
    cwd=self.git_repo_dir,
)
```

instead of:

```python
execute_console_command(
    f"dvc remote add -d {remote_name} {remote_dir}",
    cwd=self.git_repo_dir,
)
```

Links:

* [OS Command Injection in Python](https://semgrep.dev/docs/cheat-sheets/python-command-injection/)
* [Command injection prevention for Python](https://knowledge-base.secureflag.com/vulnerabilities/code_injection/os_command_injection_python.html)
