# pyHWM14 Solo Developer Quick Reference

This document provides a quick reference for common maintenance tasks for solo developers.

## Daily/Weekly Tasks

### Monitor Issues & PRs
```bash
# Check GitHub Issues & PRs
# https://github.com/rilma/pyHWM14/issues
# https://github.com/rilma/pyHWM14/pulls
```

### Run Local CI Before Pushing
```bash
# One-command local CI check
pytest tests/ --cov=pyhwm2014 && mypy pyhwm2014 && ruff check pyhwm2014 tests
```

### Code Review Checklist
- ✅ Lint passes: `ruff check pyhwm2014 tests`
- ✅ Format correct: `ruff format --check pyhwm2014 tests`
- ✅ Types pass: `mypy pyhwm2014`
- ✅ Tests pass: `pytest tests/ --cov=pyhwm2014` (>80% coverage)
- ✅ Docstrings added/updated
- ✅ CHANGELOG.md updated

## Release Workflow

### Pre-Release (1-2 hours)
```bash
# 1. Run full CI locally
pytest tests/ --cov=pyhwm2014 --cov-report=term-missing
mypy pyhwm2014
ruff check pyhwm2014 tests

# 2. Update CHANGELOG.md
# Move [Unreleased] items to new version with date

# 3. Commit and push
git add CHANGELOG.md
git commit -m "chore: prepare release v1.2.0"
git push origin main
```

### Release (5 minutes)
```bash
# 1. Create annotated/signed tag
git tag -a v1.2.0 -m "Release v1.2.0"
# or: git tag -s v1.2.0 -m "Release v1.2.0"

# 2. Push tag (triggers trusted publishing workflow)
git push origin v1.2.0

# 3. Verify PyPI (wait ~2 min for build)
pip install --upgrade pyhwm2014
python -c "import pyhwm2014; print(pyhwm2014.__version__)"
```

### Optional TestPyPI Dry Run
Use **Actions → Publish Python Package** with:
- `release_tag`: `vX.Y.Z` or prerelease tag (`vX.Y.Zrc1`)
- `target_repository`: `testpypi`

## Monthly Maintenance

### Review Dependabot PRs
- Check: https://github.com/rilma/pyHWM14/dependabot/updates
- Test each PR with: `pytest tests/ -v`
- Merge safe updates immediately

### Audit Security
```bash
pip-audit
```

### Check Coverage
```bash
pytest tests/ --cov=pyhwm2014 --cov-report=html
# Open htmlcov/index.html to review
```

## Quarterly Tasks

### Update Python Version Support (if applicable)
1. Update `requires-python` in `pyproject.toml`
2. Update matrix in `.github/workflows/ci.yaml`
3. Update classifiers in `pyproject.toml`
4. Test locally with new Python version
5. Document in CHANGELOG.md

### Dependency Review
```bash
# Check for updates
pip list --outdated

# Remove unused packages from pyproject.toml
# Update version constraints if needed
```

### Stale Issues Cleanup
Search for issues inactive > 90 days:
```
https://github.com/rilma/pyHWM14/issues?q=updated:%3C2025-11-15+is:open
```
Add comment requesting update, close after 1-2 weeks if no response.

## Key Files Reference

| File | Purpose |
|------|---------|
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | How to contribute (for external contributors) |
| [MAINTENANCE.md](MAINTENANCE.md) | Full maintenance & release guide (this role) |
| [ROADMAP.md](ROADMAP.md) | Project direction & priorities |
| [../CHANGELOG.md](../CHANGELOG.md) | User-facing release notes |
| `.github/workflows/ci.yaml` | Automated lint/type/test/security checks |
| `.github/workflows/release-pypi.yaml` | Trusted publishing release workflow |
| `.pre-commit-config.yaml` | Local code quality checks |
| `pyproject.toml` | Project metadata and dependencies |
| `.github/ISSUE_TEMPLATE/` | Issue templates for reporters |
| `.github/pull_request_template.md` | PR template for contributors |

## Emergency Response

### Critical Bug
1. Create and test fix immediately
2. Create hotfix branch: `git checkout -b hotfix/issue-XXX`
3. Merge to main and tag as patch: `git tag v1.1.1`
4. Push: `git push origin main --tags`

### Security Vulnerability
1. Create private GitHub Advisory
2. Develop and test fix
3. Release patch ASAP with security advisory

## Automation Checklist

✅ **Already Configured:**
- GitHub Actions CI + release workflows (lint, test, security, publish)
- Pre-commit hooks (local code quality)
- Dependabot (dependency updates)
- Type checking (mypy strict mode)
- Code coverage reporting (Codecov)
- PyPI auto-publishing from git tags

## Useful Links

- **GitHub Repo**: https://github.com/rilma/pyHWM14
- **PyPI Package**: https://pypi.org/project/pyhwm2014/
- **GitHub Actions**: https://github.com/rilma/pyHWM14/actions
- **GitHub Discussions**: https://github.com/rilma/pyHWM14/discussions
- **Dependabot**: https://github.com/rilma/pyHWM14/dependabot/updates

---

**Pro Tips:**
1. Always run local CI before pushing: use `&&` to chain commands
2. Use GitHub Discussions to redirect feature ideas away from Issues
3. Label issues immediately after creation for quick triaging
4. Keep CHANGELOG.md updated incrementally (easier than doing it all at release)
5. Tag PRs from contributors with `good-first-issue` or `help-wanted` for visibility
