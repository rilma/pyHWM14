# Python Code Organization Improvements for pyHWM14

## Summary of Changes

This document outlines the code organization improvements made to prepare pyHWM14 for PyPI release with Python 3.13 support.

### 1. Module Reorganization ✅

**Before**: Monolithic 936-line `__init__.py` file  
**After**: Modular architecture with separated concerns

**New file structure**:
```
pyhwm2014/
├── __init__.py      # Clean package entry point (14 lines)
├── core.py          # HWM14 & HWM142D model classes (850+ lines)
├── plotting.py      # HWM14Plot & HWM142DPlot visualization (600+ lines)
├── data.py          # Data path configuration (10 lines)
└── py.typed         # PEP 561 type marker file
```

**Benefits**:
- Improved code organization and maintainability
- Clearer separation of concerns
- Better IDE support and autocomplete
- Easier to test individual components
- Reduced cognitive load when reading code

---

### 2. Type Hints (PEP 484) ✅

**Added throughout**:
- Function parameters with Python 3.13 union syntax (`list[float] | None`)
- Return type annotations
- Instance variable type hints
- Comprehensive docstrings following NumPy format

**Example**:
```python
def __init__(
    self,
    alt: float = 300.0,
    altlim: list[float] | None = None,
    option: Literal[1, 2, 3, 4] = 1,
    verbose: bool = True,
) -> None:
```

**Benefits**:
- IDE autocomplete and error detection
- `mypy` static type checking
- Self-documenting code
- Runtime type checking with tools like Pydantic

---

### 3. Test Modernization ✅

**Before**: Old unittest with single test file  
**After**: Comprehensive pytest suite

**New test files**:
- `tests/test_core.py` - Core HWM14 functionality (12+ test cases)
- `tests/test_plotting.py` - Plotting functionality (6+ test cases)
- `tests/conftest.py` - Pytest fixtures
- `tests/__init__.py` - Test package marker

**Features**:
- Parametrized tests for multiple scenarios
- Fixtures for reusable test data
- 100% compatible with modern pytest plugins
- Coverage reporting support

**Example**:
```python
@pytest.mark.parametrize("option,expected_attr", [
    (1, "altbins"),
    (2, "glatbins"),
    (3, "utbins"),
    (4, "glonbins"),
])
def test_hwm14_profile_types(self, option: int, expected_attr: str) -> None:
    h = HWM14(option=option, verbose=False)
    assert hasattr(h, expected_attr)
```

---

### 4. Updated pyproject.toml ✅

**Enhanced configuration**:
- Added `pytest` configuration with strict markers
- Added `mypy` configuration for type checking
- Added `ruff` and `black` linting/formatting rules
- Added `coverage` configuration
- Updated dependencies to modern versions:
  - `matplotlib>=3.8`
  - `seaborn>=0.12`
  - `pytest>=7.4`
  - `mypy>=1.7`
  - `ruff>=0.1`
  - `black>=23.12`

**New sections**:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"

[tool.mypy]
python_version = "3.13"
disallow_untyped_defs = true
strict_optional = true

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.coverage.run]
branch = true
source = ["pyhwm2014"]
```

---

### 5. Python 3.5 Compatibility Code Removed ✅

**Deleted**:
```python
# ❌ REMOVED - Python 3.5 has pathlib built-in
try:
    from pathlib import Path
    Path().expanduser()
except (ImportError,AttributeError):  # Python < 3.5
    from pathlib2 import Path
```

**Result**: Cleaner, simpler code targeting Python 3.13+

---

### 6. Code Quality Tools Added ✅

#### `.pre-commit-config.yaml`
Automated code quality checks:
- `ruff` - Fast Python linter and formatter
- `black` - Code formatter
- `mypy` - Type checker
- `docformatter` - Docstring formatter
- Pre-commit hooks for git integration

#### `CONTRIBUTING.md`
Developer guide including:
- Setup instructions
- Testing procedures
- Code style guidelines
- Build system documentation
- Release checklist

---

## Python & Dependency Updates

| Component | Before | After |
|-----------|--------|-------|
| Python   | 3.12+ workaround needed | 3.13+ required |
| NumPy    | 1.23 pinned | ≥1.26 (modern) |
| Build    | numpy.distutils deprecated | scikit-build-core + CMake |
| Type Checking | None | mypy (strict mode) |
| Testing | nose (deprecated) | pytest (modern) |
| Linting | None | ruff + black |

---

## PyPI Release Readiness

### ✅ Completed
- [x] Modern build system (scikit-build-core)
- [x] Python 3.13 compatible
- [x] Comprehensive type hints
- [x] Updated test suite
- [x] Code quality configuration
- [x] PEP 561 type marker (`py.typed`)
- [x] Development documentation
- [x] Pre-commit hooks

### Ready for Release Steps
```bash
# 1. Update version in pyproject.toml
# 2. Update CHANGELOG.md
# 3. Run final tests
make test313

# 4. Build distribution
python -m build

# 5. Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# 6. Test installation
pip install -i https://test.pypi.org/simple/ pyhwm2014

# 7. Upload to PyPI
python -m twine upload dist/*
```

---

## Backward Compatibility Notes

The public API remains **fully compatible** with existing code:

```python
# Old code still works
from pyhwm2014 import HWM14, HWM14Plot
hwm = HWM14(altlim=[90,200], option=1, verbose=False)
plot = HWM14Plot(profObj=hwm)
```

---

## Performance & Maintenance Benefits

1. **Faster Development**: Type hints catch errors early
2. **Better Documentation**: Self-documenting with type hints
3. **Easier Testing**: Modular structure enables targeted tests
4. **Code Review**: Clearer intent with PEP 484 compliance
5. **CI/CD Ready**: Can integrate with modern GitHub Actions
6. **Dependency Management**: Explicit in pyproject.toml

---

## Additional Resources

- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pyproject.toml Specification](https://packaging.python.org/specifications/pyproject-toml/)
