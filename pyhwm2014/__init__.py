"""Python interface for HWM14 (Horizontal Wind Model 2014).

This package provides a Python interface to the HWM14 model for calculating
atmospheric wind speeds at various geophysical locations and conditions.
"""

from .core import HWM14, HWM142D
from .plotting import HWM14Plot, HWM142DPlot
from .data import HWMPATH

__all__ = ["HWM14", "HWM142D", "HWM14Plot", "HWM142DPlot", "HWMPATH"]
__version__ = "1.1.0"