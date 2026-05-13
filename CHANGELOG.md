# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced CI/CD pipeline with linting, type checking, and security audits
- Comprehensive CONTRIBUTING.md guide for collaboration
- MAINTENANCE.md documenting release and maintenance processes
- ROADMAP.md outlining future development directions
- Pre-commit hook configuration for automated code quality checks
- Coverage reporting in CI pipeline via Codecov
- Security vulnerability scanning with pip-audit
- Dedicated release workflow for trusted publishing to PyPI/TestPyPI from version tags

### Fixed
- (Pending)

### Changed
- Updated GitHub Actions versions (v3 → v4, v4 → v5)
- Improved CI workflow organization (separate lint, test, security jobs)
- Release documentation now follows dynamic `setuptools_scm` versioning (tag-driven, no manual pyproject version edits)

### Deprecated
- (None at this time)

### Removed
- (None at this time)

### Security
- Added automated security audit during CI pipeline

## [1.1.0] - 2026-02-15

### Added
- Full type hint coverage with mypy strict mode
- Comprehensive test suite covering all major functionality
- PyPI publishing with automated CI/CD pipeline
- Support for Python 3.13
- Modern build system (scikit-build-core)
- API documentation with docstrings

### Fixed
- Initial release of pyHWM14 package

## [Previous]

See GitHub releases for historical versions: https://github.com/rilma/pyHWM14/releases
