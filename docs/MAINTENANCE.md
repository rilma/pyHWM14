# Maintenance Guide for pyHWM14

This guide documents the maintenance and release process for pyHWM14, intended for the project maintainer.

## Release Process

### Pre-Release Checklist

1. **Ensure all tests pass locally:**
   ```bash
   make test313  # or: pytest tests/ -v --cov=pyhwm2014
   ```

2. **Verify type checking and linting:**
   ```bash
   make check
   ```

3. **Create/update CHANGELOG.md:**
   - Move items from "Unreleased" to current version
   - Follow [keepachangelog.com](https://keepachangelog.com) format
   - Include: Added, Fixed, Changed, Deprecated, Removed sections
   - Example:
     ```markdown
     ## [1.2.0] - 2026-02-15

     ### Added
     - Support for Python 3.14
     - New `interpolate()` method for smoother wind profiles

     ### Fixed
     - Bug #42: Incorrect wind calculation at equator

     ### Changed
     - Improved performance by 15% through vectorization
     ```

4. **Commit changes:**
   ```bash
   git add CHANGELOG.md
   git commit -m "chore: prepare release v1.2.0"
   git push origin main
   ```

5. **Create annotated/signed release tag from the target commit on `main`:**
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   # or signed:
   # git tag -s v1.2.0 -m "Release v1.2.0"
   ```

### Creating a Release

1. **Push the release tag:**
   ```bash
   git push origin v1.2.0
   ```

2. **GitHub Actions will automatically:**
   - Run dedicated release workflow (`.github/workflows/release-pypi.yaml`)
   - Build source and wheel distributions
   - Validate package metadata and wheel installability
   - Publish to PyPI via Trusted Publishing (OIDC)
   - Run post-publish install/import verification

3. **Verify PyPI deployment:**
   ```bash
   pip install --upgrade pyhwm2014
   python -c "import pyhwm2014; print(pyhwm2014.__version__)"
   ```

## Dependency Management

### Monthly: Review Dependabot PRs

Dependabot automatically checks for updates:
- Review each PR for breaking changes
- Run tests to verify compatibility
- Merge safe updates immediately
- For major updates, test thoroughly before merging

### Quarterly: Maintenance Audit

1. **Check for security vulnerabilities:**
   ```bash
   pip-audit
   ```

2. **Review dependency versions:**
   ```bash
   pip list --outdated
   ```

3. **Remove unused dependencies:**
   - Check imports in codebase
   - Update `pyproject.toml` if unused packages found

4. **Drop support for EOL Python versions:**
   - Update `requires-python` in `pyproject.toml`
   - Update CI matrix in `.github/workflows/ci.yaml`
   - Document in CHANGELOG

### Current Dependency Policy

- **NumPy**: >= 1.23 (supports Python 3.13)
- **Python**: >= 3.13 (latest stable, updated yearly)
- **Build**: scikit-build-core, cmake, ninja, meson (pinned in CI)
- **Dev**: pytest, mypy, ruff, black (flexible versions)

**Rationale**: Focus on latest Python versions to benefit from performance and features.

## Managing Issues

### Triage Workflow

1. **Label new issues:**
   - `bug` - Incorrect behavior or crash
   - `feature` - New functionality request
   - `enhancement` - Improvement to existing feature
   - `documentation` - Docs/examples issue
   - `help-wanted` - Seeking contributions
   - `good-first-issue` - Suitable for new contributors

2. **Stale Issues (>90 days no activity):**
   - Add comment asking for clarification or update
   - Close after 1-2 weeks if no response
   - Use template:
     ```markdown
     @user This issue has been inactive for 3 months.
     Please provide more details or we'll close it to keep the tracker clean.
     ```

3. **Duplicate Issues:**
   - Reference the original issue
   - Close with label `duplicate`

### Quick Response Guidelines

| Issue Type | Target Response |
|-----------|-----------------|
| Security bug | <24 hours |
| Critical bug | <1 week |
| Regular bug | <2 weeks |
| Feature request | <1 month (or send to Discussions) |

## Project Health Metrics

### Monthly Check

1. **Test Coverage:** Should remain >80%
   ```bash
   make test313
   ```

2. **Open Issues/PRs:**
   - Keep <10 open issues
   - Keep <3 open PRs
   - Prioritize high-impact items

3. **Dependency Status:**
   - All CI checks passing
   - No unresolved Dependabot PRs >1 week old

### Annual Review (Once per Year)

1. **Technical Debt Assessment:**
   - Review TODO and FIXME comments
   - Refactor heavily used code paths
   - Update architecture docs if needed

2. **Roadmap Update:**
   - Reflect on past year's achievements
   - Set priorities for next 12 months
   - Update `ROADMAP.md` and Discussions

3. **Community Engagement:**
   - Thank active contributors
   - Review feedback and feature requests
   - Plan community initiatives

## Deployment

### PyPI Publishing (Automatic)

When you push a tag `v*`, GitHub Actions release workflow:
1. Resolves release version from the git tag (`vX.Y.Z` → `X.Y.Z`) using dynamic versioning
2. Verifies the tag commit is reachable from `main`
3. Builds wheel + source distribution
4. Runs artifact checks (`twine check`) and wheel smoke test
5. Publishes to PyPI with Trusted Publishing (OIDC)
6. Verifies install/import from package index

**Manual PyPI upload** (if needed):
```bash
# Emergency fallback only (not the default path)
python -m pip install build twine
python -m build
python -m twine upload dist/*
```

### TestPyPI Dry Run (Recommended Before Major Releases)

Use manual workflow dispatch:
1. Open **Actions → Publish Python Package**
2. Run workflow with:
   - `release_tag`: e.g. `v1.2.0rc1`
   - `target_repository`: `testpypi`
3. Verify install:
   ```bash
   python -m pip install \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple/ \
     pyhwm2014==1.2.0rc1
   ```

### Testing the Release

```bash
# Test in clean environment
python -m venv test_env
source test_env/bin/activate
pip install pyhwm2014[plot,docs]
python -c "from pyhwm2014 import HWM14; print('✓ Import successful')"
```

## Documentation Maintenance

### Keeping Docs Current

1. **After each release:** Update examples if API changed
2. **Quarterly:** Review and update guides
3. **When deps update:** Check for compatibility issues
4. **User feedback:** Improve docs based on common questions

## Emergency Procedures

### Critical Bug in Released Version

1. **Assess severity:**
   - Does it cause crashes? → Critical
   - Does it produce wrong results? → Critical
   - Is workaround available? → Can wait for next release

2. **Hot-fix process:**
   ```bash
   git checkout v1.1.0  # Switch to tag
   git checkout -b hotfix/issue-XXX
   # Make minimal fix
   git commit -m "fix: [critical issue]"

   # Tag as patch version
   git tag v1.1.1
   git push origin v1.1.1
   ```

3. **Update main branch** with backported fix

### Security Vulnerability

1. **Create private security advisory** on GitHub
2. **Develop and test fix immediately**
3. **Release patch version ASAP**
4. **Publish security advisory publicly**

## Useful Commands Reference

```bash
# Setup development environment
make venv313 && source .venv313/bin/activate && pip install -e ".[dev,plot,docs]"

# Run full CI locally
make test313 && make check

# Format code
make fix

# Create release
git tag -a v1.2.0 -m "Release v1.2.0" && git push origin v1.2.0

# Check for stale Python versions
python --version  # Ensure you're running supported version
```

## Support & Questions

For questions about maintenance:
- Review GitHub Issues labeled `maintenance`
- Check existing maintenance PRs
- Consult [../CONTRIBUTING.md](../CONTRIBUTING.md) for contributor guidelines

---

**Last Updated:** February 2026
**Maintained By:** Ronald Ilma
