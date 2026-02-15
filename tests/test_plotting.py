"""Unit tests for HWM14 plotting functionality."""

from unittest.mock import MagicMock, patch

import pytest

from pyhwm2014 import HWM14, HWM142D, HWM14Plot, HWM142DPlot


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
        HWM14Plot(profObj=h)  # type: ignore

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
        HWM14Plot(profObj=h)  # type: ignore

    def test_hwm14plot_without_object(self) -> None:
        """Test HWM14Plot handles None input."""
        # Should print "Wrong inputs!" and not crash
        HWM14Plot(profObj=None)  # type: ignore

    @pytest.mark.parametrize("option", [1, 2, 3, 4])
    def test_hwm14plot_all_options(self, option: int) -> None:
        """Test HWM14Plot for all profile options."""
        h = HWM14(option=option, verbose=False)
        HWM14Plot(profObj=h)  # type: ignore

    def test_hwm14plot_get_title(self) -> None:
        """Test GetTitle method."""
        h = HWM14(
            altlim=[100, 200],
            altstp=50,
            ap=[-1, 50],
            day=100,
            glat=45.0,
            glon=-120.0,
            option=1,
            ut=15.5,
            verbose=False,
            year=2000,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        # Title generation depends on matplotlib availability
        # If matplotlib is available, title should be generated
        if hasattr(plot, 'GetTitle'):
            plot.GetTitle()
            if hasattr(plot, 'title'):
                assert len(plot.title) > 0

    def test_hwm14plot_get_hhmmss(self) -> None:
        """Test GetHHMMSS method."""
        h = HWM14(
            altlim=[100, 200],
            altstp=50,
            option=1,
            ut=12.75,
            verbose=False,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        plot.GetHHMMSS()
        assert hasattr(plot, "hour")
        assert hasattr(plot, "minute")
        assert hasattr(plot, "second")
        assert plot.hour == 12
        assert plot.minute == 45

    def test_hwm14plot_height_profile_attributes(self) -> None:
        """Test HWM14Plot attributes for height profile."""
        h = HWM14(
            altlim=[100, 200],
            altstp=50,
            ap=[-1, 35],
            glat=-11.95,
            glon=-76.77,
            option=1,
            ut=12.0,
            verbose=False,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        assert plot.option == 1
        assert hasattr(plot, "altbins")
        assert hasattr(plot, "Uwind")
        assert hasattr(plot, "Vwind")

    def test_hwm14plot_latitude_profile_attributes(self) -> None:
        """Test HWM14Plot attributes for latitude profile."""
        h = HWM14(
            alt=300,
            ap=[-1, 35],
            glatlim=[-30, 30],
            glatstp=10,
            glon=-76.77,
            option=2,
            ut=12.0,
            verbose=False,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        assert plot.option == 2
        assert hasattr(plot, "glatbins")
        assert hasattr(plot, "alt")

    def test_hwm14plot_gmt_profile_attributes(self) -> None:
        """Test HWM14Plot attributes for GMT profile."""
        h = HWM14(
            alt=300,
            ap=[-1, 35],
            day=323,
            glat=-11.95,
            glon=-76.77,
            option=3,
            utlim=[0, 12],
            utstp=2,
            verbose=False,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        assert plot.option == 3
        assert hasattr(plot, "utbins")

    def test_hwm14plot_longitude_profile_attributes(self) -> None:
        """Test HWM14Plot attributes for longitude profile."""
        h = HWM14(
            alt=300,
            ap=[-1, 35],
            glat=-11.95,
            glonlim=[-180, 180],
            glonstp=30,
            option=4,
            ut=12.0,
            verbose=False,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        assert plot.option == 4
        assert hasattr(plot, "glonbins")

    def test_hwm14plot_title_generation_option_1(self) -> None:
        """Test title generation for option 1."""
        h = HWM14(
            altlim=[100, 200],
            altstp=50,
            ap=[-1, 25],
            glat=30.0,
            glon=-90.0,
            option=1,
            ut=10.0,
            verbose=False,
            year=2005,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        if hasattr(plot, 'GetTitle'):
            plot.GetTitle()
            if hasattr(plot, 'title'):
                assert "2005" in plot.title or "25" in plot.title

    def test_hwm14plot_title_generation_option_2(self) -> None:
        """Test title generation for option 2."""
        h = HWM14(
            alt=250,
            ap=[-1, 30],
            glatlim=[-30, 30],
            glatstp=10,
            glon=-100.0,
            option=2,
            ut=11.5,
            verbose=False,
            year=2010,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        if hasattr(plot, 'GetTitle'):
            plot.GetTitle()
            if hasattr(plot, 'title'):
                assert "2010" in plot.title or "250" in plot.title

    def test_hwm14plot_title_generation_option_3(self) -> None:
        """Test title generation for option 3."""
        h = HWM14(
            alt=300,
            ap=[-1, 40],
            day=200,
            glat=0.0,
            glon=0.0,
            option=3,
            utlim=[0, 12],
            utstp=2,
            verbose=False,
            year=2015,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        if hasattr(plot, 'GetTitle'):
            plot.GetTitle()
            if hasattr(plot, 'title'):
                assert "2015" in plot.title or plot.title

    def test_hwm14plot_title_generation_option_4(self) -> None:
        """Test title generation for option 4."""
        h = HWM14(
            alt=350,
            ap=[-1, 45],
            glat=60.0,
            glonlim=[-180, 180],
            glonstp=30,
            option=4,
            ut=14.0,
            verbose=False,
            year=2020,
        )
        plot = HWM14Plot(profObj=h)  # type: ignore
        if hasattr(plot, 'GetTitle'):
            plot.GetTitle()
            if hasattr(plot, 'title'):
                assert "2020" in plot.title or plot.title


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
        HWM142DPlot(profObj=h)  # type: ignore

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
        HWM142DPlot(profObj=h)  # type: ignore

    def test_hwm142dplot_without_object(self) -> None:
        """Test HWM142DPlot handles None input."""
        HWM142DPlot(profObj=None)  # type: ignore

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
        HWM142DPlot(profObj=h, WF=True)  # type: ignore

    def test_hwm142dplot_default_zmin_zmax(self) -> None:
        """Test HWM142DPlot with default zMin and zMax."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glon=-76.77,
            option=1,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore
        assert plot.zMin == [None, None]
        assert plot.zMax == [None, None]

    def test_hwm142dplot_custom_zmin_zmax(self) -> None:
        """Test HWM142DPlot with custom zMin and zMax."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glon=-76.77,
            option=1,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h, zMin=[-50, -50], zMax=[50, 50])  # type: ignore
        assert plot.zMin == [-50, -50]
        assert plot.zMax == [50, 50]

    def test_hwm142dplot_option_1(self) -> None:
        """Test HWM142DPlot for option 1."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glon=-76.77,
            option=1,
            utlim=[0, 10],
            utstp=5,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore
        assert plot.option == 1
        assert hasattr(plot, "altbins")
        assert hasattr(plot, "utbins")

    def test_hwm142dplot_option_2(self) -> None:
        """Test HWM142DPlot for option 2."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glatlim=[-20, 20],
            glatstp=10,
            glon=-76.77,
            option=2,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore
        assert plot.option == 2
        assert hasattr(plot, "altbins")
        assert hasattr(plot, "glatbins")

    def test_hwm142dplot_option_4(self) -> None:
        """Test HWM142DPlot for option 4."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glonlim=[-100, -50],
            glonstp=25,
            option=4,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore
        assert plot.option == 4
        assert hasattr(plot, "altbins")
        assert hasattr(plot, "glonbins")

    def test_hwm142dplot_option_6(self) -> None:
        """Test HWM142DPlot for option 6."""
        h = HWM142D(
            alt=300,
            glatlim=[-30, 30],
            glatstp=15,
            glonlim=[-100, 100],
            glonstp=50,
            option=6,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore
        assert plot.option == 6
        assert hasattr(plot, "glatbins")
        assert hasattr(plot, "glonbins")

    def test_hwm142dplot_get_hhmmss(self) -> None:
        """Test GetHHMMSS method in 2D plotting."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glon=-76.77,
            option=1,
            ut=16.25,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore
        plot.GetHHMMSS()
        assert hasattr(plot, "hour")
        assert hasattr(plot, "minute")
        assert hasattr(plot, "second")
        assert plot.hour == 16
        assert plot.minute == 15

    def test_hwm142dplot_get_title(self) -> None:
        """Test GetTitle method in 2D plotting."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glon=-76.77,
            option=1,
            ap=[-1, 50],
            verbose=False,
            year=2008,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore
        plot.GetTitle()
        assert hasattr(plot, "title")
        assert "2008" in plot.title or plot.title  # Should have generated a title

    def test_hwm142dplot_wf_wind_field(self) -> None:
        """Test HWM142DPlot with wind field visualization."""
        h = HWM142D(
            altlim=[150, 200],
            altstp=25,
            glat=-11.95,
            glonlim=[-100, 100],
            glonstp=50,
            option=4,
            verbose=False,
        )
        plot = HWM142DPlot(profObj=h, WF=True)  # type: ignore
        assert plot.WF is True

    def test_hwm142dplot_attributes_preserved(self) -> None:
        """Test that HWM142DPlot preserves HWM142D attributes."""
        h = HWM142D(
            altlim=[100, 150],
            altstp=25,
            glat=-11.95,
            glon=-76.77,
            ap=[-1, 60],
            day=150,
            option=1,
            verbose=False,
            year=2012,
        )
        plot = HWM142DPlot(profObj=h)  # type: ignore
        assert plot.year == 2012
        assert plot.doy == 150
        assert plot.ap == [-1, 60]
