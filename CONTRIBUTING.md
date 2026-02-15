# Contributing to pyHWM14

Thank you for your interest in contributing to pyHWM14! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites
- Python 3.13+
- `uv` (fast Python package manager) - see README for installation
- `git`
- CMake 3.15+
- Fortran compiler (gfortran)

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/rilma/pyHWM14.git
cd pyHWM14

# Create development environment with Python 3.13
make venv313

# Activate virtual environment
source .venv313/bin/activate  # Linux/macOS
# or .venv313\Scripts\activate on Windows

# Install in development mode with all extras
pip install -e ".[dev,plot,docs]"
```

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or for bugfixes:
git checkout -b fix/your-bug-fix
```

Use descriptive branch names following conventional commits:
- `feature/add-wind-interpolation`
- `fix/altitude-calculation-error`
- `docs/improve-readme`

### 2. Make Your Changes

**Code Style Requirements:**
- Follow PEP 8 with line length of 100 characters
- Use type hints for all functions and variables
- Use meaningful variable names and include docstrings (NumPy format)
- Format and lint with: `make fix`
- Type check with: `make type-check`

**Example function with proper style:**
```python
def calculate_wind_profile(
    altitude: np.ndarray,
    latitude: float,
    year: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate wind profile at given altitude levels.
    
    Parameters
    ----------
    altitude : np.ndarray
        Altitude levels in kilometers.
    latitude : float
        Geographic latitude in degrees.
    year : int
        Year for the model calculation.
    
    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Zonal and meridional wind components.
    """
    # Implementation here
    return u_wind, v_wind
```

### 3. Write Tests

All new features must include tests. Run tests locally:
```bash
# Run all tests
make test313

# Run specific test file (advanced option)
uv run pytest tests/test_core.py -v
```

Target test coverage: **>80%**

### 4. Update Documentation

- Update docstrings for modified functions
- Update relevant sections in README.rst if user-facing changes
- Add CHANGELOG entry (see [CHANGELOG Format](#changelog-format) below)

### 5. Commit Your Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Good commits
git commit -m "feat: add interpolation method for wind profiles"
git commit -m "fix: correct altitude bias in HWM14 calculation"
git commit -m "docs: clarify year parameter requirements"
git commit -m "test: add coverage for edge cases"
git commit -m "refactor: simplify wind vector calculation"
```

Commit types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring without feature changes
- `perf:` - Performance improvements
- `ci:` - CI/CD changes

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub with:
- Clear title following conventional commits
- Description of what changed and why
- Link to any related issues (e.g., "Closes #123")
- Checklist items completed (see PR template)

## CHANGELOG Format

Add an entry to `CHANGELOG.md` for all user-facing changes:

```markdown
## [Unreleased]

### Added
- New interpolation method for smoother wind profiles

### Fixed
- Correct altitude bias when using option=2

### Changed
- Improved performance of wind vector calculation by 20%

### Deprecated
- Legacy `get_wind()` method (use `calculate()` instead)

### Removed
- Support for Python 3.12 (>= 3.13 required)
```

## Review Process

**All PRs require:**
1. ✅ Passing CI (lint, type check, tests)
2. ✅ Test coverage maintained (>80%)
3. ✅ Docstrings and type hints added
4. ✅ CHANGELOG entry added

## Code Quality Checklist

Before submitting a PR, run:

```bash
# Run all tests
make test313

# Format and lint (auto-fixes)
make fix

# Type checking
make type-check

# All checks (local CI)
make check && make test313
```

## Reporting Issues

### Bug Reports
Include:
- Python version and OS
- Minimal reproducible example
- Expected vs actual behavior
- Stack trace (if applicable)

### Feature Requests
Include:
- Use case and motivation
- Proposed API if applicable
- Any alternatives considered

## Questions & Discussions

Use GitHub Discussions for:
- General usage questions
- Best practices for HWM14
- Ideas for future improvements

## Additional Resources

- [pyHWM14 README](./README.rst) - Installation and usage
- [Maintenance Guide](./docs/MAINTENANCE.md) - Release process and project maintenance
- [Development Roadmap](./docs/ROADMAP.md) - Future direction and priorities
- [HWM14 Model](https://www.nrl.navy.mil/research/nrl-review/2015/atmospheric-science/drob) - Model reference

---

Thank you for contributing! 🚀
