#!/bin/bash

docker run --rm -it \
    --volume $(pwd)/src:/app \
    nautilus-librarian "$@"
