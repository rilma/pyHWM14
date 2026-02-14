"""Unit tests for HWM14 core functionality."""

import pytest
from pyhwm2014 import HWM14, HWM142D


class TestHWM14Initialization:
    """Test HWM14 class initialization and basic calculations."""

    def test_hwm14_height_profile(self) -> None:
        """Test height profile calculation with standard parameters."""
        h = HWM14(
            altlim=[90, 200],
            altstp=1,
            ap=[-1, 35],
            day=323,
            option=1,
            ut=11.66667,
            verbose=False,
            year=1993,
        )
        assert len(h.Uwind) == 111
        assert len(h.Vwind) == 111
        # Verify specific values match expected model output
        assert pytest.approx(h.Uwind[92], rel=1e-3) == -16.502953
        assert pytest.approx(h.Vwind[92], rel=1e-3) == -39.811909

    def test_hwm14_latitude_profile(self) -> None:
        """Test latitude profile calculation."""
        h = HWM14(
            alt=300,
            ap=[-1, 35],
            glatlim=[-30, 30],
            glatstp=10,
            glon=-76.77,
            option=2,
            ut=12.0,
            verbose=False,
            year=1993,
        )
        assert hasattr(h, "glatbins")
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0

    def test_hwm14_gmt_profile(self) -> None:
        """Test GMT profile calculation."""
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
            year=1993,
        )
        assert hasattr(h, "utbins")
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0

    def test_hwm14_longitude_profile(self) -> None:
        """Test longitude profile calculation."""
        h = HWM14(
            alt=300,
            ap=[-1, 35],
            glat=-11.95,
            glonlim=[-180, 180],
            glonstp=30,
            option=4,
            ut=12.0,
            verbose=False,
            year=1993,
        )
        assert hasattr(h, "glonbins")
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0

    @pytest.mark.parametrize("option,expected_attr", [
        (1, "altbins"),
        (2, "glatbins"),
        (3, "utbins"),
        (4, "glonbins"),
    ])
    def test_hwm14_profile_types(self, option: int, expected_attr: str) -> None:
        """Test that HWM14 creates correct attributes for each option."""
        h = HWM14(option=option, verbose=False)
        assert hasattr(h, expected_attr)

    def test_hwm14_invalid_option(self) -> None:
        """Test that invalid option doesn't crash."""
        h = HWM14(option=5, verbose=False)  # type: ignore
        # Should handle gracefully
        assert h.Uwind == []

    def test_hwm14_mutable_defaults(self) -> None:
        """Test that mutable defaults are properly isolated."""
        h1 = HWM14(verbose=False)
        h2 = HWM14(verbose=False)
        # Modifying h1.ap should not affect h2
        h1.ap[1] = 100
        assert h2.ap[1] == 35


class TestHWM142D:
    """Test HWM142D class for 2D array calculations."""

    def test_hwm142d_initialization(self) -> None:
        """Test HWM142D initialization."""
        h = HWM142D(
            altlim=[90, 200],
            altstp=10,
            glat=-11.95,
            glon=-76.77,
            option=1,
            utlim=[0, 12],
            utstp=3,
            verbose=False,
            year=1993,
        )
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0

    @pytest.mark.parametrize("option", [1, 2, 4, 6])
    def test_hwm142d_options(self, option: int) -> None:
        """Test various HWM142D profile options."""
        h = HWM142D(option=option, verbose=False)
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0


class TestDataPathConfiguration:
    """Test data path is properly configured."""

    def test_hwmpath_is_set(self) -> None:
        """Test that HWMPATH is correctly configured."""
        from pyhwm2014 import HWMPATH
        import os

        assert HWMPATH is not None
        assert os.path.exists(HWMPATH) or "HWMPATH" in os.environ
