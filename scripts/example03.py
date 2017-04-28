#!/usr/bin/env python
from pyhwm2014 import HWM14, HWM14Plot

def example03():


    # Single GMT profile
    hwm14Obj = HWM14( alt=130., ap=[-1, 35], day=323,
        option=3, utlim=[0., 23.45], utstp=.25, verbose=False, year=1993 )

    # GMT profile plot
    hwm14Gbj = HWM14Plot( profObj=hwm14Obj )


example03()
