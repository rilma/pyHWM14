
# Python 3.12+ with scikit-build-core + CMake + f2py (Meson backend)
# Minimum Python 3.12 required (see GitHub issue #11: numpy.distutils deprecation)
# For Python 3.11 or earlier support, use git tag v1.0.x

CLEAN_VENV ?= 0

.PHONY: install-gfortran install test \
	install-python312 venv312 install312-sci test312 clean

install-gfortran:
	sudo apt-get -y install gfortran

install-python312:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" python install 3.12; \
	"$$UV_BIN" python pin 3.12

venv312: install-python312
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" venv --python 3.12 --seed --clear .venv312

install312-sci: venv312
	.venv312/bin/python -m ensurepip --upgrade
	.venv312/bin/python -m pip install --upgrade pip
	.venv312/bin/python -m pip install scikit-build-core cmake ninja numpy
	rm -rf build dist pyhwm2014.egg-info
	.venv312/bin/pip install -e .

test312: install312-sci
	.venv312/bin/python -m unittest discover -s tests --verbose

install: install-python312 install312-sci

test: test312

clean:
	rm -rf build dist pyhwm2014.egg-info
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	rm -f .coverage
	@if [ "$(CLEAN_VENV)" = "1" ]; then rm -rf .venv .venv312; fi
