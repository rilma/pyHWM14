"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def hwm14_simple_height_profile():
    """Fixture providing a simple height profile HWM14 calculation."""
    from pyhwm2014 import HWM14

    return HWM14(
        altlim=[90, 150],
        altstp=5,
        ap=[-1, 35],
        day=323,
        option=1,
        ut=11.66667,
        verbose=False,
        year=1993,
    )


@pytest.fixture
def hwm14_latitude_profile():
    """Fixture providing a latitude profile HWM14 calculation."""
    from pyhwm2014 import HWM14

    return HWM14(
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


@pytest.fixture
def hwm142d_2d_height_vs_time():
    """Fixture providing a 2D height vs time calculation."""
    from pyhwm2014 import HWM142D

    return HWM142D(
        altlim=[100, 150],
        altstp=10,
        glat=-11.95,
        glon=-76.77,
        option=1,
        utlim=[0, 12],
        utstp=3,
        verbose=False,
        year=1993,
    )
