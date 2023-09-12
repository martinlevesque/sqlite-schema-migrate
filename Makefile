
test-unit:
	python -m pytest

test-unit-on-change:
	find . -name '*.py' | entr python -m pytest

test-end-to-end:
	bash tests/end_to_end.sh

test-all: test-unit test-end-to-end
