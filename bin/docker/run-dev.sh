#!/bin/bash

docker run --rm -it \
    --volume "$(pwd)":/app \
    nautilus-librarian "$@"
