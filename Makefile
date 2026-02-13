
PYTHON_VERSION ?= 3.11
CLEAN_VENV ?= 0

.PHONY: install-gfortran install test \
	install-python311 venv311 install311 test311 clean

install-gfortran:
	sudo apt-get -y install gfortran

install-python311:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" python install $(PYTHON_VERSION); \
	"$$UV_BIN" python pin $(PYTHON_VERSION)

venv311: install-python311
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" venv --python $(PYTHON_VERSION) --seed --clear .venv

install311: venv311
	.venv/bin/python -m ensurepip --upgrade
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install "setuptools<60"
	.venv/bin/python -m pip install coveralls "numpy==1.23.5"
	rm -rf build pyhwm2014.egg-info
	.venv/bin/python setup.py develop

test311: install311
	.venv/bin/python -m coverage run --source=. --module unittest discover --start-directory tests --verbose

install:
	pip install "setuptools<60"
	pip install coveralls "numpy==1.23.5"
	rm -rf build pyhwm2014.egg-info
	python setup.py develop

test:
	coverage run --source=. --module unittest discover --start-directory tests --verbose

clean:
	rm -rf build dist pyhwm2014.egg-info
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	rm -f .coverage
	@if [ "$(CLEAN_VENV)" = "1" ]; then rm -rf .venv; fi
