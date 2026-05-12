"""
Data path management for HWM14 model data files.
"""

from os import environ
from pathlib import Path

# Set HWMPATH to the location of data files:
# - hwm123114.bin
# - dwm07b104i.dat
# - gd2qd.dat
HWMPATH: str = str(Path(__file__).parent / "data")
environ["HWMPATH"] = HWMPATH
