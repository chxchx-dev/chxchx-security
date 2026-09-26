.PHONY: venv install test check integration doctor clean

venv:
	python3 -m venv .venv

install:
	.venv/bin/pip install -e . pytest

test:
	.venv/bin/pytest

check: test
	bash -n install-fedora.sh

integration:
	CHXSEC_RUN_LIVE_TESTS=1 .venv/bin/pytest tests/integration

doctor:
	.venv/bin/chxsec doctor

clean:
	rm -rf build dist .pytest_cache .coverage
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
