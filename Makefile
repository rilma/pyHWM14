
# Python 3.13+ with scikit-build-core + CMake + f2py (Meson backend)
# Minimum Python 3.13 required (see GitHub issue #11: numpy.distutils deprecation)
# For Python 3.12 or earlier support, use git tag v1.1.0

CLEAN_VENV ?= 0
export UV_LINK_MODE = copy

.PHONY: install-gfortran install test \
	install-python313 venv313 install313-sci test313 clean

install-gfortran:
	sudo apt-get -y install gfortran

install-python313:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" python install 3.13; \
	"$$UV_BIN" python pin 3.13

venv313: install-python313
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" venv --python 3.13 --seed --clear .venv313

install313-sci: venv313
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" pip install --python .venv313/bin/python --upgrade pip; \
	"$$UV_BIN" pip install --python .venv313/bin/python scikit-build-core cmake ninja numpy meson pytest
	rm -rf build dist pyhwm2014.egg-info
	@UV_BIN="$${HOME}/.local/bin/uv"; \
	if command -v uv >/dev/null 2>&1; then UV_BIN="$$(command -v uv)"; fi; \
	"$$UV_BIN" pip install --python .venv313/bin/python -e .

test313: install313-sci
	.venv313/bin/python -m pytest tests/ -v --tb=short

install: install-python313 install313-sci

test: test313

clean:
	rm -rf build dist pyhwm2014.egg-info
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	rm -f .coverage
	@if [ "$(CLEAN_VENV)" = "1" ]; then rm -rf .venv .venv313; fi
