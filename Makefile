#!/usr/bin/make -f

PULL=git pull origin

.PHONY: main
main: install run

.PHONY: install
install:
	$(PULL) master
	git submodule update

.PHONY:
update:
	git submodule foreach '${PULL} main'

.PHONY: run
run:
	COMPOSE_DOCKER_CLI_BUILD=1 docker-compose up --build --force-recreate -d

.PHONY: stop
stop:
	docker-compose down
