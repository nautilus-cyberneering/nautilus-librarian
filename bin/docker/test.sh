#!/bin/bash

docker run --rm -it \
	--volume "$(pwd)":/app \
	--entrypoint="pytest" \
	nautilus-librarian "$@"
