.PHONY: export-dependencies
export-dependencies:
	poetry export -o requirements.txt
	poetry export -o requirements.txt --only dev
