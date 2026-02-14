"""Development setup guide for pyHWM14.

This document outlines recommended practices for contributing to pyHWM14.
"""

# Contributing to pyHWM14

## Development Setup

### Requirements
- Python 3.13+
- Git
- CMake 3.15+
- Fortran compiler (gfortran)

### Setup Virtual Environment

```bash
# Install Python 3.13 using uv (recommended)
make install-python313

# Create virtual environment
make venv313

# Install development dependencies
make install313-sci

# Activate environment
source .venv313/bin/activate
```

### Running Tests

```bash
# Run all tests
make test313

# Or using pytest directly
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=pyhwm2014 --cov-report=html
```

## Code Quality

### Type Checking

```bash
# Run mypy type checker
mypy pyhwm2014

# Run ruff linter/formatter
ruff check pyhwm2014
ruff format pyhwm2014

# Run black formatter
black pyhwm2014
```

### Code Style

The project follows:
- **Type Hints**: PEP 484 style hints (Python 3.13+ syntax)
- **Formatting**: Black (100 character line length)
- **Linting**: Ruff with E, F, W, I, UP, B, C4 rules
- **Docstrings**: NumPy format (RST style)

Example:
```python
from typing import Literal

def calculate_profile(
    option: Literal[1, 2, 3, 4] = 1,
    verbose: bool = True,
) -> None:
    """Calculate atmospheric wind profile.
    
    Parameters
    ----------
    option : Literal[1, 2, 3, 4], optional
        Profile type selection. Default is 1.
    verbose : bool, optional
        Print debug output. Default is True.
    """
```

## Project Structure

```
pyhwm2014/
  __init__.py      # Package entry point with exports
  core.py          # HWM14 and HWM142D model classes
  plotting.py      # HWM14Plot and HWM142DPlot visualization
  data.py          # Data path configuration
  py.typed         # PEP 561 type hint marker
  data/            # Model data files (binary, dat)

tests/
  conftest.py      # Pytest fixtures and configuration
  test_core.py     # Core module tests
  test_plotting.py # Plotting module tests
```

## Build System

### Modern Build Stack
- **Build System**: scikit-build-core (CMake + Meson + f2py)
- **Configuration**: `pyproject.toml` + `CMakeLists.txt` + `meson.build`
- **Python Support**: 3.13+
- **NumPy**: ≥1.26 (modern NumPy with f2py support)

### Building from Source

```bash
# Python 3.13 development install
pip install -e .

# Build wheel
python -m build

# Clean build artifacts
make clean
```

## Before Submitting a PR

1. **Run tests**: `pytest tests/ -v`
2. **Check types**: `mypy pyhwm2014`
3. **Format code**: `black pyhwm2014 && ruff check --fix pyhwm2014`
4. **Update CHANGELOG.md** with your changes
5. **Add tests** for new features
6. **Document** public APIs with docstrings

## Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create git tag: `git tag vX.Y.Z`
5. Push to main: `git push origin main --tags`
6. GitHub Actions will build and publish to PyPI automatically

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError: No module named 'pyhwm2014.hwm14'`, 
the Fortran extension needs to be built:
```bash
pip install -e .
```

### Type Checking Errors
Update mypy stubs if needed:
```bash
mypy --install-types
```

### Build Failures
Ensure build dependencies are installed:
```bash
pip install scikit-build-core cmake ninja numpy meson
```

## Questions?

Open an issue on [GitHub](https://github.com/rilma/pyHWM14/issues)
or check the [README](README.rst).
