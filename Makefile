.PHONY: create_env download_data extract_data select_data pre_process_data transform_data all download_and_process run_analisys

PYTHON_INTERPRETER = python3
#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Create environment
create_env:
	 conda env create -f environment.yml
	
## Download data
download_data: 
	@echo "This whole script takes a few minutes, go grab a coffee :)"
	@mkdir -p data/raw_data/enade_data
	$(PYTHON_INTERPRETER) src/get_data/get_raw_data.py --data_path data/raw_data/enade_data --download

## Extract data from zip to csv
extract_data:
	$(PYTHON_INTERPRETER) src/get_data/get_raw_data.py --data_path data/raw_data/enade_data --manuals_path references/ --extract

## Select Computer Science data from CSVs
select_data:
	@echo "Selecting Computer Science data"
	$(PYTHON_INTERPRETER) src/selection/select_data.py
	@echo "Selection completed"

## Pre-process data from Computer Science CSVs
pre_process_data:
	@echo "Pre-processing data"
	$(PYTHON_INTERPRETER) src/pre_processing/pre_process.py
	@echo "Pre-processing completed"

## Transform data from Processed CSVs
transform_data:
	@echo "Transforming data"
	$(PYTHON_INTERPRETER) src/transformation/transform.py
	@echo "Data transformed"

run_analysis:
	@echo "Running Analisys"
	mkdir -p results/
	papermill notebooks/subject_analysis.ipynb results/subject_analysis.ipynb -r CODE_COURSE $(code_course)
	papermill notebooks/difficulty.ipynb results/difficulty.ipynb -r CODE_COURSE $(code_course)
	papermill notebooks/type_exam.ipynb results/type_exam.ipynb -r CODE_COURSE $(code_course)
	papermill notebooks/absent_and_blank.ipynb results/absent_and_blank.ipynb -r CODE_COURSE $(code_course)

## Run all necessary comamnds
all: download_data extract_data select_data pre_process_data transform_data run_analisys
	@echo "Done"

download_and_process: download_data extract_data select_data pre_process_data transform_data
	@echo "Done"

## remove data files
clean:
	rm -rf data/raw_data/enade_data
	rm -rf data/selected_data
	rm -rf data/processed_data




.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')


