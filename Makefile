SHELL := /bin/bash

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

venv:
	./tools/create_venv.sh

lint:
	@echo "*********** YAMLLINT"
	@yamllint -c=.yamllint.yml . || true
	@echo "*********** BLACK"
	@black . || true
	@echo "*********** FLAKE8"
	@flake8 . || true
	@echo "*********** MYPY"
	@mypy . || true

test:
	@sudo .venv/bin/python3 -m pytest -rP

pyclean:
	@find . \
    | grep -E '(__pycache__|\.hypothesis|\.perm|\.cache|\.static|\.py[cod]$)' \
    | xargs rm -rf \
  || true

docker_build:
	@echo "*********** DOCKER: Build image"
	@docker-compose -f docker-compose-dev.yml build
	@echo "*********** Creating test images"
	@docker-compose -f docker-compose-dev.yml run --rm -u root app bash -c "/letsdare/tools/create_test_images.sh"

docker_lint:
	@docker-compose -f docker-compose-dev.yml run --rm app sh -c '\
		echo "*********** YAMLLINT" && \
		yamllint -c=.yamllint.yml . || true && \
		echo "*********** BLACK" && \
		black . || true && \
		echo "*********** FLAKE8" && \
		flake8 . || true && \
		echo "*********** MYPY" && \
		mypy . || true \
	 '

docker_test:
	@docker-compose -f docker-compose-dev.yml run --rm -u root app bash -c "pytest -rP"
