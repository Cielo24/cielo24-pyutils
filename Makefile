ACTIVATE_VENV = . bin/activate
PYTHON = ./bin/python
PIP = ./bin/pip
VENV := $(shell which virtualenv 2>/dev/null)

.PHONY: bootstrap \
	cheeseshop \
	coverage-report \
	create-coverage-html
	ensure-venv-exists \
	flake8 \
	isort \
	isort-check \
	nuke-venv \
	test


bootstrap: nuke-venv ensure-venv-exists cheeseshop

cheeseshop: ensure-venv-exists
	@$(ACTIVATE_VENV) && $(PIP) -q install -r requirements/test.txt

coverage-report:
	@$(ACTIVATE_VENV) && coverage report -m

create-coverage-html:
	@$(ACTIVATE_VENV) && coverage html

ensure-venv-exists:
ifndef VENV
	$(virtualenv not installed. No Python dependecies will be available.)
else
	@$(VENV) -q . >/dev/null
endif

flake8: ensure-venv-exists
	@$(ACTIVATE_VENV) && flake8 cielo24_utils

isort:
	@$(ACTIVATE_VENV) && isort -rc cielo24_utils

isort-check:
	@$(ACTIVATE_VENV) && isort -rc cielo24_utils -c -vb --diff --verbose

nuke-venv:
	@rm -rf bin/ include/ lib/ local/

test: ensure-venv-exists flake8 isort-check
	@$(ACTIVATE_VENV) && py.test --cov-config .coveragerc --cov=cielo24_utils cielo24_utils/
