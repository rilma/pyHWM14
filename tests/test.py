#!/usr/bin/env python
from numpy.testing import run_module_suite,assert_array_almost_equal
from pyhwm2014 import HWM14

def test_hwm14():
    # Single Height profile
    h = HWM14( altlim=[90,200], altstp=1, ap=[-1, 35], day=323,
        option=1, ut=11.66667, verbose=False, year=1993 )

    assert_array_almost_equal([h.Uwind[92],h.Vwind[92]],
                              [-16.502953,-39.811909])


if __name__ == '__main__':
    run_module_suite()
