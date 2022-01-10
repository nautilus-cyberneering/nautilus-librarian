# Install

Requirements:

- Libvips-dev 8.10.5-2
- Python 3.9

Install Python Package:

```shell
pip install nautilus-librarian
```

Install system dependencies (ubuntu):

```shell
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y libvips-dev
```

Example commands:

```shell
nautilus-librarian [OPTIONS] COMMAND [ARGS]...
nautilus-librarian --help
nautilus-librarian namecodes --help
nautilus-librarian namecodes validate-filename 000000-32.600.2.tif
```

You can also use the docker image from the DockerHub registry:

```shell
docker run --rm -it nautiluscyberneering/librarian [OPTIONS] COMMAND [ARGS]...
docker run --rm -it nautiluscyberneering/librarian --help
```

Or the docker image from the GitHub registry:

```shell
docker run --rm -it ghcr.io/nautilus-cyberneering/librarian [OPTIONS] COMMAND [ARGS]...
docker run --rm -it ghcr.io/nautilus-cyberneering/librarian --help
```

## Links

- [DockerHub docker image nautiluscyberneering/librarian](https://hub.docker.com/repository/docker/nautiluscyberneering/librarian)
- [GitHub docker image ghcr.io/nautiluscyberneering/librarian](https://github.com/Nautilus-Cyberneering/librarian/pkgs/container/librarian)
