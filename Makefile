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
	conda env update --name $(PROJECT_NAME) --file requirements.txt --prune

## Save env to text file
.PHONY: save_env
save_env:
	conda list --explicit > requirements.txt

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
	conda env create --name $(PROJECT_NAME) -f requirements.txt
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
	python ./border_towns/utils/kwic.py ./data/external/Kexholm ./data/raw/Kexholm/family ./wordlists/family --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Kexholm ./data/raw/Kexholm/places ./wordlists/places --window_size 100
	# Brahea 1668-1679
	python ./border_towns/utils/kwic.py ./data/external/Brahea ./data/raw/Brahea/debt ./wordlists/debt --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Brahea ./data/raw/Brahea/trade ./wordlists/trade --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Brahea ./data/raw/Brahea/transport ./wordlists/transport --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Brahea ./data/raw/Brahea/family ./wordlists/family --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Brahea ./data/raw/Brahea/places ./wordlists/places --window_size 100
	# Sordavala 1673-1699
	python ./border_towns/utils/kwic.py ./data/external/Sordavala ./data/raw/Sordavala/debt ./wordlists/debt --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Sordavala ./data/raw/Sordavala/trade ./wordlists/trade --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Sordavala ./data/raw/Sordavala/transport ./wordlists/transport --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Sordavala ./data/raw/Sordavala/family ./wordlists/family --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Sordavala ./data/raw/Sordavala/places ./wordlists/places --window_size 100
	# Nyen 1684-1699
	python ./border_towns/utils/kwic.py ./data/external/Nyen ./data/raw/Nyen/debt ./wordlists/debt --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Nyen ./data/raw/Nyen/trade ./wordlists/trade --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Nyen ./data/raw/Nyen/transport ./wordlists/transport --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Nyen ./data/raw/Nyen/family ./wordlists/family --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Nyen ./data/raw/Nyen/places ./wordlists/places --window_size 100
	# Kajana 1659-1699
	python ./border_towns/utils/kwic.py ./data/external/Kajana ./data/raw/Kajana/debt ./wordlists/debt --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Kajana ./data/raw/Kajana/trade ./wordlists/trade --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Kajana ./data/raw/Kajana/transport ./wordlists/transport --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Kajana ./data/raw/Kajana/family ./wordlists/family --window_size 100
	python ./border_towns/utils/kwic.py ./data/external/Kajana ./data/raw/Kajana/places ./wordlists/places --window_size 100

## Build network
.PHONY: network
network:
	python ./border_towns/data/build_network.py main \
	./data/interim/csv/henkilot_Kexholm.csv ./data/interim/csv/yhteydet_Kexholm.csv \
	./data/interim/csv/verkosto_Kexholm.csv \
	hlotunnus henkilo_source henkilo_target \
	./data/raw/duplicates.yaml --duplicates

## Visualize a network of relations
.PHONY: plot_network
plot_network:
	python ./border_towns/visualize/plot_network.py main \
		./data/interim/csv/verkosto_Kexholm.csv \
		./reports/figures/kexholm.png \
		nimi_source nimi_target "tyyppi in ['kauppa']"

## Visualize database
.PHONY: plot_db
plot_db:
	plantuml references/original_data.uml

## Combine multiple files into one
.PHONY: combine_pages
combine_pages:
	sh ./border_towns/utils/combine-pages.sh ./data/external/Kexholm ./data/external/Kexholm_1659_1699.txt
	sh ./border_towns/utils/combine-pages.sh ./data/external/Brahea ./data/external/Brahea_1668_1679.txt
	sh ./border_towns/utils/combine-pages.sh ./data/external/Kajana/RO_1659_1699 ./data/external/Kajana_1659_1699.txt
	sh ./border_towns/utils/combine-pages.sh ./data/external/Sordavala/s1 ./data/external/Sordavala_s1.txt
	sh ./border_towns/utils/combine-pages.sh ./data/external/Sordavala/s2 ./data/external/Sordavala_s2.txt
	sh ./border_towns/utils/combine-pages.sh ./data/external/Sordavala/s3 ./data/external/Sordavala_s3.txt
	sh ./border_towns/utils/combine-pages.sh ./data/external/Nyen/RO_1697 ./data/external/Nyen_RO_1697.txt

## Turn xlsx to csv
.PHONY: csv
csv:
	python ./border_towns/utils/xlsx_to_csv.py ./data/interim/xlsx/henkilot_Kexholm.xlsx ./data/interim/csv/henkilot_Kexholm.csv
	python ./border_towns/utils/xlsx_to_csv.py ./data/interim/xlsx/yhteydet_Kexholm.xlsx ./data/interim/csv/yhteydet_Kexholm.csv

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
