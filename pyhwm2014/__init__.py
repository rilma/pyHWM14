"""Python interface for HWM14 (Horizontal Wind Model 2014).

This package provides a Python interface to the HWM14 model for
calculating atmospheric wind speeds at various geophysical locations and
conditions.
"""

from .core import HWM14, HWM142D, hwm14_vectorized
from .data import HWMPATH
from .plotting import HWM14Plot, HWM142DPlot

__all__ = ["HWM14", "HWM142D", "HWM14Plot", "HWM142DPlot", "HWMPATH", "hwm14_vectorized"]

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pyhwm2014")
except PackageNotFoundError:
    __version__ = "0.0.0"
