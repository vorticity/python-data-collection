SHELL := /bin/bash
PYTHON_EXECUTABLE := python3.11

VENV ?= .venv

VENV_FLAKE8 := $(VENV)/bin/flake8
VENV_PIP := $(VENV)/bin/pip
VENV_PIPENV := $(VENV)/bin/pipenv
VENV_PYTEST := $(VENV)/bin/pytest
VENV_PYTHON := $(VENV)/bin/$(PYTHON_EXECUTABLE)
VENV_UVICORN := $(VENV)/bin/uvicorn

.PHONY: all install virtualenv run test

all: install

install: virtualenv

virtualenv: $(VENV)/.virtualenv-touchfile

$(VENV)/.virtualenv-touchfile: Pipfile.lock
	$(VENV_PIPENV) install --dev
	touch $@

Pipfile.lock: Pipfile
	$(VENV_PIPENV) lock
	touch $@

Pipfile: .pipenv-touchfile

.pipenv-touchfile: $(VENV)/bin/activate
	$(VENV_PIP) install --upgrade pipenv
	touch .pipenv-touchfile

$(VENV)/bin/activate:
	@test -f $(VENV)/bin/activate || $(PYTHON_EXECUTABLE) -m venv --symlinks --upgrade-deps $(VENV)

run: install
	$(VENV_UVICORN) main:app --reload --host 0.0.0.0

generate_requirements_txt: requirements.txt

requirements.txt: install 
	$(VENV_PIPENV) requirements --dev  > requirements.txt

test: install
	PYTHONPATH=$PYTHONPATH:. db_path=":memory:" $(VENV_PYTEST) -vv tests/

lint: install
	$(VENV_FLAKE8) --ignore .venv data_collection/ main.py

clean:
	rm -f test.db database.db .virtualenv-touchfile .pipenv-touchfile
	rm -rf .venv
