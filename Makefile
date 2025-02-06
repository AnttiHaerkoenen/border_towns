#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = border_towns
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
.PHONY: requirements
requirements:
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 border_towns
	isort --check --diff --profile black border_towns
	black --check --config pyproject.toml border_towns

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml border_towns

## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	conda env create --name $(PROJECT_NAME) -f environment.yml
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Keywords-in-context analysis
.PHONY: kwic
kwic:
	# Kexholm 1659-1699
	python ./border_towns/utils/kwic.py ./data/external/Kexholm ./data/raw/Kexholm/debt ./wordlists/debt --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Kexholm ./data/raw/Kexholm/trade ./wordlists/trade --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Kexholm ./data/raw/Kexholm/transport ./wordlists/transport --window_size 100
	# Brahea 1668-1679
	python ./border_towns/utils/kwic.py ./data/external/Brahea ./data/raw/Brahea/debt ./wordlists/debt --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Brahea ./data/raw/Brahea/trade ./wordlists/trade --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Brahea ./data/raw/Brahea/transport ./wordlists/transport --window_size 100

## Build network
.PHONY: network
network:
	python ./border_towns/data/build_network.py main \
	./data/external/testi/toimijat.csv ./data/external/testi/yhteydet.csv \
	./data/interim/verkosto.csv toimija_tunnus toimija_tunnus_1 toimija_tunnus_2

## Visualize a network of relations
.PHONY: plot_network
plot_network: network
	python ./border_towns/visualize/plot_network.py main \
		./data/interim/verkosto.csv \
		./reports/figures/sortavala.png \
		nimi_source nimi_target "suhde in ['velka', 'omistaja', 'operaattori']"

## Visualize database
.PHONY: plot_db
plot_db:
	plantuml references/original_data.uml

## Combine multiple files into one
.PHONY: combine_pages
combine_pages:
	sh ./border_towns/utils/combine-pages.sh ./data/external/Kexholm ./data/external/Kexholm_1659_1699.txt
	sh ./border_towns/utils/combine-pages.sh ./data/external/Brahea ./data/external/Brahea_1668_1679.txt

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
