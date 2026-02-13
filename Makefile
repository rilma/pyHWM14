
.PHONY: install-gfortran install test install-python310 venv310 install310 test310

install-gfortran:
	sudo apt-get -y install gfortran

install-python310:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" python install 3.10; \
	"$$UV_BIN" python pin 3.10

venv310: install-python310
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" venv --python 3.10 --seed --clear .venv

install310: venv310
	.venv/bin/python -m ensurepip --upgrade
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install "setuptools<60"
	.venv/bin/python -m pip install coveralls "numpy==1.23.5"
	rm -rf build pyhwm2014.egg-info
	.venv/bin/python setup.py develop

test310: install310
	.venv/bin/python -m coverage run --source=. --module unittest discover --start-directory tests --verbose

install:
	pip install "setuptools<60"
	pip install coveralls "numpy==1.23.5"
	rm -rf build pyhwm2014.egg-info
	python setup.py develop

test:
	coverage run --source=. --module unittest discover --start-directory tests --verbose
