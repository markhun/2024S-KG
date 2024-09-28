VENV := .venv

PYTHON_VERSION_REQ = python3.10  # Also name of the required python executable 
CYPHER_SHELL := cypher-shell  # path to cypher-shell executable
PYTHON_INSTALLED := $(shell command -v $(PYTHON_VERSION_REQ) 2> /dev/null)  # Check if executable is installed
XSV_INSTALLED := $(shell command -v xsv 2> /dev/null)  # Check if executable is installed

.PHONY: dev venv
.PHONY: install
.PHONY: lint flake black
.PHONY: data-prep
.PHONY: import-neo4j-data
.PHONY: clean
.PHONY: clean-neo4j-db-data clean-data-prep

dev: venv install
	@printf "Checking out goodbooks-10k dataset git submodule"
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
		pip install -e './book-recommendations[dev,test,dataprep]'

data-prep:
ifndef XSV_INSTALLED
	$(error "xsv is not available. Please install xsv before executing data preprocessing.")
endif
	cd ./goodbooks-10k && \
	xsv join tag_id tags.csv tag_id book_tags.csv | xsv search -s count "\d{3,}" | xsv select tag_id,goodreads_book_id,count > book_tags_reduced_imm.csv  && \
	xsv join goodreads_book_id book_tags_reduced_imm.csv goodreads_book_id books.csv |  xsv select tag_id,book_id,goodreads_book_id,count > book_tags_reduced.csv && \
	xsv join tag_id tags.csv tag_id book_tags.csv | xsv search -s count "\d{3,}" | xsv select tag_id,tag_name | tail -n +2 | sort | uniq | sort | cat <(echo "tag_id,tag_name") - | xsv sort --select tag_id --numeric > tags_reduced.csv && \
	rm book_tags_reduced_imm.csv

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

import-neo4j-data:
	@echo ">>> Importing data into neo4j relies on cypher-shell being installed on this sytem!"
	# sudo cp ./data/*.csv ./neo4j_db/import/
	cat ./data/cypher-scripts/data-importer.cypher | $(CYPHER_SHELL) -u neo4j -p password
	cat ./data/cypher-scripts/split-authors.cypher | $(CYPHER_SHELL) -u neo4j -p password
	cat ./data/cypher-scripts/split-genres.cypher  | $(CYPHER_SHELL) -u neo4j -p password
	@echo ">>> The database now contains the following numbers of nodes:"
	$(CYPHER_SHELL) -u neo4j -p password <<< "match (n) return labels(n) as label, count(*)"

clean: clean-neo4j-db-data clean-data-prep
	rm -rf $(VENV)
	rm -rf ./src/*.egg-info
	rm -rf ./*/.pytest_cache
	@echo
	@echo "Run 'deactivate' to exit virtual environment"

clean-neo4j-db-data:
	sudo rm -rf ./neo4j_db/*/*

clean-data-prep:
	rm -f ./goodbooks-10k/book_tags_reduced.csv
	rm -f ./goodbooks-10k/tags_reduced.csv