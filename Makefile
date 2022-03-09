export PYTHONPATH=$(shell pwd)/src/
export PYTHONDONTWRITEBYTECODE=1
export SECRET_KEY=FAKE_SECRET_KEY

ifndef DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=labqoda.settings.test
endif

.PHONY=help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean: ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

###
# Dependencies section
###
_base_pip:
	@pip install -U pip poetry wheel

conf-env:	## Generate the .env file for local development
	@cp -n contrib/localenv .env

dev-dependencies: _base_pip ## Install development dependencies
	@poetry install

ci-dependencies: _base_pip
	@poetry export --without-hashes --dev -f requirements.txt > requirements.txt
	@pip install -r requirements.txt

dependencies: _base_pip ## Install dependencies
	@poetry install --no-dev

outdated: ## Show outdated packages
	@poetry show --outdated


###
# Lint section
###
_flake8:
	@flake8 --show-source src/

_isort:
	@isort --check-only src/

_black:
	@black --check src/

_isort-fix:
	@isort src/

_black_fix:
	@black src/

_dead_fixtures:
	@pytest --dead-fixtures

_mypy:
	@mypy src/

detect_missing_migrations:  ## Detect missing model migration
	@python src/manage.py makemigrations --dry-run | grep -q "No changes detect"

validate_openapi_schema:  ## Validate Openapi Schema
	@python src/manage.py spectacular --fail-on-warn --validate 1> /dev/null

lint: _flake8 _isort _black _dead_fixtures detect_missing_migrations  ## Check code lint
format-code: _isort-fix _black_fix  ## Format code


###
# Tests section
###
test: clean ## Run tests
	@pytest src/

test-coverage: clean ## Run tests with coverage output
	@pytest src/ --cov . --cov-report term-missing --cov-report xml

test-debug: clean ## Run tests with active pdb
	@pytest -s -x src/

test-matching: clean ## Run tests by match ex: make test-matching k=name_of_test
	@pytest -s -k $(k) src/

###
# Shell section
###
shell:  ## Run repl with development settings
	@python src/manage.py shell


###
# Run section
###
run-prod:  ## Run server with prod settings 
	@python src/manage.py migrate --no-input
	@gunicorn --log-level INFO --workers 3 --bind 0.0.0.0:8080 labqoda.wsgi:application


run-dev: ## Run server with development settings
	@python src/manage.py migrate --no-input --settings labqoda.settings.development
	@python src/manage.py runserver 0.0.0.0:8080 --settings labqoda.settings.development

###
# Manage section
###
manager: ## Run a django manage ex: make manager args=makemigrations
	@python src/manage.py $(args)

collectstatic:  ## Run collectstatic
	@python src/manage.py collectstatic --no-input

migrate-oauth:
	@python src/manage.py migrate oauth2_provider
