#!/usr/bin/env python
from pyhwm2014 import HWM14, HWM14Plot

def example01():
    # Single Height profile
    hwm14Obj = HWM14( altlim=[90,200], altstp=1, ap=[-1, 35], day=323,
        option=1, ut=11.66667, verbose=False, year=1993 )

    # Height profile plot
    hwm14Gbj = HWM14Plot( profObj=hwm14Obj )


example01()
