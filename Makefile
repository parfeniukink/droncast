# This file includes application scripts that could be used
# by developers for any purposes.

# Dependency management
# -------------------------------------------------------------------------
.PHONY: lock 				# pin main dependencies
lock:
	python -m piptools compile -o requirements/main.txt
	python -m piptools compile --extra=dev -o requirements/dev.txt


.PHONY: install				# sync for dev dependencies
install:
	python -m piptools sync requirements/dev.txt


.PHONY: install.prod 		# sync for prod dependencies
install.prod:
	python -m piptools sync requirements/main.txt


.PHONY: upgrade  			# upgrade dependencies (generate new .txt files)
upgrade:
	python -m piptools compile --upgrade -o requirements/main.txt
	python -m piptools compile --extra dev --upgrade -o requirements/dev.txt




# Application entrypoint
# -------------------------------------------------------------------------
.PHONY: run					# run with Uvicorn
run:
	uvicorn src.main:app --reload

.PHONY: run.prod			# run with Gunicorn
run.prod:
	gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker


# Tests
# -------------------------------------------------------------------------
.PHONY: test
test:
	python -m pytest ./tests


# Code quality
# -------------------------------------------------------------------------
.PHONY: quality				# fix files with quality checkers
quality:
	python -m black .
	python -m isort .


.PHONY: check				# run quality checkers without chaning files
check:
	python -m flake8 .
	python -m isort --check .
	python -m black --check .
	python -m mypy --check-untyped-defs


