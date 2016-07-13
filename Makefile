ACTIVATE_VENV = . bin/activate
PYTHON = ./bin/python
PIP = ./bin/pip
VENV := $(shell which virtualenv 2>/dev/null)


bootstrap: ensure-venv-exists cheeseshop

cheeseshop: ensure-venv-exists
	@$(ACTIVATE_VENV) && $(PIP) -q install -r requirements/test.txt

ensure-venv-exists:
ifndef VENV
	$(virtualenv not installed. No Python dependecies will be available.)
else
	@$(VENV) -q . >/dev/null
endif

nuke-venv:
	@rm -rf bin/ include/ lib/ local/
