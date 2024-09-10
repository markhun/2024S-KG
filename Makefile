VENV := .venv

PYTHON_VERSION_REQ = python3.10
PYTHON_INSTALLED := $(shell command -v $(PYTHON_VERSION_REQ) 2> /dev/null)

.PHONY: dev venv
.PHONY: install
.PHONY: lint flake black
.PHONY: clean
.PHONY: clean-neo4j-db-data:

dev: venv install
	@printf "Checkking out goodbooks-10k git submodule"
	git submodule update --init --recursive
	@printf "\n\nDevelopment Environment is now setup\n"
	@printf "Run 'source $(VENV)/bin/activate' to enter virtual environment\n"

venv: 
ifndef PYTHON_INSTALLED
	$(error "$(PYTHON_VERSION_REQ) is not available. Please install $(PYTHON_VERSION_REQ)")
endif
	@$(PYTHON_VERSION_REQ) -m venv $(VENV)

install:
	@. $(VENV)/bin/activate && \
		pip install -e './book-recommendations[dev,test]'

test:
	@. $(VENV)/bin/activate && \
		pytest

lint: isort black

black:
	@. $(VENV)/bin/activate && \
		black . 

isort:
	@. $(VENV)/bin/activate && \
		isort . --profile black

clean:
	rm -rf $(VENV)
	rm -rf ./src/*.egg-info
	rm -rf ./*/.pytest_cache
	rm -rf ./neo4j_db/*/*
	@echo
	@echo "Run 'deactivate' to exit virtual environment"

clean-neo4j-db-data:
	sudo rm -rf ./neo4j_db/*/*