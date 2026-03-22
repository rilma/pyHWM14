# Fork: pyHWM14 with batch API

This fork adds a **vectorized/batch API** and matches upstream **Python 3.13+** (`requires-python`). It is intended to be proposed upstream via pull request; if not accepted, the fork can be maintained under a name such as `pyhwm14-numpy2` or `pyhwm2014-batch`.

## Build requirements

- **Fortran compiler** (e.g. `gfortran`). CMake must find it.
  - macOS: `brew install gcc` (provides `gfortran`), or set `FC=gfortran` if already installed.
  - Linux: install `gfortran` from your distro.
- CMake 3.15+, Python 3.13+, NumPy ≥1.23.

## Install from this tree

```bash
# Ensure Fortran is available (e.g. brew install gcc on macOS)
pip install -e /path/to/external/pyHWM14
```

## New: batch/vectorized API

Function `hwm14_vectorized` evaluates HWM14 at many (alt, lat, lon, utc) points in one call. If the Fortran extension was built with the batch routine, a single Fortran call is used; otherwise a Python loop over the existing single-point `hwm14` is used.

```python
from pyhwm2014 import hwm14_vectorized
import numpy as np

# Example: 100 points
alt_km = np.linspace(200, 400, 100)
glat_deg = np.full(100, -11.95)
glon_deg = np.full(100, -76.77)
utc_hours = np.full(100, 12.0)
iyd = 93323  # 1993 day 323

zonal, meridional = hwm14_vectorized(alt_km, glat_deg, glon_deg, utc_hours, iyd)
# zonal, meridional: (100,) m/s
```

Scalars are broadcast: e.g. single altitude with many lats/lons works.

## Changes in this fork

- **Batch API:** `hwm14_vectorized(alt_km, glat_deg, glon_deg, utc_hours, iyd, ap=None, ...)` in `pyhwm2014.core` and exported from `pyhwm2014`.
- **Fortran:** New subroutine `hwm14_batch(n, iyd, sec, alt, glat, glon, stl, f107a, f107, ap, w_merid, w_zonal)` in `source/hwm14.f90`, declared in `source/reference/hwm14.pyf`. The Python batch wrapper uses it when available.

## Pull request / upstream

1. Fork `rilma/pyHWM14` on GitHub.
2. Push this tree to a branch (e.g. `pr-to-upstream` or `batch-api`).
3. Open a PR describing: batch API, optional Fortran vectorization, matplotlib compatibility fixes as applicable.
4. If the PR is not merged, keep this fork (e.g. publish to PyPI under a different name like `pyhwm2014-batch`).

## Original project

- Repository: https://github.com/rilma/pyHWM14
- HWM14: Horizontal Wind Model 2014 (NRL).
