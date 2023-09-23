.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: up
up:
	@docker compose up

.PHONY: stop
stop:
	@docker compose stop

.PHONY: down
down:
	@docker compose down --remove-orphans

.PHONY: build
build:
	@docker compose build

.PHONY: rebuild
rebuild:
	@docker compose down --remove-orphans
	@docker compose build --no-cache

.PHONY: shell
shell:
	@docker compose run --rm client ipython

.PHONY: test
test:
	@docker compose run --rm client pytest

.PHONY: coverage
coverage: 
	@docker compose run --rm client coverage run -m pytest
	@docker compose run --rm client coverage report -m
