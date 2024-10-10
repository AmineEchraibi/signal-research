## VARS

$(info [Makefile] Loading commons variables from env/base.env ...)
include env/base.env


## HELP

.DEFAULT_GOAL:=help
help: ## list all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


# INSTALL

isset-%: ## Test if variable % is set or exit with error.
	# @: $(if $(value $*),,$(error Variable $* is not set))


init-install: install-dev install-hooks

# INSTALLERS

install-dev: ## Install the project in dev mode.
	poetry install

install-prod: ## Install the project in prod mode.
	poetry install --only main

install-hooks: ## Install the project commit hooks.
	poetry run pre-commit install

# CLEANERS

clean-packages: ## Clean the project packages.
	rm -rf dist/

clean-reports: ## Clean the project generated reports.
	rm -rf reports/*.*

clean-coverage: ## Clean the project generated coverage.
	rm -f .coverage*

clean-python: ## Clean the Python caches.
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -delete

clean-caches: ## Clean the project caches.
	rm -f .coverage
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/

clean-install: ## Clean the project install.
	rm -rf .venv/
	rm -f poetry.lock

cleaners: clean-install clean-caches clean-python clean-packages clean-reports clean-coverage

## DOCUMENTERS

document-api: ## Document the project API.
	poetry run sphinx-apidoc -o docs/source/_api src/*

document-%: ## Document the project in format %.
	poetry run sphinx-build -b $* docs/source docs/build

documenters: clean-docs document-api document-html ## Run all the documenter

## BUILDERS

build-%: ## Build package for format %.
	poetry build --format=$*

builders: build-wheel
## CHECKERS

check-types: ## Check the project code types with mypy.
	poetry run mypy src/
	# Need to do this to have separate fixture files
	poetry run mypy --no-namespace-packages tests

check-tests: ## Check the project unit tests with pytest.
	poetry run pytest -n auto tests/

check-format: ## Check the project code format with isort and black.
	poetry run isort --check src/ tests/
	poetry run black --check src/ tests/

check-poetry: ## Check the project pyproject.toml with poetry.
	poetry chec

check-docker: ## Check the project docker image with hadolint.
	hadolint --config=docker/hadolint.yaml docker/Dockerfile.*

check-quality: ## Check the project code quality with pylint.
	poetry run pylint --recursive=y --fail-under 9.0 src/ tests/


check-coverage: ## Check the project test coverage with coverage.
	$(eval SYS_ARCH := $(shell uname -m))
	@if [ $(SYS_ARCH) = "arm64" ]; then \
		PYTORCH_ENABLE_MPS_FALLBACK=1 poetry run pytest -n auto --cov-report term-missing --cov=src/ tests/; \
	else \
		poetry run pytest -n auto --cov=src/ tests/; \
	fi

checkers: check-types check-format check-poetry check-quality check-coverage

## REPORTERS

report-tests: ## Generate the project unit test report.
	poetry run pytest -n auto --junitxml=reports/pytest.xml tests/

report-quality: ## Generate the project quality report.
	poetry run pylint --recursive=y --output-format=parseable src/ tests/ | tee reports/pylint.txt

# report-security: ## Generate the project security report.
# 	# -ll: MEDIUM level, -ii = MEDIUM confidence
# 	poetry run bandit --recursive -ll -ii --format=xml --output=reports/bandit.xml src/

report-coverage: ## Generate the project test coverage report.
	poetry run pytest -n auto --cov=. --cov-report=xml:reports/coverage.xml tests/

report-dependencies: ## Generate the project dependencies report.
	poetry export --without-hashes --output=reports/requirements.txt

reporters: report-tests report-quality report-coverage report-dependencies ## Run all the reporters.

## FORMATTERS

format-imports: ## Format the project imports with isort.
	poetry run isort src/ tests/

format-sources: ## Format the project sources with black.
	poetry run black src/ tests/

formatters: format-imports format-sources ## Run all the formatters.

# BUMP PYTHON VERSION

bump-python-version: isset-PYTHON_VERSION ## Bump the python version installed.
	echo "$(PYTHON_VERSION)" > .python-version

bump-init-file: isset-PACKAGE_VERSION ## Bump the package version of the project in the __init__ file.
	sed -i.bak 's/^__version__ = .*/__version__ = "$(PACKAGE_VERSION)"/' src/trading_middlewares/__init__.py && rm src/trading_middlewares/__init__.py.bak

bump-package-project: isset-PACKAGE_VERSION ## Bump the package version of the project.
	sed -i.bak 's/^version = .*/version = "$(PACKAGE_VERSION)"/' pyproject.toml && rm pyproject.toml.bak

bump-package: bump-init-file bump-package-project

# Publish
publish:
	twine upload --repository-url http://localhost:8080/ -u server -p server dist/*


VENV_PATH := .venv
install-local-packages:
	# Ensure a local package path is provided
	@if [ -z "$(LOCAL_PACKAGE_PATH)" ]; then \
		echo "Error: LOCAL_PACKAGE_PATH is not set."; \
		exit 1; \
	fi; \
	# Extract the package name from the local package path (last element of the path)
	# Uninstall the existing package if already installed
	poetry remove $$(basename $(LOCAL_PACKAGE_PATH)) || true; \
	# Install the local package in editable mode using Poetry
	poetry add --editable $(LOCAL_PACKAGE_PATH)
