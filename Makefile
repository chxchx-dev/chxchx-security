.PHONY: venv install test check doctor clean

venv:
	python3 -m venv .venv

install:
	.venv/bin/pip install -e . pytest

test:
	.venv/bin/pytest

check: test
	bash -n install-fedora.sh

doctor:
	.venv/bin/chxsec doctor

clean:
	rm -rf build dist .pytest_cache .coverage
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
