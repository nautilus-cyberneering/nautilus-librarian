# Install

Requirements:

- Libvips-dev 8.10.5-2
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
