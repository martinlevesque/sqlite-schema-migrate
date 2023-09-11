
pytest:
	python -m pytest

pytest-on-change:
	find . -name '*.py' | entr python -m pytest
