"""Unit tests for HWM14 plotting functionality."""

import pytest
from unittest.mock import patch, MagicMock

from pyhwm2014 import HWM14, HWM14Plot, HWM142D, HWM142DPlot


class TestHWM14Plot:
    """Test HWM14Plot class for 1D profile plotting."""

    @patch("pyhwm2014.plotting.figure", None)
    def test_hwm14plot_no_matplotlib(self) -> None:
        """Test that HWM14Plot handles missing matplotlib gracefully."""
        h = HWM14(
            altlim=[90, 200],
            altstp=10,
            option=1,
            verbose=False,
        )
        # Should not crash even if matplotlib is unavailable
        plot = HWM14Plot(profObj=h)  # type: ignore

    def test_hwm14plot_with_object(self) -> None:
        """Test HWM14Plot initialization with valid HWM14 object."""
        h = HWM14(
            altlim=[90, 200],
            altstp=50,
            option=1,
            verbose=False,
        )
        # Verify HWM14Plot can be instantiated
        # (actual plotting requires matplotlib)
        plot = HWM14Plot(profObj=h)  # type: ignore

    def test_hwm14plot_without_object(self) -> None:
        """Test HWM14Plot handles None input."""
        # Should print "Wrong inputs!" and not crash
        plot = HWM14Plot(profObj=None)  # type: ignore

    @pytest.mark.parametrize("option", [1, 2, 3, 4])
    def test_hwm14plot_all_options(self, option: int) -> None:
        """Test HWM14Plot for all profile options."""
        h = HWM14(option=option, verbose=False)
        plot = HWM14Plot(profObj=h)  # type: ignore


class TestHWM142DPlot:
    """Test HWM142DPlot class for 2D array plotting."""

    @patch("pyhwm2014.plotting.figure", None)
    def test_hwm142dplot_no_matplotlib(self) -> None:
        """Test that HWM142DPlot handles missing matplotlib gracefully."""
        h = HWM142D(
            altlim=[90, 200],
            altstp=50,
            glat=-11.95,
            glon=-76.77,
            option=1,
            verbose=False,
        )
        # Should not crash
        plot = HWM142DPlot(profObj=h)  # type: ignore

    def test_hwm142dplot_initialization(self) -> None:
        """Test HWM142DPlot initialization with valid parameters."""
        h = HWM142D(
            altlim=[90, 200],
            altstp=50,
            glat=-11.95,
            glon=-76.77,
            option=1,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore

    def test_hwm142dplot_without_object(self) -> None:
        """Test HWM142DPlot handles None input."""
        plot = HWM142DPlot(profObj=None)  # type: ignore

    def test_hwm142dplot_wind_field_option(self) -> None:
        """Test HWM142DPlot with wind field visualization enabled."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glonlim=[-100, -50],
            glonstp=25,
            option=6,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h, WF=True)  # type: ignore
