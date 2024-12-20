initialize_git:
	@echo "Initializing git..."
	git init

install:
	@echo "Installing..."
	poetry install --no-root

activate:
	@echo "Activating virtual environment"
	poetry shell

setup_precommit:
	@echo "Setting up pre-commit"
	pre-commit install

setup: initialize_git install activate setup_precommit

pretest:
	@echo "Init test db"
	poetry run bash ./pretest.sh

test: pretest
	@echo "Running tests"
	poetry run pytest

testcov: pretest
	@echo "Running tests with generating test coverage xml"
	poetry run pytest --cov --cov-report=xml

testcov_re: pretest
	@echo "Running test with generating test coverage report html"
	poetry run pytest --cov --cov-report=html:coverage_re

format:
	@echo "Formatting code using Black"
	poetry run black .

precommit:
	@echo "Running Pre-commit"
	poetry run pre-commit run --all-files

## Delete all compiled Python files
clean:
	@echo "Cleaning up the repo"
	find . -type f -name "*.py[co]" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
