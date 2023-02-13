.PHONY: all develop test lint clean doc format
.PHONY: clean clean-build clean-pyc clean-test coverage dist docs install lint lint/flake8

# The package name
PKG=pagic


all: test lint

#
# Setup
#

## install development dependencies and pre-commit hook
develop: install-deps activate-pre-commit configure-git

install-deps:
	@echo "--> Installing dependencies"
	pip install -U pip setuptools wheel
	poetry install

activate-pre-commit:
	@echo "--> Activating pre-commit hook"
	pre-commit install

configure-git:
	@echo "--> Configuring git"
	git config branch.autosetuprebase always


#
# testing & checking
#

## Run tests quickly
test:
	@echo "--> Running Python tests"
	pytest -x -p no:randomly
	@echo ""

test-randomly:
	@echo "--> Running Python tests in random order"

## Run tests with coverage
test-with-coverage:
	@echo "--> Running Python tests"
	pytest --cov $(PKG)
	@echo ""

## Run tests with typeguard
test-with-typeguard:
	@echo "--> Running Python tests with typeguard"
	pytest --typeguard-packages=${PKG}
	@echo ""


## remove test and coverage artifacts##
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

## Check style and annotation
lint:
	adt all

#
# Formatting
#

## Format code
format: format-py format-js

format-py:
	docformatter -i -r src
	black --target-version py310 src tests
	isort src tests

format-js:
	echo "TODO"


#
# Everything else
#
help:
	@inv help-make

install:
	poetry install

doc: doc-html doc-pdf

doc-html:
	sphinx-build -W -b html docs/ docs/_build/html

doc-pdf:
	sphinx-build -W -b latex docs/ docs/_build/latex
	make -C docs/_build/latex all-pdf

## Clean up repo
clean:
	rm -f **/*.pyc
	find . -type d -empty -delete
	rm -rf *.egg-info *.egg .coverage .eggs .cache .mypy_cache .pyre \
		.pytest_cache .pytest .DS_Store  docs/_build docs/cache docs/tmp \
		dist build pip-wheel-metadata junit-*.xml htmlcov coverage.xml

## Cleanup harder
tidy: clean
	rm -rf .tox .nox .dox .travis-solo
	rm -rf node_modules
	rm -rf instance

## Update dependencies
update-deps:
	pip install -U pip setuptools wheel
	poetry update

## Publish to PyPI
publish: clean
	git push --tags
	poetry build
	twine upload dist/*
