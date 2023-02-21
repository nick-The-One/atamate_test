init: install-poetry
	poetry install

install-poetry:
	python3 -m pip install --upgrade poetry

test:
	poetry run pytest -vv
