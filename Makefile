mak.SILENT:
.PHONY: clean

PORT ?= 8080
MODULE ?= app
DJANGO_APP ?= vessels
PYTHONPATH=$(shell pwd)

ENVIRONMENT_CMD ?= PYTHONPATH="${PYTHONPATH}" pipenv run

DOCKER_PROJECT ?= modec
DOCKER_PARAMS ?= -f docker/ports.yml -f docker/extra.yml
DOCKER_CMD = docker-compose -f docker-compose.yml ${DOCKER_PARAMS} -p ${DOCKER_PROJECT}

SINGLE_FILE_TEST_PATH = "tests/unit/errors/test_client_error.py"

# General
install:
	@pipenv install --deploy

start: clean
	@echo "[STARTING aiohttp LOCAL SERVER 0.0.0.0:$(PORT)]"
	@$(ENVIRONMENT_CMD) gunicorn --chdir ${MODULE} --bind :${PORT} ${MODULE}.wsgi:application

test: 
	@echo "\n\n[RUNNING ${MODULE} TESTS]\n"
	@$(ENVIRONMENT_CMD) python ${MODULE}/manage.py test tests

migrate: 
	@echo "\n\n[RUNNING ${MODULE} MIGRATIONS]\n"
	@$(ENVIRONMENT_CMD) python ${MODULE}/manage.py makemigrations ${DJANGO_APP}
	@$(ENVIRONMENT_CMD) python ${MODULE}/manage.py migrate

test-coverage: test
	@$(ENVIRONMENT_CMD) coverage html --ignore-errors
	@$(ENVIRONMENT_CMD) coverage report --include=$(shell pwd)/* --ignore-errors
	@$(ENVIRONMENT_CMD) codecov --token=${CODECOV_TOKEN}

lint:
	@$(ENVIRONMENT_CMD) pylama ${PYTHONPATH}

clean-coverage:
	@rm -f .coverage
	@rm -rf htmlcov/

# Docker
docker-build:
	@${DOCKER_CMD} build

docker-start: 
	@${DOCKER_CMD} up -d web 

docker-restart:
	@${DOCKER_CMD} restart

docker-test:
	@${DOCKER_CMD} run --rm web make test

docker-logs:
	@${DOCKER_CMD} logs -f --tail=30 web

docker-migrate:
	@${DOCKER_CMD} run --rm web make migrate

docker-test-coverage:
	@${DOCKER_CMD} run --rm web make test-coverage