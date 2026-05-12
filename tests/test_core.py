"""
Unit tests for HWM14 core functionality.
"""

import numpy as np
import pytest

from pyhwm2014 import HWM14, HWM142D, hwm14_vectorized


class TestHWM14Initialization:
    """
    Test HWM14 class initialization and basic calculations.
    """

    def test_hwm14_height_profile(self) -> None:
        """
        Test height profile calculation with standard parameters.
        """
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
        """
        Test latitude profile calculation.
        """
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
        """
        Test GMT profile calculation.
        """
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
        """
        Test longitude profile calculation.
        """
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

    @pytest.mark.parametrize(
        "option,expected_attr",
        [
            (1, "altbins"),
            (2, "glatbins"),
            (3, "utbins"),
            (4, "glonbins"),
        ],
    )
    def test_hwm14_profile_types(self, option: int, expected_attr: str) -> None:
        """
        Test that HWM14 creates correct attributes for each option.
        """
        h = HWM14(option=option, verbose=False)
        assert hasattr(h, expected_attr)

    def test_hwm14_invalid_option(self) -> None:
        """
        Test that invalid option doesn't crash.
        """
        h = HWM14(option=5, verbose=False)  # type: ignore
        # Should handle gracefully
        assert h.Uwind == []

    def test_hwm14_mutable_defaults(self) -> None:
        """
        Test that mutable defaults are properly isolated.
        """
        h1 = HWM14(verbose=False)
        h2 = HWM14(verbose=False)
        # Modifying h1.ap should not affect h2
        h1.ap[1] = 100
        assert h2.ap[1] == 35


class TestHWM142D:
    """
    Test HWM142D class for 2D array calculations.
    """

    def test_hwm142d_initialization(self) -> None:
        """
        Test HWM142D initialization.
        """
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
        """
        Test various HWM142D profile options.
        """
        h = HWM142D(option=option, verbose=False)
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0

    def test_hwm142d_option_3(self) -> None:
        """
        Test HWM142D option 3 (GMT vs Latitude).
        """
        h = HWM142D(
            alt=300,
            ap=[-1, 35],
            glatlim=[-20, 20],
            glatstp=10,
            glon=-76.77,
            option=3,
            utlim=[0, 12],
            utstp=4,
            verbose=False,
            year=1993,
        )
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0
        assert hasattr(h, "utbins")
        assert hasattr(h, "glatbins")

    def test_hwm142d_invalid_option(self) -> None:
        """
        Test that HWM142D handles invalid option gracefully.
        """
        h = HWM142D(option=9, verbose=False)  # type: ignore
        # Invalid option should result in empty wind arrays
        assert hasattr(h, "Uwind")
        assert hasattr(h, "Vwind")
        assert h.Uwind.size == 0
        assert h.Vwind.size == 0

    def test_hwm142d_mutable_defaults(self) -> None:
        """
        Test that HWM142D mutable defaults are properly isolated.
        """
        h1 = HWM142D(verbose=False)
        h2 = HWM142D(verbose=False)
        # Modifying h1.ap should not affect h2
        h1.ap[1] = 100
        assert h2.ap[1] == 35


class TestHWM14Methods:
    """
    Test HWM14 utility methods.
    """

    def test_toMLT_conversion(self) -> None:
        """
        Test magnetic local time conversion.
        """
        h = HWM14(
            altlim=[90, 200],
            altstp=50,
            glat=-11.95,
            glon=-76.77,
            option=1,
            ut=12.0,
            verbose=False,
            year=1993,
        )
        # toMLT should set self.mlt attribute
        h.toMLT(12.0)
        assert hasattr(h, "mlt")
        assert isinstance(h.mlt, float)

    def test_toMLT_multiple_times(self) -> None:
        """
        Test magnetic local time conversion for different UT values.
        """
        h = HWM14(verbose=False)
        for ut in [0.0, 6.0, 12.0, 18.0]:
            h.toMLT(ut)
            assert hasattr(h, "mlt")
            assert -12.0 <= h.mlt <= 12.0  # MLT is within [-12, 12] range

    def test_profile_data_consistency(self) -> None:
        """
        Test that profile data arrays have consistent length.
        """
        h = HWM14(
            altlim=[100, 200],
            altstp=10,
            option=1,
            verbose=False,
        )
        assert len(h.Uwind) == len(h.Vwind)
        assert len(h.Uwind) == len(h.altbins)

    def test_wind_components_are_numeric(self) -> None:
        """
        Test that wind components are numeric values.
        """
        import numpy as np

        h = HWM14(
            altlim=[200, 300],
            altstp=25,
            option=1,
            verbose=False,
        )
        assert all(isinstance(u, (int, float, np.floating)) for u in h.Uwind)
        assert all(isinstance(v, (int, float, np.floating)) for v in h.Vwind)

    def test_different_solar_conditions(self) -> None:
        """
        Test calculations with different solar indices.
        """
        h1 = HWM14(
            altlim=[200, 250],
            altstp=10,
            f107=70.0,
            f107a=70.0,
            option=1,
            verbose=False,
        )
        h2 = HWM14(
            altlim=[200, 250],
            altstp=10,
            f107=200.0,
            f107a=200.0,
            option=1,
            verbose=False,
        )
        # Both should calculate successfully
        assert len(h1.Uwind) > 0
        assert len(h2.Uwind) > 0

    def test_different_ap_indices(self) -> None:
        """
        Test calculations with different AP indices.
        """
        h1 = HWM14(
            altlim=[200, 250],
            altstp=10,
            ap=[-1, 10],
            option=1,
            verbose=False,
        )
        h2 = HWM14(
            altlim=[200, 250],
            altstp=10,
            ap=[-1, 100],
            option=1,
            verbose=False,
        )
        # Both should calculate successfully
        assert len(h1.Uwind) > 0
        assert len(h2.Uwind) > 0

    def test_year_parameter(self) -> None:
        """
        Test that year parameter is properly handled.
        """
        h1 = HWM14(
            altlim=[200, 250],
            altstp=25,
            option=1,
            verbose=False,
            year=1993,
        )
        h2 = HWM14(
            altlim=[200, 250],
            altstp=25,
            option=1,
            verbose=False,
            year=2010,
        )
        # Both should calculate successfully
        assert len(h1.Uwind) > 0
        assert len(h2.Uwind) > 0

    def test_day_of_year_variations(self) -> None:
        """
        Test calculations for different days of year.
        """
        h1 = HWM14(
            altlim=[200, 250],
            altstp=25,
            day=1,
            option=1,
            verbose=False,
        )
        h2 = HWM14(
            altlim=[200, 250],
            altstp=25,
            day=180,
            option=1,
            verbose=False,
        )
        # Different days should produce different results
        assert h1.Uwind != h2.Uwind

    def test_high_altitude_profile(self) -> None:
        """
        Test calculations at high altitudes.
        """
        h = HWM14(
            altlim=[300, 400],
            altstp=25,
            option=1,
            verbose=False,
        )
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0

    def test_low_altitude_profile(self) -> None:
        """
        Test calculations at low altitudes.
        """
        h = HWM14(
            altlim=[0, 100],
            altstp=10,
            option=1,
            verbose=False,
        )
        assert len(h.Uwind) > 0
        assert len(h.Vwind) > 0

    def test_equatorial_latitude(self) -> None:
        """
        Test calculations at equatorial latitudes.
        """
        h = HWM14(
            alt=300,
            glat=0.0,
            glon=0.0,
            option=2,
            glatlim=[-5, 5],
            glatstp=1,
            verbose=False,
        )
        assert len(h.Uwind) > 0

    def test_high_northern_latitude(self) -> None:
        """
        Test calculations at high northern latitudes.
        """
        h = HWM14(
            alt=300,
            glat=75.0,
            glon=0.0,
            option=2,
            glatlim=[70, 80],
            glatstp=2,
            verbose=False,
        )
        assert len(h.Uwind) > 0

    def test_high_southern_latitude(self) -> None:
        """
        Test calculations at high southern latitudes.
        """
        h = HWM14(
            alt=300,
            glat=-75.0,
            glon=0.0,
            option=2,
            glatlim=[-80, -70],
            glatstp=2,
            verbose=False,
        )
        assert len(h.Uwind) > 0


class TestHWM14Vectorized:
    """
    Test batch/vectorized hwm14_vectorized API.
    """

    def test_vectorized_single_point(self) -> None:
        """
        Single point returns 0-d arrays with same value as HWM14.
        """
        z, m = hwm14_vectorized(300.0, -11.95, -76.77, 12.0, 93323)
        assert np.ndim(z) == 0 and np.ndim(m) == 0
        h = HWM14(
            alt=300,
            glat=-11.95,
            glon=-76.77,
            ut=12.0,
            day=323,
            year=1993,
            option=1,
            altlim=[300, 300],
            altstp=1,
            verbose=False,
        )
        assert pytest.approx(float(z), rel=1e-5) == h.Uwind[0]
        assert pytest.approx(float(m), rel=1e-5) == h.Vwind[0]

    def test_vectorized_batch_matches_hwm14(self) -> None:
        """
        Batch result matches HWM14 height profile.
        """
        alt = np.linspace(200, 400, 5)
        z, m = hwm14_vectorized(alt, -11.95, -76.77, 12.0, 93323)
        assert z.shape == (5,) and m.shape == (5,)
        h = HWM14(
            altlim=[200, 400],
            altstp=50,
            glat=-11.95,
            glon=-76.77,
            ut=12.0,
            day=323,
            year=1993,
            option=1,
            verbose=False,
        )
        for i in range(5):
            assert pytest.approx(z[i], rel=1e-5) == h.Uwind[i]
            assert pytest.approx(m[i], rel=1e-5) == h.Vwind[i]

    def test_vectorized_ap_default(self) -> None:
        """
        Default ap matches explicitly passing the default value.
        """
        z1, _ = hwm14_vectorized(300.0, -11.95, -76.77, 12.0, 93323)
        z2, _ = hwm14_vectorized(300.0, -11.95, -76.77, 12.0, 93323, ap=[-1, 35])
        assert pytest.approx(float(z1), rel=1e-9) == float(z2)

    def test_vectorized_broadcast(self) -> None:
        """Scalar broadcast: one alt, many lats."""
        glat = np.array([-10.0, 0.0, 10.0])
        z, m = hwm14_vectorized(300.0, glat, -76.77, 12.0, 93323)
        assert z.shape == (3,) and m.shape == (3,)


class TestDataPathConfiguration:
    """
    Test data path is properly configured.
    """

    def test_hwmpath_is_set(self) -> None:
        """
        Test that HWMPATH is correctly configured.
        """
        import os

        from pyhwm2014 import HWMPATH

        assert HWMPATH is not None
        assert os.path.exists(HWMPATH) or "HWMPATH" in os.environ
