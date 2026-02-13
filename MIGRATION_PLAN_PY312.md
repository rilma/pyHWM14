# Python 3.12 Migration Plan for pyHWM14

## ✅ MIGRATION COMPLETE

**Status**: Successfully migrated from `numpy.distutils` to `scikit-build-core` + CMake + f2py (Meson backend)

**Date Completed**: February 13, 2026

**Key Achievements**:
- ✅ Python 3.12 builds successfully with scikit-build-core
- ✅ Fortran extension (hwm14) compiles with modern NumPy 2.x + Meson backend
- ✅ All tests pass with Python 3.12
- ✅ CI/CD migrated to use Python 3.12 + modern build system
- ✅ Documentation updated to reflect Python 3.12 requirement
- ✅ Makefile targets updated with 3.12 as primary version
- ✅ Removed dependency on deprecated `setuptools<60` and `numpy==1.23.5` pins

**Breaking Changes**:
- Python 3.12+ now required (was: 3.11 workaround)
- Build system is now CMake + f2py (Meson), not numpy.distutils
- No more setuptools version pinning required

## Overview
This document outlines the completed migration from deprecated `numpy.distutils` to a modern build system that supports Python 3.12+ and future Python versions.

## Current State
- **Python support**: 3.11 (temporary workaround)
- **Build system**: `numpy.distutils` (deprecated, removed in Python 3.12)
- **Fortran extension**: Single f2py module (`hwm14`)
- **Data files**: `.dat` and `.bin` files packaged with module
- **Dependencies**: numpy 1.23.5, setuptools<60 (pinned for compatibility)

## Recommended Solution: scikit-build-core

**Why scikit-build-core?**
- Purpose-built for Fortran + f2py projects
- Modern, actively maintained (unlike numpy.distutils)
- Works seamlessly with meson build system
- Explicit configuration (meson.build)
- Supports Python 3.12+ without workarounds
- Minimal code changes required in setup.py

## Migration Steps

### Phase 1: Setup New Build Configuration

1. **Create `pyproject.toml`** (replaces setuptools config)
   ```toml
   [build-system]
   requires = ["scikit-build-core", "numpy"]
   build-backend = "scikit_build_core.build"

   [project]
   name = "pyhwm2014"
   version = "1.1.0"
   description = "HWM14 neutral winds model"
   requires-python = ">=3.12"
   dependencies = ["numpy", "timeutil"]
   ```

2. **Create `meson.build`** (explicit Fortran build rules)
   ```meson
   project('pyhwm2014', 'fortran')
   
   f2py_exe = find_program('f2py')
   
   hwm14_ext = f2py_exe.process(
     'source/hwm14.f90',
     output_name: 'hwm14'
   )
   ```

3. **Simplify `setup.py`** → minimal wrapper or remove entirely

### Phase 2: Update Dependencies

- Replace `numpy==1.23.5` pin with `numpy>=1.23` (modern numpy supports f2py)
- Remove `setuptools<60` constraint
- Add `scikit-build-core` to `pyproject.toml`
- Update CI workflow: no custom setuptools pinning needed

### Phase 3: Update Makefiles & Documentation

1. Update [Makefile](Makefile):
   - Remove `setuptools<60` pin from targets
   - Update `install311` → `install312` (and variants)
   - Keep build cleanup consistent

2. Update CI ([.github/workflows/ci.yaml](.github/workflows/ci.yaml)):
   - Change matrix from `3.11` to `3.12`
   - Remove custom pip constraints

3. Update docs ([README.rst](README.rst)):
   - State "Supports Python 3.12+"
   - Document new build system

### Phase 4: Testing & Validation

1. **Local testing**:
   ```bash
   make install312
   make test312
   ```

2. **CI validation**: Verify GitHub Actions passes with new build system

3. **Backwards compatibility check**: Ensure existing install paths still work

## Implementation Order

1. Create `pyproject.toml` and `meson.build` (alongside existing setup.py)
2. Test local builds with scikit-build-core
3. Update CI workflow to use Python 3.12
4. Remove/deprecate old setup.py
5. Update documentation
6. Tag release as 3.12-compatible

## Risk Mitigation

- **Reversible**: Keep setup.py during transition; meson.build coexists
- **Test-first**: Validate builds locally before CI merge
- **Gradual rollout**: Test on branch, merge only after validation

## Timeline Estimate

- **Phase 1** (Config): ~1-2 hours
- **Phase 2** (Dependencies): ~30 minutes
- **Phase 3** (Makefile/Docs): ~30 minutes
- **Phase 4** (Testing): ~1 hour
- **Total**: 3-5 hours of focused work

## Long-term Benefits

✅ Python 3.12+ support  
✅ Python 3.13+ forward compatible  
✅ Modern, maintainable build system  
✅ Community-standard approach  
✅ No version/architecture pinning workarounds  

## Related Issues

- Resolves GitHub issue #11 (Build tools deprecated)
- Enables modern CI/CD on Python 3.12+ systems

---

**Next step**: Start Phase 1 implementation (create pyproject.toml + meson.build)
