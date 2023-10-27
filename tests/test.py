from unittest import TestCase
from pyhwm2014 import HWM14

class Test(TestCase):
    def test_hwm14(self):
        h = HWM14( altlim=[90,200], altstp=1, ap=[-1, 35], day=323,
            option=1, ut=11.66667, verbose=False, year=1993 )
        self.assertAlmostEqual(h.Uwind[92], -16.502953, places=3)
        self.assertAlmostEqual(h.Vwind[92], -39.811909, places=3)