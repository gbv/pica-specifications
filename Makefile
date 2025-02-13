docs:
	quarto render

preview:
	quarto preview

deps:
	python -m venv .venv
	.venv/bin/pip install -r tests/requirements.txt

suite:
	tests/run-suite.sh
