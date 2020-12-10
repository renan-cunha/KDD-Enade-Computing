.PHONY: raw_data requirements

PYTHON_INTERPRETER = python3
#################################################################################
# COMMANDS                                                                      #
#################################################################################
.DEFAULT_GOAL := raw_data

requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

raw_data: requirements
	mkdir -p data/raw_data/enade_data
	$(PYTHON_INTERPRETER) src/data/download_raw_data.py --path data/raw_data/enade_data

test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

clean:
	rm -rf data/raw_data/enade_data



