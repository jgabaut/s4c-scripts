py_venv="$(PY_VENV_BIN_PATH)"
init:
	@echo -e "Installing dependencies for s4c CLI:\n"
	$(py_venv)/pip install -r requirements.txt
	@echo -e "Done.\n"

install:
	@echo -e "Installing s4c CLI:\n"
	$(py_venv)/pip install .
	@echo -e "Done.\n"

test:
	@echo -e "Running tests:\n"
	#py.test tests
	@echo -e "No tests.\n"
	@echo -e "Done.\n"

all: init install test
.PHONY: all
